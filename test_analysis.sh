#!/bin/bash

echo "=== Testing Analysis System ==="

# 1. Check API is running
echo "1. Checking API health..."
API_HEALTH=$(curl -s http://localhost:8000/api/health)
echo "API Response: $API_HEALTH"

# 2. Start an analysis
echo -e "\n2. Starting analysis..."
RESPONSE=$(curl -s -X POST http://localhost:8000/api/analysis \
  -H "Content-Type: application/json" \
  -d '{"project_name": "spring-petclinic-microservices"}')

echo "Analysis Response: $RESPONSE"

# Extract analysis ID
ANALYSIS_ID=$(echo $RESPONSE | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('analysis_id', 'ERROR'))")
echo "Analysis ID: $ANALYSIS_ID"

if [ "$ANALYSIS_ID" = "ERROR" ]; then
    echo "Failed to start analysis!"
    exit 1
fi

# 3. Wait for completion
echo -e "\n3. Waiting 6 seconds for analysis to complete..."
sleep 6

# 4. Get results
echo -e "\n4. Getting results..."
RESULTS=$(curl -s http://localhost:8000/api/analysis/$ANALYSIS_ID/results)
echo "Results:"
echo $RESULTS | python3 -m json.tool

echo -e "\n=== Test Complete ==="
