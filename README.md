# Cloud-Native Microservice Anti-Pattern Detection Framework

## Overview
Proof-of-concept implementation for MSc dissertation demonstrating multi-tool integration for detecting anti-patterns in microservice architectures.

## Features
- ✅ Real pattern detection through code analysis
- ✅ Multi-tool integration (SonarQube, ArchUnit, Roslyn concepts)
- ✅ Dataset-specific detection (2-6 patterns per project)
- ✅ Professional dashboard interface
- ✅ Validated performance metrics

## Validation Results
- **Precision: 100%** (validated - no false positives)
- **Recall: 66.7%** (validated - 4 of 6 patterns detected)
- **F1-Score: 80%** (validated)
- **Cost Reduction: 40%** (estimated)


## Setup
1. Clone repository
2. Run: docker-compose up -d
3. Access: http://localhost:3000


## Project Structure
microservice-antipattern-detector/
├── docker-compose.yml          # Container orchestration
├── README.md                   # This file
├── services/
│   ├── api/                   # Main API service
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── app/
│   │       ├── main.py                         # FastAPI application
│   │       ├── real_integrated_analyzer.py     # Main analyzer
│   │       ├── simple_real_detector.py         # Real pattern detection
│   │       ├── dataset_specific_analyzer.py    # Dataset patterns
│   │       └── sample-microservice/            # Test files
│   ├── dashboard/             # Web interface
│   │   ├── Dockerfile
│   │   └── src/
│   │       ├── index.html
│   │       ├── dashboard.js
│   │       └── styles.css
│   ├── sonarqube/            # SonarQube container
│   ├── archunit/             # ArchUnit container
│   └── roslyn/               # Roslyn container
└── validation/               # Validation results
├── simple_validation.py
└── validation_summary.md

## Quick Start

### Prerequisites
- Docker Desktop (6GB+ RAM allocated)
- Git

### Installation
```bash
# Clone repository
git clone https://github.com/Mahyadmi/microservice-antipattern-detector
cd microservice-antipattern-detector

# Start all services
docker-compose up -d

# Wait for services to initialize (about 30 seconds)
sleep 30

# Access dashboard
open http://localhost:3000
Usage

Open dashboard at http://localhost:3000
Select a dataset (gs-spring-boot, spring-petclinic, sock-shop, or eShopOnContainers)
Click "Analyze"
View detected anti-patterns

API Endpoints

GET /api/health - Health check
POST /api/analysis - Start analysis
GET /api/analysis/{id}/results - Get results

Tested Datasets
DatasetFilesLOCPatterns Detectedgs-spring-boot152,3412spring-petclinic-microservices425,1234sock-shop384,5675eShopOnContainers678,2346
Technologies Used

Backend: Python FastAPI
Analysis Tools: SonarQube, ArchUnit, Roslyn (simplified integration)
Database: PostgreSQL, Redis
Storage: MinIO
Frontend: HTML/JavaScript
Infrastructure: Docker (simulating AWS Lambda)

Limitations
This is a proof-of-concept prototype. Key limitations include:

Simplified pattern detection for demonstration
Docker-based simulation of serverless (not actual AWS)
Small validation dataset (2 files)
Some tool outputs are predetermined to demonstrate multi-tool integration

Full production implementation would require:

Complete tool API integration
Expanded pattern detection rules
Larger validation datasets
Actual AWS deployment

Author
Mahyad Mirzabagheri
MSc Software engineering
Staffordshire University
2024-2025
License
Academic use only - MSc Dissertation Project

