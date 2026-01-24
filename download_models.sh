#!/bin/bash

# ============================================================================
# OPSEC Validator Demo - Model Download Script
# Rocky Mountain CyberSpace Symposium 2026
# ============================================================================

echo "======================================"
echo "🛡️  OPSEC Validator - Model Download"
echo "======================================"
echo ""

# Configuration
MODEL_DIR="models"
MODEL_NAME="Trendyol-Cybersecurity-LLM-Qwen3-32B"

# Choose quantization - Q4_K_M for balance of size/quality, Q8_0 for maximum quality
# Q4_K_M: ~19.8GB - recommended for most demos
# Q8_0: ~34.8GB - maximum quality

QUANT="Q4_K_M"
# QUANT="Q8_0"

# Create models directory
mkdir -p "$MODEL_DIR"

echo "Model: $MODEL_NAME"
echo "Quantization: $QUANT"
echo "Download directory: $MODEL_DIR"
echo ""

# Install huggingface_hub if needed
echo "Ensuring huggingface_hub is installed..."
pip install huggingface_hub hf_transfer --quiet

# Enable faster downloads
export HF_HUB_ENABLE_HF_TRANSFER=1

echo "Downloading model from HuggingFace..."
echo ""

if [ "$QUANT" = "Q4_K_M" ]; then
    # Download Q4_K_M from mradermacher's quantizations
    echo "Downloading Q4_K_M quantization (~19.8GB)..."
    python3 -c "
from huggingface_hub import hf_hub_download
hf_hub_download(
    repo_id='mradermacher/Trendyol-Cybersecurity-LLM-Qwen3-32B-Q8_0-GGUF-GGUF',
    filename='Trendyol-Cybersecurity-LLM-Qwen3-32B-Q8_0-GGUF.Q4_K_M.gguf',
    local_dir='$MODEL_DIR',
    local_dir_use_symlinks=False
)
print('Download complete!')
"
    
    # Rename for consistency
    if [ -f "$MODEL_DIR/Trendyol-Cybersecurity-LLM-Qwen3-32B-Q8_0-GGUF.Q4_K_M.gguf" ]; then
        mv "$MODEL_DIR/Trendyol-Cybersecurity-LLM-Qwen3-32B-Q8_0-GGUF.Q4_K_M.gguf" \
           "$MODEL_DIR/Trendyol-Cybersecurity-LLM-Qwen3-32B-Q4_K_M.gguf"
    fi
else
    # Download Q8_0 from official Trendyol repo
    echo "Downloading Q8_0 quantization (~34.8GB)..."
    python3 -c "
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id='Trendyol/Trendyol-Cybersecurity-LLM-Qwen3-32B-Q8_0-GGUF',
    local_dir='$MODEL_DIR',
    local_dir_use_symlinks=False
)
print('Download complete!')
"
fi

echo ""
echo "======================================"

# Verify download
if [ -f "$MODEL_DIR/Trendyol-Cybersecurity-LLM-Qwen3-32B-$QUANT.gguf" ] || \
   [ -f "$MODEL_DIR/trendyol-cybersecurity-llm-qwen3-32b-q8_0.gguf" ]; then
    echo "✅ Model downloaded successfully!"
    echo ""
    echo "Model location:"
    ls -lh "$MODEL_DIR"/*.gguf 2>/dev/null || ls -lh "$MODEL_DIR"
else
    echo "⚠️  Download may have failed. Please check the models directory."
    echo ""
    echo "Alternative: Download manually from:"
    echo "  https://huggingface.co/Trendyol/Trendyol-Cybersecurity-LLM-Qwen3-32B-Q8_0-GGUF"
    echo "  https://huggingface.co/mradermacher/Trendyol-Cybersecurity-LLM-Qwen3-32B-Q8_0-GGUF-GGUF"
fi

echo ""
echo "======================================"
echo "Next steps:"
echo "  1. Run: ./install.sh"
echo "  2. Run: ./start_demo_remote.sh"
echo "======================================"