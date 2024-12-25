# RF Shielding Tests: Test Protocol 📡

This document outlines the protocol for testing the **RF (radio frequency) shielding** capabilities of the Psi Defender. These tests are essential for evaluating the effectiveness of conductive materials and configurations in blocking or attenuating electromagnetic waves.

---

## 1. Objectives 🎯

1. Quantify the RF shielding effectiveness (SE) of the Psi Defender's conductive layers.
2. Identify frequency ranges where shielding is most and least effective.
3. Compare performance across different materials and configurations.

---

## 2. Equipment & Setup ⚙️

### Required Equipment
- **RF Signal Generator**  
  *Purpose*: Generate radio frequencies for testing.  
  *Example*: Software-defined radio (SDR) or signal generator device.
  
- **RF Receiver**  
  *Purpose*: Measure the intensity of RF signals.  
  *Example*: SDR dongle (e.g., RTL-SDR) or spectrum analyzer.

- **Shielded Test Chamber** (Optional)  
  *Purpose*: Create a controlled environment to minimize external interference.  

- **Decibel Meter App** (Optional)  
  *Purpose*: Complement SDR measurements for signal intensity readings.

- **Test Materials**  
  - Copper foil tape
  - Aluminum foil
  - Mu-metal sheets
  - Steel mesh or other conductive materials

### Software Tools
- **SDR Software**: Tools like SDRSharp, GQRX, or MATLAB for signal analysis.
- **Data Recording**: Spreadsheet software (e.g., Excel, Google Sheets) for logging results.

---

## 3. Test Procedure 🧪

### 3.1 Baseline Measurement
1. **Setup Signal Generator and Receiver**  
   - Place the RF signal generator at a fixed position in an open environment.  
   - Set the generator to emit a known frequency (e.g., 2.4 GHz, 5 GHz).  

2. **Record Baseline Signal**  
   - Use the RF receiver to measure the signal strength at a fixed distance.  
   - Record the signal strength in decibels (dBm).

3. **Repeat for Multiple Frequencies**  
   - Test across a range of frequencies (e.g., 1 GHz, 2.4 GHz, 5 GHz, 10 GHz).

### 3.2 Shielding Effectiveness Test
1. **Apply Test Material**  
   - Place the shielding material (e.g., copper foil, aluminum foil) between the signal generator and receiver.

2. **Measure Attenuation**  
   - Record the signal strength at the same distance as the baseline test.

3. **Calculate Shielding Effectiveness (SE)**  
   - Use the following formula:  
     $$
     SE = S_{\text{baseline}} - S_{\text{shielded}}
     $$
     Where:
     - $S_{\text{baseline}}$ = Signal strength without shielding (dBm)
     - $S_{\text{shielded}}$ = Signal strength with shielding (dBm)

4. **Repeat for Multiple Materials**  
   - Test copper foil, aluminum foil, mu-metal, and other materials.

5. **Repeat for Layered Configurations**  
   - Combine materials (e.g., copper + steel mesh) and measure their combined effectiveness.

### 3.3 Helmet Configuration Test
1. **Assemble Shielded Helmet**  
   - Incorporate the conductive materials into the helmet design.  

2. **Measure Signal Inside Helmet**  
   - Place the RF receiver inside the helmet and measure the signal strength.

3. **Compare with External Readings**  
   - Compare the internal signal strength to the external signal strength to evaluate shielding effectiveness.

---

## 4. Data Recording 📊

### Data Points
- **Frequency (GHz)**: The frequency of the RF signal.
- **Baseline Signal (dBm)**: Signal strength without shielding.
- **Shielded Signal (dBm)**: Signal strength with shielding applied.
- **Shielding Effectiveness (dB)**: Difference between baseline and shielded signal.

### Example Table
| Frequency (GHz) | Baseline Signal (dBm) | Shielded Signal (dBm) | Shielding Effectiveness (dB) |
|------------------|------------------------|------------------------|------------------------------|
| 2.4              | -20                   | -40                   | 20                           |
| 5.0              | -25                   | -50                   | 25                           |
| 10.0             | -30                   | -55                   | 25                           |

---

## 5. Analysis & Interpretation 📈

1. **Material Comparison**  
   - Identify which materials provide the highest SE across different frequencies.

2. **Frequency Trends**  
   - Determine if the shielding effectiveness varies significantly with frequency.

3. **Layered vs. Single Material**  
   - Assess whether layered configurations outperform single materials.

---

## 6. Safety Precautions ⚠️

1. **Avoid Excessive RF Exposure**  
   - Limit exposure to high-power RF signals during testing.  
   - Ensure the signal generator operates at safe power levels.

2. **Protect Sensitive Equipment**  
   - Avoid exposing the receiver or signal generator to strong magnetic fields or physical impacts.

---

## 7. Next Steps 🚀

1. Use the recorded data to refine material selection and helmet configurations.
2. Share your test results in the [test_data.csv](test_data.csv) file.
3. Experiment with advanced materials like graphene or metamaterials for improved performance.

By following this protocol, you can effectively measure and optimize the RF shielding capabilities of the Psi Defender while contributing valuable data to the community.