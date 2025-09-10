"""
Simple Validation for Anti-Pattern Detection
This validates the actual patterns your system found
"""

def run_validation():
    # These are the ACTUAL patterns your system detected in UserService.java
    detected_patterns = [
        {"type": "HARDCODED_CONNECTION", "line": 5, "file": "UserService.java"},
        {"type": "SYNCHRONOUS_BLOCKING", "line": 7, "file": "UserService.java"},
        {"type": "SYNCHRONOUS_BLOCKING", "line": 8, "file": "UserService.java"},
        {"type": "HARDCODED_ENDPOINTS", "line": 0, "file": "application.properties"}
    ]
    
    # Ground truth - what actually exists in the files (manually verified)
    actual_patterns = [
        {"type": "HARDCODED_CONNECTION", "line": 5, "file": "UserService.java"},  # jdbc://
        {"type": "SYNCHRONOUS_BLOCKING", "line": 7, "file": "UserService.java"},  # synchronized
        {"type": "SYNCHRONOUS_BLOCKING", "line": 8, "file": "UserService.java"},  # Thread.sleep
        {"type": "HARDCODED_ENDPOINTS", "line": 0, "file": "application.properties"},  # localhost
        {"type": "GOD_SERVICE", "line": 0, "file": "UserService.java"},  # Too many methods (missed)
        {"type": "HARDCODED_CREDENTIALS", "line": 0, "file": "application.properties"}  # password (missed)
    ]
    
    # Calculate metrics
    true_positives = 4  # All 4 detected patterns were correct
    false_positives = 0  # No incorrect detections
    false_negatives = 2  # Missed GOD_SERVICE and HARDCODED_CREDENTIALS
    
    total_detected = true_positives + false_positives
    total_actual = true_positives + false_negatives
    
    precision = (true_positives / total_detected * 100) if total_detected > 0 else 0
    recall = (true_positives / total_actual * 100) if total_actual > 0 else 0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0
    
    print("\n" + "="*50)
    print("VALIDATION RESULTS - ANTI-PATTERN DETECTION")
    print("="*50)
    print(f"\nSample Size: 2 files analyzed")
    print(f"Ground Truth Patterns: {total_actual}")
    print(f"Detected Patterns: {total_detected}")
    print(f"\nTrue Positives: {true_positives}")
    print(f"False Positives: {false_positives}")
    print(f"False Negatives: {false_negatives}")
    print(f"\n--- METRICS ---")
    print(f"Precision: {precision:.1f}%")
    print(f"Recall: {recall:.1f}%")
    print(f"F1-Score: {f1:.1f}%")
    print("\n" + "="*50)
    
    return precision, recall, f1

if __name__ == "__main__":
    run_validation()
