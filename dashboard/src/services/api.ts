import { Site, Field, Bin, TelemetryContract, FleetData, FleetNode, FleetStats } from '../types';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL;

// ──── DEMO DATA ────
// Used as fallback when the real backend is unreachable (e.g., Vercel public deployment)

const DEMO_SITES: Site[] = [
  { id: "site-pune-01", name: "Vermikendra Pune", location: "18.520,73.856" }
];

const DEMO_FIELDS: Field[] = [
  { id: "field-a", site_id: "site-pune-01", name: "Field A – Shade Net", boundary: '{"type":"Polygon","coordinates":[[[73.854,18.521],[73.857,18.521],[73.857,18.519],[73.854,18.519],[73.854,18.521]]]}' },
  { id: "field-b", site_id: "site-pune-01", name: "Field B – Open Sun", boundary: null },
];

const DEMO_BINS: Bin[] = [
  { id: "bin-01", site_id: "site-pune-01", field_id: "field-a", name: "BED-01", latitude: 18.5205, longitude: 73.8550 },
  { id: "bin-02", site_id: "site-pune-01", field_id: "field-a", name: "BED-02", latitude: 18.5200, longitude: 73.8558 },
  { id: "bin-03", site_id: "site-pune-01", field_id: "field-a", name: "BED-03", latitude: 18.5195, longitude: 73.8545 },
  { id: "bin-04", site_id: "site-pune-01", field_id: "field-b", name: "BED-04", latitude: 18.5210, longitude: 73.8570 },
  { id: "bin-05", site_id: "site-pune-01", field_id: "field-b", name: "BED-05", latitude: 18.5215, longitude: 73.8565 },
  { id: "bin-06", site_id: "site-pune-01", field_id: "field-b", name: "BED-06", latitude: 18.5208, longitude: 73.8575 },
];

function makeTelemetry(nodeId: number, status: FleetNode['computed_status'], reason?: string): TelemetryContract {
  const baseTemp = 28 + Math.random() * 6;
  return {
    id: nodeId,
    node_id: nodeId,
    ts: new Date(Date.now() - Math.floor(Math.random() * 120000)).toISOString(),
    ambient_c: parseFloat((baseTemp - 2 + Math.random() * 2).toFixed(1)),
    probe_1: parseFloat((baseTemp - 1).toFixed(1)),
    probe_2: parseFloat((baseTemp + 0.5).toFixed(1)),
    probe_3: parseFloat((baseTemp + 1.2).toFixed(1)),
    probe_4: parseFloat((baseTemp + 2.8).toFixed(1)),
    probe_5: parseFloat((baseTemp + 1.5).toFixed(1)),
    moisture_raw: Math.floor(50 + Math.random() * 20),
    co2_ppm: Math.floor(600 + Math.random() * 600),
    mass_g: Math.floor(500000 + Math.random() * 200000),
    battery_mv: Math.floor(3800 + Math.random() * 300),
    faults: 0,
    quality: 'VALID',
    computed_status: status,
    computed_reason: reason,
    mac_address: `AA:BB:CC:DD:EE:${(10 + nodeId).toString(16).toUpperCase()}`,
    fw_version: "v2.4.1",
    bin_name: DEMO_BINS[nodeId - 1]?.name || `BED-${String(nodeId).padStart(2, '0')}`,
    field_id: DEMO_BINS[nodeId - 1]?.field_id || "field-a",
  };
}

const DEMO_FLEET: FleetData = (() => {
  const nodes: FleetNode[] = [
    { node_id: 1, bin_id: "bin-01", field_id: "field-a", bin_name: "BED-01", mac_address: "AA:BB:CC:DD:EE:0B", last_seen: new Date().toISOString(), latest_telemetry: makeTelemetry(1, 'NORMAL'), computed_status: 'NORMAL', computed_reason: undefined },
    { node_id: 2, bin_id: "bin-02", field_id: "field-a", bin_name: "BED-02", mac_address: "AA:BB:CC:DD:EE:0C", last_seen: new Date().toISOString(), latest_telemetry: makeTelemetry(2, 'NORMAL'), computed_status: 'NORMAL', computed_reason: undefined },
    { node_id: 3, bin_id: "bin-03", field_id: "field-a", bin_name: "BED-03", mac_address: "AA:BB:CC:DD:EE:0D", last_seen: new Date().toISOString(), latest_telemetry: makeTelemetry(3, 'WATCH', 'Core temperature trending high (34.2°C). Monitor for next 2 hours.'), computed_status: 'WATCH', computed_reason: 'Core temperature trending high (34.2°C). Monitor for next 2 hours.' },
    { node_id: 4, bin_id: "bin-04", field_id: "field-b", bin_name: "BED-04", mac_address: "AA:BB:CC:DD:EE:0E", last_seen: new Date().toISOString(), latest_telemetry: makeTelemetry(4, 'NORMAL'), computed_status: 'NORMAL', computed_reason: undefined },
    { node_id: 5, bin_id: "bin-05", field_id: "field-b", bin_name: "BED-05", mac_address: "AA:BB:CC:DD:EE:0F", last_seen: new Date().toISOString(), latest_telemetry: makeTelemetry(5, 'ACTION_NEEDED', 'Moisture dropped below 45%. Immediate watering required.'), computed_status: 'ACTION_NEEDED', computed_reason: 'Moisture dropped below 45%. Immediate watering required.' },
    { node_id: 6, bin_id: "bin-06", field_id: "field-b", bin_name: "BED-06", mac_address: "AA:BB:CC:DD:EE:10", last_seen: new Date(Date.now() - 3600000).toISOString(), latest_telemetry: null, computed_status: 'OFFLINE', computed_reason: 'Node not responding for 60 minutes.' },
  ];
  const stats: FleetStats = {
    total: 6,
    online: 5,
    offline: 1,
    normal: 3,
    attention: 1,
    critical: 1,
  };
  return { nodes, stats };
})();

// ──── SAFE FETCH HELPER ────
async function safeFetch<T>(url: string, fallback: T): Promise<T> {
  if (!API_BASE) return fallback;
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 4000);
    const res = await fetch(url, { signal: controller.signal });
    clearTimeout(timeoutId);
    if (!res.ok) return fallback;
    return res.json();
  } catch {
    return fallback;
  }
}

// ──── PUBLIC API ────

export async function fetchSites(): Promise<Site[]> {
  return safeFetch(`${API_BASE}/sites`, DEMO_SITES);
}

export async function fetchFields(): Promise<Field[]> {
  return safeFetch(`${API_BASE}/fields`, DEMO_FIELDS);
}

export async function fetchBins(siteId: string): Promise<Bin[]> {
  return safeFetch(`${API_BASE}/sites/${siteId}/bins`, DEMO_BINS);
}

export async function fetchNodes(binId: string): Promise<any[]> {
  return safeFetch(`${API_BASE}/bins/${binId}/nodes`, []);
}

export async function fetchLatestTelemetry(nodeId: number): Promise<TelemetryContract> {
  const fallback = makeTelemetry(
    nodeId,
    nodeId === 5 ? 'ACTION_NEEDED' : nodeId === 3 ? 'WATCH' : 'NORMAL',
    nodeId === 5 ? 'Moisture dropped below 45%. Immediate watering required.' : nodeId === 3 ? 'Core temperature trending high (34.2°C).' : undefined
  );
  return safeFetch(`${API_BASE}/nodes/${nodeId}/telemetry/latest`, fallback);
}

export async function fetchSiteFleet(siteId: string): Promise<FleetData> {
  return safeFetch(`${API_BASE}/sites/${siteId}/fleet`, DEMO_FLEET);
}

export function getDemoBins(): Bin[] {
  return DEMO_BINS;
}
