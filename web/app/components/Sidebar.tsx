'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Sidebar() {
  const pathname = usePathname();
  
  const navItems = [
    { href: '/', icon: '🏠', label: 'Home' },
    { href: '/dashboard', icon: '📊', label: 'Dashboard' },
    { href: '/collections', icon: '📚', label: 'Collections' },
    { href: '/workspace', icon: '💬', label: 'Workspace' },
    { href: '/workflows', icon: '🔄', label: 'Workflows' },
    { href: '/stocks', icon: '📈', label: 'Stocks' },
  ];

  return (
    <aside className="w-64 bg-white border-r border-gray-200 flex flex-col">
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center">
            <span className="text-white font-bold text-lg">A</span>
          </div>
          <div>
            <div className="font-bold text-gray-900 text-lg">AstraFlow</div>
            <div className="text-xs text-gray-500">Mission Control</div>
          </div>
        </div>
      </div>

      <nav className="flex-1 p-4 space-y-1">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
              pathname === item.href
                ? 'bg-purple-50 text-purple-600 font-medium'
                : 'text-gray-600 hover:bg-gray-50'
            }`}
          >
            <span className="text-xl">{item.icon}</span>
            <span>{item.label}</span>
          </Link>
        ))}
      </nav>

      <div className="p-4 border-t border-gray-200">
        <Link
          href="/settings"
          className="flex items-center space-x-3 px-4 py-3 rounded-lg text-gray-600 hover:bg-gray-50"
        >
          <span className="text-xl">⚙️</span>
          <span>Settings</span>
        </Link>
      </div>
    </aside>
  );
}
