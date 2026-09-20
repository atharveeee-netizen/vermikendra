# Sensor Calibration Methods

## 1. Thermal Probe Array (DS18B20)
DS18B20 sensors have a factory accuracy of ±0.5°C, but gradients require tighter relative precision.
**Method (Three-Point Water Bath):**
1. Submerge all 5 probes + the TMP117 reference sensor in an insulated water bath.
2. Record values at 10°C, 25°C, and 40°C.
3. Fit linear offsets: $T_{cal} = gain \times T_{raw} + offset$.
4. Store these offsets in the gateway SQLite `calibrations` table.

## 2. Capacitive Moisture Sensors
**Method (Gravimetric Mapping):**
1. Measure raw voltage ($V_{dry}$) in completely dry compost bedding.
2. Measure raw voltage ($V_{wet}$) in saturated bedding drained for 10 minutes.
3. Take 5 samples of varying wetness, weigh them, bake them dry, and weigh them again to find exact gravimetric moisture content %.
4. Map the Wetness Index $W$ (from 0 to 1) linearly to the gravimetric %.

## 3. Load Cells (HX711)
**Method (Known Weights):**
1. Tare the empty platform.
2. Place certified 5kg, 10kg, and 20kg weights at the center and all four corners.
3. Adjust the HX711 scale factor until standard deviation across positions is minimized.
