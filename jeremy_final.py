## run this file first always
from ai_explainer import generate_ai_explanation
from semantic_search import SemanticPatternDetector
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel, Field
import ast
from datetime import datetime

from rules_engine import RuleBasedOptimizer
from rule_transformer import apply_rule_based_optimizations
from llm_optimizer import optimize_with_gemini
from utils import robust_benchmark

app = FastAPI()
rule_optimizer = RuleBasedOptimizer()
semantic_detector = SemanticPatternDetector()


class CodeRequest(BaseModel):
    code: str = Field(..., min_length=1, max_length=10000)

# ---------------- OFFLINE (FULL) ----------------
@app.post("/optimize-rules-only")
async def optimize_rules_only(req: CodeRequest):
    rules = rule_optimizer.analyze(req.code)
    optimized, transformations = apply_rule_based_optimizations(req.code, rules)
    
    try:
        ast.parse(optimized)
    except SyntaxError:
        optimized = req.code
    
    original_bench = robust_benchmark(req.code, runs=3)
    optimized_bench = robust_benchmark(optimized, runs=3)
    
    speedup = 1.0
    if original_bench and optimized_bench:
        speedup = original_bench['runtime_ms'] / optimized_bench['runtime_ms']

    return {
        "mode": "RULES_ONLY",
        "original_code": req.code,
        "optimized_code": optimized,
        "rules_detected": rules,
        "transformations": transformations,
        "benchmarks": {
            "original": original_bench,
            "optimized": optimized_bench,
            "speedup_factor": round(speedup, 2)
        },
        "timestamp": datetime.now().isoformat()
    }

# ---------------- OFFLINE (SIMPLE) ----------------
@app.post("/optimize-rules-only/simple")
async def optimize_rules_only_simple(req: CodeRequest):
    rules = rule_optimizer.analyze(req.code)
    optimized, _ = apply_rule_based_optimizations(req.code, rules)
    
    try:
        ast.parse(optimized)
    except SyntaxError:
        optimized = req.code

    return {
        "original_code": req.code,
        "optimized_code": optimized
    }


# ---------------- ONLINE (HYBRID) ----------------
@app.post("/optimize")
async def optimize_hybrid(req: CodeRequest):
    rules = rule_optimizer.analyze(req.code)
    semantic_patterns = semantic_detector.find_semantic_patterns(req.code)   #get semantic patterns
    rules = rules + semantic_patterns     #combine both


    
    try:
        optimized = await optimize_with_gemini(req.code, hints=rules)
    except Exception as e:
        raise HTTPException(500, detail=str(e))
    
    original_bench = robust_benchmark(req.code, runs=3)
    optimized_bench = robust_benchmark(optimized, runs=3)
    
    speedup = 1.0
    variance_pct = 0.0
    mem_before = 0.0
    mem_after = 0.0
    
    if original_bench and optimized_bench:
        speedup = original_bench['runtime_ms'] / optimized_bench['runtime_ms']
        variance_pct = original_bench.get('variance_pct', 0.0)
        mem_before = original_bench['memory_mb']
        mem_after = optimized_bench['memory_mb']
    
    # Safety validation
    from safety import SafetyGuard
    safety_guard = SafetyGuard()
    safety_analysis = safety_guard.validate(
        req.code, optimized, speedup, mem_before, mem_after
    )
    
    # Confidence scoring
    from metrics import calculate_confidence, generate_explainability
    confidence = calculate_confidence(rules, speedup, variance_pct)
    
    # Explainability
    explainability = generate_explainability(req.code, optimized, speedup, rules)

    # AI Explanation
    ai_explanation = await generate_ai_explanation(req.code, optimized, rules, speedup)


    return {
        "mode": "HYBRID",
        "status": "success",
        "original_code": req.code,
        "optimized_code": optimized,
        "rules_detected": rules,
        "benchmarks": {
            "original": original_bench,
            "optimized": optimized_bench,
            "speedup_factor": round(speedup, 2)
        },
        "safety_analysis": safety_analysis,
        "confidence": confidence,
        "explainability": explainability,
        "ai_explanation": ai_explanation,
        "timestamp": datetime.now().isoformat()
    }


# ---------------- FILE UPLOAD ----------------
@app.post("/upload")
async def upload_code(file: UploadFile = File(...)):
    if not file.filename.endswith('.py'):
        raise HTTPException(400, detail="Only .py files allowed")
    
    code = (await file.read()).decode("utf-8")
    return await optimize_hybrid(CodeRequest(code=code))

# ---------------- HEALTH ----------------
@app.get("/")
async def root():
    return {
        "message": "SafeOpt Code Optimizer",
        "status": "running",
        "version": "1.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("jeremy_final:app", host="0.0.0.0", port=8000, reload=True)
