#####################################################################
#
# COG Engine Development Application - Item Editor
#
# Copyright Steven M. Castellotti (2000)
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Last Update: 2001.06.11
#
#####################################################################

#####################################################################
# Functions
#####################################################################

def on_item_editor_destroy(self, obj):
	# This function is called if a user closes a window directly,
	# instead of clicking off the toggle button
	self.widget.item_togglebutton.set_active(0)


#####################################################################

def insert_data_into_item_editor(self, current_item_number):

	import string

	self.item_displayed = current_item_number

	if (len(self.itemData) is 0):
		self.itemData[self.item_displayed] = self.ItemObject()
		self.itemData[self.item_displayed].number = 1

	self.itemEditor.item_editor_selection_textentry.set_text("%i" % self.itemData[self.item_displayed].number)

	self.itemEditor.number_textentry.set_text("%i" % self.itemData[self.item_displayed].number)
	self.itemEditor.name_textentry.set_text(self.itemData[self.item_displayed].name)

	if (self.itemData[self.item_displayed].aliases == None):
		self.itemData[self.item_displayed].aliases = ""
	self.itemEditor.aliases_textentry.set_text(self.itemData[self.item_displayed].aliases)

	if (self.itemData[self.item_displayed].environment_graphic_url == None):
		self.itemData[self.item_displayed].environment_graphic_url = ""
	self.itemEditor.environmental_graphic_textentry.set_text(self.itemData[self.item_displayed].environment_graphic_url)

	if (self.itemData[self.item_displayed].environment_graphic_Xpos == None):
		self.itemData[self.item_displayed].environment_graphic_Xpos = 0
	self.itemEditor.environmental_graphic_x_textentry.set_text("%i" % self.itemData[self.item_displayed].environment_graphic_Xpos)

	if (self.itemData[self.item_displayed].environment_graphic_Ypos == None):
		self.itemData[self.item_displayed].environment_graphic_Ypos = 0
	self.itemEditor.environmental_graphic_y_textentry.set_text("%i" % self.itemData[self.item_displayed].environment_graphic_Ypos)

	if (self.itemData[self.item_displayed].closeup_graphic_url == None):
		self.itemData[self.item_displayed].closeup_graphic_url = ""
	self.itemEditor.closeup_graphic_textentry.set_text(self.itemData[self.item_displayed].closeup_graphic_url)

	if (self.itemData[self.item_displayed].icon_graphic_url == None):
		self.itemData[self.item_displayed].icon_graphic_url = ""
	self.itemEditor.icon_graphic_textentry.set_text(self.itemData[self.item_displayed].icon_graphic_url)

	if (self.itemData[self.item_displayed].equipped_graphic_url == None):
		self.itemData[self.item_displayed].equipped_graphic_url = ""
	self.itemEditor.equipped_graphic_textentry.set_text(self.itemData[self.item_displayed].equipped_graphic_url)

	self.itemEditor.description_textbox.delete_text(0, -1)
	if (self.itemData[self.item_displayed].description != None):
		self.itemEditor.description_textbox.insert_defaults(self.itemData[self.item_displayed].description)

	# Setup Locations

# 	# The follow code assumes that items can only exist in one location,
# 	# which is currently not true, and therefore this code is disabled
# 	location_list = []
# 	location_list.append("Nowhere")
# 	room_keys = self.roomData.keys()
# 	room_keys.sort()
# 	for each in room_keys:
# 		location_list.append("Room %i - %s" % (each, self.roomData[each].name) )
#
# 	self.itemEditor.location_combo.set_popdown_strings(location_list)
#
# 	if (self.itemData[self.item_displayed].location != "") and \
# 	   (self.itemData[self.item_displayed].location != "0"):
# 		import string
# 		current_item_location = string.atoi(self.itemData[self.item_displayed].location)
# 		self.itemEditor.location_combo.entry.set_text("Room %i - %s" % (current_item_location, self.roomData[current_item_location].name) )
#
# 	self.itemEditor.location_textentry.set_text(self.itemData[self.item_displayed].location)

	# Setup Location Display
	location_display = ""
	room_keys = self.roomData.keys()
	room_keys.sort()
	room_list = []
	for each in room_keys:
	 	if ( (self.roomData[each].items != None) and \
		     (self.roomData[each].items != "") ):
			item_list = string.split(self.roomData[each].items, ', ')
			for item in item_list:
				if ( string.atoi(item) == self.item_displayed ):
					room_list.append(each)

	for each in room_list:
		location_display = "%sRoom[%i - %s]\n" % (location_display, each, self.roomData[each].name)

	self.itemEditor.location_text.delete_text(0, -1)
	self.itemEditor.location_text.insert_defaults(location_display)


	if (self.itemData[self.item_displayed].equipped):
		self.itemEditor.equipped_true_radiobutton.set_active(1)
	else:
		self.itemEditor.equipped_false_radiobutton.set_active(1)

	self.itemEditor.weight_textentry.set_text("%i" % self.itemData[self.item_displayed].weight)
	self.itemEditor.bulk_textentry.set_text("%i" % self.itemData[self.item_displayed].bulk)

	self.itemEditor.notes_textbox.delete_text(0, -1)
	if (self.itemData[self.item_displayed].notes != None):
		self.itemEditor.notes_textbox.insert_defaults(self.itemData[self.item_displayed].notes)


#####################################################################

def read_item_editor_data_into_memory(self):
	import gtk, string

	if (self.itemEditor.name_textentry.get_text() != ""):
		try:
			current_item_number = string.atoi(self.itemEditor.number_textentry.get_text())
		except ValueError:
			print "Non-integer entered into current item's number field"
		else:
			self.itemData[current_item_number].number = current_item_number
			self.itemData[current_item_number].name = self.itemEditor.name_textentry.get_text()
			self.itemData[current_item_number].aliases = self.itemEditor.aliases_textentry.get_text()
			self.itemData[current_item_number].environment_graphic_url = self.itemEditor.environmental_graphic_textentry.get_text()
			if (self.itemData[current_item_number].environment_graphic_url == ""):
				self.itemData[current_item_number].environment_graphic_url = None
			self.itemData[current_item_number].environment_graphic_Xpos = string.atoi( self.itemEditor.environmental_graphic_x_textentry.get_text() )
			self.itemData[current_item_number].environment_graphic_Ypos = string.atoi( self.itemEditor.environmental_graphic_y_textentry.get_text() )
			self.itemData[current_item_number].closeup_graphic_url = self.itemEditor.closeup_graphic_textentry.get_text()
			if (self.itemData[current_item_number].closeup_graphic_url == ""):
				self.itemData[current_item_number].closeup_graphic_url = None
			self.itemData[current_item_number].icon_graphic_url = self.itemEditor.icon_graphic_textentry.get_text()
			if (self.itemData[current_item_number].icon_graphic_url == ""):
				self.itemData[current_item_number].icon_graphic_url = None
			self.itemData[current_item_number].equipped_graphic_url = self.itemEditor.equipped_graphic_textentry.get_text()
			if (self.itemData[current_item_number].equipped_graphic_url == ""):
				self.itemData[current_item_number].equipped_graphic_url = None

			self.itemData[current_item_number].description = gtk.GtkEntry.get_chars(self.itemEditor.description_textbox, 0, -1)

			self.itemData[current_item_number].equipped =  self.itemEditor.equipped_true_radiobutton.get_active()

			self.itemData[current_item_number].weight = string.atoi( self.itemEditor.weight_textentry.get_text() )
			self.itemData[current_item_number].bulk = string.atoi( self.itemEditor.bulk_textentry.get_text() )

			self.itemData[current_item_number].notes = gtk.GtkEntry.get_chars(self.itemEditor.notes_textbox, 0, -1)


	else:
		print "No name entered for this item! item will be skipped."


#####################################################################

def create_new_item(self):
	new_item_number = len(self.itemData) + 1
	self.itemData[new_item_number] = self.ItemObject()
	self.itemData[new_item_number].number = len(self.itemData)


#####################################################################

def clear_current_item(self):
	self.itemData[self.item_displayed] = self.itemObject()
	self.itemData[self.item_displayed].number = self.item_displayed
	self.itemEditor.to_which_item_textentry.set_text("")
	self.item_item_displayed = 0


#####################################################################

def on_item_editor_new_button_clicked(self, obj):
	self.read_item_editor_data_into_memory()
	self.create_new_item()
	self.insert_data_into_item_editor(len(self.itemData))


#####################################################################

def on_item_editor_first_button_clicked(self, obj):
	if (self.item_displayed != 1):
		self.read_item_editor_data_into_memory()
		self.insert_data_into_item_editor(1)
	else:
		print "Already in first item"


#####################################################################

def on_item_editor_previous_button_clicked(self, obj):
	if ((self.item_displayed - 1) > 0):
		self.read_item_editor_data_into_memory()
		self.insert_data_into_item_editor(self.item_displayed - 1)
	else:
		print "Already in first item"


#####################################################################

def on_item_editor_next_button_clicked(self, obj):
	if ((self.item_displayed + 1) <= len(self.itemData)):
		self.read_item_editor_data_into_memory()
		self.insert_data_into_item_editor(self.item_displayed + 1)
	else:
		print "Already in last item"


#####################################################################

def on_item_editor_last_button_clicked(self, obj):
	if (self.item_displayed != len(self.itemData)):
		self.read_item_editor_data_into_memory()
		self.insert_data_into_item_editor(len(self.itemData))
	else:
		print "Already in last item"


#####################################################################

def on_item_editor_selection_textentry_activate(self, obj):
	import string
	new_item_number_entry = self.itemEditor.item_editor_selection_textentry.get_text()
	new_item_number_entry = string.strip(new_item_number_entry)
	try:
		new_item_number = string.atoi(new_item_number_entry)
	except ValueError:
		print "Bad value entered into item Editor's goto field"
	else:
		if (self.itemData.has_key(new_item_number)):
			self.read_item_editor_data_into_memory()
			self.insert_data_into_item_editor(new_item_number)
		else:
			print "That item number doesn't exist!"


#####################################################################

def on_item_editor_clear_button_clicked(self, obj):
	self.clear_current_item()
	self.insert_data_into_item_editor(self.item_displayed)


#####################################################################
# Widgets
#####################################################################
# item_editor_selection_textentry
# number_textentry
# name_textentry
# aliases_textentry
# environmental_graphic_textentry
# environmental_graphic_x_textentry
# environmental_graphic_y_textentry
# closeup_graphic_textentry
# icon_graphic_textentry
# equipped_graphic_textentry
# description_textbox
# location_textentry
# equipped_true_radiobutton
# equipped_false_radiobutton
# weight_textentry
# bulk_textentry
# notes_textbox
#####################################################################
# Data Variables
#####################################################################
# self.number = -1
# self.name = ""
# self.aliases = ""
# self.environment_graphic_url = ""
# self.environment_graphic_Xpos = 0
# self.environment_graphic_Ypos = 0
# self.closeup_graphic_url = ""
# self.icon_graphic_url = ""
# self.equipped_graphic_url = ""
# self.description = ""
# self.location = ""
# self.equipped = 0 # boolean
# self.weight = 0 # negative weight implies that object cannot be picked up
# self.bulk = 0 # negative bulk indicates how much a "container" can hold (if item is a container)
# self.notes = ""

# EOF