# Hardware Truth Matrix (Syzygy P14)

> [!WARNING]
> This matrix strictly separates simulation from physical proof. Unverified claims remain explicitly untrusted.

| Component | Source Implementation | Firmware Build | Hardware Connected | Physical Measurement | Validated |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **DS18B20** | YES (`ingestion.py`) | COMPILED | UNVERIFIED | UNVERIFIED | NO |
| **SCD41** | YES (`ingestion.py`) | COMPILED | UNVERIFIED | UNVERIFIED | NO |
| **BME688** | YES (`ingestion.py`) | COMPILED | UNVERIFIED | UNVERIFIED | NO |
| **TMP117** | YES (`ingestion.py`) | COMPILED | UNVERIFIED | UNVERIFIED | NO |
| **LIS3DH** | YES (`ingestion.py`) | COMPILED | UNVERIFIED | UNVERIFIED | NO |
| **HX711 (Mass)** | YES (`ingestion.py`) | COMPILED | UNVERIFIED | UNVERIFIED | NO |
| **Battery Level** | YES (`ingestion.py`) | COMPILED | UNVERIFIED | UNVERIFIED | NO |
| **SX1262 (Radio)** | NO | COMPILED | UNVERIFIED | UNVERIFIED | NO |
| **Deep Sleep** | NO | COMPILED | UNVERIFIED | UNVERIFIED | NO |

**Conclusion:** The Python API layer and the Next.js UI are proven. The edge-node firmware successfully cross-compiles for the ARM Cortex-M4F architecture (nRF52) without errors. However, physical hardware execution has not been independently observed.
