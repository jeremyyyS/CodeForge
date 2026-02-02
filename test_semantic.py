import requests
import json

url = "http://127.0.0.1:8000/optimize"

# This pattern your rule engine won't catch, but semantic search will
code = """
idx = 0
result = []
while idx < len(data):
    result.append(data[idx])
    idx += 1
print(result)
"""

response = requests.post(url, json={"code": code})
data = response.json()

print("RULES DETECTED:")
for rule in data["rules_detected"]:
    print(f"  - {rule['rule']}: {rule['message']}")
    if 'confidence' in rule:
        print(f"    Confidence: {rule['confidence']:.1%}")
        print(f"    Suggestion: {rule['suggestion']}")

print(f"\nTotal patterns found: {len(data['rules_detected'])}")
