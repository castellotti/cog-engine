#####################################################################
#
# The Cog Engine Project - Cog Engine GtkSDL Modules
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

def initialize_sdl_graphic_area(self):

	# This method handles all of the calls to PyGame necessary for
	# creating the graphic area to display images on

	import pygame
	import pygame.image
	import pygame.locals
	import os

	pygame.init()
	self.screen = pygame.display.set_mode((640,480), pygame.locals.HWSURFACE|pygame.locals.DOUBLEBUF)
	pygame.display.set_caption('CogEngine SDL Graphic Window')
	background = pygame.Surface(self.screen.get_size())
	background.fill((255,255,255))

	file_path = os.path.dirname( os.path.abspath(self.database_filename) )

	if (self.gameInformation.introduction_graphic_url != ""):
		sprite_file = self.gameInformation.image_directory + "/" + self.gameInformation.introduction_graphic_url
	else:
		sprite_file = self.gameInformation.image_directory + "/" + self.gameInformation.image_loading_graphic_url

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

def display_image(self, graphic_url, Xpos=0, Ypos=0):

	# This methond gets called by the Cog Engine whenever a room or object
	# is displayed.

	import os

	if ((self.gameInformation.show_graphic_area) and (graphic_url != None)):

		image_url = self.gameInformation.image_directory + "/" + graphic_url

		sprite_file = image_url

		try:
			file_path = os.path.dirname( os.path.abspath(self.database_filename) )
			sprite = self.pygame.image.load(file_path + "/" + sprite_file).convert()
			self.screen.blit(sprite, (Xpos,Ypos))
			self.pygame.display.flip()
		except:
			if (self.gameInformation.debug_mode):
				print "Image failed to Load: %s" % sprite_file


#####################################################################

def output_text(self, text):

	# This method is used to append text to the text output area

	if (self.gameInformation.show_text_output_area):

		self.output_textbox.insert_defaults(text)


#####################################################################

def command_line_set_text(self, text):

	# This method is used to change the current output on the command line

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

def on_commandline_entry_activate(self, obj):

	# This method is called whenever a user hits enter after typing a command onto the command line

	command = self.commandline_entry.get_text()
	self.commandline_entry.set_text("")
	self.parse_command_line(command)


#####################################################################

def update_compass_graphicbuttons(self):

	# This method gets called by the Cog Engine whenever a room is displayed.
	# The method determines which of the graphics currently being displayed by
	# the compass are no longer accurate, and changes those images to the correct
	# ones for the current room.

	pass
