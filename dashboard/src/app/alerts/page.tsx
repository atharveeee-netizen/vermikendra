"use client";

import { useEffect, useState, useMemo } from "react";
import { Bell, CheckCircle2, AlertTriangle, AlertCircle, FileSearch, ArrowRight } from "lucide-react";
import { fetchSites, fetchSiteFleet } from "@/services/api";
import { FleetData } from "@/types";
import Link from "next/link";

export default function AlertsPage() {
  const [fleet, setFleet] = useState<FleetData | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function init() {
      try {
        const sites = await fetchSites();
        if (sites.length > 0) {
          const fleetData = await fetchSiteFleet(sites[0].id);
          setFleet(fleetData);
        }
      } catch (err) {
        // Handle error silently for now
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
    return fleet.nodes.filter(n => n.computed_status === 'ACTION_NEEDED' || n.computed_status === 'SENSOR_FAULT' || n.computed_status === 'WATCH');
  }, [fleet]);

  return (
    <main className="min-h-screen bg-[#F9F8F4] p-4 md:p-8 pb-24">
      <header className="mb-6 flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-black tracking-tight text-slate-800 uppercase">Alerts</h1>
          <p className="text-slate-500 font-medium flex items-center gap-2 mt-1">
            <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
            Active Diagnostics
          </p>
        </div>
        <div className="bg-red-100 text-red-700 px-3 py-1 rounded-full font-black text-sm">
          {alerts.length} Unresolved
        </div>
      </header>

      {/* Filter summary - A7 */}
      {alerts.length > 0 && (
         <div className="flex gap-2 overflow-x-auto pb-4 scrollbar-hide snap-x">
            <span className="snap-start whitespace-nowrap px-4 py-1.5 rounded-full text-xs font-bold bg-slate-800 text-white">
                All ({alerts.length})
            </span>
            <span className="snap-start whitespace-nowrap px-4 py-1.5 rounded-full text-xs font-bold bg-white text-slate-600 border border-slate-200">
                Critical ({fleet?.stats.critical || 0})
            </span>
            <span className="snap-start whitespace-nowrap px-4 py-1.5 rounded-full text-xs font-bold bg-white text-slate-600 border border-slate-200">
                Warning ({fleet?.stats.attention || 0})
            </span>
         </div>
      )}

      <div className="space-y-4">
        {isLoading ? (
          <div className="text-center p-8 text-slate-400 font-bold">Checking systems...</div>
        ) : alerts.length === 0 ? (
          <div className="vk-card flex flex-col items-center justify-center py-16 bg-white text-center border-slate-200 border">
            <CheckCircle2 className="w-16 h-16 text-green-500 mb-4" />
            <h3 className="text-xl font-black tracking-tight text-slate-800 uppercase">All Clear!</h3>
            <p className="text-slate-500 mt-2 max-w-xs mx-auto font-medium">
              Your compost beds are operating within optimal parameters. No active alerts.
            </p>
          </div>
        ) : (
          alerts.map(alert => {
            const isCritical = alert.computed_status === 'ACTION_NEEDED' || alert.computed_status === 'SENSOR_FAULT';
            
            // Agronomy Advice Logic (A8)
            let advice = "Inspect the bed for anomalies.";
            if (alert.computed_reason?.includes('high')) {
               advice = "Water top layer with 35L immediately or draw extra shade net to reduce core temperature.";
            } else if (alert.computed_reason?.includes('low')) {
               advice = "Add moisture. Ensure drainage is not blocked. Mix fresh substrate.";
            } else if (alert.computed_status === 'SENSOR_FAULT') {
               advice = "Hardware fault detected. Check sensor connections and battery level.";
            }

            return (
              <div key={alert.node_id} className="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm">
                 <div className={`p-4 border-b ${isCritical ? 'bg-red-50 border-red-100' : 'bg-orange-50 border-orange-100'}`}>
                    <div className="flex items-center gap-2 mb-2">
                       {isCritical ? <AlertCircle className="w-5 h-5 text-red-600" /> : <AlertTriangle className="w-5 h-5 text-orange-600" />}
                       <h3 className={`font-black text-lg tracking-tight uppercase ${isCritical ? 'text-red-700' : 'text-orange-700'}`}>
                          {alert.bin_name}
                       </h3>
                    </div>
                    <p className={`text-xs font-bold uppercase tracking-widest ${isCritical ? 'text-red-600' : 'text-orange-600'}`}>
                       {alert.computed_status.replace('_', ' ')}
                    </p>
                 </div>
                 
                 <div className="p-4">
                    <p className="text-sm font-bold text-slate-800 mb-4 bg-slate-50 p-3 rounded-lg border border-slate-100">
                       {alert.computed_reason}
                    </p>
                    
                    <div className="border-t-2 border-dashed border-slate-200 my-4"></div>
                    
                    <div>
                       <h4 className="text-[10px] font-black text-slate-400 uppercase tracking-widest flex items-center gap-1.5 mb-2">
                          <span className="text-lg">🧑‍🌾</span> Recommended Action
                       </h4>
                       <p className="text-sm font-medium text-slate-700 leading-relaxed">
                          {advice}
                       </p>
                    </div>
                 </div>

                 <div className="bg-slate-50 p-2 flex gap-2 border-t border-slate-100">
                    <Link href={`/bed/${alert.node_id}`} className="flex-1 bg-white border border-slate-200 py-3 rounded-lg text-sm font-bold text-slate-700 flex justify-center items-center gap-2 active:scale-95 transition-transform hover:border-slate-300">
                       <FileSearch className="w-4 h-4" /> Inspect Bed
                    </Link>
                    <button className="flex-1 bg-[#2d7a42] border border-[#2d7a42] py-3 rounded-lg text-sm font-bold text-white flex justify-center items-center gap-2 active:scale-95 transition-transform">
                       Resolve <ArrowRight className="w-4 h-4" />
                    </button>
                 </div>
              </div>
            )
          })
        )}
      </div>
    </main>
  );
}
