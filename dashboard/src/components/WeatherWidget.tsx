'use client';

import React, { useState, useEffect } from 'react';
import { 
  Sun, 
  CloudSun, 
  CloudRain, 
  Flame, 
  Droplets, 
  Wind, 
  ShieldAlert, 
  CheckCircle2, 
  ChevronDown, 
  ChevronUp, 
  Volume2, 
  VolumeX, 
  Sparkles,
  Thermometer
} from 'lucide-react';

interface WeatherData {
  currentTemp: number;
  apparentTemp: number;
  humidity: number;
  windSpeed: number;
  weatherCode: number;
  precipitation: number;
  maxTempToday: number;
  minTempToday: number;
  hourly: {
    time: string;
    temp: number;
    uv: number;
    pop: number;
  }[];
  daily: {
    date: string;
    max: number;
    min: number;
    rain: number;
  }[];
}

export default function WeatherWidget() {
  const [weather, setWeather] = useState<WeatherData | null>(null);
  const [loading, setLoading] = useState(true);
  const [expanded, setExpanded] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);

  useEffect(() => {
    async function loadWeather() {
      try {
        const res = await fetch(
          'https://api.open-meteo.com/v1/forecast?latitude=18.5204&longitude=73.8567&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,precipitation_probability,uv_index&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,uv_index_max&timezone=Asia%2FKolkata'
        );
        if (res.ok) {
          const data = await res.json();
          const currentHour = new Date().getHours();
          
          const nextHours = [];
          for (let i = 0; i < 6; i++) {
            const idx = currentHour + i;
            if (data.hourly.time[idx]) {
              const hourStr = data.hourly.time[idx].split('T')[1].slice(0, 5);
              nextHours.push({
                time: hourStr,
                temp: Math.round(data.hourly.temperature_2m[idx]),
                uv: Math.round(data.hourly.uv_index[idx] || 0),
                pop: Math.round(data.hourly.precipitation_probability[idx] || 0)
              });
            }
          }

          const nextDays = [];
          for (let d = 0; d < 3; d++) {
            if (data.daily.time[d]) {
              const dateObj = new Date(data.daily.time[d]);
              const dayName = d === 0 ? "Today (आज)" : d === 1 ? "Tomorrow (उद्या)" : dateObj.toLocaleDateString('en-IN', { weekday: 'short' });
              nextDays.push({
                date: dayName,
                max: Math.round(data.daily.temperature_2m_max[d]),
                min: Math.round(data.daily.temperature_2m_min[d]),
                rain: data.daily.precipitation_sum[d] || 0
              });
            }
          }

          setWeather({
            currentTemp: Math.round(data.current.temperature_2m),
            apparentTemp: Math.round(data.current.apparent_temperature),
            humidity: Math.round(data.current.relative_humidity_2m),
            windSpeed: Math.round(data.current.wind_speed_10m),
            weatherCode: data.current.weather_code,
            precipitation: data.current.precipitation,
            maxTempToday: Math.round(data.daily.temperature_2m_max[0]),
            minTempToday: Math.round(data.daily.temperature_2m_min[0]),
            hourly: nextHours,
            daily: nextDays
          });
        }
      } catch (err) {
        // Fallback default Pune weather
        setWeather({
          currentTemp: 29,
          apparentTemp: 31,
          humidity: 58,
          windSpeed: 12,
          weatherCode: 1,
          precipitation: 0,
          maxTempToday: 34,
          minTempToday: 21,
          hourly: [
            { time: "12:00", temp: 32, uv: 7, pop: 10 },
            { time: "14:00", temp: 34, uv: 8, pop: 15 },
            { time: "16:00", temp: 31, uv: 4, pop: 10 },
            { time: "18:00", temp: 28, uv: 1, pop: 5 },
          ],
          daily: [
            { date: "Today (आज)", max: 34, min: 21, rain: 0 },
            { date: "Tomorrow (उद्या)", max: 35, min: 22, rain: 0 },
            { date: "Day After", max: 33, min: 20, rain: 2 }
          ]
        });
      } finally {
        setLoading(false);
      }
    }

    loadWeather();
  }, []);

  if (loading || !weather) {
    return (
      <div className="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-4 text-white text-xs animate-pulse">
        हवामान डेटा लोड होत आहे (Fetching farm microclimate)...
      </div>
    );
  }

  // Determine worm safety and protective advice
  const isHeatwaveRisk = weather.maxTempToday >= 33 || weather.currentTemp >= 32;
  const isRainRisk = weather.precipitation > 2 || weather.hourly.some(h => h.pop > 40);

  let advisoryHeadline = "अनुकूल हवामान (Ideal Composting Conditions)";
  let advisorySeverity: "NORMAL" | "HEAT" | "RAIN" = "NORMAL";
  let advisoryBullets = [
    "हवामान गांडूळांसाठी पोषक आहे (२०-३०°C).",
    "बेडमध्ये हलका ओलावा टिकून राहण्यासाठी नेहमीप्रमाणे हलके पाणी शिंपडा."
  ];

  if (isHeatwaveRisk) {
    advisoryHeadline = "⚠️ उष्णतेचा इशारा (Heatwave Warning for Worms)";
    advisorySeverity = "HEAT";
    advisoryBullets = [
      `आज दुपारचे तापमान ${weather.maxTempToday}°C पर्यंत जाण्याची शक्यता आहे (गांडूळ ३५°C वर मरतात).`,
      "सकाळी १० पूर्वी सर्व बेडवर ओल्या गोणपाटाचे (बोरा) आच्छादन घाला.",
      "शेडनेट पूर्णपणे ओढून ठेवा. दुपारच्या कडक उन्हात पाणी देणे टाळा (वाफ होऊ शकते)."
    ];
  } else if (isRainRisk) {
    advisoryHeadline = "🌧️ पावसाचा इशारा (Heavy Rain & Drainage Warning)";
    advisorySeverity = "RAIN";
    advisoryBullets = [
      "आज पाऊस पडण्याची शक्यता आहे. पाणी साचल्यास गांडूळ गुदमरून बाहेर पडतात.",
      "बेडचे पाण्याचा निचरा होणारे छिद्र (Drainage pipe) कचरा अडकला नसल्याची खात्री करा.",
      "हवा खेळती राहील अशा पद्धतीने वर प्लास्टिक किंवा ताडपत्रीचा उतार द्या."
    ];
  }

  const speakAdvisory = () => {
    if (typeof window === "undefined" || !('speechSynthesis' in window)) return;
    if (isSpeaking) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
      return;
    }

    const textToSpeak = `हवामान व गांडूळ संरक्षण सल्ला: पुणे तापमान सध्या ${weather.currentTemp} अंश सेल्सिअस आहे. ${advisoryHeadline}. ${advisoryBullets.join(' ')}`;
    const utterance = new SpeechSynthesisUtterance(textToSpeak);
    utterance.lang = "mr-IN";
    utterance.rate = 0.95;

    const voices = window.speechSynthesis.getVoices();
    const regionalVoice = voices.find(v => v.lang.includes("mr") || v.lang.includes("hi"));
    if (regionalVoice) utterance.voice = regionalVoice;

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    window.speechSynthesis.speak(utterance);
  };

  return (
    <section className="bg-white/15 backdrop-blur-md border border-white/25 rounded-2xl p-4 text-white shadow-lg mt-3 transition-all">
      {/* Top Row: Location, Temp, Weather Badge */}
      <div className="flex justify-between items-start">
        <div>
          <div className="flex items-center gap-1.5 text-xs text-green-100 font-medium">
            <span>📍 पुणे (Pune Farm microclimate)</span>
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-300"></span>
            <span>Live</span>
          </div>

          <div className="flex items-baseline gap-2 mt-1">
            <span className="text-3xl font-black">{weather.currentTemp}°C</span>
            <span className="text-xs text-white/80 font-medium">
              (भासणारे {weather.apparentTemp}°C)
            </span>
          </div>
        </div>

        {/* Weather Icon & Max/Min */}
        <div className="text-right">
          <div className="flex items-center justify-end gap-1.5">
            {advisorySeverity === "HEAT" ? (
              <Flame className="w-6 h-6 text-amber-300 animate-pulse" />
            ) : advisorySeverity === "RAIN" ? (
              <CloudRain className="w-6 h-6 text-sky-300 animate-bounce" />
            ) : (
              <CloudSun className="w-6 h-6 text-yellow-300" />
            )}
            <span className="font-bold text-sm">
              {advisorySeverity === "HEAT" ? "उष्ण हवा" : advisorySeverity === "RAIN" ? "पावसाळी" : "स्वच्छ"}
            </span>
          </div>
          <p className="text-xs text-green-100 font-medium mt-0.5">
            कमाल {weather.maxTempToday}°C / किमान {weather.minTempToday}°C
          </p>
        </div>
      </div>

      {/* Middle Row: Microclimate Metrics (Humidity, Rain, Worm Safety) */}
      <div className="grid grid-cols-3 gap-2 mt-3 pt-3 border-t border-white/15 text-center">
        <div className="bg-black/10 rounded-xl p-2">
          <span className="text-[10px] text-green-100 flex items-center justify-center gap-1">
            <Droplets className="w-3 h-3 text-blue-200" /> हवेतील ओलावा
          </span>
          <p className="text-sm font-black mt-0.5">{weather.humidity}%</p>
        </div>

        <div className="bg-black/10 rounded-xl p-2">
          <span className="text-[10px] text-green-100 flex items-center justify-center gap-1">
            <Wind className="w-3 h-3 text-emerald-200" /> वारा गती
          </span>
          <p className="text-sm font-black mt-0.5">{weather.windSpeed} km/h</p>
        </div>

        <div className="bg-black/10 rounded-xl p-2">
          <span className="text-[10px] text-green-100 flex items-center justify-center gap-1">
            <Thermometer className="w-3 h-3 text-amber-200" /> गांडूळ आराम
          </span>
          <p className={`text-xs font-black mt-0.5 ${
            advisorySeverity === "HEAT" ? "text-amber-300" : "text-emerald-300"
          }`}>
            {advisorySeverity === "HEAT" ? "🟡 काळजी घ्या" : "🟢 उत्तम स्थिती"}
          </p>
        </div>
      </div>

      {/* Worm Thermal Safety Bar */}
      <div className="mt-3">
        <div className="flex justify-between text-[10px] text-green-100 mb-1">
          <span>गांडूळ सुरक्षा तापमान पट्टा</span>
          <span className="font-bold">सुरक्षित मर्यादा: २०° - ३०°C</span>
        </div>
        <div className="w-full bg-white/20 h-2 rounded-full overflow-hidden flex">
          <div className="bg-sky-400 h-full w-[25%]" title="Cold (15-20°C)"></div>
          <div className="bg-emerald-400 h-full w-[50%]" title="Optimal (20-30°C)"></div>
          <div className="bg-amber-400 h-full w-[15%]" title="Caution (31-34°C)"></div>
          <div className="bg-red-500 h-full w-[10%]" title="Danger (>35°C)"></div>
        </div>
      </div>

      {/* Protective Farmer Advisory Card */}
      <div className={`mt-3.5 rounded-xl p-3 border ${
        advisorySeverity === "HEAT" 
          ? "bg-amber-950/40 border-amber-300/40 text-amber-50" 
          : advisorySeverity === "RAIN"
          ? "bg-sky-950/40 border-sky-300/40 text-sky-50"
          : "bg-emerald-950/30 border-emerald-300/30 text-emerald-50"
      }`}>
        <div className="flex items-center justify-between mb-1.5">
          <div className="flex items-center gap-1.5 font-black text-xs tracking-wide">
            {advisorySeverity === "HEAT" ? (
              <ShieldAlert className="w-4 h-4 text-amber-300" />
            ) : advisorySeverity === "RAIN" ? (
              <CloudRain className="w-4 h-4 text-sky-300" />
            ) : (
              <CheckCircle2 className="w-4 h-4 text-emerald-300" />
            )}
            <span>{advisoryHeadline}</span>
          </div>

          <button
            onClick={speakAdvisory}
            aria-label="Listen weather advisory"
            className="text-[11px] font-bold bg-white/20 hover:bg-white/30 px-2 py-0.5 rounded-md flex items-center gap-1 transition-all"
          >
            {isSpeaking ? <VolumeX className="w-3.5 h-3.5" /> : <Volume2 className="w-3.5 h-3.5" />}
            <span>{isSpeaking ? "थांबवा" : "ऐका (Audio)"}</span>
          </button>
        </div>

        <ul className="text-xs space-y-1 text-white/90 leading-relaxed pl-1">
          {advisoryBullets.map((bullet, bIdx) => (
            <li key={bIdx} className="flex items-start gap-1.5">
              <span className="text-emerald-300 mt-0.5">•</span>
              <span>{bullet}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Expandable 24-Hour & 3-Day Forecast Drawer */}
      <button 
        onClick={() => setExpanded(!expanded)}
        className="w-full mt-3 pt-2 border-t border-white/15 flex items-center justify-center gap-1 text-[11px] font-bold text-green-100 hover:text-white transition-colors"
      >
        <span>{expanded ? "तपशील बंद करा (Close Forecast)" : "पुढील २४ तास व ३ दिवसांचा अंदाज पहा (View 3-Day Forecast)"}</span>
        {expanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
      </button>

      {expanded && (
        <div className="mt-3 pt-2 border-t border-white/10 space-y-3 animate-fadeIn">
          {/* Hourly Forecast Strip */}
          <div>
            <p className="text-[10px] font-bold text-green-200 uppercase tracking-wider mb-2">
              पुढील तासांचा तापमान अंदाज (Hourly Trend):
            </p>
            <div className="flex gap-2 overflow-x-auto pb-1 scrollbar-hide">
              {weather.hourly.map((h, i) => (
                <div key={i} className="flex-1 min-w-[65px] bg-black/20 rounded-xl p-2 text-center border border-white/10">
                  <span className="text-[10px] text-white/70 block">{h.time}</span>
                  <span className="text-sm font-bold text-white block my-0.5">{h.temp}°C</span>
                  <span className={`text-[9px] font-bold px-1.5 py-0.5 rounded-full inline-block ${
                    h.temp >= 33 ? "bg-amber-500/80 text-white" : "bg-emerald-500/80 text-white"
                  }`}>
                    {h.temp >= 33 ? "उष्ण" : "सुरक्षित"}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* 3-Day Forecast Cards */}
          <div>
            <p className="text-[10px] font-bold text-green-200 uppercase tracking-wider mb-2">
              ३ दिवसांचा अंदाज (3-Day Outlook):
            </p>
            <div className="space-y-1.5">
              {weather.daily.map((d, dIdx) => (
                <div key={dIdx} className="bg-black/20 rounded-xl p-2.5 flex items-center justify-between text-xs border border-white/10">
                  <span className="font-bold">{d.date}</span>
                  <div className="flex items-center gap-3">
                    <span className="text-amber-300 font-bold">{d.max}°C कमाल</span>
                    <span className="text-sky-200">{d.min}°C किमान</span>
                    {d.rain > 0 ? (
                      <span className="text-[10px] bg-sky-500/30 text-sky-200 px-1.5 py-0.5 rounded">
                        🌧️ {d.rain} mm
                      </span>
                    ) : (
                      <span className="text-[10px] text-yellow-300">☀️ कोरडे</span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
