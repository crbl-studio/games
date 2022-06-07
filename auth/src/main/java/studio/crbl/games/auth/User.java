public class User {
    private String email;
    private String password;
    private boolean admin = false;
    private boolean activeAcc = false;

    //TODO: Encrypt password
    public User(String email, String password) {
        this.email = email;
        this.password = password;
    }

    public void setPassword(String newPassword) {
        this.password = newPassword;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getEmail() {
        return this.email;
    }

    public String getPassword() {
        return this.password;
    }

}
