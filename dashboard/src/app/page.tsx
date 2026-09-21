"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { fetchSites, fetchBins, fetchNodes } from "../services/api";
import { Site, Bin, Node } from "../types";
import { Activity, Thermometer, Droplet, ChevronRight } from "lucide-react";

export default function Home() {
  const [site, setSite] = useState<Site | null>(null);
  const [bins, setBins] = useState<Bin[]>([]);
  const [nodes, setNodes] = useState<Node[]>([]);
  const [initError, setInitError] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function discover() {
      try {
        const sites = await fetchSites();
        if (sites.length > 0) {
          setSite(sites[0]);
          const siteBins = await fetchBins(sites[0].id);
          setBins(siteBins);
          
          // Fetch nodes for all bins (simplified for fleet view)
          let allNodes: Node[] = [];
          for (const b of siteBins) {
            const bNodes = await fetchNodes(b.id);
            allNodes = [...allNodes, ...bNodes];
          }
          setNodes(allNodes);
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
  }, []);

  if (initError) {
    return <div className="p-8 text-red-600 font-bold">{initError}</div>;
  }

  return (
    <div className="flex flex-col min-h-screen pb-24">
      <header className="bg-[#2d7a42] text-white p-6 shadow-md rounded-b-3xl mb-4">
        <h1 className="text-2xl font-black uppercase tracking-wider">{site?.name || "Loading..."}</h1>
        <p className="text-green-100 font-medium opacity-90 mt-1">
          {nodes.length} Active Nodes • Operations normal
        </p>
      </header>

      <main className="p-4 flex flex-col gap-4 max-w-lg mx-auto w-full">
        <div className="flex justify-between items-end mb-2 px-1">
          <h2 className="text-lg font-bold text-slate-800">Bed Fleet Status</h2>
          <span className="text-xs font-bold text-slate-400 uppercase tracking-widest">Active Only</span>
        </div>

        {isLoading ? (
           <div className="text-center p-8 text-slate-400">Loading fleet data...</div>
        ) : nodes.length === 0 ? (
           <div className="vk-card text-center py-8 text-slate-500">No beds connected.</div>
        ) : (
          nodes.map((node) => (
            <Link href={`/bed/${node.id}`} key={node.id} className="block">
              <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm hover:border-[#2d7a42] transition-colors active:scale-[0.98]">
                <div className="flex justify-between items-center mb-3">
                  <div className="flex items-center gap-3">
                     <div className="w-10 h-10 bg-green-50 rounded-full flex items-center justify-center">
                        <Activity className="w-5 h-5 text-[#2d7a42]" />
                     </div>
                     <div>
                       <h3 className="font-bold text-slate-800 text-lg uppercase">Node {node.id}</h3>
                       <p className="text-xs text-slate-500">{bins.find(b => b.id === node.bin_id)?.name || "Unknown Bin"}</p>
                     </div>
                  </div>
                  <span className="status-normal text-[10px]">ACTIVE</span>
                </div>
                
                <div className="grid grid-cols-2 gap-2 mt-3 p-3 bg-slate-50 rounded-lg">
                  <div className="flex items-center gap-2">
                    <Thermometer className="w-4 h-4 text-orange-500" />
                    <span className="text-sm font-bold text-slate-700">-- °C</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Droplet className="w-4 h-4 text-blue-500" />
                    <span className="text-sm font-bold text-slate-700">-- %</span>
                  </div>
                </div>
                
                <div className="mt-3 flex justify-end">
                  <span className="text-xs font-bold text-[#2d7a42] flex items-center gap-1 uppercase tracking-wider">
                    View Telemetry <ChevronRight className="w-4 h-4" />
                  </span>
                </div>
              </div>
            </Link>
          ))
        )}
      </main>
    </div>
  );
}
