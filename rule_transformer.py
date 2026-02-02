# rule_transformer.py
import ast
import re
from typing import List, Dict, Tuple

def apply_rule_based_optimizations(code: str, rules: List[Dict]) -> Tuple[str, List[Dict]]:
    """
    Applies deterministic, offline optimizations.
    """
    optimized = code
    transformations = []

    try:
        ast.parse(code)
    except:
        return code, []

    for rule in rules:
        if rule["rule"] == "range_len_pattern":
            match = re.search(r"for (\w+) in range\(len\((\w+)\)\):", optimized)
            if match:
                loop_var, collection = match.groups()
                optimized = re.sub(
                    r"for " + loop_var + r" in range\(len\(" + collection + r"\)\):",
                    f"for {loop_var}, item in enumerate({collection}):",
                    optimized
                )
                optimized = re.sub(rf"{collection}\[{loop_var}\]", "item", optimized)
                transformations.append(rule)

        elif rule["rule"] == "constant_folding":
            optimized = re.sub(
                r"(\d+)\s*\+\s*(\d+)",
                lambda m: str(int(m.group(1)) + int(m.group(2))),
                optimized
            )
            transformations.append(rule)

    return optimized, transformations
