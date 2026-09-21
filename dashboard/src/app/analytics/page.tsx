'use client';

import { LineChart, Clock, TrendingUp } from 'lucide-react';

export default function AnalyticsPage() {
  return (
    <main className="min-h-screen bg-[#F9F8F4] p-4 md:p-8 pb-24">
      <header className="mb-6">
        <h1 className="text-3xl font-black tracking-tight text-slate-800 uppercase">Analytics</h1>
        <p className="text-slate-500 font-medium">Historical compost intelligence.</p>
      </header>

      <div className="grid gap-4">
        {/* Placeholder for Historical Chart */}
        <div className="vk-card flex flex-col items-center justify-center py-12 bg-white">
          <LineChart className="w-12 h-12 text-slate-300 mb-4" />
          <h3 className="text-lg font-bold text-slate-600">Temperature History</h3>
          <p className="text-sm text-slate-400">Not enough data collected yet.</p>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="vk-card bg-white">
            <div className="flex items-center gap-2 mb-2">
              <TrendingUp className="w-4 h-4 text-green-600" />
              <h4 className="font-bold text-sm text-slate-500 uppercase">Avg Temp</h4>
            </div>
            <p className="text-2xl font-black">-- °C</p>
          </div>
          <div className="vk-card bg-white">
            <div className="flex items-center gap-2 mb-2">
              <Clock className="w-4 h-4 text-blue-600" />
              <h4 className="font-bold text-sm text-slate-500 uppercase">Uptime</h4>
            </div>
            <p className="text-2xl font-black">100%</p>
          </div>
        </div>
      </div>
    </main>
  );
}
