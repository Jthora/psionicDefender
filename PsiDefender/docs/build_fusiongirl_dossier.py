import json
import re
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

API = "https://wiki.fusiongirl.app/api.php"
ROOT = Path("PsiDefender/docs")
INDEX_PATH = ROOT / "fusiongirl_wiki_index.json"
OUT_JSON = ROOT / "fusiongirl_psi_engineering_pages.json"
OUT_MD = ROOT / "fusiongirl_psi_engineering_dossier.md"


def call(params):
    query = urllib.parse.urlencode({**params, "format": "json"})
    url = f"{API}?{query}"
    with urllib.request.urlopen(url, timeout=40) as response:
        return json.loads(response.read().decode("utf-8", errors="replace"))


def main():
    idx = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    titles = [p["title"] for p in idx["all_pages"]]

    pattern = re.compile(
        r"(psi|psionic|psionics|telepathy|telekinesis|consciousness|neural|resonance|field|magnet|shield|sensor|equation|formula|algorithm|physics|engineering|device|hardware|signal|wave)",
        re.IGNORECASE,
    )
    selected = sorted([t for t in titles if pattern.search(t)])

    pages = []
    for i in range(0, len(selected), 20):
        chunk = selected[i : i + 20]
        data = call(
            {
                "action": "query",
                "prop": "revisions|categories|links|info",
                "rvprop": "content|timestamp",
                "rvslots": "main",
                "cllimit": "max",
                "pllimit": "max",
                "inprop": "url",
                "titles": "|".join(chunk),
            }
        )
        for page in data.get("query", {}).get("pages", {}).values():
            revisions = page.get("revisions", [])
            timestamp = ""
            wikitext = ""
            if revisions:
                rev = revisions[0]
                timestamp = rev.get("timestamp", "")
                wikitext = ((rev.get("slots") or {}).get("main") or {}).get("*", "")

            pages.append(
                {
                    "title": page.get("title", ""),
                    "timestamp": timestamp,
                    "fullurl": page.get("fullurl", ""),
                    "length": page.get("length", 0),
                    "categories": [c.get("title", "") for c in page.get("categories", [])],
                    "links": [l.get("title", "") for l in page.get("links", [])],
                    "wikitext": wikitext,
                }
            )

    OUT_JSON.write_text(
        json.dumps({"selected_count": len(selected), "pages": pages}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    md = []
    md.append("# FusionGirl Wiki Psi/Engineering Deep-Dive Dossier")
    md.append("")
    md.append("Generated via MediaWiki API full-title inventory scan (4,457 pages indexed).")
    md.append("")
    md.append(f"- Selected topical pages: {len(selected)}")
    md.append(f"- Snapshot pages fetched: {len(pages)}")
    md.append("")

    cat_counter = Counter()
    for page in pages:
        for cat in page["categories"]:
            cat_counter[cat] += 1

    md.append("## Dominant Categories")
    for cat, count in cat_counter.most_common(50):
        md.append(f"- {cat}: {count}")
    md.append("")

    tech_terms = [
        "equation",
        "formula",
        "algorithm",
        "frequency",
        "resonance",
        "coil",
        "magnet",
        "field",
        "shield",
        "sensor",
        "voltage",
        "current",
        "power",
        "signal",
        "wave",
        "neural",
        "hardware",
        "device",
        "prototype",
        "build",
        "materials",
        "safety",
    ]

    for page in sorted(pages, key=lambda x: x["title"].lower()):
        text = page["wikitext"] or ""
        lower_text = text.lower()
        hits = [term for term in tech_terms if term in lower_text]
        if not hits and len(text.strip()) < 50:
            continue

        headings = re.findall(r"^==+\s*(.*?)\s*==+", text, flags=re.MULTILINE)
        lines = [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.strip().startswith("[[")]
        snippet = " ".join(lines[:3])[:400]

        md.append(f"## {page['title']}")
        md.append(f"- URL: {page['fullurl']}")
        md.append(f"- Updated: {page['timestamp']}")
        md.append(f"- Page length: {page['length']}")
        if headings:
            md.append(f"- Key sections: {', '.join(headings[:10])}")
        if hits:
            md.append(f"- Technical term hits: {', '.join(hits)}")
        if page["categories"]:
            md.append(f"- Categories: {', '.join(page['categories'][:10])}")
        if snippet:
            md.append(f"- Abstract snippet: {snippet}")
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")

    print(f"selected_titles={len(selected)}")
    print(f"pages_fetched={len(pages)}")
    print(f"wrote={OUT_JSON}")
    print(f"wrote={OUT_MD}")


if __name__ == "__main__":
    main()
