import csv
import glob
import json
import re
from pathlib import Path

ROOT = Path("PsiDefender/docs")
DUMP_GLOB = str(ROOT / "fusiongirl_dump" / "batch_*.json")
OUT_CLASS_JSON = ROOT / "fusiongirl_second_pass_classification.json"
OUT_PACK_MD = ROOT / "fusiongirl_second_pass_engineering_pack.md"
OUT_SHORTLIST_CSV = ROOT / "fusiongirl_second_pass_shortlist.csv"
FOCUSED_PAGES_JSON = ROOT / "fusiongirl_psi_engineering_pages.json"

real_world_terms = {
    "signal": 2,
    "sensor": 3,
    "rf": 2,
    "sdr": 3,
    "dsp": 3,
    "acoustic": 2,
    "frequency": 2,
    "fft": 3,
    "electromagnetic": 2,
    "electromagnetism": 2,
    "mhd": 3,
    "magnetohydrodynamic": 4,
    "shielding": 2,
    "current": 1,
    "voltage": 1,
    "power": 1,
    "materials": 1,
    "equation": 1,
    "formula": 1,
    "algorithm": 2,
    "transistor": 3,
    "microcontroller": 3,
    "noise cancellation": 3,
    "quantum": 2,
    "experiment": 2,
    "evidence": 2,
    "measurement": 2,
    "protocol": 2,
    "field": 1,
    "energy density": 2,
    "derivation": 2,
    "microtubules": 3,
    "biophoton": 3,
    "superradiance": 3,
    "neuron": 2,
    "glia": 2,
    "electrical": 2,
    "magnetic": 2,
}

speculative_terms = {
    "psionic": 4,
    "psionics": 4,
    "psi": 2,
    "telepathy": 4,
    "telekinesis": 4,
    "consciousness field": 4,
    "scalar wave": 4,
    "non-hertzian": 4,
    "gravitomagnetic": 4,
    "electrogravitic": 4,
    "magnetogravitic": 4,
    "zero-point": 3,
    "zpe": 3,
    "heim theory": 4,
    "woodward": 3,
    "pais": 3,
    "morphic": 3,
    "universal language": 2,
    "cosmic cypher": 2,
}

lore_terms = {
    "natra": 3,
    "fusion girl": 3,
    "tho'ra": 3,
    "earth alliance": 2,
    "draken": 3,
    "nefarium": 3,
    "timeline": 2,
    "solar cycle": 2,
    "canorbius": 3,
    "faction": 2,
    "clan": 2,
    "character": 2,
    "saga": 2,
    "lore": 2,
    "gameplay": 2,
}


def score_text(text: str, weighted_terms: dict[str, int]) -> int:
    s = 0
    for term, weight in weighted_terms.items():
        count = len(re.findall(r"\b" + re.escape(term) + r"\b", text))
        s += count * weight
    return s


def classify_page(title: str, text: str) -> tuple[str, dict[str, int], str, float]:
    full = f"{title}\n{text}".lower()
    rw = score_text(full, real_world_terms)
    sp = score_text(full, speculative_terms)
    lr = score_text(full, lore_terms)

    # Bonus if citations / references suggest real-world anchoring.
    if rw > 0 and ("<ref" in text.lower() or "doi:" in text.lower() or "phys. rev" in text.lower()):
        rw += 5

    # De-prioritize astronomy transit spam from engineering perspective.
    if "astro events" in title.lower() or "planetary transits" in title.lower():
        lr += 8

    scores = {
        "testable_real_world_engineering": rw,
        "speculative_hypotheses": sp,
        "lore_only": lr,
    }

    # Conservative labeling for low-signal pages.
    if max(scores.values()) == 0:
        label = "lore_only"
    elif sp >= max(rw + 2, 4) and sp >= lr + 1:
        label = "speculative_hypotheses"
    elif rw >= max(sp + 2, 3) and rw >= lr:
        label = "testable_real_world_engineering"
    elif lr >= max(rw, sp):
        label = "lore_only"
    else:
        label = max(scores, key=scores.get)

    # Confidence from score margin.
    sorted_scores = sorted(scores.values(), reverse=True)
    top = sorted_scores[0]
    second = sorted_scores[1]
    confidence = 0.5 if top == 0 else min(0.99, 0.55 + (top - second) / max(10, top + second))

    rationale = (
        "Contains operational engineering language and/or cited physics references"
        if label == "testable_real_world_engineering"
        else "Contains concepts that may inspire hypotheses but are not established"
        if label == "speculative_hypotheses"
        else "Primarily narrative/worldbuilding context"
    )

    return label, scores, rationale, round(confidence, 2)


def classify_focused_page(title: str, text: str) -> tuple[str, dict[str, int], str, float]:
    full = f"{title}\n{text}".lower()
    rw = score_text(full, real_world_terms)
    sp = score_text(full, speculative_terms)
    lr = score_text(full, lore_terms)

    has_citation = "<ref" in text.lower() or "doi:" in text.lower() or "phys. rev" in text.lower()
    if rw > 0 and has_citation:
        rw += 5

    if rw >= 8 and (rw >= sp * 0.35 or has_citation):
        label = "testable_real_world_engineering"
        rationale = "Focused page with concrete technical language and/or cited scientific references"
    else:
        label = "speculative_hypotheses"
        rationale = "Focused page is hypothesis-rich but lacks enough engineering anchoring"

    scores = {
        "testable_real_world_engineering": rw,
        "speculative_hypotheses": sp,
        "lore_only": lr,
    }
    confidence = 0.65 if rw == sp else min(0.99, 0.6 + abs(rw - sp) / max(10, rw + sp + 1))
    return label, scores, rationale, round(confidence, 2)


def extract_categories(text: str) -> list[str]:
    return re.findall(r"\[\[Category:([^\]]+)\]\]", text)


def top_entries(items: list[dict], label: str, n: int = 40) -> list[dict]:
    filtered = [x for x in items if x["classification"] == label]
    filtered.sort(key=lambda x: (x["scores"][label], x["confidence"], x["length"], x["title"].lower()), reverse=True)
    return filtered[:n]


def mk_link(title: str) -> str:
    return "https://wiki.fusiongirl.app/index.php?title=" + title.replace(" ", "_")


def main():
    focused_titles = set()
    if FOCUSED_PAGES_JSON.exists():
        focused_payload = json.loads(FOCUSED_PAGES_JSON.read_text(encoding="utf-8"))
        focused_titles = {p.get("title", "") for p in focused_payload.get("pages", []) if p.get("title")}

    items = []
    total_pages = 0
    for batch in sorted(glob.glob(DUMP_GLOB)):
        data = json.loads(Path(batch).read_text(encoding="utf-8"))
        for page in data:
            total_pages += 1
            title = page.get("title", "")
            text = page.get("wikitext", "")
            if title in focused_titles:
                classification, scores, rationale, confidence = classify_focused_page(title, text)
            else:
                classification = "lore_only"
                scores = {
                    "testable_real_world_engineering": 0,
                    "speculative_hypotheses": 0,
                    "lore_only": 1,
                }
                rationale = "Outside focused psionics/engineering subset; treated as narrative/context"
                confidence = 0.95
            items.append(
                {
                    "title": title,
                    "url": mk_link(title),
                    "timestamp": page.get("timestamp"),
                    "length": len(text),
                    "classification": classification,
                    "scores": scores,
                    "confidence": confidence,
                    "rationale": rationale,
                    "categories": extract_categories(text),
                }
            )

    counts = {
        "testable_real_world_engineering": sum(1 for x in items if x["classification"] == "testable_real_world_engineering"),
        "speculative_hypotheses": sum(1 for x in items if x["classification"] == "speculative_hypotheses"),
        "lore_only": sum(1 for x in items if x["classification"] == "lore_only"),
    }

    payload = {
        "total_pages_processed": total_pages,
        "classification_counts": counts,
        "method": {
            "note": "Heuristic text classification based on weighted terminology and citation hints.",
            "classes": [
                "testable_real_world_engineering",
                "speculative_hypotheses",
                "lore_only",
            ],
        },
        "items": items,
    }
    OUT_CLASS_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    # Shortlist CSV for quick filtering and human review.
    shortlist = (
        top_entries(items, "testable_real_world_engineering", 80)
        + top_entries(items, "speculative_hypotheses", 80)
        + top_entries(items, "lore_only", 40)
    )
    with OUT_SHORTLIST_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["title", "classification", "confidence", "score_real_world", "score_speculative", "score_lore", "url"])
        for x in shortlist:
            w.writerow(
                [
                    x["title"],
                    x["classification"],
                    x["confidence"],
                    x["scores"]["testable_real_world_engineering"],
                    x["scores"]["speculative_hypotheses"],
                    x["scores"]["lore_only"],
                    x["url"],
                ]
            )

    # Build markdown action pack.
    rw_top = top_entries(items, "testable_real_world_engineering", 25)
    sp_top = top_entries(items, "speculative_hypotheses", 25)
    lr_top = top_entries(items, "lore_only", 15)

    md = []
    md.append("# Psi Defender Second-Pass Engineering Pack")
    md.append("")
    md.append("This second pass separates extracted wiki content into three evidence buckets and defines immediate Tech Lab experiments with safety gates.")
    md.append("")
    md.append("## 1) Classification Snapshot")
    md.append(f"- Total pages processed: {total_pages}")
    md.append(f"- Testable real-world engineering: {counts['testable_real_world_engineering']}")
    md.append(f"- Speculative hypotheses: {counts['speculative_hypotheses']}")
    md.append(f"- Lore-only: {counts['lore_only']}")
    md.append("")

    md.append("## 2) Highest-Signal Testable Engineering Sources")
    md.append("Use these for implementation-first workstreams:")
    for x in rw_top:
        md.append(f"- {x['title']} (confidence {x['confidence']}) -> {x['url']}")
    md.append("")

    md.append("## 3) Highest-Signal Speculative Sources")
    md.append("Use these as hypothesis inputs only; require falsifiable test plans:")
    for x in sp_top:
        md.append(f"- {x['title']} (confidence {x['confidence']}) -> {x['url']}")
    md.append("")

    md.append("## 4) Lore-Only Sources")
    md.append("Use these for naming, narrative framing, and design language, not engineering requirements:")
    for x in lr_top:
        md.append(f"- {x['title']} (confidence {x['confidence']}) -> {x['url']}")
    md.append("")

    md.append("## 5) Immediate Tech Lab Experiments (Safety-Gated)")
    md.append("Each experiment has a measurable output and a hard stop condition.")
    md.append("")

    md.append("### Experiment A: RF Shielding Layer Benchmark")
    md.append("- Objective: Quantify shielding effectiveness in dB across selected frequency bands.")
    md.append("- Protocol baseline: experiments/rf_shielding_tests/test_protocol.md")
    md.append("- Output: Update experiments/rf_shielding_tests/test_data.csv with per-layer and stacked-layer results.")
    md.append("- Safety gate: RF power capped to low-power bench levels; stop on unexpected heating or device instability.")
    md.append("")

    md.append("### Experiment B: Acoustic Layer Transfer Function")
    md.append("- Objective: Measure attenuation vs frequency for foam, MLV, and composite stacks.")
    md.append("- Protocol baseline: experiments/acoustic_tests/test_methodology.md")
    md.append("- Output: Update experiments/acoustic_tests/test_results.csv with baseline and attenuated dB values.")
    md.append("- Safety gate: hearing protection mandatory for high SPL tests; stop if discomfort appears.")
    md.append("")

    md.append("### Experiment C: Real-Time FFT Survey for Environmental Interference")
    md.append("- Objective: Build a repeatable interference profile in your Tech Lab using time-series FFT snapshots.")
    md.append("- Script baseline: software/dsp_module/frequency_analysis_script.py")
    md.append("- Output: Store file_analysis_results.csv snapshots and compare dominant peaks by time window.")
    md.append("- Safety gate: no ultrasonic/high-SPL emissions during occupied lab periods.")
    md.append("")

    md.append("### Experiment D: Narrow-Band Noise Cancellation Characterization")
    md.append("- Objective: Validate notch filter depth and collateral distortion around target frequencies.")
    md.append("- Script baseline: software/dsp_module/noise_cancellation_code.py")
    md.append("- Output: Capture cancellation_log.csv and compute attenuation at target +/- bandwidth.")
    md.append("- Safety gate: start low gain; stop if clipping/feedback oscillation occurs.")
    md.append("")

    md.append("### Experiment E: Passive Magnet Layout A/B Test")
    md.append("- Objective: Compare static magnet ring configurations for repeatable sensor-side effects (if any) rather than subjective perception.")
    md.append("- Build baseline: docs/quick_start_build.md")
    md.append("- Output: Structured A/B measurements with identical geometry except magnet arrangement.")
    md.append("- Safety gate: magnet handling controls from docs/safety_guidelines.md; keep away from storage media and medical implants.")
    md.append("")

    md.append("### Experiment F: Reproducibility Run (Cross-Day Repeatability)")
    md.append("- Objective: Ensure effects observed in A-E are repeatable over multiple days and not one-off artifacts.")
    md.append("- Method: Repeat each test at least three times under logged environmental conditions.")
    md.append("- Output: Mean, standard deviation, and confidence interval for each metric.")
    md.append("- Safety gate: abort run on any equipment fault or uncontrolled temperature rise.")
    md.append("")

    md.append("## 6) Decision Rule for What Goes Into Psi Defender v1")
    md.append("Promote an idea from hypothesis to build candidate only if all are true:")
    md.append("- Measurable metric exists and is logged.")
    md.append("- At least 3 independent repeats show similar effect size.")
    md.append("- Confounders are documented and bounded.")
    md.append("- Safety and legal constraints are satisfied.")
    md.append("")

    md.append("## 7) Files Generated by This Pass")
    md.append(f"- {OUT_CLASS_JSON}")
    md.append(f"- {OUT_SHORTLIST_CSV}")
    md.append(f"- {OUT_PACK_MD}")

    OUT_PACK_MD.write_text("\n".join(md), encoding="utf-8")

    print(f"Wrote {OUT_CLASS_JSON}")
    print(f"Wrote {OUT_SHORTLIST_CSV}")
    print(f"Wrote {OUT_PACK_MD}")
    print("Counts:", counts)


if __name__ == "__main__":
    main()
