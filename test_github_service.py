#!/usr/bin/env python3
"""
Test script for GitHub Documentation Generator
"""

import requests
import json
import sys
import time

def test_health():
    """Test if the service is running"""
    print("🔍 Testing service health...")
    try:
        response = requests.get("http://localhost:8087/health", timeout=5)
        if response.status_code == 200:
            print("✅ Service is healthy!")
            return True
        else:
            print(f"❌ Service returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to service. Is it running?")
        print("   Start it with: bash start-github-service.sh")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_generate_docs():
    """Test documentation generation"""
    print("\n📝 Testing documentation generation...")
    print("   Using repository: https://github.com/octocat/Hello-World")
    
    payload = {
        "repo_url": "https://github.com/octocat/Hello-World",
        "license_type": "MIT",
        "generate_readme": True,
        "project_name": "Hello World Test",
        "project_description": "A test repository",
        "author_name": "Test User"
    }
    
    try:
        print("   Sending request...")
        response = requests.post(
            "http://localhost:8087/generate-docs",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Documentation generated successfully!")
            print(f"\n📊 Results:")
            print(f"   Project: {data['project_name']}")
            print(f"   License: {data['license_type']}")
            print(f"   Languages: {', '.join(data['repository_info']['languages'])}")
            print(f"   Has Tests: {data['repository_info']['has_tests']}")
            print(f"   README Length: {len(data['readme']) if data['readme'] else 0} characters")
            print(f"   LICENSE Length: {len(data['license'])} characters")
            return True
        else:
            print(f"❌ Request failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out. Repository cloning may take longer.")
        print("   Try with a smaller repository or increase timeout.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_api_gateway():
    """Test if API Gateway is running"""
    print("\n🌐 Testing API Gateway...")
    try:
        response = requests.get("http://localhost:8080/health", timeout=5)
        if response.status_code == 200:
            print("✅ API Gateway is healthy!")
            return True
        else:
            print(f"⚠️  API Gateway returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("⚠️  API Gateway is not running")
        print("   Start it with: cd services/api_gateway && python main.py")
        return False
    except Exception as e:
        print(f"⚠️  Error: {e}")
        return False

def test_web_interface():
    """Test if web interface is accessible"""
    print("\n🖥️  Testing web interface...")
    try:
        response = requests.get("http://localhost:8080/github-docs", timeout=5)
        if response.status_code == 200:
            print("✅ Web interface is accessible!")
            print("   Open in browser: http://localhost:8080/github-docs")
            return True
        else:
            print(f"⚠️  Web interface returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("⚠️  Cannot access web interface")
        return False
    except Exception as e:
        print(f"⚠️  Error: {e}")
        return False

def main():
    print("=" * 60)
    print("GitHub Documentation Generator - Test Suite")
    print("=" * 60)
    
    results = []
    
    # Test 1: Service Health
    results.append(("Service Health", test_health()))
    
    if not results[0][1]:
        print("\n❌ Service is not running. Please start it first.")
        print("\nTo start the service:")
        print("  Windows: start-github-service.bat")
        print("  Linux/Mac: bash start-github-service.sh")
        sys.exit(1)
    
    # Test 2: Documentation Generation
    time.sleep(1)
    results.append(("Documentation Generation", test_generate_docs()))
    
    # Test 3: API Gateway
    time.sleep(1)
    results.append(("API Gateway", test_api_gateway()))
    
    # Test 4: Web Interface
    time.sleep(1)
    results.append(("Web Interface", test_web_interface()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    print(f"\nPassed: {passed_count}/{total_count}")
    
    if passed_count == total_count:
        print("\n🎉 All tests passed! The service is working correctly.")
        print("\n🚀 You can now use the GitHub Docs Generator at:")
        print("   http://localhost:8080/github-docs")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
