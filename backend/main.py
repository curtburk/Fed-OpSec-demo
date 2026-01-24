"""
OPSEC Validator Demo - Backend API
Rocky Mountain CyberSpace Symposium 2026
Demonstrates prompt engineering impact on OPSEC violation detection

Uses: Trendyol-Cybersecurity-LLM-Qwen3-32B (cybersecurity fine-tuned)
Hardware: HP ZGX Nano AI Station with NVIDIA GB10 Grace Blackwell Superchip
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import uvicorn
from llama_cpp import Llama
import json
import time
import os
import gc

app = FastAPI(
    title="OPSEC Validator Demo",
    description="AI-powered OPSEC violation detection for military communications",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model configuration
MODEL_PATH = os.environ.get(
    "OPSEC_MODEL_PATH",
    "/home/curtburk/Desktop/Fed-cybersecurity-demo/models/Trendyol-Cybersecurity-LLM-Qwen3-32B-Q4_K_M.gguf"
)

# Global model instance
model = None
model_loaded = False

# ============================================================================
# OPSEC Categories (Based on DoD OPSEC Doctrine)
# ============================================================================
OPSEC_CATEGORIES = {
    "UNIT_ID": {
        "name": "Unit/Force Identification",
        "description": "Unit names, call signs, organizational structure, personnel names with roles",
        "severity": "HIGH",
        "examples": ["unit designations", "call signs", "commander names", "squadron identifiers"]
    },
    "LOCATION": {
        "name": "Locations",
        "description": "Current positions, future destinations, facilities, coordinates, bases",
        "severity": "CRITICAL",
        "examples": ["GPS coordinates", "base names", "grid references", "city/region mentions"]
    },
    "TIMING": {
        "name": "Timing/Schedules",
        "description": "Operations timing, deployment dates, rotation schedules, meeting times",
        "severity": "HIGH",
        "examples": ["deployment dates", "operation times", "shift schedules", "arrival/departure times"]
    },
    "CAPABILITIES": {
        "name": "Capabilities",
        "description": "Equipment, weapons systems, personnel strength, readiness levels",
        "severity": "CRITICAL",
        "examples": ["aircraft types", "weapon counts", "troop numbers", "equipment status"]
    },
    "INTENTIONS": {
        "name": "Intentions/Plans",
        "description": "Mission objectives, future operations, strategic goals, tactical plans",
        "severity": "CRITICAL",
        "examples": ["mission objectives", "target information", "operational plans", "strategic goals"]
    },
    "VULNERABILITIES": {
        "name": "Vulnerabilities",
        "description": "Weaknesses, gaps, limitations, supply issues, morale problems",
        "severity": "HIGH",
        "examples": ["equipment shortages", "personnel gaps", "defensive weaknesses", "supply chain issues"]
    }
}

# ============================================================================
# Prompt Templates
# NOTE: All curly braces in JSON examples are DOUBLED to escape them
# Only {text} remains single as it's the actual placeholder
# ============================================================================

GENERIC_PROMPT = """<|im_start|>system
You are a helpful assistant that reviews text for sensitive information.
<|im_end|>
<|im_start|>user
Review the following text and identify any sensitive information that should not be shared publicly:

{text}

List any sensitive items found.
<|im_end|>
<|im_start|>assistant
"""

OPSEC_PROMPT = """<|im_start|>system
You are an OPSEC analyst. Output valid JSON only. No markdown, no explanations, no text before or after the JSON.
<|im_end|>
<|im_start|>user
Analyze for OPSEC violations. Return ONLY this JSON structure:
{{"violations": [{{"category": "UNIT_ID|LOCATION|TIMING|CAPABILITIES|INTENTIONS|VULNERABILITIES", "text": "exact quote", "severity": "CRITICAL|HIGH|MEDIUM|LOW", "explanation": "why", "recommendation": "fix"}}], "risk_assessment": "CRITICAL|HIGH|MEDIUM|LOW|CLEAN", "summary": "one sentence"}}

Text to analyze:
{text}
<|im_end|>
<|im_start|>assistant
{{"violations": ["""


# ============================================================================
# Pydantic Models
# ============================================================================

class AnalysisRequest(BaseModel):
    text: str
    max_tokens: int = 2048
    temperature: float = 0.1

class Violation(BaseModel):
    category: str
    category_name: str
    text: str
    severity: str
    explanation: str
    recommendation: str

class AnalysisResult(BaseModel):
    violations: List[Violation]
    risk_assessment: str
    summary: str
    processing_time: float

class ComparisonResponse(BaseModel):
    original_text: str
    generic_result: AnalysisResult
    opsec_result: AnalysisResult
    generic_time: float
    opsec_time: float
    timestamp: str
    improvement_summary: str


# ============================================================================
# Model Loading
# ============================================================================

def load_model():
    """Load the Trendyol Cybersecurity LLM"""
    global model, model_loaded
    
    try:
        print("=" * 60)
        print("Loading Trendyol-Cybersecurity-LLM-Qwen3-32B...")
        print(f"Model path: {MODEL_PATH}")
        print("=" * 60)
        
        if not os.path.exists(MODEL_PATH):
            print(f"ERROR: Model file not found at {MODEL_PATH}")
            print("Please run download_models.sh first.")
            return False
        
        model = Llama(
            model_path=MODEL_PATH,
            n_gpu_layers=-1,      # Use GPU for all layers
            n_ctx=8192,           # Context window for longer documents
            n_batch=2048,         # Batch size for prompt processing
            n_threads=8,          # CPU threads for any CPU work
            verbose=False
        )
        
        print("✓ Model loaded successfully!")
        model_loaded = True
        return True
        
    except Exception as e:
        print(f"ERROR loading model: {e}")
        return False


# ============================================================================
# Analysis Functions
# ============================================================================

def parse_generic_response(response_text: str) -> AnalysisResult:
    """Parse the generic prompt response into structured format"""
    # Generic responses are typically unstructured text
    # We'll create a simple parsing that extracts any mentioned items
    
    violations = []
    lines = response_text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if line and not line.startswith(('Here', 'The', 'I ', 'Based', 'After')):
            # Try to identify if this looks like a finding
            if any(keyword in line.lower() for keyword in ['name', 'location', 'date', 'time', 'unit', 'base']):
                violations.append(Violation(
                    category="UNCLASSIFIED",
                    category_name="Unclassified Finding",
                    text=line[:100],
                    severity="UNKNOWN",
                    explanation="Generic detection without specific categorization",
                    recommendation="Review manually"
                ))
    
    risk = "LOW" if len(violations) > 0 else "CLEAN"
    if len(violations) > 3:
        risk = "MEDIUM"
    
    return AnalysisResult(
        violations=violations,
        risk_assessment=risk,
        summary=f"Generic analysis found {len(violations)} potential items without military context.",
        processing_time=0
    )


def parse_opsec_response(response_text: str) -> AnalysisResult:
    """Parse the OPSEC-specific JSON response"""
    try:
        # The prompt prefills with '{"violations": [' so we need to add it back
        text = response_text.strip()
        
        # Strip Qwen3 thinking tags if present
        if '<think>' in text:
            import re
            text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()
        
        # Add back the prefilled JSON start
        text = '{"violations": [' + text
        
        # Try to extract JSON from the response
        json_start = text.find('{')
        json_end = text.rfind('}') + 1
        
        if json_start != -1 and json_end > json_start:
            json_str = text[json_start:json_end]
            data = json.loads(json_str)
            
            violations = []
            for v in data.get('violations', []):
                category = v.get('category', 'UNKNOWN')
                category_info = OPSEC_CATEGORIES.get(category, {})
                
                violations.append(Violation(
                    category=category,
                    category_name=category_info.get('name', category),
                    text=v.get('text', ''),
                    severity=v.get('severity', 'UNKNOWN'),
                    explanation=v.get('explanation', ''),
                    recommendation=v.get('recommendation', '')
                ))
            
            return AnalysisResult(
                violations=violations,
                risk_assessment=data.get('risk_assessment', 'UNKNOWN'),
                summary=data.get('summary', 'Analysis complete.'),
                processing_time=0
            )
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        print(f"Response text: {response_text[:500]}")
    
    # Fallback if JSON parsing fails
    return AnalysisResult(
        violations=[],
        risk_assessment="ERROR",
        summary="Failed to parse model response. Please try again.",
        processing_time=0
    )


def analyze_with_prompt(text: str, prompt_template: str, max_tokens: int = 2048, temperature: float = 0.1) -> tuple:
    """Run analysis with a specific prompt template"""
    if not model_loaded:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    prompt = prompt_template.format(text=text)
    
    start_time = time.time()
    
    response = model(
        prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        stop=["<|im_end|>", "<|im_start|>"],
        echo=False,
        repeat_penalty=1.1
    )
    
    elapsed_time = time.time() - start_time
    output = response['choices'][0]['text'].strip()
    
    # Debug logging
    print(f"=== MODEL OUTPUT (first 500 chars) ===")
    print(output[:500])
    print(f"=== END OUTPUT ===")
    
    return output, elapsed_time


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/")
def read_root():
    """Health check and status endpoint"""
    return {
        "status": "OPSEC Validator Demo Running",
        "model_loaded": model_loaded,
        "model": "Trendyol-Cybersecurity-LLM-Qwen3-32B" if model_loaded else "Not loaded",
        "categories": list(OPSEC_CATEGORIES.keys()),
        "event": "Rocky Mountain CyberSpace Symposium 2026"
    }


@app.get("/categories")
def get_categories():
    """Get OPSEC category definitions"""
    return OPSEC_CATEGORIES


@app.get("/load_model")
async def load_model_endpoint():
    """Endpoint to trigger model loading"""
    if model_loaded:
        return {"status": "Model already loaded"}
    
    success = load_model()
    if success:
        return {"status": "Model loaded successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to load model. Check model path.")


@app.post("/analyze/generic")
async def analyze_generic(request: AnalysisRequest):
    """Analyze text using generic prompt (baseline)"""
    if not model_loaded:
        load_model()
        if not model_loaded:
            raise HTTPException(status_code=503, detail="Model not loaded")
    
    output, elapsed_time = analyze_with_prompt(
        request.text, 
        GENERIC_PROMPT,
        request.max_tokens,
        request.temperature
    )
    
    result = parse_generic_response(output)
    result.processing_time = round(elapsed_time, 2)
    
    return result


@app.post("/analyze/opsec")
async def analyze_opsec(request: AnalysisRequest):
    """Analyze text using OPSEC-specific prompt"""
    if not model_loaded:
        load_model()
        if not model_loaded:
            raise HTTPException(status_code=503, detail="Model not loaded")
    
    output, elapsed_time = analyze_with_prompt(
        request.text,
        OPSEC_PROMPT,
        request.max_tokens,
        request.temperature
    )
    
    result = parse_opsec_response(output)
    result.processing_time = round(elapsed_time, 2)
    
    return result


@app.post("/analyze/compare")
async def analyze_compare(request: AnalysisRequest):
    """Compare generic vs OPSEC-specific analysis side-by-side"""
    if not model_loaded:
        load_model()
        if not model_loaded:
            raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Run generic analysis
    generic_output, generic_time = analyze_with_prompt(
        request.text,
        GENERIC_PROMPT,
        request.max_tokens,
        request.temperature
    )
    generic_result = parse_generic_response(generic_output)
    generic_result.processing_time = round(generic_time, 2)
    
    # Run OPSEC analysis
    opsec_output, opsec_time = analyze_with_prompt(
        request.text,
        OPSEC_PROMPT,
        request.max_tokens,
        request.temperature
    )
    opsec_result = parse_opsec_response(opsec_output)
    opsec_result.processing_time = round(opsec_time, 2)
    
    # Generate improvement summary
    generic_count = len(generic_result.violations)
    opsec_count = len(opsec_result.violations)
    
    if opsec_count > generic_count:
        improvement = f"OPSEC-specific prompt detected {opsec_count - generic_count} additional violations with proper military categorization."
    elif opsec_count == generic_count:
        improvement = "Both prompts detected similar counts, but OPSEC prompt provides military-specific categorization and actionable recommendations."
    else:
        improvement = "OPSEC prompt provides focused, high-confidence detections with proper severity classification."
    
    return ComparisonResponse(
        original_text=request.text,
        generic_result=generic_result,
        opsec_result=opsec_result,
        generic_time=round(generic_time, 2),
        opsec_time=round(opsec_time, 2),
        timestamp=datetime.now().isoformat(),
        improvement_summary=improvement
    )


@app.get("/samples")
def get_sample_texts():
    """Get sample military communications for demo"""
    return {
        "samples": [
            {
                "id": "email_deployment",
                "name": "Deployment Email",
                "category": "Email Communication",
                "text": """Subject: Re: Family Day Plans

Hey Sarah,

Just wanted to let you know I won't be able to make it to Mom's birthday next month. The 42nd Infantry Division is deploying to Camp Arifjan, Kuwait on March 15th. We're supposed to be there for 9 months, so I'll miss Thanksgiving too.

Captain Rodriguez says we need to have all our gear ready by the 10th. We're taking 12 Stryker vehicles and about 180 personnel from our battalion. The flight leaves from Fort Drum at 0600.

I'll try to video call when I can, but communication might be limited the first few weeks while we set up operations near the Iraqi border.

Love,
Mike
SSG Michael Torres
B Company, 2-14 Infantry"""
            },
            {
                "id": "sitrep_patrol",
                "name": "Patrol SITREP",
                "category": "Situation Report",
                "text": """SITREP - Patrol Alpha-7
DTG: 150830ZJAN26
Location: Grid 38SMB 4523 6712

1. SITUATION: Completed security patrol of MSR Tampa from CP Delta to FOB Warrior. 

2. PERSONNEL: 8 PAX mounted in 2x M-ATV vehicles. PL: 1LT Chen, PSG: SFC Williams

3. SIGNIFICANT ACTIVITIES:
- Observed possible IED emplacement activity at Grid 38SMB 4518 6698 at 0745Z
- Local national provided HUMINT on suspected weapons cache 2km north of patrol route
- Fuel status: Vehicle 1 at 60%, Vehicle 2 at 45% - will need resupply before next patrol

4. EQUIPMENT STATUS: M240B on Vehicle 2 experiencing feed tray issues. Requested replacement part from battalion S4.

5. NEXT PATROL: Scheduled for 160600Z, same route.

SEND"""
            },
            {
                "id": "social_media",
                "name": "Social Media Post",
                "category": "Personal Social Media",
                "text": """Just landed in Djibouti! 🛫 

The C-17 flight was brutal - 14 hours from Dover AFB. Our F-15E squadron (335th Fighter Squadron, "Chiefs") is here to support Operation Enduring Freedom. 

Can't say too much but we're doing night ops starting next week. The base (Camp Lemonnier) is actually pretty nice - they have a good gym and the chow hall food isn't bad.

Shoutout to my crew chief TSgt Martinez! She keeps tail number 91-0312 flying perfect every mission.

Won't have much internet access for the next few days while we do some classified training exercises with our French allies.

#AirForce #Deployed #FighterPilot #335thFS #CampLemonnier"""
            },
            {
                "id": "clean_message",
                "name": "Clean Communication",
                "category": "Properly Sanitized",
                "text": """Hi Team,

Just a reminder that our regular team meeting is scheduled for this Thursday at the usual time in the main conference room.

Please come prepared to discuss project updates and any blockers you're experiencing. We'll also review the quarterly objectives.

If you have any agenda items to add, please send them to me by end of day Wednesday.

Thanks,
John"""
            },
            {
                "id": "logistics_email",
                "name": "Logistics Request",
                "category": "Supply Chain",
                "text": """From: CPT Amanda Foster, S4
To: Battalion Logistics
Subject: Urgent Resupply Request - Exercise Iron Sword

Battalion,

We need the following items delivered to our assembly area at Training Area 12, Joint Base Lewis-McChord by 0400 on February 3rd:

- 5,000 rounds 5.56mm ball ammunition
- 200 MREs (Menu variety)
- 2,000 gallons JP-8 fuel
- 12 replacement IOTV plates (Size Large)
- 3 PRC-152 radios with SINCGARS fill

Our current supplies will last through February 1st. We have 3 M978 fuel tankers and 4 LMTVs available for transport from the Supply Support Activity.

The exercise involves 450 personnel from 1st Battalion, 23rd Infantry Regiment conducting live-fire exercises from Feb 3-10.

V/R,
CPT Foster
S4, 1-23 IN
DSN: 555-1234"""
            }
        ]
    }


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("OPSEC Validator Demo")
    print("Rocky Mountain CyberSpace Symposium 2026")
    print("=" * 60)
    print()
    print("Model: Trendyol-Cybersecurity-LLM-Qwen3-32B")
    print("Hardware: HP ZGX Nano AI Station")
    print()
    
    # Attempt to load model on startup
    print("Loading model on startup...")
    success = load_model()
    if success:
        print("✓ Model ready for inference!")
    else:
        print("⚠ Model not loaded. Use /load_model endpoint to load manually.")
    
    print()
    print("Starting API server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)