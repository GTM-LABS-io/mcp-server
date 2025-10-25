#!/usr/bin/env python3
"""
GTM Labs MCP Server (Portable Version)
Exposes website components, layouts, animations, and scaffolds via Model Context Protocol

This version uses a config file to locate the GTM Labs project, making it portable.
"""

import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional
import sys

# MCP SDK imports
try:
    from mcp.server import Server
    from mcp.types import (
        Resource,
        Tool,
        TextContent,
        ImageContent,
        EmbeddedResource,
    )
    import mcp.server.stdio
except ImportError:
    print("Error: MCP SDK not installed. Install with: pip install mcp", file=sys.stderr)
    sys.exit(1)

# Load configuration
def load_config():
    """Load project path from config file"""
    # Check for config in multiple locations
    config_locations = [
        Path.home() / ".gtm-labs-mcp" / "config.json",
        Path.home() / ".config" / "gtm-labs-mcp" / "config.json",
        Path(__file__).parent / "config.json",
    ]
    
    for config_path in config_locations:
        if config_path.exists():
            try:
                with open(config_path) as f:
                    config = json.load(f)
                return Path(config["project_root"])
            except Exception as e:
                print(f"Warning: Could not load config from {config_path}: {e}", file=sys.stderr)
    
    # Fallback: assume script is in project root
    return Path(__file__).parent.resolve()

# Project paths - Load from config
PROJECT_ROOT = load_config()
HOMEPAGE_ROOT = PROJECT_ROOT / "homepage"
COMPONENTS_DIR = HOMEPAGE_ROOT / "components"
APP_DIR = HOMEPAGE_ROOT / "app"
LIB_DIR = HOMEPAGE_ROOT / "lib"

# Verify paths exist
if not HOMEPAGE_ROOT.exists():
    print(f"Error: Homepage directory not found at {HOMEPAGE_ROOT}", file=sys.stderr)
    print(f"Create a config file at ~/.gtm-labs-mcp/config.json with:", file=sys.stderr)
    print(json.dumps({"project_root": "/path/to/your/gtm-labs-project"}, indent=2), file=sys.stderr)
    sys.exit(1)

# Security: Files/patterns to EXCLUDE
EXCLUDED_PATTERNS = [
    r"\.env",
    r".*secret.*",
    r".*private.*",
    r"personas/",
    r"messaging/",
    r"internal-docs/",
    r"Deep Research/",
    r"node_modules/",
    r"\.git/",
]

# Security: Content to REDACT
REDACT_PATTERNS = [
    (r"(MyMarky|UseQueue)", "[REDACTED_TOOL]"),
    (r"(sk-[a-zA-Z0-9]{48}|api[_-]?key[_-]?[a-zA-Z0-9]+)", "[REDACTED_KEY]"),
]


def should_exclude_file(file_path: Path) -> bool:
    """Check if file should be excluded based on security rules"""
    path_str = str(file_path)
    for pattern in EXCLUDED_PATTERNS:
        if re.search(pattern, path_str, re.IGNORECASE):
            return True
    return False


def redact_content(content: str) -> str:
    """Redact sensitive content from file contents"""
    for pattern, replacement in REDACT_PATTERNS:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    return content


def get_git_versions(file_path: Optional[Path] = None) -> List[Dict[str, str]]:
    """Get all Git versions (tags and commits) for a file or entire repo"""
    try:
        if file_path:
            # Get commits for specific file
            cmd = ["git", "log", "--pretty=format:%H|%ai|%s", "--", str(file_path)]
        else:
            # Get all tags
            cmd = ["git", "tag", "-l", "--format=%(refname:short)|%(creatordate:iso)|%(subject)"]
        
        result = subprocess.run(
            cmd,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True
        )
        
        versions = []
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            parts = line.split("|")
            if len(parts) >= 2:
                versions.append({
                    "version": parts[0],
                    "date": parts[1] if len(parts) > 1 else "",
                    "message": parts[2] if len(parts) > 2 else ""
                })
        return versions
    except Exception:
        return []


def get_file_at_version(file_path: Path, version: str = "HEAD") -> Optional[str]:
    """Get file contents at specific Git version"""
    try:
        rel_path = file_path.relative_to(PROJECT_ROOT)
        result = subprocess.run(
            ["git", "show", f"{version}:{rel_path}"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True
        )
        return redact_content(result.stdout)
    except Exception:
        return None


def get_component_dependencies(file_path: Path) -> List[str]:
    """Extract import dependencies from a component file"""
    try:
        content = file_path.read_text()
        dependencies = []
        
        # Match imports from local files
        import_pattern = r"import\s+.*?\s+from\s+['\"](@/[^'\"]+|\.+/[^'\"]+)['\"]"
        matches = re.findall(import_pattern, content)
        
        for match in matches:
            # Convert to absolute path
            if match.startswith("@/"):
                dep_path = HOMEPAGE_ROOT / match[2:]
            else:
                dep_path = (file_path.parent / match).resolve()
            
            dependencies.append(str(dep_path.relative_to(PROJECT_ROOT)))
        
        return dependencies
    except Exception:
        return []


def scan_components() -> Dict[str, List[Path]]:
    """Scan and categorize all components"""
    categories = {
        "sections": [],
        "navigation": [],
        "animations": [],
        "ui": [],
        "cosmic": [],
        "magicui": [],
        "experiments": [],
    }
    
    if not COMPONENTS_DIR.exists():
        return categories
    
    for file_path in COMPONENTS_DIR.rglob("*.tsx"):
        if should_exclude_file(file_path):
            continue
        
        rel_path = file_path.relative_to(COMPONENTS_DIR)
        
        # Categorize based on directory structure
        if "cosmic" in rel_path.parts:
            categories["cosmic"].append(file_path)
        elif "magicui" in rel_path.parts:
            categories["magicui"].append(file_path)
        elif "experiments" in rel_path.parts:
            categories["experiments"].append(file_path)
        elif "ui" in rel_path.parts:
            # Check if it's a section or animation
            if "section" in file_path.stem.lower():
                categories["sections"].append(file_path)
            elif "animation" in file_path.stem.lower():
                categories["animations"].append(file_path)
            else:
                categories["ui"].append(file_path)
        else:
            # Top-level components
            if any(keyword in file_path.stem.lower() for keyword in ["nav", "header", "footer"]):
                categories["navigation"].append(file_path)
            else:
                categories["ui"].append(file_path)
    
    return categories


def get_component_specs(file_path: Path) -> Dict[str, Any]:
    """Extract detailed specs from component (colors, animations, sizes, etc.)"""
    try:
        content = file_path.read_text()
        specs = {
            "colors": [],
            "animations": [],
            "borders": [],
            "spacing": [],
            "fonts": []
        }
        
        # Extract Tailwind classes and inline styles
        # Colors
        color_pattern = r"(?:bg|text|border)-(?:slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-\d+"
        specs["colors"] = list(set(re.findall(color_pattern, content)))
        
        # Animations
        animation_pattern = r"animate-[\w-]+"
        specs["animations"] = list(set(re.findall(animation_pattern, content)))
        
        # Border radius
        border_pattern = r"rounded-(?:none|sm|md|lg|xl|2xl|3xl|full|\d+)"
        specs["borders"] = list(set(re.findall(border_pattern, content)))
        
        # Spacing (padding, margin)
        spacing_pattern = r"(?:p|m|px|py|pl|pr|pt|pb|mx|my|ml|mr|mt|mb)-\d+"
        specs["spacing"] = list(set(re.findall(spacing_pattern, content)))
        
        # Font sizes
        font_pattern = r"text-(?:xs|sm|base|lg|xl|2xl|3xl|4xl|5xl|6xl|7xl|8xl|9xl)"
        specs["fonts"] = list(set(re.findall(font_pattern, content)))
        
        return specs
    except Exception:
        return {}


# Initialize MCP Server
app = Server("gtm-labs")


@app.list_resources()
async def list_resources() -> List[Resource]:
    """List all available GTM Labs resources"""
    resources = []
    
    # Scan components
    components = scan_components()
    
    for category, files in components.items():
        for file_path in files:
            name = file_path.stem
            uri = f"gtm-labs://components/{category}/{name}"
            
            resources.append(Resource(
                uri=uri,
                name=f"{category}/{name}",
                mimeType="text/typescript",
                description=f"Component: {name} from {category}"
            ))
    
    # Add config files
    config_files = [
        ("tailwind.config.ts", "Config: Tailwind configuration"),
        ("next.config.ts", "Config: Next.js configuration"),
        ("package.json", "Config: Package dependencies"),
    ]
    
    for file_name, description in config_files:
        file_path = HOMEPAGE_ROOT / file_name
        if file_path.exists():
            resources.append(Resource(
                uri=f"gtm-labs://config/{file_name}",
                name=file_name,
                mimeType="application/json" if file_name.endswith(".json") else "text/typescript",
                description=description
            ))
    
    # Add design tokens
    if LIB_DIR.exists():
        for lib_file in LIB_DIR.glob("*.ts"):
            if not should_exclude_file(lib_file):
                resources.append(Resource(
                    uri=f"gtm-labs://lib/{lib_file.stem}",
                    name=lib_file.stem,
                    mimeType="text/typescript",
                    description=f"Library: {lib_file.stem}"
                ))
    
    # Add scaffolds
    resources.append(Resource(
        uri="gtm-labs://scaffolds/nextjs-full-project",
        name="nextjs-full-project",
        mimeType="application/json",
        description="Scaffold: Full Next.js project with GTM Labs structure"
    ))
    
    return resources


@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read a specific resource"""
    parts = uri.replace("gtm-labs://", "").split("/")
    
    if parts[0] == "components":
        # components/{category}/{name}
        category = parts[1]
        name = parts[2]
        
        # Find the component file
        components = scan_components()
        if category in components:
            for file_path in components[category]:
                if file_path.stem == name:
                    content = file_path.read_text()
                    return redact_content(content)
    
    elif parts[0] == "config":
        file_name = parts[1]
        file_path = HOMEPAGE_ROOT / file_name
        if file_path.exists():
            content = file_path.read_text()
            return redact_content(content)
    
    elif parts[0] == "lib":
        lib_name = parts[1]
        file_path = LIB_DIR / f"{lib_name}.ts"
        if file_path.exists():
            content = file_path.read_text()
            return redact_content(content)
    
    elif parts[0] == "scaffolds":
        # Return scaffold template
        return json.dumps({
            "scaffold": parts[1],
            "message": "Use the create_scaffold tool to generate this scaffold"
        }, indent=2)
    
    return "Resource not found"


@app.list_tools()
async def list_tools() -> List[Tool]:
    """List all available tools"""
    return [
        Tool(
            name="list_components",
            description="List all available components, optionally filtered by category or version",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Filter by category: sections, navigation, animations, ui, cosmic, magicui, experiments",
                        "enum": ["sections", "navigation", "animations", "ui", "cosmic", "magicui", "experiments", "all"]
                    },
                    "version": {
                        "type": "string",
                        "description": "Optional: specific Git tag or commit hash"
                    }
                }
            }
        ),
        Tool(
            name="get_component",
            description="Get a specific component with full blueprint (includes dependencies, specs, and code)",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Component name (e.g., 'hero-section', 'how-we-help-section')"
                    },
                    "version": {
                        "type": "string",
                        "description": "Optional: Git tag, commit hash, or 'latest' (default: latest)"
                    },
                    "include_dependencies": {
                        "type": "boolean",
                        "description": "Include all dependent files (default: true)"
                    }
                },
                "required": ["name"]
            }
        ),
        Tool(
            name="get_component_specs",
            description="Get detailed specifications for a component (colors, animations, borders, spacing, fonts)",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Component name"
                    },
                    "property": {
                        "type": "string",
                        "description": "Optional: specific property (colors, animations, borders, spacing, fonts)",
                        "enum": ["colors", "animations", "borders", "spacing", "fonts", "all"]
                    }
                },
                "required": ["name"]
            }
        ),
        Tool(
            name="get_changelog",
            description="Get version history and changelog for a component or entire project",
            inputSchema={
                "type": "object",
                "properties": {
                    "component": {
                        "type": "string",
                        "description": "Optional: specific component name (omit for project-wide changelog)"
                    },
                    "version_range": {
                        "type": "string",
                        "description": "Optional: version range (e.g., 'v1.0.0..v1.2.0')"
                    }
                }
            }
        ),
        Tool(
            name="search_components",
            description="Search components by query (name, content, or properties)",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "filters": {
                        "type": "object",
                        "description": "Optional filters (category, has_animation, color_scheme, etc.)"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="create_scaffold",
            description="Create a project scaffold with selected components and structure",
            inputSchema={
                "type": "object",
                "properties": {
                    "template": {
                        "type": "string",
                        "description": "Scaffold template: 'nextjs-full-project' or 'landing-page'",
                        "enum": ["nextjs-full-project", "landing-page"]
                    },
                    "components": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of component names to include"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Output directory path"
                    }
                },
                "required": ["template", "output_path"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> List[TextContent]:
    """Handle tool calls"""
    
    if name == "list_components":
        category = arguments.get("category", "all")
        version = arguments.get("version")
        
        components = scan_components()
        result = {"components": {}}
        
        if category == "all":
            result["components"] = {
                cat: [str(f.relative_to(COMPONENTS_DIR)) for f in files]
                for cat, files in components.items()
            }
        elif category in components:
            result["components"][category] = [
                str(f.relative_to(COMPONENTS_DIR)) for f in components[category]
            ]
        
        if version:
            result["version"] = version
            result["note"] = f"Showing components at version: {version}"
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    elif name == "get_component":
        component_name = arguments["name"]
        version = arguments.get("version", "HEAD")
        include_deps = arguments.get("include_dependencies", True)
        
        # Find component file
        components = scan_components()
        component_file = None
        
        for files in components.values():
            for file_path in files:
                if file_path.stem == component_name:
                    component_file = file_path
                    break
            if component_file:
                break
        
        if not component_file:
            return [TextContent(
                type="text",
                text=json.dumps({"error": f"Component '{component_name}' not found"})
            )]
        
        # Get component content
        content = get_file_at_version(component_file, version)
        if not content:
            content = component_file.read_text()
            content = redact_content(content)
        
        result = {
            "name": component_name,
            "path": str(component_file.relative_to(PROJECT_ROOT)),
            "version": version,
            "content": content,
            "specs": get_component_specs(component_file)
        }
        
        if include_deps:
            result["dependencies"] = get_component_dependencies(component_file)
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    elif name == "get_component_specs":
        component_name = arguments["name"]
        property_filter = arguments.get("property", "all")
        
        # Find component
        components = scan_components()
        component_file = None
        
        for files in components.values():
            for file_path in files:
                if file_path.stem == component_name:
                    component_file = file_path
                    break
            if component_file:
                break
        
        if not component_file:
            return [TextContent(
                type="text",
                text=json.dumps({"error": f"Component '{component_name}' not found"})
            )]
        
        specs = get_component_specs(component_file)
        
        if property_filter != "all":
            specs = {property_filter: specs.get(property_filter, [])}
        
        result = {
            "component": component_name,
            "specs": specs
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    elif name == "get_changelog":
        component = arguments.get("component")
        version_range = arguments.get("version_range")
        
        if component:
            # Find component file
            components = scan_components()
            component_file = None
            
            for files in components.values():
                for file_path in files:
                    if file_path.stem == component:
                        component_file = file_path
                        break
                if component_file:
                    break
            
            if not component_file:
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": f"Component '{component}' not found"})
                )]
            
            versions = get_git_versions(component_file)
            result = {
                "component": component,
                "changelog": versions
            }
        else:
            # Project-wide changelog (tags)
            versions = get_git_versions()
            result = {
                "project": "gtm-labs",
                "releases": versions
            }
        
        if version_range:
            result["version_range"] = version_range
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    elif name == "search_components":
        query = arguments["query"].lower()
        filters = arguments.get("filters", {})
        
        components = scan_components()
        results = []
        
        for category, files in components.items():
            for file_path in files:
                name = file_path.stem
                
                # Check if query matches name
                if query in name.lower():
                    results.append({
                        "name": name,
                        "category": category,
                        "path": str(file_path.relative_to(PROJECT_ROOT))
                    })
                # Check content
                else:
                    try:
                        content = file_path.read_text().lower()
                        if query in content:
                            results.append({
                                "name": name,
                                "category": category,
                                "path": str(file_path.relative_to(PROJECT_ROOT)),
                                "match": "content"
                            })
                    except Exception:
                        pass
        
        return [TextContent(
            type="text",
            text=json.dumps({"query": query, "results": results}, indent=2)
        )]
    
    elif name == "create_scaffold":
        template = arguments["template"]
        components_list = arguments.get("components", [])
        output_path = arguments["output_path"]
        
        scaffold_data = {
            "template": template,
            "output_path": output_path,
            "structure": {
                "app/": ["layout.tsx", "page.tsx", "globals.css"],
                "components/": ["ui/", "cosmic/", "magicui/"],
                "lib/": ["utils.ts", "design-tokens.ts"],
                "public/": [],
            },
            "configs": [
                "package.json",
                "tailwind.config.ts",
                "next.config.ts",
                "tsconfig.json"
            ],
            "components_to_include": components_list,
            "note": "Use this data to create the scaffold structure. Copy files from GTM Labs project to output_path."
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(scaffold_data, indent=2)
        )]
    
    return [TextContent(
        type="text",
        text=json.dumps({"error": "Unknown tool"})
    )]


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
