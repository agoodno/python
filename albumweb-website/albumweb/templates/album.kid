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
    <form name="frmAlbum" action="postalbum" method="post">
        <div style="float: left; width: 70px; margin-top: 2px;">
            <ul>
                <li>Name:</li>
                <li>Disc:</li>
                <li>Year:</li>
                <li>Artist:</li>
            </ul>
        </div>
        <div style="float: left; width: 100px;">
            <ul>
                <li><input name="name" value="${name}"/></li>
                <li><input name="discId" value="${discId}"/></li>
                <li><input name="year" value="${year}"/></li>
                <li>
                    <!--<select name="artistId">
                        <option py:for="artist in artists" value="${artist.id}" py:if="${artist.id} == ${artistId}" selected="true">${artist.name}</option>
                    </select>-->
                    <select name="artistId">
                        <option py:for="value, content in sorted(artistMap.iteritems())"
                            py:content="content"
                            py:attrs="dict(value=value, selected=(value==selected and 'selected' or None))" />
                    </select>
                </li>
            </ul>
            <input name="btnSubmit" type="submit" value="Save"/>
            <input name="id" type="hidden" value="${id}"/>
            <input name="mode" type="hidden" value="${mode}"/>
        </div>
        <div style="clear: both;"/>
    </form>
</body>
</html>