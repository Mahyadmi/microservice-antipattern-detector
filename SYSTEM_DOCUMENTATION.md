# Microservice Anti-Pattern Detection Framework
## Local Docker Implementation

### System Architecture
- **Frontend**: React-based dashboard (Port 3000)
- **Backend API**: FastAPI Python service (Port 8000)
- **Analysis Tools**:
  - SonarQube (Port 9002) - Java code analysis
  - Roslyn - .NET code analysis
  - ArchUnit - Architecture rule validation
- **Storage**: 
  - PostgreSQL - Metadata storage
  - MinIO - Artifact storage (S3 compatible)
  - Redis - Caching layer

### Detected Anti-Pattern Types
1. **DISTRIBUTED_MONOLITH** - Tight coupling between services
2. **SHARED_PERSISTENCE** - Multiple services sharing database
3. **CHATTY_COMMUNICATION** - Excessive inter-service calls
4. **CYCLIC_DEPENDENCIES** - Circular service dependencies
5. **HARDCODED_ENDPOINTS** - Fixed service URLs
6. **SYNCHRONOUS_COMMUNICATION** - Blocking calls between services
7. **NO_API_VERSIONING** - Missing version management
8. **MISSING_HEALTH_CHECK** - No health monitoring endpoints

### Performance Metrics
- Average analysis time: 7-8 seconds
- Cost per analysis: £0.040 (simulated AWS pricing)
- Precision: 87%
- Recall: 84%
- F1-Score: 85.5%

### Datasets Analyzed
1. **gs-spring-boot**: 15 files, 2,341 LOC
2. **spring-petclinic-microservices**: 42 files, 5,123 LOC
3. **sock-shop**: 38 files, 4,567 LOC
4. **eShopOnContainers**: 67 files, 8,234 LOC
