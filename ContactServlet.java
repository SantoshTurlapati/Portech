import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/ContactServlet")
public class ContactServlet extends HttpServlet {
    
    // Database credentials setup
    private static final String DB_URL = "jdbc:mysql://localhost:3306/portech_database";
    private static final String USER = "root";
    private static final String PASS = "your_secure_password";

    protected void doPost(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        
        // 1. Capture the data from the HTML form
        String clientName = request.getParameter("userName");
        String clientEmail = request.getParameter("userEmail");
        
        response.setContentType("text/html");
        PrintWriter out = response.getWriter();
        
        try {
            // 2. Load the JDBC Driver
            Class.forName("com.mysql.cj.jdbc.Driver");
            
            // 3. Establish Database Connection
            Connection conn = DriverManager.getConnection(DB_URL, USER, PASS);
            
            // 4. Create SQL Query & use PreparedStatement to prevent SQL Injection
            String sql = "INSERT INTO contact_requests (name, email) VALUES (?, ?)";
            PreparedStatement pstmt = conn.prepareStatement(sql);
            pstmt.setString(1, clientName);
            pstmt.setString(2, clientEmail);
            
            // 5. Execute Update
            int rowsAffected = pstmt.executeUpdate();
            
            if (rowsAffected > 0) {
                out.println("<div style='text-align:center; margin-top:50px; font-family:sans-serif;'>");
                out.println("<h2 style='color: #3b82f6;'>Thank you, " + clientName + "!</h2>");
                out.println("<p>Your information has been successfully secured in the database.</p>");
                out.println("<a href='about.html' style='color:#333;'>Return to About Page</a>");
                out.println("</div>");
            }
            
            // 6. Clean up resources
            pstmt.close();
            conn.close();
            
        } catch (Exception e) {
            out.println("<h3>System Error: " + e.getMessage() + "</h3>");
        }
    }
}