#!/usr/bin/env python2.1
#!/usr/bin/env python2.2
#!/usr/bin/env python
#
# Cog Engine Application (GtkSDL)
#
# Copyright Steven M. Castellotti (2002)
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
# - None
#
#####################################################################


#####################################################################
# Classes
#####################################################################

class CogEngine_Application_GtkSDL:

	# Import windows gtk module if os is windows
	import os
	import sys
	if (os.name == "nt") or (os.name == "dos"):
		sys.path.append('win32')

	import gtk
	import libglade

	import CogEngine_Utilities

	from CogObjects import *
	from CogEngine_Modules import *
	from CogEngine_GtkSDL_Modules import *


	glade_filename = "CogEngine_Application_GtkSDL.glade"
	database_filename = ""
	data_loaded = 0
	debug_mode = 0

	def __init__(self):
		# Create the main window and the widget store.
		self.mainwindow = self.readglade("CogEngine")
		self.widget = self.CogEngine_Utilities.WidgetStore(self.mainwindow)
		if ( (len(self.sys.argv) == 2) and (self.os.path.isfile( self.sys.argv[1] )) ):
			(self.gameInformation, self.playerInformation, \
			self.directionData, self.roomData, \
			self.itemData, self.obstructionData, self.verbData) \
			= self.CogEngine_Utilities.load_data_file(self.sys.argv[1])
			self.database_filename = self.sys.argv[1]
			self.backup_default_game_settings()
			self.initialize_new_game()
		else:
			self.on_open_activate(None)

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
		self.restore_default_game_settings()

		
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
		self.sys.exit(0)


	def on_about_activate(self, obj):
		# This handler opens the about dialog
		about = self.readglade("about")


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
				self.backup_default_game_settings()
				self.initialize_new_game()
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

	def initialize_new_game(self):

		self.initialize_widgets()
		self.initialize_sdl_graphic_area()
		self.initialize_engine()


#####################################################################

	def initialize_widgets(self):

		self.output_textbox = self.widget.output_textbox
		self.commandline_entry = self.widget.commandline_entry
		self.statistics_textbox = self.widget.statistics_textbox
		self.inventory_textbox = self.widget.inventory_textbox


#####################################################################

	def exit_cog_engine(self):

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



	CogEngine_Application_GtkSDL()
