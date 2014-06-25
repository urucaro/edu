<html>
<head>

<link rel="stylesheet" 
    type="text/css" 
    href="/mystyle.css">

<title>All Series</title>

<h1> {{other['heading1']}}</h1>

<script type="text/javascript">


function GoUrlTitles(l)
{
var x = l;
   window.location.href = x;
}

</script>

</head>
<body>

<table border="1" style="width:300px">
%   for d in data:
%       k ='/serie/%s/seasons' %d[0]
        <tr>
        <td><a href="javascript:GoUrlTitles('{{k}}')">{{d[0]}}</a></td>
        <td><a href="javascript:GoUrlTitles('{{k}}')">{{d[1]}}</a></td>
        </tr>
    %end
</table> 


</body>
</html>



