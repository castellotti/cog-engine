#####################################################################
#
# COG Engine Development Application - Room Editor
#
# Copyright Steven M. Castellotti (2000)
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Last Update: 2001.06.12
#
#####################################################################
# Bugs
#####################################################################
#  - fix automatic selection of new direction after it is added (see comments)
#  - direction_description has been ignored!
#####################################################################

#####################################################################
# Functions
#####################################################################

def on_room_editor_destroy(self, obj):
	# This function is called if a user closes a window directly,
	# instead of clicking off the toggle button
	self.widget.room_togglebutton.set_active(0)


#####################################################################

def insert_data_into_room_editor(self, current_room_number):

	import string

	self.room_displayed = current_room_number

	self.roomEditor.room_editor_selection_textentry.set_text("%i" % self.room_displayed)

	self.roomEditor.number_textentry.set_text("%i" % self.roomData[self.room_displayed].number)
	self.roomEditor.name_textentry.set_text(self.roomData[self.room_displayed].name)
	self.roomEditor.graphic_url_textentry.set_text(self.roomData[self.room_displayed].graphic_url)

	self.roomEditor.text_description_long_textbox.delete_text(0, -1)
	self.roomEditor.text_description_long_textbox.insert_defaults(self.roomData[self.room_displayed].description_long)
	self.roomEditor.text_description_short_textbox.delete_text(0, -1)
	self.roomEditor.text_description_short_textbox.insert_defaults(self.roomData[self.room_displayed].description_short)


	# Setup Item Display
	item_display = ""
	if ( (self.roomData[self.room_displayed].items != None) and \
	     (self.roomData[self.room_displayed].items != "") ):
		item_list = string.split(self.roomData[self.room_displayed].items, ', ')
		for each in item_list:
			item_display = "%sItem[%s - %s]\n" % (item_display, each, self.itemData[string.atoi(each)].name)

	self.roomEditor.item_text.delete_text(0, -1)
	self.roomEditor.item_text.insert_defaults(item_display)


	# Setup Available Item List
	if (self.itemData == {}):
		self.roomEditor.item_list_combo.entry.set_text("No Items Available")
	else:
		item_keys = self.itemData.keys()
		item_keys.sort()
		item_list = []
		for each in item_keys:
			item_list.append("Item %i - %s" % (each, self.itemData[each].name) )
		self.roomEditor.item_list_combo.set_popdown_strings(item_list)


	# Calling the following function will set up the direction optionmenu
	# with the room's current settings.
	self.room_direction_displayed = 0
	setup_directional_object_optionmenu(self)

	# Add this room's notes to the notes_textbox
	self.roomEditor.notes_textbox.delete_text(0, -1)
	if (self.roomData[self.room_displayed].notes == None):
		self.roomData[self.room_displayed].notes = ""
	self.roomEditor.notes_textbox.insert_defaults(self.roomData[self.room_displayed].notes)


#####################################################################

def setup_directional_object_optionmenu(self):
	import gtk

	# Set up directional object optionmenu
	self.direction_menu = gtk.GtkMenu()
	self.direction_submenu = gtk.GtkMenu()

	self.roomData[self.room_displayed].direction.keys().sort()
	self.directionData.keys().sort()
	unused_direction_list = self.directionData.keys()
	unused_direction_list.sort()

	menu_default_set = 0 # we use this to make sure that the directional object information
	                     # is set by default to the data related to the first menu item

	if (self.roomData[self.room_displayed].direction != {}):
		direction_keys = self.roomData[self.room_displayed].direction.keys()
		direction_keys.sort()
		for each in direction_keys:
			del unused_direction_list[ unused_direction_list.index(each) ]
			menu_item = gtk.GtkMenuItem(self.directionData[each].name)
			# The following line could be written better - if memory space was structured better
			menu_item.connect("activate", self.setup_directional_objects, each)
			#self.direction_menu.prepend(menu_item)
			self.direction_menu.append(menu_item)
			menu_item.show()
			if (menu_default_set == 0):
				self.setup_directional_objects(None, each)
				menu_default_set = 1
				self.room_direction_displayed = each

	for each in unused_direction_list:
		menu_item = gtk.GtkMenuItem(self.directionData[each].name)
		# The following line could be written better - if memory space was structured better
		menu_item.connect("activate", self.add_new_directional_object, each)
		#self.direction_submenu.append(menu_item)
		self.direction_submenu.prepend(menu_item)
		menu_item.show()

	submenu_item = gtk.GtkMenuItem("Add New Direction")
	submenu_item.set_submenu(self.direction_submenu)
	self.direction_menu.append(submenu_item)
	submenu_item.show()

	self.roomEditor.directional_object_optionmenu.set_menu(self.direction_menu)


#####################################################################

def setup_directional_objects(self, obj, new_direction):

	import string

	# Clear textboxes
	#self.roomEditor.first_transition_text_textbox.delete_text(0, -1)
	#self.roomEditor.transition_text_textbox.delete_text(0 , -1)

	# Read all data from currently displayed room direction into memory
	self.read_direction_object_information_data_into_memory(self.room_displayed)

	# Display new room's data
# 	self.roomEditor.to_which_room_textentry.set_text("%i" % self.roomData[self.room_displayed].direction[new_direction].to_which_room)
	room_keys = self.roomData.keys()
	room_keys.sort()
	room_list = []
	room_list.append("Nowhere")
	for each in room_keys:
		room_list.append("Room %i - %s" % (each, self.roomData[each].name) )
	to_which_room = self.roomData[self.room_displayed].direction[new_direction].to_which_room
	self.roomEditor.to_which_room_combo.set_popdown_strings(room_list)
	if (to_which_room > 0):
		self.roomEditor.to_which_room_combo.entry.set_text("Room %i - %s" % (to_which_room, self.roomData[to_which_room].name) )

	if (self.roomData[self.room_displayed].direction[new_direction].has_moved_this_way):
		self.roomEditor.player_moved_this_way_true_radiobutton.set_active(1)
	else:
		self.roomEditor.player_moved_this_way_false_radiobutton.set_active(1)


	# Setup Obstruction Display
	obstruction_display = ""
	if ( (self.roomData[self.room_displayed].direction[new_direction].obstructions != None) and \
	     (self.roomData[self.room_displayed].direction[new_direction].obstructions != "") ):

		obstruction_list = string.split(self.roomData[self.room_displayed].direction[new_direction].obstructions, ', ')
		for each in obstruction_list:

			obstruction_display = "%sObstruction[%s - %s]\n" % (obstruction_display, each, self.obstructionData[string.atoi(each)].name)

	self.roomEditor.obstruction_text.delete_text(0, -1)
	self.roomEditor.obstruction_text.insert_defaults(obstruction_display)


	# Setup Available Obstruction List
	if (self.obstructionData == {}):
		self.roomEditor.obstruction_list_combo.entry.set_text("No Obstructions Available")
	else:
		obstruction_keys = self.obstructionData.keys()
		obstruction_keys.sort()
		obstruction_list = []
		for each in obstruction_keys:
			obstruction_list.append("Obstruction %i - %s" % (each, self.obstructionData[each].name) )
		self.roomEditor.obstruction_list_combo.set_popdown_strings(obstruction_list)


	if (self.roomData[self.room_displayed].direction[new_direction].first_transition_text == None):
		self.roomData[self.room_displayed].direction[new_direction].first_transition_text = ""
	self.roomEditor.first_transition_text_textentry.set_text(self.roomData[self.room_displayed].direction[new_direction].first_transition_text)
# 	self.roomEditor.first_transition_text_textbox.delete_text(0, -1)
# 	self.roomEditor.first_transition_text_textbox.insert_defaults(self.roomData[self.room_displayed].direction[new_direction].first_transition_text)

	if (self.roomData[self.room_displayed].direction[new_direction].transition_text == None):
		self.roomData[self.room_displayed].direction[new_direction].transition_text = ""
	self.roomEditor.transition_text_textentry.set_text(self.roomData[self.room_displayed].direction[new_direction].transition_text)
#	self.roomEditor.transition_text_textbox.delete_text(0, -1)
#	self.roomEditor.transition_text_textbox.insert_defaults(self.roomData[self.room_displayed].direction[new_direction].transition_text)

	if (self.roomData[self.room_displayed].direction[new_direction].first_transition_graphic == None):
		self.roomData[self.room_displayed].direction[new_direction].first_transition_graphic = ""
	self.roomEditor.first_transition_graphic_textentry.set_text(self.roomData[self.room_displayed].direction[new_direction].first_transition_graphic)

	if (self.roomData[self.room_displayed].direction[new_direction].transition_graphic == None):
		self.roomData[self.room_displayed].direction[new_direction].transition_graphic = ""
	self.roomEditor.transition_graphic_textentry.set_text(self.roomData[self.room_displayed].direction[new_direction].transition_graphic)

	self.room_direction_displayed = new_direction


#####################################################################

def add_new_directional_object(self, obj, new_direction):

	self.roomData[self.room_displayed].direction[new_direction] = self.DirectionObject()
	self.setup_directional_object_optionmenu()

#  The folowing section of code should set the new direction to display by default
#  after being added, but the update to the optionmenu does not appear to take hold
#
# 	# Set widgets to new_direction's data
# 	self.setup_directional_objects(None, new_direction)
#
#  # Set menu to display new direction
# 	direction_menu = self.roomEditor.directional_object_optionmenu.get_menu()
# 	unused_direction_list = self.roomData[self.room_displayed].direction.keys()
# 	unused_direction_list.sort()
# 	print "unused_direction_list: %s" % unused_direction_list
# 	print "new_direction: %i" % new_direction
# 	menu_index = unused_direction_list.index(new_direction)
# 	print "menu_index: %i" % menu_index
# 	direction_menu.set_active(menu_index)
# 	self.roomEditor.directional_object_optionmenu.set_menu(self.direction_menu)


#####################################################################

def read_room_editor_data_into_memory(self):
	import gtk, string

	try:
		current_room_number = string.atoi(self.roomEditor.number_textentry.get_text())
	except ValueError:
		print "Non-integer entered into current room's number field"
	else:
		self.roomData[current_room_number].number = current_room_number
		self.roomData[current_room_number].name = self.roomEditor.name_textentry.get_text()
		self.roomData[current_room_number].graphic_url = self.roomEditor.graphic_url_textentry.get_text()

		self.roomData[current_room_number].description_long = gtk.GtkEntry.get_chars(self.roomEditor.text_description_long_textbox, 0, -1)
		self.roomData[current_room_number].description_short = gtk.GtkEntry.get_chars(self.roomEditor.text_description_short_textbox, 0, -1)

		# Collect items - Divide up into individual items, convert to integers, and store.
		item_entry = gtk.GtkEntry.get_chars(self.roomEditor.item_text, 0, -1)
		if (item_entry != ""):
			item_list = string.split(item_entry, '\n')
			item_entry = ""
			for each in item_list:
				if (each != ""):
					item_name = each[5:-1]
					item_number = string.split(item_name, ' - ')[0]

					item_entry = "%s%s, " % (item_entry, item_number)

			item_entry = item_entry[:-2] # remove trailing ", "

		self.roomData[current_room_number].items = item_entry


		self.read_direction_object_information_data_into_memory(current_room_number)

		# Collect this room's notes
		self.roomData[current_room_number].notes = gtk.GtkEntry.get_chars(self.roomEditor.notes_textbox, 0, -1)


#####################################################################

def read_direction_object_information_data_into_memory(self, room_number):

	import gtk, string

	# Collect previous room's data
	if (self.room_direction_displayed != 0):
		if (self.roomEditor.to_which_room_combo.entry.get_text() == "Nowhere"):
			print "Warning! No to_which_room defined for previous direction... removing direction!"
			del (self.roomData[self.room_displayed].direction[self.room_direction_displayed])
			self.room_direction_displayed = 0
			setup_directional_object_optionmenu(self)

		else:
			#print gtk.GtkEntry.get_chars(self.roomEditor.transition_text_textbox, 0, -1)
			to_which_room_string = self.roomEditor.to_which_room_combo.entry.get_text()
			self.roomData[room_number].direction[self.room_direction_displayed].to_which_room = string.atoi( string.split(to_which_room_string, ' ')[1] )
			self.roomData[room_number].direction[self.room_direction_displayed].has_moved_this_way = self.roomEditor.player_moved_this_way_true_radiobutton.get_active()

			# Collect Obstructions - Divide up into individual obstructions, convert to integers, and store.
			obstruction_entry = gtk.GtkEntry.get_chars(self.roomEditor.obstruction_text, 0, -1)

			if (obstruction_entry != ""):
				obstruction_list = string.split(obstruction_entry, '\n')
				obstruction_entry = ""
				for each in obstruction_list:
					if (each != ""):
						obstruction_name = each[12:-1]
						obstruction_number = string.split(obstruction_name, ' - ')[0]

						obstruction_entry = "%s%s, " % (obstruction_entry, obstruction_number)

				obstruction_entry = obstruction_entry[:-2] # remove trailing ", "

			self.roomData[room_number].direction[self.room_direction_displayed].obstructions = obstruction_entry


			self.roomData[room_number].direction[self.room_direction_displayed].first_transition_text = self.roomEditor.first_transition_text_textentry.get_text()
			self.roomData[room_number].direction[self.room_direction_displayed].transition_text = self.roomEditor.transition_text_textentry.get_text()
			self.roomData[room_number].direction[self.room_direction_displayed].first_transition_graphic = self.roomEditor.first_transition_graphic_textentry.get_text()
			self.roomData[room_number].direction[self.room_direction_displayed].transition_graphic = self.roomEditor.transition_graphic_textentry.get_text()


#####################################################################

def create_new_room(self):
	new_room_number = len(self.roomData) + 1
	self.roomData[new_room_number] = self.RoomObject()
	self.roomData[new_room_number].number = len(self.roomData)
	self.roomEditor.to_which_room_combo-entry.set_text("")


#####################################################################

def clear_current_room(self):
	self.roomData[self.room_displayed] = self.RoomObject()
	self.roomData[self.room_displayed].number = self.room_displayed
	self.roomEditor.to_which_room_combo-entry.set_text("")
	self.room_direction_displayed = 0


#####################################################################

def on_room_editor_new_button_clicked(self, obj):
	self.read_room_editor_data_into_memory()
	self.create_new_room()
	self.insert_data_into_room_editor(len(self.roomData))


#####################################################################

def on_room_editor_first_button_clicked(self, obj):
	if (self.room_displayed != 1):
		self.read_room_editor_data_into_memory()
		self.insert_data_into_room_editor(1)
	else:
		print "Already in first room"


#####################################################################

def on_room_editor_previous_button_clicked(self, obj):
	if ((self.room_displayed - 1) > 0):
		self.read_room_editor_data_into_memory()
		self.insert_data_into_room_editor(self.room_displayed - 1)
	else:
		print "Already in first room"


#####################################################################

def on_room_editor_next_button_clicked(self, obj):
	if ((self.room_displayed + 1) <= len(self.roomData)):
		self.read_room_editor_data_into_memory()
		self.insert_data_into_room_editor(self.room_displayed + 1)
	else:
		print "Already in last room"


#####################################################################

def on_room_editor_last_button_clicked(self, obj):
	if (self.room_displayed != len(self.roomData)):
		self.read_room_editor_data_into_memory()
		self.insert_data_into_room_editor(len(self.roomData))
	else:
		print "Already in last room"


#####################################################################

def on_room_editor_selection_textentry_activate(self, obj):
	import string
	new_room_number_entry = self.roomEditor.room_editor_selection_textentry.get_text()
	new_room_number_entry = string.strip(new_room_number_entry)
	try:
		new_room_number = string.atoi(new_room_number_entry)
	except ValueError:
		print "Bad value entered into Room Editor's goto field"
	else:
		if (self.roomData.has_key(new_room_number)):
			self.read_room_editor_data_into_memory()
			self.insert_data_into_room_editor(new_room_number)
		else:
			print "That room number doesn't exist!"


#####################################################################

def on_room_editor_clear_button_clicked(self, obj):
	self.clear_current_room()
	self.insert_data_into_room_editor(self.room_displayed)


#####################################################################

def on_room_editor_add_item_button_clicked(self, obj):

	selected_item = self.roomEditor.item_list_combo.entry.get_text()
	if (selected_item != "No Items Available"):

		import gtk, string

		selected_item = selected_item[5:]
		selected_item = "Item[%s]" % selected_item

		current_item_display = gtk.GtkEntry.get_chars(self.roomEditor.item_text, 0, -1)

		if (current_item_display == ""):

			self.roomEditor.item_text.insert_defaults(selected_item)

		elif ( string.find(current_item_display, selected_item) == -1 ):
			# We don't want to add the same item twice
			self.roomEditor.item_text.delete_text(0, -1)
			new_item_display = "%s\n%s" % (current_item_display, selected_item)
			self.roomEditor.item_text.insert_defaults(new_item_display)


#####################################################################

def on_room_editor_add_obstruction_button_clicked(self, obj):

# start here

	selected_obstruction = self.roomEditor.obstruction_list_combo.entry.get_text()
	if (selected_obstruction != "No Obstructions Available"):

		import gtk, string
		selected_obstruction = selected_obstruction[12:]
		selected_obstruction = "Obstruction[%s]" % selected_obstruction

		current_obstruction_display = gtk.GtkEntry.get_chars(self.roomEditor.obstruction_text, 0, -1)

		if (current_obstruction_display == ""):

			self.roomEditor.obstruction_text.insert_defaults(selected_obstruction)

		elif ( string.find(current_obstruction_display, selected_obstruction) == -1 ):
			# We don't want to add the same Obstruction twice
			self.roomEditor.obstruction_text.delete_text(0, -1)
			new_obstruction_display = "%s\n%s" % (current_obstruction_display, selected_obstruction)
			self.roomEditor.obstruction_text.insert_defaults(new_obstruction_display)


#####################################################################
# Widgets
#####################################################################
# room_editor_new_button
# room_editor_first_button
# room_editor_previous_button
# room_editor_next_button
# room_editor_last_button
# room_editor_selection_textentry
# room_editor_delete_button

# number_textentry
# name_textentry
# graphic_url_textentry
# text_description_long_textbox
# text_description_short_textbox
# directions_textentry
# items_textentry
# directional_object_optionmenu
# player_moved_this_way_true_radiobutton
# player_moved_this_way_false_radiobutton
# obstruction_textentry
# transition_text_textbox
# first_transition_text_textbox
# first_transition_graphic_textentry
# notes_textbox

#####################################################################
# Data Variables
#####################################################################
# self.number = -1
# self.name = ""
# self.visited = 0 # boolean
# self.graphic_url = ""
# self.description_long = ""
# self.description_short = ""
# self.direction = {}
# self.items = ""
# self.notes = ""


# EOF