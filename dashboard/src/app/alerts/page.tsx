'use client';

import { Bell, CheckCircle2 } from 'lucide-react';

export default function AlertsPage() {
  return (
    <main className="min-h-screen bg-[#F9F8F4] p-4 md:p-8 pb-24">
      <header className="mb-6">
        <h1 className="text-3xl font-black tracking-tight text-slate-800 uppercase">Alerts</h1>
        <p className="text-slate-500 font-medium">System notifications and warnings.</p>
      </header>

      <div className="space-y-4">
        {/* Placeholder for Empty Alerts */}
        <div className="vk-card flex flex-col items-center justify-center py-16 bg-white text-center">
          <CheckCircle2 className="w-16 h-16 text-green-500 mb-4" />
          <h3 className="text-xl font-bold text-slate-800">All Clear!</h3>
          <p className="text-slate-500 mt-2 max-w-xs mx-auto">
            Your compost beds are operating within optimal parameters. No active alerts.
          </p>
        </div>
      </div>
    </main>
  );
}
