#!/usr/bin/env python3
"""
Script to add logout button to all templates
"""
from pathlib import Path
import re

templates = [
    "templates/collections.html",
    "templates/index.html", 
    "templates/settings.html",
    "templates/stocks.html",
    "templates/workflows.html",
    "templates/workspace.html",
    "templates/rag.html"
]

# Pattern to find Settings button
settings_pattern = r'(<a href="/settings"[^>]*>[\s\S]*?</a>)'

# Replacement with logout button
logout_button = '''                <button onclick="logout()" class="w-full flex items-center space-x-2 px-3 py-2 rounded-lg text-red-600 hover:bg-red-50 text-sm">
                    <span>🚪</span>
                    <span>Logout</span>
                </button>'''

# Logout function to add to scripts
logout_function = '''        // Logout function
        function logout() {
            if (confirm('Are you sure you want to logout?')) {
                localStorage.removeItem('token');
                window.location.href = '/login';
            }
        }

'''

for template_path in templates:
    path = Path(template_path)
    if not path.exists():
        print(f"⚠️  Skipping {template_path} (not found)")
        continue
    
    content = path.read_text()
    
    # Check if logout already exists
    if 'onclick="logout()"' in content:
        print(f"✓ {template_path} already has logout button")
        continue
    
    # Add logout button after Settings
    if 'href="/settings"' in content:
        # Make Settings link have mb-2 class
        content = re.sub(
            r'(<a href="/settings"[^>]*class="[^"]*?)(")',
            r'\1 mb-2\2',
            content
        )
        
        # Add logout button after Settings closing tag
        content = re.sub(
            r'(</a>\s*)(</div>\s*</aside>)',
            r'\1' + logout_button + '\n            \2',
            content
        )
        
        # Add logout function to script if not present
        if 'function logout()' not in content:
            content = re.sub(
                r'(<script>\s*)',
                r'\1' + logout_function,
                content
            )
        
        path.write_text(content)
        print(f"✓ Added logout to {template_path}")
    else:
        print(f"⚠️  No Settings button found in {template_path}")

print("\n✓ Done!")
