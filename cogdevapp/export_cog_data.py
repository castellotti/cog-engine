#!/usr/bin/env jython
#
# CogEngine Data Exporter
#
# Copyright Steven M. Castellotti (2001)
# The author can be reached at: SteveC@innocent.com
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Version x.x
# Last Update: 2001.06.12
#
# Calling Convention:
# ./export_cog_data.py <CogDevApp file> <CogEngine file>
#
#
#####################################################################

import sys
from CogObjects import *

#####################################################################
# Global Variables
#####################################################################

# input_filename = "Cycon-COG.dev"
# output_filename = "Cycon-COG.dat.new"
input_filename = sys.argv[-2]
output_filename = sys.argv[-1]
cPython_library_path = '/usr/lib/python1.5/'

#####################################################################
# Functions
#####################################################################

def add_cPython_modules():
	import sys
	import __main__
	sys.path.append(__main__.cPython_library_path)


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

def convert_game_information(python):

	# Player's current room is currently not handled


	print "Converting Game Information...",

	import GameInfoOBJ
	java = GameInfoOBJ()

	java.Game_Title = python.game_title
	java.Version_Number = python.version_number
	java.Game_Designer =  python.game_designer
	java.Game_Designer_Email_Address = python.game_designer_email_address
	java.LastUpdate = python.last_update
	java.DebugMode = python.debug_mode
	java.GameURL = python.game_url
	java.DatabaseURL = python.database_url
	java.ShowAllVerbs = python.show_all_verbs
	java.Introduction_Text = python.introduction_text
	java.ImageLoading_GraphicURL = python.image_loading_graphic_url
	java.Introduction_GraphicURL =  python.introduction_graphic_url
	java.Image_Directory = python.image_directory
	java.PreferredGraphicSizeX = python.preferred_graphic_size_X
	java.PreferredGraphicSizeY = python.preferred_graphic_size_Y
	java.ShowStats = python.show_stats
	java.ShowInventory = python.show_inventory
	java.ShowCommandLine = python.show_command_line
	java.ShowCompass = python.show_compass
	java.CenterButtonIndicatesItems = python.center_button_indicates_items
	java.LoadAllCompassImages = python.load_all_compass_images
	java.MenuButton_GraphicURL = python.menu_button_graphic_url
	java.GameInfoHeaderNotes = python.game_information_notes
	print "done"
	return(java)


####################################################################

def convert_player_information(python, jRoomArray, total_items):

	print "Converting Player Information...",

	import PlayerOBJ
	java = PlayerOBJ()

 	java.Name = python.name
	java.Email_Address = python.email_address
	java.Points = python.points
	java.Exp = python.experience
	java.experienceLevel = python.experience_level
	java.HP = python.hp
	java.MP = python.mp
	java.Str = python.strength
	java.IQ = python.intelligence
	java.Dex = python.dexterity
	java.Agil = python.agility
	java.Charisma = python.charisma
	java.Armor_Level = python.armor_level
	java.Max_Weight = python.max_weight
	java.Max_Bulk = python.max_bulk
	java.Current_Weight = python.current_weight
	java.Current_Bulk = python.current_bulk

 	# handle items list
	from jarray import zeros
	java.Items = zeros( total_items, 'z' ) # create a boolean array of necessary length

	for each in python.items:
		java.Items[ each ] = 1

	# handle current room
	java.CurrentRoom = jRoomArray[ python.current_room ]

 	print "done"

 	return(java)


#####################################################################

def convert_direction_data(directionData):

	print "Converting Direction Data...",

	import DirectionInfoOBJ
	from jarray import zeros
	java = zeros( len(directionData) + 1, DirectionInfoOBJ )

	for each in directionData.keys():
		java[each] = DirectionInfoOBJ()
		java[each].Number = directionData[each].number
		java[each].Name = directionData[each].name
		java[each].Abbreviation = directionData[each].abbreviation
		java[each].CG_AvailableURL = directionData[each].compass_graphic_available_url
		java[each].CG_UnavailableURL = directionData[each].compass_graphic_unavailable_url
		java[each].CG_SpecialURL = directionData[each].compass_graphic_special_url

	print "done"

	return(java)


#####################################################################

def convert_room_data(roomData):

	print "Converting Room Data...",

	import RoomOBJ, DirectionOBJ
	from jarray import zeros
	java = zeros( len(roomData) + 1, RoomOBJ )

	for each in roomData.keys():
		java[each] = RoomOBJ()
		java[each].Number = roomData[each].number
		java[each].Name = roomData[each].name
		java[each].Visited = roomData[each].visited
		java[each].GraphicURL = roomData[each].graphic_url
		java[each].Description_Long = roomData[each].description_long
		java[each].Description_Short = roomData[each].description_short
		java[each].Direction_Description = roomData[each].direction_description
		java[each].Items = roomData[each].items
		java[each].Notes = roomData[each].notes

		# Handle direction objects
		import __main__
		java[each].DirectionArray = zeros( len(__main__.jDirectionInfoArray), DirectionOBJ )

		for direction in roomData[each].direction.keys():
			java[each].DirectionArray[direction] = DirectionOBJ()
			java[each].DirectionArray[direction].ToWhichRoom = roomData[each].direction[direction].to_which_room
			java[each].DirectionArray[direction].Obstructions = roomData[each].direction[direction].obstructions
			java[each].DirectionArray[direction].HasMovedThisWay = roomData[each].direction[direction].has_moved_this_way
			java[each].DirectionArray[direction].FirstTransitionText = roomData[each].direction[direction].first_transition_text
			java[each].DirectionArray[direction].TransitionText = roomData[each].direction[direction].transition_text
			java[each].DirectionArray[direction].FirstTransitionGraphic = roomData[each].direction[direction].first_transition_graphic
			java[each].DirectionArray[direction].TransitionGraphic = roomData[each].direction[direction].transition_graphic

	print "done"

	return(java)


#####################################################################

def convert_item_data(itemData):

	print "Converting Item Data...",

	import ItemOBJ
	from jarray import zeros
	java = zeros( len(itemData) + 1, ItemOBJ )

	for each in itemData.keys():
		java[each] = ItemOBJ()
		java[each].Number = itemData[each].number
		java[each].Name = itemData[each].name
		java[each].Aliases = itemData[each].aliases
		java[each].Environment_GraphicURL = itemData[each].environment_graphic_url
		java[each].Environment_Graphic_Xpos = itemData[each].environment_graphic_Xpos
		java[each].Environment_Graphic_Ypos = itemData[each].environment_graphic_Ypos
		java[each].CloseUp_GraphicURL = itemData[each].closeup_graphic_url
		java[each].Icon_GraphicURL = itemData[each].icon_graphic_url
		java[each].Equipped_GraphicURL = itemData[each].equipped_graphic_url
		java[each].Description = itemData[each].description
		java[each].Location = itemData[each].location
		java[each].Equipped = itemData[each].equipped
		java[each].Weight = itemData[each].weight
		java[each].Bulk = itemData[each].bulk
		java[each].Notes = itemData[each].notes

	print "done"

	return(java)


#####################################################################

def convert_obstruction_data(obstructionData):

	print "Converting Obstruction Data...",

	import ObstructionOBJ
	from jarray import zeros
	java = zeros( len(obstructionData) + 1, ObstructionOBJ )

	for each in obstructionData.keys():
		java[each] = ObstructionOBJ()
		java[each].Number = obstructionData[each].number
		java[each].Name = obstructionData[each].name
		java[each].Aliases = obstructionData[each].aliases
		java[each].Environment_GraphicURL = obstructionData[each].environment_graphic_url
		java[each].Environment_Graphic_Xpos = obstructionData[each].environment_graphic_Xpos
		java[each].Environment_Graphic_Ypos = obstructionData[each].environment_graphic_Ypos
		java[each].CloseUp_GraphicURL = obstructionData[each].closeup_graphic_url
		java[each].Description = obstructionData[each].description
		java[each].Type = obstructionData[each].type
		java[each].Locations = obstructionData[each].locations
		java[each].Visible = obstructionData[each].visible
		java[each].Notes = obstructionData[each].notes

	print "done"

	return(java)


#####################################################################

def convert_verb_data(verbData):

	print "Converting Verb/Event Data...",

	import VerbOBJ, EventOBJ
	from jarray import zeros
	java = zeros( len(verbData) + 1, VerbOBJ )

	for each in verbData.keys():
		java[each] = VerbOBJ()
		java[each].Number = verbData[each].number
		java[each].Name = verbData[each].name
		java[each].Aliases = verbData[each].aliases

		# Handle Events for this Verb
		java[each].Events = zeros( len(verbData[each].events) + 1, EventOBJ)

		counter = 1
		while ( counter <= len(verbData[each].events) ):
			java[each].Events[counter] = EventOBJ()
			java[each].Events[counter].Action = verbData[each].events[counter].action
			java[each].Events[counter].Object = verbData[each].events[counter].object
			java[each].Events[counter].Preposition = verbData[each].events[counter].preposition
			java[each].Events[counter].Object2 = verbData[each].events[counter].object2
			java[each].Events[counter].Requirements = verbData[each].events[counter].requirements
			java[each].Events[counter].EffectString = verbData[each].events[counter].effects
			java[each].Events[counter].HasBeenExecuted = verbData[each].events[counter].has_been_executed
			counter = counter + 1

		java[each].TotalEvents = len(verbData[each].events)

	print "done"

	return(java)


#####################################################################

def serialize_data_file(filename, \
	                     jGameInformation, jPlayerInformation, \
	                     jDirectionInfoArray, jRoomArray, \
	                     jItemArray, jObstructionArray, \
	                     jVerbArray):

	# This function takes in the name of the COG Engine Data File to be generated
	# as a parameter, and serialized the java objects which have been converted
	# over from their corresponding python data structures.

	print "Serializing Data File...",

	from java.io import FileOutputStream, ObjectOutputStream
	stream = FileOutputStream(filename)
	p = ObjectOutputStream(stream)

	p.writeObject(jGameInformation);
	p.writeObject(jDirectionInfoArray);
	p.writeObject(jPlayerInformation);
	p.writeObject(jRoomArray);
	p.writeObject(jItemArray);
	p.writeObject(jObstructionArray);
	p.writeObject(jVerbArray);
	stream.close();

	print "done"


#####################################################################
# Main
#####################################################################

if __name__ == '__main__':

	(gameInformation, playerInformation, \
	directionData, roomData, \
	itemData, obstructionData, \
	verbData) = load_python_data(input_filename)

	jGameInformation = convert_game_information(gameInformation)
 	jDirectionInfoArray = convert_direction_data(directionData)
 	jRoomArray = convert_room_data(roomData)
 	jItemArray = convert_item_data(itemData)
 	jPlayerInformation = convert_player_information(playerInformation, jRoomArray, len(jItemArray))
 	jObstructionArray = convert_obstruction_data(obstructionData)
 	jVerbArray = convert_verb_data(verbData)

	# Update Totals
	jGameInformation.TotalDirections = len(directionData)
	jGameInformation.TotalRooms = len(roomData)
	jGameInformation.TotalItems = len(itemData)
	jGameInformation.TotalObstructions = len(obstructionData)
	jGameInformation.TotalVerbs = len(verbData)

	# Update Miscellaneous Data
	jPlayerInformation.CurrentRoom = jRoomArray[ playerInformation.current_room ]
	jPlayerInformation.Facing = jDirectionInfoArray[ playerInformation.facing ]

	serialize_data_file(output_filename, \
	                    jGameInformation, jPlayerInformation, \
	                    jDirectionInfoArray, jRoomArray, \
	                    jItemArray, jObstructionArray, \
	                    jVerbArray)

# EOF