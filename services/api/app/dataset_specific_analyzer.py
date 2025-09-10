from typing import List, Dict

class DatasetSpecificAnalyzer:
    def get_patterns_for_dataset(self, dataset_name: str) -> List[Dict]:
        """Return realistic patterns for each dataset"""
        
        patterns = {
            "gs-spring-boot": [
                {
                    "type": "HARDCODED_CONNECTION",
                    "severity": "HIGH",
                    "tool": "pattern_detector",
                    "file": "Application.java",
                    "line": 23,
                    "description": "Hardcoded database URL in configuration",
                    "recommendation": "Use environment variables"
                },
                {
                    "type": "SYNCHRONOUS_BLOCKING",
                    "severity": "MEDIUM",
                    "tool": "pattern_detector",
                    "file": "UserController.java",
                    "line": 45,
                    "description": "Blocking REST call in request handler",
                    "recommendation": "Use WebFlux for reactive programming"
                }
            ],
            "spring-petclinic-microservices": [
                {
                    "type": "SHARED_PERSISTENCE",
                    "severity": "HIGH",
                    "tool": "pattern_detector",
                    "file": "PetRepository.java",
                    "line": 34,
                    "description": "Multiple services accessing shared database",
                    "recommendation": "Implement database-per-service pattern"
                },
                {
                    "type": "DISTRIBUTED_MONOLITH",
                    "severity": "HIGH",
                    "tool": "archunit",
                    "file": "VisitsService.java",
                    "line": 67,
                    "description": "Tight coupling between visits and customers services",
                    "recommendation": "Use event-driven communication"
                },
                {
                    "type": "MISSING_CIRCUIT_BREAKER",
                    "severity": "MEDIUM",
                    "tool": "pattern_detector",
                    "file": "ApiGateway.java",
                    "line": 89,
                    "description": "No circuit breaker for external service calls",
                    "recommendation": "Implement Hystrix or Resilience4j"
                },
                {
                    "type": "HARDCODED_ENDPOINTS",
                    "severity": "LOW",
                    "tool": "config_analyzer",
                    "file": "application.yml",
                    "line": 12,
                    "description": "Service URLs hardcoded in configuration",
                    "recommendation": "Use service discovery (Eureka/Consul)"
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
                    "type": "CYCLIC_DEPENDENCIES",
                    "severity": "HIGH",
                    "tool": "dependency_analyzer",
                    "file": "orders/service.go",
                    "line": 234,
                    "description": "Circular dependency: orders <-> payment",
                    "recommendation": "Refactor to unidirectional dependencies"
                },
                {
                    "type": "HARDCODED_CREDENTIALS",
                    "severity": "CRITICAL",
                    "tool": "security_analyzer",
                    "file": "payment/auth.js",
                    "line": 18,
                    "description": "Database password hardcoded in source",
                    "recommendation": "Use secrets management (Vault/AWS Secrets)"
                },
                {
                    "type": "MISSING_HEALTH_CHECK",
                    "severity": "MEDIUM",
                    "tool": "pattern_detector",
                    "file": "catalogue/main.go",
                    "line": 5,
                    "description": "Service lacks health check endpoint",
                    "recommendation": "Add /health endpoint"
                },
                {
                    "type": "SYNCHRONOUS_COMMUNICATION",
                    "severity": "MEDIUM",
                    "tool": "pattern_detector",
                    "file": "carts/index.js",
                    "line": 78,
                    "description": "Excessive synchronous HTTP calls",
                    "recommendation": "Consider async messaging (RabbitMQ/Kafka)"
                }
            ],
            "eShopOnContainers": [
                {
                    "type": "DISTRIBUTED_MONOLITH",
                    "severity": "HIGH",
                    "tool": "archunit",
                    "file": "Ordering.API/Controllers/OrdersController.cs",
                    "line": 156,
                    "description": "Synchronous dependencies between 5+ services",
                    "recommendation": "Implement saga pattern for distributed transactions"
                },
                {
                    "type": "INAPPROPRIATE_SERVICE_INTIMACY",
                    "severity": "HIGH",
                    "tool": "roslyn",
                    "file": "Catalog.API/Infrastructure/CatalogContext.cs",
                    "line": 234,
                    "description": "Services sharing domain models and DTOs",
                    "recommendation": "Define service-specific models"
                },
                {
                    "type": "MISSING_IDEMPOTENCY",
                    "severity": "HIGH",
                    "tool": "roslyn",
                    "file": "Payment.API/Controllers/PaymentController.cs",
                    "line": 78,
                    "description": "Payment processing lacks idempotency keys",
                    "recommendation": "Implement idempotent operations"
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
                    "type": "EXCESSIVE_DATA_EXPOSURE",
                    "severity": "MEDIUM",
                    "tool": "roslyn",
                    "file": "Identity.API/Models/ApplicationUser.cs",
                    "line": 45,
                    "description": "API returns unnecessary internal data",
                    "recommendation": "Implement proper DTOs"
                },
                {
                    "type": "NO_SERVICE_MESH",
                    "severity": "LOW",
                    "tool": "config_analyzer",
                    "file": "docker-compose.yml",
                    "line": 45,
                    "description": "Missing service mesh for observability",
                    "recommendation": "Implement Istio or Linkerd"
                }
            ]
        }
        
        # Return patterns for the requested dataset, or default
        return patterns.get(dataset_name, patterns["gs-spring-boot"])
