# Testing Guide

## Quick System Test
```bash
# 1. Check all services are running
docker-compose ps

# 2. Test API health
curl http://localhost:8000/api/health

# 3. Run validation
python3 validation/simple_validation.py
Expected Results

API should return "healthy" status
Validation should show 100% precision, 66.7% recall
Dashboard should load at http://localhost:3000
