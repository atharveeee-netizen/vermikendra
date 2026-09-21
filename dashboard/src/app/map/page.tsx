'use client';

import { useState, useEffect } from 'react';
import { fetchBins, fetchFields, fetchSites } from '@/services/api';
import { Bin, Field, Site } from '@/types';
import dynamic from 'next/dynamic';
import { Navigation, Filter } from 'lucide-react';

// Leaflet relies on window, must be loaded dynamically without SSR
const FarmMap = dynamic(() => import('@/components/FarmMap'), { ssr: false });

export default function MapPage() {
  const [sites, setSites] = useState<Site[]>([]);
  const [fields, setFields] = useState<Field[]>([]);
  const [bins, setBins] = useState<Bin[]>([]);
  const [loading, setLoading] = useState(true);

  // Filter state
  const [statusFilter, setStatusFilter] = useState<'ALL' | 'NORMAL' | 'ATTENTION' | 'WARNING' | 'OFFLINE'>('ALL');
  const [fieldFilter, setFieldFilter] = useState<string>('ALL');

  useEffect(() => {
    async function loadData() {
      try {
        const [sitesData, fieldsData] = await Promise.all([fetchSites(), fetchFields()]);
        setSites(sitesData);
        setFields(fieldsData);
        
        if (sitesData.length > 0) {
          const binsData = await fetchBins(sitesData[0].id);
          setBins(binsData);
        }
      } catch (e) {
        console.error("Failed to load map data", e);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  // Filter Bins based on state
  // In a real implementation with live telemetry, we'd filter by computed status.
  // Since we only have static bins here, status filtering is UI-only for now.
  const filteredBins = bins.filter(bin => {
    if (fieldFilter !== 'ALL' && bin.field_id !== fieldFilter) return false;
    return true;
  });

  const binsWithNoLocation = filteredBins.filter(b => !b.latitude || !b.longitude);

  return (
    <main className="h-screen w-full flex flex-col relative bg-slate-100 overflow-hidden">
      
      {/* Map Filter Overlay */}
      <div className="absolute top-0 left-0 right-0 p-2 z-10 pointer-events-none safe-area-pt">
        <div className="bg-white/95 backdrop-blur-md rounded-xl shadow-lg pointer-events-auto border border-slate-200 flex flex-col">
          {/* Top Row: Title & Actions */}
          <div className="flex justify-between items-center p-3 border-b border-slate-100">
             <div>
                <h1 className="font-black text-slate-800 text-sm uppercase tracking-tight flex items-center gap-1">
                  <Navigation className="w-4 h-4 text-green-700" /> Farm Map
                </h1>
             </div>
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

          {/* Bottom Row: Status Filters */}
          <div className="flex gap-2 p-2 overflow-x-auto no-scrollbar">
            {['ALL', 'NORMAL', 'ATTENTION', 'WARNING', 'OFFLINE'].map((status) => (
              <button 
                key={status}
                onClick={() => setStatusFilter(status as any)}
                className={`flex-shrink-0 px-3 py-1.5 rounded-full text-[10px] font-bold uppercase tracking-wider transition-colors ${
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

      {/* The Actual Map */}
      <div className="flex-1 w-full h-full relative z-0">
        {loading ? (
          <div className="w-full h-full flex items-center justify-center text-slate-500">
            Loading Spatial Data...
          </div>
        ) : (
          <FarmMap fields={fields} bins={filteredBins} />
        )}
      </div>

      {/* No Location Overlay */}
      {binsWithNoLocation.length > 0 && (
        <div className="absolute bottom-[90px] left-4 right-4 bg-white/95 backdrop-blur rounded-xl shadow-xl p-3 border border-slate-200 z-10">
          <div className="flex justify-between items-center">
            <h3 className="font-bold text-slate-800 uppercase text-[10px] tracking-wider">Unmapped Assets</h3>
            <span className="bg-slate-100 text-slate-500 px-2 py-0.5 rounded text-[10px] font-bold">{binsWithNoLocation.length}</span>
          </div>
          <div className="mt-2 flex flex-wrap gap-2">
            {binsWithNoLocation.map(bin => (
              <span key={bin.id} className="text-[10px] font-medium bg-slate-50 border border-slate-100 px-2 py-1 rounded text-slate-600">
                {bin.name}
              </span>
            ))}
          </div>
        </div>
      )}
    </main>
  );
}
