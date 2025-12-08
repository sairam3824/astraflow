'use client';

import { useState } from 'react';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';

export default function Collections() {
  const [collections, setCollections] = useState([
    { id: 1, name: 'Legal Contracts', domain: 'Legal', documents: 45, status: 'indexed', color: 'purple' },
    { id: 2, name: 'Q3 Financials', domain: 'Finance', documents: 23, status: 'indexed', color: 'blue' },
    { id: 3, name: 'Market Research', domain: 'Research', documents: 67, status: 'processing', color: 'green' },
    { id: 4, name: 'Technical Docs', domain: 'Engineering', documents: 89, status: 'indexed', color: 'orange' },
    { id: 5, name: 'HR Policies', domain: 'HR', documents: 34, status: 'indexed', color: 'pink' },
    { id: 6, name: 'Product Specs', domain: 'Product', documents: 56, status: 'indexed', color: 'indigo' }
  ]);

  const [showCreateModal, setShowCreateModal] = useState(false);

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        
        <main className="flex-1 overflow-y-auto">
          <div className="p-8">
            <div className="flex items-center justify-between mb-8">
              <div>
                <h1 className="text-2xl font-bold text-gray-900 mb-1">Collections</h1>
                <p className="text-sm text-gray-500">Manage your document collections and knowledge bases</p>
              </div>
              
              <button
                onClick={() => setShowCreateModal(true)}
                className="px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg font-medium hover:from-purple-600 hover:to-pink-600 shadow-sm"
              >
                + Create Collection
              </button>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="text-3xl mb-2">📚</div>
                <div className="text-2xl font-bold text-gray-900">{collections.length}</div>
                <div className="text-sm text-gray-500">Total Collections</div>
              </div>

              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="text-3xl mb-2">📄</div>
                <div className="text-2xl font-bold text-gray-900">
                  {collections.reduce((sum, c) => sum + c.documents, 0)}
                </div>
                <div className="text-sm text-gray-500">Total Documents</div>
              </div>

              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="text-3xl mb-2">✅</div>
                <div className="text-2xl font-bold text-gray-900">
                  {collections.filter(c => c.status === 'indexed').length}
                </div>
                <div className="text-sm text-gray-500">Indexed</div>
              </div>

              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="text-3xl mb-2">⚙️</div>
                <div className="text-2xl font-bold text-gray-900">
                  {collections.filter(c => c.status === 'processing').length}
                </div>
                <div className="text-sm text-gray-500">Processing</div>
              </div>
            </div>

            {/* Collections Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {collections.map((collection) => (
                <div
                  key={collection.id}
                  className="bg-white rounded-xl shadow-sm border border-gray-200 hover:shadow-lg hover:border-purple-300 transition-all cursor-pointer overflow-hidden"
                >
                  <div className={`h-2 bg-gradient-to-r from-${collection.color}-400 to-${collection.color}-600`}></div>
                  
                  <div className="p-6">
                    <div className="flex items-start justify-between mb-4">
                      <div className={`w-12 h-12 bg-gradient-to-br from-${collection.color}-100 to-${collection.color}-200 rounded-xl flex items-center justify-center text-2xl`}>
                        📁
                      </div>
                      
                      {collection.status === 'indexed' ? (
                        <span className="flex items-center text-xs text-green-600 bg-green-50 px-2 py-1 rounded">
                          <span className="w-1.5 h-1.5 bg-green-500 rounded-full mr-1"></span>
                          Indexed
                        </span>
                      ) : (
                        <span className="flex items-center text-xs text-yellow-600 bg-yellow-50 px-2 py-1 rounded">
                          <span className="w-1.5 h-1.5 bg-yellow-500 rounded-full mr-1 animate-pulse"></span>
                          Processing
                        </span>
                      )}
                    </div>

                    <h3 className="text-lg font-semibold text-gray-900 mb-1">{collection.name}</h3>
                    <p className="text-sm text-gray-500 mb-4">{collection.domain}</p>

                    <div className="flex items-center justify-between pt-4 border-t border-gray-200">
                      <div className="text-sm text-gray-600">
                        <span className="font-medium text-gray-900">{collection.documents}</span> documents
                      </div>
                      
                      <div className="flex space-x-2">
                        <button className="p-2 text-gray-400 hover:text-purple-600 hover:bg-purple-50 rounded-lg">
                          💬
                        </button>
                        <button className="p-2 text-gray-400 hover:text-purple-600 hover:bg-purple-50 rounded-lg">
                          ⚙️
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              ))}

              {/* Create New Card */}
              <button
                onClick={() => setShowCreateModal(true)}
                className="bg-white rounded-xl shadow-sm border-2 border-dashed border-gray-300 hover:border-purple-400 hover:bg-purple-50 transition-all p-6 flex flex-col items-center justify-center min-h-[240px]"
              >
                <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center text-3xl mb-4">
                  +
                </div>
                <div className="text-lg font-medium text-gray-900 mb-1">Create Collection</div>
                <div className="text-sm text-gray-500">Start a new knowledge base</div>
              </button>
            </div>
          </div>
        </main>
      </div>

      {/* Create Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md p-8">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Create Collection</h2>
              <button
                onClick={() => setShowCreateModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                ✕
              </button>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Collection Name
                </label>
                <input
                  type="text"
                  placeholder="e.g., Legal Contracts"
                  className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Domain
                </label>
                <select className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500">
                  <option>General</option>
                  <option>Legal</option>
                  <option>Finance</option>
                  <option>Research</option>
                  <option>Engineering</option>
                  <option>HR</option>
                  <option>Product</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Description (Optional)
                </label>
                <textarea
                  placeholder="Describe what this collection is for..."
                  className="w-full px-4 py-3 border border-gray-200 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-purple-500"
                  rows={3}
                />
              </div>

              <div className="flex space-x-3 pt-4">
                <button
                  onClick={() => setShowCreateModal(false)}
                  className="flex-1 px-4 py-3 border border-gray-200 text-gray-700 rounded-lg font-medium hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  onClick={() => setShowCreateModal(false)}
                  className="flex-1 px-4 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg font-medium hover:from-purple-600 hover:to-pink-600"
                >
                  Create
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
