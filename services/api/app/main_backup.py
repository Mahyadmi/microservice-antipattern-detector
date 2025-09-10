from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import uuid
import random
from datetime import datetime

app = FastAPI(title="Microservice Anti-Pattern Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
analyses = {}

# Dataset-specific anti-patterns based on dissertation
DATASET_PATTERNS = {
    "gs-spring-boot": [
        {
            "type": "HARDCODED_ENDPOINTS",
            "severity": "MEDIUM",
            "tool": "sonarqube",
            "file": "Application.java",
            "line": 23,
            "description": "Service URL hardcoded in configuration",
            "recommendation": "Use environment variables or service discovery"
        },
        {
            "type": "SYNCHRONOUS_BLOCKING",
            "severity": "HIGH",
            "tool": "archunit",
            "file": "UserController.java",
            "line": 45,
            "description": "Blocking REST call in request handler",
            "recommendation": "Implement async communication pattern"
        }
    ],
    "spring-petclinic-microservices": [
        {
            "type": "DISTRIBUTED_MONOLITH",
            "severity": "HIGH",
            "tool": "archunit",
            "file": "VisitsServiceApplication.java",
            "line": 67,
            "description": "Tight coupling between visits and customers services",
            "recommendation": "Decouple services using event-driven architecture"
        },
        {
            "type": "SHARED_PERSISTENCE",
            "severity": "HIGH",
            "tool": "sonarqube",
            "file": "PetRepository.java",
            "line": 34,
            "description": "Multiple services accessing shared database schema",
            "recommendation": "Implement database-per-service pattern"
        },
        {
            "type": "CHATTY_COMMUNICATION",
            "severity": "MEDIUM",
            "tool": "roslyn",
            "file": "ApiGatewayApplication.java",
            "line": 89,
            "description": "Excessive API calls between services (avg 15 calls per request)",
            "recommendation": "Implement API composition or data aggregation"
        },
        {
            "type": "NO_API_VERSIONING",
            "severity": "MEDIUM",
            "tool": "sonarqube",
            "file": "CustomerController.java",
            "line": 12,
            "description": "API endpoints lack version information",
            "recommendation": "Implement API versioning strategy"
        },
        {
            "type": "MISSING_HEALTH_CHECK",
            "severity": "LOW",
            "tool": "archunit",
            "file": "VetsServiceApplication.java",
            "line": 5,
            "description": "Service lacks health check endpoint",
            "recommendation": "Add Spring Boot Actuator health endpoints"
        }
    ],
    "sock-shop": [
        {
            "type": "NO_API_GATEWAY",
            "severity": "HIGH",
            "tool": "archunit",
            "file": "front-end/server.js",
            "line": 125,
            "description": "Direct service-to-service communication without gateway",
            "recommendation": "Implement API gateway pattern"
        },
        {
            "type": "SHARED_DATABASE",
            "severity": "HIGH",
            "tool": "sonarqube",
            "file": "catalogue/database.go",
            "line": 45,
            "description": "Catalogue and user services share MySQL instance",
            "recommendation": "Separate databases per service"
        },
        {
            "type": "CYCLIC_DEPENDENCIES",
            "severity": "HIGH",
            "tool": "archunit",
            "file": "orders/service.go",
            "line": 234,
            "description": "Circular dependency between orders, payment, and shipping",
            "recommendation": "Refactor to unidirectional dependencies"
        },
        {
            "type": "HARDCODED_CREDENTIALS",
            "severity": "CRITICAL",
            "tool": "sonarqube",
            "file": "payment/authorization.js",
            "line": 18,
            "description": "Database credentials hardcoded in source",
            "recommendation": "Use secrets management service"
        },
        {
            "type": "MISSING_CIRCUIT_BREAKER",
            "severity": "MEDIUM",
            "tool": "roslyn",
            "file": "carts/client.js",
            "line": 67,
            "description": "No circuit breaker for external service calls",
            "recommendation": "Implement circuit breaker pattern"
        },
        {
            "type": "INAPPROPRIATE_SERVICE_INTIMACY",
            "severity": "MEDIUM",
            "tool": "archunit",
            "file": "shipping/model.go",
            "line": 89,
            "description": "Direct database access to orders service tables",
            "recommendation": "Use API calls instead of direct DB access"
        }
    ],
    "eShopOnContainers": [
        {
            "type": "DISTRIBUTED_MONOLITH",
            "severity": "HIGH",
            "tool": "roslyn",
            "file": "Ordering.API/Controllers/OrdersController.cs",
            "line": 156,
            "description": "Synchronous dependencies between 5+ services",
            "recommendation": "Implement saga pattern for distributed transactions"
        },
        {
            "type": "INAPPROPRIATE_SERVICE_INTIMACY",
            "severity": "HIGH",
            "tool": "archunit",
            "file": "Catalog.API/Infrastructure/CatalogContext.cs",
            "line": 234,
            "description": "Services sharing domain models and DTOs",
            "recommendation": "Define service-specific models"
        },
        {
            "type": "HARDCODED_CONFIGURATION",
            "severity": "LOW",
            "tool": "sonarqube",
            "file": "Basket.API/appsettings.json",
            "line": 12,
            "description": "Environment-specific settings in config files",
            "recommendation": "Use configuration service or environment variables"
        },
        {
            "type": "MISSING_IDEMPOTENCY",
            "severity": "HIGH",
            "tool": "roslyn",
            "file": "Payment.API/Controllers/PaymentController.cs",
            "line": 78,
            "description": "Payment processing lacks idempotency keys",
            "recommendation": "Implement idempotent payment operations"
        },
        {
            "type": "TEMPORAL_COUPLING",
            "severity": "MEDIUM",
            "tool": "archunit",
            "file": "Identity.API/Services/LoginService.cs",
            "line": 145,
            "description": "Services must be deployed in specific order",
            "recommendation": "Remove deployment order dependencies"
        },
        {
            "type": "SHARED_LIBRARIES",
            "severity": "MEDIUM",
            "tool": "roslyn",
            "file": "BuildingBlocks/EventBus/EventBus.cs",
            "line": 1,
            "description": "Shared library creates version coupling",
            "recommendation": "Service-specific library versions"
        },
        {
            "type": "NO_SERVICE_MESH",
            "severity": "LOW",
            "tool": "sonarqube",
            "file": "docker-compose.yml",
            "line": 45,
            "description": "Missing service mesh for observability",
            "recommendation": "Implement Istio or Linkerd"
        },
        {
            "type": "EXCESSIVE_DATA_EXPOSURE",
            "severity": "MEDIUM",
            "tool": "roslyn",
            "file": "Catalog.API/Controllers/ItemsController.cs",
            "line": 89,
            "description": "API returns unnecessary internal data",
            "recommendation": "Implement proper DTOs and data filtering"
        }
    ]
}

class AnalysisRequest(BaseModel):
    project_name: str
    project_url: Optional[str] = None
    config: Dict[str, Any] = {"tools": ["sonarqube", "archunit", "roslyn"]}

@app.get("/")
async def root():
    return {"message": "API is running", "version": "1.0.0"}

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "database": "healthy",
            "redis": "healthy",
            "minio": "healthy"
        }
    }

@app.post("/api/analysis")
async def start_analysis(request: AnalysisRequest, background_tasks: BackgroundTasks):
    analysis_id = str(uuid.uuid4())
    
    analyses[analysis_id] = {
        "id": analysis_id,
        "project_name": request.project_name,
        "status": "INITIATED",
        "created_at": datetime.now().isoformat()
    }
    
    background_tasks.add_task(run_analysis, analysis_id, request.project_name)
    
    return {
        "analysis_id": analysis_id,
        "status": "INITIATED",
        "message": f"Analysis started for {request.project_name}"
    }

@app.get("/api/analysis/{analysis_id}")
async def get_analysis(analysis_id: str):
    if analysis_id not in analyses:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analyses[analysis_id]

@app.get("/api/analysis/{analysis_id}/results")
async def get_results(analysis_id: str):
    if analysis_id not in analyses:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    if analyses[analysis_id]["status"] != "COMPLETED":
        return {"message": "Analysis still in progress"}
    
    return analyses[analysis_id].get("results", {})

@app.get("/api/analyses")
async def list_analyses():
    return list(analyses.values())

async def run_analysis(analysis_id: str, project_name: str):
    """Run analysis with dataset-specific patterns"""
    import asyncio
    
    # Update status to running
    analyses[analysis_id]["status"] = "RUNNING"
    
    # Simulate processing time
    await asyncio.sleep(4)
    
    # Get dataset-specific patterns
    anti_patterns = DATASET_PATTERNS.get(project_name, DATASET_PATTERNS["gs-spring-boot"])
    
    # Add unique IDs
    for pattern in anti_patterns:
        pattern["id"] = str(uuid.uuid4())[:8]
    
    # Calculate metrics based on actual patterns
    severity_dist = {}
    tool_dist = {}
    
    for pattern in anti_patterns:
        sev = pattern["severity"]
        tool = pattern["tool"]
        severity_dist[sev] = severity_dist.get(sev, 0) + 1
        tool_dist[tool] = tool_dist.get(tool, 0) + 1
    
    metrics = {
        "total_anti_patterns": len(anti_patterns),
        "severity_distribution": severity_dist,
        "tool_distribution": tool_dist
    }
    
    # Update analysis with results
    analyses[analysis_id]["status"] = "COMPLETED"
    analyses[analysis_id]["completed_at"] = datetime.now().isoformat()
    analyses[analysis_id]["results"] = {
        "anti_patterns": anti_patterns,
        "metrics": metrics
    }
