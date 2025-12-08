'use client';

import { useEffect, useState } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import DesignPrompt from './components/DesignPrompt';

export default function Dashboard() {
  const [stats, setStats] = useState({
    totalDocuments: 0,
    celeryWorkers: 'Active',
    monthlyCost: 0,
    kafkaStatus: 'Stable'
  });
  const [collections, setCollections] = useState([]);
  const [stockTicker, setStockTicker] = useState<any[]>([]);

  useEffect(() => {
    // Fetch system stats
    fetch('http://localhost:8000/health')
      .then(res => res.json())
      .then(data => {
        setStats({
          totalDocuments: data.total_documents || 0,
          celeryWorkers: data.celery_status || 'Active',
          monthlyCost: data.estimated_cost || 0,
          kafkaStatus: data.kafka_status || 'Stable'
        });
      })
      .catch(err => console.error(err));

    // Fetch collections
    fetch('http://localhost:8000/collections')
      .then(res => res.json())
      .then(data => setCollections(data))
      .catch(err => console.error(err));

    // Simulate stock ticker
    const mockStocks = [
      { symbol: 'AAPL', price: 178.23, change: 2.34 },
      { symbol: 'GOOGL', price: 142.56, change: -1.23 },
      { symbol: 'MSFT', price: 378.91, change: 5.67 },
      { symbol: 'TSLA', price: 242.84, change: -3.45 },
      { symbol: 'AMZN', price: 151.94, change: 1.89 }
    ];
    setStockTicker(mockStocks);
  }, []);

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        
        <main className="flex-1 overflow-y-auto">
          <div className="p-8">
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-2xl">📄</span>
                  <span className="text-xs font-medium text-green-600 bg-green-50 px-2 py-1 rounded">+12%</span>
                </div>
                <div className="text-2xl font-bold text-gray-900">{stats.totalDocuments.toLocaleString()}</div>
                <div className="text-sm text-gray-500">Total Documents Ingested</div>
              </div>

              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-2xl">⚙️</span>
                  <span className={`w-2 h-2 rounded-full ${stats.celeryWorkers === 'Active' ? 'bg-green-500' : 'bg-red-500'}`}></span>
                </div>
                <div className="text-2xl font-bold text-gray-900">{stats.celeryWorkers}</div>
                <div className="text-sm text-gray-500">Celery Workers</div>
              </div>

              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-2xl">💰</span>
                  <span className="text-xs font-medium text-blue-600 bg-blue-50 px-2 py-1 rounded">Est.</span>
                </div>
                <div className="text-2xl font-bold text-gray-900">${stats.monthlyCost}</div>
                <div className="text-sm text-gray-500">Monthly API Cost</div>
              </div>

              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-2xl">📡</span>
                  <span className={`w-2 h-2 rounded-full ${stats.kafkaStatus === 'Stable' ? 'bg-green-500' : 'bg-yellow-500'}`}></span>
                </div>
                <div className="text-2xl font-bold text-gray-900">{stats.kafkaStatus}</div>
                <div className="text-sm text-gray-500">Kafka Stream Status</div>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
              {/* Recent Collections */}
              <div className="lg:col-span-2 bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-lg font-semibold text-gray-900">Recent Collections</h2>
                  <button className="text-sm text-purple-600 hover:text-purple-700 font-medium">View All →</button>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {collections.length === 0 ? (
                    <div className="col-span-2 text-center py-8 text-gray-400">
                      No collections yet. Create your first one!
                    </div>
                  ) : (
                    collections.slice(0, 4).map((collection: any) => (
                      <div key={collection.id} className="border border-gray-200 rounded-lg p-4 hover:border-purple-300 hover:shadow-sm transition-all cursor-pointer">
                        <div className="flex items-start justify-between mb-3">
                          <div className="w-10 h-10 bg-gradient-to-br from-purple-100 to-pink-100 rounded-lg flex items-center justify-center text-xl">
                            📁
                          </div>
                          <span className="text-xs text-gray-500">{collection.domain || 'General'}</span>
                        </div>
                        <h3 className="font-medium text-gray-900 mb-2">{collection.name}</h3>
                        <div className="flex items-center justify-between text-xs text-gray-500">
                          <span>Indexing: 100%</span>
                          <div className="w-16 h-1.5 bg-gray-200 rounded-full overflow-hidden">
                            <div className="h-full bg-green-500 rounded-full" style={{ width: '100%' }}></div>
                          </div>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>

              {/* Quick Chat */}
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Ask AstraFlow</h2>
                <div className="space-y-4">
                  <textarea
                    placeholder="Ask anything across all collections..."
                    className="w-full h-32 px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  />
                  <button className="w-full px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg font-medium hover:from-purple-600 hover:to-pink-600 transition-all">
                    Send Query
                  </button>
                  <div className="text-xs text-gray-400 text-center">
                    Powered by Auto-Router
                  </div>
                </div>
              </div>
            </div>

            {/* Stock Ticker */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-semibold text-gray-900">Live Market Stream (Kafka)</h2>
                <span className="text-xs text-green-600 bg-green-50 px-2 py-1 rounded flex items-center">
                  <span className="w-1.5 h-1.5 bg-green-500 rounded-full mr-1.5 animate-pulse"></span>
                  Live
                </span>
              </div>
              
              <div className="flex space-x-6 overflow-x-auto pb-2">
                {stockTicker.map((stock) => (
                  <div key={stock.symbol} className="flex items-center space-x-3 min-w-fit">
                    <div className="font-semibold text-gray-900">{stock.symbol}</div>
                    <div className="text-lg font-bold text-gray-900">${stock.price}</div>
                    <div className={`text-sm font-medium ${stock.change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {stock.change >= 0 ? '↑' : '↓'} {Math.abs(stock.change)}%
                    </div>
                  </div>
                ))}
              </div>
            </div>

           {/* Design Prompt */}
           <DesignPrompt
             title="Copy this Prompt for Image Generation"
             prompt={"A high-fidelity UI design of a modern SaaS dashboard named \"AstraFlow\", light mode, clean white background, soft drop shadows. Left sidebar navigation with icons for \"Collections\", \"Workflows\", \"Stocks\". Main area features rounded widgets: one widget showing \"Document Ingestion Status\" with a progress bar, another widget showing \"Live Kafka Stream\" with a mini green line chart, and a widget for \"Recent AI Chats\". Aesthetic is similar to Linear or Vercel, minimalist, sans-serif typography, pastel accent colors. --ar 16:9 --v 6.0"}
           />
         </div>
       </main>
      </div>
    </div>
  );
}
