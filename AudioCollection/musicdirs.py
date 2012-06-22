import os, os.path

def list_music(musicroot):
	artists = os.listdir(musicroot)
	for artist in artists:
		artistdir = os.path.abspath(os.path.join(musicroot, artist))
		if os.path.isdir(artistdir):
			#print artist
			albums = os.listdir(artistdir)
			for album in albums:
				albumdir = os.path.abspath(os.path.join(artistdir, album))
				if (os.path.isdir(albumdir)):
					#print "\t" + album
					tracks = os.listdir(albumdir)
					for track in tracks:
						trackfile = os.path.abspath(os.path.join(albumdir, track))
						if (os.path.isfile(trackfile)):
							#print "\t\t" + track
							#print trackfile.split(".")[1]
							if (trackfile.split("."))[1] == "mp3":
								from ID3 import ID3
								id3info = ID3(trackfile)
								print (id3info.artist,id3info.album,id3info.year,id3info.track,id3info.title,id3info.comment)
				
if __name__ == "__main__":
	list_music("/home/andrew/media/music")
		
