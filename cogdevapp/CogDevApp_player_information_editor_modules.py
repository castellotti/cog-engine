#####################################################################
#
# COG Engine Development Application - Player Information Editor
#
# Copyright Steven M. Castellotti (2001)
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Last Update: 2001.06.13
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

	import string

	self.playerInformationEditor.player_name_textentry.set_text(self.playerInformation.name)

	if (self.playerInformation.email_address == None):
		self.playerInformation.email_address = ""
	self.playerInformationEditor.email_address_textentry.set_text(self.playerInformation.email_address)


	#self.playerInformationEditor.current_room_textentry.set_text("%i" % self.playerInformation.current_room)

	# Setup Current Room Combo
	room_list = []
	room_keys = self.roomData.keys()
	room_keys.sort()
	for each in room_keys:
		room_list.append("Room[%i - %s]" % (each, self.roomData[each].name) )

	self.playerInformationEditor.current_room_combo.set_popdown_strings(room_list)
	self.playerInformationEditor.current_room_combo.entry.set_text("Room[%i - %s]" % \
	   (self.playerInformation.current_room, self.roomData[self.playerInformation.current_room].name) )


	# Setup Inventory Display
	inventory_display = ""
	for each in self.playerInformation.items:
		inventory_display = "%sItem[%i - %s]\n" % (inventory_display, each, self.itemData[each].name)

	self.playerInformationEditor.inventory_text.set_wrap_mode(gtk.WRAP_WORD)
	self.playerInformationEditor.inventory_text.get_buffer().delete(self.playerInformationEditor.inventory_text.get_buffer().get_start_iter(), self.playerInformationEditor.inventory_text.get_buffer().get_end_iter())
	self.playerInformationEditor.inventory_text.get_buffer().insert_at_cursor(inventory_display)


	# Setup Available Item List
	if (self.itemData == {}):
		self.playerInformationEditor.item_list_combo.entry.set_text("No Items Available")
	else:
		item_keys = self.itemData.keys()
		item_keys.sort()
		item_list = []
		for each in item_keys:
			item_list.append("Item %i - %s" % (each, self.itemData[each].name) )
		self.playerInformationEditor.item_list_combo.set_popdown_strings(item_list)


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

	import gtk, string

	self.playerInformation.name = self.playerInformationEditor.player_name_textentry.get_text()
	self.playerInformation.email_address = (self.playerInformationEditor.email_address_textentry.get_text())


	# Get Player's Current Room Setting
	current_room_entry = self.playerInformationEditor.current_room_combo.entry.get_text()
	if (current_room_entry != ""):
		room_name = current_room_entry[5:-1]
		room_number = string.split(room_name, ' - ')[0]

		self.playerInformation.current_room = string.atoi(room_number)


	# Collect items - Divide up into individual items, convert to integers, and store.
	inventory_list = []
	inventory_data = gtk.GtkEditable.get_chars(self.playerInformationEditor.inventory_text, 0, -1)
	if (inventory_data != ""):
		item_list = string.split(inventory_data, '\n')
		for each in item_list:
			if (each != ""):
				item_name = each[5:-1]
				item_number = string.split(item_name, ' - ')[0]

				inventory_list.append( string.atoi(item_number) )

	self.playerInformation.items = inventory_list


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

def on_player_editor_add_item_button_clicked(self, obj):

	selected_item = self.playerInformationEditor.item_list_combo.entry.get_text()
	if (selected_item != "No Items Available"):

		import gtk, string

		selected_item = selected_item[5:]
		selected_item = "Item[%s]" % selected_item

		current_item_display = gtk.GtkEditable.get_chars(self.playerInformationEditor.inventory_text, 0, -1)

		if (current_item_display == ""):

			self.playerInformationEditor.inventory_text.get_buffer().insert_at_cursor(selected_item)

		elif ( string.find(current_item_display, selected_item) == -1 ):
			# We don't want to add the same item twice
			self.playerInformationEditor.inventory_text.get_buffer().delete(self.playerInformationEditor.inventory_text.get_buffer().get_start_iter(), self.playerInformationEditor.inventory_text.get_buffer().get_end_iter())
			new_item_display = "%s\n%s" % (current_item_display, selected_item)
			self.playerInformationEditor.inventory_text.get_buffer().insert_at_cursor(new_item_display)


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
