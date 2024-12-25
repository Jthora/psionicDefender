# Acoustic Tests: Test Methodology 🔇

This document outlines the methodology for testing the acoustic dampening and noise cancellation capabilities of the Psi Defender. These tests are designed to validate the effectiveness of materials and configurations in blocking, absorbing, or countering sound waves across various frequencies.

---

## 1. Objectives 🎯

1. Measure the effectiveness of acoustic dampening layers (e.g., foam, mass-loaded vinyl).
2. Analyze the impact of different materials on infrasound, audible sound, and ultrasound frequencies.
3. Validate the performance of active noise cancellation (ANC) modules.

---

## 2. Equipment & Setup ⚙️

### Required Equipment
- **Sound source**: A speaker or tone generator capable of emitting frequencies from 10 Hz to 30 kHz.
- **Decibel meter**: To measure sound intensity (dB) before and after the Psi Defender layers are applied.
- **Test enclosure**: A controlled environment, such as a small soundproofed box or quiet room.
- **Microcontroller**: (Optional) For active noise cancellation, use a device like an Arduino Nano or Teensy.
- **Software**: Use audio spectrum analysis tools (e.g., Audacity, MATLAB, or a smartphone decibel meter app).

---

## 3. Test Procedure 🧪

### 3.1 Passive Acoustic Tests
#### Materials:
- Acoustic foam
- Mass-loaded vinyl (MLV)
- Combinations of the above

#### Steps:
1. **Baseline Measurement**  
   - Place the sound source inside the test enclosure.  
   - Emit a tone at a specific frequency (e.g., 100 Hz, 1 kHz, 10 kHz).  
   - Measure the decibel level at a fixed distance outside the enclosure.

2. **Add Dampening Layers**  
   - Apply the acoustic material (foam or MLV) to the interior or exterior of the test enclosure.  
   - Repeat the tone emission and measure the decibel level at the same position.

3. **Record Results**  
   - Note the difference in decibel levels before and after applying the material.  
   - Repeat for a range of frequencies (e.g., 10 Hz, 100 Hz, 1 kHz, 10 kHz, 20 kHz).

### 3.2 Active Noise Cancellation (ANC) Tests
#### Materials:
- Piezoelectric sensors
- Microcontroller (e.g., Arduino Nano, Teensy)
- Small transducers or speakers for counter-phase output

#### Steps:
1. **Set Up the ANC System**  
   - Connect the piezoelectric sensors to the microcontroller to detect incoming sound waves.  
   - Program the microcontroller to generate a counter-phase waveform through the speakers.

2. **Baseline Measurement**  
   - Emit a test tone at a specific frequency and measure the decibel level outside the enclosure.

3. **Activate ANC**  
   - Enable the ANC system and measure the decibel level again.  
   - Compare the results with and without ANC enabled.

4. **Repeat Across Frequencies**  
   - Test the system with various frequencies (e.g., 100 Hz, 1 kHz, 10 kHz) and record the data.

---

## 4. Data Recording 📊

### Data Points
- **Frequency (Hz):** The frequency of the emitted sound.
- **Baseline dB:** Decibel level without any dampening or ANC.
- **Dampened dB:** Decibel level with acoustic materials applied.
- **ANC dB:** Decibel level with active noise cancellation enabled.
- **Reduction (dB):** The difference in decibel levels before and after applying dampening or ANC.

### Example Table
| Frequency (Hz) | Baseline dB | Dampened dB | ANC dB | Reduction (dB) |
|----------------|-------------|-------------|--------|----------------|
| 100            | 75          | 65          | 60     | 15             |
| 1000           | 85          | 70          | 65     | 20             |
| 10000          | 90          | 75          | 70     | 20             |

---

## 5. Analysis & Interpretation 📈

1. **Effectiveness of Materials**  
   - Determine which materials provide the most significant reduction in decibel levels across different frequencies.

2. **ANC Performance**  
   - Assess the ability of the ANC system to cancel specific frequencies.  
   - Identify any limitations in the system's range or responsiveness.

3. **Optimization**  
   - Use the results to refine material selection and ANC system configurations.

---

## 6. Safety Precautions ⚠️

1. **Hearing Protection**  
   - Avoid prolonged exposure to high-decibel sounds during testing.  
   - Use ear protection if necessary.

2. **Equipment Handling**  
   - Ensure all electronic components are powered off before adjustments.  
   - Keep sensitive equipment (e.g., piezo sensors) free from physical damage.

---

## 7. Next Steps 🚀

1. Use the recorded data to update the Psi Defender's material and module configurations.
2. Share your test results with the community in the [test_results.csv](test_results.csv) file.
3. Conduct further tests to explore advanced materials or frequency ranges.

---

By following this methodology, you can validate and improve the acoustic defense capabilities of the Psi Defender while contributing valuable data to the project.