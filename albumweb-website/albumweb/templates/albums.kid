<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Entity</title>
    <link name="Main CSS" type="text/css" href="form.css"/>
    <style type="text/css">
        li {
            list-style-type: none;
            height: 25px;
        }
    </style>
</head>

<body>
    <p>My albums&nbsp;&nbsp;<a href="album?mode=add">Add</a></p>
    <ul>
      <li py:for="album in albums"> 
        ${album.name}&nbsp;&nbsp;<a href="album?mode=edit&amp;id=${album.id}">Edit</a>&nbsp;&nbsp;<a href="album?mode=remove&amp;id=${album.id}">Remove</a>
      </li> 
    </ul>
</body>
</html>