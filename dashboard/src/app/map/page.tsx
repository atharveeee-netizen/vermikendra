'use client';

import { MapPin, Navigation } from 'lucide-react';

export default function MapPage() {
  return (
    <main className="min-h-screen bg-slate-100 flex flex-col pb-20 relative">
      {/* Search / Header overlay */}
      <div className="absolute top-0 left-0 right-0 p-4 z-10 pointer-events-none">
         <div className="bg-white/90 backdrop-blur-md rounded-xl shadow-lg p-4 pointer-events-auto border border-slate-200 flex justify-between items-center">
            <div>
               <h1 className="font-black text-slate-800 text-lg uppercase tracking-tight">Farm Map</h1>
               <p className="text-xs text-slate-500 font-medium">Viewing 1 active site</p>
            </div>
            <button className="p-2 bg-slate-100 rounded-full text-slate-600 hover:bg-slate-200">
               <Navigation className="w-5 h-5" />
            </button>
         </div>
      </div>

      {/* Fake Map Background using CSS pattern to simulate a grid/satellite view placeholder */}
      <div className="flex-1 bg-[#e5e5f7] relative w-full h-full" style={{ backgroundImage: 'radial-gradient(#444cf7 0.5px, #e5e5f7 0.5px)', backgroundSize: '10px 10px' }}>
         
         {/* Map Pins */}
         <div className="absolute top-[40%] left-[30%] flex flex-col items-center group cursor-pointer">
            <div className="bg-white p-1 rounded-full shadow-lg border-2 border-[#2d7a42] group-hover:scale-110 transition-transform">
               <MapPin className="w-6 h-6 text-[#2d7a42] fill-green-100" />
            </div>
            <span className="mt-1 bg-white px-2 py-1 rounded text-[10px] font-bold shadow-sm uppercase tracking-wider text-slate-700">Bed 1</span>
         </div>
         
         <div className="absolute top-[45%] left-[60%] flex flex-col items-center group cursor-pointer">
            <div className="bg-white p-1 rounded-full shadow-lg border-2 border-slate-300 group-hover:scale-110 transition-transform">
               <MapPin className="w-6 h-6 text-slate-400 fill-slate-100" />
            </div>
            <span className="mt-1 bg-white px-2 py-1 rounded text-[10px] font-bold shadow-sm uppercase tracking-wider text-slate-700">Bed 2 (Offline)</span>
         </div>

      </div>

      {/* Bottom Sheet overlay */}
      <div className="absolute bottom-20 left-4 right-4 bg-white rounded-xl shadow-xl p-4 border border-slate-200">
         <h3 className="font-bold text-slate-800 uppercase text-sm mb-2">Location Summary</h3>
         <p className="text-slate-600 text-xs leading-relaxed">
            All active vermicompost beds are currently located in Zone A. No spatial anomalies detected.
         </p>
      </div>
    </main>
  );
}
