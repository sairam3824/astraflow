from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from prometheus_client import make_asgi_app
from typing import Optional, List
from enum import Enum
import os
import tempfile
import shutil
import google.generativeai as genai
from pathlib import Path
from libs.utils.logging import setup_logger
from libs.utils.config import config

logger = setup_logger("github-analysis")
app = FastAPI(title="GitHub Analysis Service")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini API
genai.configure(api_key=config.GEMINI_API_KEY)

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

class LicenseType(str, Enum):
    MIT = "MIT"
    APACHE = "Apache-2.0"
    GPL_3 = "GPL-3.0"
    BSD_3 = "BSD-3-Clause"
    UNLICENSE = "Unlicense"

class GenerateDocsRequest(BaseModel):
    repo_url: str
    license_type: LicenseType
    generate_readme: bool = True
    project_name: Optional[str] = None
    project_description: Optional[str] = None
    author_name: Optional[str] = None
    author_email: Optional[str] = None

class AnalyzeRequest(BaseModel):
    repo_url: str

def clone_repository(repo_url: str, target_dir: str) -> bool:
    """Clone a GitHub repository to a temporary directory"""
    try:
        import git
        git.Repo.clone_from(repo_url, target_dir, depth=1)
        logger.info(f"Successfully cloned repository: {repo_url}")
        return True
    except Exception as e:
        logger.error(f"Failed to clone repository: {e}")
        return False

def analyze_repository_structure(repo_path: str) -> dict:
    """Analyze repository structure and extract key information"""
    repo_info = {
        "languages": [],
        "frameworks": [],
        "files": [],
        "has_tests": False,
        "has_docs": False,
        "structure": ""
    }
    
    try:
        path = Path(repo_path)
        
        # Detect languages and frameworks
        if (path / "package.json").exists():
            repo_info["languages"].append("JavaScript/TypeScript")
            repo_info["frameworks"].append("Node.js")
        
        if (path / "requirements.txt").exists() or (path / "setup.py").exists() or (path / "pyproject.toml").exists():
            repo_info["languages"].append("Python")
        
        if (path / "pom.xml").exists() or (path / "build.gradle").exists():
            repo_info["languages"].append("Java")
        
        if (path / "go.mod").exists():
            repo_info["languages"].append("Go")
        
        if (path / "Cargo.toml").exists():
            repo_info["languages"].append("Rust")
        
        # Check for tests
        test_dirs = ["test", "tests", "__tests__", "spec"]
        for test_dir in test_dirs:
            if (path / test_dir).exists():
                repo_info["has_tests"] = True
                break
        
        # Check for documentation
        doc_dirs = ["docs", "documentation", "doc"]
        for doc_dir in doc_dirs:
            if (path / doc_dir).exists():
                repo_info["has_docs"] = True
                break
        
        # Get file structure (limited depth)
        structure_lines = []
        for item in sorted(path.iterdir())[:20]:  # Limit to first 20 items
            if item.name.startswith('.'):
                continue
            if item.is_dir():
                structure_lines.append(f"📁 {item.name}/")
            else:
                structure_lines.append(f"📄 {item.name}")
        
        repo_info["structure"] = "\n".join(structure_lines)
        
    except Exception as e:
        logger.error(f"Error analyzing repository: {e}")
    
    return repo_info

def generate_readme_with_gemini(repo_info: dict, project_name: str, project_description: Optional[str]) -> str:
    """Generate README using Gemini API"""
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""Generate a comprehensive and professional README.md file for a GitHub repository with the following information:

Project Name: {project_name}
{f"Description: {project_description}" if project_description else ""}
Languages: {', '.join(repo_info['languages']) if repo_info['languages'] else 'Not detected'}
Frameworks: {', '.join(repo_info['frameworks']) if repo_info['frameworks'] else 'Not detected'}
Has Tests: {'Yes' if repo_info['has_tests'] else 'No'}
Has Documentation: {'Yes' if repo_info['has_docs'] else 'No'}

Repository Structure:
{repo_info['structure']}

Please create a README.md that includes:
1. Project title and description
2. Features section
3. Installation instructions
4. Usage examples
5. Project structure overview
6. Contributing guidelines
7. License information (mention that license file is included)
8. Contact/Support section

Make it professional, clear, and engaging. Use proper markdown formatting with badges, code blocks, and sections."""

        response = model.generate_content(prompt)
        readme_content = response.text
        
        logger.info("Successfully generated README with Gemini")
        return readme_content
        
    except Exception as e:
        logger.error(f"Error generating README with Gemini: {e}")
        # Fallback to basic README
        return f"""# {project_name}

{project_description or 'A software project'}

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd {project_name}

# Install dependencies
# Add installation commands here
```

## Usage

Add usage instructions here.

## License

See LICENSE file for details.
"""

def get_license_text(license_type: LicenseType, author_name: Optional[str], year: str = "2024") -> str:
    """Get license text based on license type"""
    
    author = author_name or "[Your Name]"
    
    licenses = {
        LicenseType.MIT: f"""MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""",
        
        LicenseType.APACHE: f"""Apache License
Version 2.0, January 2004
http://www.apache.org/licenses/

Copyright {year} {author}

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
""",
        
        LicenseType.GPL_3: f"""GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Copyright (C) {year} {author}

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
""",
        
        LicenseType.BSD_3: f"""BSD 3-Clause License

Copyright (c) {year}, {author}

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
""",
        
        LicenseType.UNLICENSE: f"""This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org>
"""
    }
    
    return licenses.get(license_type, licenses[LicenseType.MIT])

@app.post("/generate-docs")
async def generate_documentation(req: GenerateDocsRequest):
    """Generate README and LICENSE files for a GitHub repository"""
    temp_dir = None
    
    try:
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        logger.info(f"Created temporary directory: {temp_dir}")
        
        # Clone repository
        if not clone_repository(req.repo_url, temp_dir):
            raise HTTPException(status_code=400, detail="Failed to clone repository")
        
        # Analyze repository
        repo_info = analyze_repository_structure(temp_dir)
        
        # Extract project name from repo URL
        project_name = req.project_name or req.repo_url.split('/')[-1].replace('.git', '')
        
        # Generate README if requested
        readme_content = None
        if req.generate_readme:
            readme_content = generate_readme_with_gemini(
                repo_info, 
                project_name, 
                req.project_description
            )
        
        # Generate LICENSE
        from datetime import datetime
        current_year = datetime.now().year
        license_content = get_license_text(
            req.license_type, 
            req.author_name, 
            str(current_year)
        )
        
        logger.info(f"Successfully generated documentation for {project_name}")
        
        return {
            "status": "success",
            "project_name": project_name,
            "readme": readme_content,
            "license": license_content,
            "license_type": req.license_type,
            "repository_info": repo_info
        }
        
    except Exception as e:
        logger.error(f"Error generating documentation: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Cleanup temporary directory
        if temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
                logger.info(f"Cleaned up temporary directory: {temp_dir}")
            except Exception as e:
                logger.error(f"Failed to cleanup temporary directory: {e}")

@app.post("/analyze")
async def analyze_repository(req: AnalyzeRequest):
    """Analyze a repository without generating documentation"""
    temp_dir = None
    
    try:
        temp_dir = tempfile.mkdtemp()
        
        if not clone_repository(req.repo_url, temp_dir):
            raise HTTPException(status_code=400, detail="Failed to clone repository")
        
        repo_info = analyze_repository_structure(temp_dir)
        project_name = req.repo_url.split('/')[-1].replace('.git', '')
        
        logger.info(f"Successfully analyzed repository: {project_name}")
        
        return {
            "status": "success",
            "project_name": project_name,
            "repository_info": repo_info
        }
        
    except Exception as e:
        logger.error(f"Error analyzing repository: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
            except Exception as e:
                logger.error(f"Failed to cleanup: {e}")

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config.GITHUB_ANALYSIS_PORT)
