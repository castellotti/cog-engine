#####################################################################
#
# COG Engine Development Application - Cog Engine Routines
#
# Copyright Steven M. Castellotti (2002)
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Last Update: 2002.04.29
#
#####################################################################
# To Do List:
#####################################################################
#
#  - If Grammar support is going to be added for a verb with no objects
#    then it can be done quite easily in resolve_event, and the methods
#    which call it
#
#  - Remove check for direction 5 in parse_command_line
#
#  - It may be possible to extend event grammer to allow
#    verb-only actions (no objects) by working within the
#    user-defined verbs section of the command line parser
#
#  - Connect gtk_widget_destroy() signals on the windows to a method that
#    removes the windows from the self namespace
#
#
#####################################################################


#####################################################################
# Functions
#####################################################################

#def initialize_engine(self):
#def initialize_gui(self):
#def initialize_sdl_graphic_area(self):
#def hide_windows(self):
#def display_image(self, graphic_url, Xpos, Ypos):
#def output_text(self, text):
#def command_line_set_text(self, text):
#def display_introduction(self):
#def display_room(self, room):
#def parse_command_line(self, command):
#def display_verbs(self):
#def move_in_direction(self, direction):
#def room_warp(self, new_room):
#def execute_effect(self, effect):
#def resolve_verb(self, user_verb):
#def resolve_direction_name(self, direction):
#def get_item(self, item_name):
#def drop_item(self, item_name):
#def room_contains_item(self, room_number, item_number):
#def room_contains_obstruction(self, room_number, obstruction_number):
#def room_direction_contains_obstruction(self, room_number, direction_number, obstruction_number):
#def resolve_item_name(self, item_name, location):
#def resolve_obstruction_name(self, obstruction_name, location):
#def find_item_alias(self, item_name, location):
#def find_obstruction_alias(self, obstruction_name, location):
#def add_item_to_room(self, room_number, item_number):
#def add_obstruction_to_room(self, room_number, direction_number, obstruction_number):
#def remove_item_from_room(self, room_number, item_number):
#def remove_obstruction_from_room_direction(self, room_number, direction_number, obstruction_number):
#def parse_command_line_objects(self, remainder):
#def parse_object(self, phrase, search_focus):
#def resolve_event(self, action, objects):
#def requirements_met(self, requirements):
#def make_comparison( self, comparison, value1, value2):
#def evaluate_expression(self, expression, value1, value2):
#def examine_object(self, object_name):
#def load_game(self):
#def save_game(self):


#####################################################################

#def on_room_editor_destroy(self, obj):
#	# This function is called if a user closes a window directly,
#	# instead of clicking off the toggle button
#	self.widget.room_togglebutton.set_active(0)


#####################################################################

def initialize_engine(self):

	initialize_gui(self)
	# Display Introduction text if the current room is 1
	display_room(self, self.playerInformation.current_room)
	self.last_command = ""


#####################################################################

def initialize_gui(self):

	import utils

	# Display Graphic Area
	initialize_sdl_graphic_area(self)

	# Load CogEngine Window
	cog_engine_window = self.readglade("CogEngine")
	self.cog_engine = utils.WidgetStore(cog_engine_window)
	self.io = self.cog_engine
	self.stats = self.cog_engine
	self.inventory = self.cog_engine

	# Display Output Window and Command Line
#	textmode_window = self.readglade("textmode_window")
#	self.io = utils.WidgetStore(textmode_window)

	# Display Statistics Window
#	if (self.gameInformation.show_stats):
#		statistics_window = self.readglade("statistics_window")
#		self.stats = utils.WidgetStore(statistics_window)

	# Display Inventory Window
#	if (self.gameInformation.show_inventory):
#		inventory_window = self.readglade("inventory_window")
#		self.inventory = utils.WidgetStore(inventory_window)

	# Display Introduction text if the current room is the first room
	if (self.playerInformation.current_room == 1):
		display_introduction(self)


#####################################################################

def initialize_sdl_graphic_area(self):

	import pygame
	import pygame.image
	import pygame.locals

	pygame.init()
	screen = pygame.display.set_mode((640,480), pygame.locals.HWSURFACE|pygame.locals.DOUBLEBUF)
	background = pygame.Surface(screen.get_size())
	background.fill((255,255,255))

	import os
	file_path = os.path.dirname( os.path.abspath(self.database_filename) )
	print file_path

	if (self.gameInformation.introduction_graphic_url != ""):
		sprite_file = self.gameInformation.image_directory + "/" + self.gameInformation.introduction_graphic_url
		try:
			sprite = pygame.image.load(sprite_file)
			#sprite_position = sprite.get_rect()
			#sprite_position.bottom = (480 / 2)
			#sprite_position.left = (640 / 2)
			screen.blit(background, (0,0))
			#screen.blit(sprite, sprite_position)
			screen.blit(sprite, (0,0))
			pygame.display.flip()
		except:
			try:
				import os
				file_path = os.path.dirname( os.path.abspath(self.database_filename) )
				print file_path
				sprite = self.pygame.image.load(file_path + "/" + sprite_file)
				#sprite_position = sprite.get_rect()
				#sprite_position.bottom = (480 / 2)
				#sprite_position.left = (640 / 2)
				screen.blit(background, (0,0))
				#screen.blit(sprite, sprite_position)
				screen.blit(sprite, (Xpos,Ypos))
				self.pygame.display.flip()
			except:
				if (self.gameInformation.debug_mode):
					print "Image failed to Load: %s" % sprite_file

	self.pygame = pygame


#####################################################################

def hide_windows(self):

	self.cog_engine.CogEngine.hide()

#	self.io.textmode_window.hide()
#
#	if (self.gameInformation.show_stats):
#		self.stats.statistics_window.hide()
#	if (self.gameInformation.show_inventory):
#		self.inventory.inventory_window.hide()


#####################################################################

def display_image(self, graphic_url, Xpos, Ypos):

	if (self.gameInformation.show_graphic_area):

		image_url = self.gameInformation.image_directory + "/" + graphic_url

		screen = self.pygame.display.set_mode((640,480), self.pygame.locals.HWSURFACE|self.pygame.locals.DOUBLEBUF)
		background = self.pygame.Surface(screen.get_size())
		background.fill((255,255,255))

		print self.database_filename

		sprite_file = image_url
		try:
			sprite = self.pygame.image.load(sprite_file)
			#sprite_position = sprite.get_rect()
			#sprite_position.bottom = (480 / 2)
			#sprite_position.left = (640 / 2)
			screen.blit(background, (0,0))
			#screen.blit(sprite, sprite_position)
			screen.blit(sprite, (Xpos,Ypos))
			self.pygame.display.flip()
		except:
			try:
				import os
				file_path = os.path.dirname( os.path.abspath(self.database_filename) )
				sprite = self.pygame.image.load(file_path + "/" + sprite_file)
				#sprite_position = sprite.get_rect()
				#sprite_position.bottom = (480 / 2)
				#sprite_position.left = (640 / 2)
				screen.blit(background, (0,0))
				#screen.blit(sprite, sprite_position)
				screen.blit(sprite, (Xpos,Ypos))
				self.pygame.display.flip()
			except:
				if (self.gameInformation.debug_mode):
					print "Image failed to Load: %s" % sprite_file


#####################################################################

def output_text(self, text):

	if (self.gameInformation.show_text_output_area):

		if ("io" in dir(self)):

			self.io.output_textbox.insert_defaults(text)


#####################################################################

def command_line_set_text(self, text):

	if (self.gameInformation.show_command_line):
		self.io.commandline_entry.set_text(text)

#####################################################################

def display_introduction(self):

	output_text(self, self.gameInformation.introduction_text + "\n\n" )


#####################################################################

def display_room(self, room):

	import string

	# Display Room's Graphic
	display_image(self, self.roomData[self.playerInformation.current_room].graphic_url, 0, 0)


	# Display Game Statistics
	if (self.gameInformation.show_stats):
		stats_output = "%s\n\n" % self.gameInformation.game_title
		if (self.playerInformation.name != ""):
			stats_output = "%sPlayer's Name: %s\n" % (stats_output, self.playerInformation.name)
		if (self.playerInformation.email_address != ""):
			stats_output = "%sPlayer's Email Address: %s\n" % (stats_output, self.playerInformation.email_address)
		if (self.gameInformation.debug_mode):
			stats_output = "%s\nCurrent Room Number: %s\n" % (stats_output, self.playerInformation.current_room)
			stats_output = "%sCurrent Room Name: %s\n\n" % (stats_output, self.roomData[self.playerInformation.current_room].name)
		if (self.playerInformation.points != -1):
			stats_output = "%sPoints: %s\n" % (stats_output, self.playerInformation.points)
		if (self.playerInformation.experience_level != -1):
			stats_output = "%sExperience Level: %s\n" % (stats_output, self.playerInformation.experience_level)
		if (self.playerInformation.experience != -1):
			stats_output = "%sExperience: %s\n" % (stats_output, self.playerInformation.experience)
		if (self.playerInformation.hp != -1):
			stats_output = "%sHealth Points (HP): %s\n" % (stats_output, self.playerInformation.hp)
		if (self.playerInformation.mp != -1):
			stats_output = "%sMagic Points (MP): %s\n" % (stats_output, self.playerInformation.mp)
		if (self.playerInformation.strength != -1):
			stats_output = "%sStrength: %s\n" % (stats_output, self.playerInformation.strength)
		if (self.playerInformation.intelligence != -1):
			stats_output = "%sIntelligence: %s\n" % (stats_output, self.playerInformation.intelligence)
		if (self.playerInformation.dexterity != -1):
			stats_output = "%sDexterity: %s\n" % (stats_output, self.playerInformation.dexterity)
		if (self.playerInformation.agility != -1):
			stats_output = "%sAgility: %s\n" % (stats_output, self.playerInformation.agility)
		if (self.playerInformation.charisma != -1):
			stats_output = "%sCharisma: %s\n" % (stats_output, self.playerInformation.charisma)
		if (self.playerInformation.armor_level != -1):
			stats_output = "%sArmor Level: %s\n" % (stats_output, self.playerInformation.armor_level)
		if (self.playerInformation.current_weight != -1):
			stats_output = "%sCurrent Weight: %s\n" % (stats_output, self.playerInformation.current_weight)
		if (self.playerInformation.max_weight != -1):
			stats_output = "%sMaximum Weight: %s\n" % (stats_output, self.playerInformation.max_weight)
		if (self.playerInformation.current_bulk != -1):
			stats_output = "%sCurrent Bulk: %s\n" % (stats_output, self.playerInformation.current_bulk)
		if (self.playerInformation.max_bulk != -1):
			stats_output = "%sMaximum Bulk: %s\n" % (stats_output, self.playerInformation.max_bulk)

		if ("stats" in dir(self)):
			self.stats.statistics_textbox.delete_text(0, -1)
			self.stats.statistics_textbox.insert_defaults(stats_output)


	# Display Player's Inventory
	if (self.gameInformation.show_inventory):
		inventory_output = ""

		for each in self.playerInformation.items:

				if (self.itemData[each].equipped):
					# Item is equipped, so we want to display "(Equipped)" by its name in the inventory window
					inventory_output = "%s%s (Equipped)\n" % (inventory_output, self.itemData[each].name)
				else:
					# Item is not equipped
					inventory_output = "%s%s\n" % (inventory_output, self.itemData[each].name)
		if ("inventory" in dir(self)):
			self.inventory.inventory_textbox.delete_text(0, -1)
			self.inventory.inventory_textbox.insert_defaults(inventory_output)


	# Display Room Description
	if (self.gameInformation.show_text_output_area):
		if (not self.roomData[room].visited):
			output_text(self, self.roomData[room].description_long + "\n\n")
			output_text(self, self.roomData[room].direction_description + "\n\n")
			if (not self.gameInformation.debug_mode):
				self.roomData[room].visited = 1
		else:
			output_text(self, self.roomData[room].description_short + "\n\n")


	# Display Obstructions in Current Room
	for direction in self.roomData[ room ].direction.keys():
		obstruction_list = self.roomData[ room ].direction[direction].obstructions
		if (obstruction_list != None):
			# Convert string of comma-separated obstruction numbers into a list of integers
			obstruction_strings = string.split(obstruction_list, ', ')
			obstructions = []
			for each in obstruction_strings:
				if (self.obstructionData[ string.atoi(each) ].visible):
					obstructions.append(string.atoi(each))
			if (obstructions == []):
				break # we need to break if there are no visible obstructions in the current room

			# Setup the text to be displayed
			obstruction_output = "A"
			if ( string.lower(self.obstructionData[ obstructions[0] ].name)[0] in ['a', 'e', 'i', 'o', 'u'] ):
				obstruction_output = "%sn" % obstruction_output
			obstruction_output = "%s %s" % (obstruction_output, self.obstructionData[ obstructions[0] ].name)

			for current_obstruction in obstructions[1:]:
				obstruction_output = "%s, and a" % obstruction_output
				if ( string.lower(self.obstructionData[ current_obstruction ].name)[0] in ['a', 'e', 'i', 'o', 'u'] ):
					obstruction_output = "%sn" % obstruction_output
				obstruction_output = "%s %s" % (obstruction_output, self.obstructionData[ current_obstruction ].name)

			obstruction_output = "%s prevents you from moving %s." % (obstruction_output, self.directionData[ direction ].name)
			output_text(self, obstruction_output + "\n")


	# Display Items in Current Room
	item_list = self.roomData[ room ].items
	if (item_list != None):
		# Convert string of comman-separated item numbers into a list of integers
		item_strings = string.split(item_list, ', ')
		items = []
		for each in item_strings:
			items.append(string.atoi(each))

		# Setup the text to be displayed
		item_output = "Looking around, you see a"
		if ( string.lower(self.itemData[ items[0] ].name)[0] in ['a', 'e', 'i', 'o', 'u'] ):
			item_output = "%sn" % item_output
		item_output = "%s %s" % (item_output, self.itemData[ items[0] ].name)

		for current_item in items[1:]:
			item_output = "%s, and a" % item_output
			if ( string.lower(self.itemData[ current_item ].name)[0] in ['a', 'e', 'i', 'o', 'u'] ):
				item_output = "%sn" % item_output
			item_output = "%s %s" % (item_output, self.itemData[ current_item ].name)

		item_output = "%s." % item_output
		output_text(self, item_output + "\n")


#####################################################################

def parse_command_line(self, command):

	import string

	command_executed = 0

	# Print command to output window
	command = string.strip(command)
	output_text(self, "\n> " + command + "\n\n")
	if (self.gameInformation.debug_mode):
		print "\n> " + command + "\n"


	# Parse out Verb
	if ((command[-1] == ".") or (command[-1] == "!") or (command[-1] == "?")):
		command = command[:-1]

	verb = string.split(command, ' ')[0]
	verb = string.lower(verb)
	remainder = string.split(command, ' ')[1:]
	remainder = string.join(remainder, ' ')
	remainder = string.lower(remainder)


	# Hard-wired Verbs
	if ((verb == "help") or (verb == "verblist") or (verb == "listverbs")):
		display_verbs(self)
		command_executed = 1

	if ((verb == "quit") or (verb == "exit")):
		self.widget.play_togglebutton.set_active(0)

	# Check to see if the command is to move in a particular direction
	direction = resolve_direction_name(self, verb)

	if ((direction != 0) and (direction != 5)):
		move_in_direction(self, direction)
		command_executed = 1


	# Debug Mode Verbs
	if (self.gameInformation.debug_mode):
		if ( ((verb == "warp") or (verb == "xyzzy"))
			and not(remainder == "") ):
			room_warp(self, remainder)
			command_executed = 1

		if (verb == "execute"):
			execute_effect(self, remainder)
			display_room(self, self.playerInformation.current_room)
			command_executed = 1


	# User Defined Verbs
	if (not command_executed):
		verb = resolve_verb(self, verb) # if the command line's verb is an alias
		                                # we need to resolve it

	if (verb == "get"):
		get_item(self, remainder)
		display_room(self, self.playerInformation.current_room)
		command_executed = 1

	if (verb == "drop"):
		drop_item(self, remainder)
		display_room(self, self.playerInformation.current_room)
		command_executed = 1

	verb_list = []
	for each in self.verbData.keys():
		verb_list.append( string.lower(self.verbData[each].name) )

	if (not command_executed):
		if (verb in verb_list):
			objects = parse_command_line_objects( self, remainder )
			if (not objects == []): # current event grammer requires at least one object
				effect_string = resolve_event(self, verb, objects)
				if (not effect_string == None):
					execute_effect(self, effect_string)
					display_room(self, self.playerInformation.current_room)
				else:
					output_text(self, "\nYou can't do that.\n")
				command_executed = 1


	# More Hard-Wired Verbs

	if (not command_executed):
		if ( (remainder == "") and ( (verb == "look") or (verb == "l") ) ):
			temp_boolean = self.roomData[ self.playerInformation.current_room ].visited
			display_room(self, self.playerInformation.current_room)
			self.roomData[ self.playerInformation.current_room ].visited = temp_boolean
			command_executed = 1

	if (not command_executed):
		if ( (verb == "examine") or (verb == "ex") or (verb == "read") or (verb == "look") or (verb == "l") ):
			examine_object(self, remainder)
			command_executed = 1

	if ((verb == "last") or (verb == "repeat")):
		command_line_set_text(self, self.last_command)
		command = self.last_command
		command_executed = 1

	if (verb == "load"):
		load_game(self)
		command_executed = 1

	if (verb == "save"):
		save_game(self)
		command_executed = 1


	if (not command_executed):
		output_text(self, "I don't understand your command.\n")

	self.last_command = command


#####################################################################

def display_verbs(self):

	# This routine displays help information about the game,
	# in the form of a list of available verbs the player can use

	import string

	output_text(self, "Verbs build into the Cog Engine: ")
	output_text(self, "Look, Examine, Load, Save, Help, Quit")

	verb_list = []
	for each in self.verbData.keys():
		verb_list.append( string.lower(self.verbData[each].name) )

	# We don't want to show Get and Drop here if the game author
	# has overridden their usage
	show_get = ("get" in verb_list)
	show_drop = ("drop" in verb_list)

	if ((not show_get) and (not show_drop)):
		output_text(self, ", and Last.\n")
	if ((show_get) and (not show_drop)):
		output_text(self, ", Get, and Last.\n")
	if ((not show_get) and (show_drop)):
		output_test(self, ", Drop, and Last.\n")
	if ((show_get) and (show_drop)):
		output_text(self, ", Get, Drop, and Last.\n")

	if (self.gameInformation.debug_mode):
		output_text(self, "Available Debugging Verbs: Warp, and Execute.\n")

	# Finally we show the verbs the game author has added to the engine
	# (as long as either debug_mode or show_all_verbs is enabled'
	if ((self.gameInformation.debug_mode) or (self.gameInformation.show_all_verbs)):
		output_text(self, "Other Verbs in this game include: ")
		capitalized_verb_list = []
		for each in verb_list:
			capitalized_verb_list.append(string.capitalize(each))
		verb_list_output = string.join(capitalized_verb_list, ', ')
		and_index = string.rfind(verb_list_output, ', ')
		verb_list_output = verb_list_output[:and_index] + ', and' + verb_list_output[and_index+1:] + '.\n'
		output_text(self, verb_list_output)


#####################################################################

def move_in_direction(self, direction):

	# This method takes in the direction (as an integer) that the player would like
	# to move, and moves them into that room if they are allowed, otherwise
	# printing out an appropriate error message.

	import string

	# First we make sure that the direction the player wants to move in exists in this
	# room, and then we make sure the room the direction leads to is a legal room
	if ( (direction in self.roomData[ self.playerInformation.current_room ].direction.keys())
		and (self.roomData[ self.playerInformation.current_room ].direction[ direction ].to_which_room > 0)
		and (self.roomData[ self.playerInformation.current_room ].direction[ direction ].to_which_room <= len(self.roomData.keys()) ) ):


		# Check to see if path is obstructed
		if (self.roomData[ self.playerInformation.current_room ].direction[ direction ].obstructions != None):

			print "Obstructions: -%s-" % self.roomData[ self.playerInformation.current_room ].direction[ direction ].obstructions

			output_text(self, "You can't move ")
			output_text(self, string.capitalize(self.directionData[direction].name) )

			obstruction_list = string.split(self.roomData[ self.playerInformation.current_room ].direction[direction].obstructions, ', ')

			visible_obstructions = []
			for each in obstruction_list:
				obstruction = string.atoi(each)
				if (self.obstructionData[obstruction].visible):
					visible_obstructions.append(obstruction)

			if ( len(visible_obstructions) > 0 ):
				output_text(self, " because your path is blocked by a")

				obstruction_output_list = ""

				for each in visible_obstructions:
					temp_output = ""
					if (string.lower(self.obstructionData[each].name)[0] in ['a', 'e', 'i', 'o', 'u']):
						temp_output = "n"
					temp_output = temp_output + " " + self.obstructionData[each].name
					if ( len(visible_obstructions) != 1):
						if (each != visible_obstructions[-2]):
							if (each != visible_obstructions[-1]):
								temp_output = temp_output + ", a"
						else:
							temp_output = temp_output + ", and a"

					obstruction_output_list = obstruction_output_list + temp_output

				output_text(self, obstruction_output_list)

			output_text(self, ".\n\n")


		# Path is not obstructed
		else:

			output_text(self, "You move " + self.directionData[direction].name + ".\n\n")

			if ( (self.roomData[self.playerInformation.current_room].direction[direction].first_transition_text != None)
				and (self.roomData[self.playerInformation.current_room].direction[direction].first_transition_text != "")
				and (not self.roomData[self.playerInformation.current_room].direction[direction].has_moved_this_way) ):

				output_text(self, " " + self.roomData[self.playerInformation.current_room].direction[direction].first_transition_text + "\n")

			if ( (self.roomData[self.playerInformation.current_room].direction[direction].transition_text != None)
				and (self.roomData[self.playerInformation.current_room].direction[direction].transition_text != "") ):

				output_text(self, " " + self.roomData[self.playerInformation.current_room].direction[direction].transition_text + "\n")

			self.roomData[self.playerInformation.current_room].direction[direction].has_moved_this_way = 1

			# Set player's current room to the new room
			self.playerInformation.current_room = self.roomData[self.playerInformation.current_room].direction[direction].to_which_room


	# Direction does not exist, or does not lead to a legal room
	else:

		output_text(self, "You can't move ")
		output_text(self, string.capitalize(self.directionData[direction].name) )
		output_text(self, ".\n\n")


	display_room(self, self.playerInformation.current_room)


#####################################################################

def room_warp(self, new_room):

	# This method, otherwise known as the "Xyzzy feature" allows the player
	# to jump to any room in the game. The command line parser makes
	# sure that debug mode is enabled for this feature to be used

	import string

	if (self.roomData.has_key( string.atoi(new_room) ) ):
		self.playerInformation.current_room = string.atoi(new_room)
		display_room(self, self.playerInformation.current_room)
	else:
		output_text(self, "That is not a valid room number!\n")


#####################################################################

def execute_effect(self, effect):

	# ExecuteEffect works as a recursive method that executes an event's effect field.
	# The first effect found is executed, and if an "and" is found instead of a semicolon
	# at the end of that effect (indicating that another effect is supposed to take place)
	# the method recursively calls itself, feeding the new instance the remainder of the
	# current event's effect string. Damn I'm good.
	#
	# The effect string is split up into a list of words by whitespace.
	# We then examine the words one by own, removing them from the list as we go.

	import string

	if (self.gameInformation.debug_mode):
		effect_debug_display = string.split(effect, 'and ')[0]
		effect_debug_display = string.split(effect_debug_display, 'or ')[0]
		effect_debug_display = self.convert_reference_numbers_to_names(effect_debug_display)
		print "  Executing --> \"%s\"" % string.strip(effect_debug_display)

	effect_word_list = string.split(effect, ' ')

	word = effect_word_list[0]
	del(effect_word_list[0])

	if (word == "Adds"):
		word = effect_word_list[0]
		del(effect_word_list[0])

		if (word[0:4] == "Item"):
		# We're adding an Item

			item_number = string.atoi(word[5:-1])

			word = effect_word_list[0]
			del(effect_word_list[0])

			if ( (not(word == "Inventory")) and (not(word == "CurrentRoom")) \
			and (not(word[0:4] == "Room"))):
				# Skip the preposition
				word = effect_word_list[0]
				del(effect_word_list[0])

			if (word == "Inventory"):
				if ((self.gameInformation.debug_mode) and (item_number in self.playerInformation.items)):
					print "Warning! Player already has Item #%i in their inventory!" % item_number
				else:
					self.playerInformation.items.append(item_number)
			if (word == "CurrentRoom"):
				add_item_to_room(self, self.playerInformation.current_room, item_number)
			if (word[0:4] == "Room"):
				room_number = string.atoi(word[5:-1])
				add_item_to_room(self, room_number, item_number)

		elif (word[0:11] == "Obstruction"):
			# We're adding an Obstruction
			obstruction_number = string.atoi(word[12:-1])

			word = effect_word_list[0]
			del(effect_word_list[0])

			if ( not(word[0:4] == "Room")):
				# Skip the preposition
				word = effect_word_list[0]
				del(effect_word_list[0])

			if (word[0:4] == "Room"):
				room_number = string.split(word, '(')[1]
				room_number = string.split(room_number, ')')[0]
				room_number = string.atoi(room_number)

				direction_number = string.split(word, '(')[2]
				direction_number = string.split(direction_number, ')')[0]
				direction_number = string.atoi(direction_number)

				add_obstruction_to_room(self, room_number, direction_number, obstruction_number)

	if (word == "Removes"):
		word = effect_word_list[0]
		del(effect_word_list[0])

		if (word[0:4] == "Item"):
		# We're removing an Item

			item_number = string.atoi(word[5:-1])

			word = effect_word_list[0]
			del(effect_word_list[0])

			if ( (not(word == "Inventory")) and (not(word == "CurrentRoom")) \
			and (not(word[0:4] == "Room"))):
				# Skip the preposition
				word = effect_word_list[0]
				del(effect_word_list[0])

			if (word == "Inventory"):
				if ((self.gameInformation.debug_mode) and (item_number not in self.playerInformation.items)):
					print "Warning! Player did not have Item #%i in their inventory!" % item_number
				else:
					index = self.playerInformation.items.index(item_number)
					del(self.playerInformation.items[ index ])
			if (word == "CurrentRoom"):
				remove_item_from_room(self, self.playerInformation.current_room, item_number)
			if (word[0:4] == "Room"):
				room_number = string.atoi(word[5:-1])
				remove_item_from_room(self, room_number, item_number)

		elif (word[0:11] == "Obstruction"):
			# We're removing an Obstruction
			obstruction_number = string.atoi(word[12:-1])

			word = effect_word_list[0]
			del(effect_word_list[0])

			if ( not(word[0:4] == "Room")):
				# Skip the preposition
				word = effect_word_list[0]
				del(effect_word_list[0])

			if (word[0:4] == "Room"):
				room_number = string.split(word, '(')[1]
				room_number = string.split(room_number, ')')[0]
				room_number = string.atoi(room_number)

				direction_number = string.split(word, '(')[2]
				direction_number = string.split(direction_number, ')')[0]
				direction_number = string.atoi(direction_number)

				remove_obstruction_from_room_direction(self, room_number, direction_number, obstruction_number)

	if (word == "Modifies"):

		word = effect_word_list[0]
		del(effect_word_list[0])

		if (word == "Player"):
			word = effect_word_list[0]
			del(effect_word_list[0])

			expression = string.split(word, '[')[1]
			expression = string.split(expression, ']')[0]

			number = string.split(word, '(')[1]
			number = string.split(number, ')')[0]
			number = string.atoi(number)

			if (word[0:12] == "PlayerPoints"):
				self.playerInformation.points = evaluate_expression(self, expression, self.playerInformation.points, number)
			if (word[0:9] == "PlayerExp"):
				self.playerInformation.experience = evaluate_expression(self, expression, self.playerInformation.experience, number)
			if (word[0:8] == "PlayerHP"):
				self.playerInformation.hp = evaluate_expression(self, expression, self.playerInformation.hp, number)
			if (word[0:8] == "PlayerMP"):
				self.playerInformation.mp = evaluate_expression(self, expression, self.playerInformation.mp, number)
			if (word[0:9] == "PlayerStr"):
				self.playerInformation.strength = evaluate_expression(self, expression, self.playerInformation.strength, number)
			if (word[0:8] == "PlayerIQ"):
				self.playerInformation.intelligence = evaluate_expression(self, expression, self.playerInformation.intelligence, number)
			if (word[0:9] == "PlayerDex"):
				self.playerInformation.dexterity = evaluate_expression(self, expression, self.playerInformation.dexterity, number)
			if (word[0:10] == "PlayerAgil"):
				self.playerInformation.agility = evalutate_expression(self, expression, self.playerInformation.agility, number)
			if (word[0:14] == "PlayerCharisma"):
				self.playerInformation.charisma = evaluate_expression(self, expression, self.playerInformation.charisma, number)
			if (word[0:16] == "PlayerArmorLevel"):
				self.playerInformation.armor_level = evaluate_expression(self, expression, self.playerInformation.armor_level, number)
			if (word[0:19] == "PlayerCurrentWeight"):
				self.playerInformation.current_weight = evaluate_expression(self, expression, self.playerInformation.current_weight, number)

		if (word[0:4] == "Room"):

			room_number = string.split(word, '(')[1]
			room_number = string.split(room_number, ')')[0]
			room_number = string.atoi(room_number)

			word = effect_word_list[0]
			del(effect_word_list[0])

			if (word[0:21] == "TextDescription(Long)"):
				word = string.join(string.split(word, '[')[1:], '[') # Remove "TextDescription(Long)[" from word
				if ((word[:-1] == "null") or (word[:-1] == "")):
					new_description = None
				else:
					new_description = ""
					while (not word[-1] == "]"):
						new_description = "%s%s " % (new_description, word)
						word = effect_word_list[0]
						del(effect_word_list[0])
					new_description = "%s%s" % (new_description, word[:-1])
				self.roomData[room_number].description_long = new_description

			if (word[0:22] == "TextDescription(Short)"):
				word = string.join(string.split(word, '[')[1:], '[') # Remove "TextDescription(Short)[" from word
				if ((word[:-1] == "null") or (word[:-1] == "")):
					new_description = None
				else:
					new_description = ""
					while (not word[-1] == "]"):
						new_description = "%s%s " % (new_description, word)
						word = effect_word_list[0]
						del(effect_word_list[0])
					new_description = "%s%s" % (new_description, word[:-1])
				self.roomData[room_number].description_short = new_description

			if (word[0:20] == "DirectionDescription"):
				word = string.join(string.split(word, '[')[1:], '[') # Remove "DirectionDescription[" from word
				if ((word[:-1] == "null") or (word[:-1] == "")):
					new_description = None
				else:
					new_description = ""
					while (not word[-1] == "]"):
						new_description = "%s%s " % (new_description, word)
						word = effect_word_list[0]
						del(effect_word_list[0])
					new_description = "%s%s" % (new_description, word[:-1])
				self.roomData[room_number].direction_description = new_description

			if (word[0:10] == "GraphicURL"):
				word = string.join(string.split(word, '[')[1:], '[') # Remove "GraphicURL[" from word
				if ((word[:-1] == "null") or (word[:-1] == "")):
					new_url = None
				else:
					new_url = ""
					while (not word[-1] == "]"):
						new_url = "%s%s " % (new_url, word)
						word = effect_word_list[0]
						del(effect_word_list[0])
					new_url = "%s%s" % (new_url, word[:-1])
					if (self.gameInformation.debug_mode):
						print "Setting GraphicURL for Room #%i to \"%s\"" % (room_number, new_url)
				self.roomData[room_number].graphic_url = new_url

			if (word[0:7] == "Visited"):
				boolean = ((word[-6:] == "(true)") or (word[-3:] == "(1)"))
				self.roomData[room_number].visited = boolean

			if (word[0:15] == "DirectionObject"):

				direction_number = string.split(word, '(')[1]
				direction_number = string.split(direction_number, ')')[0]
				direction_number = string.atoi(direction_number)

				word = string.join(string.split(word, ')')[1:], ')') # remove "DirectionObject<Ref> from word

				if (word[0:11] == "ToWhichRoom"):
					to_which_room = string.split(word, '(')[1]
					to_which_room = string.split(to_which_room, ')')[0]
					to_which_room = string.atoi(to_which_room)

					if (to_which_room == 0):
						del(self.roomData[room_number].direction[direction_number])
					else:
						if (not self.roomData[room_number].direction.has_key(direction_number)):
							self.roomData[room_number].direction[direction_number] = self.DirectionObject()

						self.roomData[room_number].direction[direction_number].to_which_room = to_which_room

				if ((word[0:19] == "FirstTransitionText") and (self.roomData[room_number].direction.has_key(direction_number))):
					word = string.join(string.split(word, '[')[1:], '[') # Remove "FirstTransitionText[" from word
					if ((word[:-1] == "null") or (word[:-1] == "")):
						new_text = None
					else:
						new_text = ""
						while (not word[-1] == "]"):
							new_text = "%s%s " % (new_text, word)
							word = effect_word_list[0]
							del(effect_word_list[0])
						new_text = "%s%s" % (new_text, word[:-1])
					self.roomData[room_number].direction[direction_number].first_transition_text = new_text

				if ((word[0:14] == "TransitionText") and (self.roomData[room_number].direction.has_key(direction_number))):
					word = string.join(string.split(word, '[')[1:], '[') # Remove "TransitionText[" from word
					if ((word[:-1] == "null") or (word[:-1] == "")):
						new_text = None
					else:
						new_text = ""
						while (not word[-1] == "]"):
							new_text = "%s%s " % (new_text, word)
							word = effect_word_list[0]
							del(effect_word_list[0])
						new_text = "%s%s" % (new_text, word[:-1])
					self.roomData[room_number].direction[direction_number].transition_text = new_text

				if ((word[0:22] == "FirstTransitionGraphic") and (self.roomData[room_number].direction.has_key(direction_number))):
					word = string.join(string.split(word, '[')[1:], '[') # Remove "FirstTransitionGraphic[" from word
					if ((word[:-1] == "null") or (word[:-1] == "")):
						new_url = None
					else:
						new_url = ""
						while (not word[-1] == "]"):
							new_url = "%s%s " % (new_url, word)
							word = effect_word_list[0]
							del(effect_word_list[0])
						new_url = "%s%s" % (new_url, word[:-1])
					self.roomData[room_number].direction[direction_number].first_transition_graphic = new_url

				if ((word[0:17] == "TransitionGraphic") and (self.roomData[room_number].direction.has_key(direction_number))):
					word = string.join(string.split(word, '[')[1:], '[') # Remove "TransitionGraphic[" from word
					if ((word[:-1] == "null") or (word[:-1] == "")):
						new_url = None
					else:
						new_url = ""
						while (not word[-1] == "]"):
							new_url = "%s%s " % (new_url, word)
							word = effect_word_list[0]
							del(effect_word_list[0])
						new_url = "%s%s" % (new_url, word[:-1])
					self.roomData[room_number].direction[direction_number].transition_graphic = new_url

				if ((word[0:15] == "HasMovedThisWay") and (self.roomData[room_number].direction.has_key(direction_number))):
					boolean = ((word[-6:] == "(true)") or (word[-3:] == "(1)"))
					self.roomData[room_number].direction[direction_number].has_moved_this_way = boolean

		if (word[0:4] == "Item"):

			item_number = string.split(word, '(')[1]
			item_number = string.split(item_number, ')')[0]
			item_number = string.atoi(item_number)

			word = effect_word_list[0]
			del(effect_word_list[0])

			if (word[0:8] == "Equipped"):
				boolean = ((word[-6:] == "(true)") or (word[-3:] == "(1)"))
				self.itemData[item_number].equipped = boolean

			if (word[0:6] == "Weight"):
				weight = string.split(word, '(')[1]
				weight = string.split(weight, ')')[0]
				weight = string.atoi(weight)
				self.itemData[item_number].weight = weight

			if (word[0:4] == "Bulk"):
 				bulk = string.split(word, '(')[1]
				bulk = string.split(bulk, ')')[0]
				bulk = string.atoi(bulk)
				self.itemData[item_number].bulk = bulk

			if (word[0:15] == "TextDescription"):
				word = string.join(string.split(word, '[')[1:], '[') # Remove "TextDescription[" from word
				if ((word[:-1] == "null") or (word[:-1] == "")):
					new_description = None
				else:
					new_description = ""
					while (not word[-1] == "]"):
						new_description = "%s%s " % (new_description, word)
						word = effect_word_list[0]
						del(effect_word_list[0])
					new_description = "%s%s" % (new_description, word[:-1])
				self.itemData[item_number].description = new_description

			if (word[0:22] == "Environment_GraphicURL"):
				word = string.join(string.split(word, '[')[1:], '[') # Remove "Environment_GraphicURL[" from word
				if ((word[:-1] == "null") or (word[:-1] == "")):
					new_url = None
				else:
					new_url = ""
					while (not word[-1] == "]"):
						new_url = "%s%s " % (new_url, word)
						word = effect_word_list[0]
						del(effect_word_list[0])
					new_url = "%s%s" % (new_url, word[:-1])
				self.itemData[item_number].environment_graphic_url = new_url

			if (word[0:22] == "Environment_GraphicPos"):
				word = effect_word_list[0]
				del(effect_word_list[0])
				x = string.split(word, ',')[0]
				x = string.atoi(x)

				word = effect_word_list[0]
				del(effect_word_list[0])
				y = string.split(word, ',')[0]
				y = string.atoi(x)

				word = effect_word_list[0] # word should now be pointed to ")"
				del(effect_word_list[0])

				self.itemData[item_number].environment_graphic_Xpos = x
				self.itemData[item_number].environment_graphic_Ypos = y

			if (word[0:18] == "CloseUp_GraphicURL"):
				word = string.join(string.split(word, '[')[1:], '[') # Remove "CloseUp_GraphicURL[" from word
				if ((word[:-1] == "null") or (word[:-1] == "")):
					new_url = None
				else:
					new_url = ""
					while (not word[-1] == "]"):
						new_url = "%s%s " % (new_url, word)
						word = effect_word_list[0]
						del(effect_word_list[0])
					new_url = "%s%s" % (new_url, word[:-1])
				self.itemData[item_number].closeup_graphic_url = new_url

			if (word[0:15] == "Icon_GraphicURL"):
				word = string.join(string.split(word, '[')[1:], '[') # Remove "Icon_GraphicURL[" from word
				if ((word[:-1] == "null") or (word[:-1] == "")):
					new_url = None
				else:
					new_url = ""
					while (not word[-1] == "]"):
						new_url = "%s%s " % (new_url, word)
						word = effect_word_list[0]
						del(effect_word_list[0])
					new_url = "%s%s" % (new_url, word[:-1])
				self.itemData[item_number].icon_graphic_url = new_url

			if (word[0:19] == "Equipped_GraphicURL"):
				word = string.join(string.split(word, '[')[1:], '[') # Remove "Equipped_GraphicURL[" from word
				if ((word[:-1] == "null") or (word[:-1] == "")):
					new_url = None
				else:
					new_url = ""
					while (not word[-1] == "]"):
						new_url = "%s%s " % (new_url, word)
						word = effect_word_list[0]
						del(effect_word_list[0])
					new_url = "%s%s" % (new_url, word[:-1])
				self.itemData[item_number].equipped_graphic_url = new_url

		if (word[0:11] == "Obstruction"):

			obstruction_number = string.split(word, '(')[1]
			obstruction_number = string.split(item_number, ')')[0]
			obstruction_number = string.atoi(item_number)

			word = effect_word_list[0]
			del(effect_word_list[0])

			if (word[0:7] == "Visible"):
				boolean = ((word[-6:] == "(true)") or (word[-3:] == "(1)"))
				self.obstructionData[obstruction_number].visible = boolean

			if (word[0:15] == "TextDescription"):
				word = string.join(string.split(word, '[')[1:], '[') # Remove "TextDescription[" from word
				if ((word[:-1] == "null") or (word[:-1] == "")):
					new_description = None
				else:
					new_description = ""
					while (not word[-1] == "]"):
						new_description = "%s%s " % (new_description, word)
						word = effect_word_list[0]
						del(effect_word_list[0])
					new_description = "%s%s" % (new_description, word[:-1])
				self.obstructionData[obstruction_number].description = new_description

			if (word[0:22] == "Environment_GraphicURL"):
				word = string.join(string.split(word, '[')[1:], '[') # Remove "Environment_GraphicURL[" from word
				if ((word[:-1] == "null") or (word[:-1] == "")):
					new_url = None
				else:
					new_url = ""
					while (not word[-1] == "]"):
						new_url = "%s%s " % (new_url, word)
						word = effect_word_list[0]
						del(effect_word_list[0])
					new_url = "%s%s" % (new_url, word[:-1])
				self.obstructionData[obstruction_number].environment_graphic_url = new_url

			if (word[0:22] == "Environment_GraphicPos"):
				word = effect_word_list[0]
				del(effect_word_list[0])
				x = string.split(word, ',')[0]
				x = string.atoi(x)

				word = effect_word_list[0]
				del(effect_word_list[0])
				y = string.split(word, ',')[0]
				y = string.atoi(x)

				word = effect_word_list[0] # word should now be pointed to ")"
				del(effect_word_list[0])

				self.obstructionData[obstruction_number].environment_graphic_Xpos = x
				self.obstructionData[obstruction_number].environment_graphic_Ypos = y

			if (word[0:18] == "CloseUp_GraphicURL"):
				word = string.join(string.split(word, '[')[1:], '[') # Remove "CloseUp_GraphicURL[" from word
				if ((word[:-1] == "null") or (word[:-1] == "")):
					new_url = None
				else:
					new_url = ""
					while (not word[-1] == "]"):
						new_url = "%s%s " % (new_url, word)
						word = effect_word_list[0]
						del(effect_word_list[0])
					new_url = "%s%s" % (new_url, word[:-1])
				self.obstructionData[obstruction_number].closeup_graphic_url = new_url


	if (word[0:11] == "TextMessage"):

		word = string.join(string.split(word, '[')[1:], '[') # Remove "TextMessage[" from word

		while (not word[-1] == "]"):
			output_text(self, word + " ")
			word = effect_word_list[0]
			del(effect_word_list[0])

		output_text(self, word[:-1] + "\n\n")

	if (word[0:14] == "GraphicMessage"):

		image_file = word[15:-2] # the -2 removes the comma

		word = effect_word_list[0]
		del(effect_word_list[0])

		x = string.atoi(word[:-1])

		word = effect_word_list[0]
		del(effect_word_list[0])

		y = string.atoi(word[:-1])

		display_image(self, image_file, x, y)


	# The following sequence makes to the recursive call to execute_effect if there
	# are more Effects for this Event.

	if (effect_word_list != []):
		word = effect_word_list[0]
		del(effect_word_list[0])

		if (string.lower(word) == "and"):
			remainder = string.join(effect_word_list, ' ')

			execute_effect(self, remainder)


#####################################################################

def resolve_verb(self, user_verb):

	# This method will take in a verb the user has entered on the command line
	# and check to see if it is the alias of one of the game's verbs.
	# If the user's verb directly matches a game's verb, the game's verb is
	# returned, and aliases are not checked

	import string

	user_verb = string.lower(user_verb)

	verb = ""

	verb_list = []
	for each in self.verbData.keys():
		verb_list.append( string.lower(self.verbData[each].name) )

	if (not (user_verb in verb_list)):
		for each in self.verbData.keys():
			lowercase_alias_string = string.lower(self.verbData[each].aliases)
			alias_list = string.split( lowercase_alias_string, ', ')

			if (user_verb in alias_list):

				if (verb == ""):
					verb = string.lower(self.verbData[each].name)

				elif (self.gameInformation.debug_mode):
					# We want to print out an error message if more than one verb has
					# the same alias

					print "Warning! Multiple matching verb aliases detected!"


	# If the user's verb does not match an alias, or if the user's verb
	# *directly* matches a verb name, we're going to return the user's verb
	if (verb == ""):
		verb = user_verb

	return(verb)


#####################################################################

def resolve_direction_name(self, direction):

	# This method takes in the name of a direction as a string,
	# and returns the corresponding direction number as an integer
	# (if a match exists, otherwise it returns 0)

	import string

	direction_number = 0

	direction = string.lower(direction)

	for each in self.directionData.keys():
		if ( (direction == string.lower(self.directionData[each].name)) or
			(direction == string.lower(self.directionData[each].abbreviation)) ):
			direction_number = self.directionData[each].number
			break

	return(direction_number)


#####################################################################

def get_item(self, item_name):

	#   This Action begins by searching to see if you are referring to a legal itemname.
	# The "Name" field of all Items is searched first, followed by the "Aliases" field.
	# In the case that two permissable aliases are found, an error is returned, prompting
	# the Player for more specific input. Next, the Player's Current Room is searched
	# to make sure that the item exists in it. Finally, the "Get" Action's Event Array
	# is searched (if it exists) to see if some Event other than the default should occur.
	# If there is no such exception, the default Event is to add the item to the Player's
	# Inventory, and remove the item from the Current Room.

	import string
	item_number = 0
	get_all = 0
	ok_to_pick_up = 1

	# Call get_item recursively if user is electing to get all items in the current room
	if ( (item_name == "all") or (item_name == "everything") ):
		get_all = 1
		if (self.roomData[self.playerInformation.current_room].items == None):
			item_number = -2 # this number will be used later to generate a specific error message
		else:
			for each in string.split(self.roomData[self.playerInformation.current_room].items, ', '):
				if (self.gameInformation.debug_mode):
					print "Getting %s" % self.itemData[string.atoi(each)].name
					print "Current Room contains: %s" % self.roomData[self.playerInformation.current_room].items
				get_item(self, self.itemData[ string.atoi(each) ].name)

	if (item_number != -2):
		item_number = resolve_item_name( self, item_name, "CurrentRoom")
	if ((item_number == 0) and not (get_all)):
		item_number = find_item_alias( self, item_name, "CurrentRoom")


	# We have figured out which item the player is talking about (whether they referred to it
	# by a name or by an alias), and now decide which action to take

	if (self.gameInformation.debug_mode):
		print "Item Number: %i" % item_number

	if (item_number == 0):
		if (not get_all): # (We don't want to display this if the player wants to "get all")
			output_text(self, "You don't see anything like that here.\n\n")

	elif (item_number == -1):
		output_text(self, "I'm not certain precisely what you are referring to. Please be more specific.\n\n")

	elif (item_number == -2):
		output_text(self, "There's nothing to get in this room.\n\n")

	else:

		object_list = [["Item", item_number]]
		effect_string = resolve_event(self, "Get", object_list)

		if (effect_string != None):
			# An Event exists for this Item
			execute_effect( self, effect_string )

		else:
			# No Event exists for this Item, so we execute the default Actions

			if ( self.itemData[item_number].weight == -1 ):
				output_text(self, "You can't pick up the %s.\n\n" % self.itemData[item_number].name)
				ok_to_pick_up = 0

			if ( ( self.playerInformation.max_weight != -1) and ( self.itemData[item_number].weight + self.playerInformation.current_weight > self. playerInformation.max_weight) ):
				output_text(self, "The %s is too heavy for you to pick up.\n\n" % self.itemData[item_number].name)
				ok_to_pick_up = 0

			if ( ( self.playerInformation.max_bulk != -1) and ( self.itemData[item_number].bulk + self.playerInformation.current_bulk > self.playerInformation.max_bulk) ):
				output_text(self, "The %s is to bulk for you to carry." % self.itemData[item_number].name)
				ok_to_pick_up = 0

			if ( ok_to_pick_up):
				if ( (self.gameInformation.debug_mode) and ( item_number in self.playerInformation.items ) ):
					print "Warning! Player's Inventory already includes Item #%i (%s)!" % (item_number, self.itemData[item_number].name)
				output_text(self, "You pick up the %s.\n\n" % self.itemData[item_number].name)

				remove_item_from_room( self, self.playerInformation.current_room, item_number)
				self.playerInformation.items.append(item_number)

				if (self.playerInformation.max_weight != -1):
					self.playerInformation.weight = self.playerInformation.weight + self.itemData[item_number].weight

				if (self.playerInformation.max_bulk != -1):
					# We allow items to have negative bulk, to represent containers.
					# Picking up a container with negative bulk actually increases the player's available bulk!
					self.playerInformation.bulk = self.playerInfromation.bulk + self.itemData[item_number].bulk


#####################################################################

def drop_item(self, item_name):

	#   This Action begins by searching to see if you are referring to a legal itemname.
	# The "Name" field of all Items is searched first, followed by the "Aliases" field.
	# In the case that two permissable aliases are found, an error is returned, prompting
	# the Player for more specific input. Next, the Player's Inventory is searched
	# to make sure that the item exists in it. Finally, the "Drop" Action's Event Array
	# is searched (if it exists) to see if some Event other than the default should occur.
	# If there is no such exception, the default Event is to remove the item from the Player's
	# Inventory, and add the item to the Current Room.
	#
	# Note: If a special event should be executed whenever an item is de-eqipped,
	# it will not necessarily be executed when the item is dropped. Under such
	# circumstances, the best thing to do is to write a "drop" even which includes
	# an item-equipped requirement

	item_number = 0
	drop_all = 0

	if (self.playerInformation.items == []):
		item_number = -2 # this number will be used later to generate a specific error message

	# Call drop_item recursively if user is electing to get all items in the current room
	if ( (item_name == "all") or (item_name == "everything") ):
		drop_all = 1
		item_list = self.playerInformation.items[:] # We make a duplicate list because we delete items by index during the recursive calls
		for each in item_list:
			if (self.gameInformation.debug_mode):
				print "Dropping %s" % self.itemData[each].name
			drop_item(self, self.itemData[each].name)

	if (item_number != -2):
		item_number = resolve_item_name( self, item_name, "Inventory")
	if ((item_number == 0) and not (drop_all)):
		item_number = find_item_alias( self, item_name, "Inventory")


	# We have figured out which item the player is talking about (whether they referred to it
	# by a name or by an alias), and now decide which action to take

	if (item_number == 0):
		if (not drop_all): # We don't want to display this if we are dropping all
			output_text(self, "You don't have anything like that in your inventory.\n\n")

	elif (item_number == -1):
		output_text(self, "I'm not sure precisely what you are referring to. Please be more specific.\n\n")

	elif (item_number == -2):
		output_text(self, "You don't have anything in your inventory to drop!\n\n")

	else:

		effect_string = resolve_event( self, "Drop", [["Item", item_number]] )

		if (effect_string != None):
			# An Event exists for this Item
			execute_effect( self, effect_string )

		else:
			# No Event exists for this Item, so we execute the default Actions

			if (self.itemData[item_number].equipped):
				self.itemData[item_number].eqipped = 0
				output_text(self, "You de-equip the %s.\n\n" % self.itemData[item_number].name)

			output_text(self, "You drop the %s.\n\n" % self.itemData[item_number].name)

			add_item_to_room( self, self.playerInformation.current_room, item_number )
			del self.playerInformation.items[ self.playerInformation.items.index( item_number ) ]


#####################################################################

def room_contains_item(self, room_number, item_number):

	# This function checks to see if a particular item is located in a particular room
	# The function returns 1 if the item is in the room, 0 if it is not

	import string

	item_exists_in_room = 0

	if (self.roomData[room_number].items != None):
		for each in string.split(self.roomData[room_number].items, ', '):
			if (item_number == string.atoi(each)):
				item_exists_in_room = 1

	return(item_exists_in_room)


#####################################################################

def room_contains_obstruction(self, room_number, obstruction_number):

	# This fuction checks to see if a particular obstruction is located
	# in a particular room

	import string

	obstruction_exists_in_room = 0

	for direction in self.roomData[room_number].direction:
		if (self.roomData[room_number].direction[direction].obstructions != None):
			obstruction_list = string.split(self.roomData[room_number].direction[direction].obstructions, ', ')
			for obstruction in obstruction_list:
				if (obstruction == ("%i" % obstruction_number)):
					obstruction_exists_in_room = 1

	return(obstruction_exists_in_room)

#####################################################################

def room_direction_contains_obstruction(self, room_number, direction_number, obstruction_number):

	# This fuction checks to see if a particular obstruction is located
	# in a particular direction of a particular room

	import string

	obstruction_exists_in_room_direction = 0

	if (self.roomData[room_number].direction[direction_number].obstructions != None):
		obstruction_list = string.split(self.roomData[room_number].direction[direction_number].obstructions, ', ')
		for obstruction in obstruction_list:
			if (obstruction == ("%i" % obstruction_number)):
				obstruction_exists_in_room = 1

	return(obstruction_exists_in_room_direction)


#####################################################################

def resolve_item_name(self, item_name, location):

	# This functions takes in a name of an item and returns the
	# item's number if the item exists in the location specified
	# Returns 0 if no matching items are found

	import string

	item_number = 0
	item_found = 0

	item_name = string.lower(item_name)

	for each in self.itemData.keys():
		if ( item_name == string.lower(self.itemData[each].name) ):

			# We've found a matching name for the item
			# Now we much check to see if the location is correct

			# Search Current Room
			if ( (location == "CurrentRoom") and
			     (room_contains_item( self, self.playerInformation.current_room, each) ) ):
#				if (self.gameInformation.debug_mode):
#					print "Item \"" + self.itemData[each].name + "\" found."
				if ( (self.gameInformation.debug_mode) and (item_found) ):
					print "Item #%i and Item #%i have duplicate names!" % (each, item_number)
				else:
					item_found = 1
					item_number = each

			# Search Inventory
			if ( (location == "Inventory") and
			     (each in self.playerInformation.items) ):
				if (self.gameInformation.debug_mode):
					print "Item \"" + self.itemData[each].name + "\" found."
				if ( (self.gameInformation.debug_mode) and (item_found) ):
					print "Item #%i and Item #%i have duplicate names!" % (each, item_number)
				else:
					item_found = 1
					item_number = each

			# location "ItemArray" didn't appear to be used in Java version of Cog Engine
			# so it has not been recoded

	return(item_number)


#####################################################################

def resolve_obstruction_name(self, obstruction_name, location):

	# This functions takes in a name of an obstruction and returns the
	# obstruction's number if the obstruction exists in the location specified
	#
	# returns obstructions number if a match is found
	# retuns 0 if no matching obstructions are found

	import string

	obstruction_number = 0
	found_obstruction = 0

	for each in self.obstructionData:
		if (string.lower(obstruction_name) == string.lower(self.obstructionData[each].name)):
			# We've found the matching obstruction, now we need to verify that
			# it is in the correct location

			if ((location == "CurrentRoom") and (room_contains_obstruction( self, self.playerInformation.current_room, each) ) ):
				if (self.gameInformation.debug_mode):
					print "Obstruction \"" + self.obstructionData[each].name + "\" found."
				if ( (self.gameInformation.debug_mode) and (found_obstruction) ):
					print "Obstruction #%i and Obstruction #%i have duplicate names!" % (obstruction_number, each)
				else:
					found_obstruction = 1
     				obstruction_number = each

			# location "ObstructionArray" didn't appear to be used in Java version of Cog Engine
			# so it has not been recoded

	return(obstruction_number)


#####################################################################

def find_item_alias(self, item_name, location):

	# location determines whether to search the current room or all items for an alias match
	# returns 0 if item_name does not match an alias
	# returns -1 if item_name matches multiple aliases
	# returns item number of legitimate item

	import string

	item_number = 0
	item_found = 0

	item_name = string.lower(item_name)

	if (self.gameInformation.debug_mode):
		print "Searching %s for Item with Alias \"%s\"" % (location, item_name)

	for item in self.itemData.keys():
		if (self.itemData[item].aliases != ""):

			for alias in string.split(self.itemData[item].aliases, ', '):

				if (string.lower(alias) == item_name):

					# We've found a matching Alias for the current item
					# Now we must check to see if the location is correct

					# Search Current Room
					if (location == "CurrentRoom"):
						if ( not(item_found) and room_contains_item( self, self.playerInformation.current_room, item) ):
							if (self.gameInformation.debug_mode):
								print "Item \"%s\" found." % self.itemData[item].name
							item_found = 1
							item_number = item
						else:
							if (room_contains_item( self, self.playerInformation.current_room, item) ):
								# More than one items in the current room have the same alias
								if (self.gameInformation.debug_mode):
									print "More than one items in the current room have this alias!"
								item_number = -1

					if (location == "Inventory"):
						if ( not(item_found) and (item in self.playerInformation.items)):
							if (self.gameInformation.debug_mode):
								print "Item \"%s\" found." % self.itemData[item].name
							item_found = 1
							item_number = item
						else:
							if (room_contains_item( self, self.playerInformation.current_room, item) ):
								# More than one items in the current room have the same alias
								if (self.gameInformation.debug_mode):
									print "More than one items in the player's inventory have this alias!"
								item_number = -1

					# location "ItemArray" didn't appear to be used in Java version of Cog Engine
					# so it has not been recoded

	return(item_number)


#####################################################################

def find_obstruction_alias(self, obstruction_name, location):

	# location determines whether to search the current room or all obstructions for an alias match
	# returns 0 if obstruction_name does not match an alias
	# returns -1 if obstruction_name matches multiple aliases
	# returns obstruction number of legitimate item

	import string

	obstruction_number = 0
	obstruction_found = 0

	if (self.gameInformation.debug_mode):
		print "Searching %s for Obstruction with Alias \"%s\"" % (location, obstruction_name)

	for obstruction in self.obstructionData:
		if (self.obstructionData[obstruction].aliases != None):

			for alias in string.split(self.obstructionData[obstruction].aliases, ', '):

				if (string.lower(obstruction_name) == string.lower(alias)):

					# We've found a matching alias for the current obstruction
					# Now we must check to see if the location is correct

					if (location == "CurrentRoom"):

						if ((not obstruction_found) and room_contains_obstruction(self, self.playerInformation.current_room, obstruction) ):

							if (self.gameInformation.debug_mode):
								print "Obstruction \"%s\" found." % self.obstructionData[obstruction].name

							obstruction_found = 1
							obstruction_number = obstruction

						else:
							if ( room_contains_obstruction( self, self.playerInformation.current_room, obstruction) ):
								# More than one obstructions in the current room have the same alias

								if (self.gameInformation.debug_mode):
									print "More than one obstructions in the Current Room have this Alias!"

								obstruction_number = -1


					# location "ObstructionArray" didn't appear to be used in Java version of Cog Engine
					# so it has not been recoded


	return(obstruction_number)


#####################################################################

def add_item_to_room(self, room_number, item_number):

	# This method takes in a room number and an item number,
	# and adds the item to that room

	if (self.roomData[room_number].items == None):
		self.roomData[room_number].items = "%i" % item_number
	else:
		if ( (self.gameInformation.debug_mode) and (room_contains_item( self, room_number, item_number)) ):
			print "Warning! Room #%i already includes Item #%i!" % (room_number, item_number)
		else:
			self.roomData[room_number].items = "%s, %i" % ( self.roomData[room_number].items, item_number )


#####################################################################

def add_obstruction_to_room(self, room_number, direction_number, obstruction_number):

	# This method takes in a room number, a direction number, and an obstruction
	# number, and adds the obstruction the that room's direction

	new_obstruction_list = ""

	if (direction_number not in self.roomData[room_number].direction.keys()):
		self.roomData[room_number].direction[direction_number] = self.DirectionObject()

	if ((self.gameInformation.debug_mode) and (room_direction_contains_obstruction(self, room_number, direction_number, obstruction_number))):
		print "Warning! Room #%i already contains Obstruction #%i in Direction #%i!" % (room_number, obstruction_number, direction_number)
	else:
		if (self.roomData[room_number].direction[direction_number].obstructions == None):
			# If there's no obstruction in the current room's direction, we will add the new obstruction's number
			self.roomData[room_number].direction[direction_number].obstructions = "%s" % obstruction_number
		else:
			# If there's already at least one obstruction in the current room's direction, we append the new one to the list
			self.roomData[room_number].direction[direction_number].obstructions = "%s, %i" % (self.roomData[room_number].direction[direction_number].obstructions, obstruction_number)


#####################################################################

def remove_item_from_room(self, room_number, item_number):

	# This method takes in a room number and an item number, and removes
	# the item from that room

	import string

	new_item_list = ""

	if (self.roomData[room_number].items != None):
		room_item_list = string.split(self.roomData[room_number].items, ', ')

		for each in room_item_list:
			if (each != "%i" % item_number):
				new_item_list = "%s%s, " % (new_item_list, each)

		new_item_list = new_item_list[:-2] # remove trailing ", "

	if (new_item_list == ""):
		new_item_list = None

	self.roomData[room_number].items = new_item_list


#####################################################################

def remove_obstruction_from_room_direction(self, room_number, direction_number, obstruction_number):

	# This method takes in room number, a direction number, and an obstruction
	# number, and remove the obstruction from that room's direction

	import string

	new_obstruction_list = ""

	if (self.roomData[room_number].direction.has_key(direction_number)):

		if (self.roomData[room_number].direction[direction_number].obstructions != None):

			obstruction_list = string.split(self.roomData[room_number].direction[direction_number].obstructions, ', ')

			for each in obstruction_list:
				if (each != "%i" % obstruction_number):
					new_obstruction_list = "%s%s, " % (new_obstruction_list, each)

			new_obstruction_list = new_obstruction_list[:-2] # remove trailing ", "

			if (new_obstruction_list == ""):
				new_obstruction_list = None

			self.roomData[room_number].direction[direction_number].obstructions = new_obstruction_list

		elif (self.gameInformation.debug_mode):
			print "Warning! Attempted to remove non-existant Obstruction #%i from Room #%i, Direction #%i." % (obstruction_number, room_number, direction_number)


#####################################################################

def parse_command_line_objects(self, remainder):

	# This method takes in the remainder of a command line (all words
	# after the first one, which is considered the verb), and parses
	# out a maximum of two object names/aliases by passing calls to
	# the parse_object method
	#
	# parse_command_line_objects returns a list of objects (if any are found)
	# which are themselves a list containing an object type in the first field
	# and the number of the object in the second (see parse_object for more info.

	command_line_objects_list = []

	object1 = parse_object(self, remainder, "Beginning")

	if (object1 != None):
		if (self.gameInformation.debug_mode):
			print "Object1 = %s(%i)" % (object1[0], object1[1])

		command_line_objects_list.append(object1)


	object2 = parse_object(self, remainder, "End-Exclusive") # see note in parse_objects comments for more information about "End-Exclusive"

	if (object2 != None):
		if (self.gameInformation.debug_mode):
			print "Object2 = %s(%i)" % (object2[0], object2[1])

		command_line_objects_list.append(object2)

	if (self.gameInformation.debug_mode):
		print "CMO:",
		print command_line_objects_list

	return( command_line_objects_list )


#####################################################################

def parse_object(self, phrase, search_focus):

	# parse_object takes in the string "phrase" and checks to see if
	# the whole string matches and obstruction's name (in the current room).
	# If not, it checks the whole string against the names of items (in both
	# the current room and the player's inventory). If nothing is found,
	# the one word from "phrase" is removed, (according to the search_focus)
	# and the process begins again.
	#
	# Note: If we the search_focus is set to "End-Exclusive" then a match will not be
	# made on the entire phrase. This is because when this method is called by
	# the parse_command_line_objects method, we don't want to think that a single
	# object name is actually two separate objects.
	#
	# parse_object returns a list of two items
	# The first item is a string declaring the object type
	# of the parsed object. The second item is the
	# cooresponding number of the object.

	import string

	object_list = None
	object_found = 0
	scratch = phrase[:]

	# "End-Exclusive Work-Around (see above comments)
	if (search_focus == "End-Exclusive"):
		scratch_word_list = string.split(scratch, ' ')
		scratch = string.join(scratch_word_list[1:], ' ')

	if (self.gameInformation.debug_mode):
		print "Searching: \"" + scratch + "\""

	while ((scratch != "") and not(object_found)):

		# Check Obstructions
		object_number = resolve_obstruction_name(self, scratch, "CurrentRoom")
		if (object_number == 0):
			object_number = find_obstruction_alias(self, scratch, "CurrentRoom")
		if (object_number > 0):
			# We've found a non-duplicate obstruction in the current room
			object_found = 1
			object_list = ["Obstruction", object_number]

		# Check Items
		if (object_number == 0):
			object_number = resolve_item_name(self, scratch, "CurrentRoom")
		if (object_number == 0):
			object_number = resolve_item_name(self, scratch, "Inventory")
		if (object_number == 0):
			object_number = find_item_alias(self, scratch, "CurrentRoom")
		if (object_number == 0):
			object_number = find_item_alias(self, scratch, "Inventory")
		if (object_number > 0):
			if (not object_found):
				# We've found a non-duplicate item in either the current room or player's inventory
				object_found = 1
				object_list = ["Item", object_number]
			else:
				# We've already found an object in this room which matches the current object string
				# so we want to spawn the duplicate object error message
				object_number = -1

		if (object_number == -1):
			object_found = 1
			output_text(self, "I'm not certain precisely what you are referring to. Please be more specific.\n\n")

		if (not object_found):
			# We didn't find a matching object on this pass, so we want to remove a word,
			# according to the search_focus variable.

			if ((search_focus == "Beginning") or (search_focus == "Start")):
				scratch_word_list = string.split(scratch, ' ')
				scratch = string.join(scratch_word_list[:-1], ' ')

			elif (search_focus == "End-Exclusive"):
				scratch_word_list = string.split(scratch, ' ')
				scratch = string.join(scratch_word_list[1:], ' ')

			elif (search_focus == "End"):
				scratch_word_list = string.split(scratch, ' ')
				scratch = string.join(scratch_word_list[1:], ' ')


	return( object_list )


####################################################################

def resolve_event(self, action, objects):

	# This method takes in a "action" string (verb provided on the command line
	# and a list of objects, and searches
	# through all of the possible event strings for the verb provided.
	# The first match (including requirements) found will be returned,
	# even if there are other duplicate matches.
	#
	# Note: Verb aliases should have already been resolved into the correct verb

	import string

	effect_string = None
	event_found = 0

	object1 = ""
	object2 = ""

	if ( len(objects) == 1 ):
		object1 = "%s(%i)" % (objects[0][0], objects[0][1])
	elif ( len(objects) == 2):
		object1 = "%s(%i)" % (objects[0][0], objects[0][1])
		object2 = "%s(%i)" % (objects[1][0], objects[1][1])

	for verb in self.verbData:
		if (string.lower(action) == string.lower(self.verbData[verb].name)):
			for event in self.verbData[verb].events:

				if ( not(event_found) and (self.verbData[verb].events[event] != None) ):

					# This next part is a bit tricky, since if a match exists, we want it
					# to be found regardless of the order the programmer entered the objects,
					# versus the order the player entered them on the command line

					if ( ( ((self.verbData[verb].events[event].object == None) or
					        (self.verbData[verb].events[event].object == object1))
					     and ((self.verbData[verb].events[event].object2 == None) or
					          (self.verbData[verb].events[event].object2 == object2)) )

					  or ( ((self.verbData[verb].events[event].object2 == None) or
					        (self.verbData[verb].events[event].object2 == object1))
					     and ((self.verbData[verb].events[event].object == None) or
						       (self.verbData[verb].events[event].object == object2)) ) ):

						# If we've made it this far, then all that's left is to very
						# that the current event's requirements are met
						if ( requirements_met(self, self.verbData[verb].events[event].requirements) ):

							event_found = 1
							effect_string = self.verbData[verb].events[event].effects

							if (self.gameInformation.debug_mode):
								# We want to print out a nicely-formatted copy of the entire event
								# to the debug console before the event is executed
								event_debug_display = self.format_event_text(self.verbData[verb].events[event])
								event_debug_display = self.convert_reference_numbers_to_names(event_debug_display)
								print "Event Found:"
								print event_debug_display, # we don't want an additional end-of-line character printed here
								                           # since format_event_text already leaves us with two


	return( effect_string )


#####################################################################

def requirements_met(self, requirements):

	# This method takes in a CogScript formatted requirements string
	# and determines whether the game's current environment meets
	# those requirements (stored in and returned as the "all_good" variable)

	import string

	all_good = 0
	contains_not = 0

	if ((requirements == None) or (requirements == "")):
		all_good = 1
	else:
		if (self.gameInformation.debug_mode):
			print "Verifying the following Requirements: " + requirements

		requirements_list = string.split(requirements, " ")

		del(requirements_list[0]) # Remove "(Requires"

		word = requirements_list[0]

		if ( (word == "(Not)") or ( word == "!") ):
			contains_not = 1
			del(requirements_list)[0]
			word = requirements_list[0]


		if (word[0:6] == "Player"):
			comparison = string.split(string.split(word, '[')[1], ']')[0]
			value = string.atoi(string.split(string.split(word, '(')[1], ')')[0])

			if (word[6:12] == "Points"):
				all_good = make_comparison( self, comparison, self.playerInformation.points, value)
			if (word[6:9] == "Exp"):
				all_good = make_comparison( self, comparison, self.playerInformation.experience, value)
			if (word[6:8] == "HP"):
				all_good = make_comparison( self, comparison, self.playerInformation.hp, value)
			if (word[6:9] == "MP"):
				all_good = make_comparison( self, comparison, self.playerInformation.mp, value)
			if (word[6:9] == "Str"):
				all_good = make_comparison( self, comparison, self.playerInformation.strength, value)
			if (word[6:8] == "IQ"):
				all_good = make_comparison( self, comparison, self.playerInformation.intelligence, value)
			if (word[6:9] == "Dex"):
				all_good = make_comparison( self, comparison, self.playerInformation.dexterity, value)
			if (word[6:10] == "Agil"):
				all_good = make_comparison( self, comparison, self.playerInformation.agility, value)
			if (word[6:14] == "Charisma"):
				all_good = make_comparison( self, comparison, self.playerInformation.charisma, value)
			if (word[6:16] == "ArmorLevel"):
				all_good = make_comparison( self, comparison, self.playerInformation.armor_level, value)
			if (word[6:17] == "CurrentWeight"):
				all_good = make_comparison( self, comparison, self.playerInformation.current_weight, value)

		if (word[0:4] == "Room"):
			room_number = string.atoi(string.split(string.split(word, '(')[1], ')')[0])

			if (word[-14:-1] == "IsCurrentRoom"):
				all_good = (self.playerInformation.current_room == room_number)
			if (word[-11:-1] == "HasVisited"):
				all_good = (self.roomData[room_number].visited)

		if (word[0:4] == "Item"):
			item_number = string.atoi(string.split(string.split(word, '(')[1], ')')[0])

			if (word[-12:-1] == "InInventory"):
				all_good = (item_number in self.playerInformation.items)
			if (word[-11:-1] == "IsEquipped"):
				all_good = (self.itemData[item_number].equipped)
			if (string.find(word, "ExistsInRoom") != -1):
				room_number = string.atoi(string.split(string.split(word, '(')[2], ')')[0])
				all_good = room_contains_item(self, room_number, item_number)
			if (string.find(word, "Weight") != -1):
				comparison = string.split(string.split(word, '[')[1], ']')[0]
				value = string.atoi(string.split(string.split(word, '(')[2], ')')[0])
				all_good = make_comparison(self, comparison, self.itemData[item_number].weight, value)
			if (string.find(word, "Bulk") != -1):
				comparison = string.split(string.split(word, '[')[1], ']')[0]
				value = string.atoi(string.split(string.split(word, '(')[2], ')')[0])
				all_good = make_comparison(self, comparison, self.itemData[item_number].bulk, value)

		if (word[0:11] == "Obstruction"):
			obstruction_number = string.atoi(string.split(string.split(word, '(')[1], ')')[0])

			if (string.find(word, 'ExistsInRoom') != -1):
				room_number = string.atoi(string.split(string.split(word, '(')[2], ')')[0])
				if (string.find(word, "Direction") != -1):
					# We are referring to a specific direction
					direction_number = string.atoi(string.split(string.split(word, '(')[-1], ')')[0])
					if (direction_number in self.roomData[room_number].direction):
						if (self.roomData[room_number].direction[direction_number].obstructions != None):
							obstruction_list = string.split(self.roomData[room_number].direction[direction_number].obstructions, ', ')
							for obstruction in obstruction_list:
								if (obstruction == ("%i" % obstruction_number)):
									all_good = 1
				else:
					# We are referring to any direction
					all_good = room_contains_obstruction(self, room_number, obstruction_number)

			if (string.find(word, "IsVisible") != -1):
				all_good = self.obstructionData[obstruction_number].visible

		if (contains_not):
			all_good = (not all_good)

		del(requirements_list[0])

		if (requirements_list != []):
			word = requirements_list[0]

			if (string.lower(word) == "and"):
				del(requirements_list[0]) # remove "and" from requirements string
				all_good = (all_good) and requirements_met(self, string.join(requirements_list, ' '))
			elif (string.lower(word) == "or"):
				del(requirements_list[0]) # remove "or" from requirements string
				all_good = (all_good) or requirements_met(self, string.join(requirements_list, ' '))

		if (self.gameInformation.debug_mode):
			if (all_good):
				print "Requirements Verified"
			else:
				print "Requirements Not Met"

	return(all_good)


#####################################################################

def make_comparison( self, comparison, value1, value2):

	# This method takes in a string and two integers.
	# The string contains a specific type of comparison we wish
	# to make with the two integers. The result of
	# the comparison is returned as a boolean

	result = 0

	if (comparison == "=="):
		result = (value1 == value2)
	elif (comparison == "!="):
		result = (value1 != value2)
	elif (comparison == ">"):
		result = (value1 > value2)
	elif (comparison == "<"):
		result = (value1 < value2)
	elif (comparison == ">="):
		result = (value1 >= value2)
	elif (comparison == "<="):
		result = (value1 <= value2)
	else:
		if (self.gameInformation.debug_mode):
			print "Bad comparison: %s" % comparison

	return(result)


#####################################################################

def evaluate_expression(self, expression, value1, value2):

	if (expression == "="):
		value1 = value2
	if (expression == "+"):
		value1 = value1 + value2
	if (expression == "-"):
		value1 = value1 - value2

	return(value1)
	

#####################################################################

def examine_object(self, object_name):

	# We parse from the end in order to allow a preposition
	# between the word "examine" and the object. The extra
	# space inserted before it is to get around a parse_object
	# issue.

	resolved_object = parse_object( self, object_name, "End")

	print "Resolved: ",
	print resolved_object

	if (resolved_object != None):

		if (resolved_object[0] == "Item"):
			item_number = resolved_object[1]

			if ((self.itemData[item_number].description != None) and
			(self.itemData[item_number].description != "")):
				output_text(self, self.itemData[item_number].description + "\n\n")

			if ((self.itemData[item_number].closeup_graphic_url != None) and
			(self.itemData[item_number].closeup_graphic_url != "")):
				display_image(self, self.itemData[item_number].closeup_graphic_url, 0, 0)

		if (resolved_object[0] == "Obstruction"):
			obstruction_number = resolved_object[1]

			if ( (self.obstructionData[obstruction_number].description != None) and
			(self.obstructionData[obstruction_number].description != "") and
			(self.obstructionData[obstruction_number].visible) ):
				output_text(self, self.obstructionData[obstruction_number].description + "\n\n")

			if ( (self.obstructionData[obstruction_number].closeup_graphic_url != None) and
			(self.obstructionData[obstruction_number].closeup_graphic_url != "") and
			(self.obstructionData[obstruction_number].visible) ):
				display_image(self, self.obstructionData[obstruction_number].closeup_graphic_url, 0, 0)

	else:
		output_text(self, "You don't see anything like that here.\n\n")


#####################################################################

def load_game(self):

	pass


#####################################################################

def save_game(self):

	pass


#####################################################################
#####################################################################
#####################################################################
#####################################################################
#####################################################################



#####################################################################
# Widgets
#####################################################################
# statistics_window
# statistics_textbox
#
# inventory_window
# inventory_textbox
#
# textmode_window
# output_textbox
# commandline_entry


# EOF
