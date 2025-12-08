'use client';

import { useState } from 'react';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
import DesignPrompt from '../components/DesignPrompt';

export default function Workflows() {
  const [nodes, setNodes] = useState([
    { id: 1, type: 'start', label: 'Ingest PDF', icon: '📄', x: 100, y: 200 },
    { id: 2, type: 'process', label: 'Vector Search', icon: '🔍', x: 300, y: 200 },
    { id: 3, type: 'router', label: 'Router', icon: '🔀', x: 500, y: 200 },
    { id: 4, type: 'llm', label: 'LLM: Gemini', icon: '🤖', x: 700, y: 150 },
    { id: 5, type: 'llm', label: 'LLM: OpenAI', icon: '🤖', x: 700, y: 250 },
    { id: 6, type: 'end', label: 'Response', icon: '✅', x: 900, y: 200 }
  ]);
  
  const [connections] = useState([
    { from: 1, to: 2 },
    { from: 2, to: 3 },
    { from: 3, to: 4 },
    { from: 3, to: 5 },
    { from: 4, to: 6 },
    { from: 5, to: 6 }
  ]);

  const [selectedNode, setSelectedNode] = useState<any>(null);
  const [showProperties, setShowProperties] = useState(false);

  const nodeTypes = [
    { type: 'start', label: 'Start', icon: '▶️' },
    { type: 'process', label: 'Vector Search', icon: '🔍' },
    { type: 'router', label: 'Router', icon: '🔀' },
    { type: 'llm', label: 'LLM', icon: '🤖' },
    { type: 'tool', label: 'Tool', icon: '🔧' },
    { type: 'end', label: 'End', icon: '✅' }
  ];

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        
        <div className="flex-1 flex overflow-hidden">
          {/* Canvas */}
          <div className="flex-1 relative bg-white" style={{
            backgroundImage: 'radial-gradient(circle, #e5e7eb 1px, transparent 1px)',
            backgroundSize: '20px 20px'
          }}>
            {/* Floating Toolbar */}
            <div className="absolute top-6 left-1/2 transform -translate-x-1/2 z-10">
              <div className="bg-white rounded-xl shadow-lg border border-gray-200 px-4 py-3 flex items-center space-x-3">
                <button className="px-4 py-2 bg-purple-500 text-white rounded-lg text-sm font-medium hover:bg-purple-600">
                  + Add Node
                </button>
                <div className="w-px h-6 bg-gray-200"></div>
                <button className="px-4 py-2 text-gray-700 hover:bg-gray-50 rounded-lg text-sm font-medium">
                  Test Run
                </button>
                <button className="px-4 py-2 text-gray-700 hover:bg-gray-50 rounded-lg text-sm font-medium">
                  Save JSON
                </button>
                <div className="w-px h-6 bg-gray-200"></div>
                <button className="p-2 text-gray-400 hover:text-gray-600">
                  <span className="text-lg">↩️</span>
                </button>
                <button className="p-2 text-gray-400 hover:text-gray-600">
                  <span className="text-lg">↪️</span>
                </button>
              </div>
            </div>

            {/* SVG for connections */}
            <svg className="absolute inset-0 w-full h-full pointer-events-none">
              {connections.map((conn, idx) => {
                const fromNode = nodes.find(n => n.id === conn.from);
                const toNode = nodes.find(n => n.id === conn.to);
                if (!fromNode || !toNode) return null;

                const x1 = fromNode.x + 80;
                const y1 = fromNode.y + 40;
                const x2 = toNode.x;
                const y2 = toNode.y + 40;
                
                const midX = (x1 + x2) / 2;
                
                return (
                  <path
                    key={idx}
                    d={`M ${x1} ${y1} C ${midX} ${y1}, ${midX} ${y2}, ${x2} ${y2}`}
                    stroke="#9333ea"
                    strokeWidth="2"
                    fill="none"
                    strokeDasharray="5,5"
                  />
                );
              })}
            </svg>

            {/* Nodes */}
            {nodes.map((node) => (
              <div
                key={node.id}
                className={`absolute cursor-pointer transition-all ${
                  selectedNode?.id === node.id ? 'ring-2 ring-purple-500' : ''
                }`}
                style={{ left: node.x, top: node.y }}
                onClick={() => {
                  setSelectedNode(node);
                  setShowProperties(true);
                }}
              >
                <div className="bg-white rounded-xl shadow-lg border-2 border-gray-200 hover:border-purple-300 hover:shadow-xl transition-all w-40 p-4">
                  <div className="flex items-center space-x-3 mb-2">
                    <span className="text-2xl">{node.icon}</span>
                    <div className="flex-1">
                      <div className="font-semibold text-sm text-gray-900">{node.label}</div>
                      <div className="text-xs text-gray-500">{node.type}</div>
                    </div>
                  </div>
                  
                  {node.type === 'router' && (
                    <div className="mt-2 pt-2 border-t border-gray-200">
                      <div className="text-xs text-gray-500">2 branches</div>
                    </div>
                  )}
                  
                  {node.type === 'llm' && (
                    <div className="mt-2 pt-2 border-t border-gray-200">
                      <div className="text-xs text-gray-500">Model: {node.label.split(': ')[1]}</div>
                    </div>
                  )}
                </div>
              </div>
            ))}

            {/* Node Palette */}
            <div className="absolute bottom-6 left-6 bg-white rounded-xl shadow-lg border border-gray-200 p-4">
              <div className="text-sm font-semibold text-gray-900 mb-3">Node Types</div>
              <div className="space-y-2">
                {nodeTypes.map((type) => (
                  <button
                    key={type.type}
                    className="w-full flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-gray-50 text-left"
                  >
                    <span className="text-xl">{type.icon}</span>
                    <span className="text-sm text-gray-700">{type.label}</span>
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Properties Panel */}
          {showProperties && selectedNode && (
            <div className="w-96 bg-white border-l border-gray-200 overflow-y-auto">
              <div className="p-6">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="font-semibold text-gray-900">Node Properties</h3>
                  <button
                    onClick={() => setShowProperties(false)}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    ✕
                  </button>
                </div>

                <div className="space-y-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Node Type
                    </label>
                    <div className="px-4 py-3 bg-gray-50 rounded-lg text-sm text-gray-900">
                      {selectedNode.type}
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Label
                    </label>
                    <input
                      type="text"
                      value={selectedNode.label}
                      className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                  </div>

                  {selectedNode.type === 'llm' && (
                    <>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Model
                        </label>
                        <select className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500">
                          <option>GPT-4</option>
                          <option>Gemini 1.5 Pro</option>
                          <option>Claude 3 Opus</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Temperature
                        </label>
                        <input
                          type="range"
                          min="0"
                          max="1"
                          step="0.1"
                          defaultValue="0.7"
                          className="w-full"
                        />
                        <div className="flex justify-between text-xs text-gray-500 mt-1">
                          <span>Precise</span>
                          <span>Creative</span>
                        </div>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Max Tokens
                        </label>
                        <input
                          type="number"
                          defaultValue="2000"
                          className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                        />
                      </div>
                    </>
                  )}

                  {selectedNode.type === 'router' && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Routing Logic
                      </label>
                      <textarea
                        className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 font-mono text-sm"
                        rows={6}
                        defaultValue={`if (query.complexity > 0.7) {
  return "gemini";
} else {
  return "openai";
}`}
                      />
                    </div>
                  )}

                  <div className="pt-4 border-t border-gray-200">
                    <button className="w-full px-4 py-2 bg-red-50 text-red-600 rounded-lg text-sm font-medium hover:bg-red-100">
                      Delete Node
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

       {/* Design Prompt */}
       <div className="px-8 pb-8">
         <DesignPrompt
           title="Copy this Prompt for Image Generation"
           prompt={"A node-based visual workflow editor UI, similar to n8n or LangFlow. White background with a subtle dot grid. Colorful rounded rectangular nodes connected by smooth curved lines. Nodes are labeled \"Start\", \"Vector Search\", \"LLM Router\", \"Summarize\". A floating properties panel on the right side. Clean, minimal, tech-focused design. --ar 16:9"}
         />
       </div>
     </div>
   </div>
 );
}
