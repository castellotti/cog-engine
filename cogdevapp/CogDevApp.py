#!/usr/bin/env python
#
# COG Engine Development Application
#
# Copyright Steven M. Castellotti (2001, 2002)
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Last Update: 2002.04.29
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

# Import windows gtk module if os is windows
import os
if (os.name == "nt") or (os.name == "dos"):
	import sys
	sys.path.append('win32')


import gtk
import libglade
import utils
#import gnome.ui
#import GDK
#import gtkhtml

# Quick hack to supress warnings introduced in Python 2.1
try:
	import warnings
	warnings.filterwarnings(action="ignore", message='.*import.*', category=SyntaxWarning)
except:
	pass


#####################################################################
# Classes
#####################################################################

class CogDevApp:

	gladefilename = "CogDevApp.glade"
	database_filename = ""
	data_loaded = 0
	debug_mode = 0
# 	current_direction = 1
# 	current_room = 1
# 	current_item = 1
# 	current_obstruction = 1
# 	current_verb = 1
# 	current_event = 1

	# Import handler functionality from modules
	from CogObjects import *
	from game_information_editor_modules import *
	from player_information_editor_modules import *
	from direction_editor_modules import *
	from room_editor_modules import *
	from item_editor_modules import *
	from obstruction_editor_modules import *
	from verb_editor_modules import *
	from event_editor_modules import *
	from event_builder_modules import *

	def __init__(self):
		import sys, os
		# Create the main window and the widget store.
		self.mainwindow = self.readglade("CogDevApp")
		self.widget = utils.WidgetStore(self.mainwindow)
		if ( (len(sys.argv) == 2) and (os.path.isfile( sys.argv[1] )) ):
			(self.gameInformation, self.playerInformation, \
			self.directionData, self.roomData, \
			self.itemData, self.obstructionData, self.verbData) \
			= utils.load_data_file(sys.argv[1])
			self.database_filename = sys.argv[1]
		else:
			self.on_new_file_activate(None)
		gtk.mainloop()


	def readglade(self, name, o=None):
		# Read in a Glade tree. Signals are attached to methods on the
		# supplied object o; if o is omitted, this object is used.
		if not o:
			o = self
		obj = libglade.GladeXML(self.gladefilename, name)
		obj.signal_autoconnect(utils.Callback(o))
		return obj


#####################################################################
	# Begin Menubar Handler Fuctions

	def on_new_file_activate(self, obj):
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
		# self.verbData[1] = self.VerbObject()
		# self.verbData[1].number = 1
		# self.verbData[1].name = "Get"
		# self.verbData[2] = self.VerbObject()
		# self.verbData[2].number = 2
		# self.verbData[2].name = "Drop"
		self.data_loaded = 1


	def on_open_activate(self, obj):
		# Opens a GTK File Selection Dialog
		dialog = self.readglade("open_fileselection")
		self.openFileselection = utils.WidgetStore(dialog)


	def on_save_activate(self, obj):
		if (self.database_filename == ""):
			self.on_save_as_activate(self)
		else:
			utils.save_data_file(self.database_filename, \
										self.gameInformation, self.playerInformation, \
										self.directionData, self.roomData, \
										self.itemData, self.obstructionData, self.verbData)


	def on_save_as_activate(self, obj):
		# Opens a GTK File Selection Dialog
		dialog = self.readglade("save_as_fileselection")
		self.saveAsFileselection = utils.WidgetStore(dialog)


	def on_quit(self, obj):
		# Now I can do "self.widget.glade_widget_name" and it will automatically look up
		# "glade_widget_name" in the tree and return it to me (all cached so it's fast).
		# What's more, I can tell Glade to connect a button to the signal
		# "on_quit" and when I press it, the "on_quit()" method is
		# automatically invoked:
		import sys
		sys.exit(0)


	def on_about_activate(self, obj):
		# This handler opens the about dialog
		self.about = self.readglade("about")

#		The following statements will create a Gnome About Box
# 		application_title = "Cog Development Application"
# 		application_version = "0.90"
# 		application_copyright = "Copyright (2001)"
# 		application_authors = []
# 		application_authors.append("Steven M. Castellotti (SteveC@innocent.com)")
# 		application_comments = "The Cog Development Application creates and modifies game databases "
# 		application_comments = application_comments +  "used by the COG Engine. For more information, please visit:\n"
# 		application_comments = application_comments +  "http://cogengine.sourceforge.net"
# 		application_logo = "icon-cycon.jpg"
#
# 		about_box = gnome.ui.GnomeAbout(application_title, application_version, application_copyright, \
# 			application_authors, application_comments, application_logo)
# 		about_box.show(self)


	def destroy_about_box(self, obj):
		obj.destroy()


	def display_dialog_box(self, title, message):

		# This method creates a dialog box with the title and message passed to it

		# First we clean up the message
		message = "\n     %s     \n" % message

		# Then we create the label and the OK Button
		dialog_box_label = gtk.GtkLabel()
		dialog_box_label.set_text(message)
		dialog_box_button = gtk.GtkButton("OK")

		# Next we set up the dialog box
		dialog_box = gtk.GtkDialog()
		dialog_box.set_title(title)
		dialog_vbox = dialog_box.children()[0]
		dialog_vbox.pack_start(dialog_box_label)
		dialog_action_area = dialog_box.children()[0].children()[-1]
		dialog_action_area.add(dialog_box_button)

		# Now we configure the OK button to destroy the dialog box when clicked
		dialog_box_button.connect("clicked", self.destroy_dialog_box, dialog_box)

		# Finally we display the dialog box
		dialog_box.show_all()


	def destroy_dialog_box(self, obj, box):
		box.destroy()


	def on_open_fileselection_ok_button_clicked(self, obj):
		filename = self.openFileselection.open_fileselection.get_filename()
		# The following section verifies that a valid file was selected
		import os
		if (os.path.isfile(filename)): # Check if entry is a file (will follow symlinks)
			if (os.access(filename, os.R_OK)):
				self.database_filename = filename
				(self.gameInformation, self.playerInformation, \
				self.directionData, self.roomData, \
				self.itemData, self.obstructionData, self.verbData) \
				= utils.load_data_file(filename)
				self.data_loaded = 1
				self.display_dialog_box("Open File", "File opened successfully")
			else:
				self.display_dialog_box("Error", "The file is not readable!")
		else:
			self.display_dialog_box("Error", "This is not a file!")
		self.openFileselection.open_fileselection.destroy()


	def on_open_fileselection_cancel_button_clicked(self, obj):
		self.openFileselection.open_fileselection.destroy()


	def on_save_as_fileselection_ok_button_clicked(self, obj):
		filename = self.saveAsFileselection.save_as_fileselection.get_filename()
		# The following section verifies that a valid file was entered
		import os
		if (os.access(filename, os.W_OK)):
				self.database_filename = filename
				utils.save_data_file(self.database_filename, \
											self.gameInformation, self.playerInformation, \
											self.directionData, self.roomData, \
											self.itemData, self.obstructionData, self.verbData)
				self.display_dialog_box("File Saved", "File saved successfully")

		else:
			if (os.access(filename, os.F_OK)):
				self.display_dialog_box("Error", "The file is not writable!")
			else:
				# Check if directory is writable
				if (os.access(os.path.dirname(filename), os.W_OK)):
					self.database_filename = filename
					utils.save_data_file(self.database_filename, \
												self.gameInformation, self.playerInformation, \
												self.directionData, self.roomData, \
												self.itemData, self.obstructionData, self.verbData)
					self.display_dialog_box("File Saved", "File saved successfully")
				else:
					self.display_dialog_box("Error", "Write permission not granted!")
		self.saveAsFileselection.save_as_fileselection.destroy()


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
				self.gameInformationEditor = utils.WidgetStore(editor)
				self.insert_data_into_game_editor()
		else:
			self.read_game_editor_data_into_memory()
			self.gameInformationEditor.game_information_editor.hide()

	def on_player_information_togglebutton_toggled(self, obj):
		# this handler opens or closes the player information editor window,
		# depending on the status of the togglebutton
		# (when the togglebutton's activity is set to "1" then it was just depressed)
		if (self.widget.player_information_togglebutton.get_active()):
			editor = self.readglade("player_information_editor")
			self.playerInformationEditor = utils.WidgetStore(editor)
			self.insert_data_into_player_editor()
		else:
			self.read_player_editor_data_into_memory()
			self.playerInformationEditor.player_information_editor.hide()


	def on_direction_togglebutton_toggled(self, obj):
		# this handler opens or closes the direction editor window,
		# depending on the status of the togglebutton
		# (when the togglebutton's activity is set to "1" then it was just depressed)
		if (self.widget.direction_togglebutton.get_active()):
			editor = self.readglade("direction_editor")
			self.directionEditor = utils.WidgetStore(editor)
			self.insert_data_into_direction_editor(1)
		else:
			self.read_direction_editor_data_into_memory()
			self.directionEditor.direction_editor.hide()


	def on_room_togglebutton_toggled(self, obj):
		# this handler opens or closes the room editor window,
		# depending on the status of the togglebutton
		# (when the togglebutton's activity is set to "1" then it was just depressed)
		if (self.widget.room_togglebutton.get_active()):
			editor = self.readglade("room_editor")
			self.roomEditor = utils.WidgetStore(editor)
			self.insert_data_into_room_editor(1)
		else:
			self.read_room_editor_data_into_memory()
			self.roomEditor.room_editor.hide()


	def on_item_togglebutton_toggled(self, obj):
		# this handler opens or closes the item editor window,
		# depending on the status of the togglebutton
		# (when the togglebutton's activity is set to "1" then it was just depressed)
		if (self.widget.item_togglebutton.get_active()):
			editor = self.readglade("item_editor")
			self.itemEditor = utils.WidgetStore(editor)
			self.insert_data_into_item_editor(1)
		else:
			self.read_item_editor_data_into_memory()
			self.itemEditor.item_editor.hide()


	def on_obstruction_togglebutton_toggled(self, obj):
		# this handler opens or closes the obstruction editor window,
		# depending on the status of the togglebutton
		# (when the togglebutton's activity is set to "1" then it was just depressed)
		if (self.widget.obstruction_togglebutton.get_active()):
			editor = self.readglade("obstruction_editor")
			self.obstructionEditor = utils.WidgetStore(editor)
			self.insert_data_into_obstruction_editor(1)
		else:
			self.read_obstruction_editor_data_into_memory()
			self.obstructionEditor.obstruction_editor.hide()


	def on_verb_togglebutton_toggled(self, obj):
		# this handler opens or closes the verb editor window,
		# depending on the status of the togglebutton
		# (when the togglebutton's activity is set to "1" then it was just depressed)
		if (self.widget.verb_togglebutton.get_active() == 1):
			editor = self.readglade("verb_editor")
			self.verbEditor = utils.WidgetStore(editor)
			self.insert_data_into_verb_editor(1)
		else:
			self.read_verb_editor_data_into_memory()
			self.verbEditor.verb_editor.hide()


	def on_event_togglebutton_toggled(self, obj):
		# this handler opens or closes the event editor window,
		# depending on the status of the togglebutton
		# (when the togglebutton's activity is set to "1" then it was just depressed)
		if (self.widget.event_togglebutton.get_active() == 1):
			editor = self.readglade("event_editor")
			self.eventEditor = utils.WidgetStore(editor)
			self.setup_default_data_in_event_builder()
			self.insert_data_into_event_editor()
		else:
			self.read_event_editor_data_into_memory()
			self.eventEditor.event_editor.hide()


	def on_play_togglebutton_toggled(self, obj):
		# this handler launches or closes a running game,
		# depending on the status of the togglebutton
		# (when the togglebutton's activity is set to "1" then it was just depressed)
		if (self.widget.play_togglebutton.get_active() == 1):
			import CogEngine
			CogEngine.initialize_engine(self)
		else:
			import CogEngine
			CogEngine.hide_windows(self)


	def on_commandline_entry_activate(self, obj):
		import CogEngine
		command = self.io.commandline_entry.get_text()
		self.io.commandline_entry.set_text("")
		CogEngine.parse_command_line(self, command)


#####################################################################
# Main
#####################################################################

if __name__ == '__main__':
	CogDevApp()
