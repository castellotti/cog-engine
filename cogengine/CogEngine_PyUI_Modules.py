#####################################################################
#
# The Cog Engine Project - Cog Engine PyUI Modules
#
# Copyright Steven M. Castellotti (2002)
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Last Update: 2002.05.16
#
######################################################################


#####################################################################
# Functions
#####################################################################

def initialize_gui(self, display_type="2d"):

	# This method is called when the Cog Engine Application is first run.
	# The method lays out all of the widgets used by the Cog Engine.

	import os, pyui

	pyui.init(875,650, display_type)

	mainWindow = pyui.widgets.Window(0, 0, 875, 650)


	mainSplitterPanel = pyui.widgets.SplitterPanel(pyui.widgets.SplitterPanel.HORIZONTAL,
													pyui.widgets.SplitterPanel.PIXELS,
													480)

	topSplitterPanel = pyui.widgets.SplitterPanel(pyui.widgets.SplitterPanel.VERTICAL,
													pyui.widgets.SplitterPanel.PIXELS,
													235)

	bottomSplitterPanel = pyui.widgets.SplitterPanel(pyui.widgets.SplitterPanel.VERTICAL,
													pyui.widgets.SplitterPanel.PIXELS,
													150)


	menuPanel = pyui.widgets.Panel()
	menuPanel.setLayout(pyui.layouts.GridLayoutManager(1,2))

	self.statisticsEdit = pyui.widgets.Edit("Statistics", 0, None)
	self.inventoryEdit = pyui.widgets.Edit("Inventory", 0, None)

	menuPanel.addChild(self.statisticsEdit)
	menuPanel.addChild(self.inventoryEdit)

	# Set up the Graphic Display Area
	image_path = os.path.dirname( os.path.abspath(self.game_database_filename) )

	if (self.gameInformation.introduction_graphic_url != ""):
		image_file = self.gameInformation.image_directory + "/" + self.gameInformation.introduction_graphic_url
	else:
		image_file = self.gameInformation.image_directory + "/" + self.gameInformation.image_loading_graphic_url

	self.graphicPicture = pyui.widgets.Picture(image_file)


	self.commandlineEdit = pyui.widgets.Edit("", 0, self.on_commandline_edit_activate)

	compassPanel = pyui.widgets.Panel()
	compassPanel.setLayout(pyui.layouts.GridLayoutManager(3,3))

	for i in ['NW', 'N', 'NE', 'W', 'Center', 'E', 'SW', 'S', 'SE']:
		imagebutton = pyui.widgets.ImageButton("Images/COG-Compass-Available(%s).jpg" % i, self.on_button_press, i)
		compassPanel.addChild(imagebutton)

	self.outputEdit = pyui.widgets.Edit("", 0, None)

	navigationSplitterPanel = pyui.widgets.SplitterPanel(pyui.widgets.SplitterPanel.HORIZONTAL,
													pyui.widgets.SplitterPanel.PIXELS,
													20)

	navigationSplitterPanel.replaceFirstPanel(self.commandlineEdit)
	navigationSplitterPanel.replaceSecondPanel(compassPanel)


	topSplitterPanel.replaceFirstPanel(menuPanel)
	topSplitterPanel.replaceSecondPanel(self.graphicPicture)

	bottomSplitterPanel.replaceFirstPanel(navigationSplitterPanel)
	bottomSplitterPanel.replaceSecondPanel(self.outputEdit)

	mainSplitterPanel.replaceFirstPanel(topSplitterPanel)
	mainSplitterPanel.replaceSecondPanel(bottomSplitterPanel)

	mainWindow.replacePanel(mainSplitterPanel)

	mainWindow.pack()

	self.pyui = pyui


#####################################################################

def display_image(self, graphic_url, Xpos=0, Ypos=0):

	# This methond gets called by the Cog Engine whenever a room or object
	# is displayed.

	import os

	if ((self.gameInformation.show_graphic_area) and (graphic_url != None)):

		image_url = self.gameInformation.image_directory + "/" + graphic_url
		file_path = os.path.dirname( os.path.abspath(self.game_database_filename) )
		image_file = "%s/%s" % (file_path, image_url)

	try:
		graphic_picture.setFilename(image_file)
	except:
		if (self.gameInformation.debug_mode):
			print "Image failed to Load: %s" % sprite_file


#####################################################################

def output_text(self, append_text):

	# This method is used to append text to the text output area

	print "output_text called"

	if (self.gameInformation.show_text_output_area):

		current_text = self.outputEdit.text
		new_text = current_text + append_text

		self.outputEdit.setText(new_text)


#####################################################################

def command_line_set_text(self, text):

	# This method is used to change the current output on the command line

	self.commandlineEdit.setText(text)


#####################################################################

def set_statistics_text(self, text):

	# This method is used to change the text being displayed in the Statistics/Information window

	self.statisticsEdit.setText(text)


#####################################################################

def set_inventory_text(self, text):

	# This method is used to change the text being displayed in the Inventory window

	self.inventoryEdit.setText(text)


#####################################################################

def on_commandline_edit_activate(self, edit):

	# This method is called whenever a user hits enter after typing a command onto the command line

	print "Entered: ", edit.text


#####################################################################

def on_button_press(self, event):

	# This method is called whenever a button is pressed

	print "the button was pressed"


#####################################################################

def update_compass_graphicbuttons(self):

	# This method gets called by the Cog Engine whenever a room is displayed.
	# The method determines which of the graphics currently being displayed by
	# the compass are no longer accurate, and changes those images to the correct
	# ones for the current room.

	pass


# EOF
