#####################################################################
#
# COG Engine Development Application - Cog Objects
#
# Copyright Steven M. Castellotti (2000-2002)
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Last Update: 2002.06.15
#
#####################################################################

#####################################################################
# Classes
#####################################################################

class GameInformationObject:
	def __init__(self):
		self.game_title = ""
		self.version_number = "0.0"
		self.game_designer = ""
		self.game_designer_email_address = ""
		self.last_update = ""
		self.debug_mode = 1                    # boolean
		self.game_url = ""
		self.database_url = ""
		self.show_all_verbs = 0                # boolean
		self.introduction_text = ""
		self.image_loading_graphic_url = ""
		self.introduction_graphic_url = ""
		self.image_directory = ""
		self.audio_directory = ""
		self.game_information_notes = ""

		self.text_to_speech_enabled = 1
		self.command_history = []
		self.output_history = ""

		# Advanced Game Settings
		self.show_stats = 1											# boolean
		self.show_inventory = 1             				   # boolean
		self.show_command_line = 1 				            # boolean
		self.show_text_output_area = 1							# boolean

		# Display Settings
		self.show_graphic_area = 1									# boolean
		self.graphical_display_window_x_dimension = 640
		self.graphical_display_window_y_dimension = 595
		self.graphical_display_x_coordinate = 0
		self.graphical_display_y_coordinate = 0
		self.graphic_panel_x_dimension = 640
		self.graphic_panel_y_dimension = 480
		self.default_mouse_pointer_graphic = ""

		# Graphical Compass Settings
		self.show_compass = 1										# boolean
		self.center_button_indicates_items = 1 				# boolean
		self.load_all_compass_images = 1 				      # boolean
		self.display_help_button = 1 				            # boolean
		self.graphical_compass_display_x_coordinate = 246
		self.graphical_compass_display_y_coordinate = 482
		self.graphical_compass_x_icons = 4
		self.graphical_compass_y_icons = 3
		self.graphical_compass_panel_padding = 0
		self.graphical_compass_background_image = ""
		self.graphical_compass_graphic_not_available_icon = ""
		self.menu_button_graphic_url = ""
		self.menu_button_display_position = 0

		# Graphical Inventory Panel Settings
		self.show_graphical_inventory_panel = 1				# boolean
		self.show_graphical_inventory_panel_scrollbars = 1	# boolean
		self.graphical_inventory_panel_Xoffset = 415
		self.graphical_inventory_panel_Yoffset = 488
		self.graphical_inventory_x_icons = 4
		self.graphical_inventory_y_icons = 2
		self.graphical_inventory_panel_padding = 1
		self.graphical_inventory_blank_icon = ""
		self.graphical_inventory_graphic_not_available_icon = ""
		self.inventory_panel_scroll_up_available_icon = ""
		self.inventory_panel_scroll_up_unavailable_icon = ""
		self.inventory_panel_scroll_down_available_icon = ""
		self.inventory_panel_scroll_down_unavailable_icon = ""

		# Graphical Object Panel Settings
		self.show_graphical_object_panel = 1					# boolean
		self.show_graphical_object_panel_scrollbars = 1		# boolean
		self.object_panel_Xoffset = 5
		self.object_panel_Yoffset = 538
		self.object_panel_x_icons = 4
		self.object_panel_y_icons = 1
		self.object_panel_padding = 1
		self.object_panel_blank_icon = ""
		self.object_panel_graphic_not_available_icon = ""
		self.object_panel_scroll_up_available_icon = ""
		self.object_panel_scroll_up_unavailable_icon = ""
		self.object_panel_scroll_down_available_icon = ""
		self.object_panel_scroll_down_unavailable_icon = ""


#####################################################################

class PlayerInformationObject:
	def __init__(self):
		self.name = "Player"
		self.email_address = ""
		self.points = -1
		self.experience = -1
		self.experience_level = -1
		self.hp = -1
		self.mp = -1
		self.strength = -1
		self.intelligence = -1
		self.dexterity = -1
		self.agility = -1
		self.charisma = -1
		self.armor_level = -1
		self.max_weight = -1
		self.max_bulk = -1
		self.current_weight = -1
		self.current_bulk = -1
		self.current_room = 1
		self.items = [] # list


#####################################################################

class DirectionInformationObject:
	# Note - DirectionInfoOBJ objects are used to
	# keep track of infomation relating to a particular
	# direction for the entire game (such as the
	# direction's name).  DirectionOBJ objects are used
	# to keep track of information relating to a particular
	# direction within a particular room.
	def __init__(self):
		self.number = -1
		self.name = ""
		self.abbreviation = ""
		self.compass_graphic_available_url = ""
		self.compass_graphic_unavailable_url = ""
		self.compass_graphic_special_url = ""
		self.compass_graphic_never_traveled = ""
		self.compass_graphic_last_direction_traveled = ""
		self.compass_panel_display_position = 0


#####################################################################

class RoomObject:
	def __init__(self):
		self.number = -1
		self.name = ""
		self.visited = 0 # boolean
		self.graphic_url = ""
		self.description_long = ""
		self.description_short = ""
		self.direction_description = ""
		self.direction = {}
		self.items = None
		self.notes = ""


#####################################################################

class DirectionObject:
	# Note - DirectionOBJ objects are used to keep track of
	# information relating to a particular direction within
	# a particular room. DirectionInfoOBJ objects are used
	# to keep track of infomation relating to a particular
	# direction for the entire game (such as the direction's name)
	def __init__(self):
		self.to_which_room = -1
		self.obstructions = None
		self.has_moved_this_way = 0        # boolean
		self.first_transition_text = ""
		self.transition_text = ""
		self.first_transition_graphic = ""
		self.transition_graphic = ""


#####################################################################

class ItemObject:
	def __init__(self):
		self.number = -1
		self.name = ""
		self.aliases = ""
		self.environment_graphic_url = ""
		self.environment_graphic_Xpos = 0
		self.environment_graphic_Ypos = 0
		self.closeup_graphic_url = ""
		self.icon_graphic_url = ""
		self.equipped_graphic_url = ""
		self.description = ""
		self.equipped = 0 # boolean
		self.weight = 0 # negative weight implies that object cannot be picked up
		self.bulk = 0 # negative bulk indicates how much a "container" can hold (if item is a container)
		self.notes = ""


#####################################################################

class ObstructionObject:
	def __init__(self):
		self.number = -1
		self.name = ""
		self.aliases = ""
		self.environment_graphic_url = ""
		self.environment_graphic_Xpos = 0
		self.environment_graphic_Ypos = 0
		self.closeup_graphic_url = ""
		self.icon_graphic_url = ""
		self.description = ""
		self.visible = 1 # boolean
		self.notes = ""


#####################################################################

class VerbObject:
	def __init__(self):
		self.number = -1
		self.name = ""
		self.aliases = ""
		self.mouse_pointer_graphic = ""
		self.events = {} # why not a list?
		self.notes = ""


#####################################################################

class EventObject:
	def __init__(self):
		self.action = ""
		self.object = ""
		self.preposition = ""
		self.object2 = ""
		self.requirements = "" # don't forget to error-check this while parsing!
		self.effects = "" # don't forget to error-check this while parsing!
		self.has_been_executed = 0 # boolean # Not currently implemented. Aids in point calculations
      
