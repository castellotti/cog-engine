#####################################################################
#
# COG Engine Development Application - Game Information Editor - Advanced Settings
#
# Copyright Steven M. Castellotti (2001, 2002)
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Last Update: 2002.06.07
#
#####################################################################


#####################################################################
# Functions
#####################################################################

def on_game_information_editor_advanced_settings_destroy(self, obj):
	# This function is called if a user closes a window directly,
	# instead of clicking off the toggle button
	self.gameInformationEditor.advanced_settings_togglebutton.set_active(0)
                           

#####################################################################

def insert_data_into_advanced_game_editor(self):
	# This function is called when a user opens the game editor. The fuction
	# configures the window's widgets according to the data stored in memory.
	
	# Advanced Game Settings
	self.gameInformationEditorAdvancedSettings.show_graphic_display_area_checkbutton.set_active(self.gameInformation.show_graphic_area)
	self.gameInformationEditorAdvancedSettings.show_statistical_display_checkbutton.set_active(self.gameInformation.show_stats)
	self.gameInformationEditorAdvancedSettings.show_inventory_checkbutton.set_active(self.gameInformation.show_inventory)
	self.gameInformationEditorAdvancedSettings.show_command_line_checkbutton.set_active(self.gameInformation.show_command_line)
	self.gameInformationEditorAdvancedSettings.show_text_output_display_area_checkbutton.set_active(self.gameInformation.show_text_output_area)
	self.gameInformationEditorAdvancedSettings.show_compass_checkbutton.set_active(self.gameInformation.show_compass)
	self.gameInformationEditorAdvancedSettings.center_button_indicates_items_checkbutton.set_active(self.gameInformation.center_button_indicates_items)
	self.gameInformationEditorAdvancedSettings.load_all_compass_images_checkbutton.set_active(self.gameInformation.load_all_compass_images)
	self.gameInformationEditorAdvancedSettings.show_graphical_inventory_checkbutton.set_active(self.gameInformation.show_graphical_inventory_panel)
	self.gameInformationEditorAdvancedSettings.show_graphical_inventory_panel_scrollbars_checkbutton.set_active(self.gameInformation.show_graphical_inventory_panel_scrollbars)
	self.gameInformationEditorAdvancedSettings.show_graphical_object_panel_checkbutton.set_active(self.gameInformation.show_graphical_object_panel)
	self.gameInformationEditorAdvancedSettings.show_graphical_object_panel_scrollbars_checkbutton.set_active(self.gameInformation.show_graphical_object_panel_scrollbars)
	self.gameInformationEditorAdvancedSettings.show_all_verbs_checkbutton.set_active(self.gameInformation.show_all_verbs)

	# Display Settings
	self.gameInformationEditorAdvancedSettings.graphical_display_window_x_dimension_textentry.set_text("%i" % self.gameInformation.graphical_display_window_x_dimension)
	self.gameInformationEditorAdvancedSettings.graphical_display_window_y_dimension_textentry.set_text("%i" % self.gameInformation.graphical_display_window_y_dimension)
	self.gameInformationEditorAdvancedSettings.graphical_display_x_coordinate_textentry.set_text("%i" % self.gameInformation.graphical_display_x_coordinate)
	self.gameInformationEditorAdvancedSettings.graphical_display_y_coordinate_textentry.set_text("%i" % self.gameInformation.graphical_display_y_coordinate)

	# Graphical Compass Settings
	self.gameInformationEditorAdvancedSettings.graphical_compass_x_coordinate_textentry.set_text("%i" % self.gameInformation.graphical_compass_display_x_coordinate)
	self.gameInformationEditorAdvancedSettings.graphical_compass_y_coordinate_textentry.set_text("%i" % self.gameInformation.graphical_compass_display_y_coordinate)
	self.gameInformationEditorAdvancedSettings.graphical_compass_button_image_x_dimension_textentry.set_text("%i" % self.gameInformation.graphical_compass_button_image_x_dimension)
	self.gameInformationEditorAdvancedSettings.graphical_compass_button_image_y_dimension_textentry.set_text("%i" % self.gameInformation.graphical_compass_button_image_y_dimension)
	self.gameInformationEditorAdvancedSettings.graphic_compass_help_menu_button_icon_textentry.set_text(self.gameInformation.menu_button_graphic_url)

	# Graphical Inventory Panel Settings
	self.gameInformationEditorAdvancedSettings.graphical_inventory_panel_x_display_coordinate_textentry.set_text("%i" % self.gameInformation.graphical_inventory_panel_Xoffset)
	self.gameInformationEditorAdvancedSettings.graphical_inventory_panel_y_display_coordinate_textentry.set_text("%i" % self.gameInformation.graphical_inventory_panel_Yoffset)
	self.gameInformationEditorAdvancedSettings.graphical_inventory_panel_x_icon_dimensions_textentry.set_text("%i" % self.gameInformation.graphical_inventory_x_icon_dimension)
	self.gameInformationEditorAdvancedSettings.graphical_inventory_panel_y_icon_dimensions_textentry.set_text("%i" % self.gameInformation.graphical_inventory_y_icon_dimension)
	self.gameInformationEditorAdvancedSettings.graphical_inventory_panel_x_icon_number_textentry.set_text("%i" % self.gameInformation.graphical_inventory_x_icons)
	self.gameInformationEditorAdvancedSettings.graphical_inventory_panel_y_icon_number_textentry.set_text("%i" % self.gameInformation.graphical_inventory_y_icons)
	self.gameInformationEditorAdvancedSettings.graphical_inventory_panel_blank_icon_textentry.set_text(self.gameInformation.graphical_inventory_blank_icon)
	self.gameInformationEditorAdvancedSettings.graphical_inventory_panel_graphic_not_available_icon_textentry.set_text(self.gameInformation.graphical_inventory_graphic_not_available_icon)
	self.gameInformationEditorAdvancedSettings.graphical_inventory_panel_scroll_up_available_icon_textentry.set_text(self.gameInformation.inventory_panel_scroll_up_available_icon)
	self.gameInformationEditorAdvancedSettings.graphical_inventory_panel_scroll_up_unavailable_icon_textentry.set_text(self.gameInformation.inventory_panel_scroll_up_unavailable_icon)
	self.gameInformationEditorAdvancedSettings.graphical_inventory_panel_scroll_down_available_icon_textentry.set_text(self.gameInformation.inventory_panel_scroll_down_available_icon)
	self.gameInformationEditorAdvancedSettings.graphical_inventory_panel_scroll_down_unavailable_icon_textentry.set_text(self.gameInformation.inventory_panel_scroll_down_unavailable_icon)

	# Graphical Object Panel Settings
	self.gameInformationEditorAdvancedSettings.graphical_object_panel_x_display_coordinate_textentry.set_text("%i" % self.gameInformation.object_panel_panel_Xoffset)
	self.gameInformationEditorAdvancedSettings.graphical_object_panel_y_display_coordinate_textentry.set_text("%i" % self.gameInformation.object_panel_panel_Yoffset)
	self.gameInformationEditorAdvancedSettings.graphical_object_panel_x_icon_dimension_textentry.set_text("%i" % self.gameInformation.object_panel_x_icon_dimension)
	self.gameInformationEditorAdvancedSettings.graphical_object_panel_y_icon_dimension_textentry.set_text("%i" % self.gameInformation.object_panel_y_icon_dimension)
	self.gameInformationEditorAdvancedSettings.graphical_object_panel_x_icon_number_textentry.set_text("%i" % self.gameInformation.object_panel_x_icons)
	self.gameInformationEditorAdvancedSettings.graphical_object_panel_y_icon_number_textentry.set_text("%i" % self.gameInformation.object_panel_y_icons)
	self.gameInformationEditorAdvancedSettings.graphical_object_panel_blank_icon_textentry.set_text(self.gameInformation.object_panel_blank_icon)
	self.gameInformationEditorAdvancedSettings.graphical_object_panel_graphic_not_available_icon_textentry.set_text(self.gameInformation.object_panel_graphic_not_available_icon)
	self.gameInformationEditorAdvancedSettings.graphical_object_panel_scroll_up_available_icon_textentry.set_text(self.gameInformation.object_panel_scroll_up_available_icon)
	self.gameInformationEditorAdvancedSettings.graphical_object_panel_scroll_up_unavailable_icon_textentry.set_text(self.gameInformation.object_panel_scroll_up_unavailable_icon)
	self.gameInformationEditorAdvancedSettings.graphical_object_panel_scroll_down_available_icon_textentry.set_text(self.gameInformation.object_panel_scroll_down_available_icon)
	self.gameInformationEditorAdvancedSettings.graphical_object_panel_scroll_down_unavailable_icon_textentry.set_text(self.gameInformation.object_panel_scroll_down_unavailable_icon)


#####################################################################

def read_advanced_game_editor_data_into_memory(self):
	# This function is called whenever the game editor is closed. The function
	# reads in the state of the various widgets and stores them into memory
	
	import string

	# Advanced Game Settings
	self.gameInformation.show_graphic_area = self.gameInformationEditorAdvancedSettings.show_graphic_display_area_checkbutton.get_active()
	self.gameInformation.show_stats = self.gameInformationEditorAdvancedSettings.show_statistical_display_checkbutton.get_active()
	self.gameInformation.show_inventory = self.gameInformationEditorAdvancedSettings.show_inventory_checkbutton.get_active()
	self.gameInformation.show_command_line = self.gameInformationEditorAdvancedSettings.show_command_line_checkbutton.get_active()
	self.gameInformation.show_text_output_area = self.gameInformationEditorAdvancedSettings.show_text_output_display_area_checkbutton.get_active()
	self.gameInformation.show_compass = self.gameInformationEditorAdvancedSettings.show_compass_checkbutton.get_active()
	self.gameInformation.center_button_indicates_items = self.gameInformationEditorAdvancedSettings.center_button_indicates_items_checkbutton.get_active()
	self.gameInformation.load_all_compass_images = self.gameInformationEditorAdvancedSettings.load_all_compass_images_checkbutton.get_active()
	self.gameInformation.show_graphical_inventory_panel = self.gameInformationEditorAdvancedSettings.show_graphical_inventory_checkbutton.get_active()
	self.gameInformation.show_graphical_inventory_panel_scrollbars = self.gameInformationEditorAdvancedSettings.show_graphical_inventory_panel_scrollbars_checkbutton.get_active()
	self.gameInformation.show_graphical_object_panel = self.gameInformationEditorAdvancedSettings.show_graphical_object_panel_checkbutton.get_active()
	self.gameInformation.show_graphical_object_panel_scrollbars = self.gameInformationEditorAdvancedSettings.show_graphical_object_panel_scrollbars_checkbutton.get_active()
	self.gameInformation.show_all_verbs = self.gameInformationEditorAdvancedSettings.show_all_verbs_checkbutton.get_active()

 	# Display Settings
	try:
		current_number = string.atoi(self.gameInformationEditorAdvancedSettings.graphical_display_window_x_dimension_textentry.get_text())
	except ValueError:
		self.display_dialog_box("Error", "Non-integer entered into Graphical Display Window X Dimension's number field")
	else:
		self.gameInformation.graphical_display_window_x_dimension = current_number

	try:
		current_number = string.atoi(self.gameInformationEditorAdvancedSettings.graphical_display_window_y_dimension_textentry.get_text())
	except ValueError:
		self.display_dialog_box("Error", "Non-integer entered into Graphical Display Window Y Dimension's number field")
	else:
		self.gameInformation.graphical_display_window_y_dimension = current_number

	try:
		current_number = string.atoi(self.gameInformationEditorAdvancedSettings.graphical_display_x_coordinate_textentry.get_text())
	except ValueError:
		self.display_dialog_box("Error", "Non-integer entered into Grapical Display X Coorindate's number field")
	else:
		self.gameInformation.graphical_display_x_coordinate = current_number

	try:
		current_number = string.atoi(self.gameInformationEditorAdvancedSettings.graphical_display_y_coordinate_textentry.get_text())
	except ValueError:
		self.display_dialog_box("Error", "Non-integer entered into Grapical Display Y Coorindate's number field")
	else:
		self.gameInformation.graphical_display_y_coordinate = current_number

	
	# Graphical Compass Settings
	try:
		current_number = string.atoi(self.gameInformationEditorAdvancedSettings.graphical_compass_x_coordinate_textentry.get_text())
	except ValueError:
		self.display_dialog_box("Error", "Non-integer entered into Graphical Compass Display X Coordinate's number field")
	else:
		self.gameInformation.graphical_compass_display_x_coordinate = current_number

	try:
		current_number = string.atoi(self.gameInformationEditorAdvancedSettings.graphical_compass_y_coordinate_textentry.get_text())
	except ValueError:
		self.display_dialog_box("Error", "Non-integer entered into Graphical Compass Display X Coordinate's number field")
	else:
		self.gameInformation.graphical_compass_display_y_coordinate = current_number

	try:
		current_number = string.atoi(self.gameInformationEditorAdvancedSettings.graphical_compass_button_image_x_dimension_textentry.get_text())
	except ValueError:
		self.display_dialog_box("Error", "Non-integer entered into Graphical Compass Button Image X Dimension's number field")
	else:
		self.gameInformation.graphical_compass_button_image_x_dimension = current_number

	try:
		current_number = string.atoi(self.gameInformationEditorAdvancedSettings.graphical_compass_button_image_y_dimension_textentry.get_text())
	except ValueError:
		self.display_dialog_box("Error", "Non-integer entered into Graphical Compass Button Image Y Dimension's number field")
	else:
		self.gameInformation.graphical_compass_button_image_y_dimension = current_number

	self.gameInformation.menu_button_graphic_url = self.gameInformationEditorAdvancedSettings.graphic_compass_help_menu_button_icon_textentry.get_text()


	# Graphical Inventory Panel Settings
	try:
		current_number = string.atoi(self.gameInformationEditorAdvancedSettings.graphical_inventory_panel_x_display_coordinate_textentry.get_text())
	except ValueError:
		self.display_dialog_box("Error", "Non-integer entered into Graphical Inventory Panels X Display Coordinate's number field")
	else:
		self.gameInformation.graphical_inventory_panel_Xoffset = current_number

	try:
		current_number = string.atoi(self.gameInformationEditorAdvancedSettings.graphical_inventory_panel_y_display_coordinate_textentry.get_text())
	except ValueError:
		self.display_dialog_box("Error", "Non-integer entered into Graphical Inventory Panels Y Display Coordinate's number field")
	else:
		self.gameInformation.graphical_inventory_panel_Yoffset = current_number

	try:
		current_number = string.atoi(self.gameInformationEditorAdvancedSettings.graphical_inventory_panel_x_icon_dimensions_textentry.get_text())
	except ValueError:
		self.display_dialog_box("Error", "Non-integer entered into Graphical Inventory Panel X Icon Dimensions's number field")
	else:
		self.gameInformation.graphical_inventory_x_icon_dimension = current_number

	try:
		current_number = string.atoi(self.gameInformationEditorAdvancedSettings.graphical_inventory_panel_y_icon_dimensions_textentry.get_text())
	except ValueError:
		self.display_dialog_box("Error", "Non-integer entered into Graphical Inventory Panel Y Icon Dimensions's number field")
	else:
		self.gameInformation.graphical_inventory_y_icon_dimension = current_number

	try:
		current_number = string.atoi(self.gameInformationEditorAdvancedSettings.graphical_inventory_panel_x_icon_number_textentry.get_text())
	except ValueError:
		self.display_dialog_box("Error", "Non-integer entered into Graphical Inventory Panel X Icon Number's number field")
	else:
		self.gameInformation.graphical_inventory_x_icons = current_number

	try:
		current_number = string.atoi(self.gameInformationEditorAdvancedSettings.graphical_inventory_panel_y_icon_number_textentry.get_text())
	except ValueError:
		self.display_dialog_box("Error", "Non-integer entered into Graphical Inventory Panel Y Icon Number's number field")
	else:
		self.gameInformation.graphical_inventory_y_icons = current_number

	self.gameInformation.graphical_inventory_blank_icon = self.gameInformationEditorAdvancedSettings.graphical_inventory_panel_blank_icon_textentry.get_text()
	self.gameInformation.graphical_inventory_graphic_not_available_icon = self.gameInformationEditorAdvancedSettings.graphical_inventory_panel_graphic_not_available_icon_textentry.get_text()
	self.gameInformation.inventory_panel_scroll_up_available_icon = self.gameInformationEditorAdvancedSettings.graphical_inventory_panel_scroll_up_available_icon_textentry.get_text()
	self.gameInformation.inventory_panel_scroll_up_unavailable_icon = self.gameInformationEditorAdvancedSettings.graphical_inventory_panel_scroll_up_unavailable_icon_textentry.get_text()
	self.gameInformation.inventory_panel_scroll_down_available_icon = self.gameInformationEditorAdvancedSettings.graphical_inventory_panel_scroll_down_available_icon_textentry.get_text()
	self.gameInformation.inventory_panel_scroll_down_unavailable_icon = self.gameInformationEditorAdvancedSettings.graphical_inventory_panel_scroll_down_unavailable_icon_textentry.get_text()

	
	# Graphical Object Panel Settings
	try:
		current_number = string.atoi(self.gameInformationEditorAdvancedSettings.graphical_object_panel_x_display_coordinate_textentry.get_text())
	except ValueError:
		self.display_dialog_box("Error", "Non-integer entered into Graphical Object Panel X Display Coordinate's number field")
	else:
		self.gameInformation.object_panel_panel_Xoffset = current_number

	try:
		current_number = string.atoi(self.gameInformationEditorAdvancedSettings.graphical_object_panel_y_display_coordinate_textentry.get_text())
	except ValueError:
		self.display_dialog_box("Error", "Non-integer entered into Graphical Object Panel Y Display Coordinate's number field")
	else:
		self.gameInformation.object_panel_panel_Yoffset = current_number

	try:
		current_number = string.atoi(self.gameInformationEditorAdvancedSettings.graphical_object_panel_x_icon_dimension_textentry.get_text())
	except ValueError:
		self.display_dialog_box("Error", "Non-integer entered into Graphical Object Panel X Icon Dimension's number field")
	else:
		self.gameInformation.object_panel_x_icon_dimension = current_number

	try:
		current_number = string.atoi(self.gameInformationEditorAdvancedSettings.graphical_object_panel_y_icon_dimension_textentry.get_text())
	except ValueError:
		self.display_dialog_box("Error", "Non-integer entered into Graphical Object Panel Y Icon Dimension's number field")
	else:
		self.gameInformation.object_panel_y_icon_dimension = current_number

	try:
		current_number = string.atoi(self.gameInformationEditorAdvancedSettings.graphical_object_panel_x_icon_number_textentry.get_text())
	except ValueError:
		self.display_dialog_box("Error", "Non-integer entered into Graphical Object Panel X Icon Number's number field")
	else:
		self.gameInformation.object_panel_x_icons = current_number

	try:
		current_number = string.atoi(self.gameInformationEditorAdvancedSettings.graphical_object_panel_y_icon_number_textentry.get_text())
	except ValueError:
		self.display_dialog_box("Error", "Non-integer entered into Graphical Object Panel Y Icon Number's number field")
	else:
		self.gameInformation.object_panel_y_icons = current_number

	self.gameInformation.object_panel_blank_icon = self.gameInformationEditorAdvancedSettings.graphical_object_panel_blank_icon_textentry.get_text()
	self.gameInformation.object_panel_graphic_not_available_icon = self.gameInformationEditorAdvancedSettings.graphical_object_panel_graphic_not_available_icon_textentry.get_text()
	self.gameInformation.object_panel_scroll_up_available_icon = self.gameInformationEditorAdvancedSettings.graphical_object_panel_scroll_up_available_icon_textentry.get_text()
	self.gameInformation.object_panel_scroll_up_unavailable_icon = self.gameInformationEditorAdvancedSettings.graphical_object_panel_scroll_up_unavailable_icon_textentry.get_text()
	self.gameInformation.object_panel_scroll_down_available_icon = self.gameInformationEditorAdvancedSettings.graphical_object_panel_scroll_down_available_icon_textentry.get_text()
	self.gameInformation.object_panel_scroll_down_unavailable_icon = self.gameInformationEditorAdvancedSettings.graphical_object_panel_scroll_down_unavailable_icon_textentry.get_text()


# EOF
