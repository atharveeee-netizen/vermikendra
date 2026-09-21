import { Site, Field, Bin, Node, TelemetryContract } from '../types';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL;

export async function fetchSites(): Promise<Site[]> {
  if (!API_BASE) throw new Error("NEXT_PUBLIC_API_BASE_URL is not configured.");
  const res = await fetch(`${API_BASE}/sites`);
  if (!res.ok) throw new Error("Failed to fetch sites");
  return res.json();
}

export async function fetchFields(): Promise<Field[]> {
  const res = await fetch(`${API_BASE}/fields`);
  if (!res.ok) throw new Error("Failed to fetch fields");
  return res.json();
}

export async function fetchBins(siteId: string): Promise<Bin[]> {
  const res = await fetch(`${API_BASE}/sites/${siteId}/bins`);
  if (!res.ok) throw new Error("Failed to fetch bins");
  return res.json();
}

export async function fetchNodes(binId: string): Promise<Node[]> {
  const res = await fetch(`${API_BASE}/bins/${binId}/nodes`);
  if (!res.ok) throw new Error("Failed to fetch nodes");
  return res.json();
}

export async function fetchLatestTelemetry(nodeId: number): Promise<TelemetryContract> {
  const res = await fetch(`${API_BASE}/nodes/${nodeId}/telemetry/latest`);
  if (!res.ok) throw new Error("Failed to fetch telemetry");
  return res.json();
}

export async function fetchSiteFleet(siteId: string): Promise<import('../types').FleetData> {
  const res = await fetch(`${API_BASE}/sites/${siteId}/fleet`);
  if (!res.ok) throw new Error("Failed to fetch fleet data");
  return res.json();
}
