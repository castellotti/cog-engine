#####################################################################
#
# COG Engine Development Application - Verb Editor
#
# Copyright Steven M. Castellotti (2000)
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Last Update: 2001.02.01
#
#####################################################################

#####################################################################
# Functions
#####################################################################

def on_verb_editor_destroy(self, obj):
	# This function is called if a user closes a window directly,
	# instead of clicking off the toggle button
	self.widget.verb_togglebutton.set_active(0)

#####################################################################

def insert_data_into_verb_editor(self, current_verb_number):

	self.verb_displayed = current_verb_number

	if (len(self.verbData) is 0):
		self.verbData[self.verb_displayed] = self.VerbObject()
		self.verbData[self.verb_displayed].number = 1

	self.verbEditor.verb_editor_selection_textentry.set_text("%i" % self.verbData[self.verb_displayed].number)

	self.verbEditor.number_textentry.set_text("%i" % self.verbData[self.verb_displayed].number)
	self.verbEditor.name_textentry.set_text(self.verbData[self.verb_displayed].name)

	self.verbEditor.aliases_textbox.delete_text(0, -1)
	if (self.verbData[self.verb_displayed].aliases != None):
		self.verbEditor.aliases_textbox.insert_defaults(self.verbData[self.verb_displayed].aliases)

	self.verbEditor.notes_textbox.delete_text(0, -1)
	if (self.verbData[self.verb_displayed].notes != None):
		self.verbEditor.notes_textbox.insert_defaults(self.verbData[self.verb_displayed].notes)

#####################################################################

def read_verb_editor_data_into_memory(self):
	import gtk, string

	if (self.verbEditor.name_textentry.get_text() != ""):
		try:
			current_verb_number = string.atoi(self.verbEditor.number_textentry.get_text())
		except ValueError:
			print "Non-integer entered into current verb's number field"
		else:
			self.verbData[current_verb_number].number = current_verb_number
			self.verbData[current_verb_number].name = self.verbEditor.name_textentry.get_text()

			self.verbData[current_verb_number].aliases = gtk.GtkEntry.get_chars(self.verbEditor.aliases_textbox, 0, -1)
			self.verbData[current_verb_number].notes = gtk.GtkEntry.get_chars(self.verbEditor.notes_textbox, 0, -1)

	else:
		print "No name entered for this verb! verb will be skipped."


#####################################################################

def create_new_verb(self):
	new_verb_number = len(self.verbData) + 1
	self.verbData[new_verb_number] = self.verbObject()
	self.verbData[new_verb_number].number = len(self.verbData)

#####################################################################

def clear_current_verb(self):
	self.verbData[self.verb_displayed] = self.verbObject()
	self.verbData[self.verb_displayed].number = self.verb_displayed
	self.verbEditor.to_which_verb_textentry.set_text("")
	self.verb_verb_displayed = 0

#####################################################################

def on_verb_editor_new_button_clicked(self, obj):
	self.read_verb_editor_data_into_memory()
	self.create_new_verb()
	self.insert_data_into_verb_editor(len(self.verbData))

#####################################################################

def on_verb_editor_first_button_clicked(self, obj):
	if (self.verb_displayed != 1):
		self.read_verb_editor_data_into_memory()
		self.insert_data_into_verb_editor(1)
	else:
		print "Already in first verb"

#####################################################################

def on_verb_editor_previous_button_clicked(self, obj):
	if ((self.verb_displayed - 1) > 0):
		self.read_verb_editor_data_into_memory()
		self.insert_data_into_verb_editor(self.verb_displayed - 1)
	else:
		print "Already in first verb"

#####################################################################

def on_verb_editor_next_button_clicked(self, obj):
	if ((self.verb_displayed + 1) <= len(self.verbData)):
		self.read_verb_editor_data_into_memory()
		self.insert_data_into_verb_editor(self.verb_displayed + 1)
	else:
		print "Already in last verb"

#####################################################################

def on_verb_editor_last_button_clicked(self, obj):
	if (self.verb_displayed != len(self.verbData)):
		self.read_verb_editor_data_into_memory()
		self.insert_data_into_verb_editor(len(self.verbData))
	else:
		print "Already in last verb"

#####################################################################

def on_verb_editor_selection_textentry_activate(self, obj):
	import string
	new_verb_number_entry = self.verbEditor.verb_editor_selection_textentry.get_text()
	new_verb_number_entry = string.strip(new_verb_number_entry)
	try:
		new_verb_number = string.atoi(new_verb_number_entry)
	except ValueError:
		print "Bad value entered into verb Editor's goto field"
	else:
		if (self.verbData.has_key(new_verb_number)):
			self.read_verb_editor_data_into_memory()
			self.insert_data_into_verb_editor(new_verb_number)
		else:
			print "That verb number doesn't exist!"

#####################################################################

def on_verb_editor_clear_button_clicked(self, obj):
	self.clear_current_verb()
	self.insert_data_into_verb_editor(self.verb_displayed)


#####################################################################
# Widgets
#####################################################################
# verb_editor_selection_textentry
# number_textentry
# name_textentry
# aliases_textbox
# notes_textbox
#####################################################################
# Data Variables
#####################################################################
# self.number = -1
# self.name = ""
# self.aliases = ""
# self.events = {}
# self.total_events = 0
# self.notes = ""

# EOF