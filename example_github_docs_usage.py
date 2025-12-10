#!/usr/bin/env python3
"""
Example usage of the GitHub Documentation Generator API
"""

import requests
import json

# API endpoint
API_URL = "http://localhost:8087/generate-docs"

# Example 1: Generate docs with all options
def generate_full_docs():
    payload = {
        "repo_url": "https://github.com/octocat/Hello-World",
        "license_type": "MIT",
        "generate_readme": True,
        "project_name": "Hello World",
        "project_description": "My first repository on GitHub!",
        "author_name": "The Octocat",
        "author_email": "octocat@github.com"
    }
    
    print("Generating documentation with full options...")
    response = requests.post(API_URL, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Success! Generated docs for: {data['project_name']}")
        print(f"\nRepository Info:")
        print(f"  Languages: {', '.join(data['repository_info']['languages'])}")
        print(f"  Has Tests: {data['repository_info']['has_tests']}")
        print(f"  License: {data['license_type']}")
        
        # Save README
        with open("generated_README.md", "w") as f:
            f.write(data['readme'])
        print("\n📄 README saved to: generated_README.md")
        
        # Save LICENSE
        with open("generated_LICENSE", "w") as f:
            f.write(data['license'])
        print("📄 LICENSE saved to: generated_LICENSE")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.json())

# Example 2: Generate only license (no README)
def generate_license_only():
    payload = {
        "repo_url": "https://github.com/octocat/Hello-World",
        "license_type": "Apache-2.0",
        "generate_readme": False,
        "author_name": "Your Name"
    }

    
    print("\nGenerating license only...")
    response = requests.post(API_URL, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Generated {data['license_type']} license")
        with open("LICENSE_APACHE", "w") as f:
            f.write(data['license'])
        print("📄 LICENSE saved to: LICENSE_APACHE")
    else:
        print(f"❌ Error: {response.status_code}")

# Example 3: Analyze repository only
def analyze_repository():
    analyze_url = "http://localhost:8087/analyze"
    payload = {
        "repo_url": "https://github.com/octocat/Hello-World"
    }
    
    print("\nAnalyzing repository...")
    response = requests.post(analyze_url, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Analysis complete for: {data['project_name']}")
        print(f"\nRepository Structure:")
        print(data['repository_info']['structure'])
    else:
        print(f"❌ Error: {response.status_code}")

if __name__ == "__main__":
    print("=" * 60)
    print("GitHub Documentation Generator - Example Usage")
    print("=" * 60)
    
    # Run examples
    generate_full_docs()
    print("\n" + "=" * 60)
    generate_license_only()
    print("\n" + "=" * 60)
    analyze_repository()
    print("\n" + "=" * 60)
    print("\n✨ All examples completed!")
