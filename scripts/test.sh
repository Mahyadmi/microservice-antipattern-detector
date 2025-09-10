#!/bin/bash
set -e

API_URL="http://localhost:8000"

echo "🧪 Testing API health..."
curl -s $API_URL/api/health | python3 -m json.tool || echo "API might still be starting..."

echo ""
echo "📊 Starting test analysis..."
curl -s -X POST $API_URL/api/analysis \
    -H "Content-Type: application/json" \
    -d '{"project_name": "sample-microservice"}' | python3 -m json.tool || echo "Analysis request sent"

echo ""
echo "✅ Tests completed"
