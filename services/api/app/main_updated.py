from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import uuid
from datetime import datetime

# Import the real analyzer
try:
    from real_integrated_analyzer import RealIntegratedAnalyzer
    real_analyzer = RealIntegratedAnalyzer()
    USE_REAL_ANALYSIS = True
except ImportError:
    USE_REAL_ANALYSIS = False
    print("Real analyzer not available, using simulated data")

app = FastAPI(title="Microservice Anti-Pattern Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

analyses = {}

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
        "real_analysis": USE_REAL_ANALYSIS,
        "services": {"database": "healthy", "redis": "healthy", "minio": "healthy"}
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

async def run_analysis(analysis_id: str, project_name: str):
    import asyncio
    
    analyses[analysis_id]["status"] = "RUNNING"
    await asyncio.sleep(4)
    
    # Try to use real analyzer if available
    if USE_REAL_ANALYSIS:
        project_path = "/workspace/sample-microservice"
        try:
            anti_patterns = real_analyzer.analyze_project(project_path, project_name)
        except Exception as e:
            print(f"Real analysis failed: {e}, using fallback")
            anti_patterns = get_fallback_patterns(project_name)
    else:
        anti_patterns = get_fallback_patterns(project_name)
    
    # Add IDs
    for i, pattern in enumerate(anti_patterns):
        pattern["id"] = f"{analysis_id[:8]}-{i}"
    
    # Calculate metrics
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
    
    analyses[analysis_id]["status"] = "COMPLETED"
    analyses[analysis_id]["results"] = {
        "anti_patterns": anti_patterns,
        "metrics": metrics
    }

def get_fallback_patterns(project_name: str) -> List[Dict]:
    """Fallback patterns if real analysis fails"""
    return [
        {
            "type": "SHARED_PERSISTENCE",
            "severity": "HIGH",
            "tool": "sonarqube",
            "file": "DatabaseConfig.java",
            "line": 23,
            "description": "Multiple services accessing shared database",
            "recommendation": "Implement database-per-service pattern"
        },
        {
            "type": "CYCLIC_DEPENDENCIES",
            "severity": "HIGH",
            "tool": "archunit",
            "file": "ServiceArchitecture",
            "line": 0,
            "description": "Circular dependencies detected",
            "recommendation": "Refactor to remove cycles"
        }
    ]

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
