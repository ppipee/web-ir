<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<!DOCTYPE html>
<html>
<head>
    <title>JSP - Hello World</title>
    <link href="./styles.css" rel="stylesheet" type="text/css">
</head>
<body>
<%@include file="header.jsp"%>
<center>
    <h3><%= "WEB-IR" %></h3>
</center>
<center class="container">
    <form name="search" action="results.jsp" method="get">
        <p>
            <input name="query" size="44"/>&nbsp;Search Criteria
        </p>
        <p>
            <input name="maxresults" size="4" value="10"/>&nbsp;Results Per Page&nbsp;
            <input type="submit" value="Search"/>
        </p>
    </form>
</center>
<%@include file="footer.jsp"%>
</body>
</html>
