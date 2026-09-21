"use client";

import { useEffect, useState, useMemo } from "react";
import { 
  Bell, 
  CheckCircle2, 
  AlertTriangle, 
  AlertCircle, 
  FileSearch, 
  ArrowRight, 
  BookOpen, 
  HelpCircle, 
  Droplets, 
  Flame, 
  Sparkles,
  ChevronDown,
  ChevronUp
} from "lucide-react";
import { fetchSites, fetchSiteFleet } from "@/services/api";
import { FleetData } from "@/types";
import Link from "next/link";

export default function AlertsPage() {
  const [fleet, setFleet] = useState<FleetData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [resolvedIds, setResolvedIds] = useState<number[]>([]);
  const [expandedTip, setExpandedTip] = useState<number | null>(0);

  useEffect(() => {
    async function init() {
      try {
        const sites = await fetchSites();
        if (sites.length > 0) {
          const fleetData = await fetchSiteFleet(sites[0].id);
          setFleet(fleetData);
        }
      } catch (err) {
        // Fallback or silent
      } finally {
        setIsLoading(false);
      }
    }
    init();
    const interval = setInterval(init, 10000);
    return () => clearInterval(interval);
  }, []);

  const alerts = useMemo(() => {
    if (!fleet) return [];
    return fleet.nodes
      .filter(n => !resolvedIds.includes(n.node_id))
      .filter(n => n.computed_status === 'ACTION_NEEDED' || n.computed_status === 'SENSOR_FAULT' || n.computed_status === 'WATCH');
  }, [fleet, resolvedIds]);

  const handleResolve = (nodeId: number) => {
    setResolvedIds(prev => [...prev, nodeId]);
  };

  const knowledgeTips = [
    {
      title: "The Squeeze Ball Test for Bed Moisture",
      icon: <Droplets className="w-4 h-4 text-blue-500" />,
      tag: "Moisture 55-65%",
      content: "Take a handful of vermicompost from 10cm depth and squeeze firmly. If 1-2 droplets appear between knuckles, moisture is optimal (60%). If water runs out freely, bed is waterlogged (>75%) and risks anaerobic rot. If it crumbles dry, water with 25L."
    },
    {
      title: "Preventing Destructive Thermophilic Core Spikes",
      icon: <Flame className="w-4 h-4 text-orange-500" />,
      tag: "Temp < 35°C",
      content: "Eisenia fetida worms cannot survive past 35°C. When core probe reaches 34°C, immediately fork the top 15cm to release trapped biogas, scatter dry shredded straw, and apply cool water spray. Do not add raw green cow dung all at once."
    },
    {
      title: "Recognizing Premium Harvest Castings",
      icon: <Sparkles className="w-4 h-4 text-emerald-600" />,
      tag: "Harvest Ready",
      content: "Ready vermicompost is dark brownish-black with a rich forest-floor earthy aroma, granular spongy texture, and zero foul smell. Stop watering 3 days before harvesting so worms migrate downwards, allowing clean top scraping."
    }
  ];

  return (
    <main className="min-h-screen bg-[#F9F8F4] p-4 md:p-8 pb-28 max-w-lg mx-auto">
      <header className="mb-6 flex justify-between items-end">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Bell className="w-5 h-5 text-red-600" />
            <span className="text-xs font-bold text-red-600 uppercase tracking-widest">Diagnostics</span>
          </div>
          <h1 className="text-2xl font-black tracking-tight text-slate-800 uppercase">Farm Alerts</h1>
          <p className="text-slate-500 text-xs font-medium flex items-center gap-1.5 mt-1">
            <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
            Live Gateway Health Monitor
          </p>
        </div>
        <div className="bg-red-100 text-red-700 px-3 py-1 rounded-full font-black text-xs">
          {alerts.length} Active
        </div>
      </header>

      {/* Filter summary - A7 */}
      {alerts.length > 0 && (
         <div className="flex gap-2 overflow-x-auto pb-4 scrollbar-hide snap-x">
            <span className="snap-start whitespace-nowrap px-3.5 py-1.5 rounded-full text-xs font-bold bg-slate-800 text-white">
                All ({alerts.length})
            </span>
            <span className="snap-start whitespace-nowrap px-3.5 py-1.5 rounded-full text-xs font-bold bg-white text-slate-600 border border-slate-200">
                Critical ({fleet?.stats.critical || 0})
            </span>
            <span className="snap-start whitespace-nowrap px-3.5 py-1.5 rounded-full text-xs font-bold bg-white text-slate-600 border border-slate-200">
                Warning ({fleet?.stats.attention || 0})
            </span>
         </div>
      )}

      {/* Active Alerts List */}
      <div className="space-y-4">
        {isLoading ? (
          <div className="text-center p-8 text-slate-400 font-bold">Checking bed sensor fleet...</div>
        ) : alerts.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-12 px-6 bg-white rounded-2xl border border-slate-200 text-center shadow-sm">
            <div className="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center mb-3">
              <CheckCircle2 className="w-7 h-7 text-green-600" />
            </div>
            <h3 className="text-lg font-black tracking-tight text-slate-800 uppercase">All Beds Operating Normally</h3>
            <p className="text-slate-500 text-xs mt-1.5 max-w-xs mx-auto font-medium">
              Every vermicomposting bed is within optimal moisture and thermal limits. Worm activity is flourishing.
            </p>
          </div>
        ) : (
          alerts.map(alert => {
            const isCritical = alert.computed_status === 'ACTION_NEEDED' || alert.computed_status === 'SENSOR_FAULT';
            
            // Agronomy Advice Logic (A8)
            let advice = "Inspect the bed for anomalies and verify surface shading.";
            if (alert.computed_reason?.includes('high') || alert.computed_reason?.includes('Overheating')) {
               advice = "Turn the upper 15cm layer with a pitchfork to release heat. Water top surface with 25L and draw shading net.";
            } else if (alert.computed_reason?.includes('low') || alert.computed_reason?.includes('Moisture')) {
               advice = "Moisture is below 50%. Apply gentle sprinkling of 30L clean water. Ensure drainage hole is unblocked.";
            } else if (alert.computed_status === 'SENSOR_FAULT') {
               advice = "Hardware probe offline or disconnected. Check the 5-point sensor cable connector and battery charge.";
            }

            return (
              <div key={alert.node_id} className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm">
                 <div className={`p-4 border-b ${isCritical ? 'bg-red-50 border-red-100' : 'bg-orange-50 border-orange-100'}`}>
                    <div className="flex items-center justify-between mb-1.5">
                       <div className="flex items-center gap-2">
                          {isCritical ? <AlertCircle className="w-5 h-5 text-red-600" /> : <AlertTriangle className="w-5 h-5 text-orange-600" />}
                          <h3 className={`font-black text-base tracking-tight uppercase ${isCritical ? 'text-red-700' : 'text-orange-700'}`}>
                             {alert.bin_name}
                          </h3>
                       </div>
                       <span className={`text-[10px] font-black uppercase px-2 py-0.5 rounded-full ${isCritical ? 'bg-red-200/70 text-red-800' : 'bg-orange-200/70 text-orange-800'}`}>
                          {alert.computed_status.replace('_', ' ')}
                       </span>
                    </div>
                    <p className="text-xs font-bold text-slate-700">
                       {alert.computed_reason}
                    </p>
                 </div>
                 
                 <div className="p-4 bg-white">
                    <div className="bg-slate-50 border border-slate-100 rounded-xl p-3">
                       <h4 className="text-[10px] font-black text-[#2d7a42] uppercase tracking-widest flex items-center gap-1.5 mb-1.5">
                          <span>🧑‍🌾</span> Agronomist Remediation Action
                       </h4>
                       <p className="text-xs font-medium text-slate-700 leading-relaxed">
                          {advice}
                       </p>
                    </div>
                 </div>

                 <div className="bg-slate-50 p-3 flex gap-2 border-t border-slate-100">
                    <Link 
                      href={`/bed/${alert.node_id}`} 
                      className="flex-1 bg-white border border-slate-200 py-2.5 rounded-xl text-xs font-bold text-slate-700 flex justify-center items-center gap-1.5 active:scale-95 transition-all shadow-sm"
                    >
                       <FileSearch className="w-3.5 h-3.5 text-slate-500" /> Inspect Bed
                    </Link>
                    <button 
                      onClick={() => handleResolve(alert.node_id)}
                      className="flex-1 bg-[#2d7a42] text-white py-2.5 rounded-xl text-xs font-bold flex justify-center items-center gap-1.5 active:scale-95 transition-all shadow-md shadow-green-900/20"
                    >
                       Mark Resolved <ArrowRight className="w-3.5 h-3.5" />
                    </button>
                 </div>
              </div>
            );
          })
        )}

        {/* Agronomy Knowledge Feed (A22) */}
        <section className="mt-8 pt-4 border-t border-slate-200">
          <div className="flex items-center gap-2 mb-3">
            <BookOpen className="w-4 h-4 text-[#2d7a42]" />
            <h2 className="text-xs font-bold text-slate-500 uppercase tracking-wider">Field Agronomy Handbook</h2>
          </div>

          <div className="space-y-2.5">
            {knowledgeTips.map((tip, idx) => {
              const isOpen = expandedTip === idx;
              return (
                <div key={idx} className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
                  <button 
                    onClick={() => setExpandedTip(isOpen ? null : idx)}
                    className="w-full p-3.5 flex items-center justify-between text-left hover:bg-slate-50 transition-colors"
                  >
                    <div className="flex items-center gap-2.5">
                      {tip.icon}
                      <div>
                        <p className="text-xs font-bold text-slate-800">{tip.title}</p>
                        <span className="text-[10px] font-bold text-[#2d7a42] uppercase">{tip.tag}</span>
                      </div>
                    </div>
                    {isOpen ? <ChevronUp className="w-4 h-4 text-slate-400" /> : <ChevronDown className="w-4 h-4 text-slate-400" />}
                  </button>
                  {isOpen && (
                    <div className="px-3.5 pb-3.5 pt-1 text-xs text-slate-600 leading-relaxed border-t border-slate-100 bg-slate-50/50">
                      {tip.content}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </section>

      </div>
    </main>
  );
}
