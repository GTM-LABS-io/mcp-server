# GTM Labs MCP Server

Transform your GTM Labs website into a reusable component library and project scaffolding system via Model Context Protocol (MCP).

## 🎯 What This Does

The GTM Labs MCP Server exposes your entire website codebase as:
- **Individual components** (hero sections, two-column layouts, animations, etc.)
- **Full blueprints** (component + dependencies + styles + utilities)
- **Design tokens** (Tailwind config, design tokens, animation utilities)
- **Project scaffolds** (full Next.js skeleton with your components)
- **Version control** (access any historical version via Git tags/commits)

## 📦 Installation

### 1. Install Python Dependencies

```bash
pip3 install mcp
# or
pip3 install -r mcp-requirements.txt
```

### 2. Set Up MCP Directory

```bash
# Create MCP directory
mkdir -p ~/mcp-servers

# Copy the MCP file
cp gtm-labs-mcp.py ~/mcp-servers/

# Make it executable
chmod +x ~/mcp-servers/gtm-labs-mcp.py
```

### 3. Test the Server

```bash
# Test it runs (press Ctrl+C to stop)
python3 ~/mcp-servers/gtm-labs-mcp.py
```

### 4. Configure Windsurf

Create `.windsurf/mcp_config.json` in your workspace:

```json
{
  "gtm-labs": {
    "command": "python3",
    "args": ["/Users/YOUR_USERNAME/mcp-servers/gtm-labs-mcp.py"]
  }
}
```

Replace `YOUR_USERNAME` with your actual username, or use:

```bash
# Auto-create config
mkdir -p .windsurf
cat > .windsurf/mcp_config.json << 'EOF'
{
  "gtm-labs": {
    "command": "python3",
    "args": ["${HOME}/mcp-servers/gtm-labs-mcp.py"]
  }
}
EOF
```

### 5. Restart Windsurf

Restart Windsurf to load the new MCP server.

## 🧪 Testing

Try these commands in Windsurf:

```
✓ "Use GTM Labs MCP to list all components"
✓ "Use GTM Labs MCP to get the how-we-help-section component"
✓ "Use GTM Labs MCP to show me the design tokens"
✓ "Use GTM Labs MCP to get component specs for hero-section"
✓ "Use GTM Labs MCP to create a scaffold with navbar and hero"
```

## 📚 Available Tools

### 1. `list_components`
List all components, optionally filtered by category or version.

**Parameters:**
- `category` (optional): Filter by `sections`, `navigation`, `animations`, `ui`, `cosmic`, `magicui`, `experiments`, or `all`
- `version` (optional): Specific Git tag or commit hash

**Example:**
```
"List all section components using GTM Labs MCP"
"List components at version v1.0.0"
```

### 2. `get_component`
Get a component with full blueprint (code, dependencies, specs).

**Parameters:**
- `name` (required): Component name (e.g., `hero-section`, `how-we-help-section`)
- `version` (optional): Git tag, commit, or `latest` (default: latest)
- `include_dependencies` (optional): Include dependent files (default: true)

**Example:**
```
"Get the how-we-help-section component"
"Get hero-section at version v1.0.0"
```

### 3. `get_component_specs`
Get detailed specifications (colors, animations, borders, spacing, fonts).

**Parameters:**
- `name` (required): Component name
- `property` (optional): Specific property (`colors`, `animations`, `borders`, `spacing`, `fonts`, or `all`)

**Example:**
```
"Show me the color specs for hero-section"
"What animations does the two-column-layout use?"
```

### 4. `get_changelog`
Get version history for a component or entire project.

**Parameters:**
- `component` (optional): Component name (omit for project-wide changelog)
- `version_range` (optional): Version range (e.g., `v1.0.0..v1.2.0`)

**Example:**
```
"Show changelog for hero-section"
"Show all releases"
```

### 5. `search_components`
Search components by name, content, or properties.

**Parameters:**
- `query` (required): Search query
- `filters` (optional): Additional filters

**Example:**
```
"Search for components with 'animation'"
"Find components using framer-motion"
```

### 6. `create_scaffold`
Create a project scaffold with selected components.

**Parameters:**
- `template` (required): `nextjs-full-project` or `landing-page`
- `components` (optional): List of component names to include
- `output_path` (required): Output directory

**Example:**
```
"Create a Next.js scaffold with hero and navbar at ./new-project"
```

## 🔐 Security

The MCP automatically:
- **Excludes**: `.env*`, `*secrets*`, `*private*`, `personas/`, `messaging/`, `internal-docs/`
- **Redacts**: API keys, CRM tool names (MyMarky, UseQueue, etc.)
- **Only exposes**: Public-facing code (components, layouts, configs)

## 📂 Resource Structure

```
gtm-labs://
├── components/
│   ├── sections/          (hero-section, how-we-help-section, etc.)
│   ├── navigation/        (navbar, footer, etc.)
│   ├── animations/        (animation components)
│   ├── ui/                (buttons, cards, inputs, etc.)
│   ├── cosmic/            (cosmic design system components)
│   ├── magicui/           (magic UI components)
│   └── experiments/       (experimental components)
├── config/
│   ├── tailwind.config.ts
│   ├── next.config.ts
│   └── package.json
├── lib/
│   ├── design-tokens
│   ├── utils
│   └── brand
└── scaffolds/
    ├── nextjs-full-project
    └── landing-page-template
```

## 🏷️ Versioning Workflow

### When You Update a Component

```bash
# 1. Make changes to component
# 2. Commit with conventional commit message
git add components/ui/hero-section.tsx
git commit -m "feat: hero-section - add gradient animation"

# 3. For stable releases, create a tag
git tag -a v1.1.0 -m "Release v1.1.0: Updated hero animations"
git push origin v1.1.0
```

### Accessing Versions via MCP

```
"Get hero-section"                    → Latest version
"Get hero-section v1.1.0"            → Tagged release
"Get hero-section at commit abc123"   → Specific commit
"Show changelog for hero-section"     → All versions
```

## 🎨 Component Categories

### Sections
Full-page sections: `hero-section`, `how-we-help-section`, `how-it-works-section`, `content-library-cards`, etc.

### Navigation
Navigation components: `navbar`, `footer`, etc.

### Animations
Animation-specific components: `how-we-help-animations`, `fade-in`, `scroll-animations`, etc.

### UI Components
Reusable UI elements: `button`, `card`, `input`, `label`, `banner`, etc.

### Cosmic
Cosmic design system: `cosmic-button`, `cosmic-card`, `glass-card`, `two-column-feature`, etc.

### MagicUI
Magic UI library: `animated-beam`, `blur-fade`, `border-beam`, `shimmer-button`, etc.

### Experiments
Experimental components: `bento-grid`, various bento section variants, etc.

## 💡 Use Cases

### 1. Quick Component Reuse
```
"Use GTM Labs MCP to get the hero-section component with all dependencies"
```

### 2. Create New Project Skeleton
```
"Use GTM Labs MCP to create a Next.js scaffold with hero, navbar, and how-we-help sections at ./my-new-project"
```

### 3. Extract Specific Styles
```
"Use GTM Labs MCP to show me what colors the hero-section uses"
"What border radius does the cosmic-card component use?"
```

### 4. Version Control
```
"Get the old version of hero-section from v1.0.0"
"Show me the changelog between v1.0.0 and v1.2.0"
```

### 5. Component Discovery
```
"Search for components that use framer-motion"
"List all animation components"
```

## 🚀 Example Workflows

### Build a Landing Page from Scratch

```
1. "Use GTM Labs MCP to create a landing-page scaffold at ./new-landing"
2. "Use GTM Labs MCP to get hero-section"
3. "Use GTM Labs MCP to get how-we-help-section"
4. "Use GTM Labs MCP to get cosmic-button"
5. Copy components into your new project
```

### Clone Your Entire Site

```
"Use GTM Labs MCP to create a nextjs-full-project scaffold with all sections at ./site-clone"
```

### Inspect Component Details

```
1. "Use GTM Labs MCP to list all section components"
2. "Use GTM Labs MCP to get component specs for how-we-help-section"
3. "Show me all colors used"
4. "Show me all animations"
```

## 🐛 Troubleshooting

### MCP Not Loading
1. Check Python is installed: `python3 --version`
2. Check MCP is installed: `pip3 show mcp`
3. Verify config path in `.windsurf/mcp_config.json`
4. Restart Windsurf

### Component Not Found
- Check component name (use `list_components` first)
- Component names use kebab-case (e.g., `hero-section`, not `HeroSection`)

### Version Not Found
- Check Git tags: `git tag -l`
- Check commits: `git log --oneline`
- Use exact tag name (e.g., `v1.0.0`, not `1.0.0`)

## 📖 Additional Resources

- [MCP Documentation](https://modelcontextprotocol.io)
- [MCP Workflow Guide](./MCP-WORKFLOW.md)
- [Component Update Workflow](./MCP-WORKFLOW.md)

---

**Questions?** Check the memories stored in Windsurf or refer to `MCP-WORKFLOW.md`.
