import requests
import json

url = "http://127.0.0.1:8000/optimize"

code = """
data = list(range(1000))
result = []
for i in range(len(data)):
    result.append(data[i] * 2)
print(len(result))
"""

response = requests.post(url, json={"code": code})
data = response.json()

print("="*60)
print("AI EXPLANATION:")
print("="*60)
print(data["ai_explanation"])
print()

print("="*60)
print("TECHNICAL DETAILS:")
print("="*60)
print(f"Speedup: {data['benchmarks']['speedup_factor']}x")
print(f"Confidence: {data['confidence']['overall']}%")
print(f"Rules detected: {len(data['rules_detected'])}")
print(f"Safety: {data['safety_analysis']['verdict']}")
