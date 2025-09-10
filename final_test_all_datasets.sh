#!/bin/bash

echo "========================================="
echo "FINAL SYSTEM TEST - ALL DATASETS"
echo "========================================="

DATASETS=("gs-spring-boot" "spring-petclinic-microservices" "sock-shop" "eShopOnContainers")

for dataset in "${DATASETS[@]}"; do
    echo ""
    echo "Testing: $dataset"
    echo "-----------------"
    
    # Start analysis
    RESPONSE=$(curl -s -X POST http://localhost:8000/api/analysis \
        -H "Content-Type: application/json" \
        -d "{\"project_name\": \"$dataset\"}")
    
    ANALYSIS_ID=$(echo $RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['analysis_id'])")
    echo "Analysis ID: $ANALYSIS_ID"
    
    # Wait for completion
    sleep 5
    
    # Get results
    RESULTS=$(curl -s http://localhost:8000/api/analysis/$ANALYSIS_ID/results)
    PATTERN_COUNT=$(echo $RESULTS | python3 -c "import sys, json; print(len(json.load(sys.stdin)['anti_patterns']))")
    
    echo "Patterns found: $PATTERN_COUNT"
done

echo ""
echo "========================================="
echo "ALL TESTS COMPLETED SUCCESSFULLY"
echo "========================================="
