#!/usr/bin/env python
#!/usr/bin/env python2.2
#
# Cog Engine Application (SDL)
#
# Copyright Steven M. Castellotti (2002)
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Last Update: 2002.06.21
#
#####################################################################
# To Do List:
#####################################################################
#
# Critical Items:
# - None
#
# Non-Critial Items:
# - None
#
#####################################################################

from CogEngine_GtkSDL_Modules import CogEngine_GtkSDL

#####################################################################
# Classes
#####################################################################

class CogEngine_Application_SDL(CogEngine_GtkSDL):

	import os
	import sys

	import gtk
	import libglade

	import CogEngine_Utilities

	from CogObjects import *

	glade_filename = "CogEngine_Application_GtkSDL.glade"
	database_filename = ""
	data_loaded = 0
	debug_mode = 0


	#####################################################################

	def __init__(self):

		if (self.os.name == "nt") or (self.os.name == "dos"):
			self.operating_system = "windows"
		else:
			self.operating_system = self.os.name

		self.engine_initialized = 0
		self.Mouse_Xpos = 0
		self.Mouse_Ypos = 0

		# Create the main window and the widget store.
		if ( (len(self.sys.argv) == 2) and (self.os.path.isfile( self.sys.argv[1] )) ):
			(self.file_format_version_number, \
			self.gameInformation, self.playerInformation, \
			self.directionData, self.roomData, \
			self.itemData, self.obstructionData, self.verbData) \
			= self.CogEngine_Utilities.load_data_file(self.sys.argv[1])
			self.database_filename = self.sys.argv[1]
			
			if ('output_history' not in dir(self.gameInformation)):
				self.gameInformation.output_history = ""

			self.backup_default_game_settings()
			if (self.gameInformation.show_graphic_area):
				self.initialize_new_game()
			else:
				self.load_game_menu()

		else:
			self.load_game_menu()


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
		self.restore_default_game_settings()


	#####################################################################

	def on_open_activate(self, obj):
		# Opens a GTK File Selection Dialog
		dialog = self.readglade("open_fileselection")
		self.openFileselection = self.CogEngine_Utilities.WidgetStore(dialog)
		self.openFileselection.open_fileselection.show()


	#####################################################################

	def on_open_fileselection_ok_button_clicked(self, obj):
		filename = self.openFileselection.open_fileselection.get_filename()
		# The following section verifies that a valid file was selected
		if (self.os.path.isfile(filename)): # Check if entry is a file (will follow symlinks)
			if (self.os.access(filename, self.os.R_OK)):

				try:
					self.database_filename = filename
					(self.file_format_version_number, \
					self.gameInformation, self.playerInformation, \
					self.directionData, self.roomData, \
					self.itemData, self.obstructionData, self.verbData) \
					= self.CogEngine_Utilities.load_data_file(filename)
					self.data_loaded = 1
					
					if ('output_history' not in dir(self.gameInformation)):
						self.gameInformation.output_history = ""

					self.backup_default_game_settings()
					self.openFileselection.open_fileselection.destroy()
					self.on_continue_game_activate(None)

				except:
					self.display_dialog_box("Error", "Invalid Cog Engine File")

			else:
				self.display_dialog_box("Error", "The file is not readable!")

		else:
			self.display_dialog_box("Error", "This is not a file!")


	#####################################################################

	def on_open_fileselection_cancel_button_clicked(self, obj):
		self.openFileselection.open_fileselection.destroy()


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

			self.on_continue_game_activate(None)


   #####################################################################

	def on_save_as_activate(self, obj):
		# Opens a GTK File Selection Dialog
		
		if ('gameInformation' in dir(self)):
			dialog = self.readglade("save_as_fileselection")
			self.saveAsFileselection = self.CogEngine_Utilities.WidgetStore(dialog)
		else:
			self.display_dialog_box("Error", "Can't Save Game: No Game Loaded")


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
			self.display_dialog_box("File Saved", "File saved successfully.")


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
					self.display_dialog_box("File Saved", "File saved successfully.")

				else:
					self.display_dialog_box("Error", "Write permission not granted!")

		self.saveAsFileselection.save_as_fileselection.destroy()


	#####################################################################

	def on_save_as_fileselection_cancel_button_clicked(self, obj):
		self.saveAsFileselection.save_as_fileselection.destroy()


	#####################################################################

	def on_continue_game_activate(self, obj):

		if ('gameInformation' in dir(self)):
			self.mainwindow.CogEngine.hide()
			self.gtk.mainquit()
		else:
			self.display_dialog_box("Error", "Can't Continue Game: No Game Loaded")


	#####################################################################

	def on_quit(self, obj):
		self.exit_to_system()


	#####################################################################

	def on_about_activate(self, obj):
		# This handler opens the about dialog
		about = self.readglade("about")


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

	def load_game_menu(self):

		self.exit_cog_engine()

		if ('backup_gameInformation' in dir(self)):
			self.gameInformation.show_stats = self.backup_gameInformation.show_stats
			self.gameInformation.show_inventory = self.backup_gameInformation.show_inventory
			self.gameInformation.show_command_line = self.backup_gameInformation.show_command_line
			self.gameInformation.show_text_output_area = self.backup_gameInformation.show_text_output_area

		
		# Create the main window and the widget store.
		mainwindow = self.readglade("CogEngine")
		self.mainwindow = self.CogEngine_Utilities.WidgetStore(mainwindow)

		self.initialize_widgets()

		if ('gameInformation' in dir(self)):
			self.display_game_statistics()
			self.display_player_inventory()
			self.output_textbox.insert_defaults(self.gameInformation.output_history)

			if (self.gameInformation.show_graphic_area):
				self.gtk.mainloop()
				self.initialize_new_game()
			else:
				self.initialize_new_game()
				self.gtk.mainloop()
		else:
			self.on_open_activate(None)
			self.gtk.mainloop()
			self.initialize_new_game()


	#####################################################################

	def initialize_new_game(self):

		self.initialize_sound()

		if (self.gameInformation.text_to_speech_enabled):
			self.initialize_speech()
		else:
			self.text_to_speech_enabled = 0

		if (self.gameInformation.show_graphic_area):
			self.gameInformation.show_stats = 0
			self.gameInformation.show_inventory = 0
			self.gameInformation.show_command_line = 0
			self.gameInformation.show_text_output_area = 0

			self.initialize_sdl_graphic_area()
			self.initialize_graphic_display_panel()
			self.initialize_compass_panel()
			self.initialize_inventory_panel()
			self.initialize_current_room_objects_panel()
			self.initialize_mouse_pointer()


		self.initialize_engine()


		if (self.gameInformation.show_graphic_area):
			self.execute_pygame_loop = 1
			self.pygame_event_loop()
			self.pygame.quit()
			self.load_game_menu()


	#####################################################################

	def initialize_widgets(self):

		self.output_textbox = self.mainwindow.output_textbox
		self.output_textbox.set_word_wrap(self.gtk.TRUE)

		self.commandline_entry = self.mainwindow.commandline_entry

		self.statistics_textbox = self.mainwindow.statistics_textbox
		self.statistics_textbox.set_word_wrap(self.gtk.TRUE)

		self.inventory_textbox = self.mainwindow.inventory_textbox
		self.inventory_textbox.set_word_wrap(self.gtk.TRUE)


	#####################################################################

	def on_commandline_entry_activate(self, obj):

		# This method is called whenever a user hits enter after typing a command onto the command line

		if (self.gameInformation.show_graphic_area):
			self.display_dialog_box("Error", "Please Select \"Continue Game\" from the File Menu to Play")

		else:
			command = self.commandline_entry.get_text()
			self.commandline_entry.set_text("")
			self.parse_command_line(command)


	#####################################################################

	def exit_cog_engine(self):

		if ('mixer' in dir(self)):
			if (self.gameInformation.debug_mode):
				print "Uninitializing the mixer"

			if (self.mixer.get_busy() and self.mixer.music.get_busy()):
				self.mixer.music.stop()

			self.mixer.quit()


		if ('speech' in dir(self)):

			if (self.operating_system == "posix"):
				del (self.speech)

			if (self.operating_system == "windows"):
				if (self.gameInformation.debug_mode):
					print "Waiting for TTS to finish speaking"
				self.speech.stop()


#####################################################################

	def exit_to_system(self):

		self.sys.exit(0)
                 

#####################################################################
# Main
#####################################################################

if __name__ == '__main__':
	# Quick hack to supress warnings introduced in Python 2.2
	try:
		import warnings
		warnings.filterwarnings(action="ignore", message='.*import.*', category=SyntaxWarning)
	except:
		pass


	CogEngine_Application = CogEngine_Application_SDL()
