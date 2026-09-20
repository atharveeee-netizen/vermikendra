# Vermikendra: Failure Modes and Effects Analysis (FMEA)

This document dictates how the Vermikendra system degrades gracefully in the presence of physical and electronic failures. In an offline agricultural setting, failure is guaranteed.

## 1. Hardware Failures

### 1.1 Sensor Corrosion (DS18B20 / SCD41)
*   **Mode:** Acidic compost environment physically corrodes a wire, severing the I2C or 1-Wire connection.
*   **Effect:** Sensor returns hardware errors (e.g., `-127C` or `timeout`).
*   **Mitigation:** The `sensors.cpp` firmware explicitly checks for these errors and overwrites the payload with `0x8000`. The `vk_ingest.py` daemon explicitly casts `0x8000` to a Python `None` (SQL `NULL`).
*   **Result:** The analytics engine ignores the null probe and calculates the regression on the remaining functional probes, preventing skewed analytics.

### 1.2 Radio Link Severance
*   **Mode:** RAK4631 antenna breaks, or Gateway Raspberry Pi shuts down.
*   **Effect:** Edge Node transmits LoRa packets into the void.
*   **Mitigation:** The edge node executes a standalone fail-safe in `main.cpp`. If local thermal arrays exceed `33.0C`, the Edge node *directly* triggers its own misting pump relay without waiting for Gateway authorization.
*   **Result:** The compost pile is saved from thermal cascade, even if the central brain is dead.

## 2. Gateway Failures

### 2.1 Power Loss During Write
*   **Mode:** The Raspberry Pi CM4 loses DC power precisely as `vk_ingest.py` is executing an `INSERT` statement.
*   **Effect:** Potential database corruption.
*   **Mitigation:** `schema.sql` explicitly enforces `PRAGMA journal_mode=WAL;`. 
*   **Result:** The SQLite Write-Ahead Log guarantees atomic consistency upon the next boot.

### 2.2 SD Card Corruption
*   **Mode:** Constant I/O ruins the cheap SD card over 12 months.
*   **Effect:** Complete loss of historical respiration curves.
*   **Mitigation:** (Deferred to V2). A future update should sync the WAL file to an external USB flash drive or periodically backup to an offline phone via the PWA.
