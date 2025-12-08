# AstraFlow UI Design Prompts

Use these prompts with Midjourney, DALL-E, or other AI image generators to create high-fidelity mockups.

## 1. Main Dashboard (Home)

**Prompt:**
```
A high-fidelity UI design of a modern SaaS dashboard named "AstraFlow", light mode, clean white background, soft drop shadows. Left sidebar navigation with icons for "Collections", "Workflows", "Stocks". Main area features rounded widgets: one widget showing "Document Ingestion Status" with a progress bar, another widget showing "Live Kafka Stream" with a mini green line chart, and a widget for "Recent AI Chats". Aesthetic is similar to Linear or Vercel, minimalist, sans-serif typography, pastel accent colors. --ar 16:9 --v 6.0
```

**Key Features:**
- Stats cards showing: Total Documents, Celery Workers, Monthly Cost, Kafka Status
- Recent collections grid with progress bars
- Quick chat input box
- Live stock ticker at bottom
- Purple/pink gradient accents

---

## 2. The Workspace (RAG Chat & Collections)

**Prompt:**
```
A split-screen UI design for an AI document analysis platform. Left column is a list of PDF files with status icons. Center column is a chat interface with message bubbles; the AI message highlights text citations. Top of center column has a dropdown menu labeled "Model: Gemini 1.5 Pro". Right column shows a preview of a PDF document with highlighted text corresponding to the chat. Clean, white and light gray color scheme, modern UI, professional. --ar 16:9
```

**Key Features:**
- Three-column layout
- Left: File manager with upload button
- Center: Chat with model selector
- Right: Context panel with citations
- "Thinking..." animation state
- PDF preview with highlights

---

## 3. Workflow Builder (LangGraph Visualizer)

**Prompt:**
```
A node-based visual workflow editor UI, similar to n8n or LangFlow. White background with a subtle dot grid. Colorful rounded rectangular nodes connected by smooth curved lines. Nodes are labeled "Start", "Vector Search", "LLM Router", "Summarize". A floating properties panel on the right side. Clean, minimal, tech-focused design. --ar 16:9
```

**Key Features:**
- Canvas with dot-grid background
- Draggable nodes (Ingest, Vector Search, Router, LLM)
- Bezier curve connections
- Floating toolbar (Add Node, Test Run, Save JSON)
- Properties panel for node configuration
- Node palette on left

---

## 4. Stock Analysis (Live Kafka Stream)

**Prompt:**
```
A financial fintech dashboard UI, light mode. Large Japanese candlestick chart in the center with moving average lines. Right side panel displays a table of live stock indicators with red and green numbers. Bottom section is a terminal-style log window showing streaming JSON data. Professional, data-heavy but clean layout. --ar 16:9
```

**Key Features:**
- Large candlestick/line chart (70% of screen)
- Technical indicators panel (SMA, RSI, Volatility)
- Real-time updates with color flashes
- Dark console at bottom showing Kafka JSON logs
- Symbol selector dropdown
- Live streaming indicator

---

## 5. Collections Manager

**Prompt:**
```
A modern SaaS collections management interface. Grid layout of colorful cards, each representing a document collection. Cards have colored top borders (purple, blue, green), icons, status badges, and document counts. Top section shows statistics widgets. Clean white background, rounded corners, soft shadows. Similar to Notion or Airtable aesthetic. --ar 16:9
```

**Key Features:**
- Grid of collection cards
- Color-coded by domain
- Status indicators (Indexed/Processing)
- Stats overview at top
- Create new collection modal
- Quick actions per collection

---

## Design System Reference

### Colors
- **Primary Gradient**: `from-purple-500 to-pink-500` (#9333ea → #ec4899)
- **Success**: Green (#10b981)
- **Warning**: Yellow (#f59e0b)
- **Error**: Red (#ef4444)
- **Neutral**: Gray-50 to Gray-900

### Typography
- **Font Family**: System fonts (San Francisco, Segoe UI, Roboto)
- **Headings**: 24-32px, Bold (font-bold)
- **Body**: 14-16px, Regular
- **Small**: 12-14px

### Spacing
- **Cards**: p-6 (24px padding)
- **Gaps**: gap-6 (24px between elements)
- **Rounded**: rounded-xl (12px border radius)

### Shadows
- **Cards**: shadow-sm (subtle)
- **Hover**: shadow-lg (elevated)
- **Modals**: shadow-2xl (prominent)

### Components
- **Buttons**: Rounded-lg, gradient for primary, gray for secondary
- **Inputs**: Gray-50 background, border-gray-200, purple focus ring
- **Status Dots**: w-2 h-2, colored, rounded-full
- **Progress Bars**: h-1.5, rounded-full, colored fill

---

## Additional Prompts for Specific Components

### Sidebar Navigation
```
A modern sidebar navigation component, white background, icons with labels, active state highlighted in purple. Icons for Home, Workspace, Workflows, Stocks, Collections. Minimalist, clean spacing. --ar 9:16
```

### Chat Interface
```
A modern chat interface with message bubbles. User messages on right in purple, AI messages on left in gray. AI message includes citation links below. Clean, spacious, professional. --ar 16:9
```

### Node Editor Canvas
```
A workflow canvas with connected nodes. Dot grid background, colorful rounded nodes with icons, curved purple lines connecting them. Floating toolbar at top. Similar to Figma or Miro. --ar 16:9
```

### Stock Chart
```
A financial candlestick chart with technical indicators. Clean white background, purple accent lines, grid overlay. Professional trading interface aesthetic. --ar 16:9
```

---

## Usage Tips

1. **Midjourney**: Add `--v 6.0` for latest version, `--ar 16:9` for widescreen
2. **DALL-E**: Use detailed descriptions, mention "UI/UX design" explicitly
3. **Stable Diffusion**: Add "trending on Dribbble" for better UI results
4. **Figma**: Use these as reference for actual implementation

## Color Palette (Tailwind)

```css
purple-50:  #faf5ff
purple-500: #9333ea
purple-600: #7e22ce

pink-500:   #ec4899
pink-600:   #db2777

gray-50:    #f9fafb
gray-100:   #f3f4f6
gray-200:   #e5e7eb
gray-500:   #6b7280
gray-900:   #111827

green-500:  #10b981
yellow-500: #f59e0b
red-500:    #ef4444
```
