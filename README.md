# 🛡️ OPSEC Validator Demo

**AI-Powered Operations Security Analysis for Military Communications**

> Rocky Mountain CyberSpace Symposium 2026  
> "Dominance Through Disruption: Emerging Tech and the Cyber Enterprise"

---

## Overview

This demo showcases how **prompt engineering** dramatically improves AI detection of OPSEC (Operations Security) violations in military communications. Using the same cybersecurity-tuned model, we compare:

1. **Generic Prompt** — Basic "find sensitive information" approach
2. **OPSEC-Specific Prompt** — Military doctrine-aligned detection with DoD categories

The result: Domain-specific prompting unlocks significantly better detection capabilities without any model retraining.

---

## Key Value Propositions

### For USAF/USSF Audience

| Capability | Benefit |
|------------|---------|
| **On-Premises Processing** | Sensitive communications never leave your network |
| **Zero Cloud Dependency** | Works in air-gapped environments |
| **No Per-Token Costs** | Unlimited analysis at fixed hardware cost |
| **Military-Specific Detection** | Categories aligned with DoD OPSEC doctrine |
| **Real-Time Analysis** | Screen communications before transmission |

### Demo Story

> "The same AI model can give vastly different results based on how you ask the question. Generic prompts miss military context. OPSEC-specific prompts, aligned with DoD doctrine, catch violations that generic approaches miss entirely."

---

## Hardware Requirements

| Component | Specification |
|-----------|---------------|
| **Platform** | HP ZGX Nano AI Station |
| **GPU** | NVIDIA GB10 Grace Blackwell Superchip |
| **VRAM** | ~120GB Unified Memory |
| **Model Size** | Q4_K_M: ~20GB / Q8_0: ~35GB |

---

## Quick Start

### 1. Download Model

```bash
chmod +x download_models.sh
./download_models.sh
```

This downloads the **Trendyol-Cybersecurity-LLM-Qwen3-32B** model (~20GB for Q4_K_M).

### 2. Install Dependencies

```bash
chmod +x install.sh
./install.sh
```

### 3. Start Demo

```bash
chmod +x start_demo_remote.sh
./start_demo_remote.sh
```

### 4. Access from Windows Laptop

Open browser to: `http://YOUR_SERVER_IP:8080`

---

## OPSEC Categories (DoD Doctrine)

The demo detects violations across six military OPSEC categories:

| Category | Description | Severity |
|----------|-------------|----------|
| **UNIT_ID** | Unit names, call signs, organizational structure | HIGH |
| **LOCATION** | Current positions, coordinates, base names | CRITICAL |
| **TIMING** | Deployment dates, operation schedules | HIGH |
| **CAPABILITIES** | Equipment, weapons systems, personnel strength | CRITICAL |
| **INTENTIONS** | Mission objectives, strategic goals | CRITICAL |
| **VULNERABILITIES** | Weaknesses, supply issues, defensive gaps | HIGH |

---

## Sample Communications

The demo includes realistic (fictional) military communications:

1. **Deployment Email** — Personal email revealing deployment details
2. **Patrol SITREP** — Situation report with location and equipment info
3. **Social Media Post** — Airman posting operational details online
4. **Clean Communication** — Properly sanitized message (no violations)
5. **Logistics Request** — Supply chain email with aggregated intel value

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Windows Laptop (Browser)                  │
│                    http://SERVER_IP:8080                     │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  HP ZGX Nano AI Station                      │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Frontend (Python HTTP Server - Port 8080)          │    │
│  │  - Static HTML/CSS/JS                               │    │
│  │  - Responsive UI                                    │    │
│  └─────────────────────────────────────────────────────┘    │
│                              │                               │
│                              ▼                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Backend API (FastAPI - Port 8000)                  │    │
│  │  - /analyze/compare (side-by-side analysis)         │    │
│  │  - /analyze/generic (baseline)                      │    │
│  │  - /analyze/opsec (military-specific)               │    │
│  │  - /samples (demo texts)                            │    │
│  └─────────────────────────────────────────────────────┘    │
│                              │                               │
│                              ▼                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Trendyol-Cybersecurity-LLM-Qwen3-32B               │    │
│  │  - Cybersecurity fine-tuned                         │    │
│  │  - GGUF format via llama-cpp-python                 │    │
│  │  - GPU-accelerated inference                        │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## Model Details

### Trendyol-Cybersecurity-LLM-Qwen3-32B

| Attribute | Value |
|-----------|-------|
| **Base Model** | Qwen3-32B |
| **Parameters** | 32.76 billion |
| **Training** | ~100 hours on 3×H200 GPUs |
| **Training Data** | ~500GB cybersecurity corpus |
| **Domains** | Incident Response, Threat Hunting, Malware Analysis, Exploit Development, Reverse Engineering |
| **Context Length** | 32,768 tokens |
| **License** | Apache 2.0 |

### Why This Model?

1. **Cybersecurity-Native** — Fine-tuned specifically on security data
2. **Military-Relevant Training** — Includes threat intel, MITRE ATT&CK, incident reports
3. **Qwen3 Architecture** — Latest model with thinking/non-thinking modes
4. **GGUF Available** — Works with llama-cpp-python for local inference

---

## Demo Script (5-minute presentation)

### Opening (30 sec)
> "OPSEC violations in military communications are a persistent threat. AI can help—but only if we ask the right questions."

### Show Generic Analysis (1 min)
1. Load "Deployment Email" sample
2. Run generic analysis
3. Note: Catches some items, but lacks military context

### Show OPSEC Analysis (1 min)  
1. Same text, OPSEC-specific prompt
2. Highlights: Proper categorization, severity levels, actionable recommendations

### Key Comparison (1 min)
> "Same model, same text—dramatically different results. The OPSEC prompt:
> - Uses DoD doctrine categories
> - Provides severity classification
> - Offers specific recommendations
> - Catches context-dependent violations"

### Business Value (1 min)
> "This runs entirely on-premises on the HP ZGX Nano:
> - Zero cloud dependency
> - No per-token costs
> - Full data sovereignty
> - Works in classified environments"

### Close (30 sec)
> "Prompt engineering isn't just about getting better answers—it's about unlocking domain expertise that's already in the model."

---

## Troubleshooting

### Model won't load
```bash
# Check model file exists
ls -la models/

# Check GPU is detected
nvidia-smi

# Try loading manually
cd backend
python3 -c "from llama_cpp import Llama; print('OK')"
```

### API returns 503
- Model may still be loading (32B takes 2-3 minutes)
- Check terminal for loading progress
- Use `/load_model` endpoint to trigger manually

### Frontend can't reach backend
- Check firewall allows ports 8000 and 8080
- Verify SERVER_IP in browser matches actual IP
- Try `curl http://localhost:8000/` from server

---

## File Structure

```
opsec-validator-demo/
├── backend/
│   ├── main.py              # FastAPI application
│   └── requirements.txt     # Python dependencies
├── frontend/
│   └── index.html           # Web interface
├── models/                  # Model files (after download)
├── download_models.sh       # Model download script
├── install.sh               # Installation script
├── start_demo_remote.sh     # Demo startup script
└── README.md                # This file
```

---

## API Reference

### GET /
Health check and status

### GET /load_model
Trigger model loading

### GET /categories
Get OPSEC category definitions

### GET /samples
Get sample military communications

### POST /analyze/compare
Compare generic vs OPSEC analysis

**Request:**
```json
{
  "text": "Communication text to analyze",
  "max_tokens": 2048,
  "temperature": 0.1
}
```

**Response:**
```json
{
  "original_text": "...",
  "generic_result": { ... },
  "opsec_result": { ... },
  "improvement_summary": "..."
}
```

---

## License

- **Demo Code**: MIT License
- **Model**: Apache 2.0 (Trendyol-Cybersecurity-LLM)

---

## Contact

**Curtis Burke**  
HP ZGX Nano Product Manager  
Demo inquiries: [your-email]

---

*Developed for Rocky Mountain CyberSpace Symposium 2026*  
*"Dominance Through Disruption: Emerging Tech and the Cyber Enterprise"*
