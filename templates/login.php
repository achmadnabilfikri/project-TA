<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"
      rel="stylesheet"
      integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3"
      crossorigin="anonymous"
    />
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>

    <script src="https://cdn.datatables.net/1.10.16/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/1.10.16/js/dataTables.bootstrap4.min.js"></script>


<script>
function clearLoginForm() {
    document.getElementById("username").value = "";
    document.getElementById("password").value = "";
}
</script>
</head>
<body>
{% with messages =
get_flashed_messages(with_categories=True) %} {% if messages %}
<script>
  {% for category, message in messages %}
    {% if category == 'invalid' %}
      alert('{{ message }}');
    {% endif %}
  {% endfor %}
</script>
{% endif %} {% endwith %}
<nav class="navbar navbar-expand-lg navbar-dark bg-danger">
  <div class="container-fluid">
    <a class="navbar-brand" href="/welcome">SIKASI COV</a>
    <button
      class="navbar-toggler"
      type="button"
      data-bs-toggle="collapse"
      data-bs-target="#navbarSupportedContent"
      aria-controls="navbarSupportedContent"
      aria-expanded="false"
      aria-label="Toggle navigation"
    >
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
      </ul>
    </div>
  </div>
</nav>



<div class="wrapper-ah">
    <div class="row justify-content-center">
        <div class="col-md-4 col-md-offset-4">
            <div class="panel panel-default">
                <div class="panel-heading">
                <h3 class="panel-title text-center">Login</h3>
                
                </div>
                <div class="panel-body">
                    <form id="loginForm" action="/login" method="post">
                        <div class="form-group">
                            <label> Username </label>
                            <input type="text" id="username" name="username" value="{{ '' if clear_form else username }}" class="form-control" required><br></input>
                        </div>
                        <div class="form-group">
                            <label> Password </label>
                            <input type="password" id="password" name="password" value="" class="form-control" required><br></input>
                        </div>
                        <div class="form-group text-center"> 
                        <button type="submit" class="btn btn-primary">Masuk</button> 
                        </div>
                    </form>
                </div>            
            </div>  
        </div>
    </div>
</div>



</body>
</html>
