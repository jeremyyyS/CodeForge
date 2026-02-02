# rules_engine.py
import ast
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class OptimizationRule:
    def __init__(self, name: str, description: str, check_fn, severity: str = "medium"):
        self.name = name
        self.description = description
        self.check_fn = check_fn
        self.severity = severity

class RuleBasedOptimizer:
    """
    Detects optimization opportunities using AST analysis.
    """
    def __init__(self):
        self.rules = [
            # Existing rules
            OptimizationRule(
                "range_len_pattern",
                "Detect range(len(x)) anti-pattern",
                self._check_range_len,
            ),
            OptimizationRule(
                "append_in_loop",
                "Detect append() inside loops",
                self._check_append_in_loop,
            ),
            OptimizationRule(
                "constant_folding",
                "Detect constant expressions",
                self._check_constant_folding,
            ),
            OptimizationRule(
                "loop_invariant_motion",
                "Detect invariant len() in loops",
                self._check_loop_invariants,
            ),
            # New rules
            OptimizationRule(
                "string_concat_loop",
                "Detect string concatenation in loops",
                self._check_string_concat_loop,
            ),
            OptimizationRule(
                "list_membership",
                "Detect list membership checks in loops",
                self._check_list_membership,
            ),
            OptimizationRule(
                "repeated_dict_lookup",
                "Detect repeated dictionary lookups",
                self._check_repeated_dict_lookup,
            ),
            OptimizationRule(
                "list_comprehension_vs_generator",
                "Detect list comprehensions that should be generators",
                self._check_list_vs_generator,
            ),
            OptimizationRule(
                "multiple_isinstance",
                "Detect multiple isinstance checks",
                self._check_multiple_isinstance,
            ),
            OptimizationRule(
                "nested_loops",
                "Detect nested loops without optimization",
                self._check_nested_loops,
            ),
            OptimizationRule(
                "global_in_loop",
                "Detect global variable access in loops",
                self._check_global_in_loop,
            ),
            OptimizationRule(
                "repeated_function_call",
                "Detect repeated function calls with same args",
                self._check_repeated_function_call,
            ),
        ]

    def analyze(self, code: str) -> List[Dict]:
        try:
            tree = ast.parse(code)
        except Exception as e:
            logger.warning(f"AST parse failed: {e}")
            return []

        findings = []
        for rule in self.rules:
            findings.extend(rule.check_fn(tree))
        return findings

    # Existing rule checks
    def _check_range_len(self, tree):
        findings = []
        for node in ast.walk(tree):
            if isinstance(node, ast.For):
                if isinstance(node.iter, ast.Call) and hasattr(node.iter.func, 'id'):
                    if node.iter.func.id == 'range' and len(node.iter.args) == 1:
                        arg = node.iter.args[0]
                        if isinstance(arg, ast.Call) and hasattr(arg.func, 'id') and arg.func.id == 'len':
                            findings.append({
                                "rule": "range_len_pattern",
                                "line": node.lineno,
                                "message": "range(len(x)) detected",
                                "suggestion": "Use enumerate(x)"
                            })
        return findings

    def _check_append_in_loop(self, tree):
        findings = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While)):
                for child in ast.walk(node):
                    if isinstance(child, ast.Call) and hasattr(child.func, 'attr'):
                        if child.func.attr == 'append':
                            findings.append({
                                "rule": "append_in_loop",
                                "line": node.lineno,
                                "message": "append() inside loop",
                                "suggestion": "Use list comprehension"
                            })
                            break
        return findings

    def _check_constant_folding(self, tree):
        findings = []
        for node in ast.walk(tree):
            if isinstance(node, ast.BinOp):
                if isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Constant):
                    findings.append({
                        "rule": "constant_folding",
                        "line": node.lineno,
                        "message": "Constant expression detected",
                        "suggestion": "Pre-compute value"
                    })
        return findings

    def _check_loop_invariants(self, tree):
        findings = []
        for node in ast.walk(tree):
            if isinstance(node, ast.For) and isinstance(node.iter, ast.Call):
                if hasattr(node.iter.func, 'id') and node.iter.func.id == 'range':
                    for arg in node.iter.args:
                        if isinstance(arg, ast.Call) and hasattr(arg.func, 'id') and arg.func.id == 'len':
                            findings.append({
                                "rule": "loop_invariant_motion",
                                "line": node.lineno,
                                "message": "Invariant len() inside loop",
                                "suggestion": "Move len() outside loop"
                            })
        return findings

    # New rule checks
    def _check_string_concat_loop(self, tree):
        findings = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While)):
                for child in ast.walk(node):
                    if isinstance(child, ast.AugAssign) and isinstance(child.op, ast.Add):
                        if isinstance(child.target, ast.Name):
                            findings.append({
                                "rule": "string_concat_loop",
                                "line": node.lineno,
                                "message": "String concatenation in loop detected",
                                "suggestion": "Use ''.join() instead"
                            })
                            break
        return findings

    def _check_list_membership(self, tree):
        findings = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While)):
                for child in ast.walk(node):
                    if isinstance(child, ast.Compare):
                        if any(isinstance(op, ast.In) for op in child.ops):
                            for comp in child.comparators:
                                if isinstance(comp, ast.List):
                                    findings.append({
                                        "rule": "list_membership",
                                        "line": node.lineno,
                                        "message": "List membership check in loop",
                                        "suggestion": "Convert list to set for O(1) lookup"
                                    })
                                    break
        return findings

    def _check_repeated_dict_lookup(self, tree):
        findings = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While)):
                subscripts = []
                for child in ast.walk(node):
                    if isinstance(child, ast.Subscript):
                        subscripts.append(child)
                if len(subscripts) > 2:
                    findings.append({
                        "rule": "repeated_dict_lookup",
                        "line": node.lineno,
                        "message": "Multiple dictionary/list lookups in loop",
                        "suggestion": "Cache lookup result in variable"
                    })
                    break
        return findings

    def _check_list_vs_generator(self, tree):
        findings = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ListComp):
                parent = None
                for potential_parent in ast.walk(tree):
                    for child in ast.iter_child_nodes(potential_parent):
                        if child == node:
                            parent = potential_parent
                            break
                if isinstance(parent, (ast.Call, ast.For)):
                    findings.append({
                        "rule": "list_comprehension_vs_generator",
                        "line": node.lineno,
                        "message": "List comprehension used where generator would suffice",
                        "suggestion": "Use generator expression for memory efficiency"
                    })
        return findings

    def _check_multiple_isinstance(self, tree):
        findings = []
        for node in ast.walk(tree):
            if isinstance(node, ast.BoolOp) and isinstance(node.op, ast.Or):
                isinstance_count = sum(
                    1 for val in node.values
                    if isinstance(val, ast.Call) and 
                    hasattr(val.func, 'id') and 
                    val.func.id == 'isinstance'
                )
                if isinstance_count >= 2:
                    findings.append({
                        "rule": "multiple_isinstance",
                        "line": node.lineno,
                        "message": "Multiple isinstance checks with OR",
                        "suggestion": "Use isinstance(obj, (Type1, Type2))"
                    })
        return findings

    def _check_nested_loops(self, tree):
        findings = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While)):
                for child in ast.walk(node):
                    if child != node and isinstance(child, (ast.For, ast.While)):
                        findings.append({
                            "rule": "nested_loops",
                            "line": node.lineno,
                            "message": "Nested loop detected",
                            "suggestion": "Consider algorithmic optimization or vectorization"
                        })
                        break
        return findings

    def _check_global_in_loop(self, tree):
        findings = []
        global_vars = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Global):
                global_vars.update(node.names)
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While)):
                for child in ast.walk(node):
                    if isinstance(child, ast.Name) and child.id in global_vars:
                        findings.append({
                            "rule": "global_in_loop",
                            "line": node.lineno,
                            "message": "Global variable accessed in loop",
                            "suggestion": "Cache global variable in local variable"
                        })
                        break
        return findings

    def _check_repeated_function_call(self, tree):
        findings = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While)):
                function_calls = []
                for child in ast.walk(node):
                    if isinstance(child, ast.Call) and hasattr(child.func, 'id'):
                        function_calls.append(child.func.id)
                
                if len(function_calls) != len(set(function_calls)):
                    findings.append({
                        "rule": "repeated_function_call",
                        "line": node.lineno,
                        "message": "Repeated function calls in loop",
                        "suggestion": "Cache function result if deterministic"
                    })
                    break
        return findings
