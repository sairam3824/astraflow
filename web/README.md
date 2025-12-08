# AstraFlow Web UI

Modern, production-ready UI for the AstraFlow AI platform built with Next.js 14, TypeScript, and Tailwind CSS.

## 🎨 Pages Overview

### 1. Dashboard (Home) - `/`
**Mission Control view showing system health and overview**

Features:
- Real-time system stats (Documents, Celery Workers, API Cost, Kafka Status)
- Recent collections with indexing progress
- Quick chat interface for cross-collection queries
- Live stock market ticker from Kafka stream
- Quick action cards for common tasks

Design: Clean, card-based layout with soft shadows, similar to Linear/Vercel aesthetic

### 2. Workspace - `/workspace`
**Core RAG chat interface for document analysis**

Features:
- Left Panel: Collection file manager with upload capability
- Center Panel: Chat interface with model selector (Auto-Router, GPT-4, Gemini, Claude)
- Right Panel: Context/Citations showing retrieved chunks with relevance scores
- Real-time "Thinking..." state during LangGraph execution
- PDF preview with highlighted citations

Design: Three-column layout optimized for document Q&A workflow

### 3. Workflows - `/workflows`
**Visual LangGraph workflow builder**

Features:
- Canvas with dot-grid background for node placement
- Drag-and-drop node system (Start, Vector Search, Router, LLM, Tool, End)
- Bezier curve connections between nodes
- Properties panel for node configuration
- Floating toolbar (Add Node, Test Run, Save JSON)
- Node palette with available node types

Design: Node-based visual editor similar to n8n/LangFlow

### 4. Stocks - `/stocks`
**Live Kafka stream visualization for market data**

Features:
- Large candlestick/line chart with real-time updates
- Technical indicators panel (SMA, RSI, Volatility, Volume)
- Kafka console showing raw JSON stream
- Symbol selector for different stocks
- AI-powered analysis insights
- Color-coded indicators with animations

Design: Financial dashboard with dark console for streaming data

### 5. Collections - `/collections`
**Manage document collections and knowledge bases**

Features:
- Grid view of all collections with status indicators
- Stats overview (Total Collections, Documents, Indexed, Processing)
- Create new collection modal
- Collection cards with domain categorization
- Quick actions (Chat, Settings) per collection

Design: Card-based grid layout with color-coded collections

## 🚀 Getting Started

```bash
cd web
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

## 🛠️ Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **HTTP Client**: Axios

## 📁 Project Structure

```
web/
├── app/
│   ├── components/
│   │   ├── Sidebar.tsx       # Global navigation
│   │   └── Header.tsx        # Search & notifications
│   ├── page.tsx              # Dashboard (Home)
│   ├── workspace/
│   │   └── page.tsx          # RAG Chat Interface
│   ├── workflows/
│   │   └── page.tsx          # Workflow Builder
│   ├── stocks/
│   │   └── page.tsx          # Stock Analysis
│   ├── collections/
│   │   └── page.tsx          # Collections Manager
│   ├── layout.tsx            # Root layout
│   └── globals.css           # Global styles
├── public/                   # Static assets
└── package.json
```

## 🎨 Design System

### Colors
- **Primary**: Purple (#9333ea) to Pink (#ec4899) gradient
- **Success**: Green (#10b981)
- **Warning**: Yellow (#f59e0b)
- **Error**: Red (#ef4444)
- **Neutral**: Gray scale

### Typography
- **Font**: System fonts (San Francisco, Segoe UI, Roboto)
- **Headings**: Bold, 24-32px
- **Body**: Regular, 14-16px
- **Small**: 12-14px

### Components
- **Cards**: White background, rounded-xl, subtle shadow
- **Buttons**: Rounded-lg, gradient for primary actions
- **Inputs**: Gray-50 background, rounded-lg, purple focus ring
- **Status Indicators**: Colored dots with labels

## 🔌 API Integration

The UI connects to the AstraFlow backend at `http://localhost:8000`:

- `GET /health` - System health stats
- `GET /collections` - List collections
- `POST /collections` - Create collection
- `POST /chat` - Send chat message
- `GET /workflows` - List workflows
- `WS /stocks` - WebSocket for live stock data

## 📱 Responsive Design

All pages are fully responsive:
- **Desktop**: Full three-column layouts
- **Tablet**: Two-column layouts with collapsible sidebars
- **Mobile**: Single column with bottom navigation

## 🎯 Key Features

1. **Real-time Updates**: Live Kafka stream, WebSocket connections
2. **Smooth Animations**: Tailwind transitions, loading states
3. **Accessibility**: Semantic HTML, ARIA labels, keyboard navigation
4. **Performance**: Next.js optimizations, lazy loading, code splitting
5. **Type Safety**: Full TypeScript coverage

## 🔮 Future Enhancements

- [ ] Dark mode support
- [ ] User authentication UI
- [ ] Advanced workflow templates
- [ ] Export/import functionality
- [ ] Collaborative features
- [ ] Mobile app (React Native)

## 📄 License

Part of the AstraFlow project
