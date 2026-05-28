# MongoDB Atlas Setup for DealPulse

## 1. Create MongoDB Atlas Account
- Go to https://cloud.mongodb.com/
- Sign up for free tier
- Create new project: "DealPulse"

## 2. Create Cluster
- Choose M0 Sandbox (free tier)
- Region: AWS / us-east-1
- Cluster name: "dealpulse-cluster"

## 3. Database Access
- Create database user:
  - Username: dealpulse-user
  - Password: [generate secure password]
  - Role: Read and write to any database

## 4. Network Access
- Add IP Address: 0.0.0.0/0 (allow from anywhere for development)
- For production: restrict to specific IPs

## 5. Get Connection String
- Click "Connect" on cluster
- Choose "Connect your application"
- Copy connection string format:
  mongodb+srv://dealpulse-user:<password>@dealpulse-cluster.xxxxx.mongodb.net/dealpulse

## 6. Update .env file
MONGODB_URI=mongodb+srv://dealpulse-user:<your-password>@dealpulse-cluster.xxxxx.mongodb.net/dealpulse
MONGODB_DATABASE=dealpulse