# Vermikendra Data Contract

This document acts as the strict canonical schema definition for the Vermikendra project. All firmware, gateway, and analytics code must adhere to these exact definitions.

## 1. Primary Schemas

### `nodes`
Tracks edge hardware.
- `id` (INT): Unique LoRa Node ID.
- `bin_id` (INT): The compost bin assigned to this node.
- `key_id` (TEXT): Reference to the HMAC signing key.
- `firmware_version` (TEXT): Currently running FW version.
- `last_seen` (DATETIME): UTC timestamp of the last valid packet.
- `battery_mv` (INT): Last known battery voltage in mV.

### `telemetry` (Readings)
Preserves raw observations. Never overwrite raw data with smoothed data.
- `node_id` (INT)
- `ts` (DATETIME): UTC arrival time at gateway minus `age_s` from payload.
- `seq` (INT): LoRa packet sequence number.
- `probe_1` to `probe_5` (REAL): Calibrated temperature in °C.
- `ambient` (REAL): Ambient reference temperature in °C.
- `rh` (REAL): Relative humidity %.
- `pressure` (REAL): Barometric pressure in hPa.
- `gas_ohm` (INT): BME688 raw VOC resistance.
- `moisture_raw` (INT): Raw ADC value from capacitive sensor.
- `moisture_pct` (REAL): Calibrated gravimetric moisture %.
- `mass_g` (INT): Raw bed mass in grams.
- `co2_ppm` (INT): Latest NDIR reading.
- `rssi` (INT) / `snr` (REAL): Link quality.

### `respiration_runs`
- `bin_id` (INT)
- `ts_start` (DATETIME)
- `slope_ppm_min` (REAL): First derivative of CO2 accumulation.
- `r2` (REAL): Linearity of fit (must be $\geq 0.90$).
- `n_points` (INT): Data points used in calculation.
- `index_value` (REAL): Mass-normalized respiration index ($mg\ CO_2-C / kg / hr$).
- `valid` (BOOLEAN): False if aborted by lid opening.

### `events`
- `bin_id` (INT)
- `ts` (DATETIME)
- `type` (TEXT): `LID_OPEN`, `LID_CLOSED`, `FEEDING`, `MIST_START`, `MIST_STOP`.
- `mass_before_g` / `mass_after_g` (INT)

### `alerts`
- `bin_id` (INT)
- `ts_open` / `ts_clear` (DATETIME)
- `severity` (TEXT): `WARNING`, `CRITICAL`
- `message_key` (TEXT): For i18n translation (e.g., `alert.heat.forecast`)

### `commands`
- `node_id` (INT)
- `type` (TEXT): `MIST`, `REBOOT`, `CONFIG`
- `argument` (INT): e.g., seconds to run pump.
- `status` (TEXT): `QUEUED`, `ACKED`

### `calibrations`
- `node_id` (INT)
- `sensor` (TEXT): `probe_1`, `moisture_1`
- `parameters` (JSON): e.g., `{"gain": 1.0, "offset": -0.2}`

## 2. Valid Ranges & Units
- **Temperature:** Range $0.00^\circ C$ to $65.00^\circ C$. Stored in LoRa payload as INT16 ($T \times 100$).
- **CO2:** Range $400$ to $5000\ ppm$. Stored as UINT16.
- **Battery:** Range $3000$ to $4200\ mV$. Stored as UINT16.
- **Moisture:** Range $0.0\%$ to $100.0\%$.

## 3. Missing Value & Fault Behavior
- If a sensor fails or is missing, the firmware MUST pack the value `0x8000` (for INT16) or `0xFFFF` (for UINT16) into the LoRa payload.
- The `vk-ingest` gateway service MUST map these exact hex values to SQL `NULL`.
- Analytics must explicitly handle `NULL` values and must NEVER interpolate across a gap larger than 1 hour.

## 4. Schema Migration Strategy
- Production databases follow an **Append-Only** strategy. 
- Schema updates (e.g., adding a new column) are permitted via Alembic or raw `ALTER TABLE ADD COLUMN`.
- Data destruction (dropping tables, deleting raw telemetry columns) is strictly forbidden to preserve scientific records.
