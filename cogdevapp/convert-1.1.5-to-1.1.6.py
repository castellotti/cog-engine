#!/usr/bin/env python
#
# CogEngine Data Upgrader (1.1.5 to 1.1.6)
#
# Copyright Steven M. Castellotti (2001, 2002)
# The author can be reached at: SteveC@innocent.com
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Last Update: 2002.07.13
#
# Calling Convention:
# ./upgrade_cog_data_1.1.5_to_1.1.6.py <CogDevApp 1.1.5 file> <CogDevApp 1.1.6 file>
#
#
#####################################################################

import sys, pickle
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

def pickle_python_data_file(filename, \
                            file_format_version_number, \
                            gameInformation, playerInformation, \
                            directionData, roomData, \
									 itemData, obstructionData, verbData):

	print "Writing Data File...",
	file = open(filename, 'w')
	pickle.dump(file_format_version_number, file)
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

	(file_format_version_number, \
	gameInformation, playerInformation, \
	directionData, roomData, \
	itemData, obstructionData, \
	verbData) = load_python_data(input_filename)



	file_format_version_number = "1.1.6"



	playerInformation.last_room = -1


	for direction in directionData.keys():
		directionData[direction].compass_graphic_previously_traveled = \
		     directionData[direction].compass_graphic_never_traveled



	pickle_python_data_file(output_filename, \
			file_format_version_number, \
			gameInformation, playerInformation, \
			directionData, roomData, \
			itemData, obstructionData, verbData)



# EOF
