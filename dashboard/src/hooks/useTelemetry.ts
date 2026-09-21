import { useState, useEffect, useRef } from 'react';
import { TelemetryContract } from '../types';

const WS_URL = process.env.NEXT_PUBLIC_WS_URL || "ws://127.0.0.1:8000/ws/telemetry";

export function useTelemetry(nodeId: number | null) {
  const [telemetry, setTelemetry] = useState<TelemetryContract | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const retryCount = useRef(0);

  useEffect(() => {
    if (nodeId === null) return;

    // --- DEMO MODE FOR VERCEL DEPLOYMENTS ---
    if (typeof window !== 'undefined' && window.location.hostname.includes('vercel.app')) {
      setIsConnected(true);
      const interval = setInterval(() => {
        setTelemetry((prev) => {
          const base = prev || { node_id: nodeId, ambient_c: 25, probe_1: 22, co2_ppm: 400, faults: 0, ts: new Date().toISOString() };
          return {
            ...base,
            ambient_c: base.ambient_c! + (Math.random() - 0.5),
            probe_1: base.probe_1! + (Math.random() - 0.2),
            co2_ppm: base.co2_ppm! + (Math.random() * 10 - 5),
            ts: new Date().toISOString()
          } as unknown as TelemetryContract;
        });
      }, 2500);
      return () => clearInterval(interval);
    }
    // ----------------------------------------

    let reconnectTimeout: NodeJS.Timeout;

    const connect = () => {
      wsRef.current = new WebSocket(WS_URL);

      wsRef.current.onopen = () => {
        setIsConnected(true);
        retryCount.current = 0; // reset backoff on success
      };

      wsRef.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          // Phase 12: Ensure it matches the node we are looking at
          if (data.node === nodeId || data.node_id === nodeId) {
            setTelemetry((prev) => ({
              ...prev,
              ...data,
              // Normalize MQTT payload to TelemetryContract if needed
              ts: data.ts || new Date().toISOString(),
              ambient_c: data.ambient_c ?? prev?.ambient_c,
              probe_1: data.probes_c?.[0] ?? prev?.probe_1,
              co2_ppm: data.co2_ppm ?? prev?.co2_ppm,
              faults: data.faults ?? 0,
            } as TelemetryContract));
          }
        } catch (e) {
          console.error("WS Parse Error", e);
        }
      };

      wsRef.current.onclose = () => {
        setIsConnected(false);
        // Phase 13: Exponential Backoff (max 30s)
        const delay = Math.min(1000 * Math.pow(2, retryCount.current), 30000);
        retryCount.current += 1;
        reconnectTimeout = setTimeout(connect, delay);
      };
    };

    connect();

    return () => {
      clearTimeout(reconnectTimeout);
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [nodeId]);

  return { telemetry, isConnected, setTelemetry };
}
