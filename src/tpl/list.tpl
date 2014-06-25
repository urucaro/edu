<html>

<head>

<link rel="stylesheet" 
    type="text/css" 
    href="/mystyle.css">
    
<title>All Episodes</title>


<h1> {{other['heading1']}} </h1>

<h2> {{other['title']}}</h2>
<h3> {{get('nr','')}}</h3>

</head>


<body>
<ul>
%   for d in data:
%       new = d.replace('_',' ')
        <li> {{new}}</li>
    %end
<ul/>
</body>

</html>
