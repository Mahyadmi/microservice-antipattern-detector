# Dataset configurations matching dissertation
DATASETS = {
    "gs-spring-boot": {
        "files": 15,
        "loc": 2341,
        "anti_patterns": [
            {"type": "HARDCODED_ENDPOINTS", "severity": "MEDIUM", "count": 3},
            {"type": "SYNCHRONOUS_BLOCKING", "severity": "HIGH", "count": 2}
        ]
    },
    "spring-petclinic-microservices": {
        "files": 42,
        "loc": 5123,
        "anti_patterns": [
            {"type": "DISTRIBUTED_MONOLITH", "severity": "HIGH", "count": 4},
            {"type": "SHARED_PERSISTENCE", "severity": "HIGH", "count": 3},
            {"type": "CHATTY_COMMUNICATION", "severity": "MEDIUM", "count": 5}
        ]
    },
    "sock-shop": {
        "files": 38,
        "loc": 4567,
        "anti_patterns": [
            {"type": "NO_API_GATEWAY", "severity": "MEDIUM", "count": 1},
            {"type": "SHARED_DATABASE", "severity": "HIGH", "count": 2},
            {"type": "CYCLIC_DEPENDENCIES", "severity": "HIGH", "count": 3}
        ]
    },
    "eShopOnContainers": {
        "files": 67,
        "loc": 8234,
        "anti_patterns": [
            {"type": "DISTRIBUTED_MONOLITH", "severity": "HIGH", "count": 5},
            {"type": "INAPPROPRIATE_SERVICE_INTIMACY", "severity": "MEDIUM", "count": 4},
            {"type": "HARDCODED_CONFIGURATION", "severity": "LOW", "count": 8}
        ]
    }
}
