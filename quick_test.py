print("=== DealPulse Quick Test ===")

# Test 1: Check if .env exists
import os
if os.path.exists('.env'):
    print("✓ .env file exists")
else:
    print("✗ .env file missing")

# Test 2: Check Node.js for MCP server
import subprocess
try:
    result = subprocess.run(['node', '--version'], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✓ Node.js available: {result.stdout.strip()}")
    else:
        print("✗ Node.js not found")
except:
    print("✗ Node.js not found")

# Test 3: Check if we can import basic modules
try:
    from datetime import datetime
    print("✓ Basic Python modules work")
except:
    print("✗ Python module import failed")

print("\n=== Next Steps ===")
print("1. Set up MongoDB Atlas (5 minutes)")
print("2. Update .env with real connection string")
print("3. Install MCP dependencies: cd mcp && npm install")
print("4. Test the system")

print("\nFor MongoDB Atlas:")
print("- Go to https://cloud.mongodb.com")
print("- Create free M0 cluster")
print("- Get connection string")
print("- Update MONGODB_URI in .env file")