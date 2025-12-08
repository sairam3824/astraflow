# AstraFlow Component Library

Reusable components and patterns used throughout the AstraFlow UI.

## 🧩 Core Components

### Sidebar
**Location**: `web/app/components/Sidebar.tsx`

Global navigation component with active state highlighting.

```typescript
import Sidebar from './components/Sidebar';

<Sidebar />
```

Features:
- Active route highlighting (purple background)
- Icon + label navigation items
- Responsive collapse (coming soon)

---

### Header
**Location**: `web/app/components/Header.tsx`

Top header with search and notifications.

```typescript
import Header from './components/Header';

<Header />
```

Features:
- Global search input
- Notification bell with badge
- User profile dropdown

---

## 🎨 Design Patterns

### Page Layout
Standard three-section layout used across all pages:

```typescript
<div className="flex h-screen bg-gray-50">
  <Sidebar />
  
  <div className="flex-1 flex flex-col overflow-hidden">
    <Header />
    
    <main className="flex-1 overflow-y-auto">
      <div className="p-8">
        {/* Your content */}
      </div>
    </main>
  </div>
</div>
```

---

### Stats Card
Display key metrics with icons and badges:

```typescript
<div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
  <div className="flex items-center justify-between mb-2">
    <span className="text-2xl">📄</span>
    <span className="text-xs font-medium text-green-600 bg-green-50 px-2 py-1 rounded">
      +12%
    </span>
  </div>
  <div className="text-2xl font-bold text-gray-900">1,234</div>
  <div className="text-sm text-gray-500">Total Documents</div>
</div>
```

---

### Status Indicator
Show live status with colored dots:

```typescript
{/* Active/Connected */}
<span className="flex items-center text-sm text-green-600 bg-green-50 px-3 py-2 rounded-lg">
  <span className="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></span>
  Live
</span>

{/* Processing */}
<span className="flex items-center text-xs text-yellow-600 bg-yellow-50 px-2 py-1 rounded">
  <span className="w-1.5 h-1.5 bg-yellow-500 rounded-full mr-1 animate-pulse"></span>
  Processing
</span>

{/* Indexed/Complete */}
<span className="flex items-center text-xs text-green-600">
  <span className="w-1.5 h-1.5 bg-green-500 rounded-full mr-1"></span>
  Indexed
</span>
```

---

### Progress Bar
Visual progress indicator:

```typescript
<div className="w-full h-1.5 bg-gray-200 rounded-full overflow-hidden">
  <div 
    className="h-full bg-green-500 rounded-full transition-all"
    style={{ width: '65%' }}
  ></div>
</div>
```

With label:
```typescript
<div className="flex items-center justify-between text-xs text-gray-500 mb-1">
  <span>Indexing: 65%</span>
</div>
<div className="w-full h-1.5 bg-gray-200 rounded-full overflow-hidden">
  <div className="h-full bg-green-500 rounded-full" style={{ width: '65%' }}></div>
</div>
```

---

### Button Variants

**Primary (Gradient)**
```typescript
<button className="px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg font-medium hover:from-purple-600 hover:to-pink-600">
  Primary Action
</button>
```

**Secondary**
```typescript
<button className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200">
  Secondary Action
</button>
```

**Outline**
```typescript
<button className="px-4 py-2 border border-gray-200 text-gray-700 rounded-lg hover:bg-gray-50">
  Outline Button
</button>
```

**Danger**
```typescript
<button className="px-4 py-2 bg-red-50 text-red-600 rounded-lg hover:bg-red-100">
  Delete
</button>
```

---

### Input Fields

**Text Input**
```typescript
<input
  type="text"
  placeholder="Enter text..."
  className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
/>
```

**Textarea**
```typescript
<textarea
  placeholder="Enter description..."
  className="w-full px-4 py-3 border border-gray-200 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-purple-500"
  rows={3}
/>
```

**Select Dropdown**
```typescript
<select className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500">
  <option>Option 1</option>
  <option>Option 2</option>
</select>
```

**Search Input**
```typescript
<div className="relative">
  <input
    type="text"
    placeholder="Search..."
    className="w-full px-4 py-2 pl-10 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
  />
  <span className="absolute left-3 top-2.5 text-gray-400">🔍</span>
</div>
```

---

### Card Layouts

**Basic Card**
```typescript
<div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
  <h2 className="text-lg font-semibold text-gray-900 mb-4">Card Title</h2>
  <p className="text-gray-600">Card content goes here</p>
</div>
```

**Hoverable Card**
```typescript
<div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-lg hover:border-purple-300 transition-all cursor-pointer">
  {/* Content */}
</div>
```

**Gradient Card**
```typescript
<div className="bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl shadow-sm p-6 text-white">
  <h2 className="text-lg font-semibold mb-3">Gradient Card</h2>
  <p className="text-sm opacity-90">White text on gradient</p>
</div>
```

---

### Modal/Dialog

```typescript
{showModal && (
  <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
    <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md p-8">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Modal Title</h2>
        <button
          onClick={() => setShowModal(false)}
          className="text-gray-400 hover:text-gray-600"
        >
          ✕
        </button>
      </div>

      <div className="space-y-4">
        {/* Modal content */}
      </div>

      <div className="flex space-x-3 pt-4">
        <button
          onClick={() => setShowModal(false)}
          className="flex-1 px-4 py-3 border border-gray-200 text-gray-700 rounded-lg hover:bg-gray-50"
        >
          Cancel
        </button>
        <button className="flex-1 px-4 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg hover:from-purple-600 hover:to-pink-600">
          Confirm
        </button>
      </div>
    </div>
  </div>
)}
```

---

### Chat Bubble

**User Message**
```typescript
<div className="flex justify-end">
  <div className="max-w-2xl bg-purple-500 text-white rounded-2xl px-6 py-4">
    <div className="text-sm leading-relaxed">User message here</div>
  </div>
</div>
```

**AI Message**
```typescript
<div className="flex justify-start">
  <div className="max-w-2xl bg-gray-100 text-gray-900 rounded-2xl px-6 py-4">
    <div className="text-sm leading-relaxed">AI response here</div>
  </div>
</div>
```

**Thinking State**
```typescript
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
```

---

### Toggle Switch

```typescript
{/* Off State */}
<button className="w-12 h-6 bg-gray-200 rounded-full relative">
  <div className="w-5 h-5 bg-white rounded-full absolute left-0.5 top-0.5"></div>
</button>

{/* On State */}
<button className="w-12 h-6 bg-purple-500 rounded-full relative">
  <div className="w-5 h-5 bg-white rounded-full absolute right-0.5 top-0.5"></div>
</button>
```

---

### Tab Navigation

```typescript
const [activeTab, setActiveTab] = useState('general');

const tabs = [
  { id: 'general', label: 'General', icon: '⚙️' },
  { id: 'advanced', label: 'Advanced', icon: '🔧' }
];

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
```

---

### Grid Layouts

**2-Column**
```typescript
<div className="grid grid-cols-1 md:grid-cols-2 gap-6">
  {/* Items */}
</div>
```

**3-Column**
```typescript
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {/* Items */}
</div>
```

**4-Column**
```typescript
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
  {/* Items */}
</div>
```

---

## 🎨 Color Utilities

### Background Colors
```typescript
bg-white          // White
bg-gray-50        // Light gray
bg-gray-100       // Lighter gray
bg-purple-50      // Light purple
bg-gradient-to-r from-purple-500 to-pink-500  // Gradient
```

### Text Colors
```typescript
text-gray-900     // Dark text
text-gray-600     // Medium text
text-gray-500     // Light text
text-purple-600   // Purple text
text-green-600    // Success
text-red-600      // Error
text-yellow-600   // Warning
```

### Border Colors
```typescript
border-gray-200   // Default border
border-purple-300 // Hover border
border-green-500  // Success border
```

---

## 📐 Spacing Scale

```typescript
p-2   // 8px padding
p-4   // 16px padding
p-6   // 24px padding (most common)
p-8   // 32px padding

gap-2 // 8px gap
gap-4 // 16px gap
gap-6 // 24px gap (most common)

space-x-3  // 12px horizontal spacing
space-y-4  // 16px vertical spacing
```

---

## 🔤 Typography Scale

```typescript
text-xs    // 12px
text-sm    // 14px
text-base  // 16px (default)
text-lg    // 18px
text-xl    // 20px
text-2xl   // 24px
text-3xl   // 30px

font-medium   // 500 weight
font-semibold // 600 weight
font-bold     // 700 weight
```

---

## 🎭 Animation Classes

```typescript
transition-all        // Smooth transitions
hover:shadow-lg       // Lift on hover
animate-pulse         // Pulsing animation
animate-bounce        // Bouncing animation
```

---

## 💡 Best Practices

1. **Consistency**: Use the same patterns across pages
2. **Spacing**: Stick to the 24px (gap-6) grid
3. **Colors**: Use purple/pink for primary actions
4. **Shadows**: Keep them subtle (shadow-sm)
5. **Rounded**: Use rounded-xl for cards, rounded-lg for buttons
6. **Focus**: Always include focus:ring-2 on inputs
7. **Hover**: Add hover states to interactive elements
8. **Loading**: Show loading states for async operations
9. **Responsive**: Test on mobile, tablet, desktop
10. **Accessibility**: Use semantic HTML and ARIA labels

---

## 🔧 Customization

To customize these components:

1. **Colors**: Edit `tailwind.config.js`
2. **Spacing**: Modify Tailwind theme
3. **Fonts**: Update `globals.css`
4. **Components**: Create new files in `components/`

---

## 📚 Resources

- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Heroicons](https://heroicons.com/) - Icon library
- [Headless UI](https://headlessui.com/) - Unstyled components
- [Radix UI](https://www.radix-ui.com/) - Accessible components
