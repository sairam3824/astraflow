#!/usr/bin/env python3
"""
Diagnostic script for GitHub Docs Generator
Checks all requirements and configuration
"""

import sys
import os
import subprocess
import importlib.util

def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (Need 3.8+)")
        return False

def check_git():
    """Check if Git is installed"""
    print("\n📦 Checking Git installation...")
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ {result.stdout.strip()}")
            return True
        else:
            print("   ❌ Git not found")
            return False
    except FileNotFoundError:
        print("   ❌ Git not installed")
        print("      Install from: https://git-scm.com/")
        return False

def check_dependencies():
    """Check if required Python packages are installed"""
    print("\n📚 Checking Python dependencies...")
    
    required = [
        'fastapi',
        'uvicorn',
        'pydantic',
        'google.generativeai',
        'git',  # GitPython
        'dotenv',
        'prometheus_client'
    ]
    
    missing = []
    for package in required:
        spec = importlib.util.find_spec(package.replace('.', '/'))
        if spec is None:
            print(f"   ❌ {package} - Not installed")
            missing.append(package)
        else:
            print(f"   ✅ {package}")
    
    if missing:
        print(f"\n   Install missing packages:")
        print(f"   pip install -r requirements.txt")
        return False
    return True

def check_env_file():
    """Check if .env file exists and has required variables"""
    print("\n⚙️  Checking configuration...")
    
    if not os.path.exists('.env'):
        print("   ❌ .env file not found")
        print("      Copy .env.example to .env")
        return False
    
    print("   ✅ .env file exists")
    
    # Check for required variables
    with open('.env', 'r') as f:
        content = f.read()
    
    required_vars = [
        'GITHUB_ANALYSIS_PORT',
        'API_GATEWAY_PORT',
        'GEMINI_API_KEY'
    ]
    
    missing_vars = []
    for var in required_vars:
        if var in content:
            # Get the value
            for line in content.split('\n'):
                if line.startswith(var):
                    value = line.split('=')[1].strip() if '=' in line else ''
                    if value and value != 'your-api-key-here':
                        print(f"   ✅ {var} is set")
                    else:
                        print(f"   ⚠️  {var} is empty or placeholder")
                        if var == 'GEMINI_API_KEY':
                            print(f"      Get key from: https://makersuite.google.com/app/apikey")
                    break
        else:
            print(f"   ❌ {var} not found")
            missing_vars.append(var)
    
    return len(missing_vars) == 0

def check_file_structure():
    """Check if required files exist"""
    print("\n📁 Checking file structure...")
    
    required_files = [
        'services/github_analysis/main.py',
        'services/api_gateway/main.py',
        'templates/github_docs.html',
        'libs/utils/config.py',
        'requirements.txt'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - Missing")
            all_exist = False
    
    return all_exist

def check_ports():
    """Check if required ports are available"""
    print("\n🔌 Checking ports...")
    
    import socket
    
    ports = {
        8080: 'API Gateway',
        8087: 'GitHub Analysis Service'
    }
    
    all_available = True
    for port, service in ports.items():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        
        if result == 0:
            print(f"   ⚠️  Port {port} ({service}) - In use")
            print(f"      Service may already be running")
        else:
            print(f"   ✅ Port {port} ({service}) - Available")
    
    return True  # Not critical if ports are in use

def check_internet():
    """Check internet connectivity"""
    print("\n🌐 Checking internet connection...")
    
    import socket
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        print("   ✅ Internet connection available")
        return True
    except OSError:
        print("   ❌ No internet connection")
        print("      Required for cloning repositories")
        return False

def main():
    print("=" * 60)
    print("GitHub Docs Generator - Diagnostic Tool")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Git Installation", check_git),
        ("Python Dependencies", check_dependencies),
        ("Configuration File", check_env_file),
        ("File Structure", check_file_structure),
        ("Port Availability", check_ports),
        ("Internet Connection", check_internet)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"   ❌ Error during check: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Diagnostic Summary")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    print(f"\nPassed: {passed_count}/{total_count}")
    
    if passed_count == total_count:
        print("\n🎉 All checks passed! You're ready to start the service.")
        print("\nNext steps:")
        print("  1. Start the service: bash start-github-service.sh")
        print("  2. Test it: python test_github_service.py")
        print("  3. Open browser: http://localhost:8080/github-docs")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  • Install dependencies: pip install -r requirements.txt")
        print("  • Install Git: https://git-scm.com/")
        print("  • Configure .env: Copy .env.example to .env")
        print("  • Get Gemini API key: https://makersuite.google.com/app/apikey")
    
    print("=" * 60)
    
    return 0 if passed_count == total_count else 1

if __name__ == "__main__":
    sys.exit(main())
