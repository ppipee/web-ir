<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<!DOCTYPE html>
<html>
<head>
    <title>JSP - Hello World</title>
</head>
<body>
<%@include file="header.jsp"%>
<h1><%= "Hello World!" %>
</h1>
<center>
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
