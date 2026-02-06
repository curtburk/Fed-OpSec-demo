#!/bin/bash

# ============================================================================
# OPSEC Validator Demo - Installation Script
# Rocky Mountain CyberSpace Symposium 2026
# HP ZGX Nano AI Station (GB10 Blackwell)
# ============================================================================

echo "======================================"
echo "🛡️  OPSEC Validator Demo Installer"
echo "======================================"
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed."
    echo "Please install with: sudo apt-get install python3 python3-pip python3-venv"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1)
echo "✓ Python found: $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
VENV_NAME="opsec-venv"

if [ ! -d "$VENV_NAME" ]; then
    echo ""
    echo "Creating virtual environment: $VENV_NAME"
    python3 -m venv "$VENV_NAME"
    echo "✓ Virtual environment created"
else
    echo "✓ Found existing virtual environment: $VENV_NAME"
fi

# Activate virtual environment
source "$VENV_NAME/bin/activate"

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install PyTorch with CUDA support
echo ""
echo "Installing PyTorch with CUDA support..."
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu130

# Install backend dependencies (except llama-cpp-python)
echo ""
echo "Installing backend dependencies..."
pip install fastapi uvicorn pydantic python-multipart python-dotenv

# ============================================================================
# CUDA 13 / GB10 Blackwell Configuration
# ============================================================================
echo ""
echo "======================================"
echo "🔧 Configuring for GB10 Blackwell GPU"
echo "======================================"

# Check for CUDA 13
CUDA13_NVCC="/usr/local/cuda-13.0/bin/nvcc"
if [ -f "$CUDA13_NVCC" ]; then
    echo "✓ Found CUDA 13 compiler: $CUDA13_NVCC"
    
    echo ""
    echo "Installing llama-cpp-python with CUDA 13 support..."
    echo "This may take several minutes to compile..."
    echo ""
    
    # Build llama-cpp-python with correct CUDA 13 compiler for Blackwell
    CMAKE_ARGS="-DGGML_CUDA=on -DCMAKE_CUDA_COMPILER=$CUDA13_NVCC -DCMAKE_CUDA_ARCHITECTURES=120" \
        pip install llama-cpp-python --no-cache-dir --force-reinstall
    
    if [ $? -eq 0 ]; then
        echo "✓ llama-cpp-python installed with CUDA 13 / Blackwell support"
    else
        echo "❌ Failed to build llama-cpp-python with CUDA support"
        echo "Falling back to CPU-only version..."
        pip install llama-cpp-python
    fi
else
    echo "⚠️  CUDA 13 not found at $CUDA13_NVCC"
    echo "Checking for other CUDA installations..."
    
    # Try to find any CUDA installation
    if [ -d "/usr/local/cuda" ]; then
        CUDA_NVCC="/usr/local/cuda/bin/nvcc"
        if [ -f "$CUDA_NVCC" ]; then
            CUDA_VERSION=$($CUDA_NVCC --version | grep "release" | sed 's/.*release //' | sed 's/,.*//')
            echo "Found CUDA $CUDA_VERSION at $CUDA_NVCC"
            
            CMAKE_ARGS="-DGGML_CUDA=on -DCMAKE_CUDA_COMPILER=$CUDA_NVCC" \
                pip install llama-cpp-python --no-cache-dir --force-reinstall
        fi
    else
        echo "No CUDA found. Installing CPU-only version..."
        pip install llama-cpp-python
    fi
fi

# Verify llama-cpp-python installation
echo ""
echo "Verifying llama-cpp-python installation..."
if python3 -c "from llama_cpp import Llama; print('✓ llama-cpp-python OK')" 2>/dev/null; then
    echo "✓ llama-cpp-python installed successfully"
else
    echo "❌ llama-cpp-python installation failed"
    exit 1
fi

# ============================================================================
# Model Configuration
# ============================================================================
echo ""
echo "======================================"
echo "📁 Model Configuration"
echo "======================================"
echo ""

# Detect model file
MODEL_DIR="models"
MODEL_FILE=""

if [ -f "$MODEL_DIR/Trendyol-Cybersecurity-LLM-Qwen3-32B-Q4_K_M.gguf" ]; then
    MODEL_FILE="$MODEL_DIR/Trendyol-Cybersecurity-LLM-Qwen3-32B-Q4_K_M.gguf"
elif [ -f "$MODEL_DIR/trendyol-cybersecurity-llm-qwen3-32b-q8_0.gguf" ]; then
    MODEL_FILE="$MODEL_DIR/trendyol-cybersecurity-llm-qwen3-32b-q8_0.gguf"
fi

if [ -n "$MODEL_FILE" ]; then
    echo "✓ Found model: $MODEL_FILE"
    
    # Create .env file for model path
    FULL_PATH=$(realpath "$MODEL_FILE")
    echo "OPSEC_MODEL_PATH=$FULL_PATH" > .env
    echo "✓ Created .env with model path"
else
    echo "⚠️  No model file found in $MODEL_DIR/"
    echo ""
    echo "Please run ./download_models.sh first, or manually place the model file:"
    echo "  - Trendyol-Cybersecurity-LLM-Qwen3-32B-Q4_K_M.gguf (~19.8GB)"
    echo "  - or Q8_0 variant (~34.8GB)"
fi

echo ""
echo "======================================"
echo "✅ Installation Complete!"
echo "======================================"
echo ""
echo "To start the demo:"
echo "  ./start_demo_remote.sh"
echo ""
echo "Or manually:"
echo "  source $VENV_NAME/bin/activate"
echo "  cd backend && python3 main.py"
echo ""
echo "Then access from your Windows laptop:"
echo "  http://YOUR_SERVER_IP:8080"
echo ""
