#!/usr/bin/env python2.1
#!/usr/bin/env python2.2
#!/usr/bin/env python
#
# Cog Engine Development Application
#
# Copyright Steven M. Castellotti (2001, 2002)
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Last Update: 2002.05.12
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


#####################################################################
# Classes
#####################################################################

class CogDevApp:

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
	from game_information_editor_modules import *
	from player_information_editor_modules import *
	from direction_editor_modules import *
	from room_editor_modules import *
	from item_editor_modules import *
	from obstruction_editor_modules import *
	from verb_editor_modules import *
	from event_editor_modules import *
	from event_builder_modules import *

	from CogEngine_Modules import *
	from CogEngine_GtkSDL_Modules import *

	glade_filename = "CogDevApp.glade"
	database_filename = ""
	data_loaded = 0
	debug_mode = 0


	def __init__(self):
		# Create the main window and the widget store.
		self.mainwindow = self.readglade("CogDevApp")
		self.widget = self.CogEngine_Utilities.WidgetStore(self.mainwindow)
		if ( (len(self.sys.argv) == 2) and (self.os.path.isfile( self.sys.argv[1] )) ):
			(self.gameInformation, self.playerInformation, \
			self.directionData, self.roomData, \
			self.itemData, self.obstructionData, self.verbData) \
			= self.CogEngine_Utilities.load_data_file(self.sys.argv[1])
			self.database_filename = self.sys.argv[1]
		else:
			self.on_new_file_activate(None)

		self.gtk.mainloop()


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
		self.openFileselection = self.CogEngine_Utilities.WidgetStore(dialog)


	def on_save_activate(self, obj):
		if (self.database_filename == ""):
			self.on_save_as_activate(self)
		else:
			self.CogEngine_Utilities.save_data_file(self.database_filename, \
										self.gameInformation, self.playerInformation, \
										self.directionData, self.roomData, \
										self.itemData, self.obstructionData, self.verbData)


	def on_save_as_activate(self, obj):
		# Opens a GTK File Selection Dialog
		dialog = self.readglade("save_as_fileselection")
		self.saveAsFileselection = self.CogEngine_Utilities.WidgetStore(dialog)


	def on_quit(self, obj):
		# Now I can do "self.widget.glade_widget_name" and it will automatically look up
		# "glade_widget_name" in the tree and return it to me (all cached so it's fast).
		# What's more, I can tell Glade to connect a button to the signal
		# "on_quit" and when I press it, the "on_quit()" method is
		# automatically invoked:
		self.sys.exit(0)


	def on_about_activate(self, obj):
		# This handler opens the about dialog
		self.about = self.readglade("about")


	def destroy_about_box(self, obj):
		obj.destroy()


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


	def destroy_dialog_box(self, obj, box):
		box.destroy()


	def on_open_fileselection_ok_button_clicked(self, obj):
		filename = self.openFileselection.open_fileselection.get_filename()
		# The following section verifies that a valid file was selected
		if (self.os.path.isfile(filename)): # Check if entry is a file (will follow symlinks)
			if (self.os.access(filename, self.os.R_OK)):
				self.database_filename = filename
				(self.gameInformation, self.playerInformation, \
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


	def on_open_fileselection_cancel_button_clicked(self, obj):
		self.openFileselection.open_fileselection.destroy()


	def on_save_as_fileselection_ok_button_clicked(self, obj):
		filename = self.saveAsFileselection.save_as_fileselection.get_filename()
		# The following section verifies that a valid file was entered
		if (self.os.access(filename, self.os.W_OK)):
				self.database_filename = filename
				self.CogEngine_Utilities.save_data_file(self.database_filename, \
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
				self.gameInformationEditor = self.CogEngine_Utilities.WidgetStore(editor)
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
			self.playerInformationEditor = self.CogEngine_Utilities.WidgetStore(editor)
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
			self.directionEditor = self.CogEngine_Utilities.WidgetStore(editor)
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
			self.roomEditor = self.CogEngine_Utilities.WidgetStore(editor)
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
			self.itemEditor = self.CogEngine_Utilities.WidgetStore(editor)
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
			self.obstructionEditor = self.CogEngine_Utilities.WidgetStore(editor)
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
			self.verbEditor = self.CogEngine_Utilities.WidgetStore(editor)
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
			self.eventEditor = self.CogEngine_Utilities.WidgetStore(editor)
			self.setup_default_data_in_event_builder()
			self.insert_data_into_event_editor()
		else:
			self.read_event_editor_data_into_memory()
			self.eventEditor.event_editor.hide()

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
			self.cogengine.CogEngine.hide()
			self.pygame.quit()


	def initialize_widgets(self):

		self.output_textbox = self.cogengine.output_textbox
		self.commandline_entry = self.cogengine.commandline_entry
		self.statistics_textbox = self.cogengine.statistics_textbox
		self.inventory_textbox = self.cogengine.inventory_textbox


	def initialize_new_game(self):

		self.initialize_widgets()
		self.initialize_sdl_graphic_area()
		self.initialize_engine()


	def exit_cog_engine(self):
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

