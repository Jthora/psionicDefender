# Defense Build Path (Inventory-Aware)

## Objective
Build a measurable defensive platform equivalent to a practical "Psi Defender" concept:
- Detect anomalies across RF, magnetic, electric, acoustic, and vibration channels.
- Reduce coupling into the operator system via passive and active hardening.
- Log evidence with reproducible metrics.

## Available inventory integration
- Compute: Jetson Orin AGX, Jetson Nano, Raspberry Pi, Arduino Nano v3.
- Sensing and RF: SDR hardware across multiple bands.
- Materials: copper wire/cable, faraday fabric, neodymium magnets, graphite powder, quartz sand, ferrofluid.
- Fabrication: 3D printer + CNC PCB capability + full electronics tooling.
- Power: 12 V ecosystem, regulators, battery backups.

## Architecture
1. Sensing ring
- Distributed nodes around helmet/disk test article.
- Each node: magnetometer + optional E-field proxy + acoustic/vibration channel.

2. Fusion core
- Jetson Orin AGX aggregates all streams.
- Computes spectral, coherence, and burst metrics.
- Generates risk index and event markers.

3. Shielding stack (passive)
- Outer conductive shell (faraday fabric + copper seam continuity).
- Lossy layer (graphite-loaded composite where practical).
- Mechanical damping layer for low-frequency coupling.

4. System hardening
- Battery-only operation mode.
- Filtered power entry and cable ferrites.
- Minimized loop areas and star-ground discipline.

## Build phases
Phase A: Passive-only validation
- Establish baseline attenuation and noise floor changes.
- Compare open-air vs shielded states.

Phase B: Sensorized defense article
- Add distributed sensing and synchronized logging.
- Validate localization and event confidence metrics.

Phase C: Controlled adaptive response
- Rule-based alerts and operating mode shifts.
- Example: auto-isolate nonessential radios on burst detection.

## Test metrics
- RF attenuation by band (dB).
- Magnetic anomaly rate above baseline (events/hour).
- Acoustic outlier incidence by band.
- False positive rate under known benign environments.
- Repeatability across independent runs.

## Practical notes on specific materials
- Copper and faraday fabric: strong first-line for E-field shielding when seam continuity is maintained.
- Neodymium magnets: useful for mechanical fixtures and some sensor experiments, but not a primary shielding mechanism for broad RF threats.
- Graphite composites: useful as lossy absorbers in certain regimes; characterize empirically.
- Ferrofluid: treat as experimental material, not first-line protective element.
- Quartz sand: useful mechanically/thermally; direct EM shielding role is limited without specific composite design.

## Non-goals in pass 1
- No claims of proving new fundamental scalar physics.
- No body-worn HV experiments.
- No offensive waveform generation.

## Recommended next artifacts
- Schematic set for node hardware.
- BOM with alternates.
- Test script package for SDR and sensor synchronization.
