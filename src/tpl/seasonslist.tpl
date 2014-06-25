<html>
<head>

<link rel="stylesheet" 
    type="text/css" 
    href="/mystyle.css">
    
<title>All Seasons</title>

<h1> {{other['heading1']}}</h1>
</head>

<body>
<h2> {{other['title']}}</h2>
<h3> {{get('nr','')}}</h3>

<ul>
%   for d in data:
%        k = '/serie/%s/%s/titles' %(other['serie_id'], d)
        <li><a href={{k}}>season {{d}}</a></li>
    %end
</ul>    
</body>


</html>
