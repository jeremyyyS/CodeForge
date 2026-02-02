import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")

# Validation
if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY not found in environment!\n"
        "Please create a .env file with your API key.\n"
        "See .env.example for template."
    )

# API Settings
API_TIMEOUT = 30
MAX_CODE_LENGTH = 10000

# Benchmark Settings
BENCHMARK_RUNS = 3
BENCHMARK_ITERATIONS = 50

# Safety Thresholds
MICRO_OPTIMIZATION_THRESHOLD = 1.05  # 5% speedup minimum
CODE_GROWTH_THRESHOLD = 1.2  # 20% max code growth
MEMORY_BLOAT_THRESHOLD = 1.5  # 50% max memory increase
COMPLEXITY_THRESHOLD = 1.3  # 30% max complexity increase
