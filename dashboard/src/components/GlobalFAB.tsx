'use client';

import { useState, useRef } from 'react';
import { AssistantResponse } from '../types';

export default function GlobalFAB() {
  const [voiceState, setVoiceState] = useState<"IDLE" | "LISTENING" | "THINKING" | "SPEAKING" | "ERROR">("IDLE");
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  const handleStartListening = async () => {
    try {
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
      setVoiceState("ERROR");
      setTimeout(() => setVoiceState("IDLE"), 3000);
    }
  };

  const handleStopListening = () => {
    if (mediaRecorderRef.current && voiceState === "LISTENING") {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach(t => t.stop());
    }
  };

  const sendAudioToAssistant = async (audioBlob: Blob) => {
    try {
      const formData = new FormData();
      formData.append("audio", audioBlob, "question.webm");
      formData.append("language", "en-IN");
      formData.append("node_id", "1"); // Default context for now

      const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL;
      const res = await fetch(`${API_BASE}/assistant/voice`, { method: "POST", body: formData });
      
      if (!res.ok) throw new Error("Assistant unavailable.");

      const responseData: AssistantResponse = await res.json();
      
      if (responseData.audio_status === "ok" && responseData.audio_base64) {
        const audioUrl = `data:audio/wav;base64,${responseData.audio_base64}`;
        const audio = new Audio(audioUrl);
        setVoiceState("SPEAKING");
        audio.onended = () => setVoiceState("IDLE");
        await audio.play();
      } else {
        setVoiceState("ERROR");
        setTimeout(() => setVoiceState("IDLE"), 3000);
      }
    } catch (error) {
      setVoiceState("ERROR");
      setTimeout(() => setVoiceState("IDLE"), 3000);
    }
  };

  return (
    <button 
      onClick={voiceState === "LISTENING" ? handleStopListening : handleStartListening}
      disabled={voiceState === "THINKING" || voiceState === "SPEAKING"}
      className={`fixed bottom-[80px] right-4 w-14 h-14 text-white rounded-full shadow-xl flex items-center justify-center active:scale-95 transition-all z-40 ${
          voiceState === "IDLE" ? "bg-[#2d7a42] shadow-green-900/30" :
          voiceState === "LISTENING" ? "bg-red-600 animate-pulse shadow-red-900/30" :
          voiceState === "THINKING" ? "bg-[#dd6b20] shadow-orange-900/30" :
          voiceState === "SPEAKING" ? "bg-blue-600 shadow-blue-900/30" :
          "bg-slate-500"
      }`}
    >
       <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" clipRule="evenodd" />
       </svg>
    </button>
  );
}
