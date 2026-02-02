# metrics.py
from typing import List, Dict
from difflib import unified_diff

def calculate_confidence(rules: List[Dict], speedup: float, variance_pct: float) -> Dict:
    """Calculate confidence score for optimization."""
    rule_score = min(len(rules) * 10, 40)
    
    # Non-linear speedup scoring
    if speedup >= 2.0:
        speedup_score = 40
    elif speedup >= 1.5:
        speedup_score = 30
    elif speedup >= 1.2:
        speedup_score = 20
    elif speedup >= 1.1:
        speedup_score = 10
    else:
        speedup_score = 5
    
    stability_score = max(20 - variance_pct, 5)
    total = rule_score + speedup_score + stability_score
    confidence = min(100, total)
    
    return {
        "overall": round(confidence),
        "breakdown": {
            "rule_certainty": rule_score,
            "speedup_gain": round(speedup_score),
            "benchmark_stability": round(stability_score)
        },
        "recommendation": (
            "APPLY" if confidence >= 75 else
            "REVIEW" if confidence >= 50 else
            "CAUTION"
        ),
        "confidence_level": (
            "HIGH" if confidence >= 75 else
            "MEDIUM" if confidence >= 50 else
            "LOW"
        )
    }

def generate_explainability(original: str, optimized: str, speedup: float, rules: List[Dict]) -> Dict:
    """Generate human-readable explanation of optimizations."""
    diff_lines = list(unified_diff(
        original.splitlines(),
        optimized.splitlines(),
        fromfile='original',
        tofile='optimized',
        lineterm=''
    ))
    
    added = len([l for l in diff_lines if l.startswith('+')])
    removed = len([l for l in diff_lines if l.startswith('-')])
    
    return {
        "code_diff": "\n".join(diff_lines[:30]),
        "transformation": {
            "original_lines": len(original.splitlines()),
            "optimized_lines": len(optimized.splitlines()),
            "net_change": len(optimized.splitlines()) - len(original.splitlines()),
            "lines_added": added,
            "lines_removed": removed
        },
        "performance": {
            "speedup_factor": round(speedup, 2),
            "speedup_percentage": round((speedup - 1) * 100, 1)
        },
        "rules_applied": [
            f"Line {r['line']}: {r['message']}" 
            for r in rules[:5]
        ],
        "key_transformations": [
            r['suggestion'] for r in rules[:3]
        ]
    }
