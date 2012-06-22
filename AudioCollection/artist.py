#!/usr/bin/env python

from sqlobject import *
from sqlobject.postgres import builder

connection = builder()(db='albumdb', user='andrew')

class Artist(SQLObject):
	_connection = connection
	name = StringCol(varchar=True,length=100,unique=True)
	category = StringCol(varchar=True,length=50)
	albums = MultipleJoin('Album')

@classmethod
def get(artistName):
	return Artist.select(Artist.q.name.contains(artistName))
	
if __name__ == "__main__":
	pass

