#!/bin/bash

# Railway Deployment Script
echo "🚀 Deploying Personality Test to Railway..."

# Check if railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Login to Railway (if not already logged in)
echo "🔐 Logging into Railway..."
railway login

# Deploy the project
echo "📤 Starting deployment..."
railway deploy

echo "✅ Deployment completed!"
echo "🌐 Your app should be available at your Railway project URL"
echo "🔧 Admin Dashboard: https://your-app.railway.app/admin.html"
echo "👤 Admin Login: admin / admin123"
