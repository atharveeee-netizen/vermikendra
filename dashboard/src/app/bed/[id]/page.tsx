"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { fetchLatestTelemetry } from "../../../services/api";
import { useTelemetry } from "../../../hooks/useTelemetry";
import { 
  ArrowLeft, 
  Thermometer, 
  Droplet, 
  Wind, 
  Scale, 
  Activity, 
  FileText, 
  BarChart3, 
  ChevronRight, 
  Calendar, 
  Clock, 
  PlusCircle, 
  CheckCircle2, 
  X, 
  Sprout, 
  Sparkles 
} from "lucide-react";

interface ActionLog {
  id: string;
  action: string;
  detail: string;
  timestamp: string;
}

export default function BedDetail() {
  const params = useParams();
  const router = useRouter();
  const nodeId = parseInt(params.id as string, 10);
  const [initError, setInitError] = useState("");
  
  // Action Logger State (A12)
  const [showLogModal, setShowLogModal] = useState(false);
  const [selectedAction, setSelectedAction] = useState("Watered Bed (15L)");
  const [actionNotes, setActionNotes] = useState("");
  const [logs, setLogs] = useState<ActionLog[]>([
    { id: "1", action: "Watered Bed (12L)", detail: "Sprinkled moisture over surface layer", timestamp: "Today, 10:30 AM" },
    { id: "2", action: "Turned & Aerated Pile", detail: "Fork-turned upper 15cm to prevent thermal core spike", timestamp: "Yesterday, 4:15 PM" },
    { id: "3", action: "Added Dry Straw Bedding", detail: "Added 5kg shredded paddy straw", timestamp: "3 days ago" },
  ]);

  // Chart view toggle (A20)
  const [chartMetric, setChartMetric] = useState<"temp" | "moisture">("temp");

  const { telemetry, isConnected, setTelemetry } = useTelemetry(nodeId || null);

  useEffect(() => {
    async function init() {
      if (!nodeId || isNaN(nodeId)) {
        setInitError("Invalid bed ID.");
        return;
      }
      try {
        const latest = await fetchLatestTelemetry(nodeId);
        setTelemetry(latest);
      } catch (err) {
        setInitError("Cannot reach Vermikendra gateway.");
      }
    }
    init();
  }, [nodeId, setTelemetry]);

  const handleAddLog = () => {
    if (!selectedAction) return;
    const newLog: ActionLog = {
      id: Date.now().toString(),
      action: selectedAction,
      detail: actionNotes || "Routine maintenance recorded by farmer.",
      timestamp: "Just now"
    };
    setLogs([newLog, ...logs]);
    setActionNotes("");
    setShowLogModal(false);
  };

  if (initError) {
    return (
       <div className="flex flex-col min-h-screen bg-[#F9F8F4]">
          <header className="bg-white p-4 shadow-sm flex items-center gap-4">
             <button onClick={() => router.back()}><ArrowLeft /></button>
             <h1 className="text-xl font-bold text-slate-800">Error</h1>
          </header>
          <div className="p-8 text-red-600 font-bold">{initError}</div>
       </div>
    );
  }

  let timeAgo = "Just now";
  if (telemetry?.ts) {
     const ms = new Date().getTime() - new Date(telemetry.ts).getTime();
     const mins = Math.floor(ms / 60000);
     if (mins > 0) timeAgo = `${mins} min ago`;
  }

  // Calculate probe gradient data
  const probes = [
    { label: "Surface", value: telemetry?.probe_1 },
    { label: "Upper", value: telemetry?.probe_2 },
    { label: "Mid", value: telemetry?.probe_3 },
    { label: "Core", value: telemetry?.probe_4 },
    { label: "Base", value: telemetry?.probe_5 }
  ];
  const maxProbe = Math.max(...probes.map(p => p.value || 0));
  const maxProbeIndex = probes.findIndex(p => p.value === maxProbe);
  const shellTemp = probes[0].value;
  const coreTemp = probes[3].value;
  const delta = (coreTemp !== undefined && shellTemp !== undefined && coreTemp !== null && shellTemp !== null) 
                  ? (coreTemp - shellTemp).toFixed(1) 
                  : '--';

  // Simulated 24h trend data points (A20)
  const tempTrend = [28.5, 29.2, 30.1, 31.0, 31.8, 32.4, 32.1, 31.4, 30.8, 30.2, 29.6, 29.1];
  const moistureTrend = [58, 59, 60, 62, 63, 62, 61, 60, 62, 63, 61, 62];

  return (
    <div className="flex flex-col min-h-screen pb-28 bg-[#F9F8F4]">
      {/* Header */}
      <header className="bg-[#2d7a42] text-white p-4 shadow-md flex items-center gap-3 sticky top-0 z-10 pb-6 rounded-b-[1.5rem]">
         <button onClick={() => router.back()} className="p-2 -ml-2 rounded-full hover:bg-green-700/50 transition-colors">
            <ArrowLeft className="w-6 h-6 text-white" />
         </button>
         <div>
            <h1 className="text-xl font-black uppercase tracking-wider">{telemetry?.bin_name || `BED ${nodeId}`}</h1>
            <p className="text-green-100 text-xs font-medium uppercase tracking-widest">{telemetry?.field_id || 'Field Area'}</p>
         </div>
      </header>

      <main className="p-4 flex flex-col gap-4 max-w-lg mx-auto w-full -mt-4 relative z-20">
        
        {/* Status Card */}
        <section className="bg-white rounded-xl shadow-sm border border-slate-200 p-4">
           <div className="flex justify-between items-center mb-1">
               <h2 className="text-sm font-bold text-slate-500 uppercase tracking-widest">System Status</h2>
               {!isConnected ? (
                 <span className="status-offline flex items-center gap-1.5 px-2 py-1 rounded-md border text-[10px] font-black uppercase tracking-wider bg-slate-100 text-slate-600 border-slate-200">
                   <span className="w-1.5 h-1.5 rounded-full bg-slate-400"></span> OFFLINE
                 </span>
               ) : (
                 <span className={`flex items-center gap-1.5 px-2 py-1 rounded-md border text-[10px] font-black uppercase tracking-wider ${
                    telemetry?.computed_status === 'NORMAL' ? 'bg-green-50 text-green-700 border-green-200' :
                    telemetry?.computed_status === 'WATCH' ? 'bg-orange-50 text-orange-700 border-orange-200' :
                    'bg-red-50 text-red-700 border-red-200'
                 }`}>
                   <span className={`w-1.5 h-1.5 rounded-full ${
                      telemetry?.computed_status === 'NORMAL' ? 'bg-green-500' :
                      telemetry?.computed_status === 'WATCH' ? 'bg-orange-500' :
                      'bg-red-500 animate-pulse'
                   }`}></span>
                   {telemetry?.computed_status || "NORMAL"}
                 </span>
               )}
           </div>
           
           {telemetry?.computed_reason && telemetry?.computed_status !== 'NORMAL' && (
              <p className="text-sm font-bold text-slate-800 mt-2">{telemetry.computed_reason}</p>
           )}
           <p className="text-xs font-medium text-slate-500 mt-1">Eisenia fetida active. Composting stage: <span className="text-slate-800 font-bold">Active Maturation</span></p>
        </section>

        {/* Harvest Stage Tracker (A13) */}
        <section className="bg-white rounded-xl border border-slate-200 shadow-sm p-4">
          <div className="flex justify-between items-center mb-2">
            <div className="flex items-center gap-2">
              <Sprout className="w-4 h-4 text-[#2d7a42]" />
              <span className="text-xs font-bold text-slate-600 uppercase tracking-wider">Harvest Cycle Progress</span>
            </div>
            <span className="text-xs font-black text-[#2d7a42] bg-green-50 px-2 py-0.5 rounded-full border border-green-200">
              Day 42 / 60
            </span>
          </div>

          <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden mb-2">
            <div className="bg-[#2d7a42] h-full rounded-full transition-all duration-500" style={{ width: '70%' }}></div>
          </div>

          <div className="flex justify-between text-[10px] font-bold text-slate-400 mb-3">
            <span>Bed Bedding (Day 1)</span>
            <span className="text-[#2d7a42]">Active Digestion (Now)</span>
            <span>Harvest Ready (~18 Days)</span>
          </div>

          <div className="bg-green-50/70 border border-green-200 rounded-lg p-2.5 flex items-center justify-between text-xs">
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-green-700" />
              <span className="font-medium text-green-900">Estimated Yield: <strong className="font-bold">450 kg</strong> Premium Castings</span>
            </div>
            <span className="text-[10px] font-bold text-green-800 uppercase">Stage 3</span>
          </div>
        </section>

        {/* Rich Sensor Dashboard (A4) */}
        <section className="grid grid-cols-2 gap-3">
           {/* CORE TEMP */}
           <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-3">
              <div className="flex justify-between items-start mb-2">
                 <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Core Temp</span>
                 <Thermometer className="w-4 h-4 text-orange-500" />
              </div>
              <div className="font-black text-2xl text-slate-800 mb-1">
                 {coreTemp !== undefined && coreTemp !== null ? `${coreTemp.toFixed(1)}°C` : '--'}
              </div>
              <div className="text-xs font-medium text-slate-400">Pref: 28-32°C</div>
           </div>

           {/* MOISTURE */}
           <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-3">
              <div className="flex justify-between items-start mb-2">
                 <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Moisture</span>
                 <Droplet className="w-4 h-4 text-blue-500" />
              </div>
              <div className="font-black text-2xl text-slate-800 mb-1">
                 {telemetry?.moisture_raw !== undefined && telemetry?.moisture_raw !== null ? `${telemetry.moisture_raw}%` : '--'}
              </div>
              <div className="text-xs font-medium text-slate-400">Optimal: 50-65%</div>
           </div>

           {/* CO2 RESP */}
           <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-3">
              <div className="flex justify-between items-start mb-2">
                 <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">CO2 Resp</span>
                 <Wind className="w-4 h-4 text-slate-400" />
              </div>
              <div className="font-black text-2xl text-slate-800 mb-1">
                 {telemetry?.co2_ppm !== undefined && telemetry?.co2_ppm !== null ? `${telemetry.co2_ppm} ppm` : '--'}
              </div>
              <div className="text-xs font-medium text-slate-400">
                 {telemetry?.co2_ppm && telemetry.co2_ppm > 1000 ? <span className="text-green-600 font-bold">High activity</span> : 'Normal activity'}
              </div>
           </div>

           {/* BED MASS */}
           <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-3">
              <div className="flex justify-between items-start mb-2">
                 <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Est. Mass</span>
                 <Scale className="w-4 h-4 text-slate-400" />
              </div>
              <div className="font-black text-2xl text-slate-800 mb-1">
                 {telemetry?.mass_g !== undefined && telemetry?.mass_g !== null ? `${(telemetry.mass_g / 1000).toFixed(0)} kg` : '620 kg'}
              </div>
              <div className="text-xs font-medium text-slate-400">Total biomass</div>
           </div>
        </section>

        {/* 24-Hour Telemetry Trend (A20) */}
        <section className="bg-white rounded-xl border border-slate-200 shadow-sm p-4">
          <div className="flex justify-between items-center mb-3">
            <div className="flex items-center gap-2">
              <BarChart3 className="w-4 h-4 text-slate-600" />
              <span className="text-xs font-bold text-slate-700 uppercase tracking-wider">24h Telemetry Trend</span>
            </div>
            <div className="flex bg-slate-100 rounded-lg p-0.5 text-[10px] font-bold">
              <button 
                onClick={() => setChartMetric("temp")} 
                className={`px-2 py-1 rounded-md transition-all ${chartMetric === "temp" ? "bg-white text-orange-600 shadow-sm" : "text-slate-500"}`}
              >
                Temp
              </button>
              <button 
                onClick={() => setChartMetric("moisture")} 
                className={`px-2 py-1 rounded-md transition-all ${chartMetric === "moisture" ? "bg-white text-blue-600 shadow-sm" : "text-slate-500"}`}
              >
                Moisture
              </button>
            </div>
          </div>

          {/* Trend Bar Visualization */}
          <div className="h-20 flex items-end gap-1.5 pt-2 px-1">
            {(chartMetric === "temp" ? tempTrend : moistureTrend).map((val, idx) => {
              const maxVal = chartMetric === "temp" ? 35 : 70;
              const minVal = chartMetric === "temp" ? 25 : 50;
              const heightPct = Math.max(15, Math.min(100, ((val - minVal) / (maxVal - minVal)) * 100));
              return (
                <div key={idx} className="flex-1 flex flex-col items-center gap-1 group relative">
                  <span className="opacity-0 group-hover:opacity-100 absolute -top-5 text-[9px] font-bold bg-slate-800 text-white px-1 rounded transition-opacity pointer-events-none">
                    {val}{chartMetric === "temp" ? "°" : "%"}
                  </span>
                  <div 
                    className={`w-full rounded-t-sm transition-all ${
                      chartMetric === "temp" 
                        ? "bg-gradient-to-t from-orange-300 to-orange-500 hover:from-orange-400 hover:to-orange-600" 
                        : "bg-gradient-to-t from-blue-300 to-blue-500 hover:from-blue-400 hover:to-blue-600"
                    }`}
                    style={{ height: `${heightPct}%` }}
                  ></div>
                </div>
              );
            })}
          </div>
          <div className="flex justify-between text-[10px] font-bold text-slate-400 mt-2 border-t border-slate-100 pt-1">
            <span>24h ago</span>
            <span>12h ago</span>
            <span>Current</span>
          </div>
        </section>

        {/* Probe Gradient Display (A5) */}
        <section className="bg-white rounded-xl border border-slate-200 shadow-sm p-4">
           <div className="flex justify-between items-center mb-3">
              <span className="text-xs font-bold text-slate-500 uppercase tracking-widest">Vertical Thermal Gradient (5 Depths)</span>
              <span className="text-[10px] font-bold text-slate-400 uppercase">Top to Base</span>
           </div>

           <div className="h-32 flex justify-between items-end gap-2 px-4 py-2 border-b border-slate-100">
              {probes.map((p, idx) => {
                 if (p.value === undefined || p.value === null) return (
                    <div key={p.label} className="flex flex-col items-center justify-end h-full">
                       <span className="text-[10px] font-bold text-slate-300">--</span>
                       <div className="w-8 bg-slate-100 rounded-t-md mt-1 h-4"></div>
                       <span className="text-[10px] font-bold text-slate-400 mt-2 uppercase">{p.label}</span>
                    </div>
                 );
                 const heightPct = Math.min(100, Math.max(10, (p.value / 40) * 100));
                 const isMax = idx === maxProbeIndex;
                 return (
                    <div key={p.label} className="flex flex-col items-center justify-end h-full group relative">
                       {isMax && <span className="absolute -top-5 text-[10px] font-black text-orange-600 bg-orange-100 px-1.5 py-0.5 rounded">MAX</span>}
                       <span className={`text-[10px] font-bold mb-1 ${isMax ? 'text-orange-600' : 'text-slate-600'}`}>{p.value.toFixed(1)}°</span>
                       <div className={`w-8 rounded-t-md transition-all ${isMax ? 'bg-orange-500 shadow-md shadow-orange-500/20' : 'bg-[#2d7a42]/80'}`} style={{ height: `${heightPct}%` }}></div>
                       <span className="text-[10px] font-bold text-slate-400 mt-2 uppercase">{p.label}</span>
                    </div>
                 );
              })}
           </div>
           
           <div className="mt-4 pt-3 border-t border-slate-100 flex items-center gap-2 text-sm text-slate-600 font-medium">
              <Activity className="w-4 h-4 text-slate-400" />
              Probe 4 (Core) is <span className="font-bold text-slate-800">{coreTemp !== undefined && coreTemp !== null ? `${coreTemp.toFixed(1)}°C` : '--'}</span> 
              <span className="text-slate-400">·</span> 
              <span className={`${parseFloat(delta) > 0 ? 'text-orange-600' : 'text-slate-600'} font-bold`}>+{delta}°C</span> over shell
           </div>
        </section>

        {/* Action Logger Section (A12) */}
        <section className="bg-white rounded-xl border border-slate-200 shadow-sm p-4">
          <div className="flex justify-between items-center mb-3">
            <div className="flex items-center gap-2">
              <FileText className="w-4 h-4 text-blue-600" />
              <span className="text-xs font-bold text-slate-700 uppercase tracking-wider">Field Action Log</span>
            </div>
            <button 
              onClick={() => setShowLogModal(true)}
              className="flex items-center gap-1 text-xs font-bold text-[#2d7a42] bg-green-50 px-2.5 py-1 rounded-lg border border-green-200 active:scale-95 transition-all"
            >
              <PlusCircle className="w-3.5 h-3.5" /> Log Action
            </button>
          </div>

          <div className="divide-y divide-slate-100 space-y-2">
            {logs.map(item => (
              <div key={item.id} className="pt-2 first:pt-0 flex justify-between items-start">
                <div>
                  <p className="text-xs font-bold text-slate-800">{item.action}</p>
                  <p className="text-[11px] text-slate-500">{item.detail}</p>
                </div>
                <span className="text-[10px] font-medium text-slate-400 flex items-center gap-1">
                  <Clock className="w-3 h-3" /> {item.timestamp}
                </span>
              </div>
            ))}
          </div>
        </section>

        {/* Node Metadata Footer (A6) */}
        <footer className="mt-4 text-center">
           <p className="text-xs font-bold text-slate-400 flex items-center justify-center gap-2">
              📡 Node #{telemetry?.mac_address ? telemetry.mac_address.substring(telemetry.mac_address.length - 5) : 'VK-01'} 
              · RF {telemetry?.quality === 'VALID' ? '98%' : 'Low'} 
              · FW {telemetry?.fw_version || 'v1.0'}
           </p>
           <p className="text-[10px] text-slate-400 font-medium mt-1 uppercase tracking-widest">
              Updated {timeAgo}
           </p>
        </footer>

      </main>

      {/* Action Logger Modal (A12) */}
      {showLogModal && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-end sm:items-center justify-center p-4">
          <div className="bg-white w-full max-w-sm rounded-2xl p-5 shadow-2xl animate-in slide-in-from-bottom">
            <div className="flex justify-between items-center mb-4">
              <h3 className="font-black text-slate-800 text-sm uppercase tracking-wider">Record Field Action</h3>
              <button onClick={() => setShowLogModal(false)} className="p-1 rounded-full text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3">
              <div>
                <label className="text-xs font-bold text-slate-600 block mb-1">Select Action</label>
                <select 
                  value={selectedAction} 
                  onChange={(e) => setSelectedAction(e.target.value)}
                  className="w-full text-xs font-bold p-2.5 rounded-xl border border-slate-200 bg-slate-50 outline-none focus:border-[#2d7a42]"
                >
                  <option value="Watered Bed (15L)">💧 Watered Bed (15L)</option>
                  <option value="Turned & Aerated Pile">🌀 Turned & Aerated Pile</option>
                  <option value="Added Dry Straw Bedding">🌾 Added Dry Straw Bedding</option>
                  <option value="Fed Green Waste / Fruit Peels">🥗 Fed Green Waste / Fruit Peels</option>
                  <option value="Added Rock Dust & Cow Dung Slurry">🌿 Added Rock Dust & Slurry</option>
                  <option value="Harvested Top Castings (50kg)">📦 Harvested Top Castings (50kg)</option>
                </select>
              </div>

              <div>
                <label className="text-xs font-bold text-slate-600 block mb-1">Observation Notes (Optional)</label>
                <input 
                  type="text" 
                  placeholder="e.g. core odor pleasant, high worm cluster"
                  value={actionNotes}
                  onChange={(e) => setActionNotes(e.target.value)}
                  className="w-full text-xs p-2.5 rounded-xl border border-slate-200 bg-slate-50 outline-none focus:border-[#2d7a42]"
                />
              </div>

              <div className="flex gap-2 pt-2">
                <button
                  onClick={() => setShowLogModal(false)}
                  className="flex-1 py-2.5 text-xs font-bold text-slate-600 bg-slate-100 rounded-xl active:scale-95 transition-all"
                >
                  Cancel
                </button>
                <button
                  onClick={handleAddLog}
                  className="flex-1 py-2.5 text-xs font-bold text-white bg-[#2d7a42] rounded-xl flex items-center justify-center gap-1.5 active:scale-95 transition-all shadow-md shadow-green-900/20"
                >
                  <CheckCircle2 className="w-4 h-4" /> Save Record
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
