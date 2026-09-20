# Vermikendra Data Schemas

## 1. LoRa Packets (Little-Endian)
**Type 0x01 (Periodic Reading, 44 bytes):**
- `uint8` version_type
- `uint16` node_id, `uint16` seq
- `uint8` flags, `uint16` age_s, `uint16` batt_mv
- `int16[5]` t_probe (0.01 °C)
- `int16` t_ambient, `uint16` rh, `uint16` pressure
- `uint32` gas_res, `uint16` moisture_raw, `int32` mass
- `uint16` co2_last, `uint8` fault_bits, `int8` rssi_last_ack
- `bytes[4]` HMAC tag

**Type 0x02 (Respiration Result, 28 bytes):**
- header (6b), `uint16` age_s, `int16` slope (0.1 ppm/min)
- `uint16` r2, `uint8` n_points, `uint16` co2_start, `uint16` co2_end
- `int16` t_bed_mean, `int32` mass, `uint8` resp_flags
- `bytes[4]` HMAC tag

## 2. SQLite Tables (WAL Mode)
- **`nodes`:** `id`, `bin_id`, `key_id`, `firmware_version`, `last_seen`, `battery_mv`
- **`readings`:** `node_id`, `ts`, `seq`, `probe_1` to `probe_5`, `ambient`, `rh`, `pressure`, `gas_ohm`, `moisture_raw`, `moisture_pct`, `mass_g`, `co2_ppm`, `battery_mv`, `rssi`, `snr`, `flags`, `faults`
- **`respiration_runs`:** `id`, `bin_id`, `ts_start`, `slope_ppm_min`, `r2`, `n_points`, `index_value`, `bed_temp_c`, `valid`
- **`events`:** `id`, `bin_id`, `ts`, `type`, `mass_before_g`, `mass_after_g`, `delta_g`
