#####################################################################
#
# COG Engine Development Application - Direction Editor
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

def on_direction_editor_destroy(self, obj):
	# This function is called if a user closes a window directly,
	# instead of clicking off the toggle button
	self.widget.direction_togglebutton.set_active(0)

#####################################################################

def insert_data_into_direction_editor(self, current_direction_number):

	self.direction_displayed = current_direction_number

	if (len(self.directionData) is 0):
		self.directionData[self.direction_displayed] = self.DirectionInformationObject()
		self.directionData[self.direction_displayed].number = 1

	self.directionEditor.direction_editor_selection_textentry.set_text("%i" % self.directionData[self.direction_displayed].number)
	self.directionEditor.number_textentry.set_text("%i" % self.directionData[self.direction_displayed].number)
	self.directionEditor.name_textentry.set_text(self.directionData[self.direction_displayed].name)
	self.directionEditor.abbreviation_textentry.set_text(self.directionData[self.direction_displayed].abbreviation)
	self.directionEditor.available_compass_graphic_textentry.set_text(self.directionData[self.direction_displayed].compass_graphic_available_url)
	self.directionEditor.unavailable_compass_graphic_textentry.set_text(self.directionData[self.direction_displayed].compass_graphic_unavailable_url)
	self.directionEditor.special_compass_graphic_textentry.set_text(self.directionData[self.direction_displayed].compass_graphic_special_url)

#####################################################################

def read_direction_editor_data_into_memory(self):
	import string

	if (self.directionEditor.name_textentry.get_text() != ""):
		try:
			current_direction_number = string.atoi(self.directionEditor.number_textentry.get_text())
		except ValueError:
			self.display_dialog_box("Error", "Non-integer entered into current direction's number field")
		else:
			self.directionData[current_direction_number].number = current_direction_number
			self.directionData[current_direction_number].name = self.directionEditor.name_textentry.get_text()
			self.directionData[current_direction_number].abbreviation = self.directionEditor.abbreviation_textentry.get_text()
			self.directionData[current_direction_number].compass_graphic_available_url = self.directionEditor.available_compass_graphic_textentry.get_text()
			self.directionData[current_direction_number].compass_graphic_unavailable_url = self.directionEditor.unavailable_compass_graphic_textentry.get_text()
			self.directionData[current_direction_number].compass_graphic_special_url = self.directionEditor.special_compass_graphic_textentry.get_text()
	else:
		self.display_dialog_box("Warning", "No name entered for this direction! Direction will be skipped.")

#####################################################################

def create_new_direction(self):
	new_direction_number = len(self.directionData) + 1
	self.directionData[new_direction_number] = self.DirectionInformationObject()
	self.directionData[new_direction_number].number = len(self.directionData)

#####################################################################

def clear_current_direction(self):
	self.directionData[self.direction_displayed] = self.directionObject()
	self.directionData[self.direction_displayed].number = self.direction_displayed
	self.directionEditor.to_which_direction_textentry.set_text("")
	self.direction_direction_displayed = 0

#####################################################################

def on_direction_editor_new_button_clicked(self, obj):
	self.read_direction_editor_data_into_memory()
	self.create_new_direction()
	self.insert_data_into_direction_editor(len(self.directionData))

#####################################################################

def on_direction_editor_first_button_clicked(self, obj):
	if (self.direction_displayed != 1):
		self.read_direction_editor_data_into_memory()
		self.insert_data_into_direction_editor(1)
# 	else:
# 		self.display_dialog_box("Message", "Already in first direction")

#####################################################################

def on_direction_editor_previous_button_clicked(self, obj):
	if ((self.direction_displayed - 1) > 0):
		self.read_direction_editor_data_into_memory()
		self.insert_data_into_direction_editor(self.direction_displayed - 1)
# 	else:
# 		self.display_dialog_box("Message", "Already in first direction")

#####################################################################

def on_direction_editor_next_button_clicked(self, obj):
	if ((self.direction_displayed + 1) <= len(self.directionData)):
		self.read_direction_editor_data_into_memory()
		self.insert_data_into_direction_editor(self.direction_displayed + 1)
# 	else:
# 		self.display_dialog_box("Message", "Already in last direction")

#####################################################################

def on_direction_editor_last_button_clicked(self, obj):
	if (self.direction_displayed != len(self.directionData)):
		self.read_direction_editor_data_into_memory()
		self.insert_data_into_direction_editor(len(self.directionData))
# 	else:
# 		self.display_dialog_box("Message", "Already in last direction")

#####################################################################

def on_direction_editor_selection_textentry_activate(self, obj):
	import string
	new_direction_number_entry = self.directionEditor.direction_editor_selection_textentry.get_text()
	new_direction_number_entry = string.strip(new_direction_number_entry)
	try:
		new_direction_number = string.atoi(new_direction_number_entry)
	except ValueError:
		self.display_dialog_box("Error", "Bad value entered into direction Editor's goto field")
	else:
		if (self.directionData.has_key(new_direction_number)):
			self.read_direction_editor_data_into_memory()
			self.insert_data_into_direction_editor(new_direction_number)
		else:
			self.display_dialog_box("Error", "That direction number doesn't exist!")

#####################################################################

def on_direction_editor_clear_button_clicked(self, obj):
	self.clear_current_direction()
	self.insert_data_into_direction_editor(self.direction_displayed)


#####################################################################
# Widgets
#####################################################################
# direction_editor_selection_textentry
# number_textentry
# name_textentry
# abbreviation_textentry
# available_compass_graphic_textentry
# unavailable_compass_graphic_textentry
# special_compass_graphic_textentry
#####################################################################
# Data Variables
#####################################################################
# self.number = -1
# self.name = ""
# self.abbreviation = ""
# self.compass_graphic_available_url = ""
# self.compass_graphic_unavailable_url = ""
# self.compass_graphic_special_url = ""


# EOF