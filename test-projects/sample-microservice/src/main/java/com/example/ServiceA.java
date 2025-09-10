package com.example;

public class ServiceA {
    // Anti-pattern: Hardcoded database URL (shared persistence)
    private static final String DB_URL = "jdbc:postgresql://localhost:5432/shared_db";
    
    // Anti-pattern: Hardcoded service endpoint
    private static final String SERVICE_B_URL = "http://localhost:8081/api";
    
    // Anti-pattern: Synchronous blocking call
    public String callServiceB() {
        return makeHttpCall(SERVICE_B_URL);
    }
    
    private String makeHttpCall(String url) {
        // Simulated synchronous HTTP call
        return "response";
    }
}
