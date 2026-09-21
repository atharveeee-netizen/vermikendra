'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Home, Map, Bell, Settings } from 'lucide-react';
import { useEffect, useState } from 'react';
import { fetchSites, fetchSiteFleet } from '../services/api';

export default function BottomNav() {
  const pathname = usePathname();
  const [alertCount, setAlertCount] = useState(0);

  useEffect(() => {
    async function checkAlerts() {
      try {
        const sites = await fetchSites();
        if (sites.length > 0) {
          const fleet = await fetchSiteFleet(sites[0].id);
          setAlertCount(fleet.stats.critical);
        }
      } catch (err) {
        // ignore for nav
      }
    }
    checkAlerts();
    const interval = setInterval(checkAlerts, 15000);
    return () => clearInterval(interval);
  }, []);

  const navItems = [
    { name: 'Home', href: '/', icon: Home, badge: 0 },
    { name: 'Map', href: '/map', icon: Map, badge: 0 },
    { name: 'Alerts', href: '/alerts', icon: Bell, badge: alertCount },
    { name: 'Settings', href: '/settings', icon: Settings, badge: 0 },
  ];

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-slate-200 px-4 py-2 flex justify-around items-center z-50 pb-safe">
      {navItems.map((item) => {
        const isActive = pathname === item.href;
        const Icon = item.icon;
        return (
          <Link
            key={item.name}
            href={item.href}
            className={`flex flex-col items-center p-2 rounded-xl transition-colors relative ${
              isActive ? 'text-[#2d7a42]' : 'text-slate-400 hover:text-slate-600'
            }`}
          >
            <div className="relative">
              <Icon className="w-6 h-6 mb-1" strokeWidth={isActive ? 2.5 : 2} />
              {item.badge > 0 && (
                <span className="absolute -top-1 -right-1 bg-red-500 text-white text-[9px] font-black w-4 h-4 rounded-full flex items-center justify-center border-2 border-white">
                  {item.badge}
                </span>
              )}
            </div>
            <span className={`text-[10px] font-medium tracking-wide ${isActive ? 'font-bold' : ''}`}>
              {item.name}
            </span>
          </Link>
        );
      })}
    </nav>
  );
}
