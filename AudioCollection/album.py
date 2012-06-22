#!/usr/bin/env python

from sqlobject import *
from sqlobject.postgres import builder

connection = builder()(db='albumdb', user='andrew')

class Album(SQLObject):
	_connection = connection
	disc_id = StringCol(varchar=False,length=8,unique=True)
	name = StringCol(varchar=True,length=200,unique=True)
	year = StringCol(varchar=False,length=4,default=None)
	artist = ForeignKey('Artist')
	tracks = MultipleJoin('Track')

	
if __name__ == "__main__":
	pass

