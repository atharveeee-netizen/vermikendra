import { useState, useEffect, useRef } from 'react';
import { TelemetryContract } from '../types';

const WS_URL = process.env.NEXT_PUBLIC_WS_URL;

export function useTelemetry(nodeId: number | null) {
  const [telemetry, setTelemetry] = useState<TelemetryContract | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const retryCount = useRef(0);
  const maxRetries = 3; // Don't endlessly retry

  useEffect(() => {
    if (nodeId === null) return;
    if (!WS_URL) {
      // No WebSocket URL configured — skip silently (demo mode)
      return;
    }

    let reconnectTimeout: NodeJS.Timeout;
    let isMounted = true;

    const connect = () => {
      if (!isMounted || retryCount.current >= maxRetries) return;

      try {
        wsRef.current = new WebSocket(WS_URL);

        wsRef.current.onopen = () => {
          if (!isMounted) return;
          setIsConnected(true);
          retryCount.current = 0;
        };

        wsRef.current.onmessage = (event) => {
          if (!isMounted) return;
          try {
            const data = JSON.parse(event.data);
            if (data.node === nodeId || data.node_id === nodeId) {
              setTelemetry((prev) => ({
                ...prev,
                ...data,
                ts: data.ts || new Date().toISOString(),
                ambient_c: data.ambient_c ?? prev?.ambient_c,
                probe_1: data.probes_c?.[0] ?? prev?.probe_1,
                co2_ppm: data.co2_ppm ?? prev?.co2_ppm,
                faults: data.faults ?? 0,
              } as TelemetryContract));
            }
          } catch (e) {
            // Silently ignore parse errors
          }
        };

        wsRef.current.onclose = () => {
          if (!isMounted) return;
          setIsConnected(false);
          if (retryCount.current < maxRetries) {
            const delay = Math.min(1000 * Math.pow(2, retryCount.current), 30000);
            retryCount.current += 1;
            reconnectTimeout = setTimeout(connect, delay);
          }
        };

        wsRef.current.onerror = () => {
          // Let onclose handle the reconnect logic
          if (wsRef.current) {
            wsRef.current.close();
          }
        };
      } catch {
        // WebSocket constructor failed — stop trying
        retryCount.current = maxRetries;
      }
    };

    connect();

    return () => {
      isMounted = false;
      clearTimeout(reconnectTimeout);
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [nodeId]);

  return { telemetry, isConnected, setTelemetry };
}
