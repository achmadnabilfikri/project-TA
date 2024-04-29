<?php
session_start();

// Check if user is logged in
if (!isset($_SESSION['username'])) {
    header("Location: login.php");
    exit();
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome</title>
</head>
<body>
        
    
    {% extends 'base.html' %} {% block content %}
    
    <br />
    <p class="fs-2 text-center">{% if 'username' in session %}
     Hi {{ session['username'] }},
    {% endif %} Selamat Datang di</p>
    <br />
    <h1 class="display-1 text-center fw-bold">SIKASI COV</h1>
    <p class="fs-5 text-center">Sistem Klasifikasi Gambar Sinar X COVID-19</p>
    <br />
    <br />
    <div class="row justify-content-center">
        <div class="col-sm-4">
            <img src="{{ image }}" class="img-fluid rounded" alt="Image" />
            <!-- https://www.freepik.com/free-photo/medical-supplies-items-composition-blue-surface-stack-pill-packs-top-view_13854339.htm#query=medicine&position=0&from_view=search&track=sph#position=0&query=medicine -->
        </div>
    </div>

    {% endblock %}
</body>
</html>