#####################################################################
#
# COG Engine Development Application - Cog Objects
#
# Copyright Steven M. Castellotti (2000)
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Last Update: 2001.02.01
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
		self.total_rooms = 1
		self.total_directions = 0
		self.total_items = 0
		self.total_obstructions = 0
		self.total_verbs = 0
		self.show_all_verbs = 0                # boolean
		self.introduction_text = ""
		self.image_loading_graphic_url = ""
		self.introduction_graphic_url = ""
		self.preferred_graphic_size_X = -1
		self.preferred_graphic_size_Y = -1
		self.show_stats = 1                    # boolean
		self.show_inventory = 1                # boolean
		self.show_command_line = 1             # boolean
		self.show_compass = 1                  # boolean
		self.center_button_indicates_items = 1 # boolean
		self.load_all_compass_images = 1       # boolean
		self.menu_button_graphic_url = ""
		self.game_information_notes = ""
		# self.direction_header_notes = ""
		# self.room_header_notes = ""
		# self.item_header_notes = ""
		# self.obstruction_header_notes = ""
		# self.verb_header_notes = ""
		# self.event_header_notes = ""


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
		self.facing = 1
		self.items = () # list


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
		self.items = ""
		self.notes = ""


class DirectionObject:
	# Note - DirectionOBJ objects are used to keep track of
	# information relating to a particular direction within
	# a particular room. DirectionInfoOBJ objects are used
	# to keep track of infomation relating to a particular
	# direction for the entire game (such as the direction's name)
	def __init__(self):
		self.to_which_room = -1
		self.obstructions = ""
		self.has_moved_this_way = 0        # boolean
		self.first_transition_text = ""
		self.transition_text = ""
		self.first_transition_graphic = ""
		self.transition_graphic = ""
		# self.state = "" # I forget what this is used for


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
		self.location = "" # usage is depricated
		self.equipped = 0 # boolean
		self.weight = 0 # negative weight implies that object cannot be picked up
		self.bulk = 0 # negative bulk indicates how much a "container" can hold (if item is a container)
		self.notes = ""


class ObstructionObject:
	def __init__(self):
		self.number = -1
		self.name = ""
		self.aliases = ""
		self.environment_graphic_url = ""
		self.environment_graphic_Xpos = 0
		self.environment_graphic_Ypos = 0
		self.closeup_graphic_url = ""
		self.description = ""
		self.type = "" # set to "Antagonist" or "Obstacle"
		self.locations = ""
		self.visible = 0 # boolean
		self.notes = ""


class VerbObject:
	def __init__(self):
		self.number = -1
		self.name = ""
		self.aliases = ""
		self.events = {}
		self.total_events = 0
		self.notes = ""
		# self.events_filled # I forget what this is used for

class EventObject:
	def __init__(self):
		self.action = ""
		self.object = ""
		self.preposition = ""
		self.object2 = ""
		self.requirements = "" # don't forget to error-check this while parsing!
		self.effects = "" # don't forget to error-check this while parsing!
		self.has_been_executed = 0 # boolean # Not currently implemented. Aids in point calculations
