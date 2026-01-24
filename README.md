# 🛡️ OPSEC Validator Demo

**AI-Powered Operations Security Analysis for Military Communications**

> Rocky Mountain CyberSpace Symposium 2026  
> "Dominance Through Disruption: Emerging Tech and the Cyber Enterprise"

---

## The Problem

Your analysts are already using AI tools for OPSEC review—ChatGPT, Copilot, and other consumer AI services. But these tools:

- **Send sensitive data to the cloud** — Every communication leaves your network
- **Lack military context** — No understanding of DoD OPSEC doctrine
- **Provide inconsistent results** — Generic findings without actionable categorization
- **Cost per query** — Token-based pricing at scale

## The Solution

This demo shows the difference between **consumer AI tools** and a **mission-built OPSEC analyzer** running entirely on-premises.

| Consumer AI Tool | Mission-Built OPSEC Analyzer |
|------------------|------------------------------|
| Cloud-based, data leaves network | On-premises, full data sovereignty |
| Generic "sensitive information" detection | DoD doctrine-aligned categories |
| Unstructured findings | Severity classification + recommendations |
| Per-token costs | Unlimited analysis at fixed hardware cost |
| Requires internet connectivity | Works in air-gapped environments |

---

## Key Value Propositions

### For USAF/USSF Audience

| Capability | Benefit |
|------------|---------|
| **On-Premises Processing** | Sensitive communications never leave your network |
| **Zero Cloud Dependency** | Works in classified/air-gapped environments |
| **No Per-Token Costs** | Unlimited analysis at fixed hardware cost |
| **DoD OPSEC Categories** | UNIT_ID, LOCATION, TIMING, CAPABILITIES, INTENTIONS, VULNERABILITIES |
| **Actionable Output** | Severity levels + specific remediation recommendations |

### Demo Story

> "Your analysts are already using ChatGPT and Copilot for OPSEC review. Here's what they're missing—and what a purpose-built, on-premises solution delivers."

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

The mission-built analyzer detects violations across six military OPSEC categories:

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
│  │  - /analyze/generic (consumer AI baseline)          │    │
│  │  - /analyze/opsec (mission-built analyzer)          │    │
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
3. **Qwen3 Architecture** — Latest model with optimized inference
4. **GGUF Available** — Works with llama-cpp-python for local deployment

---

## Demo Script (5-minute presentation)

### Opening (30 sec)
> "Your analysts are already using AI for OPSEC review. They're pasting messages into ChatGPT, Copilot, whatever's available. But there's a problem—that data is leaving your network, and the results aren't built for military operations."

### Show Consumer AI Results (1 min)
1. Load "Deployment Email" sample
2. Click "Analyze & Compare"
3. Point to left panel: "This is what a consumer AI tool finds—generic sensitive information without military context."

### Show Mission-Built Results (1 min)  
1. Point to right panel: "Now look at the mission-built analyzer."
2. Highlight: DoD OPSEC categories, severity classification, specific recommendations
3. "Same communication, dramatically different actionable intelligence."

### Key Differentiators (1 min)
> "The mission-built solution provides:
> - Categories aligned with DoD OPSEC doctrine
> - Severity classification for prioritization  
> - Specific remediation recommendations
> - All running entirely on-premises"

### Business Value (1 min)
> "This runs on the HP ZGX Nano AI Station:
> - Zero cloud dependency—works in classified environments
> - No per-token costs—unlimited analysis
> - Full data sovereignty—nothing leaves your network
> - Portable—takes this capability to the edge"

### Close (30 sec)
> "The question isn't whether your analysts will use AI for OPSEC review—they already are. The question is whether you give them consumer tools or mission-built capabilities."

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
Compare consumer AI vs mission-built analysis

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
