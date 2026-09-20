# Vermikendra OpenDesign Rules

## 1. Core Principles
- **Offline-First Resilience:** Absolutely no external dependencies. Fonts, icons, and CSS frameworks must be bundled locally. No CDNs.
- **Data Density:** Visualizations (gauges, heatmaps) take priority over text. Must be readable outdoors on a 5-inch screen.
- **Translation:** Must support English, Hindi, and Gujarati (stored locally).

## 2. Threshold Colors
- **vk-good:** `#38a169` (Green) -> 12-30°C / 60-80% Moisture
- **vk-warning:** `#dd6b20` (Orange) -> 30-33°C / 55-60% Moisture
- **vk-critical:** `#e53e3e` (Red) -> >33°C / <55% Moisture

## 3. Component Mandates
- **Thermal Gradient:** A vertical stack of 5 temperature readings mapping to the 5x DS18B20 probes.
- **Respiration Graph:** Time-series of the CO2 ppm/min slope.
- **Readiness:** Based purely on evidence (respiration trend, stability), not a "magical AI score."
