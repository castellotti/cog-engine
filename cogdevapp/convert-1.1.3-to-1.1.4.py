#!/usr/bin/env python
#
# CogEngine Data Upgrader (1.1.3 to 1.1.4)
#
# Copyright Steven M. Castellotti (2001, 2002)
# The author can be reached at: SteveC@innocent.com
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Last Update: 2002.06.16
#
# Calling Convention:
# ./upgrade_cog_data_1.1.3_to_1.1.4.py <CogDevApp 1.1.3 file> <CogDevApp 1.1.4 file>
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



	file_format_version_number = "1.1.4"


	gameInformation.graphic_panel_x_dimension = 640
	gameInformation.graphic_panel_y_dimension = 480
	gameInformation.default_mouse_pointer_graphic = ""

	gameInformation.display_help_button = 1
	gameInformation.graphical_compass_x_icons = 4
	gameInformation.graphical_compass_y_icons = 3
	gameInformation.graphical_compass_panel_padding = 0
	gameInformation.graphical_compass_background_image = ""
	gameInformation.graphical_compass_graphic_not_available_icon = ""
	gameInformation.menu_button_display_position = 0
	if ('graphical_compass_button_image_x_dimension' in dir(gameInformation)):
		del(gameInformation.graphical_compass_button_image_x_dimension)
	if ('graphical_compass_button_image_y_dimension' in dir(gameInformation)):
		del(gameInformation.graphical_compass_button_image_y_dimension)


	gameInformation.graphical_inventory_panel_padding = 1
	if ('graphical_inventory_x_icon_dimension' in dir(gameInformation)):
		del(gameInformation.graphical_inventory_x_icon_dimension)
	if ('graphical_inventory_y_icon_dimension' in dir(gameInformation)):
		del(gameInformation.graphical_inventory_y_icon_dimension)


	if ('object_panel_panel_Xoffset' in dir(gameInformation)):
	        gameInformation.object_panel_Xoffset = gameInformation.object_panel_panel_Xoffset
		del (gameInformation.object_panel_panel_Xoffset)
	if ('object_panel_panel_Yoffset' in dir(gameInformation)):
		gameInformation.object_panel_Yoffset = gameInformation.object_panel_panel_Yoffset
		del (gameInformation.object_panel_panel_Yoffset)
	gameInformation.object_panel_padding = 1
	if ('object_panel_x_icon_dimension' in dir(gameInformation)):
		del(gameInformation.object_panel_x_icon_dimension)
	if ('object_panel_y_icon_dimension' in dir(gameInformation)):
		del(gameInformation.object_panel_y_icon_dimension)


	for each in directionData.keys():
		directionData[each].compass_panel_display_position = 0


	for each in verbData.keys():
		verbData[each].mouse_pointer_graphic = ""



	pickle_python_data_file(output_filename, \
			file_format_version_number, \
			gameInformation, playerInformation, \
			directionData, roomData, \
			itemData, obstructionData, verbData)



# EOF
