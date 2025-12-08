'use client';

import { useEffect, useState } from 'react';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
import DesignPrompt from '../components/DesignPrompt';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function Stocks() {
  const [selectedSymbol, setSelectedSymbol] = useState('AAPL');
  const [chartData, setChartData] = useState<any[]>([]);
  const [indicators, setIndicators] = useState({
    sma20: 178.45,
    rsi: 62.3,
    volatility: 1.8,
    volume: 52340000
  });
  const [kafkaLogs, setKafkaLogs] = useState<any[]>([]);

  useEffect(() => {
    // Generate mock chart data
    const mockData = [];
    const basePrice = 175;
    for (let i = 0; i < 50; i++) {
      mockData.push({
        time: `${9 + Math.floor(i / 12)}:${(i % 12) * 5}`,
        price: basePrice + Math.random() * 10 - 5,
        volume: Math.floor(Math.random() * 1000000) + 500000
      });
    }
    setChartData(mockData);

    // Simulate Kafka logs
    const mockLogs = [
      { timestamp: '2024-12-08 14:23:45', symbol: 'AAPL', price: 178.23, volume: 1234567, type: 'TRADE' },
      { timestamp: '2024-12-08 14:23:46', symbol: 'AAPL', price: 178.25, volume: 987654, type: 'TRADE' },
      { timestamp: '2024-12-08 14:23:47', symbol: 'GOOGL', price: 142.56, volume: 654321, type: 'TRADE' }
    ];
    setKafkaLogs(mockLogs);

    // Simulate real-time updates
    const interval = setInterval(() => {
      const newLog = {
        timestamp: new Date().toISOString().replace('T', ' ').substring(0, 19),
        symbol: selectedSymbol,
        price: (175 + Math.random() * 10).toFixed(2),
        volume: Math.floor(Math.random() * 1000000) + 500000,
        type: 'TRADE'
      };
      setKafkaLogs(prev => [newLog, ...prev.slice(0, 19)]);
      
      // Update indicators
      setIndicators(prev => ({
        ...prev,
        rsi: Math.max(0, Math.min(100, prev.rsi + (Math.random() - 0.5) * 5)),
        volatility: Math.max(0, prev.volatility + (Math.random() - 0.5) * 0.2)
      }));
    }, 2000);

    return () => clearInterval(interval);
  }, [selectedSymbol]);

  const symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN'];

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        
        <main className="flex-1 overflow-y-auto">
          <div className="p-8">
            {/* Header */}
            <div className="flex items-center justify-between mb-6">
              <div>
                <h1 className="text-2xl font-bold text-gray-900 mb-1">Market Stream</h1>
                <p className="text-sm text-gray-500">Kafka Topic: market.ticks</p>
              </div>
              
              <div className="flex items-center space-x-3">
                <select
                  value={selectedSymbol}
                  onChange={(e) => setSelectedSymbol(e.target.value)}
                  className="px-4 py-2 bg-white border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                >
                  {symbols.map(symbol => (
                    <option key={symbol} value={symbol}>{symbol}</option>
                  ))}
                </select>
                
                <span className="flex items-center text-sm text-green-600 bg-green-50 px-3 py-2 rounded-lg">
                  <span className="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></span>
                  Live Streaming
                </span>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-6">
              {/* Main Chart */}
              <div className="lg:col-span-3 bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="flex items-center justify-between mb-6">
                  <div>
                    <h2 className="text-lg font-semibold text-gray-900">{selectedSymbol}</h2>
                    <div className="flex items-center space-x-3 mt-1">
                      <span className="text-2xl font-bold text-gray-900">
                        ${chartData[chartData.length - 1]?.price.toFixed(2) || '0.00'}
                      </span>
                      <span className="text-sm text-green-600 bg-green-50 px-2 py-1 rounded">
                        +2.34%
                      </span>
                    </div>
                  </div>
                  
                  <div className="flex space-x-2">
                    <button className="px-3 py-1.5 text-sm text-gray-600 hover:bg-gray-50 rounded-lg">1D</button>
                    <button className="px-3 py-1.5 text-sm bg-purple-50 text-purple-600 rounded-lg">1W</button>
                    <button className="px-3 py-1.5 text-sm text-gray-600 hover:bg-gray-50 rounded-lg">1M</button>
                    <button className="px-3 py-1.5 text-sm text-gray-600 hover:bg-gray-50 rounded-lg">1Y</button>
                  </div>
                </div>

                <ResponsiveContainer width="100%" height={400}>
                  <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                    <XAxis 
                      dataKey="time" 
                      stroke="#9ca3af"
                      style={{ fontSize: '12px' }}
                    />
                    <YAxis 
                      stroke="#9ca3af"
                      style={{ fontSize: '12px' }}
                      domain={['dataMin - 2', 'dataMax + 2']}
                    />
                    <Tooltip 
                      contentStyle={{
                        backgroundColor: '#fff',
                        border: '1px solid #e5e7eb',
                        borderRadius: '8px',
                        padding: '8px 12px'
                      }}
                    />
                    <Line 
                      type="monotone" 
                      dataKey="price" 
                      stroke="#9333ea" 
                      strokeWidth={2}
                      dot={false}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>

              {/* Indicators Panel */}
              <div className="space-y-6">
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                  <h3 className="font-semibold text-gray-900 mb-4">Technical Indicators</h3>
                  
                  <div className="space-y-4">
                    <div>
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm text-gray-600">SMA (20)</span>
                        <span className={`text-sm font-semibold ${indicators.sma20 > 175 ? 'text-green-600' : 'text-red-600'}`}>
                          ${indicators.sma20.toFixed(2)}
                        </span>
                      </div>
                      <div className="w-full h-1.5 bg-gray-200 rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-green-500 rounded-full transition-all"
                          style={{ width: '65%' }}
                        ></div>
                      </div>
                    </div>

                    <div>
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm text-gray-600">RSI</span>
                        <span className={`text-sm font-semibold ${
                          indicators.rsi > 70 ? 'text-red-600' : 
                          indicators.rsi < 30 ? 'text-green-600' : 
                          'text-yellow-600'
                        }`}>
                          {indicators.rsi.toFixed(1)}
                        </span>
                      </div>
                      <div className="w-full h-1.5 bg-gray-200 rounded-full overflow-hidden">
                        <div 
                          className={`h-full rounded-full transition-all ${
                            indicators.rsi > 70 ? 'bg-red-500' : 
                            indicators.rsi < 30 ? 'bg-green-500' : 
                            'bg-yellow-500'
                          }`}
                          style={{ width: `${indicators.rsi}%` }}
                        ></div>
                      </div>
                    </div>

                    <div>
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm text-gray-600">Volatility</span>
                        <span className="text-sm font-semibold text-gray-900">
                          {indicators.volatility.toFixed(2)}%
                        </span>
                      </div>
                      <div className="w-full h-1.5 bg-gray-200 rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-purple-500 rounded-full transition-all"
                          style={{ width: `${Math.min(indicators.volatility * 20, 100)}%` }}
                        ></div>
                      </div>
                    </div>

                    <div className="pt-4 border-t border-gray-200">
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-600">Volume</span>
                        <span className="text-sm font-semibold text-gray-900">
                          {(indicators.volume / 1000000).toFixed(1)}M
                        </span>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl shadow-sm p-6 text-white">
                  <h3 className="font-semibold mb-3">AI Analysis</h3>
                  <p className="text-sm opacity-90 leading-relaxed">
                    Strong bullish momentum detected. RSI indicates healthy buying pressure. Consider entry points near support levels.
                  </p>
                  <button className="mt-4 w-full px-4 py-2 bg-white/20 hover:bg-white/30 rounded-lg text-sm font-medium transition-colors">
                    Get Full Report
                  </button>
                </div>
              </div>
            </div>

            {/* Kafka Console */}
            <div className="bg-gray-900 rounded-xl shadow-sm border border-gray-700 overflow-hidden">
              <div className="px-6 py-4 border-b border-gray-700 flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <span className="text-green-400 text-sm font-mono">●</span>
                  <h3 className="font-semibold text-white">Kafka Stream Console</h3>
                  <span className="text-xs text-gray-400">market.ticks</span>
                </div>
                <button className="text-xs text-gray-400 hover:text-white">Clear</button>
              </div>
              
              <div className="p-6 font-mono text-xs text-green-400 h-64 overflow-y-auto">
                {kafkaLogs.map((log, idx) => (
                  <div key={idx} className="mb-2 hover:bg-gray-800 px-2 py-1 rounded">
                    <span className="text-gray-500">[{log.timestamp}]</span>{' '}
                    <span className="text-blue-400">{log.type}</span>{' '}
                    <span className="text-yellow-400">{log.symbol}</span>{' '}
                    <span className="text-white">price:</span> {log.price}{' '}
                    <span className="text-white">volume:</span> {log.volume.toLocaleString()}
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Design Prompt */}
          <div className="px-8 pb-8">
            <DesignPrompt
              title="Copy this Prompt for Image Generation"
              prompt={"A financial fintech dashboard UI, light mode. Large Japanese candlestick chart in the center with moving average lines. Right side panel displays a table of live stock indicators with red and green numbers. Bottom section is a terminal-style log window showing streaming JSON data. Professional, data-heavy but clean layout. --ar 16:9"}
            />
          </div>
        </main>
      </div>
    </div>
  );
}
