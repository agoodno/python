#!/usr/bin/env python

import sys
from types import *
from artist import Artist
from album import Album
from track import Track
import DiscID, CDDB

cmds = ["view", "save", "quit"]

class cmdError (Exception):
    pass

def printDisc(disc_info):
	category = disc_info["category"]
	disc_id = disc_info["disc_id"]
	title = disc_info["title"]
	
	(track_status, track_info) = CDDB.read(category, disc_id)
	
	print "%s\t(%s)" % (title,category)
	tracks = {}
	for (k,v) in track_info.items():
		if k.find("TTITLE") != -1:
			num = int(k[len("TTITLE"):]) + 1
			tracks[num] = v
	
	tracks.items().sort()
	for (k,v) in tracks.items():
	     print "%s. %s" % (k,v)

	     
def listDisc(artistName):
	artists = Artist.selectBy(name=artistName)
	print "NumArtists=%d" % artists.count()
	for artist in artists:
		print "Artist: %s" % artist.name
		for album in artist.albums:
			print "Album: %s" % album.name
	
		
def saveDisc(disc_info):
	category = disc_info["category"]
	disc_id = disc_info["disc_id"]
	title = disc_info["title"]
	(artistName, albumName) = disc_info["title"].split("/")
	artistName = artistName.strip()
	albumName = albumName.strip()
	
	#Search for existing artist
	artists = Artist.selectBy(name=artistName)
	if artists.count() == 0:
		#Create artist
		artist = Artist(name=artistName,category=category)
	else:
		#Use existing artist
		artist = artists[0]
		
	#Search for existing album
	albums = Album.selectBy(name=albumName)
	if albums.count() == 0:
		#Create album
		album = Album(disc_id=disc_id,name=albumName,artist=artist)
	
		#Create tracks
		(track_status, track_info) = CDDB.read(category, disc_id)
		tracks = {}
		for (k,v) in track_info.items():
			if k.find("TTITLE") != -1:
				num = int(k[len("TTITLE"):]) + 1
				tracks[num] = v
		
		tracks.items().sort()
		for (k,v) in tracks.items():
		     track = Track(num=k,name=v,album=album)
		     
		print "***Saved in catalogue***"
	else:
		print "***Already catalogued***"
	
	printDisc(disc_info)


if __name__ == "__main__":
	device = DiscID.open()
	discid = DiscID.disc_id(device)
	(query_status, query_info) = CDDB.query(discid)
	
	if type(query_info) is not ListType:
		saveDisc(query_info)
	else:
		cmd = ""
		choice = 0
		print "There is more than one entry."
		while cmd != "save" and cmd != "quit":
			print "Choose one:"
			choices = []
			count = 1
			for info in query_info:
				choices.append(count)
				print "%d) %s" % (count,info["category"])
				count = count + 1
			try:
				userinput = raw_input("Command> ").strip()
				if userinput == "quit":
					break
				(cmd,num) = userinput.split(" ")
				choice = int(num)
				
				if cmd not in cmds:
					raise cmdError("Invalid command")
				
				if choice not in choices:
					raise cmdError("Invalid choice")
				
				if cmd == "view":
					printDisc(query_info[choice - 1])
				elif cmd == "save":
					saveDisc(query_info[choice - 1])
			except cmdError, e:
				print "%s: cmd=%s;choice=%s" % (e,cmd,choice)
			except Exception, e:
				print "%s" % e
