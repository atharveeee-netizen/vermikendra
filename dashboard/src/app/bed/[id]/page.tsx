"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { fetchLatestTelemetry } from "../../../services/api";
import { useTelemetry } from "../../../hooks/useTelemetry";
import { ArrowLeft, Thermometer, Droplet, Wind, Scale, Activity, FileText, BarChart3, ChevronRight } from "lucide-react";

export default function BedDetail() {
  const params = useParams();
  const router = useRouter();
  const nodeId = parseInt(params.id as string, 10);
  const [initError, setInitError] = useState("");

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

  const currentTemp = telemetry?.ambient_c ?? telemetry?.probe_1;
  const statusColor = telemetry?.computed_status === 'ACTION_NEEDED' ? 'status-critical' :
                      telemetry?.computed_status === 'WATCH' ? 'status-warning' :
                      telemetry?.computed_status === 'SENSOR_FAULT' ? 'status-critical' :
                      'status-normal';

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

  return (
    <div className="flex flex-col min-h-screen pb-20 bg-[#F9F8F4]">
      {/* Header */}
      <header className="bg-[#2d7a42] text-white p-4 shadow-md flex items-center gap-3 sticky top-0 z-10 pb-6 rounded-b-[1.5rem]">
         <button onClick={() => router.back()} className="p-2 -ml-2 rounded-full hover:bg-green-700/50 transition-colors">
            <ArrowLeft className="w-6 h-6 text-white" />
         </button>
         <div>
            <h1 className="text-xl font-black uppercase tracking-wider">{telemetry?.bin_name || `BED ${nodeId}`}</h1>
            <p className="text-green-100 text-xs font-medium uppercase tracking-widest">{telemetry?.field_id || 'Loading...'}</p>
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
           <p className="text-xs font-medium text-slate-500 mt-1">Eisenia fetida active. Composting stage: <span className="text-slate-800 font-bold">Active</span></p>
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
                 <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Bed Mass</span>
                 <Scale className="w-4 h-4 text-slate-400" />
              </div>
              <div className="font-black text-2xl text-slate-800 mb-1">
                 {telemetry?.mass_g !== undefined && telemetry?.mass_g !== null ? `${(telemetry.mass_g/1000).toFixed(1)} kg` : '--'}
              </div>
              <div className="text-xs font-medium text-slate-400">Harvest due: <span className="text-slate-700 font-bold">12d</span></div>
           </div>
        </section>

        {/* Probe Gradient Display (A5) */}
        <section className="bg-white rounded-xl shadow-sm border border-slate-200 p-4">
           <h2 className="text-sm font-bold text-slate-500 uppercase tracking-widest mb-4 flex items-center gap-2">
              <BarChart3 className="w-4 h-4" /> Thermal Profile
           </h2>
           <div className="flex justify-between h-32 px-2 items-end">
              {probes.map((p, idx) => {
                 if (p.value === undefined || p.value === null) return (
                    <div key={p.label} className="flex flex-col items-center justify-end h-full">
                       <span className="text-[10px] font-bold text-slate-300">--</span>
                       <div className="w-8 bg-slate-100 rounded-t-md mt-1 h-4"></div>
                       <span className="text-[10px] font-bold text-slate-400 mt-2 uppercase">{p.label}</span>
                    </div>
                 );
                 // Calculate height relative to 40C max
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

        {/* Action Buttons */}
        <section className="flex flex-col gap-2 mt-2">
           <button className="w-full bg-white border border-slate-200 p-4 rounded-xl shadow-sm flex justify-between items-center active:scale-[0.98] transition-transform">
              <div className="flex items-center gap-3">
                 <div className="bg-green-50 p-2 rounded-lg">
                    <BarChart3 className="w-5 h-5 text-green-700" />
                 </div>
                 <span className="font-bold text-slate-800">Open Full Telemetry Chart</span>
              </div>
              <ChevronRight className="w-5 h-5 text-slate-400" />
           </button>
           
           <button className="w-full bg-white border border-slate-200 p-4 rounded-xl shadow-sm flex justify-between items-center active:scale-[0.98] transition-transform">
              <div className="flex items-center gap-3">
                 <div className="bg-blue-50 p-2 rounded-lg">
                    <FileText className="w-5 h-5 text-blue-600" />
                 </div>
                 <span className="font-bold text-slate-800">Log Field Action (Water/Aerate)</span>
              </div>
              <ChevronRight className="w-5 h-5 text-slate-400" />
           </button>
        </section>

        {/* Node Metadata Footer (A6) */}
        <footer className="mt-6 text-center">
           <p className="text-xs font-bold text-slate-400 flex items-center justify-center gap-2">
              📡 Node #{telemetry?.mac_address ? telemetry.mac_address.substring(telemetry.mac_address.length - 5) : 'VK-00'} 
              · RF {telemetry?.quality === 'VALID' ? '98%' : 'Low'} 
              · FW {telemetry?.fw_version || 'v1.0'}
           </p>
           <p className="text-[10px] text-slate-400 font-medium mt-1 uppercase tracking-widest">
              Updated {timeAgo}
           </p>
        </footer>

      </main>
    </div>
  );
}
