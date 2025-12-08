# AstraFlow HTML Templates

This folder contains the HTML templates for the AstraFlow web interface.

## Pages

- **index.html** - Dashboard home page
- **login.html** - Login and registration page
- **collections.html** - Collection management page
- **rag.html** - RAG search interface

## Features

### Dashboard (index.html)
- Overview of collections and activity
- Quick action buttons
- Statistics display

### Collections (collections.html)
- Create new collections
- Upload PDF documents
- Delete collections
- View collection details

### RAG Search (rag.html)
- Select collection to search
- Semantic search with AI-generated answers
- View source documents with relevance scores
- Adjustable search parameters (top_k)

## API Endpoints Used

All templates connect to the API Gateway at `http://localhost:8000`:

- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /collections` - List collections
- `POST /collections` - Create collection
- `DELETE /collections/{id}` - Delete collection
- `POST /collections/{id}/upload` - Get upload URL
- `POST /collections/{id}/ingest` - Trigger document processing
- `GET /collections/{id}/search` - RAG search

## Usage

1. Start the API Gateway: `python -m services.api_gateway.main`
2. Navigate to `http://localhost:8000`
3. Register/login
4. Create collections and upload documents
5. Use RAG search to query your documents

## Styling

All templates use Tailwind CSS via CDN for styling.
