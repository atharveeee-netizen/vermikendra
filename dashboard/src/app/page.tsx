"use client";

import { useEffect, useState, useMemo } from "react";
import Link from "next/link";
import { fetchSites, fetchFields, fetchSiteFleet } from "../services/api";
import { Site, Field, FleetData, FleetNode } from "../types";
import { Thermometer, Droplet, Activity, ChevronRight, CheckCircle2, AlertTriangle, XCircle, CloudSun, AlertCircle } from "lucide-react";

export default function Home() {
  const [site, setSite] = useState<Site | null>(null);
  const [fields, setFields] = useState<Field[]>([]);
  const [fleet, setFleet] = useState<FleetData | null>(null);
  const [initError, setInitError] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [filter, setFilter] = useState<'ALL' | 'ATTENTION' | 'NORMAL' | 'OFFLINE'>('ALL');

  useEffect(() => {
    async function discover() {
      try {
        const [sites, fieldsData] = await Promise.all([fetchSites(), fetchFields()]);
        if (sites.length > 0) {
          const currentSite = sites[0];
          setSite(currentSite);
          setFields(fieldsData);
          
          const fleetData = await fetchSiteFleet(currentSite.id);
          setFleet(fleetData);
        } else {
          setInitError("No sites configured.");
        }
      } catch (err) {
        setInitError("Cannot reach Vermikendra gateway.");
      } finally {
        setIsLoading(false);
      }
    }
    discover();
    
    // Polling every 10 seconds for real-time fleet updates
    const interval = setInterval(discover, 10000);
    return () => clearInterval(interval);
  }, []);

  const filteredNodes = useMemo(() => {
    if (!fleet) return [];
    if (filter === 'ALL') return fleet.nodes;
    if (filter === 'ATTENTION') return fleet.nodes.filter(n => n.computed_status === 'ACTION_NEEDED' || n.computed_status === 'WATCH' || n.computed_status === 'SENSOR_FAULT');
    if (filter === 'NORMAL') return fleet.nodes.filter(n => n.computed_status === 'NORMAL');
    if (filter === 'OFFLINE') return fleet.nodes.filter(n => n.computed_status === 'OFFLINE');
    return fleet.nodes;
  }, [fleet, filter]);

  if (initError) {
    return <div className="p-8 text-red-600 font-bold">{initError}</div>;
  }

  // Calculate Averages for A19
  const avgTemp = useMemo(() => {
    if (!fleet) return null;
    const nodesWithTemp = fleet.nodes.filter(n => n.latest_telemetry && (n.latest_telemetry.ambient_c ?? n.latest_telemetry.probe_1) !== null);
    if (nodesWithTemp.length === 0) return null;
    const sum = nodesWithTemp.reduce((acc, n) => acc + (n.latest_telemetry!.ambient_c ?? n.latest_telemetry!.probe_1 ?? 0), 0);
    return (sum / nodesWithTemp.length).toFixed(1);
  }, [fleet]);

  const avgMoisture = useMemo(() => {
    if (!fleet) return null;
    const nodesWithMoisture = fleet.nodes.filter(n => n.latest_telemetry && n.latest_telemetry.moisture_raw !== null);
    if (nodesWithMoisture.length === 0) return null;
    const sum = nodesWithMoisture.reduce((acc, n) => acc + n.latest_telemetry!.moisture_raw!, 0);
    return Math.round(sum / nodesWithMoisture.length);
  }, [fleet]);

  return (
    <div className="flex flex-col min-h-screen pb-24 bg-[#F9F8F4]">
      {/* Header - A1 */}
      <header className="bg-[#2d7a42] text-white p-5 pb-8 rounded-b-[2rem] shadow-md relative z-10">
        <div className="flex justify-between items-start mb-4">
           <div>
             <div className="flex items-center gap-2 mb-1">
                <span className="text-xs font-bold text-green-200 uppercase tracking-widest">Site</span>
                <span className="flex items-center gap-1 text-xs bg-green-800/40 px-2 py-0.5 rounded-full font-medium">
                   <div className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse"></div> Gateway Online
                </span>
             </div>
             <h1 className="text-2xl font-black uppercase tracking-wider">{site?.name || "Loading..."}</h1>
           </div>
        </div>

        {/* Weather placeholder (A9) */}
        <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-xl p-3 flex justify-between items-center mt-2">
            <div>
               <p className="text-xs text-green-100 font-medium">Pune, Maharashtra</p>
               <div className="flex items-center gap-3 mt-1">
                  <CloudSun className="w-5 h-5 text-yellow-300" />
                  <span className="font-bold">29° Clear</span>
               </div>
            </div>
            <div className="text-right flex items-center gap-4 text-sm font-medium">
               <span className="flex items-center gap-1"><Droplet className="w-3 h-3 text-blue-300" /> 17%</span>
               <span>🌬️ 12km/h</span>
            </div>
        </div>
      </header>

      <main className="p-4 flex flex-col gap-5 max-w-lg mx-auto w-full -mt-4 relative z-20">
        
        {/* Quick Stats Row - A19 */}
        <div className="grid grid-cols-4 gap-2">
           <div className="bg-white rounded-xl p-3 border border-slate-200 shadow-sm flex flex-col items-center justify-center text-center">
              <Thermometer className="w-5 h-5 text-orange-500 mb-1" />
              <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Avg Temp</span>
              <span className="font-black text-slate-800">{avgTemp ? `${avgTemp}°` : '--'}</span>
           </div>
           <div className="bg-white rounded-xl p-3 border border-slate-200 shadow-sm flex flex-col items-center justify-center text-center">
              <Droplet className="w-5 h-5 text-blue-500 mb-1" />
              <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Moisture</span>
              <span className="font-black text-slate-800">{avgMoisture ? `${avgMoisture}%` : '--'}</span>
           </div>
           <div className="bg-white rounded-xl p-3 border border-slate-200 shadow-sm flex flex-col items-center justify-center text-center">
              <CheckCircle2 className="w-5 h-5 text-green-500 mb-1" />
              <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Online</span>
              <span className="font-black text-slate-800">{fleet?.stats.online || 0}/{fleet?.stats.total || 0}</span>
           </div>
           <div className="bg-white rounded-xl p-3 border border-slate-200 shadow-sm flex flex-col items-center justify-center text-center">
              <AlertTriangle className={`w-5 h-5 mb-1 ${fleet && fleet.stats.critical > 0 ? 'text-red-500' : 'text-slate-400'}`} />
              <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Alerts</span>
              <span className="font-black text-slate-800">{fleet?.stats.critical || 0}</span>
           </div>
        </div>

        {/* Filter Tabs - A3 */}
        <div className="flex gap-2 overflow-x-auto pb-2 scrollbar-hide snap-x">
            <button 
                onClick={() => setFilter('ALL')}
                className={`snap-start whitespace-nowrap px-4 py-1.5 rounded-full text-xs font-bold transition-all border ${filter === 'ALL' ? 'bg-slate-800 text-white border-slate-800' : 'bg-white text-slate-600 border-slate-200'}`}
            >
                All ({fleet?.stats.total || 0})
            </button>
            <button 
                onClick={() => setFilter('ATTENTION')}
                className={`flex items-center gap-1 snap-start whitespace-nowrap px-4 py-1.5 rounded-full text-xs font-bold transition-all border ${filter === 'ATTENTION' ? 'bg-red-50 text-red-700 border-red-200' : 'bg-white text-slate-600 border-slate-200'}`}
            >
                <div className={`w-2 h-2 rounded-full ${fleet && fleet.stats.critical > 0 ? 'bg-red-500' : fleet && fleet.stats.attention > 0 ? 'bg-orange-500' : 'bg-slate-300'}`}></div>
                Attention ({(fleet?.stats.critical || 0) + (fleet?.stats.attention || 0)})
            </button>
            <button 
                onClick={() => setFilter('NORMAL')}
                className={`flex items-center gap-1 snap-start whitespace-nowrap px-4 py-1.5 rounded-full text-xs font-bold transition-all border ${filter === 'NORMAL' ? 'bg-green-50 text-green-700 border-green-200' : 'bg-white text-slate-600 border-slate-200'}`}
            >
                <div className="w-2 h-2 rounded-full bg-green-500"></div>
                Normal ({fleet?.stats.normal || 0})
            </button>
            <button 
                onClick={() => setFilter('OFFLINE')}
                className={`flex items-center gap-1 snap-start whitespace-nowrap px-4 py-1.5 rounded-full text-xs font-bold transition-all border ${filter === 'OFFLINE' ? 'bg-slate-200 text-slate-700 border-slate-300' : 'bg-white text-slate-600 border-slate-200'}`}
            >
                <div className="w-2 h-2 rounded-full bg-slate-400"></div>
                Offline ({fleet?.stats.offline || 0})
            </button>
        </div>

        {/* Fleet List */}
        <div className="flex flex-col gap-3">
            {isLoading ? (
                <div className="text-center p-8 text-slate-400 font-bold">Loading fleet data...</div>
            ) : filteredNodes.length === 0 ? (
                <div className="vk-card text-center py-12 text-slate-500">
                    <CheckCircle2 className="w-12 h-12 text-slate-300 mx-auto mb-3" />
                    <p className="font-medium">No beds found for this filter.</p>
                </div>
            ) : (
                filteredNodes.map((node) => {
                    const field = fields.find(f => f.id === node.field_id);
                    const temp = node.latest_telemetry?.ambient_c ?? node.latest_telemetry?.probe_1;
                    const moisture = node.latest_telemetry?.moisture_raw;
                    
                    let statusColor = "bg-slate-100 text-slate-600 border-slate-200";
                    let dotColor = "bg-slate-400";
                    if (node.computed_status === 'NORMAL') {
                        statusColor = "bg-green-50 text-green-700 border-green-200";
                        dotColor = "bg-green-500";
                    } else if (node.computed_status === 'WATCH') {
                        statusColor = "bg-orange-50 text-orange-700 border-orange-200";
                        dotColor = "bg-orange-500";
                    } else if (node.computed_status === 'ACTION_NEEDED' || node.computed_status === 'SENSOR_FAULT') {
                        statusColor = "bg-red-50 text-red-700 border-red-200";
                        dotColor = "bg-red-500 animate-pulse";
                    }

                    return (
                        <Link href={`/bed/${node.node_id}`} key={node.node_id} className="block">
                            <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm hover:border-[#2d7a42] transition-colors active:scale-[0.98]">
                                <div className="flex justify-between items-start mb-3">
                                    <div>
                                        <h3 className="font-black text-slate-800 text-lg uppercase tracking-tight">{node.bin_name}</h3>
                                        <p className="text-xs text-slate-500 font-medium mt-0.5">
                                            {field?.name || 'Unassigned'}
                                        </p>
                                    </div>
                                    <div className={`flex items-center gap-1.5 px-2 py-1 rounded-md border text-[10px] font-black uppercase tracking-wider ${statusColor}`}>
                                        <div className={`w-1.5 h-1.5 rounded-full ${dotColor}`}></div>
                                        {node.computed_status === 'ACTION_NEEDED' ? 'ALERT' : node.computed_status === 'WATCH' ? 'WARNING' : node.computed_status}
                                    </div>
                                </div>
                                
                                <div className="grid grid-cols-2 gap-2 mt-4">
                                    <div>
                                        <div className="flex items-center gap-1.5 mb-1">
                                            <Thermometer className="w-3.5 h-3.5 text-slate-400" />
                                            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Core Temp</span>
                                        </div>
                                        <div className="font-black text-xl text-slate-800">
                                            {temp !== undefined && temp !== null ? `${temp.toFixed(1)}°C` : <span className="text-slate-300">No Data</span>}
                                        </div>
                                    </div>
                                    <div>
                                        <div className="flex items-center gap-1.5 mb-1">
                                            <Droplet className="w-3.5 h-3.5 text-slate-400" />
                                            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Moisture</span>
                                        </div>
                                        <div className="font-black text-xl text-slate-800">
                                            {moisture !== undefined && moisture !== null ? `${moisture}%` : <span className="text-slate-300">No Data</span>}
                                        </div>
                                    </div>
                                </div>
                                
                                {node.computed_reason && node.computed_status !== 'NORMAL' && node.computed_status !== 'OFFLINE' && (
                                    <div className="mt-3 bg-red-50/50 rounded-lg p-2 flex items-start gap-2 border border-red-100">
                                        <AlertCircle className="w-4 h-4 text-red-500 shrink-0 mt-0.5" />
                                        <span className="text-xs font-medium text-red-800 leading-snug">{node.computed_reason}</span>
                                    </div>
                                )}
                            </div>
                        </Link>
                    )
                })
            )}
        </div>
      </main>
    </div>
  );
}
