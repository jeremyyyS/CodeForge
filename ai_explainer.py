import asyncio
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, MODEL_NAME, API_TIMEOUT

client = genai.Client(api_key=GEMINI_API_KEY)

async def generate_ai_explanation(original_code: str, optimized_code: str, rules: list, speedup: float) -> str:
    """Generate natural language explanation of optimizations"""
    
    rules_text = "\n".join([f"- {r['message']}: {r['suggestion']}" for r in rules[:3]])  # Top 3 rules
    
    prompt = f"""You are a Python optimization expert. Explain in 2-3 simple sentences why the optimization improves performance.

ORIGINAL CODE:
{original_code}

OPTIMIZED CODE:
{optimized_code}

DETECTED ISSUES:
{rules_text}

SPEEDUP: {speedup}x

Explain in plain English why this optimization is faster. Focus on what happens under the hood (e.g., C implementations, memory allocation). Keep it under 60 words."""

    try:
        response = await asyncio.wait_for(
            asyncio.to_thread(
                lambda: client.models.generate_content(
                    model=MODEL_NAME,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.3,
                        thinking_config=types.ThinkingConfig(thinking_budget=0)
                    )
                )
            ),
            timeout=API_TIMEOUT
        )
        
        return response.text.strip()
    except Exception as e:
        return f"Optimization applied successfully with {speedup}x speedup."
