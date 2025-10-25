#!/bin/bash

# GTM Labs MCP - Public Installation Script
# This script installs the GTM Labs MCP server for anyone

set -e

echo "🚀 Installing GTM Labs MCP Server..."
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

echo "Current Python: $PYTHON_VERSION"

if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 10 ]); then
    echo "❌ Python 3.10+ required (you have $PYTHON_VERSION)"
    echo ""
    echo "Install Python 3.11:"
    echo "  macOS: brew install python@3.11"
    echo "  Linux: sudo apt install python3.11"
    exit 1
fi

echo "✅ Python version OK"
echo ""

# Determine Python command
if command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
    PIP_CMD="pip3.11"
elif command -v python3.10 &> /dev/null; then
    PYTHON_CMD="python3.10"
    PIP_CMD="pip3.10"
else
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
fi

echo "Using: $PYTHON_CMD"
echo ""

# Install MCP SDK
echo "📦 Installing MCP SDK..."
$PIP_CMD install 'mcp[cli]' --quiet || $PIP_CMD install mcp --quiet

if [ $? -eq 0 ]; then
    echo "✅ MCP SDK installed"
else
    echo "❌ Failed to install MCP SDK"
    exit 1
fi

# Create directories
echo ""
echo "📁 Setting up directories..."
mkdir -p ~/.mcp-servers/gtm-labs
mkdir -p ~/.gtm-labs-mcp

# Download the server (replace with actual URL when published)
echo ""
echo "⬇️  Downloading GTM Labs MCP server..."

# For now, copy from local (replace with curl when published)
if [ -f "gtm-labs-mcp-portable.py" ]; then
    cp gtm-labs-mcp-portable.py ~/.mcp-servers/gtm-labs/server.py
    chmod +x ~/.mcp-servers/gtm-labs/server.py
    echo "✅ Server installed"
else
    echo "❌ Server file not found"
    echo "Download manually from: https://github.com/gtm-labs/mcp-server"
    exit 1
fi

# Create config
echo ""
echo "⚙️  Configuration needed..."
echo ""
echo "Where is your GTM Labs project located?"
echo "Example: /Users/yourname/projects/gtm-homepage"
read -p "Project path: " PROJECT_PATH

if [ ! -d "$PROJECT_PATH" ]; then
    echo "⚠️  Warning: Directory not found: $PROJECT_PATH"
    echo "You can update this later in ~/.gtm-labs-mcp/config.json"
fi

cat > ~/.gtm-labs-mcp/config.json << EOF
{
  "project_root": "$PROJECT_PATH"
}
EOF

echo "✅ Config saved to ~/.gtm-labs-mcp/config.json"

# Detect IDE and configure
echo ""
echo "🔧 Configuring IDE..."

# Windsurf
if [ -d "$HOME/.config/windsurf" ] || [ -d "$HOME/Library/Application Support/Windsurf" ]; then
    echo "Detected: Windsurf"
    
    # Try both possible config locations
    for CONFIG_DIR in "$HOME/.config/windsurf" "$HOME/.windsurf"; do
        mkdir -p "$CONFIG_DIR"
        
        cat > "$CONFIG_DIR/mcp_config.json" << EOF
{
  "gtm-labs": {
    "command": "$PYTHON_CMD",
    "args": ["$HOME/.mcp-servers/gtm-labs/server.py"]
  }
}
EOF
        echo "✅ Windsurf config: $CONFIG_DIR/mcp_config.json"
    done
fi

# Claude Desktop
if [ -d "$HOME/Library/Application Support/Claude" ]; then
    echo "Detected: Claude Desktop"
    
    CONFIG_FILE="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
    
    if [ -f "$CONFIG_FILE" ]; then
        # Backup existing config
        cp "$CONFIG_FILE" "$CONFIG_FILE.backup"
    fi
    
    cat > "$CONFIG_FILE" << EOF
{
  "mcpServers": {
    "gtm-labs": {
      "command": "$PYTHON_CMD",
      "args": ["$HOME/.mcp-servers/gtm-labs/server.py"]
    }
  }
}
EOF
    echo "✅ Claude Desktop config updated"
fi

# Test the server
echo ""
echo "🧪 Testing server..."
$PYTHON_CMD ~/.mcp-servers/gtm-labs/server.py &
SERVER_PID=$!
sleep 2
kill $SERVER_PID 2>/dev/null || true

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ GTM Labs MCP Server Installed! ✨"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 Next Steps:"
echo "1. Restart your IDE (Windsurf, Claude Desktop, etc.)"
echo "2. Test with: 'Use GTM Labs MCP to list components'"
echo ""
echo "📖 Documentation:"
echo "   https://github.com/gtm-labs/mcp-server"
echo ""
echo "⚙️  Config file: ~/.gtm-labs-mcp/config.json"
echo "📁 Server location: ~/.mcp-servers/gtm-labs/server.py"
echo ""
