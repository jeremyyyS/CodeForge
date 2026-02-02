from sentence_transformers import SentenceTransformer
import ast
import numpy as np

class SemanticPatternDetector:
    def __init__(self):
        # Use a code-understanding model
        self.model = SentenceTransformer('microsoft/codebert-base')
        
        # Known inefficient patterns (embeddings will be computed once)
        self.inefficient_patterns = [
            "for i in range(len(array)): result.append(array[i])",
            "index = 0\nwhile index < len(array): item = array[index]; index += 1",
            "text = ''\nfor item in items: text = text + str(item)",
            "for key in dict: if key == target: return dict[key]",
            "for i in range(len(list1)): for j in range(len(list2)): compare(list1[i], list2[j])"
        ]
        
        self.pattern_embeddings = self.model.encode(self.inefficient_patterns)
    
    def extract_code_blocks(self, code: str):
        """Extract loops and function bodies from code"""
        try:
            tree = ast.parse(code)
            blocks = []
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.For, ast.While)):
                    blocks.append(ast.unparse(node))
            
            return blocks
        except:
            return []
    
    def find_semantic_patterns(self, code: str, threshold=0.75):
        """Find semantically similar inefficient patterns"""
        blocks = self.extract_code_blocks(code)
        if not blocks:
            return []
        
        # Encode code blocks
        block_embeddings = self.model.encode(blocks)
        
        detected = []
        for i, block_emb in enumerate(block_embeddings):
            # Calculate cosine similarity with known patterns
            similarities = np.dot(self.pattern_embeddings, block_emb) / (
                np.linalg.norm(self.pattern_embeddings, axis=1) * np.linalg.norm(block_emb)
            )
            
            max_sim_idx = np.argmax(similarities)
            max_similarity = similarities[max_sim_idx]
            
            if max_similarity > threshold:
                detected.append({
                    "rule": "semantic_pattern_match",
                    "line": 0,  # Can enhance with line tracking
                    "message": f"Semantically similar to inefficient pattern (confidence: {max_similarity:.2%})",
                    "suggestion": self._get_suggestion(max_sim_idx),
                    "confidence": float(max_similarity),
                    "matched_pattern": self.inefficient_patterns[max_sim_idx]
                })
        
        return detected
    
    def _get_suggestion(self, pattern_idx):
        suggestions = [
            "Use list comprehension or direct slicing",
            "Use enumerate() or direct iteration",
            "Use join() for string concatenation",
            "Use dict.get() or 'in' operator",
            "Consider using itertools or vectorized operations"
        ]
        return suggestions[pattern_idx] if pattern_idx < len(suggestions) else "Optimize this pattern"
