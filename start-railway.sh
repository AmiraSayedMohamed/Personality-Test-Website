#!/bin/bash
echo "Starting Railway deployment..."
python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
