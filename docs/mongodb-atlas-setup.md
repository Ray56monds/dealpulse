# MongoDB Atlas Setup Guide for DealPulse

## Step 1: Create MongoDB Atlas Account
1. Go to https://cloud.mongodb.com/
2. Sign up for free account or log in
3. Create new project: "DealPulse"

## Step 2: Create Cluster
1. Click "Build a Database"
2. Choose **M0 Sandbox** (Free tier)
3. Cloud Provider: **AWS**
4. Region: **N. Virginia (us-east-1)** 
5. Cluster Name: **dealpulse-cluster**
6. Click "Create"

## Step 3: Database Access (Security)
1. Go to "Database Access" in left sidebar
2. Click "Add New Database User"
3. Authentication Method: **Password**
4. Username: `dealpulse-user`
5. Password: Generate secure password (save it!)
6. Database User Privileges: **Read and write to any database**
7. Click "Add User"

## Step 4: Network Access
1. Go to "Network Access" in left sidebar
2. Click "Add IP Address"
3. Click "Allow Access from Anywhere" (0.0.0.0/0)
4. Comment: "Development access"
5. Click "Confirm"

## Step 5: Get Connection String
1. Go to "Database" in left sidebar
2. Click "Connect" on your cluster
3. Choose "Connect your application"
4. Driver: **Node.js** / Version: **4.1 or later**
5. Copy connection string (looks like):
   ```
   mongodb+srv://dealpulse-user:<password>@dealpulse-cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

## Step 6: Update .env File
1. Copy `.env.example` to `.env`
2. Replace `<password>` with your actual password
3. Add database name to connection string:

```env
MONGODB_URI=mongodb+srv://dealpulse-user:YOUR_PASSWORD@dealpulse-cluster.xxxxx.mongodb.net/dealpulse?retryWrites=true&w=majority
MONGODB_DATABASE=dealpulse
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

## Step 7: Test Connection
Run the setup verification:
```bash
python setup_check.py
```

## Troubleshooting
- **Connection timeout**: Check network access (IP whitelist)
- **Authentication failed**: Verify username/password
- **Database not found**: Database will be created automatically when first document is inserted

## Next Steps
Once MongoDB is connected:
1. Seed sample data: `python seed/seed_data.py`
2. Start MCP server: `cd mcp && npm install && npm start`
3. Test the system: `python agent/main.py`