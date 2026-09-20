# Analytics & Time-Series Methods

## 1. Deterministic Respiration Slope (vk-engine)
Instead of deep learning, we use a robust linear regression model (Ordinary Least Squares) over the measurement window (600 seconds).
- **Quality Control:** Reject the first 60 seconds of data (flushing turbulence). Reject runs with `n_points < 20`.
- **Fit:** $C(t) = a + st$, where $s$ is the slope in ppm/minute.
- **Validity:** R² must be $\geq 0.90$. If $R^2 < 0.90$, the measurement is discarded as noisy (likely due to wind or lid opening).

## 2. Heat-Risk Forecast
Predicting lethal thermal events before they occur.
- **Method:** Rolling 30-minute linear regression for each of the 5 DS18B20 probes.
- **Thresholds:** If current temp $T \geq 33^\circ C$, trigger immediate `CRITICAL` alert.
- **Forecast:** If slope $s > 0.3^\circ C/hr$, calculate $t_{cross} = (33 - T)/s$. If $t_{cross} \leq 2$ hours, trigger `HEAT_FORECAST` alert.

## 3. Wetness Index Mapping
Moisture sensors return raw millivolts.
- Calculate Wetness Index: $W = (V_{dry} - V_{raw}) / (V_{dry} - V_{wet})$.
- This normalizes sensor drift across different units.

## 4. Event Detection
- **Lid Tilt:** Hardware interrupt from LIS3DH accelerometer (triggering immediately on > 30° tilt).
- **Mass Change:** Evaluated after the lid closes. If $\Delta mass > 2kg$, flag as a "Feeding" or "Harvesting" event.
