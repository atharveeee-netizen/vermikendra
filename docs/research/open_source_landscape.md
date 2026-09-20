# Open Source Landscape

## 1. Firmware Libraries
| Library | Source | License | Relevance | Integration Risk |
| :--- | :--- | :--- | :--- | :--- |
| **RadioLib** | jgromes/RadioLib | MIT | Primary SX1262 driver for RAK4631 P2P mode. | Low |
| **DallasTemperature** | milesburton | LGPL | 1-Wire DS18B20 handling. | Low |
| **Sensirion I2C SCD4x** | Sensirion | BSD | CO2 sensor driver. | Low |
| **BSEC2 Software** | Bosch Sensortec | Proprietary (Free) | Required for BME688 gas calculations. | High (precompiled binaries) |
| **Adafruit_LIS3DH** | Adafruit | BSD | Tilt interrupt handling. | Low |

## 2. Gateway Libraries
| Library | Source | License | Relevance | Integration Risk |
| :--- | :--- | :--- | :--- | :--- |
| **Paho-MQTT** | Eclipse | EDL/EPL | Python MQTT client for `vk-radio` to `vk-ingest`. | Low |
| **FastAPI** | tiangolo | MIT | Async web framework for `vk-api`. | Low |
| **SciPy/NumPy** | SciPy | BSD | Linear regression for respiration slope (`vk-engine`). | Low |

## 3. Dashboard Frameworks
| Library | Source | License | Relevance | Integration Risk |
| :--- | :--- | :--- | :--- | :--- |
| **Next.js** | Vercel | MIT | Offline PWA generation. | Low |
| **uPlot** | leeoniya | MIT | High-performance, low-memory time-series charting. | Low |

**License Review:** All selected open-source components use MIT, BSD, or LGPL licenses, which permit closed-source dynamic linking and distribution in an embedded context without forcing the entire Vermikendra repository to become GPL open-source.
