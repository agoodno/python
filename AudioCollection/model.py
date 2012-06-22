import os
from types import *
from sqlobject import *
from sqlobject.postgres import builder
import cdrom, DiscID, CDDB

__connection__ = builder()(db='albumdb', user='andrew')


class Artist(SQLObject):
	name = StringCol(varchar=True,length=100,unique=True)
	category = StringCol(varchar=True,length=50)
	albums = MultipleJoin('Album')

class Album(SQLObject):
	disc_id = StringCol(varchar=False,length=8,unique=True)
	name = StringCol(varchar=True,length=200,unique=True)
	year = StringCol(varchar=False,length=4,default=None)
	artist = ForeignKey('Artist')
	tracks = MultipleJoin('Track')

class Track(SQLObject):
	num = StringCol(length=2)
	name = StringCol(varchar=True,length=255)
	album = ForeignKey('Album')

class Disc:

	RIP_QUALITY = 5
	
	def __init__(self):
		self.discid = None
		self.query_info = None
		self.category = None
		self.disc_id = None
		self.title = None
		self.artistName = None
		self.albumName = None
		self.albumlength = None
		self.track_info = None
		self.tracks = {}
		self.read()
		
	def read(self):
		try:
			device = DiscID.open()
			disc_info = DiscID.disc_id(device)
			(query_status, self.query_info) = CDDB.query(disc_info)
		except cdrom.error, e:
			raise cdrom.error, e
		
	def query(self):
		def fixchars(pathname):
			"""Fixes characters that cause escaping problems in string
			   constructions used to execute commands on the OS or in the DB"""
			pathname = pathname.replace(os.sep, "-")
			pathname = pathname.replace("\"", "")
			pathname = pathname.replace("?", "")
			return pathname
		
		def padNum(num):
			if int(num) < 10:
				return "0" + str(num)
			else:
				return str(num)
				
		delims = ("/", " - ")
		def findTitle(title, count):
			"""Tries the delimiters in order until it finds the right one"""
			#print title
			#print len(delims)
			if count < len(delims):
				titleparts = title.split(delims[count])
				#print titleparts
				if len(titleparts) == 2:
					self.artistName = fixchars(titleparts[0].strip())
					self.albumName = fixchars(titleparts[1].strip())
					return True
				else:
					return findTitle(title, count+1)
			return False
		
		self.category = fixchars(self.query_info["category"])
		self.disc_id = self.query_info["disc_id"]
		self.title = fixchars(self.query_info["title"])
		if not findTitle(self.title, 0):
			raise "Title not parsed: %s" % self.title

		(track_status, track_info) = CDDB.read(self.category, self.disc_id)
		
		self.genre = fixchars(track_info['DGENRE'])
		self.year = track_info['DYEAR']
		if track_info.has_key('disc_len'):
			self.albumlength = str(float(track_info['disc_len']) / 60) + " min."
		else:
			self.albumlength = ""
		self.comments = fixchars(track_info['EXTD'])
		self.albumtitle = fixchars(track_info['DTITLE'])
		
		for (tracknum,trackname) in track_info.items():
			if tracknum.find("TTITLE") != -1:
				num = int(tracknum[len("TTITLE"):]) + 1
				self.tracks[padNum(num)] = fixchars(trackname)
		#print [ (k,self.tracks[k]) for k in sorted(self.tracks.keys())]
		
	def view(self):
		if type(self.query_info) is not ListType:
			self.query()
			self.printDisc()
		else:
			self.viewselections()
			
	def viewselections(self):
		self.choices = self.query_info 
		for i in range(len(self.query_info)):
			num = i+1
			print "%d) %s" % (num,self.query_info[i]["category"])
	
	def select(self, choice):
		self.query_info = self.choices[choice - 1]
		self.view()
		
	def printDisc(self):
		print "%s\t(%s)" % (self.title,self.category)		
		for (tracknum,trackname) in sorted(self.tracks.items()):
			print "%s. %s" % (tracknum,trackname)
			
	def save(self):
		self.query()
		#Search for existing artist
		artists = Artist.selectBy(name=self.artistName)
		if artists.count() == 0:
			#Create artist
			artist = Artist(name=self.artistName,category=self.category)
		else:
			#Use existing artist
			artist = artists[0]
			
		#Search for existing album
		albums = Album.selectBy(name=self.albumName)
		if albums.count() == 0:
			#Create album
			album = Album(disc_id=self.disc_id,name=self.albumName,year=self.year,artist=artist)
		
			#Create tracks
			for (tracknum,trackname) in self.tracks.items():
				track = Track(num=tracknum,name=trackname,album=album)
			
			print "***Saved in catalogue***"
		else:
			print "***Already catalogued***"
		
	def ripAll(self):
		self.query()
		print "Ripping %s" % self.albumtitle
		for tracknum in sorted(self.tracks.keys()):
			self.cddaToWav(tracknum)
		self.wavToOgg()
		print "Finished ripping %s" % self.albumtitle
		
	def rip(self, tracknum):
		self.query()
		print "Ripping %s" % self.tracks[tracknum]
		self.cddaToWav(tracknum)
		self.wavToOgg()
		print "Finished ripping %s" % self.tracks[tracknum]
	
	def cddaToWav(self, tracknum):
		os.system("cdparanoia -q %s %s" % (tracknum,"track" + tracknum + ".cdda.wav"))
		
	def wavToOgg(self):
		for filename in os.listdir("."):
			if os.path.isfile(filename) and filename.split(".")[-1] == "wav":
				wavfilename = os.path.join(".", filename)
				tracknum = filename.split(".")[0][-2:]
				trackname = self.tracks[tracknum]
				oggfilename = os.path.join(".", "ripped", self.artistName, self.albumName, (tracknum + "-" + trackname + ".ogg"))
				cmd = "oggenc --quality %d --genre \"%s\" --artist \"%s\" --album \"%s\" --tracknum \"%s\" --title \"%s\" --comment \"%s\" --comment \"%s\" --comment \"%s\" --comment \"%s\" --comment \"%s\" --output \"%s\" \"%s\"" % (Disc.RIP_QUALITY,self.genre,self.artistName,self.albumName,tracknum,trackname,"year="+self.year,"albumlength="+self.albumlength,"comments="+self.comments,"discid="+str(self.disc_id),"category="+self.category,oggfilename,wavfilename)
				os.system(cmd)
				cmd = "rm -rf %s" % wavfilename 
				os.system(cmd)
	
	def copyToPortable(self):
		self.query()
		import shutil
		def copytree(src, dst):
			for name in os.listdir(src):
				srcname = os.path.join(src, name)
				dstname = os.path.join(dst, name)
				try:
					if os.path.isdir(srcname):
						os.mkdir(dstname)
						copytree(srcname, dstname)
					else:
						shutil.copy2(srcname, dstname)
				except (IOError, os.error), why:
					print "Can't copy %s to %s: %s" % (`srcname`, `dstname`, str(why))
		
		"""The whole tree except for the final folder must exist for this to work,
		but it copies ? marks just fine"""
		#os.makedirs("./test/%s/%s" % (self.artistName,self.albumName))
		#copytree(("./ripped/%s/%s" % (self.artistName,self.albumName)), ("./test/%s/%s" % (self.artistName,self.albumName)))
		os.system("cp -ruv ./ripped/* /media/usbdisk/Music/")
		os.system("sudo umount /media/usbdisk")
		
		
