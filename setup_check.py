import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_mongodb_connection():
    """Test MongoDB connection"""
    try:
        from pymongo import MongoClient
        
        mongodb_uri = os.getenv('MONGODB_URI')
        if not mongodb_uri:
            print("MONGODB_URI not found in .env file")
            print("Please set up MongoDB Atlas and update .env file")
            return False
            
        print("Testing MongoDB connection...")
        client = MongoClient(mongodb_uri)
        
        # Test connection
        client.admin.command('ping')
        print("MongoDB connection successful!")
        
        # Check database
        db_name = os.getenv('MONGODB_DATABASE', 'dealpulse')
        db = client[db_name]
        
        # Check collections
        collections = db.list_collection_names()
        print(f"Database: {db_name}")
        print(f"Collections: {collections}")
        
        return True
        
    except Exception as e:
        print(f"MongoDB connection failed: {str(e)}")
        print("\nPlease check:")
        print("1. MongoDB Atlas cluster is running")
        print("2. IP address is whitelisted (0.0.0.0/0 for testing)")
        print("3. Database user has correct permissions")
        print("4. Connection string is correct in .env file")
        return False

def setup_environment():
    """Check if environment is properly configured"""
    print("Checking environment setup...")
    
    # Check .env file
    if not os.path.exists('.env'):
        print(".env file not found")
        print("Please copy .env.example to .env and configure your credentials")
        return False
    
    # Check required environment variables
    required_vars = ['MONGODB_URI', 'MONGODB_DATABASE']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"Missing environment variables: {missing_vars}")
        return False
    
    print("Environment configuration looks good!")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("Installing Python dependencies...")
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Python dependencies installed successfully!")
            return True
        else:
            print(f"Failed to install dependencies: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Error installing dependencies: {str(e)}")
        return False

def main():
    print("DealPulse Setup Verification")
    print("=" * 40)
    
    # Step 1: Check environment
    if not setup_environment():
        return
    
    # Step 2: Install dependencies
    if not install_dependencies():
        return
    
    # Step 3: Test MongoDB connection
    if not check_mongodb_connection():
        return
    
    print("\nSetup verification complete!")
    print("\nNext steps:")
    print("1. Run: py seed/seed_data.py")
    print("2. Start MCP server: cd mcp && npm install && npm start")
    print("3. Test agent: py agent/main.py")
    print("4. Launch demo: streamlit run frontend/app.py")

if __name__ == "__main__":
    main()