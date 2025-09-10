import os
import re
from typing import List, Dict, Set
from collections import defaultdict

class SimpleRealDetector:
    """
    Enhanced pattern detector with real code analysis.
    Includes simple + some medium complexity features that are stable.
    """
    
    def __init__(self):
        # Microservice anti-pattern keywords
        self.db_patterns = ['jdbc://', 'mongodb://', 'mysql://', 'postgresql://', 'localhost:']
        self.sync_patterns = ['synchronized', '.wait()', '.Result', 'Thread.sleep']
        self.shared_patterns = ['SharedDatabase', 'SharedRepository', 'CommonDB']
        
    def detect_patterns(self, project_path: str) -> List[Dict]:
        patterns = []
        service_dependencies = defaultdict(set)  # Medium feature: track dependencies
        files_analyzed = 0
        max_files = 15
        
        # Scan project files
        for root, dirs, files in os.walk(project_path):
            if files_analyzed >= max_files:
                break
                
            for file in files:
                if files_analyzed >= max_files:
                    break
                    
                filepath = os.path.join(root, file)
                
                # Analyze Java files
                if file.endswith('.java'):
                    files_analyzed += 1
                    patterns.extend(self._analyze_java_file(filepath, file))
                    deps = self._extract_dependencies(filepath)
                    if deps:
                        service_dependencies[file].update(deps)
                
                # Analyze configuration files (medium feature)
                elif file.endswith(('.properties', '.yml', '.yaml')):
                    patterns.extend(self._analyze_config_file(filepath, file))
        
        # Medium feature: Detect circular dependencies
        circular = self._detect_circular_deps(service_dependencies)
        if circular:
            patterns.append({
                "type": "CIRCULAR_DEPENDENCIES",
                "severity": "HIGH",
                "tool": "dependency_analyzer",
                "file": "Multiple Services",
                "line": 0,
                "description": f"Circular dependency detected: {circular}",
                "recommendation": "Refactor to remove circular dependencies"
            })
        
        # Medium feature: Detect too many dependencies (god service)
        for service, deps in service_dependencies.items():
            if len(deps) > 5:
                patterns.append({
                    "type": "GOD_SERVICE",
                    "severity": "MEDIUM",
                    "tool": "dependency_analyzer",
                    "file": service,
                    "line": 0,
                    "description": f"Service has {len(deps)} dependencies (too many)",
                    "recommendation": "Consider splitting into smaller services"
                })
        
        return patterns[:10]  # Limit output for clarity
    
    def _analyze_java_file(self, filepath: str, filename: str) -> List[Dict]:
        """Analyze Java file for anti-patterns"""
        patterns = []
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
                
                # Check for hardcoded connections
                for i, line in enumerate(lines, 1):
                    for db_pattern in self.db_patterns:
                        if db_pattern in line:
                            patterns.append({
                                "type": "HARDCODED_CONNECTION",
                                "severity": "HIGH",
                                "tool": "pattern_detector",
                                "file": filename,
                                "line": i,
                                "description": f"Hardcoded connection: {line.strip()[:50]}",
                                "recommendation": "Use environment variables or config service"
                            })
                            break
                
                # Check for synchronous patterns
                for i, line in enumerate(lines, 1):
                    for sync_pattern in self.sync_patterns:
                        if sync_pattern in line:
                            patterns.append({
                                "type": "SYNCHRONOUS_BLOCKING",
                                "severity": "HIGH",
                                "tool": "pattern_detector",
                                "file": filename,
                                "line": i,
                                "description": f"Blocking operation: {sync_pattern}",
                                "recommendation": "Use async/reactive patterns"
                            })
                            break
                
                # Check for shared persistence
                if any(shared in content for shared in self.shared_patterns):
                    patterns.append({
                        "type": "SHARED_PERSISTENCE",
                        "severity": "HIGH",
                        "tool": "pattern_detector",
                        "file": filename,
                        "line": 0,
                        "description": "Shared database/repository detected",
                        "recommendation": "Implement database-per-service pattern"
                    })
                
                # Medium feature: Check method count (god service indicator)
                public_methods = len(re.findall(r'public\s+\w+\s+\w+\s*\(', content))
                if public_methods > 10:
                    patterns.append({
                        "type": "GOD_SERVICE",
                        "severity": "MEDIUM",
                        "tool": "complexity_analyzer",
                        "file": filename,
                        "line": 0,
                        "description": f"Service has {public_methods} public methods",
                        "recommendation": "Consider splitting into smaller services"
                    })
                
                # Medium feature: Check for missing error handling
                if 'try' not in content and ('HttpClient' in content or 'RestTemplate' in content):
                    patterns.append({
                        "type": "MISSING_ERROR_HANDLING",
                        "severity": "MEDIUM",
                        "tool": "pattern_detector",
                        "file": filename,
                        "line": 0,
                        "description": "HTTP calls without error handling",
                        "recommendation": "Add proper error handling and circuit breakers"
                    })
                    
        except Exception as e:
            # Silent fail - just skip this file
            pass
            
        return patterns
    
    def _analyze_config_file(self, filepath: str, filename: str) -> List[Dict]:
        """Analyze configuration files for anti-patterns"""
        patterns = []
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Check for hardcoded URLs in config
                if 'localhost' in content or '127.0.0.1' in content:
                    patterns.append({
                        "type": "HARDCODED_ENDPOINTS",
                        "severity": "MEDIUM",
                        "tool": "config_analyzer",
                        "file": filename,
                        "line": 0,
                        "description": "Hardcoded localhost/IP in configuration",
                        "recommendation": "Use environment-specific configuration"
                    })
                
                # Check for hardcoded passwords
                if re.search(r'password\s*=\s*["\'][\w]+["\']', content, re.IGNORECASE):
                    patterns.append({
                        "type": "HARDCODED_CREDENTIALS",
                        "severity": "CRITICAL",
                        "tool": "security_analyzer",
                        "file": filename,
                        "line": 0,
                        "description": "Hardcoded password in configuration",
                        "recommendation": "Use secrets management service"
                    })
                    
        except:
            pass
            
        return patterns
    
    def _extract_dependencies(self, filepath: str) -> Set[str]:
        """Extract service dependencies from imports"""
        dependencies = set()
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Find imports that look like other services
                imports = re.findall(r'import\s+[\w.]+\.(\w+Service);', content)
                dependencies.update(imports)
                
                # Find RestTemplate/WebClient calls
                service_calls = re.findall(r'["\']http://(\w+)-service', content)
                dependencies.update(service_calls)
                
        except:
            pass
            
        return dependencies
    
    def _detect_circular_deps(self, deps: Dict[str, Set[str]]) -> str:
        """Simple circular dependency detection"""
        for service_a, deps_a in deps.items():
            for service_b in deps_a:
                if service_b in deps:
                    if any(service_a in dep for dep in deps[service_b]):
                        return f"{service_a} <-> {service_b}"
        return ""
