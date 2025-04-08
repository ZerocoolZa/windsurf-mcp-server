#!/bin/bash

# Set environment variables
export PYTHONPATH="/Users/wws/pdf-ollama/CascadeProjects/windsurf-project/AI_GUI_PYQT6/M K Tender System/Cascade_Tools"
export MEMORY_PLUGIN_TOKEN="windsurf_mcp_token_2025"

# Terminate existing servers
pkill -f "python /Users/wws/.codeium/windsurf/windsurf_mcp_server.py"
pkill -f "npx @memoryplugin/mcp-server"

# Start Python MCP Server
python /Users/wws/.codeium/windsurf/windsurf_mcp_server.py &
sleep 2

# Start Memory Plugin MCP Server
npx @memoryplugin/mcp-server &
sleep 2

# Print running processes
echo "MCP Servers started:"
ps aux | grep -E "windsurf_mcp_server.py|mcp-server"
