#!/usr/bin/env python
from model import *

Track.dropTable()
Album.dropTable()
Artist.dropTable()

Artist.createTable()
Album.createTable()
Track.createTable()
