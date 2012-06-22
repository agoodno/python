#!/usr/bin/env python

from sqlobject import *
from sqlobject.postgres import builder

connection = builder()(db='albumdb', user='andrew')

class Track(SQLObject):
	_connection = connection
	num = IntCol()
	name = StringCol(varchar=True,length=100)
	album = ForeignKey('Album')

	
if __name__ == "__main__":
	pass

