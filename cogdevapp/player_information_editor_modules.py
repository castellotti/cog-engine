#####################################################################
#
# COG Engine Development Application - Player Information Editor
#
# Copyright Steven M. Castellotti (2000)
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Last Update: 2001.01.25
#
#####################################################################

#####################################################################
# Functions
#####################################################################

def on_player_information_editor_destroy(self, obj):
	# This function is called if a user closes a window directly,
	# instead of clicking off the toggle button
	self.widget.player_information_togglebutton.set_active(0)

#####################################################################

def insert_data_into_player_editor(self):
	# This function is called when a user opens the player editor. The fuction
	# configures the window's widgets according to the data stored in memory.

	self.playerInformationEditor.player_name_textentry.set_text(self.playerInformation.name)

	#print self.playerInformation.current_room
#	self.playerInformationEditor.current_room_textentry.set_text(self.playerInformation.)

	if (self.playerInformation.email_address == None):
		self.playerInformation.email_address = ""
	self.playerInformationEditor.email_address_textentry.set_text(self.playerInformation.email_address)

	# iterate through and display player's inventory
	item_list = ""
	if (len(self.playerInformation.items)):
		for each in self.playerInformation.items:
			item_list = item_list + "%i, " % each
		item_list = item_list[0:-2] # trim of any remaining punctuation (if it exists)
	self.playerInformationEditor.inventory_textentry.set_text(item_list)

	# Display statistical information
	self.playerInformationEditor.points_textentry.set_text("%i" % self.playerInformation.points)
	self.playerInformationEditor.experience_textentry.set_text("%i" % self.playerInformation.experience)
	self.playerInformationEditor.experience_level_textentry.set_text("%i" % self.playerInformation.experience_level)
	self.playerInformationEditor.hp_textentry.set_text("%i" % self.playerInformation.hp)
	self.playerInformationEditor.mp_textentry.set_text("%i" % self.playerInformation.mp)
	self.playerInformationEditor.strength_textentry.set_text("%i" % self.playerInformation.strength)
	self.playerInformationEditor.intelligence_textentry.set_text("%i" % self.playerInformation.intelligence)
	self.playerInformationEditor.dexterity_textentry.set_text("%i" % self.playerInformation.dexterity)
	self.playerInformationEditor.agility_textentry.set_text("%i" % self.playerInformation.agility)
	self.playerInformationEditor.charisma_textentry.set_text("%i" % self.playerInformation.charisma)
	self.playerInformationEditor.armor_level_textentry.set_text("%i" % self.playerInformation.armor_level)
	self.playerInformationEditor.max_weight_textentry.set_text("%i" % self.playerInformation.max_weight)
	self.playerInformationEditor.max_bulk_textentry.set_text("%i" % self.playerInformation.max_bulk)
	self.playerInformationEditor.current_weight_textentry.set_text("%i" % self.playerInformation.current_weight)
	self.playerInformationEditor.current_bulk_textentry.set_text("%i" % self.playerInformation.current_bulk)

#####################################################################

def read_player_editor_data_into_memory(self):
	# This function is called whenever the player editor is closed. The function
	# reads in the state of the various widgets and stores them into memory
	import string

	self.playerInformation.name = self.playerInformationEditor.player_name_textentry.get_text()
	#self.playerInformation. = self.playerInformationEditor.current_room_textentry.get_text()

	# Parse into memory player's inventory
	item_list = self.playerInformationEditor.inventory_textentry.get_text()
	if (item_list != ""):
		for each in string.split(item_list, ', '):
			self.playerInformation.items.append("%i" % each)

	self.playerInformation.email_address = (self.playerInformationEditor.email_address_textentry.get_text())

	# Parse player statistics
	self.playerInformation.points = string.atoi(self.playerInformationEditor.points_textentry.get_text())
	self.playerInformation.experience = string.atoi(self.playerInformationEditor.experience_textentry.get_text())
	self.playerInformation.experience_level = string.atoi(self.playerInformationEditor.experience_level_textentry.get_text())
	self.playerInformation.hp = string.atoi(self.playerInformationEditor.hp_textentry.get_text())
	self.playerInformation.mp = string.atoi(self.playerInformationEditor.mp_textentry.get_text())
	self.playerInformation.strength = string.atoi(self.playerInformationEditor.strength_textentry.get_text())
	self.playerInformation.intelligence = string.atoi(self.playerInformationEditor.intelligence_textentry.get_text())
	self.playerInformation.dexterity = string.atoi(self.playerInformationEditor.dexterity_textentry.get_text())
	self.playerInformation.agility = string.atoi(self.playerInformationEditor.agility_textentry.get_text())
	self.playerInformation.charisma = string.atoi(self.playerInformationEditor.charisma_textentry.get_text())
	self.playerInformation.armor_level = string.atoi(self.playerInformationEditor.armor_level_textentry.get_text())
	self.playerInformation.max_weight = string.atoi(self.playerInformationEditor.max_weight_textentry.get_text())
	self.playerInformation.max_bulk = string.atoi(self.playerInformationEditor.max_bulk_textentry.get_text())
	self.playerInformation.current_weight = string.atoi(self.playerInformationEditor.current_weight_textentry.get_text())
	self.playerInformation.current_bulk = string.atoi(self.playerInformationEditor.current_bulk_textentry.get_text())


#####################################################################
# Widgets
#####################################################################
# player_name_textentry
# current_room_textentry
# email_address_textentry
# inventory_textentry
# points_textentry
# experience_textentry
# experience_level_textentry
# hp_textentry
# mp_textentry
# strength_textentry
# intelligence_textentry
# dexterity_textentry
# agility_textentry
# charisma_textentry
# armor_level_textentry
# max_weight_textentry
# max_bulk_textentry
# current_weight_textentry
# current_bulk_textentry

#####################################################################
# Data Variables
#####################################################################
# self.name = "Player"
# self.email_address = ""
# # self.facing = DirectionInformationObject()
# self.points = -1
# self.experience = -1
# self.experience_level = -1
# self.hp = -1
# self.mp = -1
# self.strength = -1
# self.intelligence = -1
# self.dexterity = -1
# self.agility = -1
# self.charisma = -1
# self.armor_level = -1
# self.max_weight = -1
# self.max_bulk = -1
# self.current_weight = -1
# self.current_bulk = -1
# # self.current_room = RoomObject()
# self.items = {}


# EOF