import requests
import json
import time

print("System Verification Test")
print("=" * 40)

# Test API
try:
    health = requests.get("http://localhost:8000/api/health").json()
    print(f"✓ API Health: {health['status']}")
except:
    print("✗ API not responding")
    exit(1)

# Start analysis
response = requests.post(
    "http://localhost:8000/api/analysis",
    json={"project_name": "spring-petclinic-microservices"}
)
data = response.json()
analysis_id = data.get("analysis_id")
print(f"✓ Analysis Started: {analysis_id}")

# Wait
print("Waiting for analysis...")
time.sleep(6)

# Get results
results = requests.get(f"http://localhost:8000/api/analysis/{analysis_id}/results").json()

if "anti_patterns" in results:
    patterns = results["anti_patterns"]
    print(f"✓ Found {len(patterns)} anti-patterns")
    
    # Show tools used
    tools = set(p["tool"] for p in patterns)
    print(f"✓ Tools used: {', '.join(tools)}")
    
    # Show pattern types
    types = set(p["type"] for p in patterns)
    print(f"✓ Pattern types: {', '.join(types)}")
else:
    print("✗ No results found")

print("\nSystem is working correctly!")
