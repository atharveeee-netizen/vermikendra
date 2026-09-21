'use client';

import { Settings, User, MapPin, Database, LogOut } from 'lucide-react';

export default function SettingsPage() {
  return (
    <main className="min-h-screen bg-[#F9F8F4] p-4 md:p-8 pb-24">
      <header className="mb-6">
        <h1 className="text-3xl font-black tracking-tight text-slate-800 uppercase">Settings</h1>
      </header>

      <div className="space-y-6">
        {/* Profile Section */}
        <section className="bg-white rounded-xl border border-slate-200 overflow-hidden">
          <div className="p-4 border-b border-slate-100 flex items-center gap-4">
            <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
              <User className="w-6 h-6 text-green-700" />
            </div>
            <div>
              <h3 className="font-bold text-lg">Farmer Account</h3>
              <p className="text-sm text-slate-500">vermikendra-demo</p>
            </div>
          </div>
          
          <button className="w-full p-4 flex items-center gap-3 hover:bg-slate-50 transition-colors text-left border-b border-slate-100">
            <MapPin className="w-5 h-5 text-slate-400" />
            <span className="font-medium">Manage Sites & Beds</span>
          </button>
          
          <button className="w-full p-4 flex items-center gap-3 hover:bg-slate-50 transition-colors text-left border-b border-slate-100">
            <Database className="w-5 h-5 text-slate-400" />
            <span className="font-medium">Export Telemetry Data</span>
          </button>
          
          <button className="w-full p-4 flex items-center gap-3 hover:bg-slate-50 transition-colors text-left text-red-600">
            <LogOut className="w-5 h-5" />
            <span className="font-medium">Sign Out</span>
          </button>
        </section>

        {/* System Info */}
        <section className="text-center">
          <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">Vermikendra OS v1.0.0</p>
          <p className="text-xs text-slate-400 mt-1">Connected to Production Gateway</p>
        </section>
      </div>
    </main>
  );
}
