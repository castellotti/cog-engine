#!/usr/bin/env python
#
# CogEngine Data Upgrader
#
# Copyright Steven M. Castellotti (2001)
# The author can be reached at: SteveC@innocent.com
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Version x.x
# Last Update: 2001.09.22
#
# Calling Convention:
# ./export_cog_data.py <CogDevApp 0.82 file> <CogDevApp 0.90 file>
#
#
#####################################################################

import sys
from CogObjects import *


#####################################################################
# Global Variables
#####################################################################

input_filename = sys.argv[-2]
output_filename = sys.argv[-1]


#####################################################################
# Functions
#####################################################################

def load_python_data(filename):
	try:
		import cPickle
		pickle = cPickle
	except:
		try:
			import pickle
		except:
			add_cPython_modules()
			try:
				import cPickle
				pickle = cPickle
			except:
				import pickle

	print "Importing Python Data File...",
	file = open(filename, 'r')
	gameInformation = pickle.load(file)
	playerInformation = pickle.load(file)
	directionData = pickle.load(file)
	roomData = pickle.load(file)
	itemData = pickle.load(file)
	obstructionData = pickle.load(file)
	verbData = pickle.load(file)
	file.close()
	print "done"

	return(gameInformation, playerInformation, \
	       directionData, roomData, \
	       itemData, obstructionData, \
	       verbData)


#####################################################################

def pickle_python_data_file(filename, \
	gameInformation, playerInformation, \
	directionData, roomData, \
	itemData, obstructionData, verbData):
	try:
		import cPickle
		pickle = cPickle
	except:
		try:
			import pickle
		except:
			add_cPython_modules()
			try:
				import cPickle
				pickle = cPickle
			except:
				import pickle

	print "Writing Data File...",
	file = open(filename, 'w')
	pickle.dump(gameInformation, file)
	pickle.dump(playerInformation, file)
	pickle.dump(directionData, file)
	pickle.dump(roomData, file)
	pickle.dump(itemData, file)
	pickle.dump(obstructionData, file)
	pickle.dump(verbData, file)
	file.close()
	print "done"


#####################################################################
# Main
#####################################################################

if __name__ == '__main__':

	(gameInformation, playerInformation, \
	directionData, roomData, \
	itemData, obstructionData, \
	verbData) = load_python_data(input_filename)

	gameInformation.image_directory = ""

	pickle_python_data_file(output_filename, \
	gameInformation, playerInformation, \
	directionData, roomData, \
	itemData, obstructionData, verbData)

# EOF