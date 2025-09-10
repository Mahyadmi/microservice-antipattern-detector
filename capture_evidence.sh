#!/bin/bash

echo "Capturing Evidence for Dissertation"
echo "===================================="

# Create evidence directory
mkdir -p dissertation_evidence

# Save current service status
docker-compose ps > dissertation_evidence/docker_services.txt

# Save API health check
curl -s http://localhost:8000/api/health | python3 -m json.tool > dissertation_evidence/api_health.json

# Save SonarQube status
curl -s http://localhost:9002/api/system/status | python3 -m json.tool > dissertation_evidence/sonarqube_status.json

echo "Evidence saved in dissertation_evidence/"
echo ""
echo "IMPORTANT: Take screenshots of:"
echo "1. Dashboard main page (http://localhost:3000)"
echo "2. Analysis in progress"
echo "3. Results displaying anti-patterns"
echo "4. Different datasets showing different results"
