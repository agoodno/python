import turbogears
from turbogears import controllers
from model import *

class Root(controllers.Root):
    
    @turbogears.expose(html="albumweb.templates.welcome")
    def index(self):
        import time
        return dict(now=time.ctime())

    @turbogears.expose(html="albumweb.templates.albums")
    def albums(self):
        albums = list(Album.select())
        return dict(albums=albums)

    @turbogears.expose(html="albumweb.templates.album")
    def album(self, id=None, mode="add"):
        album = None
        artists = Artist.select()
        artistMap = {}
        for artist in artists:
            artistMap[artist.id] = artist.name
            
        if id != None:
            album = Album.get(id=id)
            return dict(id=id,name=album.name,discId=album.discId,year=album.year,artistId=album.artist.id,artistName=album.artist.name,artistMap=artistMap,mode=mode,selected=album.artist.id)
        return dict(id=None,name=None,discId=None,year=None,artistId=None,artistName=None,artistMap=artistMap,mode=mode,selected=None)

    @turbogears.expose(html="albumweb.templates.postalbum")
    def postalbum(self, name, year, discId, artistId, btnSubmit=None, id=None, mode=None):
        if (mode == "add"):
            Album(name=name, year=year,discId=discId,artist=Artist.get(artistId))
        elif (mode == "edit"):
            album = Album.get(id=id)
            album.name = name
            album.discId = discId
            album.year = year
            album.artist=Artist.get(artistId)
        elif (mode == "remove"):
            Album.delete(id=id)
        return self.albums()
