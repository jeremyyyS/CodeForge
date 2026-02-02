# safety.py
import ast
from typing import Dict, List
from config import (
    MICRO_OPTIMIZATION_THRESHOLD,
    CODE_GROWTH_THRESHOLD,
    MEMORY_BLOAT_THRESHOLD,
    COMPLEXITY_THRESHOLD
)

class SafetyGuard:
    """
    Validates optimizations to prevent harmful changes.
    """
    
    def validate(self, original: str, optimized: str, speedup: float,
                 mem_before: float, mem_after: float) -> Dict:
        """
        Check for 3 types of harmful optimizations:
        1. Micro-optimization: Minimal speedup but more code
        2. Memory bloat: 50%+ increase
        3. Readability loss: 30%+ complexity increase
        """
        warnings = []
        
        # Check 1: Micro-optimization
        if speedup < MICRO_OPTIMIZATION_THRESHOLD and len(optimized) > len(original) * CODE_GROWTH_THRESHOLD:
            warnings.append({
                "type": "micro_optimization",
                "severity": "HIGH",
                "message": f"Only {(speedup-1)*100:.1f}% faster but code {(len(optimized)/len(original)-1)*100:.0f}% longer",
                "recommendation": "REJECT - not worth the complexity increase"
            })
        
        # Check 2: Memory explosion
        if mem_after > 0 and mem_before > 0 and mem_after > mem_before * MEMORY_BLOAT_THRESHOLD:
            warnings.append({
                "type": "memory_bloat",
                "severity": "MEDIUM",
                "message": f"Memory increased {(mem_after/mem_before):.1f}x ({mem_after-mem_before:.1f}MB)",
                "recommendation": "WARN - verify memory trade-off is acceptable"
            })
        
        # Check 3: Readability loss
        try:
            orig_ast = ast.parse(original)
            opt_ast = ast.parse(optimized)
            orig_complexity = len(list(ast.walk(orig_ast)))
            opt_complexity = len(list(ast.walk(opt_ast)))
            
            if opt_complexity > orig_complexity * COMPLEXITY_THRESHOLD and speedup < 1.1:
                warnings.append({
                    "type": "readability_loss",
                    "severity": "MEDIUM",
                    "message": f"Code complexity increased {(opt_complexity/orig_complexity-1)*100:.0f}% for only {(speedup-1)*100:.1f}% speedup",
                    "recommendation": "WARN - prioritize readability over micro-optimizations"
                })
        except:
            pass
        
        return {
            "is_safe": len([w for w in warnings if w['severity'] == 'HIGH']) == 0,
            "warnings": warnings,
            "verdict": "SAFE TO APPLY" if len(warnings) == 0 else "REVIEW NEEDED",
            "safe_count": 3 - len(warnings)
        }
