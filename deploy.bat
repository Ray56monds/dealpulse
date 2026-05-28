@echo off
echo 🚀 Setting up DealPulse Agent...

REM Check if .env exists
if not exist .env (
    echo ❌ .env file not found. Please copy .env.example to .env and configure your credentials.
    exit /b 1
)

REM Install Python dependencies
echo 📦 Installing Python dependencies...
pip install -r requirements.txt

REM Install Node.js dependencies for MCP server
echo 📦 Installing MCP server dependencies...
cd mcp
npm install
cd ..

REM Seed MongoDB with sample data
echo 🌱 Seeding MongoDB with sample data...
python seed/seed_data.py

REM Start MCP server
echo 🔧 Starting MongoDB MCP server...
start /b cmd /c "cd mcp && npm start"

REM Test the agent
echo 🧪 Testing DealPulse agent...
python agent/main.py

echo 🎉 DealPulse setup complete!
echo.
echo Next steps:
echo 1. Configure Google Cloud Agent Builder with MCP endpoint
echo 2. Test agent queries in Agent Builder console  
echo 3. Run demo UI: streamlit run frontend/app.py
echo.
pause