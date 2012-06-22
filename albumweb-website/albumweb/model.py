from sqlobject import *
from ansistyle import MixedCaseUnderscoreANSIStyle
from turbogears.database import PackageHub

hub = PackageHub("albumweb")
__connection__ = hub

class Artist(SQLObject):
    class sqlmeta:
        style = MixedCaseUnderscoreANSIStyle(longID=True)
    name = StringCol(varchar=True,length=100,unique=True)
    category = StringCol(varchar=True,length=50)
    albums = MultipleJoin('Album')

class Album(SQLObject):
    class sqlmeta:
        style = MixedCaseUnderscoreANSIStyle(longID=True)
    discId = StringCol(varchar=False,length=8,unique=True)
    name = StringCol(varchar=True,length=200,unique=True)
    year = StringCol(varchar=False,length=4,default=None)
    tracks = MultipleJoin('Track')
    artist = ForeignKey('Artist')

class Track(SQLObject):
    class sqlmeta:
        style = MixedCaseUnderscoreANSIStyle(longID=True)
    num = IntCol()
    name = StringCol(varchar=True,length=255)
    album = ForeignKey('Album')

#Artist.sqlmeta.addJoin(MultipleJoin('Album',joinMethodName='albums'))
#Album.sqlmeta.addJoin(ForeignKey('Artist',joinMethodName='albums'))


