#!/usr/bin/env python3
"""
GTM Labs MCP Server - GitHub API Version
Fetches components directly from GitHub (always latest, no git clone needed!)

This version fetches files directly from GitHub's API, so users always get
the latest components without needing to clone repos or run git pull.
"""

import json
import base64
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# MCP SDK imports
try:
    from mcp.server import Server
    from mcp.types import Resource, Tool, TextContent
    import mcp.server.stdio
except ImportError:
    print("Error: MCP SDK not installed. Install with: pip install mcp", file=sys.stderr)
    sys.exit(1)

# HTTP requests
try:
    import requests
except ImportError:
    print("Error: requests not installed. Install with: pip install requests", file=sys.stderr)
    sys.exit(1)

# GitHub configuration - Supports multiple accounts!
GITHUB_REPOS = {
    # GTM Labs projects (GTM-LABS-io account)
    "website": {"owner": "GTM-LABS-io", "repo": "gtmlabs-website"},
    
    # Personal projects (buildingwithai account)
    # "personal-project": {"owner": "buildingwithai", "repo": "project-name"},
    
    # Add more projects as you create them:
    # "saas": {"owner": "GTM-LABS-io", "repo": "gtm-saas-landing"},
    # "portfolio": {"owner": "GTM-LABS-io", "repo": "gtm-portfolio"},
}

# Optional: Load GitHub token from config for higher rate limits
def load_github_token():
    """Load GitHub token from config if available"""
    config_path = Path.home() / ".gtm-labs-mcp" / "config.json"
    if config_path.exists():
        try:
            with open(config_path) as f:
                config = json.load(f)
                return config.get("github_token")
        except:
            pass
    return None

GITHUB_TOKEN = load_github_token()

# Initialize MCP server
app = Server("gtm-labs")

def github_request(url: str) -> requests.Response:
    """Make a request to GitHub API with optional authentication"""
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    
    response = requests.get(url, headers=headers)
    return response

def fetch_file_from_github(owner: str, repo: str, path: str) -> Dict:
    """Fetch a single file from GitHub"""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    response = github_request(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Decode base64 content
        content = base64.b64decode(data["content"]).decode("utf-8")
        
        return {
            "name": data["name"],
            "path": data["path"],
            "content": content,
            "sha": data["sha"],
            "url": data["html_url"],
            "size": data["size"]
        }
    elif response.status_code == 404:
        raise Exception(f"File not found: {path}")
    elif response.status_code == 403:
        raise Exception("GitHub API rate limit exceeded. Add a GitHub token to your config for higher limits.")
    else:
        raise Exception(f"GitHub API error: {response.status_code} - {response.text}")

def list_directory_from_github(owner: str, repo: str, path: str = "") -> List[Dict]:
    """List contents of a directory from GitHub"""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    response = github_request(url)
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        return []
    elif response.status_code == 403:
        raise Exception("GitHub API rate limit exceeded. Add a GitHub token to your config for higher limits.")
    else:
        raise Exception(f"GitHub API error: {response.status_code}")

def scan_components_from_github(owner: str, repo: str, base_path: str = "homepage/components") -> List[Dict]:
    """Recursively scan all components from a GitHub repo"""
    components = []
    
    try:
        items = list_directory_from_github(owner, repo, base_path)
        
        for item in items:
            if item["type"] == "file":
                # Include .tsx, .ts, .jsx, .js files
                if any(item["name"].endswith(ext) for ext in [".tsx", ".ts", ".jsx", ".js"]):
                    components.append({
                        "name": item["name"].rsplit(".", 1)[0],  # Remove extension
                        "path": item["path"],
                        "url": item["html_url"],
                        "type": "file",
                        "category": Path(item["path"]).parent.name
                    })
            elif item["type"] == "dir":
                # Recursively scan subdirectories
                sub_components = scan_components_from_github(owner, repo, item["path"])
                components.extend(sub_components)
    except Exception as e:
        print(f"Warning: Could not scan {base_path}: {e}", file=sys.stderr)
    
    return components

def get_component_with_dependencies(owner: str, repo: str, component_path: str) -> Dict:
    """Get a component and analyze its dependencies"""
    # Fetch the main component
    component = fetch_file_from_github(owner, repo, component_path)
    
    # Parse imports to find dependencies
    import_pattern = r'import\s+.*?\s+from\s+[\'"](.+?)[\'"]'
    imports = []
    
    for match in re.finditer(import_pattern, component["content"]):
        import_path = match.group(1)
        
        # Only include relative imports (local dependencies)
        if import_path.startswith("."):
            imports.append(import_path)
    
    # Fetch dependencies
    dependencies = []
    component_dir = Path(component_path).parent
    
    for import_path in imports:
        try:
            # Resolve relative path
            if import_path.startswith("./"):
                dep_path = component_dir / import_path[2:]
            elif import_path.startswith("../"):
                dep_path = component_dir / import_path
            else:
                continue
            
            # Add .tsx if no extension
            if not dep_path.suffix:
                dep_path = dep_path.with_suffix(".tsx")
            
            # Fetch dependency
            dep = fetch_file_from_github(owner, repo, str(dep_path))
            dependencies.append(dep)
        except Exception as e:
            print(f"Warning: Could not fetch dependency {import_path}: {e}", file=sys.stderr)
    
    return {
        "component": component,
        "dependencies": dependencies,
        "import_count": len(imports)
    }

import re

# MCP Tool Definitions
@app.list_tools()
async def list_tools() -> List[Tool]:
    """List available MCP tools"""
    return [
        Tool(
            name="list_components",
            description="List all available components from GTM Labs projects. Returns component names, paths, and categories.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project": {
                        "type": "string",
                        "description": "Project name to list components from",
                        "enum": list(GITHUB_REPOS.keys())
                    },
                    "category": {
                        "type": "string",
                        "description": "Optional: Filter by category (ui, sections, animations, etc.)"
                    }
                }
            }
        ),
        Tool(
            name="get_component",
            description="Get a specific component with its full code and dependencies. Always returns the latest version from GitHub.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Component name (e.g., 'pricing-section', 'hero-section')"
                    },
                    "project": {
                        "type": "string",
                        "description": "Project name",
                        "enum": list(GITHUB_REPOS.keys()),
                        "default": "website"
                    },
                    "include_dependencies": {
                        "type": "boolean",
                        "description": "Include all component dependencies",
                        "default": True
                    }
                },
                "required": ["name"]
            }
        ),
        Tool(
            name="search_components",
            description="Search for components across all GTM Labs projects by name or content.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (searches component names and categories)"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_design_tokens",
            description="Get design tokens (colors, spacing, typography, etc.) from a project.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project": {
                        "type": "string",
                        "description": "Project name",
                        "enum": list(GITHUB_REPOS.keys()),
                        "default": "website"
                    }
                }
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> List[TextContent]:
    """Handle tool calls"""
    
    try:
        if name == "list_components":
            project = arguments.get("project", "website")
            category_filter = arguments.get("category")
            
            repo_info = GITHUB_REPOS.get(project)
            if not repo_info:
                return [TextContent(type="text", text=f"Project '{project}' not found")]
            
            owner = repo_info["owner"]
            repo = repo_info["repo"]
            
            # Scan components
            components = scan_components_from_github(owner, repo)
            
            # Filter by category if specified
            if category_filter:
                components = [c for c in components if c["category"] == category_filter]
            
            # Group by category
            by_category = {}
            for comp in components:
                cat = comp["category"]
                if cat not in by_category:
                    by_category[cat] = []
                by_category[cat].append(comp["name"])
            
            result = {
                "project": project,
                "total_components": len(components),
                "categories": by_category,
                "components": components
            }
            
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "get_component":
            component_name = arguments["name"]
            project = arguments.get("project", "website")
            include_deps = arguments.get("include_dependencies", True)
            
            repo_info = GITHUB_REPOS.get(project)
            if not repo_info:
                return [TextContent(type="text", text=f"Project '{project}' not found")]
            
            owner = repo_info["owner"]
            repo = repo_info["repo"]
            
            # Find the component
            components = scan_components_from_github(owner, repo)
            matching = [c for c in components if component_name.lower() in c["name"].lower()]
            
            if not matching:
                return [TextContent(type="text", text=f"Component '{component_name}' not found in {project}")]
            
            # Get the first match
            component_info = matching[0]
            
            if include_deps:
                # Get component with dependencies
                full_component = get_component_with_dependencies(owner, repo, component_info["path"])
                
                result = {
                    "name": component_info["name"],
                    "project": project,
                    "path": component_info["path"],
                    "github_url": component_info["url"],
                    "code": full_component["component"]["content"],
                    "dependencies": [
                        {
                            "name": dep["name"],
                            "path": dep["path"],
                            "code": dep["content"]
                        }
                        for dep in full_component["dependencies"]
                    ],
                    "dependency_count": len(full_component["dependencies"])
                }
            else:
                # Just get the component file
                component_file = fetch_file_from_github(owner, repo, component_info["path"])
                
                result = {
                    "name": component_info["name"],
                    "project": project,
                    "path": component_info["path"],
                    "github_url": component_info["url"],
                    "code": component_file["content"]
                }
            
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "search_components":
            query = arguments["query"].lower()
            
            all_results = []
            
            # Search across all projects
            for project, repo_info in GITHUB_REPOS.items():
                try:
                    owner = repo_info["owner"]
                    repo = repo_info["repo"]
                    components = scan_components_from_github(owner, repo)
                    
                    # Search in name and category
                    matching = [
                        c for c in components 
                        if query in c["name"].lower() or query in c["category"].lower()
                    ]
                    
                    for comp in matching:
                        comp["project"] = project
                        all_results.append(comp)
                except Exception as e:
                    print(f"Warning: Could not search {project}: {e}", file=sys.stderr)
            
            result = {
                "query": query,
                "total_results": len(all_results),
                "results": all_results
            }
            
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "get_design_tokens":
            project = arguments.get("project", "website")
            
            repo_info = GITHUB_REPOS.get(project)
            if not repo_info:
                return [TextContent(type="text", text=f"Project '{project}' not found")]
            
            owner = repo_info["owner"]
            repo = repo_info["repo"]
            
            # Try to fetch design tokens file
            token_paths = [
                "homepage/lib/design-tokens.ts",
                "homepage/lib/tokens.ts",
                "lib/design-tokens.ts",
                "lib/tokens.ts"
            ]
            
            for path in token_paths:
                try:
                    tokens = fetch_file_from_github(owner, repo, path)
                    
                    result = {
                        "project": project,
                        "path": path,
                        "github_url": tokens["url"],
                        "code": tokens["content"]
                    }
                    
                    return [TextContent(type="text", text=json.dumps(result, indent=2))]
                except:
                    continue
            
            return [TextContent(type="text", text=f"Design tokens not found in {project}")]
        
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(error_msg, file=sys.stderr)
        return [TextContent(type="text", text=error_msg)]

async def main():
    """Run the MCP server"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
