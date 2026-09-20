import { useState, useEffect, useRef } from 'react';
import { TelemetryContract } from '../types';

const WS_URL = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000/ws/telemetry";

export function useTelemetry(nodeId: number | null) {
  const [telemetry, setTelemetry] = useState<TelemetryContract | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const retryCount = useRef(0);

  useEffect(() => {
    if (nodeId === null) return;

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
