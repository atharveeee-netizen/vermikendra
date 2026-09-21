export interface Site {
  id: string;
  name: string;
  location: string | null;
}

export interface Field {
  id: string;
  site_id: string;
  name: string;
  boundary: string | null;
}

export interface Bin {
  id: string;
  site_id: string;
  field_id: string | null;
  name: string;
  latitude: number | null;
  longitude: number | null;
}

export interface Node {
  id: number;
  bin_id: string;
  mac_address: string | null;
  fw_version: string | null;
  last_seen: string | null;
}

export interface TelemetryContract {
  id: number;
  node_id: number;
  ts: string;
  ambient_c: number | null;
  probe_1: number | null;
  probe_2: number | null;
  probe_3: number | null;
  probe_4: number | null;
  probe_5: number | null;
  moisture_raw: number | null;
  co2_ppm: number | null;
  mass_g: number | null;
  battery_mv: number | null;
  faults: number;
  quality: 'VALID' | 'STALE' | 'FAULT' | 'MISSING';
  computed_status?: 'NORMAL' | 'WATCH' | 'ACTION_NEEDED' | 'OFFLINE' | 'SENSOR_FAULT';
  computed_reason?: string;
  mac_address?: string;
  fw_version?: string;
  bin_name?: string;
  field_id?: string;
}

export interface AssistantResponse {
  language: string;
  transcript: string;
  intent: string;
  answer_text: string;
  audio_status: 'ok' | 'unavailable';
  audio_base64?: string;
  status: string;
}

export interface ApiError {
  error: {
    code: string;
    message: string;
    retryable: boolean;
  }
}

export interface FleetNode {
  node_id: number;
  bin_id: string;
  field_id: string | null;
  bin_name: string;
  mac_address: string | null;
  last_seen: string | null;
  latest_telemetry: TelemetryContract | null;
  computed_status: 'NORMAL' | 'WATCH' | 'ACTION_NEEDED' | 'OFFLINE' | 'SENSOR_FAULT';
  computed_reason?: string;
}

export interface FleetStats {
  total: number;
  online: number;
  offline: number;
  normal: number;
  attention: number;
  critical: number;
}

export interface FleetData {
  nodes: FleetNode[];
  stats: FleetStats;
}
