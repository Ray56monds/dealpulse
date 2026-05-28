import subprocess
import sys
import time

print("Starting DealPulse Streamlit Demo...")
print("This will open in your browser at http://localhost:8501")
print("Press Ctrl+C to stop the server")

try:
    # Start Streamlit
    process = subprocess.Popen([
        sys.executable, "-m", "streamlit", "run", "frontend/app.py",
        "--server.headless", "true",
        "--server.port", "8501"
    ])
    
    print("Streamlit server starting...")
    time.sleep(3)
    print("Demo should be available at: http://localhost:8501")
    
    # Keep running
    process.wait()
    
except KeyboardInterrupt:
    print("\nStopping Streamlit server...")
    process.terminate()
except Exception as e:
    print(f"Error starting Streamlit: {e}")