#!/bin/bash

# GTM Labs MCP - Public Installation Script (GitHub API Version)
# This script installs the GTM Labs MCP server
# Components are fetched directly from GitHub - no git clone needed!

set -e

echo "🚀 Installing GTM Labs MCP Server (GitHub API Version)..."
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

# Install requests library (for GitHub API)
echo "📦 Installing requests library..."
$PIP_CMD install requests --quiet

if [ $? -eq 0 ]; then
    echo "✅ requests installed"
else
    echo "❌ Failed to install requests"
    exit 1
fi

# Create directories
echo ""
echo "📁 Setting up directories..."
mkdir -p ~/.mcp-servers/gtm-labs

# Download the server
echo ""
echo "⬇️  Downloading GTM Labs MCP server..."

# Download from GitHub
curl -fsSL https://raw.githubusercontent.com/GTM-LABS-io/mcp-server/main/server-github.py \
  -o ~/.mcp-servers/gtm-labs/server.py

if [ $? -eq 0 ]; then
    chmod +x ~/.mcp-servers/gtm-labs/server.py
    echo "✅ Server installed"
else
    echo "❌ Failed to download server"
    echo "Visit: https://github.com/GTM-LABS-io/mcp-server"
    exit 1
fi

# Optional: Create config for GitHub token (for higher rate limits)
echo ""
echo "⚙️  Optional: GitHub Token Configuration"
echo ""
echo "The MCP fetches components from GitHub's API."
echo "Without a token: 60 requests/hour"
echo "With a token: 5,000 requests/hour"
echo ""
read -p "Do you want to add a GitHub token? (y/N): " ADD_TOKEN

if [[ "$ADD_TOKEN" =~ ^[Yy]$ ]]; then
    echo ""
    echo "Create a token at: https://github.com/settings/tokens"
    echo "No special permissions needed (public repo access only)"
    echo ""
    read -p "Enter your GitHub token: " GITHUB_TOKEN
    
    mkdir -p ~/.gtm-labs-mcp
    cat > ~/.gtm-labs-mcp/config.json << EOF
{
  "github_token": "$GITHUB_TOKEN"
}
EOF
    echo "✅ Token saved to ~/.gtm-labs-mcp/config.json"
else
    echo "⏭️  Skipping token configuration (you can add it later)"
fi

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
