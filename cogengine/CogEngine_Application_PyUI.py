#!/usr/bin/env python2
#!/usr/bin/env python2.1
#
#####################################################################
#
# Cog Engine Application (PyUI)
#
# Copyright Steven M. Castellotti (2002)
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
#
# Calling Example:
#    python CogEngine_PyUI.py <Game Data File>
# or
#    ./CogEngine_PyUI.py <Game Data File>
#
#
# Last Update: 2002.05.12
#
#
#####################################################################

class CogEngine_PyUI:

	import CogEngine_Utilities

	from CogObjects import *
	from CogEngine_Modules import *
	from CogEngine_PyUI_Modules import *


	def __init__(self):

		self.load_data_file()
		self.initialize_gui()
		self.initialize_engine()

		done = 1

		while done:
			self.pyui.draw()
			done = self.pyui.update()

		self.pyui.quit()



#####################################################################

	def load_data_file(self):

		# This methond loads the Game Data File specified on the command
		# line (refer to the calling example in the header notes

		import sys, CogEngine_Utilities

		self.game_database_filename = sys.argv[1]

		(self.gameInformation, self.playerInformation, \
		self.directionData, self.roomData, \
		self.itemData, self.obstructionData, self.verbData) \
		= self.CogEngine_Utilities.load_data_file(self.game_database_filename)


#####################################################################

	#def initialize_new_game(self):
	#def initialize_widgets(self):
	#def exit_cog_engine(self):

	#def on_new_file_activate(self, obj):
	#def on_open_activate(self, obj):
	#def on_save_activate(self, obj):
	#def on_save_as_activate(self, obj):
	#def on_quit(self, obj):
	#def on_about_activate(self, obj):
	#def on_open_fileselection_ok_button_clicked(self, obj):
	#def on_open_fileselection_cancel_button_clicked(self, obj):
	#def on_save_as_fileselection_ok_button_clicked(self, obj):
	#def on_save_as_fileselection_cancel_button_clicked(self, obj):
	#def initialize_new_game(self):
	#def initialize_widgets(self):
	#def exit_cog_engine(self):


#####################################################################
# Main
#####################################################################

if __name__ == '__main__':
	CogEngine_PyUI()


