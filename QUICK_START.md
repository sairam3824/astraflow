# AstraFlow Quick Start

## ✅ Migration Complete!

Your AstraFlow application has been successfully migrated from React/Next.js to pure HTML templates.

## 🚀 Access Your Application

**Main URL**: http://localhost:8080

### Available Pages:

- **Home**: http://localhost:8080/ or http://localhost:8080/index.html
- **Dashboard**: http://localhost:8080/dashboard.html
- **Collections**: http://localhost:8080/collections.html
- **Workspace**: http://localhost:8080/workspace.html
- **Workflows**: http://localhost:8080/workflows.html
- **Stocks**: http://localhost:8080/stocks.html
- **Settings**: http://localhost:8080/settings.html
- **Chat**: http://localhost:8080/chat.html
- **RAG**: http://localhost:8080/rag.html
- **Login**: http://localhost:8080/login.html

## 📝 Important Changes

### Port Change
- **Old**: Port 3002 (Next.js dev server)
- **New**: Port 8080 (FastAPI serving HTML)

### API Endpoints
All API endpoints now use the `/api/` prefix:
- Collections API: `http://localhost:8080/api/collections`
- Chat API: `http://localhost:8080/api/chat/sessions`
- Upload API: `http://localhost:8080/api/collections/{id}/upload`

### What Was Removed
- ❌ `web/` directory (Next.js, React, TypeScript)
- ❌ `node_modules/` (~500MB)
- ❌ Build process
- ❌ Node.js dependency

### What Was Added
- ✅ HTML templates in `templates/` folder
- ✅ Tailwind CSS from CDN
- ✅ Vanilla JavaScript
- ✅ Direct FastAPI serving

## 🎯 Starting the Application

```bash
# Start all services
./start-all.sh

# Stop all services
./stop-all.sh
```

## 🔧 Development

### Editing Pages
1. Edit HTML files in `templates/` folder
2. Refresh browser (no build needed!)
3. Changes are instant

### API Integration
All pages are configured to call the backend API:
```javascript
// Example from collections.html
const response = await fetch('http://localhost:8080/api/collections', {
    headers: { 'Authorization': `Bearer ${token}` }
});
```

## 📊 Services Running

- **API Gateway**: Port 8080 (serves HTML + API)
- **Ingestion Service**: Port 8081
- **Embedding Service**: Port 8082
- **Agent Router**: Port 8083
- **Workflow Runner**: Port 8084
- **Stock Producer**: Port 8085
- **Stock Analysis**: Port 8086
- **GitHub Analysis**: Port 8087

### Docker Services
- **ChromaDB**: Port 8000
- **MinIO**: Port 9000, 9001
- **Redis**: Port 6379
- **Kafka**: Port 9092
- **Prometheus**: Port 9090
- **Grafana**: Port 3000

## 🐛 Troubleshooting

### Can't see the page?
1. Make sure services are running: `./start-all.sh`
2. Check API Gateway is on port 8080: `curl http://localhost:8080/health`
3. Check logs: `tail -f logs/api_gateway.log`

### Internal Server Error?
- The API Gateway might not be running
- Check: `ps aux | grep api_gateway`
- Restart: `./stop-all.sh && ./start-all.sh`

### Port already in use?
```bash
# Kill process on port 8080
lsof -ti:8080 | xargs kill -9

# Restart services
./start-all.sh
```

## 📚 Documentation

- See `MIGRATION_TO_HTML.md` for migration details
- See `README.md` for full documentation
- See `FEATURES.md` for feature list

---

**Status**: ✅ Ready to use!
**Last Updated**: December 8, 2024
