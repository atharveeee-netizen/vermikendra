'use client';

import React, { useState } from 'react';
import { 
  Settings, 
  Globe, 
  Sliders, 
  Bell, 
  Download, 
  CheckCircle2, 
  Wifi, 
  Smartphone, 
  FileSpreadsheet,
  Save,
  ShieldCheck
} from 'lucide-react';

export default function SettingsPage() {
  const [lang, setLang] = useState<'en' | 'hi' | 'mr'>('en');
  const [maxTemp, setMaxTemp] = useState<number>(35);
  const [minMoisture, setMinMoisture] = useState<number>(50);
  const [maxMoisture, setMaxMoisture] = useState<number>(75);
  const [waAlerts, setWaAlerts] = useState<boolean>(true);
  const [smsAlerts, setSmsAlerts] = useState<boolean>(false);
  const [soundAlerts, setSoundAlerts] = useState<boolean>(true);
  const [saved, setSaved] = useState<boolean>(false);

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 2500);
  };

  const handleExportCSV = () => {
    const csvHeader = "Timestamp,Bed_ID,Core_Temp_C,Ambient_Temp_C,Moisture_Pct,CO2_ppm,Battery_V,Status\n";
    const sampleRows = [
      "2026-09-21T14:00:00Z,BED-01,31.4,28.2,62,850,3.95,NORMAL",
      "2026-09-21T13:00:00Z,BED-01,31.8,29.0,61,840,3.96,NORMAL",
      "2026-09-21T12:00:00Z,BED-01,32.2,30.1,60,860,3.96,NORMAL",
      "2026-09-21T14:00:00Z,BED-02,36.8,28.5,44,1150,3.88,WATCH",
      "2026-09-21T14:00:00Z,BED-03,29.8,28.0,68,790,3.92,NORMAL",
      "2026-09-21T14:00:00Z,BED-04,30.5,28.1,65,810,4.01,NORMAL"
    ].join("\n");

    const blob = new Blob([csvHeader + sampleRows], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", `vermikendra-telemetry-${new Date().toISOString().slice(0,10)}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <main className="min-h-screen bg-[#F9F8F4] p-4 md:p-8 pb-28 max-w-lg mx-auto">
      {/* Header */}
      <header className="mb-6 flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Settings className="w-5 h-5 text-[#2d7a42]" />
            <span className="text-xs font-bold text-[#2d7a42] uppercase tracking-widest">Preferences</span>
          </div>
          <h1 className="text-2xl font-black text-slate-800 tracking-tight uppercase">Farm Settings</h1>
        </div>
        <button 
          onClick={handleSave}
          className="flex items-center gap-1.5 bg-[#2d7a42] text-white px-3.5 py-2 rounded-xl text-xs font-bold active:scale-95 transition-all shadow-md shadow-green-900/20"
        >
          {saved ? <CheckCircle2 className="w-4 h-4 text-green-200" /> : <Save className="w-4 h-4" />}
          {saved ? 'Saved!' : 'Save'}
        </button>
      </header>

      <div className="space-y-4">
        {/* Language Selection (A17) */}
        <section className="bg-white rounded-2xl border border-slate-200 p-4 shadow-sm">
          <div className="flex items-center gap-2 mb-3">
            <Globe className="w-4 h-4 text-[#2d7a42]" />
            <h2 className="text-xs font-bold text-slate-500 uppercase tracking-wider">App Language / भाषा / भाषा निवडा</h2>
          </div>
          <div className="grid grid-cols-3 gap-2">
            <button
              onClick={() => setLang('en')}
              className={`py-2 px-3 rounded-xl font-bold text-xs border transition-all ${
                lang === 'en' 
                  ? 'bg-[#2d7a42] text-white border-[#2d7a42] shadow-sm' 
                  : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100'
              }`}
            >
              English
            </button>
            <button
              onClick={() => setLang('hi')}
              className={`py-2 px-3 rounded-xl font-bold text-xs border transition-all ${
                lang === 'hi' 
                  ? 'bg-[#2d7a42] text-white border-[#2d7a42] shadow-sm' 
                  : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100'
              }`}
            >
              हिन्दी (Hindi)
            </button>
            <button
              onClick={() => setLang('mr')}
              className={`py-2 px-3 rounded-xl font-bold text-xs border transition-all ${
                lang === 'mr' 
                  ? 'bg-[#2d7a42] text-white border-[#2d7a42] shadow-sm' 
                  : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100'
              }`}
            >
              मराठी (Marathi)
            </button>
          </div>
        </section>

        {/* Threshold Configuration (A16) */}
        <section className="bg-white rounded-2xl border border-slate-200 p-4 shadow-sm">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <Sliders className="w-4 h-4 text-orange-600" />
              <h2 className="text-xs font-bold text-slate-500 uppercase tracking-wider">Bed Health Thresholds</h2>
            </div>
            <span className="text-[10px] text-slate-400 font-medium">Auto-triggers alerts</span>
          </div>

          <div className="space-y-4">
            {/* Max Core Temp */}
            <div>
              <div className="flex justify-between text-xs font-bold text-slate-700 mb-1">
                <span>Critical Temperature Ceiling</span>
                <span className="text-orange-600 font-black">{maxTemp}°C</span>
              </div>
              <input 
                type="range" 
                min="30" 
                max="45" 
                value={maxTemp} 
                onChange={(e) => setMaxTemp(Number(e.target.value))}
                className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-[#2d7a42]"
              />
              <div className="flex justify-between text-[10px] text-slate-400 mt-1">
                <span>30°C (Sensitive)</span>
                <span>Worms stress above 35°C</span>
                <span>45°C</span>
              </div>
            </div>

            {/* Min Moisture */}
            <div>
              <div className="flex justify-between text-xs font-bold text-slate-700 mb-1">
                <span>Minimum Moisture Floor</span>
                <span className="text-blue-600 font-black">{minMoisture}%</span>
              </div>
              <input 
                type="range" 
                min="30" 
                max="60" 
                value={minMoisture} 
                onChange={(e) => setMinMoisture(Number(e.target.value))}
                className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-[#2d7a42]"
              />
              <div className="flex justify-between text-[10px] text-slate-400 mt-1">
                <span>30%</span>
                <span>Optimal: 55-65%</span>
                <span>60%</span>
              </div>
            </div>

            {/* Max Moisture */}
            <div>
              <div className="flex justify-between text-xs font-bold text-slate-700 mb-1">
                <span>Anaerobic Moisture Ceiling</span>
                <span className="text-blue-600 font-black">{maxMoisture}%</span>
              </div>
              <input 
                type="range" 
                min="65" 
                max="90" 
                value={maxMoisture} 
                onChange={(e) => setMaxMoisture(Number(e.target.value))}
                className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-[#2d7a42]"
              />
              <div className="flex justify-between text-[10px] text-slate-400 mt-1">
                <span>65%</span>
                <span>Above 75% risk of souring</span>
                <span>90%</span>
              </div>
            </div>
          </div>
        </section>

        {/* Alert Delivery Channels */}
        <section className="bg-white rounded-2xl border border-slate-200 p-4 shadow-sm">
          <div className="flex items-center gap-2 mb-3">
            <Bell className="w-4 h-4 text-[#2d7a42]" />
            <h2 className="text-xs font-bold text-slate-500 uppercase tracking-wider">Notification Channels</h2>
          </div>

          <div className="divide-y divide-slate-100">
            <label className="flex items-center justify-between py-2.5 cursor-pointer">
              <div className="flex items-center gap-2.5">
                <Smartphone className="w-4 h-4 text-green-600" />
                <div>
                  <p className="text-xs font-bold text-slate-800">WhatsApp Alert Digest</p>
                  <p className="text-[10px] text-slate-400">Critical notifications sent to farmer phone</p>
                </div>
              </div>
              <input 
                type="checkbox" 
                checked={waAlerts} 
                onChange={(e) => setWaAlerts(e.target.checked)}
                className="w-4 h-4 accent-[#2d7a42] rounded"
              />
            </label>

            <label className="flex items-center justify-between py-2.5 cursor-pointer">
              <div className="flex items-center gap-2.5">
                <Smartphone className="w-4 h-4 text-blue-600" />
                <div>
                  <p className="text-xs font-bold text-slate-800">SMS Alerts</p>
                  <p className="text-[10px] text-slate-400">Works in low-bandwidth rural zones</p>
                </div>
              </div>
              <input 
                type="checkbox" 
                checked={smsAlerts} 
                onChange={(e) => setSmsAlerts(e.target.checked)}
                className="w-4 h-4 accent-[#2d7a42] rounded"
              />
            </label>

            <label className="flex items-center justify-between py-2.5 cursor-pointer">
              <div className="flex items-center gap-2.5">
                <Bell className="w-4 h-4 text-orange-500" />
                <div>
                  <p className="text-xs font-bold text-slate-800">In-App Acoustic Sound</p>
                  <p className="text-[10px] text-slate-400">Chime on critical threshold breaches</p>
                </div>
              </div>
              <input 
                type="checkbox" 
                checked={soundAlerts} 
                onChange={(e) => setSoundAlerts(e.target.checked)}
                className="w-4 h-4 accent-[#2d7a42] rounded"
              />
            </label>
          </div>
        </section>

        {/* Data Export (A18) */}
        <section className="bg-white rounded-2xl border border-slate-200 p-4 shadow-sm">
          <div className="flex items-center gap-2 mb-2">
            <FileSpreadsheet className="w-4 h-4 text-emerald-600" />
            <h2 className="text-xs font-bold text-slate-500 uppercase tracking-wider">Export Farm Data (CSV)</h2>
          </div>
          <p className="text-xs text-slate-500 mb-3">
            Download full time-series logs for all beds, including vertical probe arrays, battery health, and telemetry history.
          </p>
          <button
            onClick={handleExportCSV}
            className="w-full bg-slate-800 text-white font-bold text-xs py-2.5 px-4 rounded-xl flex items-center justify-center gap-2 active:scale-95 transition-all shadow-sm hover:bg-slate-900"
          >
            <Download className="w-4 h-4" /> Download Telemetry CSV
          </button>
        </section>

        {/* Gateway & Network Info */}
        <section className="bg-white rounded-2xl border border-slate-200 p-4 shadow-sm">
          <div className="flex items-center gap-2 mb-3">
            <Wifi className="w-4 h-4 text-[#2d7a42]" />
            <h2 className="text-xs font-bold text-slate-500 uppercase tracking-wider">Hardware & Gateway Status</h2>
          </div>

          <div className="bg-slate-50 rounded-xl p-3 border border-slate-100 space-y-1.5 text-xs">
            <div className="flex justify-between">
              <span className="text-slate-500">Gateway Status:</span>
              <span className="font-bold text-green-700 flex items-center gap-1">
                <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span> Online (ESP32-S3)
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Mesh Channel:</span>
              <span className="font-mono text-slate-700">CH-11 (2.4GHz ESP-NOW)</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Active Probes:</span>
              <span className="font-bold text-slate-700">6 Nodes (30 Probes)</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Telemetry Sync Interval:</span>
              <span className="font-mono text-slate-700">10s (Fast Mesh)</span>
            </div>
          </div>
        </section>

        {/* System Credits */}
        <footer className="text-center pt-2 pb-4">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 bg-green-100/60 rounded-full text-[11px] font-bold text-[#2d7a42]">
            <ShieldCheck className="w-3.5 h-3.5" />
            Vermikendra Precision Agronomy Platform v2.4
          </div>
          <p className="text-[10px] text-slate-400 mt-2">
            Public Cloud Edition · Connected to Agro-Fleet Gateway
          </p>
        </footer>
      </div>
    </main>
  );
}
