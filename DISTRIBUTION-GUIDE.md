# GTM Labs MCP - Distribution Guide

How to make your MCP server publicly available for others to use.

---

## 🎯 Goal

Allow anyone to install and use the GTM Labs MCP server with a single command:

```bash
npx @modelcontextprotocol/create-server gtm-labs
# or
pip install gtm-labs-mcp
```

---

## 📦 Distribution Options

### Option 1: NPM Package (Recommended for MCP)

Most MCP servers are distributed via NPM for easy installation.

#### Steps:

1. **Create Package Structure**

```bash
gtm-labs-mcp/
├── package.json
├── README.md
├── LICENSE
├── src/
│   └── index.py (or index.js/ts)
└── bin/
    └── gtm-labs-mcp
```

2. **Create `package.json`**

```json
{
  "name": "@gtm-labs/mcp-server",
  "version": "1.0.0",
  "description": "GTM Labs component library MCP server",
  "main": "src/index.py",
  "bin": {
    "gtm-labs-mcp": "./bin/gtm-labs-mcp"
  },
  "scripts": {
    "start": "python3 src/index.py"
  },
  "keywords": ["mcp", "model-context-protocol", "components", "nextjs"],
  "author": "GTM Labs",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/gtm-labs/mcp-server"
  },
  "dependencies": {
    "mcp": "^1.0.0"
  }
}
```

3. **Create Executable Wrapper** (`bin/gtm-labs-mcp`)

```bash
#!/usr/bin/env python3
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Run the server
from index import main
main()
```

4. **Publish to NPM**

```bash
npm login
npm publish --access public
```

**Users install with:**
```bash
npm install -g @gtm-labs/mcp-server
```

---

### Option 2: PyPI Package (Python-focused)

Distribute as a Python package.

#### Steps:

1. **Create Package Structure**

```bash
gtm-labs-mcp/
├── setup.py
├── README.md
├── LICENSE
├── gtm_labs_mcp/
│   ├── __init__.py
│   └── server.py
└── requirements.txt
```

2. **Create `setup.py`**

```python
from setuptools import setup, find_packages

setup(
    name="gtm-labs-mcp",
    version="1.0.0",
    description="GTM Labs component library MCP server",
    author="GTM Labs",
    author_email="your@email.com",
    url="https://github.com/gtm-labs/mcp-server",
    packages=find_packages(),
    install_requires=[
        "mcp>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "gtm-labs-mcp=gtm_labs_mcp.server:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.10",
)
```

3. **Publish to PyPI**

```bash
python setup.py sdist bdist_wheel
twine upload dist/*
```

**Users install with:**
```bash
pip install gtm-labs-mcp
```

---

### Option 3: GitHub + Direct Install

Simplest option - host on GitHub, users install directly.

#### Steps:

1. **Create GitHub Repository**
   - Name: `gtm-labs-mcp-server`
   - Public repository

2. **Add Installation Script** (`install.sh`)

```bash
#!/bin/bash
echo "Installing GTM Labs MCP Server..."

# Install Python dependencies
pip3 install mcp

# Clone or download the server
mkdir -p ~/.mcp-servers/gtm-labs
curl -o ~/.mcp-servers/gtm-labs/server.py \
  https://raw.githubusercontent.com/gtm-labs/mcp-server/main/gtm-labs-mcp.py

chmod +x ~/.mcp-servers/gtm-labs/server.py

# Create config
mkdir -p ~/.config/windsurf/mcp
cat > ~/.config/windsurf/mcp/gtm-labs.json << EOF
{
  "gtm-labs": {
    "command": "python3",
    "args": ["$HOME/.mcp-servers/gtm-labs/server.py"]
  }
}
EOF

echo "✅ GTM Labs MCP installed!"
echo "Restart your IDE to use it."
```

**Users install with:**
```bash
curl -fsSL https://raw.githubusercontent.com/gtm-labs/mcp-server/main/install.sh | bash
```

---

## 🏪 MCP Marketplace Submission

To appear in the official MCP marketplace (when available):

### Requirements:

1. **Public GitHub Repository**
   - Well-documented README
   - Clear installation instructions
   - Examples and usage guide

2. **Package Metadata**
   - Name, description, keywords
   - License (MIT recommended)
   - Version number (semantic versioning)

3. **MCP Manifest** (`mcp.json`)

```json
{
  "name": "gtm-labs",
  "displayName": "GTM Labs Component Library",
  "description": "Access GTM Labs website components, layouts, and design system via MCP",
  "version": "1.0.0",
  "author": "GTM Labs",
  "license": "MIT",
  "repository": "https://github.com/gtm-labs/mcp-server",
  "homepage": "https://gtm-labs.com",
  "categories": ["components", "design-system", "nextjs"],
  "server": {
    "command": "python3",
    "args": ["${serverPath}/gtm-labs-mcp.py"]
  },
  "tools": [
    {
      "name": "list_components",
      "description": "List all available components"
    },
    {
      "name": "get_component",
      "description": "Get a component with full blueprint"
    },
    {
      "name": "get_component_specs",
      "description": "Get component specifications"
    },
    {
      "name": "search_components",
      "description": "Search for components"
    },
    {
      "name": "create_scaffold",
      "description": "Create project scaffold"
    },
    {
      "name": "get_changelog",
      "description": "Get version history"
    }
  ]
}
```

4. **Submit to Registry**

Once the official MCP registry is available:
- Submit via GitHub PR to the registry repo
- Or use CLI: `mcp publish`

---

## 🌐 Making It Portable

Your current MCP has a hardcoded path. To make it work for anyone:

### Solution: Configuration File

Create a config that users set up:

**`~/.gtm-labs-mcp/config.json`**
```json
{
  "project_root": "/path/to/their/gtm-labs-project"
}
```

**Update `gtm-labs-mcp.py`:**

```python
import json
from pathlib import Path

# Load user config
config_path = Path.home() / ".gtm-labs-mcp" / "config.json"
if config_path.exists():
    with open(config_path) as f:
        config = json.load(f)
    PROJECT_ROOT = Path(config["project_root"])
else:
    # Fallback to default
    PROJECT_ROOT = Path(__file__).parent.resolve()

HOMEPAGE_ROOT = PROJECT_ROOT / "homepage"
COMPONENTS_DIR = HOMEPAGE_ROOT / "components"
# ... rest of code
```

**Installation becomes:**

```bash
# Install the MCP
pip install gtm-labs-mcp

# Configure it
mkdir -p ~/.gtm-labs-mcp
cat > ~/.gtm-labs-mcp/config.json << EOF
{
  "project_root": "/Users/yourname/your-gtm-project"
}
EOF

# Add to Windsurf config
# ... (automatic or manual)
```

---

## 📋 Recommended Distribution Path

For GTM Labs MCP, I recommend:

1. **Phase 1: GitHub (Now)**
   - Create public repo: `gtm-labs/mcp-server`
   - Add README, LICENSE, install script
   - Users install via curl script

2. **Phase 2: NPM Package (Next)**
   - Package as `@gtm-labs/mcp-server`
   - Publish to NPM
   - Users: `npm install -g @gtm-labs/mcp-server`

3. **Phase 3: MCP Marketplace (Future)**
   - Submit to official registry when available
   - Users discover in IDE marketplace
   - One-click install

---

## 🚀 Quick Start for Public Distribution

### Step 1: Create GitHub Repo

```bash
cd /Users/jovannytovar/gtm-homepage-ver-webinarshortform/gtm-homepage-2
git init
git add gtm-labs-mcp.py MCP-README.md COMPONENT-CATALOG.md
git commit -m "Initial MCP server"
git remote add origin https://github.com/gtm-labs/mcp-server.git
git push -u origin main
```

### Step 2: Create Install Script

See `install.sh` example above.

### Step 3: Document Installation

Update README with:
```markdown
# Installation

```bash
curl -fsSL https://raw.githubusercontent.com/gtm-labs/mcp-server/main/install.sh | bash
```

Then restart your IDE.
```

### Step 4: Announce

- Post on Twitter/X
- Share in MCP community Discord
- Add to awesome-mcp list

---

## 🎯 Next Steps for You

1. **Fix Current Installation** (restart Windsurf after the path fix)
2. **Create GitHub repo** for public access
3. **Add install script** for easy setup
4. **Consider NPM package** for wider distribution
5. **Wait for MCP marketplace** and submit when ready

---

## 📞 Support

For questions about MCP distribution:
- [MCP Documentation](https://modelcontextprotocol.io)
- [MCP GitHub](https://github.com/modelcontextprotocol)
- [MCP Discord](https://discord.gg/mcp)

---

**Current Status:** Your MCP works locally. Path is now fixed. Restart Windsurf to test.

**Next:** Make it public via GitHub for others to use.
