#####################################################################
#
# The Cog Engine Project - Cog Engine GtkSDL Modules
#
# Copyright Steven M. Castellotti (2002)
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Last Update: 2002.06.10
#
######################################################################

from CogEngine_Modules import CogEngine

#####################################################################
# Classes
#####################################################################

class compass_panel:

	def __init__(self, x_image_dimension, y_image_dimension, \
					initial_x_coordinate, initial_y_coordinate, \
					pygame_instance, screen_instance, debug_mode):

		self.x_image_dimension = x_image_dimension
		self.y_image_dimension = y_image_dimension
		self.initial_x_coordinate = initial_x_coordinate
		self.initial_y_coordinate = initial_y_coordinate
		self.pygame = pygame_instance
		self.screen = screen_instance
		self.debug_mode = debug_mode
		self.button_widget_tree = {}


	#####################################################################

	def create_compass_button(self, name, image_file_path, \
									x_layout_coordinate, y_layout_coordinate):

		Xpos = (x_layout_coordinate * self.x_image_dimension) + self.initial_x_coordinate
		Ypos = (y_layout_coordinate * self.y_image_dimension) + self.initial_y_coordinate

		new_compass_button = graphic_button(image_file_path, Xpos, Ypos, name, \
									self.pygame, self.screen, self.debug_mode)

		self.button_widget_tree[name] = new_compass_button


	#####################################################################

	def set_image(self, name, image_file_path):

		self.button_widget_tree[name].set_image(image_file_path)


	#####################################################################

	def draw_compass_graphics(self):

		self.pygame.display.flip()


#####################################################################

class icon_panel:

	def __init__(self, x_image_dimension, y_image_dimension, \
					initial_x_coordinate, initial_y_coordinate, \
					max_x_size, max_y_size, blank_icon_image_path, \
					use_scrollbars, \
					scroll_up_available_image_path, scroll_up_unavailable_image_path, \
					scroll_down_available_image_path, scroll_down_unavailable_image_path, \
					pygame_instance, screen_instance, debug_mode):

		self.x_image_dimension = x_image_dimension
		self.y_image_dimension = y_image_dimension
		self.initial_x_coordinate = initial_x_coordinate
		self.initial_y_coordinate = initial_y_coordinate
		self.max_x_size = max_x_size
		self.max_y_size = max_y_size
		self.blank_icon_image_path = blank_icon_image_path
		self.use_scrollbars = use_scrollbars
		self.scroll_up_available_image_path = scroll_up_available_image_path
		self.scroll_up_unavailable_image_path = scroll_up_unavailable_image_path
		self.scroll_down_available_image_path = scroll_down_available_image_path
		self.scroll_down_unavailable_image_path = scroll_down_unavailable_image_path
		self.pygame = pygame_instance
		self.screen = screen_instance
		self.debug_mode = debug_mode
		self.icon_list = [] # list of all icons to be displayed, including the ones not visible on the current screen
		self.panel_widget_row_list = [] # list containing all of the actual panels being displayed
		self.row_to_display_as_top_row = 0 # keeps track of which row of icons should be displayed
		                                   # at the top of the panel - used with scrolling

		self.build_blank_panel()
		if (self.use_scrollbars):
			self.build_scroll_panel()
		self.draw_panel_graphics()


	#####################################################################

	def build_blank_panel(self):

		# Draw a panel full of blank widets
		current_row = 0
		while current_row < self.max_y_size:

			current_row_list = []

			Ypos = (current_row * self.y_image_dimension) + self.initial_y_coordinate + current_row

			current_column = 0
			while current_column < self.max_x_size:

				Xpos = (current_column * self.x_image_dimension) + self.initial_x_coordinate + current_column

				current_icon_panel = graphic_panel(self.blank_icon_image_path, Xpos, Ypos, "Blank", \
				                     self.pygame, self.screen, self.debug_mode)

				current_row_list.append(current_icon_panel)

				current_column = current_column + 1

			self.panel_widget_row_list.append(current_row_list)
			current_row = current_row + 1


	#####################################################################

	def build_scroll_panel(self):
	
		Xpos = (self.max_x_size * self.x_image_dimension) + self.initial_x_coordinate + self.max_x_size + 2
		Ypos = self.initial_y_coordinate
		
		self.scroll_up_panel = graphic_panel(self.scroll_up_unavailable_image_path, \
		                                     Xpos, Ypos, "Scroll Up", \
														 self.pygame, self.screen, self.debug_mode)

		if (self.max_y_size == 1):
			Ypos = self.initial_y_coordinate + (self.y_image_dimension / 2)
		else:
			Ypos = self.initial_y_coordinate + ((self.max_y_size - 1) * self.y_image_dimension) + (self.max_y_size -1)
			
		self.scroll_up_panel = graphic_panel(self.scroll_down_unavailable_image_path, \
		                                     Xpos, Ypos, "Scroll Down", \
														 self.pygame, self.screen, self.debug_mode)


	#####################################################################

	def set_icons_from_list(self, icon_list):

		self.icon_list = icon_list[:] # create a copy of the icon list and store it in the local object

		current_row = 0

		while current_row < self.max_y_size:
			
			current_panel_widget_column_list = self.panel_widget_row_list[current_row]

			Ypos = (current_row * self.y_image_dimension) + self.initial_y_coordinate + current_row

			current_column = 0
			while current_column < self.max_x_size:

				Xpos = (current_column * self.x_image_dimension) + self.initial_x_coordinate + current_column

				if (len(icon_list) > 0):
					current_icon = icon_list[0]
					del(icon_list[0])

					current_panel_widget_column_list[current_column].set_image(current_icon['image'])
					current_panel_widget_column_list[current_column].set_name(current_icon['name'])

				else:
					current_panel_widget_column_list[current_column].set_image(self.blank_icon_image_path)
					current_panel_widget_column_list[current_column].set_name("Blank")

				current_column = current_column + 1

			current_row = current_row + 1
			
		if ((self.use_scrollbars) and (len(icon_list) > 0)):
			self.scroll_up_panel.set_image(self.scroll_down_available_image_path)
		else:                                                                  
			self.scroll_up_panel.set_image(self.scroll_down_unavailable_image_path)


	#####################################################################

	def set_icon(self, name, image_file_path):

		self.icon_list[name].set_image(image_file_path)


	#####################################################################

	def draw_panel_graphics(self):

		self.pygame.display.flip()


#####################################################################

class graphic_panel:

	def __init__(self, image_file_path, Xoffset, Yoffset, name, \
					pygame_instance, screen_instance, debug_mode):

		self.image_file_path = image_file_path
		self.Xoffset = Xoffset
		self.Yoffset = Yoffset
		self.name = name
		self.pygame = pygame_instance
		self.screen = screen_instance
		self.debug_mode = debug_mode
		self.load_graphic()


	#####################################################################

	def set_image(self, new_image_file_path):

		self.image_file_path = new_image_file_path
		self.load_graphic()
		#self.draw_graphic()


	#####################################################################
	
	def set_name(self, new_name):
	
		self.name = new_name


	#####################################################################

	def load_graphic(self):

		try:
			sprite = self.pygame.image.load(self.image_file_path).convert()
			self.screen.blit(sprite, (self.Xoffset, self.Yoffset))
		except:
			if (self.debug_mode):
				print "Image failed to Load: %s" % self.image_file_path


	#####################################################################

	def draw_graphic(self):

		self.pygame.display.flip()


#####################################################################

class graphic_button(graphic_panel):

	# There are currently no differences between a graphic panel
	# and a graphic button, but this will be changed later

	pass


#####################################################################

class CogEngine_GtkSDL(CogEngine):

	def initialize_sdl_graphic_area(self):

		# This method handles all of the calls to PyGame necessary for
		# creating the graphic area to display images on

		import pygame
		import pygame.image
		import pygame.locals
		import os

		self.default_path = os.path.dirname( os.path.abspath(self.database_filename) ) + "/" + \
							self.gameInformation.image_directory + "/"

		pygame.init()
		self.screen = pygame.display.set_mode((self.gameInformation.graphical_display_window_x_dimension, \
		                                       self.gameInformation.graphical_display_window_y_dimension, \
															), pygame.locals.HWSURFACE|pygame.locals.DOUBLEBUF)
		pygame.display.set_caption('CogEngine Graphic Window')
		background = pygame.Surface(self.screen.get_size())
	#	background.fill((255,255,255))
		background.fill((128,128,128))


		if (self.gameInformation.introduction_graphic_url != ""):
			sprite_file = self.default_path + self.gameInformation.introduction_graphic_url
		else:
			sprite_file = self.default_path + self.gameInformation.image_loading_graphic_url

		try:
			sprite = pygame.image.load(sprite_file).convert()
			self.screen.blit(background, (0,0))
			self.screen.blit(sprite, (self.gameInformation.graphical_display_x_coordinate, \
			                          self.gameInformation.graphical_display_y_coordinate))
			pygame.display.flip()
		except:
			if (self.gameInformation.debug_mode):
				print "Image failed to Load: %s" % sprite_file

		self.pygame = pygame


	#####################################################################

	def initialize_sdl_compass_area(self):

		self.directionStates = {} # this variable keeps track of which graphic image a particular button is displaying
										# after we go through and create each button, we will set this to "Available" as this
										# is the graphic image we will be displaying by default

		self.compass = compass_panel(self.gameInformation.graphical_compass_button_image_x_dimension, \
                                   self.gameInformation.graphical_compass_button_image_y_dimension, \
		                             self.gameInformation.graphical_compass_display_x_coordinate, \
											  self.gameInformation.graphical_compass_display_y_coordinate, \
		                             self.pygame, self.screen, self.gameInformation.debug_mode)

		self.compass.create_compass_button("Help", self.default_path + self.gameInformation.menu_button_graphic_url, 0, 0)

		self.compass.create_compass_button(self.directionData[1].name, self.default_path + \
													self.directionData[1].compass_graphic_available_url, \
													1, 0)

		self.compass.create_compass_button(self.directionData[2].name, self.default_path + \
													self.directionData[2].compass_graphic_available_url, \
													2, 0)

		self.compass.create_compass_button(self.directionData[3].name, self.default_path + \
													self.directionData[3].compass_graphic_available_url, \
													3, 0)

		self.compass.create_compass_button(self.directionData[4].name, self.default_path + \
													self.directionData[4].compass_graphic_available_url, \
													1, 1)

		self.compass.create_compass_button(self.directionData[5].name, self.default_path + \
													self.directionData[5].compass_graphic_available_url, \
													2, 1)

		self.compass.create_compass_button(self.directionData[6].name, self.default_path + \
													self.directionData[6].compass_graphic_available_url, \
													3, 1)

		self.compass.create_compass_button(self.directionData[7].name, self.default_path + \
													self.directionData[7].compass_graphic_available_url, \
													1, 2)

		self.compass.create_compass_button(self.directionData[8].name, self.default_path + \
													self.directionData[8].compass_graphic_available_url, \
													2, 2)

		self.compass.create_compass_button(self.directionData[9].name, self.default_path + \
													self.directionData[9].compass_graphic_available_url, \
													3, 2)

		self.compass.create_compass_button(self.directionData[10].name, self.default_path + \
													self.directionData[10].compass_graphic_available_url, \
													0, 1)

		self.compass.create_compass_button(self.directionData[11].name, self.default_path + \
													self.directionData[11].compass_graphic_available_url, \
													0, 2)

		for each in [1,2,3,4,5,6,7,8,9,10,11]:
			self.directionStates[each] = "Available"

		if (self.gameInformation.center_button_indicates_items):
			self.directionStates[5] = "ItemsNotPresent"

		self.compass.draw_compass_graphics()


	#####################################################################

	def initialize_speech(self):

		self.text_to_speech_enabled = 0

		if (self.operating_system == "posix"):

			#pid = os.fork()

			#if not pid:
			#	os.execlp("which", "which", "festival_server")
			#else:
			#	childpid, exit_code = os.wait(pid)

			#if exit_code:

			try:
				import CogEngine_Festival_Modules
				self.speech = CogEngine_Festival_Modules.Festival()
			except:
				if (self.gameInformation.debug_mode):
					print "Error Initializing Festival Server"
			else:
				self.text_to_speech_enabled = 1


		elif (self.operating_system == "windows"):

			try:
				import sys
				from win32com.client import constants
				import win32com.client
				self.speech = win32com.client.Dispatch("SAPI.SpVoice")
			except:
				if (self.gameInformation.debug_mode):
					print "Error Initializing Microsoft Speech API."
			else:
				self.text_to_speech_enabled = 1

		if (self.text_to_speech_enabled) and (self.gameInformation.debug_mode):
			print "Text-To-Speech Enabled"


	#####################################################################

	def initialize_inventory_panel(self):

		self.inventory = icon_panel(self.gameInformation.graphical_inventory_x_icon_dimension,
		                            self.gameInformation.graphical_inventory_x_icon_dimension,
											 self.gameInformation.graphical_inventory_panel_Xoffset,
											 self.gameInformation.graphical_inventory_panel_Yoffset,
											 self.gameInformation.graphical_inventory_x_icons,
											 self.gameInformation.graphical_inventory_y_icons,
											 self.default_path + self.gameInformation.graphical_inventory_blank_icon, \
											 self.gameInformation.show_graphical_inventory_panel_scrollbars, \
											 self.default_path + self.gameInformation.inventory_panel_scroll_up_available_icon, \
											 self.default_path + self.gameInformation.inventory_panel_scroll_up_unavailable_icon, \
											 self.default_path + self.gameInformation.inventory_panel_scroll_down_available_icon, \
											 self.default_path + self.gameInformation.inventory_panel_scroll_down_unavailable_icon, \
											 self.pygame, self.screen, self.gameInformation.debug_mode)


	#####################################################################

	def initialize_current_room_objects_panel(self):

		self.current_room_objects = icon_panel(self.gameInformation.object_panel_x_icon_dimension, \
		                                       self.gameInformation.object_panel_y_icon_dimension, \
															self.gameInformation.object_panel_panel_Xoffset, \
															self.gameInformation.object_panel_panel_Yoffset, \
															self.gameInformation.object_panel_x_icons, \
															self.gameInformation.object_panel_y_icons, \
															self.default_path + self.gameInformation.object_panel_blank_icon, \
															self.gameInformation.show_graphical_object_panel_scrollbars, \
															self.default_path + self.gameInformation.object_panel_scroll_up_available_icon, \
															self.default_path + self.gameInformation.object_panel_scroll_up_unavailable_icon, \
															self.default_path + self.gameInformation.object_panel_scroll_down_available_icon, \
															self.default_path + self.gameInformation.object_panel_scroll_down_unavailable_icon, \
															self.pygame, self.screen, self.gameInformation.debug_mode)


	#####################################################################

	def display_inventory_icons(self):

		icon_list = []

		for each in self.playerInformation.items:

			new_icon_dict = {}

			new_icon_dict['name'] = self.itemData[each].name

			if ((self.itemData[each].icon_graphic_url != None) and (self.itemData[each].icon_graphic_url != "")):
				new_icon_dict['image'] = self.default_path + self.itemData[each].icon_graphic_url
			else:
				new_icon_dict['image'] = self.default_path + self.gameInformation.graphical_inventory_graphic_not_available_icon

			icon_list.append(new_icon_dict)

		self.inventory.set_icons_from_list(icon_list)
		self.inventory.draw_panel_graphics()


	#####################################################################

	def display_current_room_object_icons(self, room):

		import string

		obstructions = []

		# Create visible obstruction list
		for direction in self.roomData[ room ].direction.keys():
			obstruction_list = self.roomData[ room ].direction[direction].obstructions
			if (type(obstruction_list) != type(None)):
				# Convert string of comma-separated obstruction numbers into a list of integers
				obstruction_strings = string.split(obstruction_list, ', ')
				for each in obstruction_strings:
					if (self.obstructionData[ string.atoi(each) ].visible):
						obstructions.append(string.atoi(each))


		items = []

		# Create item list
		item_list = self.roomData[ room ].items
		if (type(item_list) != type(None)):
			# Convert string of comman-separated item numbers into a list of integers
			item_strings = string.split(item_list, ', ')
			for each in item_strings:
				items.append(string.atoi(each))


 		icon_list = []

		for each in obstructions:
		
			new_icon_dict = {}
			new_icon_dict['name'] = self.obstructionData[each].name
			if ((self.obstructionData[each].icon_graphic_url != None) and (self.obstructionData[each].icon_graphic_url != "")):
				new_icon_dict['image'] = self.default_path + self.obstructionData[each].icon_graphic_url
			else:
				new_icon_dict['image'] = self.default_path + self.gameInformation.object_panel_graphic_not_available_icon

			icon_list.append(new_icon_dict)


		for each in items:

			new_icon_dict = {}
			new_icon_dict['name'] = self.itemData[each].name
			if ((self.itemData[each].icon_graphic_url != None) and (self.itemData[each].icon_graphic_url != "")):
				new_icon_dict['image'] = self.default_path + self.itemData[each].icon_graphic_url
			else:
				new_icon_dict['image'] = self.default_path + self.gameInformation.object_panel_graphic_not_available_icon

			icon_list.append(new_icon_dict)

		self.current_room_objects.set_icons_from_list(icon_list)
		self.current_room_objects.draw_panel_graphics()


	#####################################################################

	def display_image(self, graphic_url, Xpos=0, Ypos=0):

		# This methond gets called by the Cog Engine whenever a room or object
		# is displayed.

		if ((self.gameInformation.show_graphic_area) and (graphic_url != None)):

			try:
				sprite = self.pygame.image.load(self.default_path + graphic_url).convert()
				self.screen.blit(sprite, (self.gameInformation.graphical_display_x_coordinate + Xpos, \
				                          self.gameInformation.graphical_display_y_coordinate + Ypos))
				self.pygame.display.flip()
			except:
				if (self.gameInformation.debug_mode):
					print "Image failed to Load: %s" % graphic_url


	#####################################################################

	def output_text(self, text, speak_text=0):

		if (speak_text) and (self.text_to_speech_enabled):
			# Send Text to the Text-To-Speech Synthesizer
			#if (self.operating_system == "windows"):
			#	import thread
			#	thread.start_new_thread(self.speech.Speak(text))
			#else:
				self.speech.Speak(text)


		# This method is used to append text to the text output area

		if (self.gameInformation.show_text_output_area):

			self.output_textbox.insert_defaults(text)


	#####################################################################

	def main_pygame_loop(self):

		import time

		self.pygame.mouse.set_visible(0)

		while 1:

			#Handle Input Events
			for event in self.pygame.event.get():
				if event.type is self.pygame.locals.QUIT:
					self.exit_cog_engine()
				elif event.type is self.pygame.locals.KEYDOWN and event.key is self.pygame.locals.K_ESCAPE:
					self.exit_cog_engine()

			(Mouse_Xpos, Mouse_Ypos) = self.pygame.mouse.get_pos()
			self.display_image(self.verbData[1].mouse_pointer_graphic, Mouse_Xpos, Mouse_Ypos)

			time.sleep(.001)


	#####################################################################

	def command_line_set_text(self, text):

		# This method is used to change the current output on the command line
		# If speak_text is set to true when the method is called, the text will also
		# be sent to the text-to-speech synthesizer

		if (self.gameInformation.show_command_line):

			self.commandline_entry.set_text(text)


	#####################################################################

	def set_statistics_text(self, text):

		# This method is used to change the text being displayed in the Statistics/Information window

		if (self.gameInformation.show_stats):

			self.statistics_textbox.delete_text(0, -1)
			self.statistics_textbox.insert_defaults(text)


	#####################################################################

	def set_inventory_text(self, text):

		# This method is used to change the text being displayed in the Inventory window

		if (self.gameInformation.show_inventory):

			self.inventory_textbox.delete_text(0, -1)
			self.inventory_textbox.insert_defaults(text)
			
			self.display_inventory_icons()


	#####################################################################

	def update_compass_graphicbuttons(self):

		# This method gets called by the Cog Engine whenever a room is displayed.
		# The method determines which of the graphics currently being displayed by
		# the compass are no longer accurate, and changes those images to the correct
		# ones for the current room.

		for direction in self.directionData.keys():

			direction_state = self.get_direction_state(direction)

			if (self.directionStates[direction] != direction_state):

				# We need to handle the special case that the Center GraphicButton is being used
				# to indicate the presense of items in the current room
				if ((direction == 5) and (self.gameInformation.center_button_indicates_items)):
					if (type(self.roomData[self.playerInformation.current_room].items) != type(None)):
						# There are items in the room
						if (self.directionStates[5] == "ItemsNotPresent"):
							self.compass.set_image("Center", self.default_path + self.directionData[5].compass_graphic_special_url)
							self.directionStates[5] = "ItemsPresent"

					else:
						# There are no items in the room
						if (self.directionStates[5] == "ItemsPresent"):
							self.compass.set_image("Center", self.default_path + self.directionData[5].compass_graphic_available_url)
							self.directionStates[5] = "ItemsNotPresent"

				else:
					# We need to change the current graphic

					if (direction_state == "Available"):
						self.compass.set_image(self.directionData[direction].name, self.default_path + \
													self.directionData[direction].compass_graphic_available_url)
						self. directionStates[direction] = "Available"

					elif (direction_state == "Unavailable"):
						self.compass.set_image(self.directionData[direction].name, self.default_path + \
													self.directionData[direction].compass_graphic_unavailable_url)
						self. directionStates[direction] = "Unavailable"

					elif (direction_state == "Obstructed"):
						self.compass.set_image(self.directionData[direction].name, self.default_path + \
													self.directionData[direction].compass_graphic_special_url)
						self. directionStates[direction] = "Unavailable"

		self.compass.draw_compass_graphics()

