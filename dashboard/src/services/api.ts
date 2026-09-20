import { Site, Bin, Node, TelemetryContract } from '../types';

// Use environment variable if deployed to cloud, fallback to local network origin
const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL;

export async function fetchSites(): Promise<Site[]> {
  const res = await fetch(`${API_BASE}/sites`);
  if (!res.ok) throw new Error("Failed to fetch sites");
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
