'use client';

import { useState } from 'react';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';

export default function Settings() {
  const [activeTab, setActiveTab] = useState('general');

  const tabs = [
    { id: 'general', label: 'General', icon: '⚙️' },
    { id: 'models', label: 'AI Models', icon: '🤖' },
    { id: 'integrations', label: 'Integrations', icon: '🔌' },
    { id: 'billing', label: 'Billing', icon: '💳' }
  ];

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        
        <main className="flex-1 overflow-y-auto">
          <div className="p-8">
            <h1 className="text-2xl font-bold text-gray-900 mb-8">Settings</h1>

            <div className="flex space-x-8">
              {/* Tabs */}
              <div className="w-64">
                <nav className="space-y-1">
                  {tabs.map((tab) => (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-left ${
                        activeTab === tab.id
                          ? 'bg-purple-50 text-purple-600 font-medium'
                          : 'text-gray-600 hover:bg-gray-50'
                      }`}
                    >
                      <span className="text-xl">{tab.icon}</span>
                      <span>{tab.label}</span>
                    </button>
                  ))}
                </nav>
              </div>

              {/* Content */}
              <div className="flex-1 max-w-3xl">
                {activeTab === 'general' && (
                  <div className="space-y-6">
                    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                      <h2 className="text-lg font-semibold text-gray-900 mb-4">Profile</h2>
                      
                      <div className="space-y-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Display Name
                          </label>
                          <input
                            type="text"
                            defaultValue="User"
                            className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                          />
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Email
                          </label>
                          <input
                            type="email"
                            defaultValue="user@astraflow.ai"
                            className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                          />
                        </div>
                      </div>
                    </div>

                    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                      <h2 className="text-lg font-semibold text-gray-900 mb-4">Preferences</h2>
                      
                      <div className="space-y-4">
                        <div className="flex items-center justify-between">
                          <div>
                            <div className="font-medium text-gray-900">Dark Mode</div>
                            <div className="text-sm text-gray-500">Use dark theme</div>
                          </div>
                          <button className="w-12 h-6 bg-gray-200 rounded-full relative">
                            <div className="w-5 h-5 bg-white rounded-full absolute left-0.5 top-0.5"></div>
                          </button>
                        </div>

                        <div className="flex items-center justify-between">
                          <div>
                            <div className="font-medium text-gray-900">Notifications</div>
                            <div className="text-sm text-gray-500">Receive email notifications</div>
                          </div>
                          <button className="w-12 h-6 bg-purple-500 rounded-full relative">
                            <div className="w-5 h-5 bg-white rounded-full absolute right-0.5 top-0.5"></div>
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {activeTab === 'models' && (
                  <div className="space-y-6">
                    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                      <h2 className="text-lg font-semibold text-gray-900 mb-4">API Keys</h2>
                      
                      <div className="space-y-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            OpenAI API Key
                          </label>
                          <input
                            type="password"
                            placeholder="sk-..."
                            className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                          />
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Google AI API Key
                          </label>
                          <input
                            type="password"
                            placeholder="AIza..."
                            className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                          />
                        </div>

                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Anthropic API Key
                          </label>
                          <input
                            type="password"
                            placeholder="sk-ant-..."
                            className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                          />
                        </div>
                      </div>
                    </div>

                    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                      <h2 className="text-lg font-semibold text-gray-900 mb-4">Model Preferences</h2>
                      
                      <div className="space-y-4">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Default Model
                          </label>
                          <select className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500">
                            <option>Auto-Router</option>
                            <option>GPT-4</option>
                            <option>Gemini 1.5 Pro</option>
                            <option>Claude 3 Opus</option>
                          </select>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {activeTab === 'integrations' && (
                  <div className="space-y-6">
                    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                      <h2 className="text-lg font-semibold text-gray-900 mb-4">Connected Services</h2>
                      
                      <div className="space-y-4">
                        {[
                          { name: 'Kafka', status: 'connected', icon: '📡' },
                          { name: 'MinIO', status: 'connected', icon: '🗄️' },
                          { name: 'ChromaDB', status: 'connected', icon: '🔍' },
                          { name: 'Celery', status: 'connected', icon: '⚙️' }
                        ].map((service) => (
                          <div key={service.name} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                            <div className="flex items-center space-x-3">
                              <span className="text-2xl">{service.icon}</span>
                              <div>
                                <div className="font-medium text-gray-900">{service.name}</div>
                                <div className="text-sm text-green-600">Connected</div>
                              </div>
                            </div>
                            <button className="px-4 py-2 text-sm text-gray-600 hover:bg-gray-50 rounded-lg">
                              Configure
                            </button>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}

                {activeTab === 'billing' && (
                  <div className="space-y-6">
                    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                      <h2 className="text-lg font-semibold text-gray-900 mb-4">Current Usage</h2>
                      
                      <div className="space-y-4">
                        <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                          <div>
                            <div className="text-sm text-gray-600">This Month</div>
                            <div className="text-2xl font-bold text-gray-900">$0.00</div>
                          </div>
                          <div className="text-right">
                            <div className="text-sm text-gray-600">API Calls</div>
                            <div className="text-lg font-semibold text-gray-900">0</div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                <div className="flex justify-end pt-6">
                  <button className="px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg font-medium hover:from-purple-600 hover:to-pink-600">
                    Save Changes
                  </button>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
