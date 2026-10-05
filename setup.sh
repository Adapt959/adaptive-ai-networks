#!/bin/bash
# Adaptive AI Command Center - one-command setup (Mac / Linux)
# Run:  curl -fsSL https://raw.githubusercontent.com/Adapt959/adaptive-ai-networks/main/setup.sh | bash
set -e
echo "=== Adaptive AI Command Center setup ==="

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 was not found. Install it from https://www.python.org/downloads/ then run this again."
  exit 1
fi

cd "$HOME"
if [ -d "adaptive-ai-command-center" ]; then
  echo "Removing old copy..."
  rm -rf adaptive-ai-command-center
fi
echo "Downloading the app..."
curl -fsSL -o cc.zip https://github.com/Adapt959/adaptive-ai-networks/archive/refs/heads/main.zip
unzip -q -o cc.zip
mv adaptive-ai-networks-main adaptive-ai-command-center
rm cc.zip
cd adaptive-ai-command-center

echo "Installing dependencies (a minute or two)..."
python3 -m venv .venv
./.venv/bin/pip install -q -r requirements.txt

if ! curl -sf --max-time 5 http://127.0.0.1:11434/api/version >/dev/null 2>&1; then
  echo "Starting Ollama in the background..."
  (ollama serve >/dev/null 2>&1 &)
  sleep 3
fi
if ! ollama list 2>/dev/null | grep -q "llama3.1"; then
  echo "Downloading the llama3.1 model (a few minutes, one time only)..."
  ollama pull llama3.1
fi

echo ""
echo "Starting the server. Open http://127.0.0.1:8001/docs in your browser to use it."
echo "Keep this window open. Press Ctrl+C to stop the server."
./.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8001
