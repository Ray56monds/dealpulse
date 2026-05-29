# Railway Deployment for DealPulse

## Quick Deploy to Railway

1. **Connect GitHub**: https://railway.app/new
2. **Select Repository**: Ray56monds/dealpulse
3. **Environment Variables**:
   ```
   MONGODB_URI=<your-mongodb-connection-string>
   MONGODB_DATABASE=dealpulse
   ```
4. **Start Command**: `streamlit run frontend/app_enhanced.py --server.port $PORT --server.address 0.0.0.0`

## Alternative: Render Deployment

1. **Connect GitHub**: https://render.com/
2. **New Web Service** from GitHub repo
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `streamlit run frontend/app_enhanced.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`

## Environment Variables for Both:
- MONGODB_URI (your connection string from MongoDB Atlas)
- MONGODB_DATABASE=dealpulse

## Expected Result:
- Live demo URL for hackathon submission
- Working MongoDB integration
- Interactive financial services dashboard