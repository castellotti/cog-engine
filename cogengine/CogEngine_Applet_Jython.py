#!/usr/bin/env jython
#
#####################################################################
#
# Cog Engine Applet (Jython)
#
# Copyright Steven M. Castellotti (2002)
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Last Update: 2002.05.16
#
#####################################################################

from java.applet import Applet
from java.awt.event import ActionListener
from java.io import FileInputStream, ObjectInputStream
import java.net.URL


#####################################################################

class CogEngine_Applet_Jython(Applet, ActionListener):

	from CogObjects import *
	from CogEngine_Modules import *
	from CogEngine_Jython_Modules import *

	def init(self):

		self.load_game_database()
		#self.scrub_objects()
		self.initialize_gui()
		self.initialize_engine()


#####################################################################

	def load_game_database(self):

		# This method first downloads the Game Database File, as specified by an HTML parameter.
		# Next, the information contained in the file is deserialized into memory

		try:
			database_url = java.net.URL( "%s%s" % (self.getCodeBase(), self.getParameter("DatabaseFilename")))
			database_url_string = "%s%s" % (self.getCodeBase(), self.getParameter("DatabaseFilename"))
			print "Database URL: (%s)\n" % database_url

			# Now that we have the URL for the Game Database, we will attempt to deserialize (unpickle) it

			p = ObjectInputStream( database_url.openStream() )

			self.gameInformation = p.readObject()
			self.playerInformation = p.readObject()
			self.directionData = p.readObject()
			self.roomData = p.readObject()
			self.itemData = p.readObject()
			self.obstructionData = p.readObject()
			self.verbData = p.readObject()

		except database_access_error:
			print "Error Downloading Game Database"
			print "%s\n" % database_access_error


#####################################################################

		# When a game database file is converted from the CogDevApp format (pickled)
		# to a format readable by Java (java serialized object), certain variables
		# set to "None" no longer carry  the same meaning. The following two methods
		# are incomplete (and unused), but are meant to convert all of the objects
		# which should have the identical meaning to the "None" object.

	def scrub_objects(self):


		data_objects = [self.gameInformation, self.playerInformation, \
		                self.directionData, self.roomData, self.itemData, \
		                self.obstructionData, self.verbData]

		for each in data_objects:

			self.scrub_data_object(each)




	def scrub_data_object(self, data_object):

		for each in dir(data_object):
			if (type(each) == (type([]) or type({}))):
				self.scrub_data_object(self, each)
			else:
				print type(each)


# EOF

