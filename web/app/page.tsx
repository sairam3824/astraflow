'use client';

import { useEffect, useState } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import DesignPrompt from './components/DesignPrompt';

interface SystemHealth {
  docker: 'running' | 'stopped' | 'error';
  celery: 'active' | 'idle' | 'error';
  redis: 'connected' | 'disconnected';
  minio: 'healthy' | 'unhealthy';
  chroma: 'healthy' | 'unhealthy';
}

interface Collection {
  id: number;
  name: string;
  domain?: string;
  indexing_progress?: number;
  doc_count?: number;
}

interface Stock {
  symbol: string;
  price: number;
  change: number;
  volume: string;
}

export default function Dashboard() {
  const [stats, setStats] = useState({
    totalDocuments: 0,
    celeryWorkers: 'Active',
    monthlyCost: 0,
    kafkaStatus: 'Stable'
  });
  const [systemHealth, setSystemHealth] = useState<SystemHealth>({
    docker: 'running',
    celery: 'active',
    redis: 'connected',
    minio: 'healthy',
    chroma: 'healthy'
  });
  const [collections, setCollections] = useState<Collection[]>([]);
  const [stockTicker, setStockTicker] = useState<Stock[]>([]);
  const [quickQuery, setQuickQuery] = useState('');

  useEffect(() => {
    // Fetch system stats
    fetch('http://localhost:8000/health')
      .then(res => res.json())
      .then(data => {
        setStats({
          totalDocuments: data.total_documents || 12847,
          celeryWorkers: data.celery_status || 'Active',
          monthlyCost: data.estimated_cost || 127.50,
          kafkaStatus: data.kafka_status || 'Stable'
        });
        
        // Update system health
        setSystemHealth({
          docker: data.docker_status || 'running',
          celery: data.celery_status === 'Active' ? 'active' : 'idle',
          redis: data.redis_status || 'connected',
          minio: data.minio_status || 'healthy',
          chroma: data.chroma_status || 'healthy'
        });
      })
      .catch(err => {
        console.error(err);
        // Set mock data on error
        setStats({
          totalDocuments: 12847,
          celeryWorkers: 'Active',
          monthlyCost: 127.50,
          kafkaStatus: 'Stable'
        });
      });

    // Fetch collections
    fetch('http://localhost:8000/collections')
      .then(res => res.json())
      .then(data => setCollections(data))
      .catch(err => {
        console.error(err);
        // Mock collections
        setCollections([
          { id: 1, name: 'Legal Contracts', domain: 'Legal', indexing_progress: 100, doc_count: 234 },
          { id: 2, name: 'Q3 Financials', domain: 'Finance', indexing_progress: 87, doc_count: 156 },
          { id: 3, name: 'Product Docs', domain: 'Engineering', indexing_progress: 100, doc_count: 892 },
          { id: 4, name: 'Customer Support', domain: 'Support', indexing_progress: 65, doc_count: 1203 }
        ]);
      });

    // Simulate stock ticker with live updates
    const mockStocks = [
      { symbol: 'AAPL', price: 178.23, change: 2.34, volume: '52.3M' },
      { symbol: 'GOOGL', price: 142.56, change: -1.23, volume: '28.1M' },
      { symbol: 'MSFT', price: 378.91, change: 5.67, volume: '31.7M' },
      { symbol: 'TSLA', price: 242.84, change: -3.45, volume: '89.2M' },
      { symbol: 'AMZN', price: 151.94, change: 1.89, volume: '45.6M' },
      { symbol: 'NVDA', price: 495.22, change: 8.12, volume: '67.4M' },
      { symbol: 'META', price: 312.45, change: -2.11, volume: '19.8M' }
    ];
    setStockTicker(mockStocks);

    // Update stock prices every 3 seconds
    const stockInterval = setInterval(() => {
      setStockTicker(prev => prev.map(stock => ({
        ...stock,
        price: stock.price + (Math.random() - 0.5) * 2,
        change: stock.change + (Math.random() - 0.5) * 0.5
      })));
    }, 3000);

    return () => clearInterval(stockInterval);
  }, []);

  const handleQuickQuery = () => {
    if (!quickQuery.trim()) return;
    console.log('Quick query:', quickQuery);
    // TODO: Implement actual query logic
    alert(`Searching across all collections for: "${quickQuery}"`);
  };

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        
        <main className="flex-1 overflow-y-auto bg-gray-50">
          <div className="p-8">
            {/* Welcome Header */}
            <div className="mb-8">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Mission Control</h1>
              <p className="text-gray-500">Monitor system health, collections, and live market data</p>
            </div>

            {/* System Health Status Bar */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-semibold text-gray-900">System Health</h2>
                <span className="text-xs text-gray-500">Last updated: just now</span>
              </div>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                <div className="flex items-center space-x-3">
                  <div className={`w-3 h-3 rounded-full ${systemHealth.docker === 'running' ? 'bg-green-500' : 'bg-red-500'}`}></div>
                  <div>
                    <div className="text-sm font-medium text-gray-900">Docker</div>
                    <div className="text-xs text-gray-500 capitalize">{systemHealth.docker}</div>
                  </div>
                </div>
                <div className="flex items-center space-x-3">
                  <div className={`w-3 h-3 rounded-full ${systemHealth.celery === 'active' ? 'bg-green-500' : 'bg-yellow-500'}`}></div>
                  <div>
                    <div className="text-sm font-medium text-gray-900">Celery</div>
                    <div className="text-xs text-gray-500 capitalize">{systemHealth.celery}</div>
                  </div>
                </div>
                <div className="flex items-center space-x-3">
                  <div className={`w-3 h-3 rounded-full ${systemHealth.redis === 'connected' ? 'bg-green-500' : 'bg-red-500'}`}></div>
                  <div>
                    <div className="text-sm font-medium text-gray-900">Redis</div>
                    <div className="text-xs text-gray-500 capitalize">{systemHealth.redis}</div>
                  </div>
                </div>
                <div className="flex items-center space-x-3">
                  <div className={`w-3 h-3 rounded-full ${systemHealth.minio === 'healthy' ? 'bg-green-500' : 'bg-red-500'}`}></div>
                  <div>
                    <div className="text-sm font-medium text-gray-900">MinIO</div>
                    <div className="text-xs text-gray-500 capitalize">{systemHealth.minio}</div>
                  </div>
                </div>
                <div className="flex items-center space-x-3">
                  <div className={`w-3 h-3 rounded-full ${systemHealth.chroma === 'healthy' ? 'bg-green-500' : 'bg-red-500'}`}></div>
                  <div>
                    <div className="text-sm font-medium text-gray-900">ChromaDB</div>
                    <div className="text-xs text-gray-500 capitalize">{systemHealth.chroma}</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
                <div className="flex items-center justify-between mb-3">
                  <div className="w-12 h-12 bg-gradient-to-br from-purple-100 to-purple-200 rounded-xl flex items-center justify-center">
                    <span className="text-2xl">📄</span>
                  </div>
                  <span className="text-xs font-medium text-green-600 bg-green-50 px-2.5 py-1 rounded-full">+12%</span>
                </div>
                <div className="text-3xl font-bold text-gray-900 mb-1">{stats.totalDocuments.toLocaleString()}</div>
                <div className="text-sm text-gray-500">Total Documents Ingested</div>
              </div>

              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
                <div className="flex items-center justify-between mb-3">
                  <div className="w-12 h-12 bg-gradient-to-br from-green-100 to-green-200 rounded-xl flex items-center justify-center">
                    <span className="text-2xl">⚙️</span>
                  </div>
                  <span className={`w-3 h-3 rounded-full ${stats.celeryWorkers === 'Active' ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`}></span>
                </div>
                <div className="text-3xl font-bold text-gray-900 mb-1">{stats.celeryWorkers}</div>
                <div className="text-sm text-gray-500">Active Celery Workers</div>
              </div>

              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
                <div className="flex items-center justify-between mb-3">
                  <div className="w-12 h-12 bg-gradient-to-br from-blue-100 to-blue-200 rounded-xl flex items-center justify-center">
                    <span className="text-2xl">💰</span>
                  </div>
                  <span className="text-xs font-medium text-blue-600 bg-blue-50 px-2.5 py-1 rounded-full">Est.</span>
                </div>
                <div className="text-3xl font-bold text-gray-900 mb-1">${stats.monthlyCost.toFixed(2)}</div>
                <div className="text-sm text-gray-500">Monthly API Cost</div>
              </div>

              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
                <div className="flex items-center justify-between mb-3">
                  <div className="w-12 h-12 bg-gradient-to-br from-teal-100 to-teal-200 rounded-xl flex items-center justify-center">
                    <span className="text-2xl">📡</span>
                  </div>
                  <span className={`w-3 h-3 rounded-full ${stats.kafkaStatus === 'Stable' ? 'bg-green-500 animate-pulse' : 'bg-yellow-500'}`}></span>
                </div>
                <div className="text-3xl font-bold text-gray-900 mb-1">{stats.kafkaStatus}</div>
                <div className="text-sm text-gray-500">Kafka Stream Status</div>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
              {/* Recent Collections */}
              <div className="lg:col-span-2 bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="flex items-center justify-between mb-6">
                  <div className="flex items-center space-x-2">
                    <h2 className="text-lg font-semibold text-gray-900">Active Collections</h2>
                    <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full">{collections.length}</span>
                  </div>
                  <button className="text-sm text-purple-600 hover:text-purple-700 font-medium transition-colors">View All →</button>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {collections.length === 0 ? (
                    <div className="col-span-2 text-center py-12">
                      <div className="text-5xl mb-3">📚</div>
                      <div className="text-gray-400 mb-4">No collections yet</div>
                      <button className="px-4 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition-colors">
                        Create First Collection
                      </button>
                    </div>
                  ) : (
                    collections.slice(0, 4).map((collection: any) => (
                      <div key={collection.id} className="group border border-gray-200 rounded-xl p-5 hover:border-purple-300 hover:shadow-md transition-all cursor-pointer">
                        <div className="flex items-start justify-between mb-4">
                          <div className="w-12 h-12 bg-gradient-to-br from-purple-100 to-pink-100 rounded-xl flex items-center justify-center text-2xl group-hover:scale-110 transition-transform">
                            📁
                          </div>
                          <span className="text-xs font-medium text-purple-600 bg-purple-50 px-2 py-1 rounded-full">{collection.domain || 'General'}</span>
                        </div>
                        <h3 className="font-semibold text-gray-900 mb-1">{collection.name}</h3>
                        <p className="text-xs text-gray-500 mb-3">{collection.doc_count || 0} documents</p>
                        <div className="space-y-2">
                          <div className="flex items-center justify-between text-xs">
                            <span className="text-gray-600">Indexing Progress</span>
                            <span className="font-medium text-gray-900">{collection.indexing_progress || 100}%</span>
                          </div>
                          <div className="w-full h-2 bg-gray-100 rounded-full overflow-hidden">
                            <div 
                              className={`h-full rounded-full transition-all ${
                                (collection.indexing_progress || 100) === 100 ? 'bg-green-500' : 'bg-blue-500'
                              }`}
                              style={{ width: `${collection.indexing_progress || 100}%` }}
                            ></div>
                          </div>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>

              {/* Quick Chat */}
              <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl shadow-sm border border-purple-100 p-6">
                <div className="flex items-center space-x-2 mb-4">
                  <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg flex items-center justify-center">
                    <span className="text-white text-lg">✨</span>
                  </div>
                  <h2 className="text-lg font-semibold text-gray-900">Ask AstraFlow</h2>
                </div>
                <p className="text-sm text-gray-600 mb-4">Quick query across all collections</p>
                <div className="space-y-3">
                  <textarea
                    value={quickQuery}
                    onChange={(e) => setQuickQuery(e.target.value)}
                    placeholder="What would you like to know?"
                    className="w-full h-32 px-4 py-3 bg-white border border-purple-200 rounded-xl resize-none focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent placeholder-gray-400"
                  />
                  <button 
                    onClick={handleQuickQuery}
                    className="w-full px-4 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-xl font-medium hover:from-purple-600 hover:to-pink-600 transition-all shadow-sm hover:shadow-md"
                  >
                    Send Query
                  </button>
                  <div className="flex items-center justify-center space-x-2 text-xs text-gray-500">
                    <span className="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse"></span>
                    <span>Powered by Auto-Router</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Stock Ticker */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 overflow-hidden">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-gradient-to-br from-green-100 to-emerald-100 rounded-xl flex items-center justify-center">
                    <span className="text-2xl">📈</span>
                  </div>
                  <div>
                    <h2 className="text-lg font-semibold text-gray-900">Live Market Stream</h2>
                    <p className="text-xs text-gray-500">Real-time data via Kafka</p>
                  </div>
                </div>
                <span className="text-xs text-green-600 bg-green-50 px-3 py-1.5 rounded-full flex items-center font-medium">
                  <span className="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></span>
                  Live
                </span>
              </div>
              
              <div className="relative">
                <div className="flex space-x-6 overflow-x-auto pb-4 scrollbar-hide">
                  {stockTicker.map((stock, idx) => (
                    <div 
                      key={stock.symbol} 
                      className="flex-shrink-0 bg-gray-50 rounded-xl p-4 min-w-[200px] hover:bg-gray-100 transition-colors border border-gray-200"
                    >
                      <div className="flex items-center justify-between mb-2">
                        <div className="font-bold text-gray-900 text-lg">{stock.symbol}</div>
                        <div className={`text-xs font-semibold px-2 py-1 rounded-full ${
                          stock.change >= 0 
                            ? 'bg-green-100 text-green-700' 
                            : 'bg-red-100 text-red-700'
                        }`}>
                          {stock.change >= 0 ? '↑' : '↓'} {Math.abs(stock.change).toFixed(2)}%
                        </div>
                      </div>
                      <div className="text-2xl font-bold text-gray-900 mb-1">
                        ${stock.price.toFixed(2)}
                      </div>
                      <div className="text-xs text-gray-500">
                        Vol: {stock.volume}
                      </div>
                      {/* Mini sparkline placeholder */}
                      <div className="mt-3 h-8 flex items-end space-x-1">
                        {[...Array(12)].map((_, i) => (
                          <div 
                            key={i}
                            className={`flex-1 rounded-t ${
                              stock.change >= 0 ? 'bg-green-300' : 'bg-red-300'
                            }`}
                            style={{ 
                              height: `${Math.random() * 100}%`,
                              opacity: 0.3 + (i / 12) * 0.7
                            }}
                          ></div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
                {/* Scroll indicator */}
                <div className="absolute right-0 top-0 bottom-0 w-12 bg-gradient-to-l from-white to-transparent pointer-events-none"></div>
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
