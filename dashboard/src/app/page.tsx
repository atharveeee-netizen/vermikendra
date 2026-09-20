export default function Home() {
  // Mock data for Phase 11 UI Scaffold
  const mockProbes = [26.1, 28.5, 31.2, 33.4, 29.8]; // Note: 33.4 is CRITICAL
  const readinessSlope = 1.2; // ppm/min
  const isReady = readinessSlope < 2.4; 

  return (
    <main className="p-4 flex flex-col gap-6 max-w-md mx-auto">
      
      {/* Header */}
      <header className="flex justify-between items-center border-b border-slate-700 pb-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Vermikendra</h1>
          <p className="text-sm text-slate-400">Bin-01 | Offline Mode</p>
        </div>
        <div className="w-4 h-4 rounded-full bg-green-500 animate-pulse"></div>
      </header>

      {/* Readiness Status (Derived from Respiration) */}
      <section className={`p-6 rounded-xl flex flex-col items-center justify-center text-center ${isReady ? 'vk-good' : 'bg-slate-800'}`}>
        <h2 className="text-lg font-semibold mb-2">Compost Readiness</h2>
        <div className="text-5xl font-black mb-2">{isReady ? 'READY' : 'ACTIVE'}</div>
        <div className="text-sm opacity-80">CO2 Slope: {readinessSlope} ppm/min</div>
      </section>

      {/* Critical Alerts */}
      <section className="vk-critical p-4 rounded-xl flex flex-col gap-2">
        <div className="flex justify-between items-center font-bold">
          <span className="flex items-center gap-2">
            ⚠️ HEAT CRITICAL
          </span>
          <span>Now</span>
        </div>
        <p className="text-sm">Probe 4 has exceeded 33.0°C. Misting pump has been automatically actuated.</p>
      </section>

      {/* Thermal Gradient Map */}
      <section className="bg-slate-800 p-4 rounded-xl">
        <h3 className="font-semibold text-slate-300 mb-4 border-b border-slate-700 pb-2">Thermal Gradient (Depth)</h3>
        <div className="flex flex-col gap-2">
          {mockProbes.map((temp, index) => {
            let colorClass = 'vk-good';
            if (temp >= 33.0) colorClass = 'vk-critical';
            else if (temp >= 30.0) colorClass = 'vk-warning';

            return (
              <div key={index} className="flex items-center justify-between">
                <span className="text-sm text-slate-400 w-20">Probe {index + 1}</span>
                <div className={`flex-1 h-8 rounded-md flex items-center px-3 font-mono font-bold ${colorClass}`}>
                  {temp.toFixed(1)} °C
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* Moisture & Gas */}
      <section className="grid grid-cols-2 gap-4">
        <div className="bg-slate-800 p-4 rounded-xl flex flex-col items-center">
          <span className="text-sm text-slate-400">Moisture</span>
          <span className="text-2xl font-bold text-[#38a169]">71.5%</span>
        </div>
        <div className="bg-slate-800 p-4 rounded-xl flex flex-col items-center">
          <span className="text-sm text-slate-400">Foul Gas</span>
          <span className="text-2xl font-bold text-slate-200">OK</span>
        </div>
      </section>

    </main>
  );
}
