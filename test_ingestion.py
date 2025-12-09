#!/usr/bin/env python3
"""
Simple Python script to test PDF ingestion pipeline
Usage: python test_ingestion.py <pdf_file_path>
"""

import sys
import time
import requests
from pathlib import Path

API_URL = "http://localhost:8080"
EMAIL = "admin@astraflow.com"
PASSWORD = "admin123"

def login():
    """Login and get access token"""
    print("🔐 Logging in...")
    response = requests.post(
        f"{API_URL}/auth/login",
        json={"email": EMAIL, "password": PASSWORD}
    )
    
    if response.status_code == 401:
        print("   User not found, registering...")
        response = requests.post(
            f"{API_URL}/auth/register",
            json={"email": EMAIL, "password": PASSWORD}
        )
    
    response.raise_for_status()
    token = response.json()["access_token"]
    print(f"   ✓ Token: {token[:20]}...")
    return token

def create_collection(token, name="Test Documents"):
    """Create a new collection"""
    print(f"\n📚 Creating collection '{name}'...")
    response = requests.post(
        f"{API_URL}/api/collections",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": name, "domain": "General"}
    )
    response.raise_for_status()
    collection = response.json()
    print(f"   ✓ Collection ID: {collection['id']}")
    return collection["id"]

def upload_pdf(token, collection_id, pdf_path):
    """Upload PDF to collection"""
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    print(f"\n📄 Uploading PDF: {pdf_path.name}")
    
    # Get upload URL
    print("   Getting upload URL...")
    response = requests.post(
        f"{API_URL}/api/collections/{collection_id}/upload",
        headers={"Authorization": f"Bearer {token}"},
        json={"filename": pdf_path.name}
    )
    response.raise_for_status()
    data = response.json()
    upload_url = data["upload_url"]
    object_name = data["object_name"]
    
    # Upload file
    print("   Uploading file to MinIO...")
    with open(pdf_path, "rb") as f:
        response = requests.put(upload_url, data=f)
        response.raise_for_status()
    
    print(f"   ✓ Uploaded: {object_name}")
    return object_name

def trigger_ingestion(token, collection_id, object_name):
    """Trigger document ingestion"""
    print("\n⚙️  Triggering ingestion...")
    response = requests.post(
        f"{API_URL}/api/collections/{collection_id}/ingest",
        headers={"Authorization": f"Bearer {token}"},
        json={"object_name": object_name}
    )
    response.raise_for_status()
    data = response.json()
    print(f"   ✓ Job ID: {data['job_id']}")
    print(f"   ✓ Document ID: {data['document_id']}")
    return data["document_id"]

def wait_for_indexing(token, document_id, max_attempts=30):
    """Wait for document to be indexed"""
    print("\n⏳ Waiting for indexing...")
    
    for attempt in range(max_attempts):
        response = requests.get(
            f"{API_URL}/api/documents/{document_id}/status",
            headers={"Authorization": f"Bearer {token}"}
        )
        response.raise_for_status()
        data = response.json()
        
        status = data["status"]
        chunks = data.get("chunks", 0)
        
        print(f"   Attempt {attempt + 1}/{max_attempts}: {status} ({chunks} chunks)")
        
        if status == "indexed":
            print(f"   ✓ Document indexed successfully! Total chunks: {chunks}")
            return True
        elif status == "failed":
            print("   ✗ Document ingestion failed!")
            return False
        
        time.sleep(2)
    
    print("   ⚠️  Timeout waiting for indexing")
    return False

def query_rag(token, collection_id, query):
    """Query collection with RAG"""
    print(f"\n🔍 Querying: '{query}'")
    response = requests.get(
        f"{API_URL}/api/collections/{collection_id}/search",
        headers={"Authorization": f"Bearer {token}"},
        params={"query": query, "top_k": 3}
    )
    response.raise_for_status()
    data = response.json()
    
    print("\n📝 Answer:")
    print(f"   {data['answer']}")
    
    print("\n📊 Top 3 relevant chunks:")
    for i, result in enumerate(data.get("results", []), 1):
        score = result.get("score", 0)
        text = result.get("text", "")[:100]
        print(f"   {i}. Score: {score:.2f}")
        print(f"      {text}...")
    
    return data

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_ingestion.py <pdf_file_path>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    print("=" * 60)
    print("PDF Ingestion Test")
    print("=" * 60)
    
    try:
        # Login
        token = login()
        
        # Create collection
        collection_id = create_collection(token)
        
        # Upload PDF
        object_name = upload_pdf(token, collection_id, pdf_path)
        
        # Trigger ingestion
        document_id = trigger_ingestion(token, collection_id, object_name)
        
        # Wait for indexing
        success = wait_for_indexing(token, document_id)
        
        if not success:
            print("\n❌ Ingestion failed or timed out")
            sys.exit(1)
        
        # Test RAG query
        query_rag(token, collection_id, "What is this document about?")
        
        print("\n" + "=" * 60)
        print("✅ Test completed successfully!")
        print("=" * 60)
        print(f"\nCollection ID: {collection_id}")
        print(f"Document ID: {document_id}")
        print(f"\nYou can now query this collection:")
        print(f"  Collection URL: {API_URL}/collections")
        print(f"  RAG URL: {API_URL}/rag")
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ API Error: {e}")
        if hasattr(e.response, 'text'):
            print(f"   Response: {e.response.text}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
