#!/usr/bin/env jython
#
#####################################################################
#
# Cog Engine Application (Jython)
#
# Copyright Steven M. Castellotti (2002)
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Last Update: 2002.05.12
#
#####################################################################


#####################################################################

class CogEngine_Jython_Applet(Applet, ActionListener):

	from java.applet import Applet
	from java import awt
	from java.awt.event import ActionListener
	import java.net.URL

	#import CogEngine_Utilities

	from CogObjects import *
	from CogEngine_Modules import *
	from CogEngine_Jython_Modules import *


	def init(self):

		self.load_game_database()
		self.initialize_gui()


#####################################################################

	def load_game_database(self):

		# This method first downloads the Game Database File, as specified by an HTML parameter.
		# Next, the information contained in the file is deserialized into memory

#			test_url = java.net.URL("%sCycon-COG.dev" % self.getCodeBase())
#			print "Test URL: %s" % test_url
#			content = test_url.getContent()
#			print type(content)


		#try:
			database_url = java.net.URL( "%s%s" % (self.getCodeBase(), self.getParameter("DatabaseFilename")))
			database_url_string = "%s%s" % (self.getCodeBase(), self.getParameter("DatabaseFilename"))
			print "Database URL: (%s)\n" % database_url


		#except database_access_error:
		#	print "Error Downloading Game Database"
		#	print "%s\n" % database_access_error

		# Now that we have the URL for the Game Database, we will attempt to deserialize (unpickle) it

		#try:
			import cPickle # 308k
			pickle = cPickle
			#import pickle # 408k
			#from urllib import urlopen
			database_content = database_url.getContent()
			print type(database_content)
			print database_content
			#database_file = open(database_url.getContent(), 'r')

			#import urllib
			#database_file_content = urllib.urlopen(database_url_string)


#			self.gameInformation = pickle.load(database_file)


			self.gameInformation = pickle.load(database_content)
			#self.gameInformation = pickle.load(database_file_content)


#			self.playerInformation = pickle.load(database_file)
#			self.directionData = pickle.load(database_file)
#			self.roomData = pickle.load(database_file)
#			self.itemData = pickle.load(database_file)
#			self.obstructionData = pickle.load(database_file)
#			self.verbData = pickle.load(database_file)

			print self.gameInformation.game_title

		#except pickle_error:
		#	print "Error Deserializing Game Database"
		#	print "%s\n" % pickle_error


