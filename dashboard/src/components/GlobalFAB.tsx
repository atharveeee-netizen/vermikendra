'use client';

import React, { useState, useEffect, useRef } from 'react';
import { Mic, Volume2, VolumeX, X, Sparkles, HelpCircle } from 'lucide-react';
import { fetchSiteFleet } from '../services/api';
import { FleetData } from '../types';

interface VoiceQueryAnswer {
  question: string;
  answer: string;
  bedHighlight?: string;
}

export default function GlobalFAB() {
  const [isOpen, setIsOpen] = useState(false);
  const [voiceState, setVoiceState] = useState<"IDLE" | "LISTENING" | "THINKING" | "SPEAKING" | "ERROR">("IDLE");
  const [transcript, setTranscript] = useState("");
  const [lastResponse, setLastResponse] = useState<VoiceQueryAnswer | null>(null);
  const [isSpeakingAudio, setIsSpeakingAudio] = useState(false);
  const [fleetData, setFleetData] = useState<FleetData | null>(null);
  
  const recognitionRef = useRef<any>(null);

  // Load live farm bed data for answering questions
  useEffect(() => {
    fetchSiteFleet("site-pune-01").then(data => setFleetData(data)).catch(() => {});
  }, []);

  const generateAnswer = (userQuery: string): VoiceQueryAnswer => {
    const q = userQuery.toLowerCase();
    const nodes = fleetData?.nodes || [];
    
    // Check specific bed queries
    for (let i = 1; i <= 6; i++) {
      const bedTag = `bed ${i}`;
      const bedTagAlt = `bed-${i}`;
      const bedTag0 = `bed 0${i}`;
      const bedTag0Alt = `bed-0${i}`;
      
      if (q.includes(bedTag) || q.includes(bedTagAlt) || q.includes(bedTag0) || q.includes(bedTag0Alt)) {
        const node = nodes.find(n => n.node_id === i);
        if (!node || !node.latest_telemetry) {
          return {
            question: userQuery,
            answer: `Bed 0${i} sensor is currently offline. Please check its battery or connection in Field B.`,
            bedHighlight: `BED-0${i}`
          };
        }
        const t = node.latest_telemetry;
        const status = node.computed_status;
        let advice = `Bed 0${i} has a moisture level of ${t.moisture_raw}% and average core temperature of ${t.ambient_c} degrees Celsius. `;
        if (status === 'ACTION_NEEDED') {
          advice += `Action needed: Moisture is critically low. Please sprinkle 30 to 40 liters of water right away to protect worm biology.`;
        } else if (status === 'WATCH') {
          advice += `Caution: Core temperature is trending high. Ensure the shade net cover is moist and in place.`;
        } else {
          advice += `Status is optimal. Earthworm activity and casting production are flourishing normally.`;
        }
        return {
          question: userQuery,
          answer: advice,
          bedHighlight: `BED-0${i}`
        };
      }
    }

    // Water or Moisture queries
    if (q.includes("water") || q.includes("pani") || q.includes("moisture") || q.includes("dry") || q.includes("spray")) {
      const dryBed = nodes.find(n => n.computed_status === 'ACTION_NEEDED');
      if (dryBed && dryBed.latest_telemetry) {
        return {
          question: userQuery,
          answer: `${dryBed.bin_name} has dropped to ${dryBed.latest_telemetry.moisture_raw}% moisture. Please spray 30 to 40 liters of clean water immediately. Other beds are currently well hydrated.`,
          bedHighlight: dryBed.bin_name
        };
      }
      return {
        question: userQuery,
        answer: "Moisture across your primary beds is in the ideal 60 to 70 percent zone. You do not need heavy irrigation today. A light surface misting will suffice."
      };
    }

    // Temperature queries
    if (q.includes("temp") || q.includes("temperature") || q.includes("garam") || q.includes("heat") || q.includes("hot")) {
      const watchBed = nodes.find(n => n.computed_status === 'WATCH');
      if (watchBed && watchBed.latest_telemetry) {
        return {
          question: userQuery,
          answer: `Caution: ${watchBed.bin_name} core temperature has reached ${watchBed.latest_telemetry.probe_4}°C. Verify shade net ventilation to prevent heat stress in the worms.`,
          bedHighlight: watchBed.bin_name
        };
      }
      return {
        question: userQuery,
        answer: "Bed temperatures are steady between 26 and 30 degrees Celsius. This is well within the 20 to 32 degree sweet spot for Eisenia fetida earthworms."
      };
    }

    // Harvest readiness
    if (q.includes("harvest") || q.includes("ready") || q.includes("compost") || q.includes("khat")) {
      return {
        question: userQuery,
        answer: "Bed 01 compost is approaching dark, granular maturity. Stop watering 3 days before harvest so worms migrate downward, allowing clean top layer scraping.",
        bedHighlight: "BED-01"
      };
    }

    // Default farm overview
    const stats = fleetData?.stats;
    const total = stats?.total || 6;
    const attention = stats?.attention || 1;
    const critical = stats?.critical || 1;
    return {
      question: userQuery,
      answer: `Vermikendra farm summary: You have ${total} beds. 3 are in optimal normal condition, ${attention} is on watch, and ${critical} requires immediate water. Worm activity is healthy overall.`
    };
  };

  const speakAnswer = (text: string) => {
    if (typeof window === "undefined" || !('speechSynthesis' in window)) return;
    
    // Cancel any ongoing speech
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.95;
    utterance.pitch = 1.0;
    utterance.lang = "en-IN";

    // Select natural voice if available
    const voices = window.speechSynthesis.getVoices();
    const indianVoice = voices.find(v => v.lang.includes("en-IN") || v.lang.includes("hi-IN"));
    if (indianVoice) {
      utterance.voice = indianVoice;
    }

    utterance.onstart = () => {
      setIsSpeakingAudio(true);
      setVoiceState("SPEAKING");
    };

    utterance.onend = () => {
      setIsSpeakingAudio(false);
      setVoiceState("IDLE");
    };

    utterance.onerror = () => {
      setIsSpeakingAudio(false);
      setVoiceState("IDLE");
    };

    window.speechSynthesis.speak(utterance);
  };

  const handleStartListening = () => {
    if (typeof window === "undefined") return;

    // Stop speaking if currently talking
    if (isSpeakingAudio) {
      window.speechSynthesis.cancel();
      setIsSpeakingAudio(false);
    }

    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setVoiceState("IDLE");
      return;
    }

    try {
      const recognition = new SpeechRecognition();
      recognitionRef.current = recognition;
      recognition.lang = "en-IN";
      recognition.interimResults = true;
      recognition.maxAlternatives = 1;

      recognition.onstart = () => {
        setVoiceState("LISTENING");
        setTranscript("");
      };

      recognition.onresult = (event: any) => {
        const current = event.resultIndex;
        const transcriptText = event.results[current][0].transcript;
        setTranscript(transcriptText);
      };

      recognition.onerror = () => {
        setVoiceState("ERROR");
        setTimeout(() => setVoiceState("IDLE"), 2500);
      };

      recognition.onend = () => {
        if (transcript.trim().length > 0) {
          processVoiceQuery(transcript);
        } else {
          setVoiceState("IDLE");
        }
      };

      recognition.start();
    } catch {
      setVoiceState("ERROR");
      setTimeout(() => setVoiceState("IDLE"), 2500);
    }
  };

  const handleStopListening = () => {
    if (recognitionRef.current && voiceState === "LISTENING") {
      recognitionRef.current.stop();
    }
  };

  const audioPlayerRef = useRef<HTMLAudioElement | null>(null);

  const processVoiceQuery = async (queryText: string) => {
    setVoiceState("THINKING");
    try {
      const res = await fetch("/api/assistant/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: queryText })
      });

      if (res.ok) {
        const data = await res.json();
        const answerText = data.text;
        const audioB64 = data.audio_base64;

        if (answerText) {
          setLastResponse({
            question: queryText,
            answer: answerText
          });

          if (audioB64) {
            if (audioPlayerRef.current) {
              audioPlayerRef.current.pause();
            }
            const audio = new Audio(`data:audio/wav;base64,${audioB64}`);
            audioPlayerRef.current = audio;
            setVoiceState("SPEAKING");
            setIsSpeakingAudio(true);
            audio.onended = () => {
              setIsSpeakingAudio(false);
              setVoiceState("IDLE");
            };
            audio.onerror = () => {
              speakAnswer(answerText);
            };
            await audio.play();
            return;
          } else {
            speakAnswer(answerText);
            return;
          }
        }
      }
    } catch (e) {
      console.warn("API assistant fallback:", e);
    }

    // Local Agronomy Engine Fallback
    const response = generateAnswer(queryText);
    setLastResponse(response);
    speakAnswer(response.answer);
  };

  const handleSampleQuestion = (sample: string) => {
    setTranscript(sample);
    processVoiceQuery(sample);
  };

  const stopVoiceSpeech = () => {
    if (audioPlayerRef.current) {
      audioPlayerRef.current.pause();
      audioPlayerRef.current = null;
    }
    if (typeof window !== "undefined" && 'speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
    setIsSpeakingAudio(false);
    setVoiceState("IDLE");
  };

  return (
    <>
      {/* Floating Action Button */}
      <button 
        id="ask-vermi-fab-btn"
        onClick={() => {
          setIsOpen(true);
          if (voiceState === "IDLE") {
            handleStartListening();
          }
        }}
        aria-label="Ask Vermi Voice Assistant"
        className={`fixed bottom-[84px] right-4 w-14 h-14 rounded-full shadow-2xl flex items-center justify-center active:scale-95 transition-all z-40 ${
          voiceState === "LISTENING" 
            ? "bg-red-600 animate-pulse text-white shadow-red-600/50 ring-4 ring-red-300" 
            : voiceState === "SPEAKING"
            ? "bg-blue-600 text-white shadow-blue-600/50 ring-4 ring-blue-200"
            : voiceState === "THINKING"
            ? "bg-amber-500 animate-spin text-white shadow-amber-500/40"
            : "bg-[#2d7a42] hover:bg-[#256336] text-white shadow-green-900/40"
        }`}
      >
        {voiceState === "LISTENING" ? (
          <Mic className="h-6 w-6" />
        ) : voiceState === "SPEAKING" ? (
          <Volume2 className="h-6 w-6" />
        ) : (
          <Mic className="h-6 w-6" />
        )}
      </button>

      {/* Voice Assistant Modal / Bottom Sheet */}
      {isOpen && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-xs z-50 flex flex-col justify-end sm:justify-center sm:items-center p-0 sm:p-4">
          <div className="bg-white w-full sm:max-w-md rounded-t-3xl sm:rounded-2xl p-5 shadow-2xl border border-stone-200 flex flex-col max-h-[85vh] overflow-y-auto">
            
            {/* Header */}
            <div className="flex items-center justify-between pb-3 border-b border-stone-100">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-full bg-emerald-100 text-emerald-800 flex items-center justify-center font-bold">
                  <Sparkles className="h-4 w-4 text-emerald-700" />
                </div>
                <div>
                  <h3 className="font-bold text-stone-900 text-base leading-tight">Ask Vermi (आस्क वर्मी)</h3>
                  <p className="text-xs text-stone-500">Field Agronomy Voice Assistant</p>
                </div>
              </div>
              
              <button 
                onClick={() => {
                  stopVoiceSpeech();
                  setIsOpen(false);
                }}
                className="p-1.5 rounded-full hover:bg-stone-100 text-stone-400 hover:text-stone-700 transition-colors"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            {/* Live Voice Interaction Status */}
            <div className="py-6 flex flex-col items-center justify-center text-center">
              <button
                onClick={voiceState === "LISTENING" ? handleStopListening : handleStartListening}
                className={`w-20 h-20 rounded-full flex items-center justify-center transition-all mb-3 ${
                  voiceState === "LISTENING"
                    ? "bg-red-600 text-white animate-pulse ring-8 ring-red-100 shadow-lg shadow-red-500/30"
                    : voiceState === "SPEAKING"
                    ? "bg-blue-600 text-white ring-8 ring-blue-100 shadow-lg shadow-blue-500/30"
                    : voiceState === "THINKING"
                    ? "bg-amber-500 text-white animate-pulse"
                    : "bg-[#2d7a42] text-white hover:bg-[#256336] ring-8 ring-green-100 shadow-lg shadow-green-900/20"
                }`}
              >
                {voiceState === "LISTENING" ? (
                  <Mic className="h-9 w-9" />
                ) : voiceState === "SPEAKING" ? (
                  <Volume2 className="h-9 w-9 animate-pulse" />
                ) : (
                  <Mic className="h-9 w-9" />
                )}
              </button>

              <div className="font-medium text-sm text-stone-800">
                {voiceState === "LISTENING" && <span className="text-red-600 font-bold">● Listening to you... Speak now</span>}
                {voiceState === "THINKING" && <span className="text-amber-600">Analyzing farm sensors...</span>}
                {voiceState === "SPEAKING" && <span className="text-blue-600 font-bold">Speaking answer aloud...</span>}
                {voiceState === "IDLE" && <span className="text-stone-600">Tap mic to speak or select question below</span>}
                {voiceState === "ERROR" && <span className="text-red-500">Mic interrupted. Tap to try again.</span>}
              </div>

              {transcript && (
                <div className="mt-3 px-3 py-1.5 bg-stone-100 rounded-lg text-xs font-medium text-stone-700 max-w-[90%] italic">
                  "{transcript}"
                </div>
              )}
            </div>

            {/* Last Spoken Response Card */}
            {lastResponse && (
              <div className="mb-4 bg-emerald-50/70 border border-emerald-200 rounded-xl p-3.5 text-left">
                <div className="flex items-center justify-between mb-1.5">
                  <span className="text-xs font-semibold uppercase tracking-wider text-emerald-800 flex items-center gap-1">
                    <Sparkles className="h-3.5 w-3.5 text-emerald-600" /> Vermi Agronomist
                  </span>
                  {isSpeakingAudio && (
                    <button 
                      onClick={stopVoiceSpeech}
                      className="text-[11px] font-medium text-blue-700 bg-blue-100 px-2 py-0.5 rounded-md flex items-center gap-1 hover:bg-blue-200"
                    >
                      <VolumeX className="h-3 w-3" /> Stop Voice
                    </button>
                  )}
                </div>
                <p className="text-xs text-stone-800 leading-relaxed">
                  {lastResponse.answer}
                </p>
                {lastResponse.bedHighlight && (
                  <div className="mt-2 text-[11px] font-bold text-emerald-900 bg-emerald-200/60 inline-block px-2 py-0.5 rounded">
                    Tagged: {lastResponse.bedHighlight}
                  </div>
                )}
              </div>
            )}

            {/* Quick Sample Questions (Farmer Prompts) */}
            <div className="mt-1">
              <p className="text-xs font-semibold text-stone-500 mb-2 flex items-center gap-1">
                <HelpCircle className="h-3.5 w-3.5 text-stone-400" /> Quick Farmer Questions:
              </p>
              <div className="grid grid-cols-1 gap-1.5">
                {[
                  "Which bed needs watering right now?",
                  "How is Bed 5 doing?",
                  "Are temperatures safe for worms today?",
                  "Is Bed 1 ready for harvest?",
                  "Overall farm health status"
                ].map((sample, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleSampleQuestion(sample)}
                    className="text-left text-xs bg-stone-50 hover:bg-stone-100 active:bg-emerald-50 text-stone-700 border border-stone-200/80 rounded-lg p-2 transition-all flex items-center justify-between"
                  >
                    <span>"{sample}"</span>
                    <span className="text-emerald-700 text-[10px] font-bold ml-2">ASK →</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Footer */}
            <div className="mt-4 pt-3 border-t border-stone-100 flex items-center justify-between text-[11px] text-stone-400">
              <span>Speaks in English & Marathi/Hindi context</span>
              <button 
                onClick={() => {
                  stopVoiceSpeech();
                  setIsOpen(false);
                }}
                className="text-stone-600 font-medium hover:underline"
              >
                Close
              </button>
            </div>

          </div>
        </div>
      )}
    </>
  );
}
