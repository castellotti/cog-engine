#####################################################################
#
# COG Engine Development Application - Obstruction Editor
#
# Copyright Steven M. Castellotti (2000)
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Last Update: 2001.09.22
#
#####################################################################
#
# Notes:
#  - The reference to "Type" of obstruction has been removed
#
#####################################################################

#####################################################################
# Functions
#####################################################################

def on_obstruction_editor_destroy(self, obj):
	# This function is called if a user closes a window directly,
	# instead of clicking off the toggle button
	self.widget.obstruction_togglebutton.set_active(0)

#####################################################################

def insert_data_into_obstruction_editor(self, current_obstruction_number):

	import string

	self.obstruction_displayed = current_obstruction_number

	if (len(self.obstructionData) is 0):
		self.obstructionData[self.obstruction_displayed] = self.ObstructionObject()
		self.obstructionData[self.obstruction_displayed].number = 1

	self.obstructionEditor.obstruction_editor_selection_textentry.set_text("%i" % self.obstructionData[self.obstruction_displayed].number)

	self.obstructionEditor.number_textentry.set_text("%i" % self.obstructionData[self.obstruction_displayed].number)
	self.obstructionEditor.name_textentry.set_text(self.obstructionData[self.obstruction_displayed].name)

	if (self.obstructionData[self.obstruction_displayed].aliases == None):
		self.obstructionData[self.obstruction_displayed].aliases = ""
	self.obstructionEditor.aliases_textentry.set_text(self.obstructionData[self.obstruction_displayed].aliases)

	if (self.obstructionData[self.obstruction_displayed].environment_graphic_url == None):
		self.obstructionData[self.obstruction_displayed].environment_graphic_url = ""
	self.obstructionEditor.environmental_graphic_textentry.set_text(self.obstructionData[self.obstruction_displayed].environment_graphic_url)

	if (self.obstructionData[self.obstruction_displayed].environment_graphic_Xpos == None):
		self.obstructionData[self.obstruction_displayed].environment_graphic_Xpos = 0
	self.obstructionEditor.environmental_graphic_x_textentry.set_text("%i" % self.obstructionData[self.obstruction_displayed].environment_graphic_Xpos)

	if (self.obstructionData[self.obstruction_displayed].environment_graphic_Ypos == None):
		self.obstructionData[self.obstruction_displayed].environment_graphic_Ypos = 0
	self.obstructionEditor.environmental_graphic_y_textentry.set_text("%i" % self.obstructionData[self.obstruction_displayed].environment_graphic_Ypos)

	if (self.obstructionData[self.obstruction_displayed].closeup_graphic_url == None):
		self.obstructionData[self.obstruction_displayed].closeup_graphic_url = ""
	self.obstructionEditor.closeup_graphic_textentry.set_text(self.obstructionData[self.obstruction_displayed].closeup_graphic_url)

	self.obstructionEditor.description_textbox.delete_text(0, -1)
	if (self.obstructionData[self.obstruction_displayed].description != None):
		self.obstructionEditor.description_textbox.insert_defaults(self.obstructionData[self.obstruction_displayed].description)

#	if (self.obstructionData[self.obstruction_displayed].type == None):
#		self.obstructionData[self.obstruction_displayed].type = ""
#	self.obstructionEditor.type_textentry.set_text(self.obstructionData[self.obstruction_displayed].type)

	# Setup Location Display
	location_display = ""
	room_keys = self.roomData.keys()
	room_keys.sort()
	for room in room_keys:

		direction_keys = self.roomData[room].direction.keys()
		direction_keys.sort()

		for direction in direction_keys:

			if ( (self.roomData[room].direction[direction].obstructions != None) and \
			     (self.roomData[room].direction[direction].obstructions != "") ):

					obstruction_list = string.split(self.roomData[room].direction[direction].obstructions, ', ')

					for obstruction in obstruction_list:
						if ( string.atoi(obstruction) == self.obstruction_displayed ):

							location_display = "%sRoom[%i - %s]Direction[%s]\n" % (location_display, room, self.roomData[room].name, self.directionData[direction].name)

	self.obstructionEditor.location_text.delete_text(0, -1)
	self.obstructionEditor.location_text.insert_defaults(location_display)


	if (self.obstructionData[self.obstruction_displayed].visible):
		self.obstructionEditor.visible_true_radiobutton.set_active(1)
	else:
		self.obstructionEditor.visible_false_radiobutton.set_active(1)

	self.obstructionEditor.notes_textbox.delete_text(0, -1)
	if (self.obstructionData[self.obstruction_displayed].notes != None):
		self.obstructionEditor.notes_textbox.insert_defaults(self.obstructionData[self.obstruction_displayed].notes)

#####################################################################

def read_obstruction_editor_data_into_memory(self):
	import gtk, string

	if (self.obstructionEditor.name_textentry.get_text() != ""):
		try:
			current_obstruction_number = string.atoi(self.obstructionEditor.number_textentry.get_text())
		except ValueError:
			self.display_dialog_box("Error", "Non-integer entered into current obstruction's number field")
		else:
			self.obstructionData[current_obstruction_number].number = current_obstruction_number
			self.obstructionData[current_obstruction_number].name = self.obstructionEditor.name_textentry.get_text()
			self.obstructionData[current_obstruction_number].aliases = self.obstructionEditor.aliases_textentry.get_text()
			self.obstructionData[current_obstruction_number].environment_graphic_url = self.obstructionEditor.environmental_graphic_textentry.get_text()
			if (self.obstructionData[current_obstruction_number].environment_graphic_url == ""):
				self.obstructionData[current_obstruction_number].environment_graphic_url = None
			self.obstructionData[current_obstruction_number].environment_graphic_Xpos = string.atoi( self.obstructionEditor.environmental_graphic_x_textentry.get_text() )
			self.obstructionData[current_obstruction_number].environment_graphic_Ypos = string.atoi( self.obstructionEditor.environmental_graphic_y_textentry.get_text() )
			self.obstructionData[current_obstruction_number].closeup_graphic_url = self.obstructionEditor.closeup_graphic_textentry.get_text()
			if (self.obstructionData[current_obstruction_number].closeup_graphic_url == ""):
				self.obstructionData[current_obstruction_number].closeup_graphic_url = None

			self.obstructionData[current_obstruction_number].description = gtk.GtkEntry.get_chars(self.obstructionEditor.description_textbox, 0, -1)

#			self.obstructionData[current_obstruction_number].type = self.obstructionEditor.type_textentry.get_text()

			self.obstructionData[current_obstruction_number].visible =  self.obstructionEditor.visible_true_radiobutton.get_active()

			self.obstructionData[current_obstruction_number].notes = gtk.GtkEntry.get_chars(self.obstructionEditor.notes_textbox, 0, -1)


	else:
		self.display_dialog_box("Error", "No name entered for this obstruction! obstruction will be skipped.")


#####################################################################

def create_new_obstruction(self):
	new_obstruction_number = len(self.obstructionData) + 1
	self.obstructionData[new_obstruction_number] = self.ObstructionObject()
	self.obstructionData[new_obstruction_number].number = len(self.obstructionData)

#####################################################################

def clear_current_obstruction(self):
	self.obstructionData[self.obstruction_displayed] = self.obstructionObject()
	self.obstructionData[self.obstruction_displayed].number = self.obstruction_displayed
	self.obstructionEditor.to_which_obstruction_textentry.set_text("")
	self.obstruction_obstruction_displayed = 0

#####################################################################

def on_obstruction_editor_new_button_clicked(self, obj):
	self.read_obstruction_editor_data_into_memory()
	self.create_new_obstruction()
	self.insert_data_into_obstruction_editor(len(self.obstructionData))

#####################################################################

def on_obstruction_editor_first_button_clicked(self, obj):
	if (self.obstruction_displayed != 1):
		self.read_obstruction_editor_data_into_memory()
		self.insert_data_into_obstruction_editor(1)
# 	else:
# 		self.display_dialog_box("Message", "Already in first obstruction")

#####################################################################

def on_obstruction_editor_previous_button_clicked(self, obj):
	if ((self.obstruction_displayed - 1) > 0):
		self.read_obstruction_editor_data_into_memory()
		self.insert_data_into_obstruction_editor(self.obstruction_displayed - 1)
# 	else:
# 		self.display_dialog_box("Message", "Already in first obstruction")

#####################################################################

def on_obstruction_editor_next_button_clicked(self, obj):
	if ((self.obstruction_displayed + 1) <= len(self.obstructionData)):
		self.read_obstruction_editor_data_into_memory()
		self.insert_data_into_obstruction_editor(self.obstruction_displayed + 1)
# 	else:
# 		self.display_dialog_box("Message", "Already in last obstruction")

#####################################################################

def on_obstruction_editor_last_button_clicked(self, obj):
	if (self.obstruction_displayed != len(self.obstructionData)):
		self.read_obstruction_editor_data_into_memory()
		self.insert_data_into_obstruction_editor(len(self.obstructionData))
# 	else:
# 		self.display_dialog_box("Message", "Already in last obstruction")

#####################################################################

def on_obstruction_editor_selection_textentry_activate(self, obj):
	import string
	new_obstruction_number_entry = self.obstructionEditor.obstruction_editor_selection_textentry.get_text()
	new_obstruction_number_entry = string.strip(new_obstruction_number_entry)
	try:
		new_obstruction_number = string.atoi(new_obstruction_number_entry)
	except ValueError:
		self.display_dialog_box("Error", "Bad value entered into obstruction Editor's goto field")
	else:
		if (self.obstructionData.has_key(new_obstruction_number)):
			self.read_obstruction_editor_data_into_memory()
			self.insert_data_into_obstruction_editor(new_obstruction_number)
		else:
			self.display_dialog_box("Error", "That obstruction number doesn't exist!")

#####################################################################

def on_obstruction_editor_clear_button_clicked(self, obj):
	self.clear_current_obstruction()
	self.insert_data_into_obstruction_editor(self.obstruction_displayed)


#####################################################################
# Widgets
#####################################################################
# obstruction_editor_selection_textentry
# number_textentry
# name_textentry
# aliases_textentry
# environmental_graphic_textentry
# environmental_graphic_x_textentry
# environmental_graphic_y_textentry
# closeup_graphic_textentry
# description_textbox
# type_textentry
# locations_textentry
# visible_true_radiobutton
# visible_false_radiobutton
# notes_textbox
#####################################################################
# Data Variables
#####################################################################
# self.number = -1
# self.name = ""
# self.aliases = ""
# self.environment_graphic_url = ""
# self.environment_graphic_Xpos = -1
# self.environment_graphic_Ypos = -1
# self.closeup_graphic_url = ""
# self.description = ""
# self.type = "" # set to "Antagonist" or "Obstacle"
# self.locations = ""
# self.visible = 0 # boolean
# self.notes = ""

# EOF