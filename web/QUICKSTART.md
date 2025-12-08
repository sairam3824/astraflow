# AstraFlow Web UI - Quick Start Guide

## 🚀 Installation & Setup

### Prerequisites
- Node.js 18+ and npm
- AstraFlow backend running on `http://localhost:8000`

### Install Dependencies
```bash
cd web
npm install
```

### Development Mode
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Production Build
```bash
npm run build
npm start
```

---

## 📱 Page Navigation

### 1. Dashboard (Home) - `http://localhost:3000/`
**Your mission control center**

What you'll see:
- ✅ System health stats (Documents, Workers, Cost, Kafka)
- 📚 Recent collections with indexing progress
- 💬 Quick chat for cross-collection queries
- 📈 Live stock ticker from Kafka stream

Try this:
1. Check system status in the stats cards
2. Click on a collection to view details
3. Use the quick chat to ask questions
4. Watch the live stock ticker update

---

### 2. Workspace - `http://localhost:3000/workspace`
**RAG chat interface for document Q&A**

What you'll see:
- 📁 Left: Your document collection
- 💬 Center: Chat interface with AI
- 📄 Right: Context/citations panel

Try this:
1. Select a model from the dropdown (Auto-Router, GPT-4, Gemini, Claude)
2. Type a question about your documents
3. Watch the "Thinking..." animation
4. See citations appear in the right panel
5. Click "Show/Hide Context" to toggle the citations panel

---

### 3. Workflows - `http://localhost:3000/workflows`
**Visual LangGraph workflow builder**

What you'll see:
- 🎨 Canvas with dot-grid background
- 🔵 Nodes connected by curved lines
- 🛠️ Floating toolbar at top
- ⚙️ Properties panel on right

Try this:
1. Click on any node to see its properties
2. Use the floating toolbar to add new nodes
3. Click "Test Run" to execute the workflow
4. Click "Save JSON" to export the workflow
5. Drag nodes to rearrange (coming soon)

Node types available:
- ▶️ Start - Entry point
- 🔍 Vector Search - Retrieve from vector DB
- 🔀 Router - Conditional branching
- 🤖 LLM - AI model execution
- 🔧 Tool - External tool call
- ✅ End - Exit point

---

### 4. Stocks - `http://localhost:3000/stocks`
**Live Kafka stream visualization**

What you'll see:
- 📊 Large candlestick/line chart
- 📈 Technical indicators (SMA, RSI, Volatility)
- 💻 Kafka console with streaming JSON
- 🔴 Live streaming indicator

Try this:
1. Select a stock symbol from the dropdown
2. Watch the chart update in real-time
3. Check technical indicators on the right
4. Scroll through the Kafka console at bottom
5. Switch time ranges (1D, 1W, 1M, 1Y)

Indicators explained:
- **SMA (20)**: 20-day Simple Moving Average
- **RSI**: Relative Strength Index (0-100)
- **Volatility**: Price volatility percentage
- **Volume**: Trading volume

---

### 5. Collections - `http://localhost:3000/collections`
**Manage your document collections**

What you'll see:
- 📊 Stats overview at top
- 🎴 Grid of collection cards
- ➕ Create new collection button

Try this:
1. Click "Create Collection" to add a new one
2. Fill in name, domain, and description
3. Click on a collection card to open it
4. Use the 💬 icon to start chatting
5. Use the ⚙️ icon to configure settings

Collection statuses:
- 🟢 **Indexed**: Ready to use
- 🟡 **Processing**: Currently indexing

---

### 6. Settings - `http://localhost:3000/settings`
**Configure your AstraFlow instance**

Tabs available:
- ⚙️ **General**: Profile and preferences
- 🤖 **AI Models**: API keys and model settings
- 🔌 **Integrations**: Connected services
- 💳 **Billing**: Usage and costs

Try this:
1. Add your API keys in the "AI Models" tab
2. Configure your default model
3. Check integration status
4. Review your usage in "Billing"

---

## 🎨 UI Features

### Design System
- **Colors**: Purple/pink gradients for primary actions
- **Typography**: System fonts, clean and readable
- **Spacing**: Consistent 24px gaps between elements
- **Shadows**: Subtle elevation for depth

### Interactive Elements
- **Hover Effects**: Cards lift on hover
- **Loading States**: Animated dots for "Thinking..."
- **Status Indicators**: Colored dots (🟢 green, 🟡 yellow, 🔴 red)
- **Smooth Transitions**: All state changes are animated

### Responsive Design
- **Desktop**: Full three-column layouts
- **Tablet**: Two-column with collapsible panels
- **Mobile**: Single column with bottom nav (coming soon)

---

## 🔌 API Integration

The UI connects to your AstraFlow backend:

```typescript
// Base URL
const API_BASE = 'http://localhost:8000';

// Endpoints used
GET  /health              // System health
GET  /collections         // List collections
POST /collections         // Create collection
POST /chat                // Send chat message
GET  /workflows           // List workflows
WS   /stocks              // WebSocket for stocks
```

### Customizing API URL

Edit `web/app/page.tsx` and other pages to change the API URL:

```typescript
// Change this line in each page
fetch('http://localhost:8000/collections')
// To your backend URL
fetch('https://your-backend.com/collections')
```

Or create an environment variable:

```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Then use it:
```typescript
fetch(`${process.env.NEXT_PUBLIC_API_URL}/collections`)
```

---

## 🐛 Troubleshooting

### Build fails
```bash
rm -rf .next node_modules
npm install
npm run build
```

### Port 3000 already in use
```bash
# Use a different port
PORT=3001 npm run dev
```

### API connection fails
1. Check backend is running: `curl http://localhost:8000/health`
2. Check CORS settings in backend
3. Open browser console for error details

### Styles not loading
```bash
# Rebuild Tailwind
npm run build
```

---

## 📚 Next Steps

1. **Customize**: Edit components in `web/app/components/`
2. **Add Pages**: Create new folders in `web/app/`
3. **Styling**: Modify `web/app/globals.css` or Tailwind config
4. **API**: Update fetch calls to match your backend
5. **Deploy**: Use Vercel, Netlify, or Docker

---

## 🎯 Common Tasks

### Add a new page
```bash
# Create new folder and page
mkdir web/app/mypage
touch web/app/mypage/page.tsx
```

```typescript
// web/app/mypage/page.tsx
'use client';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';

export default function MyPage() {
  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        <main className="flex-1 overflow-y-auto p-8">
          <h1>My New Page</h1>
        </main>
      </div>
    </div>
  );
}
```

### Add to navigation
Edit `web/app/components/Sidebar.tsx`:

```typescript
const navItems = [
  // ... existing items
  { href: '/mypage', icon: '🎯', label: 'My Page' },
];
```

### Change colors
Edit `web/tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      primary: '#your-color',
    }
  }
}
```

---

## 📖 Documentation

- [Next.js Docs](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Recharts](https://recharts.org/)
- [TypeScript](https://www.typescriptlang.org/docs)

---

## 🎉 You're Ready!

Your AstraFlow UI is now running. Start exploring the pages and building your AI-powered workflows!

Need help? Check the main README or open an issue on GitHub.
