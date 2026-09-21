"use client";

import { useState, useEffect, useMemo } from 'react';
import { fetchSites, fetchFields, fetchSiteFleet, fetchBins, getDemoBins } from '@/services/api';
import { Field, Site, FleetData, FleetNode, Bin } from '@/types';
import dynamic from 'next/dynamic';
import { Navigation, Layers, X, ChevronRight, Activity, Map as MapIcon, Globe } from 'lucide-react';
import Link from 'next/link';

const FarmMap = dynamic(() => import('@/components/FarmMap'), { ssr: false });

export default function MapPage() {
  const [sites, setSites] = useState<Site[]>([]);
  const [fields, setFields] = useState<Field[]>([]);
  const [fleet, setFleet] = useState<FleetData | null>(null);
  const [loading, setLoading] = useState(true);

  const [statusFilter, setStatusFilter] = useState<'ALL' | 'NORMAL' | 'ATTENTION' | 'WARNING' | 'OFFLINE'>('ALL');
  const [fieldFilter, setFieldFilter] = useState<string>('ALL');
  const [tileLayer, setTileLayer] = useState<'street' | 'satellite'>('satellite'); // default to satellite
  
  const [selectedNodeId, setSelectedNodeId] = useState<number | null>(null);

  useEffect(() => {
    async function loadData() {
      try {
        const [sitesData, fieldsData] = await Promise.all([fetchSites(), fetchFields()]);
        setSites(sitesData);
        setFields(fieldsData);
        
        if (sitesData.length > 0) {
          const fleetData = await fetchSiteFleet(sitesData[0].id);
          setFleet(fleetData);
        }
      } catch (e) {
        console.error("Failed to load map data", e);
      } finally {
        setLoading(false);
      }
    }
    loadData();
    const interval = setInterval(loadData, 10000);
    return () => clearInterval(interval);
  }, []);

  const filteredNodes = useMemo(() => {
    if (!fleet) return [];
    return fleet.nodes.filter(node => {
      if (fieldFilter !== 'ALL' && node.field_id !== fieldFilter) return false;
      if (statusFilter !== 'ALL') {
          if (statusFilter === 'NORMAL' && node.computed_status !== 'NORMAL') return false;
          if (statusFilter === 'OFFLINE' && node.computed_status !== 'OFFLINE') return false;
          if (statusFilter === 'ATTENTION' && (node.computed_status !== 'ACTION_NEEDED' && node.computed_status !== 'SENSOR_FAULT')) return false;
          if (statusFilter === 'WARNING' && node.computed_status !== 'WATCH') return false;
      }
      return true;
    });
  }, [fleet, fieldFilter, statusFilter]);

  const binsWithNoLocation = useMemo(() => {
     // A bin lacks location if it's in the backend bins table but maybe not in fleet, 
     // but we assume our api returns bins with lat/lon. Since we don't have lat/lon in fleet yet...
     // Wait, FleetNode doesn't have lat/lon! I missed that. 
     // I will use fetchBins to get locations, or just pretend for UI since FarmMap handles standard bins.
     // Let's pass the raw bins from fetchBins to FarmMap as we did before.
     return [];
  }, []);

  // For the map, we need the original bins since FleetNode lacks lat/lon
  const [bins, setBins] = useState<Bin[]>(getDemoBins());
  useEffect(() => {
      async function loadBins() {
          if (sites.length > 0) {
              const b = await fetchBins(sites[0].id);
              setBins(b);
          }
      }
      loadBins();
  }, [sites]);

  const mapBins = useMemo(() => {
     return bins.filter(b => {
        const node = filteredNodes.find(n => n.bin_id === b.id);
        if (!node && statusFilter !== 'ALL') return false;
        if (fieldFilter !== 'ALL' && b.field_id !== fieldFilter) return false;
        return true;
     });
  }, [bins, filteredNodes, fieldFilter, statusFilter]);

  const selectedNode = selectedNodeId ? fleet?.nodes.find(n => n.node_id === selectedNodeId) : null;
  const selectedBin = selectedNode ? bins.find(b => b.id === selectedNode.bin_id) : null;

  return (
    <main className="h-screen w-full flex flex-col relative bg-slate-900 overflow-hidden">
      
      {/* Top Filter Overlay */}
      <div className="absolute top-0 left-0 right-0 p-2 z-10 pointer-events-none pb-safe">
        <div className="bg-white/95 backdrop-blur-md rounded-xl shadow-lg pointer-events-auto border border-slate-200 flex flex-col">
          <div className="flex justify-between items-center p-3 border-b border-slate-100">
             <div>
                <h1 className="font-black text-slate-800 text-sm uppercase tracking-tight flex items-center gap-1">
                  <Navigation className="w-4 h-4 text-[#2d7a42]" /> Farm Map
                </h1>
             </div>
             <div className="flex items-center gap-2">
                 {/* Satellite Toggle (A10) */}
                 <button 
                   onClick={() => setTileLayer(t => t === 'street' ? 'satellite' : 'street')}
                   className="flex items-center gap-1 bg-slate-100 text-slate-700 px-2 py-1 rounded text-[10px] font-bold uppercase tracking-wider active:scale-95 transition-transform"
                 >
                   {tileLayer === 'street' ? <Globe className="w-3 h-3" /> : <MapIcon className="w-3 h-3" />}
                   {tileLayer === 'street' ? 'Sat' : 'Map'}
                 </button>
                 <select 
                   className="text-xs bg-slate-100 border-none rounded p-1 font-bold text-slate-700 outline-none"
                   value={fieldFilter}
                   onChange={(e) => setFieldFilter(e.target.value)}
                 >
                   <option value="ALL">All Fields</option>
                   {fields.map(f => (
                     <option key={f.id} value={f.id}>{f.name}</option>
                   ))}
                 </select>
             </div>
          </div>

          <div className="flex gap-2 p-2 overflow-x-auto scrollbar-hide snap-x">
            {['ALL', 'NORMAL', 'ATTENTION', 'WARNING', 'OFFLINE'].map((status) => (
              <button 
                key={status}
                onClick={() => setStatusFilter(status as any)}
                className={`snap-start flex-shrink-0 px-3 py-1.5 rounded-full text-[10px] font-bold uppercase tracking-wider transition-colors ${
                  statusFilter === status 
                    ? 'bg-slate-800 text-white' 
                    : 'bg-slate-100 text-slate-500 hover:bg-slate-200'
                }`}
              >
                {status}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="flex-1 w-full h-full relative z-0">
        {loading ? (
          <div className="w-full h-full flex items-center justify-center text-slate-400 font-bold">
            Loading Spatial Data...
          </div>
        ) : (
          <FarmMap 
             fields={fields} 
             bins={mapBins} 
             tileLayer={tileLayer} 
             onMarkerClick={(binId) => {
                 const node = fleet?.nodes.find(n => n.bin_id === binId);
                 if (node) setSelectedNodeId(node.node_id);
             }}
          />
        )}
      </div>

      {/* Bottom Sheet on Marker Tap (A11) */}
      <div className={`absolute bottom-[80px] left-0 right-0 p-4 transition-transform duration-300 ease-out z-20 ${selectedNode ? 'translate-y-0' : 'translate-y-[150%]'}`}>
         <div className="bg-white rounded-2xl shadow-2xl border border-slate-200 overflow-hidden flex flex-col">
            {selectedNode && (
               <>
                 <div className="p-4 border-b border-slate-100 flex justify-between items-start">
                    <div>
                        <h2 className="text-xl font-black text-slate-800 uppercase tracking-tight">{selectedNode.bin_name}</h2>
                        <p className="text-xs text-slate-500 font-medium">Field: {fields.find(f => f.id === selectedNode.field_id)?.name || 'Unknown'}</p>
                    </div>
                    <div className="flex items-start gap-2">
                        <span className={`px-2 py-1 rounded-md border text-[10px] font-black uppercase tracking-wider ${
                            selectedNode.computed_status === 'NORMAL' ? 'bg-green-50 text-green-700 border-green-200' :
                            selectedNode.computed_status === 'WATCH' ? 'bg-orange-50 text-orange-700 border-orange-200' :
                            selectedNode.computed_status === 'OFFLINE' ? 'bg-slate-100 text-slate-600 border-slate-200' :
                            'bg-red-50 text-red-700 border-red-200'
                        }`}>
                           {selectedNode.computed_status.replace('_', ' ')}
                        </span>
                        <button onClick={() => setSelectedNodeId(null)} className="p-1 rounded-full bg-slate-100 text-slate-500 hover:bg-slate-200">
                           <X className="w-4 h-4" />
                        </button>
                    </div>
                 </div>
                 <div className="p-4 bg-slate-50 grid grid-cols-2 gap-4">
                     <div>
                        <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">Temperature</p>
                        <p className="font-black text-lg text-slate-800">
                           {(selectedNode.latest_telemetry?.ambient_c ?? selectedNode.latest_telemetry?.probe_1)?.toFixed(1) || '--'}°C
                        </p>
                     </div>
                     <div>
                        <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">Moisture</p>
                        <p className="font-black text-lg text-slate-800">
                           {selectedNode.latest_telemetry?.moisture_raw || '--'}%
                        </p>
                     </div>
                 </div>
                 <div className="p-3">
                     <Link href={`/bed/${selectedNode.node_id}`} className="w-full bg-[#2d7a42] text-white py-3 rounded-xl font-bold uppercase tracking-wider text-sm flex items-center justify-center gap-2 active:scale-95 transition-transform">
                        <Activity className="w-4 h-4" /> Open Full Telemetry
                     </Link>
                 </div>
               </>
            )}
         </div>
      </div>
    </main>
  );
}
