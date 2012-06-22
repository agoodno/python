#!/usr/bin/env python

import cmd
import string, sys
import readline
from model import *

class CollectionCLI(cmd.Cmd):

	def __init__(self):
		cmd.Cmd.__init__(self)
		self.prompt = '> '
		self.disc = None

	def initDisc(self):
		if (self.disc is None):
			try:
				self.disc = Disc()
			except cdrom.error, e:
				print "No disc in drive"
				return False
		return True
		
	def help_dblist(self):
		print "syntax: dblist [artist | album | track]",
		print "-- lists the matching objects in the database"

	def help_dbquery(self):
		print "syntax: dbquery [artist | album | track] [searchstr]",
		print "-- lists the matching objects in the database"

	def help_dbget(self):
		print "syntax: dbget [artist | album | track] [id]",
		print "-- gets the matching object in the database"

	def help_cdview(self):
		print "syntax: cdview",
		print "-- shows the web entries for the disc in the tray"

	def help_cdselect(self):
		print "syntax: cdselect [num]",
		print "-- selects a specific set of web entries for later saving"
	
	def help_cdsave(self):
		print "syntax: cdsave",
		print "-- save the web entries for the disc to the db"

	def help_cdrip(self):
		print "syntax: cdrip [tracknum]",
		print "-- rip one track on the disc to the filesystem"

	def help_cdripall(self):
		print "syntax: cdripall",
		print "-- rip all the tracks on the disc to the filesystem"
		
	def help_copytogo(self):
		print "syntax: copytogo",
		print "-- copy all the ripped audio from the filesystem to an attached player"
		
	def help_quit(self):
		print "syntax: quit",
		print "-- terminates the application"

	def help_q(self):
		print "syntax: quit",
		print "-- terminates the application"

	def help_help(self):
		pass

	def do_dblist(self, arg):
		try:
			sqlcls = getEntity(arg)
			for sqlobj in sqlcls.select():
				print sqlobj
		except ValueError:
			print "Wrong number of parameters"
			self.help_dblist()

	def do_dbquery(self, arg):
		try:
			(entity, searchstr) = arg.split()
			sqlcls = getEntity(entity)
			for sqlobj in sqlcls.select(sqlcls.q.name.contains(searchstr)):
				print sqlobj
		except ValueError:
			print "Wrong number of parameters"
			self.help_dbquery()
			
	def do_dbget(self, arg):
		try:
			(entity, entity_id) = arg.split()
			sqlcls = getEntity(entity)
			try:
				print sqlcls.get(entity_id)
			except SQLObjectNotFound, e:
				print e
		except ValueError:
			print "Wrong number of parameters"
			self.help_dbget()

	def do_cdview(self, arg):
		if not self.initDisc(): return
		self.disc.view()
		
	def do_cdselect(self, arg):
		if not self.initDisc(): return
		try:
			self.disc.select(int(arg))
		except Error:
			print "Bad parameters"
			self.help_cdselect()

	def do_cdsave(self, arg):
		if not self.initDisc(): return
		self.disc.save()

	def do_cdrip(self, arg):
		if not self.initDisc(): return
		try:
			self.disc.rip(arg)
		except ValueError:
			print "Wrong number of parameters"
			self.help_cdrip()

	def do_cdripall(self, arg):
		if not self.initDisc(): return
		try:
			self.disc.ripAll()
		except ValueError:
			print "Wrong number of parameters"
			self.help_cdripall()	

	def do_copytogo(self, arg):
		if not self.initDisc(): return
		self.disc.copyToPortable()
		
	def do_quit(self, arg):
		sys.exit(1)

	# shortcuts
	do_q = do_quit
	 
def getEntity(name):
	if name == "artist":
		return Artist
	elif name == "album":
		return Album
	elif name == "track":
		return Track
	else:
		raise ValueError()

if __name__ == "__main__":
	cli = CollectionCLI()
	cli.cmdloop("Audio Collection")
