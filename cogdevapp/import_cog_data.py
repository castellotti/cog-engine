#!/usr/bin/env jython
#
# CogEngine Data Importer
#
# Copyright Steven M. Castellotti (2001)
# The author can be reached at: SteveC@innocent.com
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Version x.x
# Last Update: 2001.12.25
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

# input_filename = "Cycon-COG.dat"
# output_filename = "Cycon-COG.dev"
input_filename = sys.argv[-2]
output_filename = sys.argv[-1]
cPython_library_path = '/usr/lib/python1.5/'

#####################################################################
# Functions
#####################################################################

def deserialize_data(filename):

	# This function takes in the name of a COG Engine Data File
	# as a parameter, and attempts to read into memory the objects
	# serialized inside of it. Those objects are then returned to
	# the calling function.

	from java.io import FileInputStream, ObjectInputStream
	istream = FileInputStream(filename)
	p = ObjectInputStream(istream)

	gameInformation = p.readObject()
	directionInfoArray = p.readObject()
	playerInformation = p.readObject()
	roomArray = p.readObject()
	itemArray = p.readObject()
	obstructionArray = p.readObject()
	verbArray = p.readObject()
	istream.close()

	return(gameInformation, directionInfoArray, \
	       playerInformation, roomArray, \
	       itemArray, obstructionArray, \
	       verbArray)


#####################################################################

def convert_game_information(java, python):
	print "Converting Game Information...",
	python.game_title = java.Game_Title
	python.version_number = java.Version_Number
	python.game_designer = java.Game_Designer
	python.game_designer_email_address = java.Game_Designer_Email_Address
	python.last_update = java.LastUpdate
	python.debug_mode = java.DebugMode
	python.game_url = java.GameURL
	python.database_url = java.DatabaseURL
	python.total_rooms = java.TotalRooms
	python.total_directions = java.TotalDirections
	python.total_items = java.TotalItems
	python.total_obstructions = java.TotalObstructions
	python.total_verbs = java.TotalVerbs
	python.show_all_verbs = java.ShowAllVerbs
	python.introduction_text = java.Introduction_Text
	python.image_loading_graphic_url = java.ImageLoading_GraphicURL
	python.introduction_graphic_url = java.Introduction_GraphicURL
	python.image_directory = java.Image_Directory
	python.preferred_graphic_size_X = java.PreferredGraphicSizeX
	python.preferred_graphic_size_Y = java.PreferredGraphicSizeY
	python.show_graphic_area = java.ShowGraphicArea
	python.show_stats = java.ShowStats
	python.show_inventory = java.ShowInventory
	python.show_command_line = java.ShowCommandLine
	python.show_text_output_area = java.ShowOutputArea
	python.show_compass = java.ShowCompass
	python.center_button_indicates_items = java.CenterButtonIndicatesItems
	python.load_all_compass_images = java.LoadAllCompassImages
	python.menu_button_graphic_url = java.MenuButton_GraphicURL
	python.game_information_notes = java.GameInfoHeaderNotes
	print "done"
	return(python)


#####################################################################

def convert_player_information(java, python):
	print "Converting Player Information...",
	python.name = java.Name
	python.email_address = java.Email_Address
	python.points = java.Points
	python.experience = java.Exp
	python.experience_level = java.experienceLevel
	python.hp = java.HP
	python.mp = java.MP
	python.strength = java.Str
	python.intelligence = java.IQ
	python.dexterity = java.Dex
	python.agility = java.Agil
	python.charisma = java.Charisma
	python.armor_level = java.Armor_Level
	python.max_weight = java.Max_Weight
	python.max_bulk = java.Max_Bulk
	python.current_weight = java.Current_Weight
	python.current_bulk = java.Current_Bulk
	if (java.CurrentRoom != None):
		python.current_room = java.CurrentRoom.Number
	if (java.Facing != None):
		python.facing = java.Facing.Number
	# handle items list
	itemCounter = 1
	while (itemCounter <= len(java.Items) - 1):
		if (java.Items[itemCounter]):
			python.items.append(itemCounter)
			python.items.sort()
		itemCounter = itemCounter + 1
	print "done"
	return(python)


#####################################################################

def convert_direction_data(directionInfoArray):
	print "Converting Direction Data...",
	directionData = {}
	directionCounter = 1
	while (directionCounter <= len(directionInfoArray) - 1):
		currentDirection = DirectionInformationObject()
		currentDirection.number = directionInfoArray[directionCounter].Number
		currentDirection.name = directionInfoArray[directionCounter].Name
		currentDirection.abbreviation = directionInfoArray[directionCounter].Abbreviation
		currentDirection.compass_graphic_available_url = directionInfoArray[directionCounter].CG_AvailableURL
		currentDirection.compass_graphic_unavailable_url = directionInfoArray[directionCounter].CG_UnavailableURL
		currentDirection.compass_graphic_special_url = directionInfoArray[directionCounter].CG_SpecialURL
  		directionData[directionCounter] = currentDirection
		directionCounter = directionCounter + 1
	directionData.keys().sort()
	print "done"
	return(directionData)


#####################################################################

def convert_room_data(roomArray):
	print "Converting Room Data...",
	roomData = {}
	roomCounter = 1
	while (roomCounter <= len(roomArray) - 1):
		currentRoom = RoomObject()
 		currentRoom.number = roomArray[roomCounter].Number
  		currentRoom.name = roomArray[roomCounter].Name
  		currentRoom.visited = roomArray[roomCounter].Visited
  		currentRoom.graphic_url = roomArray[roomCounter].GraphicURL
  		currentRoom.description_long = roomArray[roomCounter].Description_Long
  		currentRoom.description_short = roomArray[roomCounter].Description_Short
		currentRoom.direction_description = roomArray[roomCounter].Direction_Description
  		currentRoom.items = roomArray[roomCounter].Items
  		currentRoom.notes = roomArray[roomCounter].Notes
		# Handle direction objects
		directionCounter = 1
		while (directionCounter <= len(roomArray[roomCounter].DirectionArray) - 1):
			javaDirection = roomArray[roomCounter].DirectionArray[directionCounter]
			if (javaDirection != None):
				currentDirection = DirectionObject()
				currentDirection.to_which_room = javaDirection.ToWhichRoom
				currentDirection.obstructions = javaDirection.Obstructions
				currentDirection.has_moved_this_way = javaDirection.HasMovedThisWay
				currentDirection.first_transition_text = javaDirection.FirstTransitionText
				currentDirection.transition_text = javaDirection.TransitionText
				currentDirection.first_transition_graphic = javaDirection.FirstTransitionGraphic
				currentDirection.transition_graphic = javaDirection.TransitionGraphic
				# currentDirction.state = javaDirection.State
				currentRoom.direction[directionCounter] = currentDirection
			directionCounter = directionCounter + 1
  		roomData[currentRoom.number] = currentRoom
		roomData[currentRoom.number].direction.keys().sort()
		roomCounter = roomCounter + 1
	roomData.keys().sort()
	print "done"
	return(roomData)


#####################################################################

def convert_item_data(itemArray):
	print "Converting Item Data...",
	itemData = {}
	itemCounter = 1
	while (itemCounter <= len(itemArray) - 1):
		currentItem = ItemObject()
		currentItem.number = itemArray[itemCounter].Number
		currentItem.name = itemArray[itemCounter].Name
		currentItem.aliases = itemArray[itemCounter].Aliases
		currentItem.environment_graphic_url = itemArray[itemCounter].Environment_GraphicURL
		currentItem.environment_graphic_Xpos = itemArray[itemCounter].Environment_Graphic_Xpos
		currentItem.environment_graphic_Ypos = itemArray[itemCounter].Environment_Graphic_Ypos
		currentItem.closeup_graphic_url = itemArray[itemCounter].CloseUp_GraphicURL
		currentItem.icon_graphic_url = itemArray[itemCounter].Icon_GraphicURL
		currentItem.equipped_graphic_url = itemArray[itemCounter].Equipped_GraphicURL
		currentItem.description = itemArray[itemCounter].Description
		currentItem.location = itemArray[itemCounter].Location
		currentItem.equipped = itemArray[itemCounter].Equipped
		currentItem.weight = itemArray[itemCounter].Weight
		currentItem.bulk = itemArray[itemCounter].Bulk
		currentItem.notes = itemArray[itemCounter].Notes
  		itemData[currentItem.number] = currentItem
		itemCounter = itemCounter + 1
	itemData.keys().sort()
	print "done"
	return(itemData)


#####################################################################

def convert_obstruction_data(obstructionArray):
	print "Converting Obstruction Data...",
	obstructionData = {}
	obstructionCounter = 1
	while (obstructionCounter <= len(obstructionArray) - 1):
		currentObstruction = ObstructionObject()
		currentObstruction.number = obstructionArray[obstructionCounter].Number
		currentObstruction.name = obstructionArray[obstructionCounter].Name
		currentObstruction.aliases = obstructionArray[obstructionCounter].Aliases
		currentObstruction.environment_graphic_url = obstructionArray[obstructionCounter].Environment_GraphicURL
		currentObstruction.environment_graphic_Xpos = obstructionArray[obstructionCounter].Environment_Graphic_Xpos
		currentObstruction.environment_graphic_Ypos = obstructionArray[obstructionCounter].Environment_Graphic_Ypos
		currentObstruction.closeup_graphic_url = obstructionArray[obstructionCounter].CloseUp_GraphicURL
		currentObstruction.description = obstructionArray[obstructionCounter].Description
		currentObstruction.type = obstructionArray[obstructionCounter].Type
		currentObstruction.locations = obstructionArray[obstructionCounter].Locations
		currentObstruction.visible = obstructionArray[obstructionCounter].Visible
		currentObstruction.notes = obstructionArray[obstructionCounter].Notes
  		obstructionData[currentObstruction.number] = currentObstruction
		obstructionCounter = obstructionCounter + 1
	print "done"
	obstructionData.keys().sort()
	return(obstructionData)


#####################################################################

def convert_verb_data(verbArray):
	print "Converting Verb/Event Data...",
	verbData = {}
	verbCounter = 1
	while (verbCounter <= len(verbArray) - 1):
		currentVerb = VerbObject()
		currentVerb.number = verbArray[verbCounter].Number
		currentVerb.name = verbArray[verbCounter].Name
		currentVerb.aliases = verbArray[verbCounter].Aliases
		# Handle Events for this Verb
		eventCounter = 1
		while (eventCounter <= len(verbArray[verbCounter].Events) - 1):
			javaEvent = verbArray[verbCounter].Events[eventCounter]
			currentEvent = EventObject()
			currentEvent.action = javaEvent.Action
			currentEvent.object = javaEvent.Object
			currentEvent.preposition = javaEvent.Preposition
			currentEvent.object2 = javaEvent.Object2
			currentEvent.requirements = javaEvent.Requirements
			currentEvent.effects = javaEvent.EffectString
			currentEvent.has_been_executed = javaEvent.HasBeenExecuted
			currentVerb.events[eventCounter] = currentEvent
			eventCounter = eventCounter + 1
		currentVerb.events.keys().sort()
		currentVerb.total_events = verbArray[verbCounter].TotalEvents
  		verbData[currentVerb.number] = currentVerb
		verbCounter = verbCounter + 1
	verbData.keys().sort()
	print "done"
	return(verbData)


#####################################################################

def add_cPython_modules():
	import sys
	import __main__
	sys.path.append(__main__.cPython_library_path)


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

	(jGameInformation, jDirectionInfoArray, \
	jPlayerInformation, jRoomArray, \
	jItemArray, jObstructionArray, \
	jVerbArray) = deserialize_data(input_filename)

	gameInformation = convert_game_information(jGameInformation, GameInformationObject())
	playerInformation = convert_player_information(jPlayerInformation, PlayerInformationObject())
	directionData = convert_direction_data(jDirectionInfoArray)
	roomData = convert_room_data(jRoomArray)
	itemData = convert_item_data(jItemArray)
	obstructionData = convert_obstruction_data(jObstructionArray)
	verbData = convert_verb_data(jVerbArray)

	pickle_python_data_file(output_filename, \
									gameInformation, playerInformation, \
									directionData, roomData, \
									itemData, obstructionData, verbData)

# EOF
