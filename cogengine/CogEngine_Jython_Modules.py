#!/usr/bin/env jython
#
#####################################################################
#
# The Cog Engine Project - Cog Engine Jython Modules
#
# Copyright Steven M. Castellotti (2002)
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Last Update: 2002.05.16
#
#####################################################################

from java import awt
import java.net.URL

#####################################################################
# Functions
#####################################################################

def initialize_gui(self):

	# This method handles the layout of the applet's GUI
	# The applet uses a GridBagLayout to handle the positioning of all of its widgets

	# Panel Reference
	# (0,0) (1,0) (2,0)
	# (0,1) (1,1) (2,1)
	# (0,2) (1,2) (2,2)

	self.setLayout(awt.GridBagLayout())
	constraints = awt.GridBagConstraints()

	##################
	# Panel Settings #
	##################

	# Setup for Top Panel
	# (includes Graphic Area and Menu Panel)
	constraints.fill = awt.GridBagConstraints.BOTH
	constraints.weightx = 1.0
	constraints.weighty = 0.0
	constraints.gridx = 0
	constraints.gridy = 0
	top_panel = awt.Panel(layout=awt.GridBagLayout())

	self.add(top_panel, constraints)

	# Setup for Bottom Panel
	# (includes Control Panel and Text Display Output Area
	constraints.weightx = 1.0
	constraints.weighty = 1.0
	constraints.gridx = 0
	constraints.gridy = 1
	bottom_panel = awt.Panel(layout=awt.GridBagLayout())

	self.add(bottom_panel, constraints)

	# Setup for Menu Panel
	if ((self.gameInformation.show_stats) or (self.gameInformation.show_inventory)):
		constraints.weightx = 1.0
		constraints.weighty = 0.0
		constraints.gridx = 0
		constraints.gridy = 0
		menu_panel = awt.Panel(layout=awt.GridBagLayout())

		top_panel.add(menu_panel, constraints)

	# Setup for Control Panel
	constraints.weightx = 0.0
	constraints.weighty = 1.0
	constraints.gridx = 0
	constraints.gridy = 0
	control_panel = awt.Panel(layout=awt.GridBagLayout())

	bottom_panel.add(control_panel, constraints)

	# Setup for Navigation Panel
	# (includes Compass Area)
	if (self.gameInformation.show_compass):
		constraints.weightx = 0.0
		constraints.weighty = 0.0
		constraints.gridx = 0
		constraints.gridy = 1
		compass_panel = awt.Panel(layout=awt.GridBagLayout())

		control_panel.add(compass_panel, constraints)

	######################
	# Component Settings #
	######################

	# Setup for GraphicArea (Canvas)
	if (self.gameInformation.show_graphic_area):
		import GraphicPanel
		constraints.anchor = awt.GridBagConstraints.CENTER
		constraints.fill = awt.GridBagConstraints.NONE
		constraints.weightx = 0.0
		constraints.weighty = 0.0
		constraints.gridx = 1
		constraints.gridy = 0

		if (self.gameInformation.introduction_graphic_url != ""):
			current_url = java.net.URL("%s%s/%s" % (self.getCodeBase(), self.gameInformation.image_directory, self.gameInformation.introduction_graphic_url))
		else:
			current_url = java.net.URL("%s%s/%s" % (self.getCodeBase(), self.gameInformation.image_directory, self.gameInformation.image_loading_graphic_url))

		#python.security.respectJavaAccessibility = 0
		self.graphic_area = GraphicPanel(self, current_url, self.gameInformation.debug_mode)

		top_panel.add(self.graphic_area, constraints)



	# Setup for the Statistical Text Area
	if (self.gameInformation.show_stats):
		constraints.anchor = awt.GridBagConstraints.CENTER
		constraints.fill = awt.GridBagConstraints.BOTH
		constraints.weightx = 1.0
		constraints.weighty = 1.0
		constraints.gridx = 0
		constraints.gridy = 0
		self.information_textarea = awt.TextArea("InfoArea", 1, 1, awt.TextArea.SCROLLBARS_NONE)
		self.information_textarea.setEditable(0)
		self.information_textarea.setText("")

		menu_panel.add(self.information_textarea, constraints)

	# Setup for the Inventory Text Area
	if (self.gameInformation.show_inventory):
		constraints.anchor = awt.GridBagConstraints.CENTER
		constraints.fill = awt.GridBagConstraints.BOTH
		constraints.weightx = 1.0
		constraints.weighty = 1.0
		constraints.gridx = 0
		constraints.gridy = 1
		self.inventory_textarea = awt.TextArea("InventoryArea", 1, 1, awt.TextArea.SCROLLBARS_VERTICAL_ONLY)
		self.inventory_textarea.setEditable(0)
		self.inventory_textarea.setText("Inventory:")

		menu_panel.add(self.inventory_textarea, constraints)

	# Setup for the Text Display Area
	if (self.gameInformation.show_text_output_area):
		constraints.anchor = awt.GridBagConstraints.CENTER
		constraints.fill = awt.GridBagConstraints.BOTH
		constraints.weightx = 1.0
		constraints.weighty = 1.0
		constraints.gridx = 1
		constraints.gridy = 0
		self.output_textarea = awt.TextArea("OutputArea", 1, 1, awt.TextArea.SCROLLBARS_VERTICAL_ONLY)
		self.output_textarea.setEditable(0)
		self.output_textarea.setText("")

		bottom_panel.add(self.output_textarea, constraints)

	# Setup for the Command Line
	if (self.gameInformation.show_command_line):
		constraints.anchor = awt.GridBagConstraints.CENTER
		constraints.fill = awt.GridBagConstraints.HORIZONTAL
		constraints.weightx = 1.0
		constraints.weighty = 1.0
		constraints.gridx = 0
		constraints.gridy = 0
		self.command_line = awt.TextField()
		self.command_line.addActionListener(self)
		self.command_line.requestFocus()

		control_panel.add(self.command_line, constraints)


	# Setup for the Compass

	# Panel Reference
	# (0,0) (1,0) (2,0)
	# (0,1) (1,1) (2,1)
	# (0,2) (1,2) (2,2)

	if (self.gameInformation.show_compass):
		import GraphicButton
		constraints.anchor = awt.GridBagConstraints.CENTER
		constraints.fill = awt.GridBagConstraints.BOTH
		constraints.weightx = 1.0
		constraints.weighty = 1.0
		constraints.gridx = 0
		constraints.gridy = 0

		if (type(self.gameInformation.menu_button_graphic_url) != type(None)):
			try:
				current_url = java.net.URL("%s%s/%s" % (self.getCodeBase(), self.gameInformation.image_directory, self.gameInformation.menu_button_graphic_url))
			except bad_url_error:
				print "Bad URL - Compass Menu Button Graphic: %s" % self.gameInformation.menu_button_graphic_url
			compass_menu_graphicbutton = GraphicButton(self, current_url)
			compass_menu_graphicbutton.setActionCommand("Help")
			compass_menu_graphicbutton.addActionListener(self)
			compass_panel.add(compass_menu_graphicbutton, constraints)
		else:
			compass_menu_textbutton = awt.Button("Help")
			compass_menu_textbutton.addActionListener(self)
			compass_panel.add(compass_menu_textbutton, constraints)

		if (self.gameInformation.load_all_compass_images):
			# Pre-Loading all of the compass button graphics during game
			# initialization will help to speed up gameplay later
			media_tracker = awt.MediaTracker(self)

			if (self.gameInformation.debug_mode):
				print "Downloading Compass Button Graphic Images...",

			for direction in self.directionData.keys():
				try:
					current_url = java.net.URL("%s%s/%s" % (self.getCodeBase(), self.gameInformation.image_directory, self.directionData[direction].compass_graphic_available_url))
					image = self.getImage(current_url)
					media_tracker.addImage(image, 0)
					media_tracker.waitForID(0)

					current_url = java.net.URL("%s%s/%s" % (self.getCodeBase(), self.gameInformation.image_directory, self.directionData[direction].compass_graphic_unavailable_url))
					image = self.getImage(current_url)
					media_tracker.addImage(image, 0)
					media_tracker.waitForID(0)

					current_url = java.net.URL("%s%s/%s" % (self.getCodeBase(), self.gameInformation.image_directory, self.directionData[direction].compass_graphic_special_url))
					image = self.getImage(current_url)
					media_tracker.addImage(image, 0)
					media_tracker.waitForID(0)

				except exception_error:
					print "Error Downloading Compass Button Graphic!"
					print "Exception was:"
					print exception_error

			if (self.gameInformation.debug_mode):
				print "Done."

			media_tracker = None


		if (len(self.directionData.keys()) >= 3):

			self.directionStates = {} # this variable keeps track of which graphic image a particular button is displaying
			                          # as we go through and create each button, we will set this to "Available" as this
			                          # is the graphic image we will be displaying by default
			# NorthWest
			try:
				current_url = java.net.URL("%s%s/%s" % (self.getCodeBase(), self.gameInformation.image_directory, self.directionData[1].compass_graphic_available_url))
			except bad_url_error:
				print "Bad URL - Compass Button Graphic: %s" % self.directionData[1].compass_graphic_available_url
			self.northwest_graphicbutton = GraphicButton(self, current_url)
			self.northwest_graphicbutton.setActionCommand(self.directionData[1].name)
			self.northwest_graphicbutton.addActionListener(self)
			constraints.gridx = 1
			constraints.gridy = 0
			compass_panel.add(self.northwest_graphicbutton, constraints)
			self.directionStates[1] = "Available"

			# North
			try:
				current_url = java.net.URL("%s%s/%s" % (self.getCodeBase(), self.gameInformation.image_directory, self.directionData[2].compass_graphic_available_url))
			except bad_url_error:
				print "Bad URL - Compass Button Graphic: %s" % self.directionData[2].compass_graphic_available_url
			self.north_graphicbutton = GraphicButton(self, current_url)
			self.north_graphicbutton.setActionCommand(self.directionData[2].name)
			self.north_graphicbutton.addActionListener(self)
			constraints.gridx = 2
			constraints.gridy = 0
			compass_panel.add(self.north_graphicbutton, constraints)
			self.directionStates[2] = "Available"

			# NorthEast
			try:
				current_url = java.net.URL("%s%s/%s" % (self.getCodeBase(), self.gameInformation.image_directory, self.directionData[3].compass_graphic_available_url))
			except bad_url_error:
				print "Bad URL - Compass Button Graphic: %s" % self.directionData[3].compass_graphic_available_url
			self.northeast_graphicbutton = GraphicButton(self, current_url)
			self.northeast_graphicbutton.setActionCommand(self.directionData[3].name)
			self.northeast_graphicbutton.addActionListener(self)
			constraints.gridx = 3
			constraints.gridy = 0
			compass_panel.add(self.northeast_graphicbutton, constraints)
			self.directionStates[3] = "Available"


		if (len(self.directionData.keys()) >= 9):

			# West
			try:
				current_url = java.net.URL("%s%s/%s" % (self.getCodeBase(), self.gameInformation.image_directory, self.directionData[4].compass_graphic_available_url))
			except bad_url_error:
				print "Bad URL - Compass Button Graphic: %s" % self.directionData[4].compass_graphic_available_url
			self.west_graphicbutton = GraphicButton(self, current_url)
			self.west_graphicbutton.setActionCommand(self.directionData[4].name)
			self.west_graphicbutton.addActionListener(self)
			constraints.gridx = 1
			constraints.gridy = 1
			compass_panel.add(self.west_graphicbutton, constraints)
			self.directionStates[4] = "Available"

			# Center
			try:
				current_url = java.net.URL("%s%s/%s" % (self.getCodeBase(), self.gameInformation.image_directory, self.directionData[5].compass_graphic_available_url))
			except bad_url_error:
				print "Bad URL - Compass Button Graphic: %s" % self.directionData[5].compass_graphic_available_url
			self.center_graphicbutton = GraphicButton(self, current_url)
			self.center_graphicbutton.setActionCommand(self.directionData[5].name)
			self.center_graphicbutton.addActionListener(self)
			constraints.gridx = 2
			constraints.gridy = 1
			compass_panel.add(self.center_graphicbutton, constraints)
			if (self.gameInformation.center_button_indicates_items):
				self.directionStates[5] = "ItemsNotPresent"
			else:
				self.directionStates[5] = "Available"

			# East
			try:
				current_url = java.net.URL("%s%s/%s" % (self.getCodeBase(), self.gameInformation.image_directory, self.directionData[6].compass_graphic_available_url))
			except bad_url_error:
				print "Bad URL - Compass Button Graphic: %s" % self.directionData[6].compass_graphic_available_url
			self.east_graphicbutton = GraphicButton(self, current_url)
			self.east_graphicbutton.setActionCommand(self.directionData[6].name)
			self.east_graphicbutton.addActionListener(self)
			constraints.gridx = 3
			constraints.gridy = 1
			compass_panel.add(self.east_graphicbutton, constraints)
			self.directionStates[6] = "Available"

			# SouthWest
			try:
				current_url = java.net.URL("%s%s/%s" % (self.getCodeBase(), self.gameInformation.image_directory, self.directionData[7].compass_graphic_available_url))
			except bad_url_error:
				print "Bad URL - Compass Button Graphic: %s" % self.directionData[7].compass_graphic_available_url
			self.southwest_graphicbutton = GraphicButton(self, current_url)
			self.southwest_graphicbutton.setActionCommand(self.directionData[7].name)
			self.southwest_graphicbutton.addActionListener(self)
			constraints.gridx = 1
			constraints.gridy = 2
			compass_panel.add(self.southwest_graphicbutton, constraints)
			self.directionStates[7] = "Available"

			# South
			try:
				current_url = java.net.URL("%s%s/%s" % (self.getCodeBase(), self.gameInformation.image_directory, self.directionData[8].compass_graphic_available_url))
			except bad_url_error:
				print "Bad URL - Compass Button Graphic: %s" % self.directionData[8].compass_graphic_available_url
			self.south_graphicbutton = GraphicButton(self, current_url)
			self.south_graphicbutton.setActionCommand(self.directionData[8].name)
			self.south_graphicbutton.addActionListener(self)
			constraints.gridx = 2
			constraints.gridy = 2
			compass_panel.add(self.south_graphicbutton, constraints)
			self.directionStates[8] = "Available"

			# SouthEast
			try:
				current_url = java.net.URL("%s%s/%s" % (self.getCodeBase(), self.gameInformation.image_directory, self.directionData[9].compass_graphic_available_url))
			except bad_url_error:
				print "Bad URL - Compass Button Graphic: %s" % self.directionData[9].compass_graphic_available_url
			self.southeast_graphicbutton = GraphicButton(self, current_url)
			self.southeast_graphicbutton.setActionCommand(self.directionData[9].name)
			self.southeast_graphicbutton.addActionListener(self)
			constraints.gridx = 3
			constraints.gridy = 2
			compass_panel.add(self.southeast_graphicbutton, constraints)
			self.directionStates[9] = "Available"


		if (len(self.directionData.keys()) >= 9):

			# Up
			try:
				current_url = java.net.URL("%s%s/%s" % (self.getCodeBase(), self.gameInformation.image_directory, self.directionData[10].compass_graphic_available_url))
			except bad_url_error:
				print "Bad URL - Compass Button Graphic: %s" % self.directionData[10].compass_graphic_available_url
			self.up_graphicbutton = GraphicButton(self, current_url)
			self.up_graphicbutton.setActionCommand(self.directionData[10].name)
			self.up_graphicbutton.addActionListener(self)
			constraints.gridx = 0
			constraints.gridy = 1
			compass_panel.add(self.up_graphicbutton, constraints)
			self.directionStates[10] = "Available"

			# Down
			try:
				current_url = java.net.URL("%s%s/%s" % (self.getCodeBase(), self.gameInformation.image_directory, self.directionData[11].compass_graphic_available_url))
			except bad_url_error:
				print "Bad URL - Compass Button Graphic: %s" % self.directionData[11].compass_graphic_available_url
			self.down_graphicbutton = GraphicButton(self, current_url)
			self.down_graphicbutton.setActionCommand(self.directionData[11].name)
			self.down_graphicbutton.addActionListener(self)
			constraints.gridx = 0
			constraints.gridy = 2
			compass_panel.add(self.down_graphicbutton, constraints)
			self.directionStates[11] = "Available"


			#awt.Graphics.setFont( awt.Font("Courier", awt.Font.PLAIN, 10), None )


	self.validate()


#####################################################################

def actionPerformed(self, action_event):

	# This method is called whenever a compass graphic button is pressed,
	# or whenever enter is hit when the command line is the active widget

	command = action_event.getActionCommand()

	if (command=="Center"):
		command = "Look"

	self.command_line_set_text("")
	self.parse_command_line(command)


#####################################################################

def display_image(self, graphic_url, Xpos=0, Ypos=0):

	# This methond gets called by the Cog Engine whenever a room or object
	# is displayed.

	if (self.gameInformation.show_graphic_area):

		if (type(graphic_url) != type(None)):

			try:
				current_url = java.net.URL( "%s%s/%s" % (self.getCodeBase(), self.gameInformation.image_directory, graphic_url))
			except bad_url_error:
				print "Graphic URL: \"%s\" is Malformed!\n" % graphic_url


			# If the image is going to be displayed at the upper-left corner of the screen, we want
			# to display this image as the root image for the graphic panel.
			#
			# If the image is going to be displayed at some other coordinates, we want to add another layer
			# to the current image instead of replacing it.

			if ((Xpos==0) and (Ypos==0)):
				self.graphic_area.setImage(self, current_url)
			else:
				self.graphic_area.addImageLayer(self, current_url, Xpos, Ypos)


#####################################################################

def output_text(self, text):

	# This method is used to append text to the text output area

	if (self.gameInformation.show_text_output_area):

		self.output_textarea.append(text)


#####################################################################

def command_line_set_text(self, text):

	# This method is used to change the current output on the command line

	if (self.gameInformation.show_command_line):

		self.command_line.setText(text)


#####################################################################

def set_statistics_text(self, text):

	# This method is used to change the text being displayed in the Statistics/Information window

	if (self.gameInformation.show_stats):

		self.information_textarea.setText(text)


#####################################################################

def set_inventory_text(self, text):

	# This method is used to change the text being displayed in the Inventory window

	if (self.gameInformation.show_inventory):

		self.inventory_textarea.setText(text)


#####################################################################

def update_compass_graphicbuttons(self):

	# Sequence to Update Compass GraphicButtons
	# Graphics should only be downloaded (by calling setImage) if
	# a different graphic should be used than the one currently
	# displayed. The graphic currently being displayed is kept
	# track of through the self.directionStates variable.

	for direction in self.directionData.keys():

		direction_state = self.get_direction_state(direction)

		if (self.directionStates[direction] != direction_state):

			# We need to handle the special case that the Center GraphicButton is being used
			# to indicate the presense of items in the current room
			if ((direction == 5) and (self.gameInformation.center_button_indicates_items)):
				if (type(self.roomData[self.playerInformation.current_room].items) != type(None)):
					# There are items in the room
					if (self.directionStates[5] == "ItemsNotPresent"):
						try:
							current_url = java.net.URL("%s%s/%s" % (self.getCodeBase(), self.gameInformation.image_directory, self.directionData[5].compass_graphic_special_url))
						except bad_url_error:
							print "Bad URL - Compass Button Graphic: %s" % self.directionData[5].compass_graphic_special_url

						self.center_graphicbutton.setImage(self, current_url)
						self.directionStates[5] = "ItemsPresent"

				else:
					# There are no items in the room
					if (self.directionStates[5] == "ItemsPresent"):
						try:
							current_url = java.net.URL("%s%s/%s" % (self.getCodeBase(), self.gameInformation.image_directory, self.directionData[5].compass_graphic_available_url))
						except bad_url_error:
							print "Bad URL - Compass Button Graphic: %s" % self.directionData[5].compass_graphic_available_url

						self.center_graphicbutton.setImage(self, current_url)
						self.directionStates[5] = "ItemsNotPresent"

			else:
				# We need to change the current graphic

				if (direction_state == "Available"):
					try:
						current_url = java.net.URL("%s%s/%s" % (self.getCodeBase(), self.gameInformation.image_directory, self.directionData[direction].compass_graphic_available_url))
					except bad_url_error:
						print "Bad URL - Compass Button Graphic: %s" % self.directionData[direction].compass_graphic_available_url
					self. directionStates[direction] = "Available"

				elif (direction_state == "Unavailable"):
					try:
						current_url = java.net.URL("%s%s/%s" % (self.getCodeBase(), self.gameInformation.image_directory, self.directionData[direction].compass_graphic_unavailable_url))
					except bad_url_error:
						print "Bad URL - Compass Button Graphic: %s" % self.directionData[direction].compass_graphic_unavailable_url
					self. directionStates[direction] = "Unavailable"

				elif (direction_state == "Obstructed"):
					try:
						current_url = java.net.URL("%s%s/%s" % (self.getCodeBase(), self.gameInformation.image_directory, self.directionData[direction].compass_graphic_special_url))
					except bad_url_error:
						print "Bad URL - Compass Button Graphic: %s" % self.directionData[direction].compass_graphic_special_url
					self. directionStates[direction] = "Unavailable"

				if (direction == 1):
					self.northwest_graphicbutton.setImage(self, current_url)
				elif (direction == 2):
					self.north_graphicbutton.setImage(self, current_url)
				elif (direction == 3):
					self.northeast_graphicbutton.setImage(self, current_url)
				elif (direction == 4):
					self.west_graphicbutton.setImage(self, current_url)
				elif (direction == 5):
					self.center_graphicbutton.setImage(self, current_url)
				elif (direction == 6):
					self.east_graphicbutton.setImage(self, current_url)
				elif (direction == 7):
					self.southwest_graphicbutton.setImage(self, current_url)
				elif (direction == 8):
					self.south_graphicbutton.setImage(self, current_url)
				elif (direction == 9):
					self.southeast_graphicbutton.setImage(self, current_url)
				elif (direction == 10):
					self.up_graphicbutton.setImage(self, current_url)
				elif (direction == 11):
					self.down_graphicbutton.setImage(self, current_url)


# EOF
