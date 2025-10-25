# GTM Labs MCP Server

> Access your GTM Labs component library via Model Context Protocol

Transform your GTM Labs website into a reusable component library accessible through AI assistants like Claude, Windsurf, and any MCP-compatible tool.

---

## 🎯 What This Does

The GTM Labs MCP Server exposes your website components, layouts, and design system through the Model Context Protocol, allowing you to:

✅ **Access any component** instantly via natural language  
✅ **Get full blueprints** with code, dependencies, and specs  
✅ **Search components** by name, content, or properties  
✅ **Extract design specs** (colors, animations, borders, etc.)  
✅ **Create project scaffolds** with your components  
✅ **Version control** - access any historical version via Git

---

## 🚀 Quick Install

### One-Line Install (Coming Soon)

```bash
curl -fsSL https://raw.githubusercontent.com/gtm-labs/mcp-server/main/install.sh | bash
```

### Manual Install

```bash
# 1. Install Python 3.10+ (if needed)
brew install python@3.11  # macOS
# or
sudo apt install python3.11  # Linux

# 2. Install MCP SDK
pip3.11 install 'mcp[cli]'

# 3. Download and install server
mkdir -p ~/.mcp-servers/gtm-labs
curl -o ~/.mcp-servers/gtm-labs/server.py \
  https://raw.githubusercontent.com/gtm-labs/mcp-server/main/gtm-labs-mcp-portable.py
chmod +x ~/.mcp-servers/gtm-labs/server.py

# 4. Configure project path
mkdir -p ~/.gtm-labs-mcp
cat > ~/.gtm-labs-mcp/config.json << EOF
{
  "project_root": "/path/to/your/gtm-labs-project"
}
EOF

# 5. Configure your IDE (see below)
```

---

## ⚙️ IDE Configuration

### Windsurf

Create `.windsurf/mcp_config.json`:

```json
{
  "gtm-labs": {
    "command": "python3.11",
    "args": ["/Users/YOUR_USERNAME/.mcp-servers/gtm-labs/server.py"]
  }
}
```

Restart Windsurf.

### Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "gtm-labs": {
      "command": "python3.11",
      "args": ["/Users/YOUR_USERNAME/.mcp-servers/gtm-labs/server.py"]
    }
  }
}
```

Restart Claude Desktop.

### Other MCP-Compatible Tools

Follow your tool's MCP configuration guide using:
- **Command:** `python3.11`
- **Args:** `["/path/to/.mcp-servers/gtm-labs/server.py"]`

---

## 🧪 Testing

Once installed, try these commands in your AI assistant:

```
Use GTM Labs MCP to list all components
Use GTM Labs MCP to get the how-we-help-section component
Use GTM Labs MCP to show me the design tokens
Use GTM Labs MCP to search for animation components
```

Expected: JSON responses with component code, specs, and metadata.

---

## 📚 Available Tools

### 1. `list_components`
List all components, optionally filtered by category.

**Example:**
```
List all section components using GTM Labs MCP
```

### 2. `get_component`
Get a component with full blueprint (code, dependencies, specs).

**Example:**
```
Get the hero-section component with all dependencies
```

### 3. `get_component_specs`
Get detailed specifications (colors, animations, borders, spacing, fonts).

**Example:**
```
Show me the color specs for hero-section
```

### 4. `search_components`
Search components by name, content, or properties.

**Example:**
```
Search for components with animation effects
```

### 5. `get_changelog`
Get version history for a component or entire project.

**Example:**
```
Show changelog for hero-section
```

### 6. `create_scaffold`
Create a project scaffold with selected components.

**Example:**
```
Create a Next.js scaffold with hero and navbar at ./new-project
```

---

## 🎨 What's Available

### Components (50+)
- **Sections:** hero, how-we-help, how-it-works, content-library
- **UI:** buttons, cards, inputs, banners, tooltips
- **Animations:** Custom animation components
- **Cosmic:** Custom design system (15+ components)
- **MagicUI:** Magic effects library (8+ components)
- **Experiments:** Bento grids, experimental layouts

### Configuration
- Tailwind config (270 lines, custom animations)
- Design tokens (256 lines, complete design system)
- Next.js config
- Package.json with all dependencies

### Utilities
- Helper functions
- Design system tokens
- Brand constants

---

## 🔐 Security

The MCP automatically:
- **Excludes:** `.env*`, `*secrets*`, `*private*`, internal docs
- **Redacts:** API keys, CRM tool names, credentials
- **Only exposes:** Public-facing code (components, configs, utilities)

---

## 📖 Documentation

- **[Component Catalog](./COMPONENT-CATALOG.md)** - Browse all components
- **[Full Documentation](./MCP-README.md)** - Complete API reference
- **[Workflow Guide](./MCP-WORKFLOW.md)** - Version control workflow
- **[Distribution Guide](./DISTRIBUTION-GUIDE.md)** - How to distribute

---

## 🛠️ Configuration

### Project Path

The MCP needs to know where your GTM Labs project is located.

**Config file:** `~/.gtm-labs-mcp/config.json`

```json
{
  "project_root": "/Users/yourname/projects/gtm-homepage"
}
```

Update this path to point to your GTM Labs project directory.

---

## 💡 Use Cases

### 1. Quick Component Reuse
```
Get the how-we-help-section component with all dependencies
```
→ Instant access to component code, styles, and dependencies

### 2. Create New Project
```
Create a Next.js scaffold with hero, navbar, and footer at ./my-new-project
```
→ Full project skeleton with your components

### 3. Extract Specific Styles
```
What colors does the cosmic-card component use?
```
→ Exact Tailwind classes and color values

### 4. Version Control
```
Get hero-section from version v1.0.0
```
→ Access any historical version

---

## 🐛 Troubleshooting

### MCP Not Loading

1. Check Python version: `python3.11 --version` (must be 3.10+)
2. Check MCP installed: `pip3.11 show mcp`
3. Verify config path: `cat ~/.gtm-labs-mcp/config.json`
4. Test server: `python3.11 ~/.mcp-servers/gtm-labs/server.py` (Ctrl+C to stop)
5. Restart your IDE completely

### Component Not Found

- Verify project path in `~/.gtm-labs-mcp/config.json`
- Check component exists: `ls /path/to/project/homepage/components/ui/`
- Use exact component name (kebab-case): `hero-section`, not `HeroSection`

### Python Version Error

```
ERROR: Package 'mcp' requires a different Python: 3.9.6 not in '>=3.10'
```

**Solution:** Install Python 3.11+
```bash
brew install python@3.11  # macOS
sudo apt install python3.11  # Linux
```

---

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

MIT License - see [LICENSE](./LICENSE) file

---

## 🔗 Links

- **GitHub:** https://github.com/gtm-labs/mcp-server
- **Documentation:** https://github.com/gtm-labs/mcp-server/wiki
- **Issues:** https://github.com/gtm-labs/mcp-server/issues
- **MCP Protocol:** https://modelcontextprotocol.io

---

## 🎉 Credits

Built by GTM Labs for the MCP community.

Powered by:
- [Model Context Protocol](https://modelcontextprotocol.io)
- [Next.js](https://nextjs.org)
- [Tailwind CSS](https://tailwindcss.com)
- [Framer Motion](https://www.framer.com/motion)

---

**Questions?** Open an issue on GitHub or check the [documentation](./MCP-README.md).
