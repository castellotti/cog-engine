#####################################################################
#
# The Cog Engine Project - Cog Engine GtkSDL Modules
#
# Copyright Steven M. Castellotti (2002)
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Last Update: 2002.05.29
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
		self.draw_graphic()


	#####################################################################

	def set_image(self, new_image_file_path):

		self.image_file_path = new_image_file_path
		self.draw_graphic()

	
	#####################################################################

	def draw_graphic(self):

		try:
			sprite = self.pygame.image.load(self.image_file_path).convert()
			self.screen.blit(sprite, (self.Xoffset, self.Yoffset))
			self.pygame.display.flip()
		except:
			if (self.debug_mode):
				print "Image failed to Load: %s" % self.image_file_path


#####################################################################

class graphic_button(graphic_panel):

	def __init__(self, image_file_path, Xoffset, Yoffset, name, \
					pygame_instance, screen_instance, debug_mode):

		self.image_file_path = image_file_path
		self.Xoffset = Xoffset
		self.Yoffset = Yoffset
		self.name = name
		self.pygame = pygame_instance
		self.screen = screen_instance
		self.debug_mode = debug_mode
		self.draw_graphic()


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
		self.screen = pygame.display.set_mode((640,595), pygame.locals.HWSURFACE|pygame.locals.DOUBLEBUF)
		pygame.display.set_caption('CogEngine SDL Graphic Window')
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
			self.screen.blit(sprite, (0,0))
			pygame.display.flip()
		except:
			if (self.gameInformation.debug_mode):
				print "Image failed to Load: %s" % sprite_file

		self.pygame = pygame


	#####################################################################

	def initialize_speech(self):

		import os

		self.text_to_speech_enabled = 0

		if (os.name == "posix"):

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
				print "Error Initializing Festival Server"
			else:
				self.text_to_speech_enabled = 1


		elif (os.name == "nt") or (os.name == "dos"):

			try:
				import sys
				from win32com.client import constants
				import win32com.client
				self.speech = win32com.client.Dispatch("SAPI.SpVoice")
			except:
				print "Error Initializing Microsoft Speech API."
			else:
				self.text_to_speech_enabled = 1

		if (self.text_to_speech_enabled) and (self.gameInformation.debug_mode):
			print "Text-To-Speech Enabled"


	#####################################################################

	def initialize_sdl_compass_area(self):

		self.directionStates = {} # this variable keeps track of which graphic image a particular button is displaying
										# after we go through and create each button, we will set this to "Available" as this
										# is the graphic image we will be displaying by default

		#self.pygame.draw.line(self.screen, (0,0,0), (0,481), (640, 481), width=1)

	#	self.compass = compass_panel(37, 37, 2, 482, \
	#	                             self.pygame, self.screen, self.gameInformation.debug_mode)
		self.compass = compass_panel(37, 37, 246, 482, \
											self.pygame, self.screen, self.gameInformation.debug_mode)

		self.compass.create_compass_button("Help", self.default_path + "COG-Compass-Menu.gif", 0, 0)

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


	#####################################################################

	def display_image(self, graphic_url, Xpos=0, Ypos=0):

		# This methond gets called by the Cog Engine whenever a room or object
		# is displayed.

		if ((self.gameInformation.show_graphic_area) and (graphic_url != None)):

			try:
				sprite = self.pygame.image.load(self.default_path + graphic_url).convert()
				self.screen.blit(sprite, (Xpos,Ypos))
				self.pygame.display.flip()
			except: 
				if (self.gameInformation.debug_mode):
					print "Image failed to Load: %s" % sprite_file


	#####################################################################

	def output_text(self, text, speak_text=0):

		if (speak_text) and (self.text_to_speech_enabled):
			# Send Text to the Text-To-Speech Synthesizer
			self.speech.Speak(text)

		# This method is used to append text to the text output area

		if (self.gameInformation.show_text_output_area):

			self.output_textbox.insert_defaults(text)


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

