#!/usr/bin/env python
#
# CogEngine Data Upgrader (1.0.x to 1.1.3)
#
# Copyright Steven M. Castellotti (2001, 2002)
# The author can be reached at: SteveC@innocent.com
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Last Update: 2002.06.07
#
# Calling Convention:
# ./upgrade_cog_data_1.0_to_1.1.3.py <CogDevApp 1.0 file> <CogDevApp 1.1.3 file>
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

	(gameInformation, playerInformation, \
	directionData, roomData, \
	itemData, obstructionData, \
	verbData) = load_python_data(input_filename)

	file_format_version_number = '1.1.3'

	gameInformation.command_history = []
	gameInformation.text_to_speech_enabled = 1
	gameInformation.menu_button_graphic_url = ""
	gameInformation.show_graphical_inventory_panel = 1
	gameInformation.graphical_inventory_panel_Xoffset = 415
	gameInformation.graphical_inventory_panel_Yoffset = 488
	gameInformation.graphical_inventory_x_icon_dimension = 50
	gameInformation.graphical_inventory_y_icon_dimension = 50
	gameInformation.graphical_inventory_x_icons = 4
	gameInformation.graphical_inventory_y_icons = 2
	gameInformation.graphical_inventory_blank_icon = ""
	gameInformation.graphical_inventory_graphic_not_available_icon = ""
	gameInformation.show_graphical_inventory_panel_scrollbars = 1
	gameInformation.inventory_panel_scroll_up_available_icon = ""
	gameInformation.inventory_panel_scroll_up_unavailable_icon = ""
	gameInformation.inventory_panel_scroll_down_available_icon = ""
	gameInformation.inventory_panel_scroll_down_unavailable_icon = ""
	gameInformation.show_graphical_object_panel = 1
	gameInformation.object_panel_panel_Xoffset = 5
	gameInformation.object_panel_panel_Yoffset = 538
	gameInformation.object_panel_x_icon_dimension = 50
	gameInformation.object_panel_y_icon_dimension = 50
	gameInformation.object_panel_x_icons = 4
	gameInformation.object_panel_y_icons = 1
	gameInformation.object_panel_blank_icon = ""
	gameInformation.object_panel_graphic_not_available_icon = ""
	gameInformation.show_graphical_object_panel_scrollbars = 1
	gameInformation.object_panel_scroll_up_available_icon = ""
	gameInformation.object_panel_scroll_up_unavailable_icon = ""
	gameInformation.object_panel_scroll_down_available_icon = ""
	gameInformation.object_panel_scroll_down_unavailable_icon = ""
	gameInformation.graphical_display_window_x_dimension = 640
	gameInformation.graphical_display_window_y_dimension = 595
	gameInformation.graphical_display_x_coordinate = 0
	gameInformation.graphical_display_y_coordinate = 0
	gameInformation.graphical_compass_display_x_coordinate = 246
	gameInformation.graphical_compass_display_y_coordinate = 482
	gameInformation.graphical_compass_button_image_x_dimension = 37
	gameInformation.graphical_compass_button_image_y_dimension = 37


	for direction in directionData.keys():
		directionData[direction].compass_graphic_never_traveled = ""
		directionData[direction].compass_graphic_last_direction_traveled = ""


	for obstruction in obstructionData.keys():
		obstructionData[obstruction].icon_graphic_url = ""


	pickle_python_data_file(output_filename, \
	                     file_format_version_number, \
								gameInformation, playerInformation, \
								directionData, roomData, \
								itemData, obstructionData, verbData)



# EOF
