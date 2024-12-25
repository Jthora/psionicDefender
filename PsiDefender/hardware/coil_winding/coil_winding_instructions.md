# Coil Winding Instructions 🌀

This document provides step-by-step instructions for creating electromagnetic coils used in the **Psi Defender**. Coils play a critical role in active jamming, RF signal disruption, and enhancing magnetic shielding.

---

## 1. Objectives 🎯

1. Create electromagnetic coils with precise specifications for active countermeasures.
2. Ensure consistent and repeatable winding for optimal performance.
3. Minimize electrical resistance and maintain structural integrity.

---

## 2. Materials & Tools 🛠️

### Required Materials
- **Copper wire**: 22–28 AWG enamel-coated wire.
- **Spool**: Empty spool or cylindrical core (e.g., PVC pipe, 3D-printed core).
- **Insulation tape**: For securing the wire layers.
- **Heat shrink tubing**: For insulating wire ends.
- **Adhesive (optional)**: Hot glue or epoxy for stabilizing the coil.

### Required Tools
- **Wire strippers**: To remove insulation from wire ends.
- **Multimeter**: To test continuity and measure resistance.
- **Drill with a spool attachment (optional)**: For faster winding.
- **Soldering iron**: To attach the coil ends to terminals or connectors.

---

## 3. Coil Design Specifications ⚙️

### Parameters to Define
1. **Number of turns (N):** Total loops of wire.
2. **Wire gauge (AWG):** Determines resistance and current capacity.
3. **Coil diameter (D):** Diameter of the core around which the wire is wound.
4. **Inductance (L):** Target inductance value in microhenries ($\mu H$).

### Example:
- **Core Diameter (D):** 5 cm
- **Wire Gauge:** 26 AWG
- **Turns (N):** 200
- **Target Inductance (L):** 100 $\mu H$

Use the following formula to estimate inductance:
$$
L = \\frac{N^2 \\cdot \\mu \\cdot A}{l}
$$
Where:
- $N$ = Number of turns
- $\\mu$ = Permeability of core material
- $A$ = Cross-sectional area of the coil
- $l$ = Length of the coil

---

## 4. Step-by-Step Instructions 🧪

### Step 1: Prepare the Core
1. Select a suitable core material:
   - **Air core** for minimal interference.
   - **Ferrite core** for enhanced inductance.
2. Cut the core to the desired length (e.g., 10 cm for a compact coil).

---

### Step 2: Start the Winding
1. Secure one end of the copper wire to the core or spool using tape or adhesive.
2. Begin winding the wire **tightly and evenly** around the core:
   - Maintain consistent tension to avoid loose loops.
   - Ensure each turn is placed closely without overlapping.

---

### Step 3: Layer the Coil
1. Once the first layer is complete, secure it with insulation tape.
2. Begin winding the second layer directly on top of the first, in the **same direction**.
3. Repeat until the desired number of turns is reached.

---

### Step 4: Secure the Coil
1. Use insulation tape or adhesive to secure the final layer of the coil.
2. Strip the insulation from the wire ends (approximately 1 cm) using wire strippers.
3. (Optional) Apply heat shrink tubing to the ends for additional insulation.

---

### Step 5: Test the Coil
1. Use a multimeter to check the continuity of the coil:
   - Place probes on each end of the wire.
   - Ensure the resistance is within the expected range for your wire gauge and length.
2. Calculate the inductance using an LCR meter if available.

---

## 5. Mounting the Coil ⚡

1. Place the completed coil in its designated position on the Psi Defender:
   - Example: Side-mounted for field disruption.
2. Secure the coil with adhesive, brackets, or zip ties.
3. Connect the coil to the circuit:
   - Use a soldering iron to attach the wire ends to terminals or connectors.
   - Ensure proper polarity if required.

---

## 6. Safety Precautions ⚠️

1. **Avoid Overheating**: Do not overheat the wire when soldering to prevent damage to the enamel coating.
2. **Check Insulation**: Ensure no exposed wire is in contact with conductive surfaces to avoid short circuits.
3. **Use Proper Tools**: Handle sharp tools (e.g., wire strippers, scissors) carefully.

---

## 7. Troubleshooting 🔧

| Issue                  | Possible Cause                     | Solution                                |
|------------------------|-------------------------------------|----------------------------------------|
| No continuity          | Broken or loose wire               | Rewind the coil or check connections.  |
| High resistance        | Excessive wire length              | Use thicker wire (lower AWG).          |
| Low inductance         | Insufficient turns or wrong core   | Increase turns or use a ferrite core.  |

---

## 8. Advanced Techniques 🚀

1. **Multi-Layer Coils**  
   - For higher inductance, increase the number of layers, ensuring even winding across all layers.

2. **Helical Coils**  
   - Wind the coil at an angle for specialized electromagnetic fields (e.g., directional jamming).

3. **Cooling Systems**  
   - For high-power applications, integrate cooling mechanisms such as airflow channels or heat sinks.

---

## 9. Conclusion ✨

Follow these instructions to create high-quality coils for your Psi Defender. The performance of your system depends on precise and consistent winding. Share your results and improvements with the community for continued development!

For more technical details, refer to the [coil_diagram.svg](coil_diagram.svg) and [coil_test_results.md](coil_test_results.md).