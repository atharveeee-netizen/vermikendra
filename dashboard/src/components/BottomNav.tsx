'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Home, Map, Bell, Settings } from 'lucide-react';

export default function BottomNav() {
  const pathname = usePathname();

  const navItems = [
    { name: 'Home', href: '/', icon: Home },
    { name: 'Map', href: '/map', icon: Map },
    { name: 'Alerts', href: '/alerts', icon: Bell },
    { name: 'Settings', href: '/settings', icon: Settings },
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
            className={`flex flex-col items-center p-2 rounded-xl transition-colors ${
              isActive ? 'text-[#2d7a42]' : 'text-slate-400 hover:text-slate-600'
            }`}
          >
            <Icon className="w-6 h-6 mb-1" strokeWidth={isActive ? 2.5 : 2} />
            <span className={`text-[10px] font-medium tracking-wide ${isActive ? 'font-bold' : ''}`}>
              {item.name}
            </span>
          </Link>
        );
      })}
    </nav>
  );
}
