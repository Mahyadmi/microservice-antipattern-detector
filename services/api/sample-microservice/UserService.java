import com.example.OrderService;
import com.example.PaymentService;

public class UserService {
    private String dbUrl = "jdbc://localhost:3306/users";  // Will be detected
    
    public synchronized void updateUser(String userId) {  // Will be detected
        Thread.sleep(1000);  // Will be detected
    }
    
    public void deleteUser() {} 
    public void getUser() {}
    public void listUsers() {}
    public void searchUsers() {}
    public void exportUsers() {}
    public void importUsers() {}
    public void validateUser() {}
    public void authenticateUser() {}
    public void authorizeUser() {}
    public void refreshToken() {}  // Too many methods - will trigger GOD_SERVICE
}
