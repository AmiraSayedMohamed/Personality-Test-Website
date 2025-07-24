#!/usr/bin/env bash
# Railway startup script

echo "🚀 Starting Personality Test Application on Railway..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements_irt.txt

# Start the FastAPI server
echo "🌐 Starting FastAPI server..."
python simple_backend.py
