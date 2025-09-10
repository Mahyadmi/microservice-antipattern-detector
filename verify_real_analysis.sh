#!/bin/bash

echo "=== Verifying Real Analysis System ==="
echo ""

# 1. Check system status
echo "1. System Status:"
STATUS=$(curl -s http://localhost:8000/api/health | python3 -c "import sys, json; d=json.load(sys.stdin); print(f'Real Analysis: {d[\"real_analysis\"]}')")
echo "   $STATUS"

# 2. Run analysis on each dataset
echo ""
echo "2. Running Analysis on All Datasets:"

for dataset in "gs-spring-boot" "spring-petclinic-microservices" "sock-shop" "eShopOnContainers"; do
    echo "   - $dataset: "
    RESPONSE=$(curl -s -X POST http://localhost:8000/api/analysis \
        -H "Content-Type: application/json" \
        -d "{\"project_name\": \"$dataset\"}")
    
    ID=$(echo $RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['analysis_id'])")
    
    sleep 5
    
    RESULTS=$(curl -s http://localhost:8000/api/analysis/$ID/results)
    COUNT=$(echo $RESULTS | python3 -c "import sys, json; print(len(json.load(sys.stdin).get('anti_patterns', [])))")
    
    echo "     Found $COUNT anti-patterns"
done

echo ""
echo "=== System Verification Complete ==="
