#!/bin/bash
# Start both backend and frontend development servers

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║ 🚀 STARTING ECHODUO DEVELOPMENT SERVERS                           ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Get the script directory (absolute path)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"

echo "📁 Project root: $PROJECT_ROOT"
echo ""

# Check if venv is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠️  Virtual environment not activated. Activating..."
    if [ -f "$PROJECT_ROOT/venv/bin/activate" ]; then
        source "$PROJECT_ROOT/venv/bin/activate"
        echo "✅ Virtual environment activated"
    else
        echo "❌ Virtual environment not found at $PROJECT_ROOT/venv"
        echo "   Please run: python3 -m venv venv"
        exit 1
    fi
fi

# Check if backend directory exists
if [ ! -d "$PROJECT_ROOT/backend" ]; then
    echo "❌ Backend directory not found at: $PROJECT_ROOT/backend"
    exit 1
fi

# Check if frontend directory exists
if [ ! -d "$PROJECT_ROOT/frontend" ]; then
    echo "❌ Frontend directory not found at: $PROJECT_ROOT/frontend"
    exit 1
fi

# Start backend in background
echo "🔧 Starting Backend API (Flask) on http://localhost:5000..."
cd "$PROJECT_ROOT/backend" || exit 1
python api.py > "$PROJECT_ROOT/backend.log" 2>&1 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"
echo "   Logs: $PROJECT_ROOT/backend.log"
echo ""

# Wait a bit for backend to start
sleep 3

# Check if backend is running
if curl -s http://localhost:5000/health > /dev/null 2>&1; then
    echo "✅ Backend is running!"
else
    echo "⚠️  Backend might not be ready yet. Check logs: tail -f $PROJECT_ROOT/backend.log"
fi
echo ""

# Start frontend
echo "🎨 Starting Frontend (Vite) on http://localhost:5173..."
cd "$PROJECT_ROOT/frontend" || exit 1
npm run dev > "$PROJECT_ROOT/frontend.log" 2>&1 &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"
echo "   Logs: $PROJECT_ROOT/frontend.log"
echo ""

# Wait a bit for frontend to start
sleep 3

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║ ✅ SERVERS STARTED!                                               ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "📍 URLs:"
echo "   Frontend: http://localhost:5173"
echo "   Backend:  http://localhost:5000"
echo ""
echo "🔍 Health Check:"
echo "   curl http://localhost:5000/health"
echo ""
echo "📊 View Logs:"
echo "   Backend:  tail -f $PROJECT_ROOT/backend.log"
echo "   Frontend: tail -f $PROJECT_ROOT/frontend.log"
echo ""
echo "🛑 To stop servers:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo "   Or: pkill -f 'python.*api.py' && pkill -f 'vite'"
echo ""

# Keep script running
wait
