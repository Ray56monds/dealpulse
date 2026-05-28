#!/bin/bash

# DealPulse Deployment Script

echo "🚀 Setting up DealPulse Agent..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please copy .env.example to .env and configure your credentials."
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install Node.js dependencies for MCP server
echo "📦 Installing MCP server dependencies..."
cd mcp
npm install
cd ..

# Seed MongoDB with sample data
echo "🌱 Seeding MongoDB with sample data..."
python seed/seed_data.py

# Start MCP server in background
echo "🔧 Starting MongoDB MCP server..."
cd mcp
npm start &
MCP_PID=$!
cd ..

echo "✅ MCP server started (PID: $MCP_PID)"

# Test the agent
echo "🧪 Testing DealPulse agent..."
python agent/main.py

echo "🎉 DealPulse setup complete!"
echo ""
echo "Next steps:"
echo "1. Configure Google Cloud Agent Builder with MCP endpoint"
echo "2. Test agent queries in Agent Builder console"
echo "3. Run demo UI: streamlit run frontend/app.py"
echo ""
echo "To stop MCP server: kill $MCP_PID"