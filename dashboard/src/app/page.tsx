"use client";

import { useEffect, useState, useRef } from "react";
import { fetchSites, fetchBins, fetchNodes, fetchLatestTelemetry } from "../services/api";
import { useTelemetry } from "../hooks/useTelemetry";
import { Site, Bin, Node, AssistantResponse } from "../types";

// Localized strings
const i18n = {
  "en-IN": { greeting: "Hello, Farmer", ask: "Ask Vermi", offline: "Offline - showing last recorded data." },
  "hi-IN": { greeting: "नमस्ते, किसान", ask: "बोलकर पूछें", offline: "ऑफ़लाइन - पिछला डेटा दिखाया जा रहा है।" },
  "gu-IN": { greeting: "નમસ્તે, ખેડૂત", ask: "બોલીને પૂછો", offline: "ઑફલાઇન - છેલ્લો ડેટા બતાવવામાં આવી રહ્યો છે." }
};

type VoiceState = "IDLE" | "LISTENING" | "THINKING" | "SPEAKING" | "ERROR";

export default function Home() {
  const [language, setLanguage] = useState<"en-IN" | "hi-IN" | "gu-IN">("en-IN");
  
  // Phase 3: Real Site/Bin/Node Selection
  const [site, setSite] = useState<Site | null>(null);
  const [bin, setBin] = useState<Bin | null>(null);
  const [node, setNode] = useState<Node | null>(null);
  
  const [initError, setInitError] = useState("");

  const { telemetry, isConnected, setTelemetry } = useTelemetry(node?.id || null);

  // Voice Assistant
  const [voiceState, setVoiceState] = useState<VoiceState>("IDLE");
  const [voiceError, setVoiceError] = useState("");
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  // Discovery Bootstrap
  useEffect(() => {
    async function discover() {
      try {
        const sites = await fetchSites();
        if (sites.length > 0) {
          setSite(sites[0]);
          const bins = await fetchBins(sites[0].id);
          if (bins.length > 0) {
            setBin(bins[0]);
            const nodes = await fetchNodes(bins[0].id);
            if (nodes.length > 0) {
              setNode(nodes[0]);
              const latest = await fetchLatestTelemetry(nodes[0].id);
              setTelemetry(latest);
            } else {
              setInitError("No active sensors found in bin.");
            }
          } else {
            setInitError("No beds configured for this site.");
          }
        } else {
          setInitError("No sites configured.");
        }
      } catch (err) {
        if (typeof window !== 'undefined' && (window.location.hostname.includes('vercel.app') || window.location.hostname.includes('github.io'))) {
           setSite({ id: 1, name: 'Demo Site', location: 'Virtual', created_at: '' });
           setBin({ id: 1, site_id: 1, name: 'Demo Bed', created_at: '' });
           setNode({ id: 999, bin_id: 1, hardware_id: 'SIMULATOR', status: 'ACTIVE', battery_v: 4.2, created_at: '' });
           return;
        }
        setInitError("Cannot reach Vermikendra gateway.");
      }
    }
    discover();
  }, [setTelemetry]);

  const handleStartListening = async () => {
    try {
      setVoiceError("");
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) audioChunksRef.current.push(event.data);
      };

      mediaRecorder.onstop = async () => {
        setVoiceState("THINKING");
        const audioBlob = new Blob(audioChunksRef.current, { type: "audio/webm" });
        await sendAudioToAssistant(audioBlob);
      };

      mediaRecorder.start();
      setVoiceState("LISTENING");
    } catch (error) {
      setVoiceError("Microphone access denied.");
      setVoiceState("ERROR");
    }
  };

  const handleStopListening = () => {
    if (mediaRecorderRef.current && voiceState === "LISTENING") {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach(t => t.stop());
    }
  };

  const sendAudioToAssistant = async (audioBlob: Blob) => {
    if (!node) return;
    try {
      const formData = new FormData();
      formData.append("audio", audioBlob, "question.webm");
      formData.append("language", language);
      formData.append("node_id", node.id.toString());

      const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL;
      const res = await fetch(`${API_BASE}/assistant/voice`, { method: "POST", body: formData });
      
      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData?.error?.message || "Assistant unavailable.");
      }

      const responseData: AssistantResponse = await res.json();
      
      if (responseData.audio_status === "ok" && responseData.audio_base64) {
        const audioUrl = `data:audio/wav;base64,${responseData.audio_base64}`;
        const audio = new Audio(audioUrl);
        setVoiceState("SPEAKING");
        audio.onended = () => setVoiceState("IDLE");
        await audio.play();
      } else {
        // Phase 35: Never return silent success
        setVoiceError(responseData.answer_text + "\n(Voice playback unavailable)");
        setVoiceState("ERROR");
        setTimeout(() => { setVoiceState("IDLE"); setVoiceError(""); }, 5000);
      }
      
    } catch (error: any) {
      setVoiceError(error.message);
      setVoiceState("ERROR");
      setTimeout(() => setVoiceState("IDLE"), 5000);
    }
  };

  if (initError) {
    return <div className="p-8 text-red-600 font-bold">{initError}</div>;
  }

  if (!node) {
    return <div className="p-8 text-slate-500">Loading Farm Data...</div>;
  }

  const currentTemp = telemetry?.ambient_c ?? telemetry?.probe_1;
  const statusColor = telemetry?.computed_status === 'ACTION_NEEDED' ? 'status-critical' :
                      telemetry?.computed_status === 'WATCH' ? 'status-warning' :
                      telemetry?.computed_status === 'SENSOR_FAULT' ? 'status-critical' :
                      'status-normal';

  // Format the relative time
  let timeAgo = "Just now";
  if (telemetry?.ts) {
     const ms = new Date().getTime() - new Date(telemetry.ts).getTime();
     const mins = Math.floor(ms / 60000);
     if (mins > 0) timeAgo = `${mins} min ago`;
  }

  const strings = i18n[language];

  return (
    <div className="flex flex-col min-h-screen pb-20">
      <header className="bg-white p-4 shadow-sm flex justify-between items-center sticky top-0 z-10 border-b border-slate-200">
        <div>
          <h1 className="text-xl font-bold uppercase tracking-wider">{site?.name || "VERMIKENDRA"}</h1>
          <p className="text-slate-500">{strings.greeting}</p>
        </div>
        <select 
          className="bg-slate-100 border border-slate-200 rounded p-2 text-sm font-bold"
          value={language}
          onChange={(e) => setLanguage(e.target.value as any)}
        >
          <option value="en-IN">EN</option>
          <option value="hi-IN">हिंदी</option>
          <option value="gu-IN">ગુજ</option>
        </select>
      </header>

      <main className="p-4 flex flex-col gap-6 flex-grow max-w-lg mx-auto w-full">
        
        <section className="vk-card">
          <div className="flex justify-between items-center mb-4">
            <div>
              <h2 className="text-2xl font-black tracking-tight uppercase">{bin?.name || "BED"}</h2>
              {node.id >= 100 && (
                <span className="inline-flex items-center px-2 py-1 mt-2 rounded-md text-xs font-medium bg-purple-100 text-purple-800 border border-purple-200">
                  SIMULATION
                </span>
              )}
            </div>
            {!isConnected ? (
              <span className="status-offline">
                <span className="w-2 h-2 rounded-full bg-slate-400"></span>
                OFFLINE
              </span>
            ) : (
              <span className={statusColor}>
                <span className="w-2 h-2 rounded-full bg-current"></span>
                {telemetry?.computed_status || "NORMAL"}
              </span>
            )}
          </div>
          
          <div className="border-t border-slate-100 pt-4 grid grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-slate-500 font-semibold uppercase tracking-wider mb-1">Temperature</p>
              <p className="text-2xl font-bold">{currentTemp ? `${currentTemp.toFixed(1)} °C` : "--"}</p>
            </div>
            <div>
              <p className="text-sm text-slate-500 font-semibold uppercase tracking-wider mb-1">Moisture</p>
              <p className="text-2xl font-bold">{telemetry?.moisture_raw ? telemetry.moisture_raw : "Unknown"}</p>
            </div>
            <div className="col-span-2">
              <p className="text-sm text-slate-500 font-semibold uppercase tracking-wider mb-1">Activity (CO2)</p>
              <p className="text-xl font-bold">{telemetry?.co2_ppm ? `${telemetry.co2_ppm} ppm` : "--"}</p>
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-slate-100 flex justify-between text-xs text-slate-400 font-bold uppercase">
             <span>Sensor: {telemetry?.quality || "UNKNOWN"}</span>
             <span>Updated: {timeAgo}</span>
          </div>
          
          {!isConnected && (
             <div className="mt-4 p-3 bg-slate-50 rounded text-sm text-slate-600 border border-slate-200">
               {strings.offline}
             </div>
          )}
        </section>

        <section className="mt-2 flex flex-col items-center">
          <button 
            className={`w-full max-w-xs aspect-[4/1] rounded-2xl flex items-center justify-center gap-3 text-white font-bold text-lg shadow-md transition-all active:scale-95 ${
              voiceState === "IDLE" || voiceState === "ERROR" ? "bg-[#2d7a42]" :
              voiceState === "LISTENING" ? "bg-red-600 animate-pulse" :
              voiceState === "THINKING" ? "bg-[#dd6b20]" :
              "bg-blue-600"
            }`}
            onClick={voiceState === "LISTENING" ? handleStopListening : handleStartListening}
            disabled={voiceState === "THINKING" || voiceState === "SPEAKING"}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" clipRule="evenodd" />
            </svg>
            {voiceState === "IDLE" && strings.ask}
            {voiceState === "LISTENING" && "Listening..."}
            {voiceState === "THINKING" && "Thinking..."}
            {voiceState === "SPEAKING" && "Answering..."}
            {voiceState === "ERROR" && "Try Again"}
          </button>
          
          {voiceError && <p className="text-red-600 text-sm mt-3 font-semibold text-center whitespace-pre-wrap">{voiceError}</p>}
        </section>

      </main>
    </div>
  );
}
