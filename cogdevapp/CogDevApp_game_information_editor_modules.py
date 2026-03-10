#####################################################################
#
# COG Engine Development Application - Game Information Editor
#
# Copyright Steven M. Castellotti (2001, 2002)
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Last Update: 2002.06.07
#
#####################################################################


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
	self.gameInformationEditor.image_directory_textentry.set_text(self.gameInformation.image_directory)
	self.gameInformationEditor.audio_directory_textentry.set_text(self.gameInformation.audio_directory)
	self.gameInformationEditor.image_loading_graphic_textentry.set_text(self.gameInformation.image_loading_graphic_url)
	self.gameInformationEditor.introduction_graphic_textentry.set_text(self.gameInformation.introduction_graphic_url)

	self.gameInformationEditor.introduction_text_textbox.set_wrap_mode(gtk.WRAP_WORD)
	self.gameInformationEditor.introduction_text_textbox.get_buffer().delete(self.gameInformationEditor.introduction_text_textbox.get_buffer().get_start_iter(), self.gameInformationEditor.introduction_text_textbox.get_buffer().get_end_iter())
	self.gameInformationEditor.introduction_text_textbox.get_buffer().insert_at_cursor(self.gameInformation.introduction_text)

 	if (self.gameInformation.debug_mode):
 		self.gameInformationEditor.debug_mode_true_radiobutton.set_active(1)
 	else:
 		self.gameInformationEditor.debug_mode_false_radiobutton.set_active(1)

	self.gameInformationEditor.text_to_speech_enabled_checkbutton.set_active(self.gameInformation.text_to_speech_enabled)

	self.gameInformationEditor.game_information_notes_textbox.set_wrap_mode(gtk.WRAP_WORD)
	self.gameInformationEditor.game_information_notes_textbox.get_buffer().delete(self.gameInformationEditor.game_information_notes_textbox.get_buffer().get_start_iter(), self.gameInformationEditor.game_information_notes_textbox.get_buffer().get_end_iter())
	self.gameInformationEditor.game_information_notes_textbox.get_buffer().insert_at_cursor(self.gameInformation.game_information_notes)


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
	self.gameInformation.image_directory = self.gameInformationEditor.image_directory_textentry.get_text()

	if (self.gameInformation.image_directory != "") and (self.gameInformation.image_directory[0] == "/"):
		self.gameInformation.image_directory = self.gameInformation.image_directory[1:]

	self.gameInformation.audio_directory = self.gameInformationEditor.audio_directory_textentry.get_text()

	if (self.gameInformation.audio_directory != "") and (self.gameInformation.audio_directory[0] == "/"):
		self.gameInformation.audio_directory = self.gameInformation.audio_directory[1:]


	self.gameInformation.image_loading_graphic_url = self.gameInformationEditor.image_loading_graphic_textentry.get_text()
	self.gameInformation.introduction_graphic_url = self.gameInformationEditor.introduction_graphic_textentry.get_text()

	self.gameInformation.introduction_text = gtk.GtkEditable.get_chars(self.gameInformationEditor.introduction_text_textbox, 0, -1)

	self.gameInformation.debug_mode =  self.gameInformationEditor.debug_mode_true_radiobutton.get_active()

	self.gameInformation.text_to_speech_enabled = self.gameInformationEditor.text_to_speech_enabled_checkbutton.get_active()	

	self.gameInformation.game_information_notes = gtk.GtkEditable.get_chars(self.gameInformationEditor.game_information_notes_textbox, 0, -1)


#####################################################################

def on_advanced_settings_togglebutton_toggled(self, obj):

	# this handler opens or closes the game information editor advanced settings window,
	# depending on the status of the togglebutton
	# (when the togglebutton's activity is set to "1" then it was just depressed)
	if (self.gameInformationEditor.advanced_settings_togglebutton.get_active()):
		try:
			self.widget.gameInformationEditorAdvancedSettings.show()
		except:
			editor = self.readglade("game_information_editor_advanced_settings")
			self.gameInformationEditorAdvancedSettings = self.CogEngine_Utilities.WidgetStore(editor)
			self.insert_data_into_advanced_game_editor()
	else:
		self.read_advanced_game_editor_data_into_memory()
		try:
			self.gameInformationEditorAdvancedSettings.game_information_editor_advanced_settings.hide()
		except:
			# The window has already been destroyed
			pass




# EOF
