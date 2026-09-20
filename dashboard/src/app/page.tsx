"use client";

import { useEffect, useState, useRef } from "react";

// Voice Assistant States
type VoiceState = "IDLE" | "LISTENING" | "THINKING" | "SPEAKING" | "ERROR";

export default function Home() {
  const [telemetry, setTelemetry] = useState<any>(null);
  const [isOffline, setIsOffline] = useState(true);
  const [nodeId, setNodeId] = useState(101);
  const [language, setLanguage] = useState("en-IN"); // hi-IN, gu-IN
  
  // Voice State
  const [voiceState, setVoiceState] = useState<VoiceState>("IDLE");
  const [voiceError, setVoiceError] = useState("");
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  useEffect(() => {
    // 1. Fetch initial state
    fetch(`http://localhost:8000/api/nodes/${nodeId}/telemetry/latest`)
      .then(res => res.json())
      .then(data => {
        setTelemetry(data);
        setIsOffline(false);
      })
      .catch(() => setIsOffline(true));

    // 2. Connect WebSocket
    const ws = new WebSocket("ws://localhost:8000/ws/telemetry");
    ws.onopen = () => setIsOffline(false);
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.node === nodeId) {
          setTelemetry((prev: any) => ({
            ...prev,
            ...data
          }));
        }
      } catch (e) {
        console.error("WS Parse Error", e);
      }
    };
    ws.onclose = () => setIsOffline(true);
    return () => ws.close();
  }, [nodeId]);

  const handleStartListening = async () => {
    try {
      setVoiceError("");
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        setVoiceState("THINKING");
        const audioBlob = new Blob(audioChunksRef.current, { type: "audio/webm" });
        await sendAudioToAssistant(audioBlob);
      };

      mediaRecorder.start();
      setVoiceState("LISTENING");
    } catch (error) {
      console.error("Microphone access denied:", error);
      setVoiceError("Microphone access denied. Check permissions.");
      setVoiceState("ERROR");
    }
  };

  const handleStopListening = () => {
    if (mediaRecorderRef.current && voiceState === "LISTENING") {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
    }
  };

  const sendAudioToAssistant = async (audioBlob: Blob) => {
    try {
      const formData = new FormData();
      formData.append("audio", audioBlob, "question.webm");
      formData.append("language", language);
      formData.append("node_id", nodeId.toString());

      const res = await fetch("http://localhost:8000/api/assistant/voice", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error("Assistant unavailable. Network may be slow.");
      }

      const audioData = await res.blob();
      const audioUrl = URL.createObjectURL(audioData);
      const audio = new Audio(audioUrl);
      
      setVoiceState("SPEAKING");
      
      audio.onended = () => {
        setVoiceState("IDLE");
      };
      
      await audio.play();
      
    } catch (error: any) {
      setVoiceError(error.message || "Failed to contact assistant.");
      setVoiceState("ERROR");
      setTimeout(() => setVoiceState("IDLE"), 5000);
    }
  };

  // Safe Accessors
  const currentTemp = telemetry?.ambient_c ?? telemetry?.probes_c?.[0] ?? telemetry?.probe_1;
  const isReady = false; // Deterministic calculation is unverified, default false

  return (
    <div className="flex flex-col min-h-screen pb-20">
      
      {/* --- HEADER --- */}
      <header className="bg-white p-4 shadow-sm flex justify-between items-center sticky top-0 z-10 border-b border-slate-200">
        <div>
          <h1 className="text-xl font-bold">VERMIKENDRA</h1>
          <p className="text-slate-500">नमस्ते, रामभाई</p>
        </div>
        <select 
          className="bg-slate-100 border border-slate-200 rounded p-2 text-sm"
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
        >
          <option value="en-IN">English</option>
          <option value="hi-IN">हिंदी</option>
          <option value="gu-IN">ગુજરાતી</option>
        </select>
      </header>

      <main className="p-4 flex flex-col gap-6 flex-grow max-w-lg mx-auto w-full">
        
        {/* --- PRIMARY BED STATUS --- */}
        <section className="vk-card">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-black tracking-tight">BED 01</h2>
            {isOffline ? (
              <span className="status-offline">
                <span className="w-2 h-2 rounded-full bg-slate-400"></span>
                OFFLINE
              </span>
            ) : (
              <span className="status-normal">
                <span className="w-2 h-2 rounded-full bg-green-500"></span>
                NORMAL
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
              <p className="text-2xl font-bold">Stable</p>
            </div>
            <div className="col-span-2">
              <p className="text-sm text-slate-500 font-semibold uppercase tracking-wider mb-1">Activity</p>
              <p className="text-xl font-bold">{telemetry?.co2_ppm ? `${telemetry.co2_ppm} ppm` : "--"}</p>
            </div>
          </div>
          
          {isOffline && (
             <div className="mt-4 p-3 bg-slate-50 rounded text-sm text-slate-600 border border-slate-200">
               Network unavailable. Showing last recorded data.
             </div>
          )}
        </section>

        {/* --- VOICE ASSISTANT --- */}
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
            aria-label="Ask Vermi"
          >
            {/* Microphone Icon SVG */}
            <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" clipRule="evenodd" />
            </svg>
            
            {voiceState === "IDLE" && "Ask Vermi"}
            {voiceState === "LISTENING" && "Listening... Tap to stop"}
            {voiceState === "THINKING" && "Thinking..."}
            {voiceState === "SPEAKING" && "Answering..."}
            {voiceState === "ERROR" && "Try Again"}
          </button>
          
          {voiceError && <p className="text-red-600 text-sm mt-3 font-semibold text-center">{voiceError}</p>}
        </section>

        {/* --- MENU LIST --- */}
        <section className="vk-card !p-0 overflow-hidden">
          <div className="divide-y divide-slate-100">
            <button className="w-full text-left p-5 flex justify-between items-center hover:bg-slate-50 active:bg-slate-100 transition-colors">
              <span className="font-bold text-lg">Temperature Details</span>
              <span className="text-slate-400 text-xl">→</span>
            </button>
            <button className="w-full text-left p-5 flex justify-between items-center hover:bg-slate-50 active:bg-slate-100 transition-colors">
              <span className="font-bold text-lg">Moisture Details</span>
              <span className="text-slate-400 text-xl">→</span>
            </button>
            <button className="w-full text-left p-5 flex justify-between items-center hover:bg-slate-50 active:bg-slate-100 transition-colors">
              <span className="font-bold text-lg">Compost Activity</span>
              <span className="text-slate-400 text-xl">→</span>
            </button>
            <button className="w-full text-left p-5 flex justify-between items-center hover:bg-slate-50 active:bg-slate-100 transition-colors">
              <span className="font-bold text-lg">Alerts</span>
              <span className="text-slate-400 text-xl">→</span>
            </button>
          </div>
        </section>
        
      </main>

      {/* --- BOTTOM NAVIGATION --- */}
      <nav className="bg-white border-t border-slate-200 fixed bottom-0 w-full flex justify-around p-2 pb-safe shadow-[0_-2px_10px_rgba(0,0,0,0.05)]">
        <button className="p-3 flex flex-col items-center gap-1 text-[#2d7a42] font-bold min-w-[80px]">
          <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20"><path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" /></svg>
          <span className="text-xs">Home</span>
        </button>
        <button className="p-3 flex flex-col items-center gap-1 text-slate-500 hover:text-slate-800 min-w-[80px]">
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" /></svg>
          <span className="text-xs">Beds</span>
        </button>
        <button className="p-3 flex flex-col items-center gap-1 text-slate-500 hover:text-slate-800 min-w-[80px]">
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          <span className="text-xs">History</span>
        </button>
      </nav>
      
    </div>
  );
}
