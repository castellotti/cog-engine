#!/usr/bin/env jython
#
# CogEngine Data Exporter
#
# Copyright Steven M. Castellotti (2001, 2002)
# The author can be reached at: SteveC@innocent.com
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Version x.x
# Last Update: 2002.05.14
#
# Calling Convention:
# ./export_cog_data.py <CogDevApp file> <CogEngine file>
#
#
#####################################################################

import sys
import cPickle
from CogObjects import *


#####################################################################
# Functions
#####################################################################

def load_python_data(filename):
	try:
		import cPickle
		pickle = cPickle
	except:
		import pickle


	print "Importing Python Data File...",
	file = open(filename, 'r')
	file_format_version_number = pickle.load(file)
	gameInformation = pickle.load(file)
	playerInformation = pickle.load(file)
	directionData = pickle.load(file)
	roomData = pickle.load(file)
	itemData = pickle.load(file)
	obstructionData = pickle.load(file)
	verbData = pickle.load(file)
	file.close()
	print "done"

	return(file_format_version_number, \
	       gameInformation, playerInformation, \
	       directionData, roomData, \
	       itemData, obstructionData, \
	       verbData)


#####################################################################

def serialize_data_file(filename, file_format_version_number, \
	                     gameInformation, playerInformation, \
	                     directionData, roomData, \
	                     itemData, obstructionData, \
	                     verbData):

	# This function takes in the name of the COG Engine Data File to be generated
	# as a parameter, and serialized the java objects which have been converted
	# over from their corresponding python data structures.

	print "Serializing Data File...",

	from java.io import FileOutputStream, ObjectOutputStream
	stream = FileOutputStream(filename)
	p = ObjectOutputStream(stream)

	p.writeObject(file_format_version_number)
	p.writeObject(gameInformation)
	p.writeObject(playerInformation)
	p.writeObject(directionData)
	p.writeObject(roomData)
	p.writeObject(itemData)
	p.writeObject(obstructionData)
	p.writeObject(verbData)
	stream.close()

	print "done"


#####################################################################
# Main
#####################################################################

if __name__ == '__main__':

	# Parse the filename from the Command Line
	input_filename = sys.argv[-2]
	output_filename = sys.argv[-1]


	# Unpickle the Python Game Database File
	(file_format_version_number, gameInformation, playerInformation, \
	directionData, roomData, \
	itemData, obstructionData, \
	verbData) = load_python_data(input_filename)


	# Serialize the Game Data
	serialize_data_file(output_filename, file_format_version_number, \
	                    gameInformation, playerInformation, \
	                    directionData, roomData, \
	                    itemData, obstructionData, \
	                    verbData)

# EOF
