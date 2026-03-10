#####################################################################
#
# COG Engine Development Application - Event Editor
#
# Copyright Steven M. Castellotti (2001, 2002)
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Last Update: 2002.06.07
#
#####################################################################
# Notes
#####################################################################
# <Action> <Object> [<Preposition> <Object>]
# [ '('Requires [! | '('Not')'] <Requirement>')' ]
# { ( and | or ) '('Requires [! | '('Not')'] <Requirement>')' } ->
# 	<Effect> {and <Effect>};
#
#
#####################################################################


#####################################################################
# Functions
#####################################################################

def on_event_editor_destroy(self, obj):
	# This function is called if a user closes a window directly,
	# instead of clicking off the toggle button
	self.widget.event_togglebutton.set_active(0)

#####################################################################

def insert_data_into_event_editor(self):

	import string

	events_written = 0

	self.eventEditor.event_editor_textbox.set_wrap_mode(gtk.WRAP_WORD)
	self.eventEditor.event_editor_textbox.get_buffer().delete(self.eventEditor.event_editor_textbox.get_buffer().get_start_iter(), self.eventEditor.event_editor_textbox.get_buffer().get_end_iter())

	textbox_output = ''

	verb_list = self.verbData.keys()
	verb_list.sort()

	for verb in verb_list:
		event_list = self.verbData[verb].events.keys()
		event_list.sort()
		for event in event_list:

			textbox_output = self.format_event_text(self.verbData[verb].events[event])

			if( self.eventEditor.event_editor_display_reference_names_radiobutton.get_active() ):
				textbox_output = self.convert_reference_numbers_to_names(textbox_output)

			events_written = events_written + 1
			self.eventEditor.event_editor_textbox.get_buffer().insert_at_cursor(textbox_output)


#####################################################################

def read_event_editor_data_into_memory(self):

	import gtk, string

	# Clear out current events from memory
	for each in self.verbData.keys():
		self.verbData[each].events = {}

	# Now read in the buffer and split the events into a list
	event_buffer = gtk.GtkEditable.get_chars(self.eventEditor.event_editor_textbox, 0, -1)
	#event_buffer = self.clean_event_buffer(event_buffer)
 	event_list = string.split(event_buffer, ';')


	# Parse Events
	for each in event_list:

		index = event_list.index(each)

		event_list[index] = string.strip( event_list[index] )

		# Convert and name-based references to number-based references
		event_list[index] = self.convert_reference_names_to_numbers( event_list[index] )

		if ( string.find( event_list[index], '->' ) != -1 ):

			current_action = string.split( event_list[index], ' ' )[0]

			current_object = string.split( event_list[index], ' ' )[1]
			current_object = string.replace( current_object, '\n', '')
			current_object = string.strip( current_object )

			remainder_index = string.find( event_list[index], current_object ) + len(current_object)

			remainder = event_list[index][ remainder_index : string.find(event_list[index], '->') ]
			remainder = string.strip( remainder )

			if ( remainder == '' ):
				current_preposition = None
				current_object2 = None
				current_requirements = None
			elif ( remainder[0] == '(' ):
				current_preposition = None
				current_object2 = None
				current_requirements = remainder
				current_requirements = string.replace( current_requirements, '\n', '')
				current_requirements = string.strip( current_requirements )

			else:
				# parse preposition and object2, then check for requirements
				current_preposition = string.split( remainder, ' ' )[0]

				current_object2 = string.split( remainder, ' ' )[1]
				current_object2 = string.replace( current_object2, '\n', '')

				if ( len( string.split(remainder, ' ') ) > 1 ):
					current_requirements = string.split( remainder, ' ')[2:]
					current_requirements = string.join( current_requirements )
					current_requirements = string.strip( current_requirements )
					if ( current_requirements == '' ):
						current_requirements = None
					else:
						current_requirements = string.replace( current_requirements, '\n', '')

				else:
					current_requirements = None

			current_effects = string.split( event_list[index], '->' )[1]
			current_effects = string.strip(current_effects)
			current_effects = string.replace( current_effects, '\n', '')

			# Now that the data in the editor has been parsed into memory, we
			# can write all of the events into memory.

			for verb_index in self.verbData.keys():

				# create a list of the verb's name and all of it's aliases
				verb_name_list = []
				verb_name_list.append('%s' % self.verbData[verb_index].name)
				if ( self.verbData[verb_index].aliases != None ):
					verb_name_list = verb_name_list + string.split( self.verbData[verb_index].aliases, ',' )
				for verb_name in verb_name_list:
					verb_name_list[verb_name_list.index(verb_name)] = string.strip(verb_name)

				if ( current_action in verb_name_list ):
					event_index = len( self.verbData[verb_index].events ) + 1
					self.verbData[verb_index].events[event_index] = self.EventObject()
					self.verbData[verb_index].events[event_index].action = current_action
					self.verbData[verb_index].events[event_index].object = current_object
					self.verbData[verb_index].events[event_index].preposition = current_preposition
					self.verbData[verb_index].events[event_index].object2 = current_object2
					self.verbData[verb_index].events[event_index].requirements = current_requirements
					self.verbData[verb_index].events[event_index].effects = current_effects
					self.verbData[verb_index].events[event_index].has_been_executed = 0


#####################################################################

def clean_event_buffer(self, event_buffer):

	# For some reason, the gtk textbox widgets don't seem to behave
	# properly when their text is read into memory. This method will
	# take in a buffer, and parse out all of the duplicates it contains,
	# and return the corrected buffer.

	import string

	event_list = string.split(event_buffer, ';')

	# Event List is way too long!
	for each in event_list:
		index = event_list.index(each)
		current_event = event_list[index]
		del event_list[index]
		for inner_each in event_list:
			inner_index = event_list.index(inner_each)
			if ( event_list[inner_index] == current_event ):
				del event_list[inner_index]
		if (index == len(event_list)):
			event_list.append(current_event)
		else:
			event_list[index] = current_event

	event_buffer = string.join(event_list, ';')

	return(event_buffer)


#####################################################################

def on_event_builder_import_button_clicked(self, obj):
	import CogEngine_Utilities
	# Opens a GTK File Selection Dialog
	dialog = self.readglade("import_event_script_fileselection")
	self.importEventScriptFileselection = CogEngine_Utilities.WidgetStore(dialog)


#####################################################################

def on_import_event_script_fileselection_ok_button_clicked(self, obj):
	filename = self.importEventScriptFileselection.import_event_script_fileselection.get_filename()
	# The following section verifies that a valid file was selected
	import os
	if (os.path.isfile(filename)): # Check if entry is a file (will follow symlinks)
		if (os.access(filename, os.R_OK)):
			self.event_script_filename = filename

			input = open(filename, 'r')
			event_buffer = input.read()
			self.eventEditor.event_editor_textbox.get_buffer().delete(self.eventEditor.event_editor_textbox.get_buffer().get_start_iter(), self.eventEditor.event_editor_textbox.get_buffer().get_end_iter())
			self.eventEditor.event_editor_textbox.get_buffer().insert_at_cursor(event_buffer)

			self.display_dialog_box("Import File", "File imported successfully")

		else:
			self.display_dialog_box("Error", "The file is not readable!")
	else:
		self.display_dialog_box("Error", "This is not a file!")
	self.importEventScriptFileselection.import_event_script_fileselection.destroy()


#####################################################################

def on_import_event_script_fileselection_cancel_button_clicked(self, obj):
	self.importEventScriptFileselection.import_event_script_fileselection.destroy()


#####################################################################

def on_event_builder_export_button_clicked(self, obj):
	import CogEngine_Utilities
	# Opens a GTK File Selection Dialog
	dialog = self.readglade("export_event_script_fileselection")
	self.exportEventScriptFileselection = CogEngine_Utilities.WidgetStore(dialog)


#####################################################################

def on_export_event_script_fileselection_ok_button_clicked(self, obj):
	filename = self.exportEventScriptFileselection.export_event_script_fileselection.get_filename()
	# The following section verifies that a valid file was entered
	import os, gtk
	if (os.access(filename, os.W_OK)):
			self.event_script_filename = filename

			output = open(filename, 'w')
			event_buffer = gtk.GtkEditable.get_chars(self.eventEditor.event_editor_textbox, 0, -1)
			#event_buffer = self.clean_event_buffer(event_buffer)
			output.write(event_buffer)
			self.display_dialog_box("Export File", "File exported successfully")
	else:
		if (os.access(filename, os.F_OK)):
			self.display_dialog_box("Error", "The file not writable!")
		else:
			# Check if directory is writable
			if (os.access(os.path.dirname(filename), os.W_OK)):
				self.database_filename = filename

				output = open(filename, 'w')
				event_buffer = gtk.GtkEditable.get_chars(self.eventEditor.event_editor_textbox, 0, -1)
				#event_buffer = self.clean_event_buffer(event_buffer)
				output.write(event_buffer)
				self.display_dialog_box("Export File", "File exported successfully")

			else:
				self.display_dialog_box("Error", "Write permission not granted!")
	self.exportEventScriptFileselection.export_event_script_fileselection.destroy()


#####################################################################

def on_export_event_script_fileselection_cancel_button_clicked(self, obj):
	self.exportEventScriptFileselection.export_event_script_fileselection.destroy()


#####################################################################

def on_event_builder_save_button_clicked(self, obj):
	self.read_event_editor_data_into_memory()


#####################################################################

def on_event_editor_display_reference_numbers_radiobutton_toggled(self, obj):
	# this function will get called whenever the numbers radiobutton is toggeled,
	# an event which occurs not only when it is click on, but when the names
	# radiobutton is clicked on (the numbers button is toggled off), so we
	# only want to respond when the radiobutton has been toggled on
	if (self.eventEditor.event_editor_display_reference_numbers_radiobutton.get_active()):
		self.read_event_editor_data_into_memory()
		self.insert_data_into_event_editor()


#####################################################################

def on_event_editor_display_reference_names_radiobutton_toggled(self, obj):
	# this function will get called whenever the names radiobutton is toggeled,
	# an event which occurs not only when it is click on, but when the numbers
	# radiobutton is clicked on (the names button is toggled off), so we
	# only want to respond when the radiobutton has been toggled on
	if (self.eventEditor.event_editor_display_reference_names_radiobutton.get_active()):
		self.read_event_editor_data_into_memory()
		self.insert_data_into_event_editor()


#####################################################################

def count_events_in_memory(self):

	total_events = 0

	for verb in self.verbData.keys():
		total_events = total_events + len(self.verbData[verb].events)

	return(total_events)


#####################################################################
# Widgets
#####################################################################
# event_builder_import_button
# event_builder_export_button
# event_editor_textbox

#####################################################################
# Data Variables
#####################################################################
# self.action = ""
# self.object = ""
# self.preposition = ""
# self.object2 = ""
# self.requirements = "" # don't forget to error-check this while parsing!
# self.effects = "" # don't forget to error-check this while parsing!
# self.has_been_executed = 0 # boolean # Not currently implemented. Aids in point calculations

# EOF
