#####################################################################
#
# The Cog Engine Project - Cog Engine GtkSDL Modules
#
# Copyright Steven M. Castellotti (2002)
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Last Update: 2002.07.12
#
######################################################################

from CogEngine_Modules import CogEngine
import threading

#####################################################################
# Classes
#####################################################################

class icon_panel:

	def __init__(self, \
	             initial_x_coordinate, initial_y_coordinate, \
					 max_x_size, max_y_size, \
					 panel_padding, \
					 use_scrollbars, \
					 blank_icon_image_path, \
					 scroll_up_available_image_path, scroll_up_unavailable_image_path, \
					 scroll_down_available_image_path, scroll_down_unavailable_image_path, \
					 pygame_instance, screen_instance, debug_mode):

		self.initial_x_coordinate = initial_x_coordinate
		self.initial_y_coordinate = initial_y_coordinate
		self.max_x_size = max_x_size
		self.max_y_size = max_y_size
		self.panel_padding = panel_padding
		self.use_scrollbars = use_scrollbars
		self.blank_icon_image_path = blank_icon_image_path
		self.scroll_up_available_image_path = scroll_up_available_image_path
		self.scroll_up_unavailable_image_path = scroll_up_unavailable_image_path
		self.scroll_down_available_image_path = scroll_down_available_image_path
		self.scroll_down_unavailable_image_path = scroll_down_unavailable_image_path
		self.pygame = pygame_instance
		self.screen = screen_instance
		self.debug_mode = debug_mode
		self.x_image_dimension = 0
		self.y_image_dimension = 0
		self.panel_x_dimension = 0
		self.panel_y_dimension = 0
		self.scroll_up_panel = None
		self.scroll_down_panel = None
		self.icon_list = {} # list of all icons to be displayed, including the ones not visible on the current screen
		self.panel_widget_row_list = [] # list containing all of the actual panels being displayed
		self.row_to_display_as_top_row = 0 # keeps track of which row of icons should be displayed
		                                   # at the top of the panel - used with scrolling

		self.build_blank_panel()

		if (self.use_scrollbars):
			self.build_scroll_panel()
		
		self.draw_panel_graphics()

		self.discover_panel_dimensions()


	#####################################################################

	def build_blank_panel(self):

		# Draw a panel full of blank widets
		current_row = 0
		while current_row < self.max_y_size:

			current_row_list = []

			Ypos = (current_row * self.y_image_dimension) + self.initial_y_coordinate + (current_row * self.panel_padding)

			current_column = 0
			while current_column < self.max_x_size:

				Xpos = (current_column * self.x_image_dimension) + self.initial_x_coordinate + (current_column * self.panel_padding)

				current_icon_panel = graphic_panel(self.blank_icon_image_path, Xpos, Ypos, "Blank", \
				                     self.pygame, self.screen, self.debug_mode)
											
				if (self.x_image_dimension == 0):
					self.x_image_dimension = current_icon_panel.rect[2]
				if (self.y_image_dimension == 0):
					self.y_image_dimension = current_icon_panel.rect[3]

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
			Ypos = self.initial_y_coordinate + ((self.max_y_size - 1) * self.y_image_dimension) + (self.max_y_size - 1)

		self.scroll_down_panel = graphic_panel(self.scroll_down_unavailable_image_path, \
		                                     Xpos, Ypos, "Scroll Down", \
														 self.pygame, self.screen, self.debug_mode)


	#####################################################################

	def discover_panel_dimensions(self):

		if (self.use_scrollbars):
			self.panel_x_dimension = self.scroll_up_panel.Xoffset + \
			                              self.scroll_up_panel.rect[2] - \
													self.initial_x_coordinate
			self.panel_y_dimension = self.scroll_down_panel.Yoffset + \
			                              self.scroll_down_panel.rect[3] - \
													self.initial_y_coordinate
		else:
			self.panel_x_dimension = self.panel_widget_row_list[0][-1].Xoffset + \
			                              self.panel_widget_row_list[0][-1].rect[2] - \
													self.initial_x_coordinate
			self.panel_y_dimension = self.panel_widget_row_list[-1][-1].Yoffset + \
			                              self.panel_widget_row_list[-1][-1].rect[3] - \
													self.initial_y_coordinate


	#####################################################################

	def set_icons_from_list(self, icon_list):

		self.icon_list = icon_list

		icon_index = icon_list.keys()
		icon_index.sort()

		for row in range(self.row_to_display_as_top_row):
			for column in range(self.max_x_size):
				if (len(icon_index) > 0):
					del(icon_index[0])


		current_row = 0

		while current_row < self.max_y_size:

			current_panel_widget_column_list = self.panel_widget_row_list[current_row]

			Ypos = (current_row * self.y_image_dimension) + self.initial_y_coordinate + current_row

			current_column = 0

			while current_column < self.max_x_size:

				Xpos = (current_column * self.x_image_dimension) + self.initial_x_coordinate + current_column

				if (len(icon_index) > 0):
					current_icon = icon_list[icon_index[0]]
					del(icon_index[0])

					current_panel_widget_column_list[current_column].set_image(current_icon['image'])
					current_panel_widget_column_list[current_column].set_name(current_icon['name'])

				else:
					current_panel_widget_column_list[current_column].set_image(self.blank_icon_image_path)
					current_panel_widget_column_list[current_column].set_name("Blank")

				current_column = current_column + 1

			current_row = current_row + 1

		if (self.use_scrollbars):

			if (self.row_to_display_as_top_row != 0):
				self.scroll_up_panel.set_image(self.scroll_up_available_image_path)
			else:
				self.scroll_up_panel.set_image(self.scroll_up_unavailable_image_path)

			if ((len(icon_index) > 0) or ((len(icon_list) != 0) and ( self.panel_widget_row_list[-1][-1].name != "Blank" ))):
				self.scroll_down_panel.set_image(self.scroll_down_available_image_path)
			else:
				self.scroll_down_panel.set_image(self.scroll_down_unavailable_image_path)


	#####################################################################

	def set_icon_from_name(self, name, image_file_path):

		for row in self.panel_widget_row_list:

			for column in row:

				if (column.name == name):

					column.set_image(image_file_path)


	#####################################################################

	def set_icon(self, name, image_file_path):

		self.icon_list[name].set_image(image_file_path)


	#####################################################################

	def draw_panel_graphics(self):

		self.pygame.display.flip()


	#####################################################################

	def get_object_information(self, Xpos, Ypos):

		object_clicked_name = ""
		object_clicked_image = ""

		for row in self.panel_widget_row_list:

			for current_panel in row:

				if ((Xpos >= current_panel.Xoffset) and \
				(Ypos >= current_panel.Yoffset) and \
				(Xpos <= (current_panel.Xoffset + current_panel.rect[2])) and \
				(Ypos <= (current_panel.Yoffset + current_panel.rect[3]))):

					object_clicked_name = current_panel.name
					object_clicked_image = current_panel.image_file_path

		if (object_clicked_name == "") and (self.use_scrollbars):

				if ((Xpos >= self.scroll_up_panel.Xoffset) and \
				(Ypos >= self.scroll_up_panel.Yoffset) and \
				(Xpos <= (self.scroll_up_panel.Xoffset + self.scroll_up_panel.rect[2])) and \
				(Ypos <= (self.scroll_up_panel.Yoffset + self.scroll_up_panel.rect[3]))):

					object_clicked_name = self.scroll_up_panel.name
					object_clicked_image = self.scroll_up_panel.image_file_path

				elif ((Xpos >= self.scroll_down_panel.Xoffset) and \
				(Ypos >= self.scroll_down_panel.Yoffset) and \
				(Xpos <= (self.scroll_down_panel.Xoffset + self.scroll_down_panel.rect[2])) and \
				(Ypos <= (self.scroll_down_panel.Yoffset + self.scroll_down_panel.rect[3]))):

					object_clicked_name = self.scroll_down_panel.name
					object_clicked_image = self.scroll_down_panel.image_file_path


		return(object_clicked_name, object_clicked_image)


	#####################################################################

	def scroll_panels_up(self):

		if (self.use_scrollbars):

			if (self.row_to_display_as_top_row != 0):

				self.row_to_display_as_top_row = self.row_to_display_as_top_row - 1

				self.set_icons_from_list(self.icon_list)

				self.draw_panel_graphics()


	#####################################################################

	def scroll_panels_down(self):

		if (self.use_scrollbars):
		
			icon_count = len(self.icon_list.keys())

			# Subtract icons in hidden rows
			icon_count = icon_count - (self.row_to_display_as_top_row * self.max_x_size)

			# Subtract currently displayed icons
			icon_count = icon_count - (self.max_x_size * self.max_y_size)

			if (icon_count >= 0):

				self.row_to_display_as_top_row = self.row_to_display_as_top_row + 1

				self.set_icons_from_list(self.icon_list)

				self.draw_panel_graphics()


#####################################################################
#####################################################################

class graphic_panel:

	def __init__(self, background_image_file_path, Xoffset, Yoffset, name, \
					 pygame_instance, screen_instance, debug_mode):

		self.background_image_file_path = background_image_file_path
		self.image_file_path = background_image_file_path
		self.Xoffset = Xoffset
		self.Yoffset = Yoffset
		self.name = name
		self.pygame = pygame_instance
		self.screen = screen_instance
		self.debug_mode = debug_mode
		self.rect = None # This variable will store the pygame rect information for the panel
		self.load_background_graphic()


	#####################################################################

	def set_image(self, new_image_file_path):

		self.image_file_path = new_image_file_path
		self.load_graphic()


	#####################################################################

	def set_name(self, new_name):

		self.name = new_name


	#####################################################################

	def load_background_graphic(self):

		try:
			self.background_image = self.pygame.image.load(self.background_image_file_path).convert()
			self.rect = self.background_image.get_rect()
			self.screen.blit(self.background_image, (self.Xoffset, self.Yoffset))
		except:
			if (self.debug_mode):
				print "Background image failed to Load: %s" % self.image_file_path


	#####################################################################

	def load_graphic(self):

		try:
			sprite = self.pygame.image.load(self.image_file_path).convert()
			self.image_rect = sprite.get_rect()
			image_Xoffset = self.Xoffset + ((self.rect[2] - self.image_rect[2]) / 2)
			image_Yoffset = self.Yoffset + ((self.rect[3] - self.image_rect[3]) / 2)
			self.screen.blit(self.background_image, (self.Xoffset, self.Yoffset))
			self.screen.blit(sprite, (image_Xoffset, image_Yoffset))
		except:
			if (self.debug_mode):
				print "Image failed to Load: %s" % self.image_file_path


	#####################################################################

	def draw_graphic(self):

		self.pygame.display.flip()


#####################################################################
#####################################################################

class layered_graphic_panel:

	def __init__(self, Xoffset, Yoffset, \
					 pygame_instance, screen_instance, debug_mode):

		self.Xoffset = Xoffset
		self.Yoffset = Yoffset

		self.pygame = pygame_instance
		self.screen = screen_instance
		self.debug_mode = debug_mode

		self.rect = None # This variable will store the pygame rect information for the panel

		self.image_layer_list = []


	#####################################################################

	def add_image_layer(self, image_file_path, name, Xpos, Ypos, object_type):

		# This methond gets called by the Cog Engine whenever a room or object
		# is displayed.

		if (image_file_path != None):

			try:

				current_image = {}

				sprite = self.pygame.image.load(image_file_path).convert()

				current_image['image'] = image_file_path
				current_image['sprite'] = sprite
				current_image['rect'] = sprite.get_rect()
				current_image['name'] = name
				current_image['Xpos'] = Xpos
				current_image['Ypos'] = Ypos
				current_image['object_type'] = object_type


				if ((name == "Background Image") or (name[0:14] == "Object CloseUp")) and \
				   (Xpos ==  0) and (Ypos == 0):
					self.image_layer_list = []

				self.image_layer_list.append(current_image)

				self.screen.blit(sprite, (self.Xoffset + Xpos, \
				                          self.Xoffset + Ypos))

				self.pygame.display.flip()


			except:
				if (self.debug_mode):
					print "Image failed to Load: %s" % image_file_path


	#####################################################################

	def get_object_information(self, Xpos, Ypos):

		image_layers = self.image_layer_list[:] # create a copy of the image layer list
		image_layers.reverse() # reverse the order of the list so that we can descend through them

		object_clicked_name = ""
		object_clicked_type = ""

		for current_image in image_layers:

			if (object_clicked_name == "") and (object_clicked_type == ""):

				if (self.collide_solid_surface(current_image['sprite'], (Xpos - current_image['Xpos'], Ypos - current_image['Ypos']))):

#				if ((Xpos >= (current_image['Xpos'] + self.Xoffset)) and \
#				    (Ypos >= (current_image['Ypos'] + self.Yoffset)) and \
#				    (Xpos <= (current_image['Xpos'] + current_image['rect'][2]) + self.Xoffset) and \
#				    (Ypos <= (current_image['Ypos'] + current_image['rect'][3]) + self.Yoffset)):

					object_clicked_name = current_image['name']
					object_clicked_type = current_image['object_type']


		return(object_clicked_name, object_clicked_type)


	#####################################################################

	def collide_solid_surface(self, sprite, position):
		'return true if pixel at position is solid'
		try:
			pixel_rgb_values = sprite.get_at(position)
			if (self.debug_mode):
				print position
				print pixel_rgb_values
		except IndexError:
			return (0)

		if pixel_rgb_values == sprite.get_colorkey():
			return (1)

		return (pixel_rgb_values[3] > 4)


#####################################################################
#####################################################################

class mouse_pointer:

	def __init__(self, mouse_pointer_list, \
	             pygame_instance, debug_mode):

		self.mouse_pointer_list = mouse_pointer_list
		self.mouse_pointer_list.append(self.mouse_pointer_list[0]) # We append the default pointer to the
		                                                           # end of the list in order to make
																					  # cycling through pointers easier
		self.pygame = pygame_instance
		self.debug_mode = debug_mode

		self.current_pointer = None
		self.name = ""
		self.graphic = None
		self.rect = None
		self.appended_name = ""
		self.appended_graphic = None
		self.appended_rect = None

		self.current_pointer_index = 0
		self.last_pointer_index = 0

		self.set_default_pointer()


	#####################################################################

	def set_default_pointer(self):

		self.set_pointer_by_index(0)


	#####################################################################

	def set_pointer_by_index(self, index):

		if (index == 0) and (self.current_pointer_index != 0):
			self.last_pointer_index = self.current_pointer_index

		self.current_pointer = self.mouse_pointer_list[index]
		self.name = self.current_pointer['name']
		self.current_pointer_index = index

		self.appended_graphic = None
		self.appended_name = ""
		self.appended_rect = (0,0,0,0)

		try:
			self.graphic = self.pygame.image.load(self.current_pointer['image'])
			self.rect = self.graphic.get_rect()
		except:
			if (self.debug_mode):
				print "Error loading %s mouse pointer Graphic: \n%s\n" % (self.curent_pointer['name'], self.current_pointer['image'])
			self.graphic = None
			self.rect = (0,0,0,0)


	#####################################################################

	def switch_to_last_pointer(self):

		if (self.current_pointer_index != 0) and (self.last_pointer_index == self.current_pointer_index):
			self.last_pointer_index = 0

		self.set_pointer_by_index(self.last_pointer_index)


	#####################################################################

	def cycle_pointer(self):

		self.current_pointer_index = self.mouse_pointer_list.index(self.current_pointer) + 1

		self.current_pointer = self.mouse_pointer_list[ self.current_pointer_index ]
		self.name = self.current_pointer['name']

		self.appended_graphic = None
		self.appended_name = ""
		self.appended_rect = (0,0,0,0)

		try:
			self.graphic = self.pygame.image.load(self.current_pointer['image'])
			self.rect = self.graphic.get_rect()
		except:
			if (self.debug_mode):
				print "Error loading mouse pointer graphic for ", self.name, ":\n", self.current_pointer['image']
			self.set_default_cursor()


	#####################################################################

	def add_icon_to_pointer(self, name, image_file_path):

#		try:
			self.appended_graphic = self.pygame.image.load(image_file_path)
			self.appended_name = name
			self.appended_rect = self.appended_graphic.get_rect()
#		except:
#			if (self.debug_mode):
#				print "Error loading mouse pointer graphic for ", self.name, ":\n", self.current_pointer


	#####################################################################

	def remove_icon_from_pointer(self):

		self.appended_graphic = None
		self.appended_name = ""
		self.appended_rect = (0,0,0,0)


#####################################################################
#####################################################################

class Background_TTS(threading.Thread):

	def __init__(self, debug_mode):
		threading.Thread.__init__(self)

		self.debug_mode = debug_mode
		self.loop = 1

		import Queue
		self.text_queue = Queue.Queue()


	#####################################################################

	def Speak(self, text, None):
		self.text_queue.put(text)		

		
	#####################################################################

	def stop(self):

		self.loop = 0


	#####################################################################
		
	def run(self):
		from win32com.client import constants
		import win32com.client
		import time

		speech = win32com.client.Dispatch("SAPI.SpVoice")

		while self.loop:

			if not(self.text_queue.empty()):
				text = self.text_queue.get()
				speech.Speak(text)
				
			time.sleep(.001)


#####################################################################
#####################################################################

class CogEngine_GtkSDL(CogEngine):

	def initialize_sdl_graphic_area(self):

		# This method handles all of the calls to PyGame necessary for
		# creating the graphic area to display images on

		import pygame
		import pygame.image
		import pygame.locals
		import os

		self.default_path = os.path.dirname( os.path.abspath(self.database_filename) ) + "/"
		self.default_image_path = self.default_path + self.gameInformation.image_directory + "/"
		if ('audio_directory' in dir(self.gameInformation)):
			self.default_audio_path = self.default_path + self.gameInformation.audio_directory + "/"


		pygame.init()
		self.screen = pygame.display.set_mode((self.gameInformation.graphical_display_window_x_dimension, \
		                                       self.gameInformation.graphical_display_window_y_dimension, \
															), pygame.locals.HWSURFACE|pygame.locals.DOUBLEBUF)
		pygame.display.set_caption('CogEngine Graphic Window')
		background = pygame.Surface(self.screen.get_size())
		#background.fill((255,255,255)) # black background
		#background.fill((128,128,128)) # grey background
		background.fill((64,64,64)) # dark grey background

		self.screen.blit(background, (0,0))

		self.pygame = pygame


	#####################################################################

	def initialize_sound(self):

		if ('mixer' not in dir(self)):
			try:
				import pygame.mixer
				self.mixer = pygame.mixer
				self.mixer.init()
			except:
				if (self.gameInformation.debug_mode):
					print "Mixer Initialization Failed"


	#####################################################################

	def initialize_speech(self):

		self.text_to_speech_enabled = 0

		if (self.operating_system == "posix"):

			try:
				import CogEngine_Festival_Modules
				self.speech = CogEngine_Festival_Modules.Festival_TTS(self.gameInformation.debug_mode)
			except:
				if (self.gameInformation.debug_mode):
					print "Error Initializing Festival Server"
			else:
				self.text_to_speech_enabled = 1


		elif (self.operating_system == "windows"):

			try:
				self.speech = Background_TTS(self.gameInformation.debug_mode)
				self.speech.start()
			except:
				if (self.gameInformation.debug_mode):
					print "Error Initializing Microsoft Speech API."
			else:
				self.text_to_speech_enabled = 1

		if (self.text_to_speech_enabled) and (self.gameInformation.debug_mode):
			print "Text-To-Speech Enabled"


	#####################################################################

	def initialize_graphic_display_panel(self):

		self.graphic = layered_graphic_panel(self.gameInformation.graphical_display_x_coordinate, \
		                                     self.gameInformation.graphical_display_y_coordinate, \
														 self.pygame, self.screen, self.gameInformation.debug_mode)

		self.display_introduction_graphic()


	#####################################################################

	def initialize_compass_panel(self):

		self.directionStates = {} # this variable keeps track of which graphic image a particular button is displaying
										  # after we go through and create each button, we will set this to "Available" as this
										  # is the graphic image we will be displaying by default

		self.compass = icon_panel(self.gameInformation.graphical_compass_display_x_coordinate,
		                          self.gameInformation.graphical_compass_display_y_coordinate,
										  self.gameInformation.graphical_compass_x_icons, \
										  self.gameInformation.graphical_compass_y_icons, \
										  self.gameInformation.graphical_compass_panel_padding, \
										  0, \
										  self.default_image_path + self.gameInformation.graphical_compass_background_image, \
										  "", \
										  "", \
										  "", \
										  "", \
		                          self.pygame, self.screen, self.gameInformation.debug_mode)

		icon_list = {}

		if (self.gameInformation.display_help_button):
			new_icon_dict = {}
			new_icon_dict['name'] = "Menu"
			new_icon_dict['image'] = self.default_image_path + self.gameInformation.menu_button_graphic_url

			icon_list[self.gameInformation.menu_button_display_position] = new_icon_dict

		for each in self.directionData.keys():

			new_icon_dict = {}
			new_icon_dict['name'] = self.directionData[each].name

			if ((self.directionData[each].compass_graphic_available_url != None) and
			    (self.directionData[each].compass_graphic_available_url != "")):
				new_icon_dict['image'] = self.default_image_path + self.directionData[each].compass_graphic_available_url


			icon_list[self.directionData[each].compass_panel_display_position] = new_icon_dict


		self.compass.set_icons_from_list(icon_list)
		self.compass.draw_panel_graphics()


		for each in [1,2,3,4,5,6,7,8,9,10,11]:
			self.directionStates[each] = "Available"

		if (self.gameInformation.center_button_indicates_items):
			self.directionStates[5] = "ItemsNotPresent"


	#####################################################################

	def initialize_inventory_panel(self):

		self.inventory = icon_panel(self.gameInformation.graphical_inventory_panel_Xoffset,
											 self.gameInformation.graphical_inventory_panel_Yoffset,
											 self.gameInformation.graphical_inventory_x_icons,
											 self.gameInformation.graphical_inventory_y_icons,
											 self.gameInformation.graphical_inventory_panel_padding, \
											 self.gameInformation.show_graphical_inventory_panel_scrollbars, \
											 self.default_image_path + self.gameInformation.graphical_inventory_blank_icon, \
											 self.default_image_path + self.gameInformation.inventory_panel_scroll_up_available_icon, \
											 self.default_image_path + self.gameInformation.inventory_panel_scroll_up_unavailable_icon, \
											 self.default_image_path + self.gameInformation.inventory_panel_scroll_down_available_icon, \
											 self.default_image_path + self.gameInformation.inventory_panel_scroll_down_unavailable_icon, \
											 self.pygame, self.screen, self.gameInformation.debug_mode)


	#####################################################################

	def initialize_current_room_objects_panel(self):

		self.object_panel = icon_panel(self.gameInformation.object_panel_Xoffset, \
		                               self.gameInformation.object_panel_Yoffset, \
		                               self.gameInformation.object_panel_x_icons, \
		                               self.gameInformation.object_panel_y_icons, \
		                               self.gameInformation.object_panel_padding, \
		                               self.gameInformation.show_graphical_object_panel_scrollbars, \
		                               self.default_image_path + self.gameInformation.object_panel_blank_icon, \
		                               self.default_image_path + self.gameInformation.object_panel_scroll_up_available_icon, \
		                               self.default_image_path + self.gameInformation.object_panel_scroll_up_unavailable_icon, \
		                               self.default_image_path + self.gameInformation.object_panel_scroll_down_available_icon, \
		                               self.default_image_path + self.gameInformation.object_panel_scroll_down_unavailable_icon, \
		                               self.pygame, self.screen, self.gameInformation.debug_mode)


	#####################################################################

	def initialize_mouse_pointer(self):

		if (self.gameInformation.default_mouse_pointer_graphic != None) and \
		   (self.gameInformation.default_mouse_pointer_graphic != ""):

			self.pygame.mouse.set_visible(0) # turn off the OS's default cursor because we want to use our own

			mouse_cursor_list = []

			cursor_item = {}
			cursor_item['name'] = "Default"
			cursor_item['image'] = self.default_image_path + self.gameInformation.default_mouse_pointer_graphic

			mouse_cursor_list.append(cursor_item)

			verb_keys = self.verbData.keys()
			verb_keys.sort()

			for each in verb_keys:
				if (self.verbData[each].mouse_pointer_graphic != None) and \
				   (self.verbData[each].mouse_pointer_graphic != ""):

					cursor_item = {}
					cursor_item['name'] = self.verbData[each].name
					cursor_item['image'] = self.default_image_path + self.verbData[each].mouse_pointer_graphic
					mouse_cursor_list.append(cursor_item)


			self.mouse_pointer = mouse_pointer(mouse_cursor_list, self.pygame, self.gameInformation.debug_mode)

		else:
			self.mouse_pointer = None


	#####################################################################

	def display_introduction_graphic(self):

		if (self.gameInformation.introduction_graphic_url != ""):
			self.display_image(self.gameInformation.introduction_graphic_url, "Background Image", 0, 0)
		else:
			self.display_image(self.gameInformation.image_loading_graphic_url, "Background Image", 0, 0)


	#####################################################################

	def display_inventory_icons(self):

		if (self.gameInformation.show_graphic_area) and \
		   (self.gameInformation.show_graphical_inventory_panel):

			icon_list = {}

			for each in self.playerInformation.items:

				new_icon_dict = {}

				new_icon_dict['name'] = self.itemData[each].name

				if ((self.itemData[each].icon_graphic_url != None) and (self.itemData[each].icon_graphic_url != "")):
					new_icon_dict['image'] = self.default_image_path + self.itemData[each].icon_graphic_url
				else:
					new_icon_dict['image'] = self.default_image_path + self.gameInformation.graphical_inventory_graphic_not_available_icon

				icon_list[len(icon_list) + 1] = new_icon_dict

			self.inventory.set_icons_from_list(icon_list)
			self.inventory.draw_panel_graphics()


	#####################################################################

	def display_current_room_object_icons(self, room):

		if (self.gameInformation.show_graphic_area) and \
		   (self.gameInformation.show_graphical_object_panel):

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


			icon_list = {}

			for each in obstructions:

				new_icon_dict = {}
				new_icon_dict['name'] = self.obstructionData[each].name
				if ((self.obstructionData[each].icon_graphic_url != None) and (self.obstructionData[each].icon_graphic_url != "")):
					new_icon_dict['image'] = self.default_image_path + self.obstructionData[each].icon_graphic_url
				else:
					new_icon_dict['image'] = self.default_image_path + self.gameInformation.object_panel_graphic_not_available_icon

				icon_list[len(icon_list) + 1] = new_icon_dict


			for each in items:

				new_icon_dict = {}
				new_icon_dict['name'] = self.itemData[each].name
				if ((self.itemData[each].icon_graphic_url != None) and (self.itemData[each].icon_graphic_url != "")):
					new_icon_dict['image'] = self.default_image_path + self.itemData[each].icon_graphic_url
				else:
					new_icon_dict['image'] = self.default_image_path + self.gameInformation.object_panel_graphic_not_available_icon

				icon_list[len(icon_list) + 1] = new_icon_dict

			self.object_panel.set_icons_from_list(icon_list)
			self.object_panel.draw_panel_graphics()


	#####################################################################

	def display_image(self, graphic_url, name="", Xpos=0, Ypos=0, object_type=""):

		# This methond gets called by the Cog Engine whenever a room or object
		# is displayed.

		if ((self.gameInformation.show_graphic_area) and (graphic_url != None)):

			image_file_path = self.default_image_path + graphic_url

			self.graphic.add_image_layer(image_file_path, name, Xpos, Ypos, object_type)

			self.current_surface = self.pygame.display.get_surface().convert()


	#####################################################################

	def play_sound_file(self, sound_filename):

		if ('mixer' in dir(self)):
			try:
				self.mixer.music.load(self.default_audio_path + sound_filename)
				self.mixer.music.play()
			except:
				if(self.gameInformation.debug_mode):
					print "Error playing audio file:", sound_filename


	#####################################################################

	def output_text(self, text, speak_text=0):

		self.gameInformation.output_history = self.gameInformation.output_history + text

		if (speak_text) and (self.text_to_speech_enabled):
			self.speech.Speak(text, self.mixer)


		# This method is used to append text to the text output area
		if (self.gameInformation.show_text_output_area):
			self.output_textbox.insert_defaults(text)


	#####################################################################

	def pygame_event_loop(self):

		import time

		Mouse_Xpos = 0
		Mouse_Ypos = 0

		self.current_surface = self.pygame.display.get_surface().convert()

		while self.execute_pygame_loop:

			last_mouse_x = Mouse_Xpos
			last_mouse_y = Mouse_Ypos

			(Mouse_Xpos, Mouse_Ypos) = self.pygame.mouse.get_pos()

			#Handle Input Events
			for event in self.pygame.event.get():

				if event.type is self.pygame.locals.QUIT:
					#self.exit_cog_engine()
					self.execute_pygame_loop = 0

				elif event.type is self.pygame.locals.KEYDOWN and event.key is self.pygame.locals.K_ESCAPE:
					#self.exit_cog_engine()
					self.execute_pygame_loop = 0

				elif event.type is self.pygame.locals.MOUSEBUTTONDOWN:
					# A mouse button was clicked

					self.erase_previous_mouse_pointer(last_mouse_x, last_mouse_y)

					if self.pygame.mouse.get_pressed()[0]:
						# Left mouse button clicked
						panel_clicked = self.resolve_panel(Mouse_Xpos, Mouse_Ypos)

						if (self.gameInformation.debug_mode):
							print "Panel:", panel_clicked
							print "Pointer:", self.mouse_pointer.name

						if (panel_clicked == "Graphic Panel"):
							(object_name, object_type) = self.graphic.get_object_information(Mouse_Xpos, Mouse_Ypos)
							object_icon = self.resolve_icon_graphic(object_name, object_type)
							self.execute_graphical_command(object_name, object_icon, panel_clicked)

						elif (panel_clicked == "Compass Panel"):
							self.execute_graphical_compass_movement(Mouse_Xpos, Mouse_Ypos)

						elif (panel_clicked == "Inventory Panel"):
							(object_name, object_image) = self.inventory.get_object_information(Mouse_Xpos, Mouse_Ypos)
							if (self.gameInformation.debug_mode):
								print "Object:", object_name
							if (object_name == "Scroll Up"):
								self.inventory.scroll_panels_up()
							elif (object_name == "Scroll Down"):
								self.inventory.scroll_panels_down()
							else:
								self.execute_graphical_command(object_name, object_image, panel_clicked)

						elif (panel_clicked == "Object Panel"):
							(object_name, object_image) = self.object_panel.get_object_information(Mouse_Xpos, Mouse_Ypos)
							if (self.gameInformation.debug_mode):
								print "Object:", object_name
							if (object_name == "Scroll Up"):
								self.object_panel.scroll_panels_up()
							elif (object_name == "Scroll Down"):
								self.object_panel.scroll_panels_down()
							else:
								self.execute_graphical_command(object_name, object_image, panel_clicked)

						self.current_surface = self.pygame.display.get_surface().convert()


					elif self.pygame.mouse.get_pressed()[1]:
						# Middle mouse button clicked
						self.mouse_pointer.switch_to_last_pointer()


					elif self.pygame.mouse.get_pressed()[2]:
						# Right mouse button clicked
						self.mouse_pointer.cycle_pointer()


					self.draw_current_mouse_pointer(Mouse_Xpos, Mouse_Ypos)


			if (last_mouse_x != Mouse_Xpos) or (last_mouse_y != Mouse_Ypos):

				self.update_mouse_pointer_position(Mouse_Xpos, Mouse_Ypos, last_mouse_x, last_mouse_y)


			time.sleep(.0001)


	#####################################################################

	def draw_current_mouse_pointer(self, Mouse_Xpos, Mouse_Ypos):

		dirty_rects = []
		self.screen.blit(self.mouse_pointer.graphic, (Mouse_Xpos, Mouse_Ypos))
		if (self.mouse_pointer.appended_graphic != None):
			self.screen.blit(self.mouse_pointer.appended_graphic, (Mouse_Xpos + self.mouse_pointer.rect[2], Mouse_Ypos))

		dirty_rects.append((Mouse_Xpos, Mouse_Ypos, self.mouse_pointer.rect[2] + self.mouse_pointer.appended_rect[2], self.mouse_pointer.rect[3]))
		self.pygame.display.update(dirty_rects)


	#####################################################################

	def erase_previous_mouse_pointer(self, last_mouse_x, last_mouse_y):

		self.screen.blit(self.current_surface, self.mouse_pointer.rect)
		dirty_rects = []
		dirty_rects.append((last_mouse_x, last_mouse_y, self.mouse_pointer.rect[2] + self.mouse_pointer.appended_rect[2], self.mouse_pointer.rect[3]))
		self.pygame.display.update(dirty_rects)


	#####################################################################

	def update_mouse_pointer_position(self, Mouse_Xpos, Mouse_Ypos, last_mouse_x, last_mouse_y):

		dirty_rects = []
		
		# erase previous mouse pointer
		self.screen.blit(self.current_surface, self.mouse_pointer.rect)
		dirty_rects.append((last_mouse_x, last_mouse_y, self.mouse_pointer.rect[2] + self.mouse_pointer.appended_rect[2], self.mouse_pointer.rect[3]))

		# draw current mouse pointer
		self.screen.blit(self.mouse_pointer.graphic, (Mouse_Xpos, Mouse_Ypos))
		if (self.mouse_pointer.appended_graphic != None):
			self.screen.blit(self.mouse_pointer.appended_graphic, (Mouse_Xpos + self.mouse_pointer.rect[2], Mouse_Ypos))

		dirty_rects.append((Mouse_Xpos, Mouse_Ypos, self.mouse_pointer.rect[2] + self.mouse_pointer.appended_rect[2], self.mouse_pointer.rect[3]))


		self.pygame.display.update(dirty_rects)


	#####################################################################

	def resolve_panel(self, Xpos, Ypos):

		panel_name = "unknown"

		if (self.gameInformation.show_graphic_area):
			if ((Xpos >= self.gameInformation.graphical_display_x_coordinate) and \
			    (Xpos <= (self.gameInformation.graphic_panel_x_dimension + self.gameInformation.graphical_display_x_coordinate)) and \
				 (Ypos >= self.gameInformation.graphical_display_y_coordinate) and \
				 (Ypos <= (self.gameInformation.graphic_panel_y_dimension + self.gameInformation.graphical_display_y_coordinate))):

				panel_name = "Graphic Panel"


		if (panel_name == "unknown") and (self.gameInformation.show_compass):
			if ((Xpos >= self.compass.initial_x_coordinate) and \
				 (Ypos >= self.compass.initial_y_coordinate) and \
				 (Xpos <= (self.compass.panel_x_dimension + self.compass.initial_x_coordinate)) and \
				 (Ypos <= (self.compass.panel_y_dimension + self.compass.initial_y_coordinate))):

				 panel_name = "Compass Panel"


		if (panel_name == "unknown") and (self.gameInformation.show_graphical_inventory_panel):
			if ((Xpos >= self.inventory.initial_x_coordinate) and \
			    (Ypos >= self.inventory.initial_y_coordinate) and \
				 (Xpos <= (self.inventory.panel_x_dimension + self.inventory.initial_x_coordinate)) and \
				 (Ypos <= (self.inventory.panel_y_dimension + self.inventory.initial_y_coordinate))):

				panel_name = "Inventory Panel"


		if (panel_name == "unknown") and (self.gameInformation.show_graphical_object_panel):
			if ((Xpos >= self.object_panel.initial_x_coordinate) and \
			    (Ypos >= self.object_panel.initial_y_coordinate) and \
				 (Xpos <= (self.object_panel.panel_x_dimension + self.object_panel.initial_x_coordinate)) and \
				 (Ypos <= (self.object_panel.panel_y_dimension + self.object_panel.initial_y_coordinate))):

				panel_name = "Object Panel"


		return(panel_name)


	#####################################################################

	def resolve_icon_graphic(self, object_name, object_type):

		object_icon = ""

		if (object_type == "Item"):

			for each in self.itemData.keys():

				if (self.itemData[each].name == object_name) and \
				   (self.itemData[each].icon_graphic_url != None) and \
					(self.itemData[each].icon_graphic_url != ""):

					object_icon = self.default_image_path + self.itemData[each].icon_graphic_url


		elif (object_type == "Obstruction"):

			for each in self.obstructionData.keys():

				if (self.obstructionData[each].name == object_name) and \
				   (self.obstructionData[each].icon_graphic_url != None) and \
					(self.obstructionData[each].icon_graphic_url != ""):

					object_icon = self.default_image_path + self.obstructionData[each].icon_graphic_url


		return(object_icon)


	#####################################################################

	def resolve_object_closeup(self, object_name):

		import string

		object_type = string.split(object_name, '[')[1]
		object_type = string.split(object_type, ']')[0]

		object_number = string.split(object_name, '(')[1]
		object_number = string.split(object_number, ')')[0]
		object_number = string.atoi(object_number)

		if (object_type == "Item"):

			object_name = self.itemData[object_number].name
			object_image = self.default_image_path + self.itemData[object_number].icon_graphic_url

		elif (object_type == "Obstruction"):

			object_name = self.obstructionData[object_number].name
			object_image = self.default_image_path + self.obstructionData[object_number].icon_graphic_url

		return(object_name, object_image)


	#####################################################################

	def execute_graphical_compass_movement(self, Xpos, Ypos):

		command_name = self.compass.get_object_information(Xpos, Ypos)[0]

		if (command_name == "Menu"):
			#self.parse_command_line("Help")
			self.execute_pygame_loop = 0

		else:
			self.parse_command_line(command_name)

		if (self.mouse_pointer.name != "Default"):
			self.mouse_pointer.set_default_pointer()


	#####################################################################

	def execute_graphical_command(self, object_name="", object_image="", panel_clicked=""):

		if (self.mouse_pointer.name == "Default") and (self.mouse_pointer.appended_name == "") and \
		   (object_name != "Blank") and (panel_clicked != "Graphic Panel"):

			for index in range(len(self.mouse_pointer.mouse_pointer_list)):

				if (self.mouse_pointer.mouse_pointer_list[index]['name'] == "Use"):

					self.mouse_pointer.set_pointer_by_index(index)
					self.mouse_pointer.last_pointer_index = 0


		if (self.mouse_pointer.name != "Default"):

			verb = self.mouse_pointer.name

			if (self.mouse_pointer.appended_name == ""):

  				if (verb == "Look"):

					if (object_image == ""): # The did not click on an image of an object

						self.parse_command_line("Look")
                                                                        
					else:

						self.parse_command_line("Examine %s" % object_name)

				else:

					if (object_name != "Blank") and (object_name != "Background Image"):

						# Check to see if image is a Close Up of an object
						if (object_name[0:14] == "Object CloseUp"):
							(object_name, object_image) = self.resolve_object_closeup(object_name)


						self.mouse_pointer.add_icon_to_pointer(object_name, object_image)

						
					else:
						if (self.gameInformation.debug_mode):
							print object_name

			else:

				if (self.gameInformation.debug_mode):
					print "Pointer Object:", self.mouse_pointer.appended_name

				if (object_name == "Blank"):

					if (panel_clicked == "Inventory Panel"):
						self.parse_command_line("Get %s" % self.mouse_pointer.appended_name)

					elif (panel_clicked == "Object Panel"):
						self.parse_command_line("Drop %s" % self.mouse_pointer.appended_name)

				else:

					if (self.mouse_pointer.appended_name == object_name):
						self.parse_command_line("%s %s" % (verb, self.mouse_pointer.appended_name))

					else:

						if (object_image == ""): # User clicked on the background image:
							self.parse_command_line("Drop %s" % self.mouse_pointer.appended_name)

						else:
							self.parse_command_line("%s %s on %s" % (verb, self.mouse_pointer.appended_name, object_name))


				self.mouse_pointer.remove_icon_from_pointer()


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

		
#		if (self.gameInformation.show_graphic_area) and \
#		   (self.gameInformation.show_graphical_inventory_panel):
#			self.display_inventory_icons()


	#####################################################################

	def update_compass_graphicbuttons(self):

		# This method gets called by the Cog Engine whenever a room is displayed.
		# The method determines which of the graphics currently being displayed by
		# the compass are no longer accurate, and changes those images to the correct
		# ones for the current room.

		if (self.gameInformation.show_graphic_area) and (self.gameInformation.show_compass):

			for direction in self.directionData.keys():

				direction_state = self.get_direction_state(direction)

				if (self.directionStates[direction] != direction_state):

					# We need to handle the special case that the Center GraphicButton is being used
					# to indicate the presense of items in the current room
					if ((direction == 5) and (self.gameInformation.center_button_indicates_items)):
						if (type(self.roomData[self.playerInformation.current_room].items) != type(None)):
							# There are items in the room
							if (self.directionStates[5] == "ItemsNotPresent"):
								self.compass.set_icon_from_name("Center", self.default_image_path + self.directionData[5].compass_graphic_special_url)
								self.directionStates[5] = "ItemsPresent"

						else:
							# There are no items in the room
							if (self.directionStates[5] == "ItemsPresent"):
								self.compass.set_icon_from_name("Center", self.default_image_path + self.directionData[5].compass_graphic_available_url)
								self.directionStates[5] = "ItemsNotPresent"

					else:
						# We need to change the current graphic

						if (direction_state == "Available"):
							self.compass.set_icon_from_name(self.directionData[direction].name, self.default_image_path + \
														self.directionData[direction].compass_graphic_available_url)
							self.directionStates[direction] = "Available"

						elif (direction_state == "Unavailable"):
							self.compass.set_icon_from_name(self.directionData[direction].name, self.default_image_path + \
														self.directionData[direction].compass_graphic_unavailable_url)
							self.directionStates[direction] = "Unavailable"

						elif (direction_state == "Obstructed"):
							self.compass.set_icon_from_name(self.directionData[direction].name, self.default_image_path + \
														self.directionData[direction].compass_graphic_special_url)
							self.directionStates[direction] = "Obstructed"

						elif (direction_state == "Previously Traveled"):
							self.compass.set_icon_from_name(self.directionData[direction].name, self.default_image_path + \
														self.directionData[direction].compass_graphic_previously_traveled)
							self.directionStates[direction] = "Previously Traveled"

						elif (direction_state == "Last Direction Traveled"):
							self.compass.set_icon_from_name(self.directionData[direction].name, self.default_image_path + \
														self.directionData[direction].compass_graphic_last_direction_traveled)
							self.directionStates[direction] = "Last Direction Traveled"


			self.compass.draw_panel_graphics()

