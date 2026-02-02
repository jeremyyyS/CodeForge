# utils.py
import ast
import timeit
import tracemalloc
import statistics
import sys
from io import StringIO
from config import BENCHMARK_RUNS, BENCHMARK_ITERATIONS


def robust_benchmark(code: str, runs: int = None, iterations: int = None):
    if runs is None:
        runs = BENCHMARK_RUNS
    if iterations is None:
        iterations = BENCHMARK_ITERATIONS
    
    samples = []
    mem_samples = []

    for run_num in range(runs):
        try:
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            tracemalloc.start()

            t = timeit.timeit(lambda: exec(code), number=iterations)

            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            sys.stdout = old_stdout

            samples.append(t * 1000 / iterations)
            mem_samples.append(peak / (1024 ** 2))
        except Exception as e:
            if sys.stdout != old_stdout:
                sys.stdout = old_stdout
            if tracemalloc.is_tracing():
                tracemalloc.stop()

    if not samples:
        return None

    return {
        "runtime_ms": round(statistics.mean(samples), 3),
        "memory_mb": round(max(mem_samples), 2),
        "runs": len(samples)
    }
