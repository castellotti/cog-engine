#####################################################################
#
# COG Engine Development Application - Game Information Editor
#
# Copyright Steven M. Castellotti (2000)
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Last Update: 2001.01.21
#
#####################################################################

#####################################################################
# Classes
#####################################################################

# class GameInformationEditorReader:
#
# 	import CogDevApp
# 	import libglade
# 	import utils
#
# 	def __init__(self):
# 		editor = self.readglade("game_information_editor")
# 		self.widget = utils.WidgetStore(editor)
#
# 	def readglade(self, name, o=None):
# 		# Read in a Glade tree. Signals are attached to methods on the
# 		# supplied object o; if o is omitted, this object is used.
# 		if not o:
# 			o = self
# 		obj = libglade.GladeXML("CogDevApp.glade", name)
# 		obj.signal_autoconnect(utils.Callback(o))
# 		return obj

#####################################################################
# Functions
#####################################################################

def on_game_information_editor_destroy(self, obj):
	# This function is called if a user closes a window directly,
	# instead of clicking off the toggle button
	self.widget.game_information_togglebutton.set_active(0)

#####################################################################

def insert_data_into_game_editor(self):
	# This function is called when a user opens the game editor. The fuction
	# configures the window's widgets according to the data stored in memory.
	self.gameInformationEditor.game_title_textentry.set_text(self.gameInformation.game_title)
	self.gameInformationEditor.version_number_textentry.set_text(self.gameInformation.version_number)
	self.gameInformationEditor.game_designer_textentry.set_text(self.gameInformation.game_designer)
	self.gameInformationEditor.game_designer_email_address_textentry.set_text(self.gameInformation.game_designer_email_address)
	self.gameInformationEditor.last_update_textentry.set_text(self.gameInformation.last_update)
	self.gameInformationEditor.game_url_textentry.set_text(self.gameInformation.game_url)
	self.gameInformationEditor.database_url_textentry.set_text(self.gameInformation.database_url)
	self.gameInformationEditor.image_loading_graphic_textentry.set_text(self.gameInformation.image_loading_graphic_url)
	self.gameInformationEditor.introduction_graphic_textentry.set_text(self.gameInformation.introduction_graphic_url)

	self.gameInformationEditor.introduction_text_textbox.delete_text(0, -1)
	self.gameInformationEditor.introduction_text_textbox.insert_defaults(self.gameInformation.introduction_text)

 	if (self.gameInformation.debug_mode):
 		self.gameInformationEditor.debug_mode_true_radiobutton.set_active(1)
 	else:
 		self.gameInformationEditor.debug_mode_false_radiobutton.set_active(1)

	self.gameInformationEditor.show_statistical_display_checkbutton.set_active(self.gameInformation.show_stats)
	self.gameInformationEditor.show_inventory_checkbutton.set_active(self.gameInformation.show_inventory)
	self.gameInformationEditor.show_command_line_checkbutton.set_active(self.gameInformation.show_command_line)
	self.gameInformationEditor.show_compass_checkbutton.set_active(self.gameInformation.show_compass)
	self.gameInformationEditor.center_button_indicates_items_checkbutton.set_active(self.gameInformation.center_button_indicates_items)
	self.gameInformationEditor.load_all_compass_images_checkbutton.set_active(self.gameInformation.load_all_compass_images)
	self.gameInformationEditor.game_information_notes_textbox.delete_text(0, -1)
	self.gameInformationEditor.game_information_notes_textbox.insert_defaults(self.gameInformation.game_information_notes)

#####################################################################

def read_game_editor_data_into_memory(self):
	# This function is called whenever the game editor is closed. The function
	# reads in the state of the various widgets and stores them into memory
	import gtk
	self.gameInformation.game_title = self.gameInformationEditor.game_title_textentry.get_text()
	self.gameInformation.version_number = self.gameInformationEditor.version_number_textentry.get_text()
	self.gameInformation.game_designer = self.gameInformationEditor.game_designer_textentry.get_text()
	self.gameInformation.game_designer_email_address = self.gameInformationEditor.game_designer_email_address_textentry.get_text()
	self.gameInformation.last_update = self.gameInformationEditor.last_update_textentry.get_text()
	self.gameInformation.game_url = self.gameInformationEditor.game_url_textentry.get_text()
	self.gameInformation.database_url = self.gameInformationEditor.database_url_textentry.get_text()
	self.gameInformation.image_loading_graphic_url = self.gameInformationEditor.image_loading_graphic_textentry.get_text()
	self.gameInformation.introduction_graphic_url = self.gameInformationEditor.introduction_graphic_textentry.get_text()

	self.gameInformation.introduction_text = gtk.GtkEntry.get_chars(self.gameInformationEditor.introduction_text_textbox, 0, -1)

	self.gameInformation.debug_mode =  self.gameInformationEditor.debug_mode_true_radiobutton.get_active()

	self.gameInformation.show_stats = self.gameInformationEditor.show_statistical_display_checkbutton.get_active()
	self.gameInformation.show_inventory = self.gameInformationEditor.show_inventory_checkbutton.get_active()
	self.gameInformation.show_command_line = self.gameInformationEditor.show_command_line_checkbutton.get_active()
	self.gameInformation.show_compass = self.gameInformationEditor.show_compass_checkbutton.get_active()
	self.gameInformation.center_button_indicates_items = self.gameInformationEditor.center_button_indicates_items_checkbutton.get_active()
	self.gameInformation.load_all_compass_images = self.gameInformationEditor.load_all_compass_images_checkbutton.get_active()

	self.gameInformation.game_information_notes = gtk.GtkEntry.get_chars(self.gameInformationEditor.game_information_notes_textbox, 0, -1)


# EOF