<?php
session_start();

// Check if form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Check username and password (replace with your validation logic)
    $valid_username = "username";
    $valid_password = "password";

    if ($_POST['user'] == $valid_username && $_POST['password'] == $valid_password) {
        // Set session variable
        $_SESSION['username'] = $_POST['user'];
        // Redirect to welcome page
        header("Location: welcome.php");
        exit();
    } else {
        echo "Invalid username or password.";
    }
}
?>
