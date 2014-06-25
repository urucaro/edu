<html>
<head>
<link rel="icon" 
      type="image/png" 
      href="favicon.ico">
      
<link rel="stylesheet" 
    type="text/css" 
    href="/mystyle.css">
    
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    
<title>Carolinas TV-Series</title>

<h1>Welcome to Carolinas TV-series page</h1>

<p> {{other['prefix']}}<p/>

<script type="text/javascript">


function GoUrlTitles()
{
   window.location.href = "series";
}

</script>

<script>
$(document).ready(function(){
  $("#p1").hover(function(){
    alert("You entered p1!");
    },
    function(){
    alert("Bye! You now leave p1!");
  }); 
});
</script>
</head>
<body>

</head>
<body>

<p id="test"> Klicka här för att testa</p>
<button>Klicka här för att testa</button>
<p id="p1">Enter this paragraph.</p>

<a href="javascript:GoUrlTitles()">Click here</a> to go to all the series titles.

</body>
</html>
