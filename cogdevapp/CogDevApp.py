#!/usr/bin/env python
#
# Cog Engine Development Application
#
# Copyright Steven M. Castellotti (2001, 2002)
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Last Update: 2002.06.15
#
#####################################################################
# To Do List:
#####################################################################
#
# Critical Items:
# - None
#
# Non-Critial Items:
# - Event Builder still calls graphic images "GraphicURL"
# - do URL entries need to be stripped of their "http://" and servername portions?
# - Handle current_room information for player editor (default to 1)
#
#####################################################################

from CogEngine_GtkSDL_Modules import CogEngine_GtkSDL

#####################################################################
# Classes
#####################################################################

class CogDevApp(CogEngine_GtkSDL):

	# Import windows gtk module if os is windows
	import os
	import sys
	if (os.name == "nt") or (os.name == "dos"):
		sys.path.append('win32')

	import gtk
	import libglade

	# Import handler functionality from modules
	import CogEngine_Utilities
	from CogObjects import *
	from CogDevApp_game_information_editor_modules import *
	from CogDevApp_game_information_editor_advanced_modules import *
	from CogDevApp_player_information_editor_modules import *
	from CogDevApp_direction_editor_modules import *
	from CogDevApp_room_editor_modules import *
	from CogDevApp_item_editor_modules import *
	from CogDevApp_obstruction_editor_modules import *
	from CogDevApp_verb_editor_modules import *
	from CogDevApp_event_editor_modules import *
	from CogDevApp_event_builder_modules import *

	glade_filename = "CogDevApp.glade"
	database_filename = ""
	data_loaded = 0
	debug_mode = 0
	version_number = "1.1.4"


	#####################################################################

	def __init__(self):
		# Create the main window and the widget store.
		self.mainwindow = self.readglade("CogDevApp")
		self.widget = self.CogEngine_Utilities.WidgetStore(self.mainwindow)
		if ( (len(self.sys.argv) == 2) and (self.os.path.isfile( self.sys.argv[1] )) ):
			(self.file_format_version_number, \
			self.gameInformation, self.playerInformation, \
			self.directionData, self.roomData, \
			self.itemData, self.obstructionData, self.verbData) \
			= self.CogEngine_Utilities.load_data_file(self.sys.argv[1])
			self.database_filename = self.sys.argv[1]
		else:
			self.on_new_file_activate(None)
		
		self.gtk.mainloop()


	#####################################################################
	
	def readglade(self, name, o=None):
		# Read in a Glade tree. Signals are attached to methods on the
		# supplied object o; if o is omitted, this object is used.
		if not o:
			o = self
		obj = self.libglade.GladeXML(self.glade_filename, name)
		obj.signal_autoconnect(self.CogEngine_Utilities.Callback(o))
		return obj


	#####################################################################

	# Begin Menubar Handler Fuctions

	def on_new_file_activate(self, obj):
		self.file_format_version_number = self.version_number
		self.gameInformation = self.GameInformationObject()
		self.playerInformation = self.PlayerInformationObject()
		self.directionData = {}
		self.roomData = {}
		self.roomData[1] = self.RoomObject()
		self.roomData[1].number = 1
		self.roomData[1].name = "Default Room"
		self.itemData = {}
		self.obstructionData = {}
		self.verbData = {}
		self.data_loaded = 1


	#####################################################################
	
	def on_open_activate(self, obj):
		# Opens a GTK File Selection Dialog
		dialog = self.readglade("open_fileselection")
		self.openFileselection = self.CogEngine_Utilities.WidgetStore(dialog)


	#####################################################################
	
	def on_save_activate(self, obj):
		if (self.database_filename == ""):
			self.on_save_as_activate(self)
		else:
			self.CogEngine_Utilities.save_data_file(self.database_filename, \
										self.file_format_version_number, \
										self.gameInformation, self.playerInformation, \
										self.directionData, self.roomData, \
										self.itemData, self.obstructionData, self.verbData)


	#####################################################################
	
	def on_save_as_activate(self, obj):
		# Opens a GTK File Selection Dialog
		dialog = self.readglade("save_as_fileselection")
		self.saveAsFileselection = self.CogEngine_Utilities.WidgetStore(dialog)


	#####################################################################

	def on_quit(self, obj):
		# Now I can do "self.widget.glade_widget_name" and it will automatically look up
		# "glade_widget_name" in the tree and return it to me (all cached so it's fast).
		# What's more, I can tell Glade to connect a button to the signal
		# "on_quit" and when I press it, the "on_quit()" method is
		# automatically invoked:
		
		import os

		if ('speech' in dir(self)) and (os.name == "posix"):
			del (self.speech)

		self.sys.exit(0)


	#####################################################################
	
	def on_about_activate(self, obj):
		# This handler opens the about dialog
		self.about = self.readglade("about")


	#####################################################################
	
	def destroy_about_box(self, obj):
		obj.destroy()


	#####################################################################
	
	def display_dialog_box(self, title, message):

		# This method creates a dialog box with the title and message passed to it

		# First we clean up the message
		message = "\n     %s     \n" % message

		# Then we create the label and the OK Button
		dialog_box_label = self.gtk.GtkLabel()
		dialog_box_label.set_text(message)
		dialog_box_button = self.gtk.GtkButton("OK")

		# Next we set up the dialog box
		dialog_box = self.gtk.GtkDialog()
		dialog_box.set_title(title)
		dialog_vbox = dialog_box.children()[0]
		dialog_vbox.pack_start(dialog_box_label)
		dialog_action_area = dialog_box.children()[0].children()[-1]
		dialog_action_area.add(dialog_box_button)

		# Now we configure the OK button to destroy the dialog box when clicked
		dialog_box_button.connect("clicked", self.destroy_dialog_box, dialog_box)

		# Finally we display the dialog box
		dialog_box.show_all()


	#####################################################################
	
	def destroy_dialog_box(self, obj, box):
		box.destroy()


	#####################################################################
	
	def on_open_fileselection_ok_button_clicked(self, obj):
		filename = self.openFileselection.open_fileselection.get_filename()
		# The following section verifies that a valid file was selected
		if (self.os.path.isfile(filename)): # Check if entry is a file (will follow symlinks)
			if (self.os.access(filename, self.os.R_OK)):
				self.database_filename = filename
				(self.file_format_version_number, \
				self.gameInformation, self.playerInformation, \
				self.directionData, self.roomData, \
				self.itemData, self.obstructionData, self.verbData) \
				= self.CogEngine_Utilities.load_data_file(filename)
				self.data_loaded = 1
				self.display_dialog_box("Open File", "File opened successfully")
			else:
				self.display_dialog_box("Error", "The file is not readable!")
		else:
			self.display_dialog_box("Error", "This is not a file!")
		self.openFileselection.open_fileselection.destroy()


	#####################################################################
	
	def on_open_fileselection_cancel_button_clicked(self, obj):
		self.openFileselection.open_fileselection.destroy()


	#####################################################################
	
	def on_save_as_fileselection_ok_button_clicked(self, obj):
		filename = self.saveAsFileselection.save_as_fileselection.get_filename()
		# The following section verifies that a valid file was entered
		if (self.os.access(filename, self.os.W_OK)):
				self.database_filename = filename
				self.CogEngine_Utilities.save_data_file(self.database_filename, \
											self.file_format_version_number, \
											self.gameInformation, self.playerInformation, \
											self.directionData, self.roomData, \
											self.itemData, self.obstructionData, self.verbData)
				self.display_dialog_box("File Saved", "File saved successfully")

		else:
			if (self.os.access(filename, self.os.F_OK)):
				self.display_dialog_box("Error", "The file is not writable!")
			else:
				# Check if directory is writable
				if (self.os.access(self.os.path.dirname(filename), self.os.W_OK)):
					self.database_filename = filename
					self.CogEngine_Utilities.save_data_file(self.database_filename, \
					                     self.file_format_version_number, \
												self.gameInformation, self.playerInformation, \
												self.directionData, self.roomData, \
												self.itemData, self.obstructionData, self.verbData)
					self.display_dialog_box("File Saved", "File saved successfully")
				else:
					self.display_dialog_box("Error", "Write permission not granted!")
		self.saveAsFileselection.save_as_fileselection.destroy()


	#####################################################################
	
	def on_save_as_fileselection_cancel_button_clicked(self, obj):
		self.saveAsFileselection.save_as_fileselection.destroy()


	#####################################################################

	# Begin togglebutton handler fuctions

	def on_game_information_togglebutton_toggled(self, obj):
		# this handler opens or closes the game information editor window,
		# depending on the status of the togglebutton
		# (when the togglebutton's activity is set to "1" then it was just depressed)
		if (self.widget.game_information_togglebutton.get_active()):
			try:
				self.widget.gameInformationEditor.show()
			except:
				editor = self.readglade("game_information_editor")
				self.gameInformationEditor = self.CogEngine_Utilities.WidgetStore(editor)
				self.insert_data_into_game_editor()
		else:
			if (self.gameInformationEditor.advanced_settings_togglebutton.get_active()):
				# If the advanced settings window is open force
				# it to read its settings into memory
				self.read_advanced_game_editor_data_into_memory()
				self.gameInformationEditorAdvancedSettings.game_information_editor_advanced_settings.hide()

			self.read_game_editor_data_into_memory()
			try:
				self.gameInformationEditor.game_information_editor.hide()
			except:
				# The window has already been destroyed
				pass


	#####################################################################
	
	def on_player_information_togglebutton_toggled(self, obj):
		# this handler opens or closes the player information editor window,
		# depending on the status of the togglebutton
		# (when the togglebutton's activity is set to "1" then it was just depressed)
		if (self.widget.player_information_togglebutton.get_active()):
			editor = self.readglade("player_information_editor")
			self.playerInformationEditor = self.CogEngine_Utilities.WidgetStore(editor)
			self.insert_data_into_player_editor()
		else:
			self.read_player_editor_data_into_memory()
			try:
				self.playerInformationEditor.player_information_editor.hide()
			except:
				# The window has already been destroyed
				pass


	#####################################################################

	def on_direction_togglebutton_toggled(self, obj):
		# this handler opens or closes the direction editor window,
		# depending on the status of the togglebutton
		# (when the togglebutton's activity is set to "1" then it was just depressed)
		if (self.widget.direction_togglebutton.get_active()):
			editor = self.readglade("direction_editor")
			self.directionEditor = self.CogEngine_Utilities.WidgetStore(editor)
			self.insert_data_into_direction_editor(1)
		else:
			self.read_direction_editor_data_into_memory()
			try:
				self.directionEditor.direction_editor.hide()
			except:
				# The window has already been destroyed
				pass


	#####################################################################

	def on_room_togglebutton_toggled(self, obj):
		# this handler opens or closes the room editor window,
		# depending on the status of the togglebutton
		# (when the togglebutton's activity is set to "1" then it was just depressed)
		if (self.widget.room_togglebutton.get_active()):
			editor = self.readglade("room_editor")
			self.roomEditor = self.CogEngine_Utilities.WidgetStore(editor)
			self.insert_data_into_room_editor(1)
		else:
			self.read_room_editor_data_into_memory()
			try:
				self.roomEditor.room_editor.hide()
			except:
				# The window has already been destroyed
				pass


	#####################################################################

	def on_item_togglebutton_toggled(self, obj):
		# this handler opens or closes the item editor window,
		# depending on the status of the togglebutton
		# (when the togglebutton's activity is set to "1" then it was just depressed)
		if (self.widget.item_togglebutton.get_active()):
			editor = self.readglade("item_editor")
			self.itemEditor = self.CogEngine_Utilities.WidgetStore(editor)
			self.insert_data_into_item_editor(1)
		else:
			self.read_item_editor_data_into_memory()
			try:
				self.itemEditor.item_editor.hide()
			except:
				# The window has already been destroyed
				pass


	#####################################################################

	def on_obstruction_togglebutton_toggled(self, obj):
		# this handler opens or closes the obstruction editor window,
		# depending on the status of the togglebutton
		# (when the togglebutton's activity is set to "1" then it was just depressed)
		if (self.widget.obstruction_togglebutton.get_active()):
			editor = self.readglade("obstruction_editor")
			self.obstructionEditor = self.CogEngine_Utilities.WidgetStore(editor)
			self.insert_data_into_obstruction_editor(1)
		else:
			self.read_obstruction_editor_data_into_memory()
			try:
				self.obstructionEditor.obstruction_editor.hide()
			except:
				# The window has already been destroyed
				pass


	#####################################################################

	def on_verb_togglebutton_toggled(self, obj):
		# this handler opens or closes the verb editor window,
		# depending on the status of the togglebutton
		# (when the togglebutton's activity is set to "1" then it was just depressed)
		if (self.widget.verb_togglebutton.get_active() == 1):
			editor = self.readglade("verb_editor")
			self.verbEditor = self.CogEngine_Utilities.WidgetStore(editor)
			self.insert_data_into_verb_editor(1)
		else:
			self.read_verb_editor_data_into_memory()
			try:
				self.verbEditor.verb_editor.hide()
			except:
				# The window has already been destroyed
				pass


	#####################################################################

	def on_event_togglebutton_toggled(self, obj):
		# this handler opens or closes the event editor window,
		# depending on the status of the togglebutton
		# (when the togglebutton's activity is set to "1" then it was just depressed)
		if (self.widget.event_togglebutton.get_active() == 1):
			editor = self.readglade("event_editor")
			self.eventEditor = self.CogEngine_Utilities.WidgetStore(editor)
			self.setup_default_data_in_event_builder()
			self.insert_data_into_event_editor()
		else:
			self.read_event_editor_data_into_memory()
			try:
				self.eventEditor.event_editor.hide()
			except:
				# The window has already been destroyed
				pass


	#####################################################################

	# CogEngine Game Routines

	def on_play_togglebutton_toggled(self, obj):
		# this handler launches or closes a running game,
		# depending on the status of the togglebutton
		# (when the togglebutton's activity is set to "1" then it was just depressed)
		if (self.widget.play_togglebutton.get_active() == 1):
			engine = self.readglade("CogEngine")
			self.cogengine = self.CogEngine_Utilities.WidgetStore(engine)

			self.backup_default_game_settings()
			self.initialize_new_game()
		else:
			try:
				self.cogengine.CogEngine.hide()
			except:
				# The window has already been destroyed
				pass
			try:
				self.pygame.quit()
			except:
				# The window has already been destroyed
				pass


	#####################################################################

	def initialize_widgets(self):

		self.output_textbox = self.cogengine.output_textbox
		self.commandline_entry = self.cogengine.commandline_entry
		self.statistics_textbox = self.cogengine.statistics_textbox
		self.inventory_textbox = self.cogengine.inventory_textbox

	#####################################################################

	def on_commandline_entry_activate(self, obj):

		# This method is called whenever a user hits enter after typing a command onto the command line

		command = self.commandline_entry.get_text()
		self.commandline_entry.set_text("")
		self.parse_command_line(command)


	#####################################################################

	def initialize_new_game(self):

		self.initialize_widgets()
		self.initialize_sdl_graphic_area()
		self.initialize_compass_panel()
		self.initialize_inventory_panel()
		self.initialize_current_room_objects_panel()
		if (self.gameInformation.text_to_speech_enabled):
			self.initialize_speech()
		else:
			self.text_to_speech_enabled = 0
		self.initialize_engine()


	#####################################################################

	def exit_cog_engine(self):

		import os

		if ('speech' in dir(self)) and (os.name == "posix"):
			del (self.speech)

		self.widget.play_togglebutton.set_active(0)


#####################################################################
# Main
#####################################################################

if __name__ == '__main__':
	# Quick hack to supress warnings introduced in Python 2.1
	try:
		import warnings
		warnings.filterwarnings(action="ignore", message='.*import.*', category=SyntaxWarning)
	except:
		pass


	CogDevApp()

