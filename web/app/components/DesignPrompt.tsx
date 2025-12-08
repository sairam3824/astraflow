"use client";

import { useState } from "react";

export default function DesignPrompt({ title, prompt }: { title: string; prompt: string }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(prompt);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch (e) {
      console.error("Copy failed", e);
    }
  };

  return (
    <div className="mt-8 bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
        <h3 className="font-semibold text-gray-900">{title}</h3>
        <button
          onClick={handleCopy}
          className={`px-3 py-1.5 text-sm rounded-lg border ${
            copied
              ? "bg-green-50 text-green-700 border-green-200"
              : "bg-gray-50 text-gray-700 border-gray-200 hover:bg-gray-100"
          }`}
          aria-label="Copy prompt to clipboard"
        >
          {copied ? "Copied!" : "Copy"}
        </button>
      </div>
      <div className="p-6">
        <pre className="whitespace-pre-wrap break-words text-sm text-gray-800 font-mono">{prompt}</pre>
      </div>
    </div>
  );
}
