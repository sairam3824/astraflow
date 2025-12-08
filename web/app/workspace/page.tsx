'use client';

import { useState } from 'react';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';
import DesignPrompt from '../components/DesignPrompt';

export default function Workspace() {
  const [selectedModel, setSelectedModel] = useState('Auto-Router');
  const [messages, setMessages] = useState<any[]>([
    {
      role: 'assistant',
      content: 'Hello! I can help you analyze documents in your collection. What would you like to know?',
      citations: []
    }
  ]);
  const [input, setInput] = useState('');
  const [files, setFiles] = useState([
    { id: 1, name: 'Q3_Financial_Report.pdf', status: 'indexed', pages: 45 },
    { id: 2, name: 'Legal_Contract_2024.pdf', status: 'indexed', pages: 23 },
    { id: 3, name: 'Market_Analysis.pdf', status: 'processing', pages: 67 }
  ]);
  const [showContext, setShowContext] = useState(false);
  const [isThinking, setIsThinking] = useState(false);

  const models = ['Auto-Router', 'GPT-4', 'Gemini 1.5 Pro', 'Claude 3 Opus'];

  const handleSend = () => {
    if (!input.trim()) return;
    
    setMessages([...messages, { role: 'user', content: input }]);
    setInput('');
    setIsThinking(true);
    
    // Simulate AI response
    setTimeout(() => {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Based on the Q3 Financial Report, revenue increased by 23% compared to Q2. The main drivers were increased sales in the APAC region and successful product launches.',
        citations: [
          { file: 'Q3_Financial_Report.pdf', page: 12, text: 'Revenue growth of 23% YoY...' },
          { file: 'Q3_Financial_Report.pdf', page: 15, text: 'APAC region contributed 45%...' }
        ]
      }]);
      setIsThinking(false);
      setShowContext(true);
    }, 2000);
  };

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        
        <div className="flex-1 flex overflow-hidden">
          {/* Left Panel - Collection Manager */}
          <div className="w-80 bg-white border-r border-gray-200 flex flex-col">
            <div className="p-4 border-b border-gray-200">
              <h2 className="font-semibold text-gray-900 mb-3">Current Collection</h2>
              <button className="w-full px-4 py-2 bg-purple-500 text-white rounded-lg font-medium hover:bg-purple-600 transition-colors">
                + Upload Document
              </button>
            </div>
            
            <div className="flex-1 overflow-y-auto p-4">
              <div className="space-y-2">
                {files.map((file) => (
                  <div
                    key={file.id}
                    className="flex items-start space-x-3 p-3 rounded-lg hover:bg-gray-50 cursor-pointer border border-gray-200"
                  >
                    <div className="text-2xl">📄</div>
                    <div className="flex-1 min-w-0">
                      <div className="font-medium text-sm text-gray-900 truncate">{file.name}</div>
                      <div className="text-xs text-gray-500">{file.pages} pages</div>
                      <div className="flex items-center mt-1">
                        {file.status === 'indexed' ? (
                          <span className="flex items-center text-xs text-green-600">
                            <span className="w-1.5 h-1.5 bg-green-500 rounded-full mr-1"></span>
                            Indexed
                          </span>
                        ) : (
                          <span className="flex items-center text-xs text-yellow-600">
                            <span className="w-1.5 h-1.5 bg-yellow-500 rounded-full mr-1 animate-pulse"></span>
                            Processing
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Center Panel - Chat */}
          <div className="flex-1 flex flex-col bg-white">
            {/* Model Selector */}
            <div className="px-6 py-4 border-b border-gray-200">
              <div className="flex items-center space-x-4">
                <label className="text-sm font-medium text-gray-700">Model:</label>
                <select
                  value={selectedModel}
                  onChange={(e) => setSelectedModel(e.target.value)}
                  className="px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                >
                  {models.map((model) => (
                    <option key={model} value={model}>{model}</option>
                  ))}
                </select>
                <button
                  onClick={() => setShowContext(!showContext)}
                  className="ml-auto px-4 py-2 text-sm text-gray-600 hover:bg-gray-50 rounded-lg"
                >
                  {showContext ? 'Hide' : 'Show'} Context
                </button>
              </div>
            </div>

            {/* Chat Area */}
            <div className="flex-1 overflow-y-auto p-6 space-y-6">
              {messages.map((message, idx) => (
                <div key={idx} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-2xl ${message.role === 'user' ? 'bg-purple-500 text-white' : 'bg-gray-100 text-gray-900'} rounded-2xl px-6 py-4`}>
                    <div className="text-sm leading-relaxed">{message.content}</div>
                    {message.citations && message.citations.length > 0 && (
                      <div className="mt-3 pt-3 border-t border-gray-200 space-y-1">
                        {message.citations.map((citation: any, cidx: number) => (
                          <div key={cidx} className="text-xs text-gray-600 flex items-center space-x-2">
                            <span>📎</span>
                            <span>{citation.file} (p.{citation.page})</span>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ))}
              
              {isThinking && (
                <div className="flex justify-start">
                  <div className="bg-gray-100 rounded-2xl px-6 py-4">
                    <div className="flex items-center space-x-2 text-gray-500">
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                      </div>
                      <span className="text-sm">Thinking...</span>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Input Area */}
            <div className="p-6 border-t border-gray-200">
              <div className="flex items-end space-x-3">
                <button className="p-3 text-gray-400 hover:text-gray-600 hover:bg-gray-50 rounded-lg">
                  <span className="text-xl">📎</span>
                </button>
                <textarea
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      handleSend();
                    }
                  }}
                  placeholder="Ask about your documents..."
                  className="flex-1 px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-purple-500"
                  rows={3}
                />
                <button
                  onClick={handleSend}
                  className="px-6 py-3 bg-purple-500 text-white rounded-lg font-medium hover:bg-purple-600 transition-colors"
                >
                  Send
                </button>
              </div>
            </div>
          </div>

          {/* Right Panel - Context/Citations */}
          {showContext && (
            <div className="w-96 bg-gray-50 border-l border-gray-200 overflow-y-auto">
              <div className="p-6">
                <h3 className="font-semibold text-gray-900 mb-4">Retrieved Context</h3>
                
                <div className="space-y-4">
                  <div className="bg-white rounded-lg border border-gray-200 p-4">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium text-gray-900">Q3_Financial_Report.pdf</span>
                      <span className="text-xs text-gray-500">Page 12</span>
                    </div>
                    <div className="text-sm text-gray-600 leading-relaxed">
                      "Revenue growth of 23% YoY driven primarily by expansion in the APAC region. Total revenue reached $4.2B in Q3 2024..."
                    </div>
                    <div className="mt-3 pt-3 border-t border-gray-200">
                      <div className="text-xs text-gray-500">Relevance: 95%</div>
                    </div>
                  </div>

                  <div className="bg-white rounded-lg border border-gray-200 p-4">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium text-gray-900">Q3_Financial_Report.pdf</span>
                      <span className="text-xs text-gray-500">Page 15</span>
                    </div>
                    <div className="text-sm text-gray-600 leading-relaxed">
                      "APAC region contributed 45% of total revenue, marking a significant increase from 32% in the previous quarter..."
                    </div>
                    <div className="mt-3 pt-3 border-t border-gray-200">
                      <div className="text-xs text-gray-500">Relevance: 89%</div>
                    </div>
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
           prompt={"A split-screen UI design for an AI document analysis platform. Left column is a list of PDF files with status icons. Center column is a chat interface with message bubbles; the AI message highlights text citations. Top of center column has a dropdown menu labeled \"Model: Gemini 1.5 Pro\". Right column shows a preview of a PDF document with highlighted text corresponding to the chat. Clean, white and light gray color scheme, modern UI, professional. --ar 16:9"}
         />
       </div>
     </div>
   </div>
 );
}
