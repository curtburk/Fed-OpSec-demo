#!/bin/bash

# ============================================================================
# OPSEC Validator Demo - Remote Access Startup Script
# Rocky Mountain CyberSpace Symposium 2026
# ============================================================================

clear
echo "======================================"
echo "🛡️  OPSEC Validator Demo (Remote Access)"
echo "    Rocky Mountain CyberSpace Symposium"
echo "======================================"
echo ""

# Get server IP
SERVER_IP=$(hostname -I | awk '{print $1}')

echo "Server Information:"
echo "  Hostname/IP: $SERVER_IP"
echo ""

# Kill any existing processes on the ports
echo "Cleaning up old processes..."
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:8080 | xargs kill -9 2>/dev/null
sleep 2

# Activate virtual environment
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ -d "opsec-venv" ]; then
    source opsec-venv/bin/activate
elif [ -d "new-ft-env" ]; then
    source new-ft-env/bin/activate
else
    echo "⚠️  Virtual environment not found. Running without venv."
fi

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | xargs)
fi

# Export performance settings
export TOKENIZERS_PARALLELISM=false
export OMP_NUM_THREADS=8
export CUDA_VISIBLE_DEVICES=0

# Start backend
echo "Starting backend API server..."
cd backend
python3 main.py &
BACKEND_PID=$!
cd ..

# Wait for backend to initialize
echo "Waiting for backend to initialize..."
sleep 5

# Test backend connection
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000 | grep -q "200"; then
    echo "✓ Backend API is running"
else
    echo "⚠️  Backend may not be fully initialized yet"
fi

# Update frontend API URL
echo "Configuring frontend for remote access..."
cd frontend
sed -i "s|const API_URL = .*|const API_URL = 'http://${SERVER_IP}:8000';|" index.html

# Start frontend server
echo "Starting frontend web server..."
python3 -m http.server 8080 --bind 0.0.0.0 &
FRONTEND_PID=$!
cd ..

# Wait for frontend
sleep 2

echo ""
echo "======================================"
echo "✅ Demo is running!"
echo "======================================"
echo ""
echo "Access the demo from your Windows laptop:"
echo "👉 http://${SERVER_IP}:8080"
echo ""
echo "Backend API endpoints:"
echo "  - Status:    http://${SERVER_IP}:8000/"
echo "  - Load:      http://${SERVER_IP}:8000/load_model"
echo "  - Compare:   http://${SERVER_IP}:8000/analyze/compare"
echo "  - Samples:   http://${SERVER_IP}:8000/samples"
echo ""
echo "Demo Flow:"
echo "  1. Open the web interface in your browser"
echo "  2. Model loads automatically on startup"
echo "  3. Select a sample communication (or paste your own)"
echo "  4. Click 'Analyze & Compare' to see both prompts"
echo "  5. Compare Generic vs OPSEC-specific detection"
echo ""
echo "Key Talking Points:"
echo "  • Same cybersecurity-tuned model (Trendyol Qwen3-32B)"
echo "  • Prompt engineering unlocks domain-specific detection"
echo "  • Military OPSEC categories based on DoD doctrine"
echo "  • All processing on-premises - zero cloud dependency"
echo ""
echo "Press Ctrl+C to stop the demo"
echo "======================================"

# Cleanup function
cleanup() {
    echo ""
    echo "Shutting down services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    
    # Restore localhost in frontend
    cd "$SCRIPT_DIR/frontend"
    sed -i "s|const API_URL = .*|const API_URL = 'http://localhost:8000';|" index.html
    
    echo "✓ Demo stopped"
    exit 0
}

# Set trap for cleanup on Ctrl+C
trap cleanup INT

# Keep script running
while true; do
    sleep 1
done
