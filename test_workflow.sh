#!/bin/bash

echo "🧪 Testing Microservice Anti-Pattern Detection System"
echo "================================================"

# 1. Check health
echo -e "\n1️⃣ Checking system health..."
curl -s http://localhost:8000/api/health | python3 -m json.tool

# 2. Start analysis
echo -e "\n2️⃣ Starting new analysis..."
RESPONSE=$(curl -s -X POST http://localhost:8000/api/analysis \
  -H "Content-Type: application/json" \
  -d '{"project_name": "test-microservice-'$(date +%s)'"}')

echo $RESPONSE | python3 -m json.tool

# Extract analysis ID
ANALYSIS_ID=$(echo $RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['analysis_id'])")
echo "Analysis ID: $ANALYSIS_ID"

# 3. Check status
echo -e "\n3️⃣ Checking analysis status..."
curl -s http://localhost:8000/api/analysis/$ANALYSIS_ID | python3 -m json.tool

# 4. Wait for completion
echo -e "\n4️⃣ Waiting for analysis to complete (6 seconds)..."
sleep 6

# 5. Get results
echo -e "\n5️⃣ Getting analysis results..."
curl -s http://localhost:8000/api/analysis/$ANALYSIS_ID/results | python3 -m json.tool

# 6. List all analyses
echo -e "\n6️⃣ Listing all analyses..."
curl -s http://localhost:8000/api/analyses | python3 -m json.tool

echo -e "\n✅ Test complete!"
