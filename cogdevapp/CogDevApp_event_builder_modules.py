#####################################################################
#
# COG Engine Development Application - Event Builder
#
# Copyright Steven M. Castellotti (2001)
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Last Update: 2001.09.15
#
#####################################################################
# Notes
#####################################################################
# <Action> <Object> [<Preposition> <Object>]
# [ '('Requires [! | '('Not')'] <Requirement>')' ]
# { ( and | or ) '('Requires [! | '('Not')'] <Requirement>')' } ->
# 	<Effect> {and <Effect>};
#
#
# Note -- Optionmenus don't provide selections to combos when no data file is loaded
# Note -- "Not" settings on requirements are forgotten between changes
# Note -- Can't modify to_which_room to point nowhere

#####################################################################
# Method Headers
#####################################################################
#
# def setup_default_data_in_event_builder(self):
# def display_event_builder(self):
# def create_event_widget_container(self, key_prefix, key_index, label, widget, widget_type):
# def setup_event_builder_action_menu(self):
# def setup_event_builder_object_menu(self, key):
# def setup_event_builder_reference_combo(self, obj, key, type):
# def setup_event_builder_preposition_combo(self, key):
# def setup_event_builder_effect_menu(self, key):
# def setup_event_builder_itemlocation_menu(self, key):
# def setup_event_builder_room_reference_combo(self, key):
# def setup_event_builder_nowhere_room_reference_combo(self, key):
# def setup_event_builder_direction_reference_optionmenu(self, key):
# def setup_event_builder_direction_reference_combo(self, key):
# def setup_event_builder_modifies_menu(self, key):
# def setup_event_builder_modifies_player_menu(self, key):
# def setup_event_builder_modifies_room_direction_menu(self, key):
# def setup_event_builder_expression_menu(self, key):
# def setup_event_builder_comparison_menu(self, key):
# def setup_event_builder_modifies_room_menu(self, key):
# def setup_event_builder_modifies_item_menu(self, key):
# def setup_event_builder_modifies_obstruction_menu(self, key):
# def setup_event_builder_requires_room_property_menu(self, key):
# def setup_event_builder_requires_item_property_menu(self, key):
# def setup_event_builder_requires_obstruction_property_menu(self, key):
# def setup_event_builder_requires_and_or_menu(self, key):
# def setup_radiobutton_vbox(self, key_prefix, key_index, default_truth_boolean):
# def add_object_toolbar(self):
# def remove_object_toolbar(self):
# def add_new_requirement_toolbar(self):
# def remove_last_requirement_toolbar(self):
# def add_new_effect_toolbar(self):
# def remove_last_effect_toolbar(self):
# def handle_action_selection(self, obj, new_selection):
# def handle_optionmenu_change(self, obj, key, selection):
# def handle_entry_change(self, obj, key):
# def handle_radiobutton_toggled(self, obj, key):
# def rebuild_action_toolbar(self):
# def rebuild_object_toolbar(self):
# def rebuild_requirement_toolbars(self):
# def rebuild_yeilds_and_button_toolbars(self):
# def rebuild_effect_toolbars(self):
# def parse_action_toolbar_widgets(self):
# def parse_object_toolbar_widgets(self):
# def parse_requirement_toolbars(self):
# def parse_effect_toolbars(self):
# def read_event_builder_widgets_into_memory(self):
# def on_event_builder_add_object_button_clicked(self, obj):
# def on_event_builder_remove_object_button_clicked(self, obj):
# def on_event_builder_add_requirement_button_clicked(self, obj):
# def on_event_builder_remove_requirement_button_clicked(self, obj):
# def on_event_builder_add_effect_button_clicked(self, obj):
# def on_event_builder_remove_effect_button_clicked(self, obj):
# def on_append_event_button_clicked(self, obj):
#
#
#####################################################################
# Functions
#####################################################################

def setup_default_data_in_event_builder(self):

	# This function creates all of the default widgets that should be
	# displayed in the event builder whenever the event editor is opened
	# for the first time, or when a new event needs to be created.

	import gtk

	key_index = 0

	# Initialize event builder widget tree
	self.eventTree = {}
	self.eventTree['display_object_toolbar'] = 0

	# Setup action toolbar
	self.rebuild_action_toolbar()

	# Setup yeilds label
	yeilds_label = gtk.GtkLabel('->')
	self.eventTree['yeilds_label:0'] = yeilds_label
	yeilds_label.show()

	# Setup effect toolbar
	self.add_new_effect_toolbar()

	# Setup has_been_executed checkbutton
# 	has_been_executed_checkbutton = gtk.GtkCheckButton('Event has been executed')
# 	self.eventTree['has_been_executed_checkbutton:0'] = has_been_executed_checkbutton
# 	# Setup toggled status
# 	has_been_executed_checkbutton.set_active( 0 )
# 	has_been_executed_checkbutton.show()

	# Setup append_event button
	append_event_button = gtk.GtkButton('Append Event')
	append_event_button.connect("clicked", self.on_append_event_button_clicked)
	self.eventTree['append_event_button:0'] = append_event_button
	append_event_button.show()

	# Setup button toolbar
	button_toolbar = gtk.GtkToolbar(gtk.ORIENTATION_HORIZONTAL, gtk.TOOLBAR_BOTH)
# 	button_toolbar.append_widget(has_been_executed_checkbutton, "", "")
	button_toolbar.append_widget(append_event_button, "", "")
	self.eventTree['button_toolbar:0'] = button_toolbar
	button_toolbar.show()

	# Call setup_event_builder to draw widgets
	self.display_event_builder()


#####################################################################

def display_event_builder(self):

	# This function draws all of the various toolbars stored in the eventTree dictionary

	import gtk, string

	# Clear current viewport
	try:
		self.eventEditor.event_builder_viewport.remove( self.eventTree['main_vbox:0'] )
		self.eventTree['main_vbox:0'].destroy()
	except KeyError:
		pass # this should only occur the first time the editor is displayed, so we can ignore it.

	eventTree_list = self.eventTree.keys()
	eventTree_list.sort()

	# Setup main vbox
	main_vbox = gtk.GtkVBox(gtk.FALSE, 0) # homogeneous, spacing

	# Extract action toolbar
	action_toolbar = self.eventTree['action_toolbar:0']
	main_vbox.pack_start(action_toolbar, gtk.FALSE, gtk.FALSE) # widget, expand, fill

	# Build object toolbar
	if ( 'object_toolbar:0' in eventTree_list ):
		object_toolbar = self.eventTree['object_toolbar:0']
		main_vbox.pack_start(object_toolbar, gtk.FALSE, gtk.FALSE)

	# Build reference toolbar(s)
	for each in eventTree_list:
		if ( string.find(each, 'requirement_toolbar') != -1 ):
			current_reference_toolbar = self.eventTree[each]
			main_vbox.pack_start(current_reference_toolbar, gtk.FALSE, gtk.FALSE)

	# Extract yeilds label
	yeilds_label = self.eventTree['yeilds_label:0']
	main_vbox.pack_start(yeilds_label, gtk.FALSE, gtk.FALSE)

	# Build effect toolbar(s)
	for each in eventTree_list:
		if ( string.find(each, 'effect_toolbar') != -1 ):
			current_effect_toolbar = self.eventTree[each]
			main_vbox.pack_start(current_effect_toolbar, gtk.FALSE, gtk.FALSE)

	# Extract button toolbar
	button_toolbar = self.eventTree['button_toolbar:0']
	main_vbox.pack_start(button_toolbar, gtk.FALSE, gtk.FALSE)

	# Pack main vbox
	self.eventTree['main_vbox:0'] = main_vbox
	main_vbox.show()

	# Add main vbox to viewport
	self.eventEditor.event_builder_viewport.add( main_vbox )


#####################################################################

def create_event_widget_container(self, key_prefix, key_index, label, widget, widget_type):
	# An "event widget container" is a vbox which contains a label and a widget

	import gtk

	vbox_key = '%s_vbox:%s' % (key_prefix, key_index)
	label_key = '%s_label:%s' % (key_prefix, key_index)
	widget_key = '%s_%s:%s' % (key_prefix, widget_type, key_index)

	vbox = gtk.GtkVBox() # homogeneous, spacing
	self.eventTree[vbox_key] = vbox

	label = gtk.GtkLabel(label)
	self.eventTree[label_key] = label

	if ( widget_type != 'vbox' ):
		self.eventTree[widget_key] = widget

	if ( widget_type == 'combo'):
		widget.entry.connect("changed", self.handle_entry_change, widget_key)

	if ( widget_type == 'entry'):
		if not self.eventTree.has_key( '%s:selection' % widget_key ):
			self.eventTree[ '%s:selection' % widget_key ] = ''
		widget.connect("changed", self.handle_entry_change, widget_key)

	vbox.pack_start(label) # widget, expand, fill
	vbox.pack_start(widget)

	label.show()
	widget.show()
	vbox.show()

	return(vbox)


#####################################################################
	 
def setup_event_builder_action_menu(self):
	import gtk

	action_menu = gtk.GtkMenu()

	verb_list = self.verbData.keys()
	verb_list.sort()

	if ( ( not self.eventTree.has_key('action_optionmenu:0:selection') ) \
	     and ( verb_list != [] ) ):
		self.eventTree['action_optionmenu:0:selection'] = self.verbData[ verb_list[0] ].name


	action_list = []
	for each in verb_list:
		if ( self.verbData[each].name not in action_list ):
			action_list.append( self.verbData[each].name )

	for each in action_list:
		menu_item = gtk.GtkMenuItem(each)
		menu_item.connect("activate", self.handle_action_selection, each)
		action_menu.append(menu_item)
		menu_item.show()
		if ( ( self.eventTree.has_key('action_optionmenu:0:selection') ) \
		     and ( self.eventTree['action_optionmenu:0:selection'] == each ) ):
			action_menu.set_active( action_list.index(each) )

	return(action_menu)


#####################################################################

def setup_event_builder_object_menu(self, key):
	import gtk, string

	object_menu = gtk.GtkMenu()

	if ( self.itemData != {} ):
		menu_item = gtk.GtkMenuItem("Item")
		menu_item.connect("activate", self.handle_optionmenu_change, key, 'Item')
		object_menu.append(menu_item)
		menu_item.show()
		if ( not self.eventTree.has_key( '%s:selection' % key ) ):
			self.eventTree['%s:selection' % key] = 'Item'

	if ( self.obstructionData != {} ):
		menu_item = gtk.GtkMenuItem("Obstruction")
		menu_item.connect("activate", self.handle_optionmenu_change, key, 'Obstruction')
		object_menu.append(menu_item)
		menu_item.show()
		if ( ( self.eventTree.has_key( '%s:selection' % key ) ) \
		     and ( self.eventTree['%s:selection' % key ] == 'Obstruction' ) ):
			object_menu.set_active( 1 ) # set obstruction to active if that was the last

	return(object_menu)


#####################################################################

def setup_event_builder_reference_combo(self, obj, key, type):
	import gtk

	reference_combo = gtk.GtkCombo()
	object_list = []

	if ( type == 'Item' and self.itemData != {} ):
		item_list = self.itemData.keys()
		item_list.sort()

		for each in item_list:
			object_list.append( "%i - %s" % (each, self.itemData[each].name) )

	elif ( type == 'Obstruction' and  self.obstructionData != {} ):
		obstruction_list = self.obstructionData.keys()
		obstruction_list.sort()

		for each in obstruction_list:
			object_list.append( "%i - %s" % (each, self.obstructionData[each].name) )


	reference_combo.set_popdown_strings(object_list)
	#reference_combo.set_child_packing(reference_combo.list, gtk.TRUE, gtk.TRUE, 0, gtk.PACK_START) # child, expand, fill, padding, pack_type

	if (self.eventTree.has_key('%s:selection' % key)) and \
	   (self.eventTree['%s:selection' % key] in object_list):
		reference_combo.entry.set_text(self.eventTree['%s:selection' % key])
	else:
		self.eventTree['%s:selection' % key] = reference_combo.entry.get_text()

	return(reference_combo)


#####################################################################

def setup_event_builder_preposition_combo(self, key):
	import gtk

	preposition_list = ['about', 'above', 'across', 'after', 'against', \
	                    'along', 'among', 'around', 'at', 'before', 'behind', \
	                    'below', 'beneath', 'beside', 'between', 'during', \
	                    'by', 'down', 'except', 'for', 'from', 'front', 'in', \
	                    'inside', 'instead', 'into', 'like', 'near', 'of', \
	                    'off', 'on', 'onto', 'out', 'outside', 'over', 'past', \
	                    'since', 'through', 'to', 'top', 'toward', 'under', \
	                    'underneath', 'until', 'up', 'upon', 'with', 'within', \
	                    'without']

	preposition_combo = gtk.GtkCombo()
	preposition_list.sort()

	preposition_combo.set_popdown_strings(preposition_list)

	if self.eventTree.has_key('%s:selection' % key):
		preposition_combo.entry.set_text( self.eventTree['%s:selection' % key] )
	else:
		self.eventTree['%s:selection' % key] = preposition_combo.entry.get_text()

	return(preposition_combo)


#####################################################################

def setup_event_builder_effect_menu(self, key):
	import gtk, string

	effect_list = ['Adds', 'Removes', 'Modifies', 'TextMessage', 'GraphicMessage', 'PlaySoundFile']
	effect_menu = gtk.GtkMenu()

	for each in effect_list:
		menu_item = gtk.GtkMenuItem(each)
		menu_item.connect("activate", self.handle_optionmenu_change, key, each)
		effect_menu.append(menu_item)
		menu_item.show()
		if ( ( self.eventTree.has_key( '%s:selection' % key ) ) \
		     and ( self.eventTree['%s:selection' % key ] == each ) ):
			effect_menu.set_active( effect_list.index(each) )

	if ( not self.eventTree.has_key( '%s:selection' % key ) ):
		self.eventTree['%s:selection' % key] = 'Adds'

	return(effect_menu)


#####################################################################

def setup_event_builder_itemlocation_menu(self, key):
	import gtk

	itemlocation_list = ['Inventory', 'CurrentRoom', 'Room']
	itemlocation_menu = gtk.GtkMenu()

	for each in itemlocation_list:
		menu_item = gtk.GtkMenuItem(each)
		menu_item.connect("activate", self.handle_optionmenu_change, key, each)
		itemlocation_menu.append(menu_item)
		menu_item.show()
		if ( ( self.eventTree.has_key( '%s:selection' % key ) ) \
		   and ( self.eventTree['%s:selection' % key ] == each ) ):
			itemlocation_menu.set_active( itemlocation_list.index(each) )

	if ( not self.eventTree.has_key( '%s:selection' % key ) ):
		self.eventTree['%s:selection' % key] = 'Inventory'

	return(itemlocation_menu)


#####################################################################

def setup_event_builder_room_reference_combo(self, key):
	import gtk

	reference_combo = gtk.GtkCombo()
	reference_list = []

	if ( self.roomData != {} ):
		room_list = self.roomData.keys()
		room_list.sort()

		for each in room_list:
			reference_list.append( "%i - %s" % (each ,self.roomData[each].name) )

	reference_combo.set_popdown_strings(reference_list)

	if (self.eventTree.has_key('%s:selection' % key)) and \
	   (self.eventTree['%s:selection' % key] in reference_list):
		reference_combo.entry.set_text(self.eventTree['%s:selection' % key])
	else:
		self.eventTree['%s:selection' % key] = reference_combo.entry.get_text()

	return(reference_combo)


#####################################################################

def setup_event_builder_nowhere_room_reference_combo(self, key):
	import gtk

	reference_combo = gtk.GtkCombo()
	reference_list = ['0 - Nowhere']

	if ( self.roomData != {} ):
		room_list = self.roomData.keys()
		room_list.sort()

		for each in room_list:
			reference_list.append( "%i - %s" % (each ,self.roomData[each].name) )

	reference_combo.set_popdown_strings(reference_list)

	if (self.eventTree.has_key('%s:selection' % key)) and \
	   (self.eventTree['%s:selection' % key] in reference_list):
		reference_combo.entry.set_text(self.eventTree['%s:selection' % key])
	else:
		self.eventTree['%s:selection' % key] = reference_combo.entry.get_text()

	return(reference_combo)


#####################################################################

def setup_event_builder_direction_reference_optionmenu(self, key):
	import gtk, string

	direction_list = self.directionData.keys()
	direction_list.sort()

	direction_names = []
	for each in direction_list:
		direction_names.append( self.directionData[each].name )

	direction_menu = gtk.GtkMenu()

	for each in direction_names:
		menu_item = gtk.GtkMenuItem(each)
		menu_item.connect("activate", self.handle_optionmenu_change, key, each)
		direction_menu.append(menu_item)
		menu_item.show()
		if ( ( self.eventTree.has_key( '%s:selection' % key ) ) \
		     and ( self.eventTree['%s:selection' % key ] == each ) ):
			direction_menu.set_active( direction_names.index(each) )

	if ( ( not self.eventTree.has_key( '%s:selection' % key ) ) \
	   and ( direction_names != [] ) ):
		self.eventTree['%s:selection' % key] = direction_names[0]

	return(direction_menu)


#####################################################################

def setup_event_builder_direction_reference_combo(self, key):
	# This widget is currently not used, in favor of the direction_reference_optionmenu
	import gtk

	reference_combo = gtk.GtkCombo()
	reference_list = []

	if ( self.directionData != {} ):
		direction_list = self.directionData.keys()
		direction_list.sort()

		for each in direction_list:
			reference_list.append( "%i - %s" % (each, self.directionData[each].name) )

	reference_combo.set_popdown_strings(reference_list)

	if (self.eventTree.has_key('%s:selection' % key)) and \
	   (self.eventTree['%s:selection' % key] in reference_list):
		reference_combo.entry.set_text(self.eventTree['%s:selection' % key])
	else:
		self.eventTree['%s:selection' % key] = reference_combo.entry.get_text()


	return(reference_combo)


#####################################################################

def setup_event_builder_modifies_menu(self, key):

	import gtk

	modification_list = ['Player', 'Room', 'Item', 'Obstruction']
	modification_menu = gtk.GtkMenu()

	for each in modification_list:
		menu_item = gtk.GtkMenuItem(each)
		menu_item.connect("activate", self.handle_optionmenu_change, key, each)
		modification_menu.append(menu_item)
		menu_item.show()
		if ( ( self.eventTree.has_key( '%s:selection' % key ) ) \
		   and ( self.eventTree['%s:selection' % key ] == each ) ):
			modification_menu.set_active( modification_list.index(each) )

	if ( not self.eventTree.has_key( '%s:selection' % key ) ):
		self.eventTree['%s:selection' % key] = 'Player'

	return(modification_menu)


#####################################################################

def setup_event_builder_modifies_player_menu(self, key):

	import gtk

	modification_list = ['PlayerPoints', 'PlayerExp', 'PlayerHP', 'PlayerMP', \
	                     'PlayerStr', 'PlayerIQ', 'PlayerDex', 'PlayerAgil', \
	                     'PlayerCharisma', 'PlayerArmorLevel', 'PlayerCurrentWeight']
	modification_menu = gtk.GtkMenu()

	for each in modification_list:
		menu_item = gtk.GtkMenuItem(each)
		menu_item.connect("activate", self.handle_optionmenu_change, key, each)
		modification_menu.append(menu_item)
		menu_item.show()
		if ( ( self.eventTree.has_key( '%s:selection' % key ) ) \
		   and ( self.eventTree['%s:selection' % key ] == each ) ):
			modification_menu.set_active( modification_list.index(each) )

	if ( not self.eventTree.has_key( '%s:selection' % key ) ):
		self.eventTree['%s:selection' % key] = 'PlayerPoints'

	return(modification_menu)

#####################################################################

def setup_event_builder_modifies_room_direction_menu(self, key):

	import gtk

	modification_list = ['ToWhichRoom', 'FirstTransitionText', 'TransitionText', \
	                     'FirstTransitionGraphic', 'TransitionGraphic', \
	                     'HasMovedThisWay']
	modification_menu = gtk.GtkMenu()

	for each in modification_list:
		menu_item = gtk.GtkMenuItem(each)
		menu_item.connect("activate", self.handle_optionmenu_change, key, each)
		modification_menu.append(menu_item)
		menu_item.show()
		if ( ( self.eventTree.has_key( '%s:selection' % key ) ) \
		   and ( self.eventTree['%s:selection' % key ] == each ) ):
			modification_menu.set_active( modification_list.index(each) )

	if ( not self.eventTree.has_key( '%s:selection' % key ) ):
		self.eventTree['%s:selection' % key] = modification_list[0]

	return(modification_menu)


#####################################################################

def setup_event_builder_expression_menu(self, key):

	import gtk

	modification_list = ['=', '+', '-']
	modification_menu = gtk.GtkMenu()

	for each in modification_list:
		menu_item = gtk.GtkMenuItem(each)
		menu_item.connect("activate", self.handle_optionmenu_change, key, each)
		modification_menu.append(menu_item)
		menu_item.show()
		if ( ( self.eventTree.has_key( '%s:selection' % key ) ) \
		   and ( self.eventTree['%s:selection' % key ] == each ) ):
			modification_menu.set_active( modification_list.index(each) )

	if ( not self.eventTree.has_key( '%s:selection' % key ) ):
		self.eventTree['%s:selection' % key] = '='

	return(modification_menu)


#####################################################################

def setup_event_builder_comparison_menu(self, key):

	import gtk

	modification_list = ['==', '!=', '>', '<', '>=', '<=']
	modification_menu = gtk.GtkMenu()

	for each in modification_list:
		menu_item = gtk.GtkMenuItem(each)
		menu_item.connect("activate", self.handle_optionmenu_change, key, each)
		modification_menu.append(menu_item)
		menu_item.show()
		if ( ( self.eventTree.has_key( '%s:selection' % key ) ) \
		   and ( self.eventTree['%s:selection' % key ] == each ) ):
			modification_menu.set_active( modification_list.index(each) )

	if ( not self.eventTree.has_key( '%s:selection' % key ) ):
		self.eventTree['%s:selection' % key] = '=='

	return(modification_menu)


#####################################################################

def setup_event_builder_modifies_room_menu(self, key):

	import gtk

	modification_list = ['TextDescription(Long)', 'TextDescription(Short)', \
	                      'DirectionDescription', 'GraphicURL', 'Visited', \
	                      'DirectionObject']
	modification_menu = gtk.GtkMenu()

	for each in modification_list:
		menu_item = gtk.GtkMenuItem(each)
		menu_item.connect("activate", self.handle_optionmenu_change, key, each)
		modification_menu.append(menu_item)
		menu_item.show()
		if ( ( self.eventTree.has_key( '%s:selection' % key ) ) \
		   and ( self.eventTree['%s:selection' % key ] == each ) ):
			modification_menu.set_active( modification_list.index(each) )

	if ( not self.eventTree.has_key( '%s:selection' % key ) ):
		self.eventTree['%s:selection' % key] = 'TextDescription(Long)'

	return(modification_menu)


#####################################################################

def setup_event_builder_modifies_item_menu(self, key):

	import gtk

	modification_list = ['Equipped', 'Weight', 'Bulk', 'TextDescription', \
	                     'Environment_GraphicURL', 'Environment_Graphic_Pos', \
	                     'CloseUp_GraphicURL', 'Icon_GraphicURL', \
	                     'Equipped_GraphicURL']
	modification_menu = gtk.GtkMenu()

	for each in modification_list:
		menu_item = gtk.GtkMenuItem(each)
		menu_item.connect("activate", self.handle_optionmenu_change, key, each)
		modification_menu.append(menu_item)
		menu_item.show()
		if ( ( self.eventTree.has_key( '%s:selection' % key ) ) \
		   and ( self.eventTree['%s:selection' % key ] == each ) ):
			modification_menu.set_active( modification_list.index(each) )

	if ( not self.eventTree.has_key( '%s:selection' % key ) ):
		self.eventTree['%s:selection' % key] = modification_list[0]

	return(modification_menu)


#####################################################################

def setup_event_builder_modifies_obstruction_menu(self, key):

	import gtk

	modification_list = ['Visible', 'TextDescription', 'Environment_GraphicURL', \
	                     'Environment_Graphic_Pos', 'CloseUp_GraphicURL']
	modification_menu = gtk.GtkMenu()

	for each in modification_list:
		menu_item = gtk.GtkMenuItem(each)
		menu_item.connect("activate", self.handle_optionmenu_change, key, each)
		modification_menu.append(menu_item)
		menu_item.show()
		if ( ( self.eventTree.has_key( '%s:selection' % key ) ) \
		   and ( self.eventTree['%s:selection' % key ] == each ) ):
			modification_menu.set_active( modification_list.index(each) )

	if ( not self.eventTree.has_key( '%s:selection' % key ) ):
		self.eventTree['%s:selection' % key] = modification_list[0]

	return(modification_menu)


#####################################################################

def setup_event_builder_requires_room_property_menu(self, key):

	import gtk

	modification_list = ['IsCurrentRoom', 'HasVisited']
	modification_menu = gtk.GtkMenu()

	for each in modification_list:
		menu_item = gtk.GtkMenuItem(each)
		menu_item.connect("activate", self.handle_optionmenu_change, key, each)
		modification_menu.append(menu_item)
		menu_item.show()
		if ( ( self.eventTree.has_key( '%s:selection' % key ) ) \
		   and ( self.eventTree['%s:selection' % key ] == each ) ):
			modification_menu.set_active( modification_list.index(each) )

	if ( not self.eventTree.has_key( '%s:selection' % key ) ):
		self.eventTree['%s:selection' % key] = modification_list[0]

	return(modification_menu)


#####################################################################

def setup_event_builder_requires_item_property_menu(self, key):

	import gtk

	modification_list = ['InInventory', 'IsEquipped', 'ExistsInRoom', 'Weight', 'Bulk']
	modification_menu = gtk.GtkMenu()

	for each in modification_list:
		menu_item = gtk.GtkMenuItem(each)
		menu_item.connect("activate", self.handle_optionmenu_change, key, each)
		modification_menu.append(menu_item)
		menu_item.show()
		if ( ( self.eventTree.has_key( '%s:selection' % key ) ) \
		   and ( self.eventTree['%s:selection' % key ] == each ) ):
			modification_menu.set_active( modification_list.index(each) )

	if ( not self.eventTree.has_key( '%s:selection' % key ) ):
		self.eventTree['%s:selection' % key] = modification_list[0]

	return(modification_menu)


#####################################################################

def setup_event_builder_requires_obstruction_property_menu(self, key):

	import gtk

	modification_list = ['ExistsInRoom', 'ExistsInRoomDirection', 'IsVisible']
	modification_menu = gtk.GtkMenu()

	for each in modification_list:
		menu_item = gtk.GtkMenuItem(each)
		menu_item.connect("activate", self.handle_optionmenu_change, key, each)
		modification_menu.append(menu_item)
		menu_item.show()
		if ( ( self.eventTree.has_key( '%s:selection' % key ) ) \
		   and ( self.eventTree['%s:selection' % key ] == each ) ):
			modification_menu.set_active( modification_list.index(each) )

	if ( not self.eventTree.has_key( '%s:selection' % key ) ):
		self.eventTree['%s:selection' % key] = modification_list[0]

	return(modification_menu)


#####################################################################

def setup_event_builder_requires_and_or_menu(self, key):

	import gtk

	modification_list = ['and', 'or']
	modification_menu = gtk.GtkMenu()

	for each in modification_list:
		menu_item = gtk.GtkMenuItem(each)
		menu_item.connect("activate", self.handle_optionmenu_change, key, each)
		modification_menu.append(menu_item)
		menu_item.show()
		if ( ( self.eventTree.has_key( '%s:selection' % key ) ) \
		   and ( self.eventTree['%s:selection' % key ] == each ) ):
			modification_menu.set_active( modification_list.index(each) )

	if ( not self.eventTree.has_key( '%s:selection' % key ) ):
		self.eventTree['%s:selection' % key] = modification_list[0]

	return(modification_menu)


#####################################################################

def setup_radiobutton_vbox(self, key_prefix, key_index, default_truth_boolean):

	import gtk

	radiobutton_vbox = gtk.GtkVBox() # homogeneous, spacing

	true_radiobutton = gtk.GtkRadioButton(label='True')
	false_radiobutton = gtk.GtkRadioButton(true_radiobutton, label='False')

	if self.eventTree.has_key('%s_true_radiobutton:%s:selection' % (key_prefix, key_index)):
		# radiobuttons have been built before - we should use their last setting
		if self.eventTree['%s_true_radiobutton:%s:selection' % (key_prefix, key_index)]:
			true_radiobutton.set_active(1)
		else:
			false_radiobutton.set_active(1)
	else:
		# radiobuttons have not been built before - we should load their setting from memory
		if (default_truth_boolean):
			true_radiobutton.set_active(1)
			self.eventTree['%s_true_radiobutton:%s:selection' % (key_prefix, key_index)] = 1
			self.eventTree['%s_false_radiobutton:%s:selection' % (key_prefix, key_index)] = 0
		else:
			false_radiobutton.set_active(1)
			self.eventTree['%s_true_radiobutton:%s:selection' % (key_prefix, key_index)] = 0
			self.eventTree['%s_false_radiobutton:%s:selection' % (key_prefix, key_index)] = 1

	true_radiobutton.connect("toggled", self.handle_radiobutton_toggled, '%s_true_radiobutton:%s' % (key_prefix, key_index))
	false_radiobutton.connect("toggled", self.handle_radiobutton_toggled, '%s_false_radiobutton:%s' % (key_prefix, key_index))

	radiobutton_vbox.pack_start(true_radiobutton)
	radiobutton_vbox.pack_start(false_radiobutton)

	self.eventTree['%s_true_radiobutton:%s' % (key_prefix, key_index)] = true_radiobutton
	self.eventTree['%s_false_radiobutton:%s' % (key_prefix, key_index)] = false_radiobutton

	true_radiobutton.show()
	false_radiobutton.show()

	return(radiobutton_vbox)


#####################################################################

def add_object_toolbar(self):

	self.eventTree['display_object_toolbar'] = 1
	self.rebuild_object_toolbar()


#####################################################################

def remove_object_toolbar(self):

	self.eventTree['object_toolbar:0'].destroy()
	del self.eventTree['object_toolbar:0']
	self.eventTree['display_object_toolbar'] = 0


#####################################################################

def add_new_requirement_toolbar(self):

	import gtk, string

	eventTree_widgets = self.eventTree.keys()
	eventTree_widgets.sort()

	total_requirement_toolbars = 0

	for each in eventTree_widgets:
		if ( string.find(each, 'requirement_toolbar') != -1):
			total_requirement_toolbars = total_requirement_toolbars + 1

	key_index = total_requirement_toolbars # we start with the 0th toolbar, so this line works

	if (self.debug_mode):
		print "Requirement toolbar key index: %i" % key_index

	# Setup requires_label
	requires_label = gtk.GtkLabel(" Requires: ")
	requires_label.show()

	# Setup requires_not_checkbutton
	requires_not_checkbutton = gtk.GtkCheckButton(' (Not) ')
	self.eventTree['requires_not_checkbutton:%i' % key_index] = requires_not_checkbutton
	# Setup toggled status
	requires_not_checkbutton.set_active( 0 )
	requires_not_checkbutton.show()

	# Setup requirement_type_vbox
	requirement_type_menu = self.setup_event_builder_modifies_menu('requirement_type_optionmenu:%i' % key_index)
	requirement_type_optionmenu = gtk.GtkOptionMenu()
	requirement_type_optionmenu.set_menu( requirement_type_menu )
	requirement_type_vbox = self.create_event_widget_container(\
					'requirement_type', key_index, \
					'<Type>', requirement_type_optionmenu, 'optionmenu')

	# Setup require_player_menu
	require_player_player_menu = self.setup_event_builder_modifies_player_menu('require_player_player_optionmenu:%s' % key_index)
	require_player_player_optionmenu = gtk.GtkOptionMenu()
	require_player_player_optionmenu.set_menu( require_player_player_menu )
	require_player_player_vbox = self.create_event_widget_container(\
					'require_player_player', key_index, \
					'<Player Attributes>', require_player_player_optionmenu, 'optionmenu')

	# Setup requires_player_comparison_vbox
	requires_player_comparison_menu = self.setup_event_builder_comparison_menu('requires_player_comparison_optionmenu:%s' % key_index)
	requires_player_comparison_optionmenu = gtk.GtkOptionMenu()
	requires_player_comparison_optionmenu.set_menu( requires_player_comparison_menu )
	requires_player_comparison_vbox = self.create_event_widget_container(\
					'requires_player_comparison', key_index, \
					'<Comparison>', requires_player_comparison_optionmenu, 'optionmenu')

	# Setup requires_player_comparison_number_vbox
	requires_player_comparison_points_entry = gtk.GtkEntry()
	if self.eventTree.has_key('requires_player_comparison_points_entry:%i:selection' % key_index):
		requires_player_comparison_points_entry.set_text( self.eventTree['requires_player_comparison_points_entry:%i:selection' % key_index] )
	elif (self.playerInformation.points != -1):
		requires_player_comparison_points_entry.set_text( '%i' % self.playerInformation.points )
		self.eventTree['requires_player_comparison_points_entry:%s:selection' % key_index] = '%i' % self.playerInformation.points
	else:
		requires_player_comparison_points_entry.set_text( '0' )
		self.eventTree['requires_player_comparison_points_entry:%s:selection' % key_index] = '0'
	requires_player_comparison_points_vbox = self.create_event_widget_container(\
					'requires_player_comparison_points', key_index, \
					'<Number>', requires_player_comparison_points_entry, 'entry')

	# Setup new effect toolbar
	requirement_toolbar = gtk.GtkToolbar(gtk.ORIENTATION_HORIZONTAL, gtk.TOOLBAR_BOTH)
	requirement_toolbar.append_widget(requires_label, "", "")
	requirement_toolbar.append_widget(requires_not_checkbutton, "", "")
	requirement_toolbar.append_widget(requirement_type_vbox, "", "")
	requirement_toolbar.append_widget(require_player_player_vbox, "", "")
	requirement_toolbar.append_widget(requires_player_comparison_vbox, "", "")
	requirement_toolbar.append_widget(requires_player_comparison_points_vbox, "", "")

	self.eventTree['requirement_toolbar:%i' % key_index ] = requirement_toolbar
	requirement_toolbar.show()


#####################################################################

def remove_last_requirement_toolbar(self):

	import gtk, string

	eventTree_widgets = self.eventTree.keys()
	eventTree_widgets.sort()

	total_requirement_toolbars = 0

	for each in eventTree_widgets:
		if ( string.find(each, 'requirement_toolbar') != -1):
			total_requirement_toolbars = total_requirement_toolbars + 1

	if (total_requirement_toolbars > 0):

		index = total_requirement_toolbars - 1 # we will remove the last toolbar according to index
		del self.eventTree['requirement_toolbar:%i' % index ]

		self.rebuild_action_toolbar()
		self.rebuild_object_toolbar()
		self.rebuild_requirement_toolbars()
		self.rebuild_yeilds_and_button_toolbars()
		self.rebuild_effect_toolbars()
		self.display_event_builder()


#####################################################################

def add_new_effect_toolbar(self):

	import gtk, string

	eventTree_widgets = self.eventTree.keys()
	eventTree_widgets.sort()

	total_effect_toolbars = 0

	for each in eventTree_widgets:
		if ( string.find(each, 'effect_toolbar') != -1):
			total_effect_toolbars = total_effect_toolbars + 1

	key_index = total_effect_toolbars # we start with the 0th toolbar, so this line works


	# Setup effect vbox
	effect_menu = self.setup_event_builder_effect_menu('effect_optionmenu:%i' % key_index )
	effect_optionmenu = gtk.GtkOptionMenu()
	effect_optionmenu.set_menu(effect_menu)
	effect_vbox = self.create_event_widget_container(\
	              'effect', key_index, \
	              '<Effect>', effect_optionmenu, 'optionmenu')


	# Setup adds_object_vbox
	effect_adds_object_menu = self.setup_event_builder_object_menu('effect_adds_object_optionmenu:%i' % key_index )
	effect_adds_object_optionmenu = gtk.GtkOptionMenu()
	effect_adds_object_optionmenu.set_menu(effect_adds_object_menu)
	effect_adds_object_vbox = self.create_event_widget_container(\
	              'effect_adds_object', key_index, \
	              '<Object>', effect_adds_object_optionmenu, 'optionmenu')


	# Setup adds_reference_vbox
	if not self.eventTree.has_key('effect_adds_object_optionmenu:%s:selection' % key_index):
		self.eventTree['effect_adds_object_optionmenu:%i:selection' % key_index] = ''
	effect_adds_reference_combo = self.setup_event_builder_reference_combo(None, 'effect_adds_reference_combo:%i' % key_index , self.eventTree['effect_adds_object_optionmenu:%i:selection' % key_index])
	effect_adds_reference_vbox = self.create_event_widget_container(\
	              'effect_adds_reference', key_index, \
	              '<Reference>', effect_adds_reference_combo, 'combo')


	# Setup adds_preposition_vbox
	effect_adds_preposition_combo = self.setup_event_builder_preposition_combo('effect_adds_preposition_combo:%i' % key_index )
	effect_adds_preposition_combo.entry.set_text('to')
	self.eventTree['effect_adds_preposition_combo:%i:selection' % key_index] = 'to'
	effect_adds_preposition_vbox = self.create_event_widget_container(\
	              'effect_adds_preposition', key_index, \
	              '<Preposition>', effect_adds_preposition_combo, 'combo')


	# Setup effect_adds_itemlocation_vbox
	effect_adds_itemlocation_menu = self.setup_event_builder_itemlocation_menu('effect_adds_itemlocation_optionmenu:%i' % key_index )
	effect_adds_itemlocation_optionmenu = gtk.GtkOptionMenu()
	effect_adds_itemlocation_optionmenu.set_menu(effect_adds_itemlocation_menu)
	effect_adds_itemlocation_vbox = self.create_event_widget_container(\
	              'effect_adds_itemlocation', key_index, \
	              '<Object>', effect_adds_itemlocation_optionmenu, 'optionmenu')


	# Setup new effect toolbar
	effect_toolbar = gtk.GtkToolbar(gtk.ORIENTATION_HORIZONTAL, gtk.TOOLBAR_BOTH)
	effect_toolbar.append_widget(effect_vbox, "", "")
	effect_toolbar.append_widget(effect_adds_object_vbox, "", "")
	effect_toolbar.append_widget(effect_adds_reference_vbox, "", "")
	effect_toolbar.append_widget(effect_adds_preposition_vbox, "", "")
	effect_toolbar.append_widget(effect_adds_itemlocation_vbox, "", "")

	self.eventTree['effect_toolbar:%i' % key_index ] = effect_toolbar
	effect_toolbar.show()


#####################################################################

def remove_last_effect_toolbar(self):

	import gtk, string

	eventTree_widgets = self.eventTree.keys()
	eventTree_widgets.sort()

	total_effect_toolbars = 0

	for each in eventTree_widgets:
		if ( string.find(each, 'effect_toolbar') != -1):
			total_effect_toolbars = total_effect_toolbars + 1

	if (total_effect_toolbars > 1):

		index = total_effect_toolbars - 1 # we will remove the last toolbar according to index
		del self.eventTree['effect_toolbar:%i' % index ]

		self.rebuild_action_toolbar()
		self.rebuild_object_toolbar()
		self.rebuild_requirement_toolbars()
		self.rebuild_yeilds_and_button_toolbars()
		self.rebuild_effect_toolbars()
		self.display_event_builder()


#####################################################################

def handle_action_selection(self, obj, new_selection):
	self.eventTree['action_optionmenu:0:selection'] = new_selection


#####################################################################

def handle_optionmenu_change(self, obj, key, selection):

	self.eventTree['%s:selection' % key] = selection

	self.rebuild_action_toolbar()
	self.rebuild_object_toolbar()
	self.rebuild_requirement_toolbars()
	self.rebuild_yeilds_and_button_toolbars()
	self.rebuild_effect_toolbars()
	self.display_event_builder()


#####################################################################

def handle_entry_change(self, obj, key):

	self.eventTree['%s:selection' % key] = obj.get_text()
	if (self.debug_mode):
		print "%s changes to %s" % ( key, self.eventTree['%s:selection' % key] )

#####################################################################

def handle_radiobutton_toggled(self, obj, key):

	self.eventTree['%s:selection' % key] = obj.get_active()


#####################################################################

def rebuild_action_toolbar(self):

	import gtk

	key_index = '0'

	# Setup action vbox
	action_menu = self.setup_event_builder_action_menu()
	action_optionmenu = gtk.GtkOptionMenu()
	action_optionmenu.set_menu(action_menu)
	action_vbox = self.create_event_widget_container(\
	        'action', key_index, \
	        '<Action>', action_optionmenu, 'optionmenu')

	# Setup object vbox
	object_menu = self.setup_event_builder_object_menu('object_optionmenu:%s' % key_index)
	object_optionmenu = gtk.GtkOptionMenu()
	object_optionmenu.set_menu(object_menu)
	object_vbox = self.create_event_widget_container(\
	        'object', key_index, \
	        '<Object>', object_optionmenu, 'optionmenu')

	# Setup reference_vbox
	if not self.eventTree.has_key('object_optionmenu:%s:selection' % key_index):
		self.eventTree['object_optionmenu:0:selection'] = ''
	reference_combo = self.setup_event_builder_reference_combo(None, 'reference_combo:%s' % key_index, self.eventTree['object_optionmenu:0:selection'])
	reference_vbox = self.create_event_widget_container(\
	        'reference', key_index, \
	        '<Reference>', reference_combo, 'combo')

	# Setup action toolbar
	action_toolbar = gtk.GtkToolbar(gtk.ORIENTATION_HORIZONTAL, gtk.TOOLBAR_BOTH)
	action_toolbar.append_widget(action_vbox, "", "") # widget, tooltip, private tooltip
	action_toolbar.append_widget(object_vbox, "", "")
	action_toolbar.append_widget(reference_vbox, "", "")
	self.eventTree['action_toolbar:%s' % key_index] = action_toolbar
	action_toolbar.show()


#####################################################################

def rebuild_object_toolbar(self):

	if (self.eventTree['display_object_toolbar']):

		import gtk

		key_index = '0'

		# Setup object2_preposition_vbox
		if not self.eventTree.has_key('object2_preposition_combo:%s:selection' % key_index):
			object2_preposition_combo = self.setup_event_builder_preposition_combo('object2_preposition_combo:%s' % key_index )
			object2_preposition_combo.entry.set_text('to')
			self.eventTree['object2_preposition_combo:%s:selection' % key_index] = 'on'
		else:
			# It is necessary to have two calls to setup_event_builder_preposition_combo
			# so that the user's last selection will persist even after the object toolbar is removed
			object2_preposition_combo = self.setup_event_builder_preposition_combo('object2_preposition_combo:%s' % key_index )
		object2_preposition_vbox = self.create_event_widget_container(\
						'object2_preposition', key_index, \
						'<Preposition>', object2_preposition_combo, 'combo')

		# Setup object2_vbox
		object2_menu = self.setup_event_builder_object_menu('object2_optionmenu:%s' % key_index)
		object2_optionmenu = gtk.GtkOptionMenu()
		object2_optionmenu.set_menu(object2_menu)
		object2_vbox = self.create_event_widget_container(\
				'object2', key_index, \
				'<Object>', object2_optionmenu, 'optionmenu')

		# Setup object2_reference_vbox
		if not self.eventTree.has_key('object2_optionmenu:%s:selection' % key_index):
			self.eventTree['object2_optionmenu:0:selection'] = ''
		object2_reference_combo = self.setup_event_builder_reference_combo(None, 'object2_reference_combo:%s' % key_index, self.eventTree['object2_optionmenu:0:selection'])
		object2_reference_vbox = self.create_event_widget_container(\
				'object2_reference', key_index, \
				'<Reference>', object2_reference_combo, 'combo')

		# Setup object_toolbar
		object_toolbar = gtk.GtkToolbar(gtk.ORIENTATION_HORIZONTAL, gtk.TOOLBAR_BOTH)
		object_toolbar.append_widget(object2_preposition_vbox, "", "") # widget, tooltip, private tooltip
		object_toolbar.append_widget(object2_vbox, "", "")
		object_toolbar.append_widget(object2_reference_vbox, "", "")
		self.eventTree['object_toolbar:%s' % key_index] = object_toolbar
		object_toolbar.show()


#####################################################################

def rebuild_requirement_toolbars(self):

	import gtk, string

	eventTree_widgets = self.eventTree.keys()
	eventTree_widgets.sort()

	for each in eventTree_widgets:
		if ( string.find(each, 'requirement_toolbar') != -1):

			key_index = string.split(each, ':')[1]
			key_index = string.atoi( key_index )

			self.eventTree[each].destroy()

			# Setup effect toolbar
			requirement_toolbar = gtk.GtkToolbar(gtk.ORIENTATION_HORIZONTAL, gtk.TOOLBAR_BOTH)


			# Setup "and/or" optionmenu if necessary
			if ( key_index > 0):
				requires_and_or_menu = self.setup_event_builder_requires_and_or_menu('requires_and_or_menu:%i' % key_index)
				requires_and_or_optionmenu = gtk.GtkOptionMenu()
				requires_and_or_optionmenu.set_menu( requires_and_or_menu )
				requires_and_or_vbox = self.create_event_widget_container(\
								'requires_and_or', key_index, \
								'<Operator>', requires_and_or_optionmenu, 'optionmenu')


				requirement_toolbar.append_widget(requires_and_or_vbox, "", "")


			# Setup requires_label
			requires_label = gtk.GtkLabel(" Requires: ")
			requires_label.show()


			requirement_toolbar.append_widget(requires_label, "", "")


			# Setup requires_not_checkbutton
			requires_not_checkbutton = gtk.GtkCheckButton(' (Not) ')
			self.eventTree['requires_not_checkbutton:%i' % key_index] = requires_not_checkbutton

			# Setup toggled status
			requires_not_checkbutton.set_active( 0 )
			requires_not_checkbutton.show()

			requirement_toolbar.append_widget(requires_not_checkbutton, "", "")

			# Setup requirement_type_vbox
			requirement_type_menu = self.setup_event_builder_modifies_menu('requirement_type_optionmenu:%i' % key_index)
			requirement_type_optionmenu = gtk.GtkOptionMenu()
			requirement_type_optionmenu.set_menu( requirement_type_menu )
			requirement_type_vbox = self.create_event_widget_container(\
							'requirement_type', key_index, \
							'<Type>', requirement_type_optionmenu, 'optionmenu')


			requirement_toolbar.append_widget(requirement_type_vbox, "", "")


			if ( self.eventTree['requirement_type_optionmenu:%i:selection' % key_index] == 'Player' ):

				# Setup require_player_menu
				require_player_menu = self.setup_event_builder_modifies_player_menu('require_player_optionmenu:%s' % key_index)
				require_player_optionmenu = gtk.GtkOptionMenu()
				require_player_optionmenu.set_menu( require_player_menu )
				require_player_vbox = self.create_event_widget_container(\
								'require_player', key_index, \
								'<Player Attributes>', require_player_optionmenu, 'optionmenu')


				requirement_toolbar.append_widget(require_player_vbox, "", "")


				# Setup requires_player_comparison_vbox
				requires_player_comparison_menu = self.setup_event_builder_comparison_menu('requires_player_comparison_optionmenu:%s' % key_index)
				requires_player_comparison_optionmenu = gtk.GtkOptionMenu()
				requires_player_comparison_optionmenu.set_menu( requires_player_comparison_menu )
				requires_player_comparison_vbox = self.create_event_widget_container(\
								'requires_player_comparison', key_index, \
								'<Comparison>', requires_player_comparison_optionmenu, 'optionmenu')


				requirement_toolbar.append_widget(requires_player_comparison_vbox, "", "")


				if ( self.eventTree['require_player_optionmenu:%i:selection' % key_index] == 'PlayerPoints' ):
					# Setup requires_player_comparison_points_vbox
					requires_player_comparison_points_entry = gtk.GtkEntry()
					if self.eventTree.has_key('requires_player_comparison_points_entry:%i:selection' % key_index):
						requires_player_comparison_points_entry.set_text( self.eventTree['requires_player_comparison_points_entry:%i:selection' % key_index] )
					elif (self.playerInformation.points != -1):
						requires_player_comparison_points_entry.set_text( self.playerInformation.points )
						self.eventTree['requires_player_comparison_points_entry:%s:selection' % key_index] = self.playerInformation.points
					else:
						requires_player_comparison_points_entry.set_text( '0' )
						self.eventTree['requires_player_comparison_points_entry:%s:selection' % key_index] = '0'
					requires_player_comparison_points_vbox = self.create_event_widget_container(\
									'requires_player_comparison_points', key_index, \
									'<Number>', requires_player_comparison_points_entry, 'entry')


					requirement_toolbar.append_widget(requires_player_comparison_points_vbox, "", "")


				elif ( self.eventTree['require_player_optionmenu:%i:selection' % key_index] == 'PlayerExp' ):
					# Setup requires_player_comparison_exp_vbox
					requires_player_comparison_exp_entry = gtk.GtkEntry()
					if self.eventTree.has_key('requires_player_comparison_exp_entry:%i:selection' % key_index):
						requires_player_comparison_exp_entry.set_text( self.eventTree['requires_player_comparison_exp_entry:%i:selection' % key_index] )
					elif (self.playerInformation.experience != -1):
						requires_player_comparison_exp_entry.set_text( self.playerInformation.experience )
						self.eventTree['requires_player_comparison_exp_entry:%s:selection' % key_index] = self.playerInformation.experience
					else:
						requires_player_comparison_exp_entry.set_text( '0' )
						self.eventTree['requires_player_comparison_exp_entry:%s:selection' % key_index] = '0'
					requires_player_comparison_exp_vbox = self.create_event_widget_container(\
									'requires_player_comparison_exp', key_index, \
									'<Number>', requires_player_comparison_exp_entry, 'entry')


					requirement_toolbar.append_widget(requires_player_comparison_exp_vbox, "", "")


				elif ( self.eventTree['require_player_optionmenu:%i:selection' % key_index] == 'PlayerHP' ):
					# Setup requires_player_comparison_hp_vbox
					requires_player_comparison_hp_entry = gtk.GtkEntry()
					if self.eventTree.has_key('requires_player_comparison_hp_entry:%i:selection' % key_index):
						requires_player_comparison_hp_entry.set_text( self.eventTree['requires_player_comparison_hp_entry:%i:selection' % key_index] )
					elif (self.playerInformation.hp != -1):
						requires_player_comparison_hp_entry.set_text( self.playerInformation.hp )
						self.eventTree['requires_player_comparison_hp_entry:%s:selection' % key_index] = self.playerInformation.hp
					else:
						requires_player_comparison_hp_entry.set_text( '0' )
						self.eventTree['requires_player_comparison_hp_entry:%s:selection' % key_index] = '0'
					requires_player_comparison_hp_vbox = self.create_event_widget_container(\
									'requires_player_comparison_hp', key_index, \
									'<Number>', requires_player_comparison_hp_entry, 'entry')


					requirement_toolbar.append_widget(requires_player_comparison_hp_vbox, "", "")


				elif ( self.eventTree['require_player_optionmenu:%i:selection' % key_index] == 'PlayerMP' ):
					# Setup requires_player_comparison_mp_vbox
					requires_player_comparison_mp_entry = gtk.GtkEntry()
					if self.eventTree.has_key('requires_player_comparison_mp_entry:%i:selection' % key_index):
						requires_player_comparison_mp_entry.set_text( self.eventTree['requires_player_comparison_mp_entry:%i:selection' % key_index] )
					elif (self.playerInformation.mp != -1):
						requires_player_comparison_mp_entry.set_text( self.playerInformation.mp )
						self.eventTree['requires_player_comparison_mp_entry:%s:selection' % key_index] = self.playerInformation.mp
					else:
						requires_player_comparison_mp_entry.set_text( '0' )
						self.eventTree['requires_player_comparison_mp_entry:%s:selection' % key_index] = '0'
					requires_player_comparison_mp_vbox = self.create_event_widget_container(\
									'requires_player_comparison_mp', key_index, \
									'<Number>', requires_player_comparison_mp_entry, 'entry')


					requirement_toolbar.append_widget(requires_player_comparison_mp_vbox, "", "")


				elif ( self.eventTree['require_player_optionmenu:%i:selection' % key_index] == 'PlayerStr' ):
					# Setup requires_player_comparison_strength_vbox
					requires_player_comparison_strength_entry = gtk.GtkEntry()
					if self.eventTree.has_key('requires_player_comparison_strength_entry:%i:selection' % key_index):
						requires_player_comparison_strength_entry.set_text( self.eventTree['requires_player_comparison_strength_entry:%i:selection' % key_index] )
					elif (self.playerInformation.strength != -1):
						requires_player_comparison_strength_entry.set_text( self.playerInformation.strength )
						self.eventTree['requires_player_comparison_strength_entry:%s:selection' % key_index] = self.playerInformation.strength
					else:
						requires_player_comparison_strength_entry.set_text( '0' )
						self.eventTree['requires_player_comparison_strength_entry:%s:selection' % key_index] = '0'
					requires_player_comparison_strength_vbox = self.create_event_widget_container(\
									'requires_player_comparison_strength', key_index, \
									'<Number>', requires_player_comparison_strength_entry, 'entry')


					requirement_toolbar.append_widget(requires_player_comparison_strength_vbox, "", "")


				elif ( self.eventTree['require_player_optionmenu:%i:selection' % key_index] == 'PlayerIQ' ):
					# Setup requires_player_comparison_intelligence_vbox
					requires_player_comparison_intelligence_entry = gtk.GtkEntry()
					if self.eventTree.has_key('requires_player_comparison_intelligence_entry:%i:selection' % key_index):
						requires_player_comparison_intelligence_entry.set_text( self.eventTree['requires_player_comparison_intelligence_entry:%i:selection' % key_index] )
					elif (self.playerInformation.intelligence != -1):
						requires_player_comparison_intelligence_entry.set_text( self.playerInformation.intelligence )
						self.eventTree['requires_player_comparison_intelligence_entry:%s:selection' % key_index] = self.playerInformation.intelligence
					else:
						requires_player_comparison_intelligence_entry.set_text( '0' )
						self.eventTree['requires_player_comparison_intelligence_entry:%s:selection' % key_index] = '0'
					requires_player_comparison_intelligence_vbox = self.create_event_widget_container(\
									'requires_player_comparison_intelligence', key_index, \
									'<Number>', requires_player_comparison_intelligence_entry, 'entry')


					requirement_toolbar.append_widget(requires_player_comparison_intelligence_vbox, "", "")


				elif ( self.eventTree['require_player_optionmenu:%i:selection' % key_index] == 'PlayerDex' ):
					# Setup requires_player_comparison_dexterity_vbox
					requires_player_comparison_dexterity_entry = gtk.GtkEntry()
					if self.eventTree.has_key('requires_player_comparison_dexterity_entry:%i:selection' % key_index):
						requires_player_comparison_dexterity_entry.set_text( self.eventTree['requires_player_comparison_dexterity_entry:%i:selection' % key_index] )
					elif (self.playerInformation.dexterity != -1):
						requires_player_comparison_dexterity_entry.set_text( "%i" % self.playerInformation.dexterity )
						self.eventTree['requires_player_comparison_dexterity_entry:%s:selection' % key_index] = self.playerInformation.dexterity
					else:
						requires_player_comparison_dexterity_entry.set_text( '0' )
						self.eventTree['requires_player_comparison_dexterity_entry:%s:selection' % key_index] = '0'
					requires_player_comparison_dexterity_vbox = self.create_event_widget_container(\
									'requires_player_comparison_dexterity', key_index, \
									'<Number>', requires_player_comparison_dexterity_entry, 'entry')


					requirement_toolbar.append_widget(requires_player_comparison_dexterity_vbox, "", "")



				elif ( self.eventTree['require_player_optionmenu:%i:selection' % key_index] == 'PlayerAgil' ):
					# Setup requires_player_comparison_agility_vbox
					requires_player_comparison_agility_entry = gtk.GtkEntry()
					if self.eventTree.has_key('requires_player_comparison_agility_entry:%i:selection' % key_index):
						requires_player_comparison_agility_entry.set_text( self.eventTree['requires_player_comparison_agility_entry:%i:selection' % key_index] )
					elif (self.playerInformation.agility != -1):
						requires_player_comparison_agility_entry.set_text( self.playerInformation.agility )
						self.eventTree['requires_player_comparison_agility_entry:%s:selection' % key_index] = self.playerInformation.agility
					else:
						requires_player_comparison_agility_entry.set_text( '0' )
						self.eventTree['requires_player_comparison_agility_entry:%s:selection' % key_index] = '0'
					requires_player_comparison_agility_vbox = self.create_event_widget_container(\
									'requires_player_comparison_agility', key_index, \
									'<Number>', requires_player_comparison_agility_entry, 'entry')


					requirement_toolbar.append_widget(requires_player_comparison_agility_vbox, "", "")



				elif ( self.eventTree['require_player_optionmenu:%i:selection' % key_index] == 'PlayerCharisma' ):
					# Setup requires_player_comparison_charisma_vbox
					requires_player_comparison_charisma_entry = gtk.GtkEntry()
					if self.eventTree.has_key('requires_player_comparison_charisma_entry:%i:selection' % key_index):
						requires_player_comparison_charisma_entry.set_text( self.eventTree['requires_player_comparison_charisma_entry:%i:selection' % key_index] )
					elif (self.playerInformation.charisma != -1):
						requires_player_comparison_charisma_entry.set_text( self.playerInformation.charisma )
						self.eventTree['requires_player_comparison_charisma_entry:%s:selection' % key_index] = self.playerInformation.charisma
					else:
						requires_player_comparison_charisma_entry.set_text( '0' )
						self.eventTree['requires_player_comparison_charisma_entry:%s:selection' % key_index] = '0'
					requires_player_comparison_charisma_vbox = self.create_event_widget_container(\
									'requires_player_comparison_charisma', key_index, \
									'<Number>', requires_player_comparison_charisma_entry, 'entry')


					requirement_toolbar.append_widget(requires_player_comparison_charisma_vbox, "", "")



				elif ( self.eventTree['require_player_optionmenu:%i:selection' % key_index] == 'PlayerArmorLevel' ):
					# Setup requires_player_comparison_armor_level_vbox
					requires_player_comparison_armor_level_entry = gtk.GtkEntry()
					if self.eventTree.has_key('requires_player_comparison_armor_level_entry:%i:selection' % key_index):
						requires_player_comparison_armor_level_entry.set_text( self.eventTree['requires_player_comparison_armor_level_entry:%i:selection' % key_index] )
					elif (self.playerInformation.armor_level != -1):
						requires_player_comparison_armor_level_entry.set_text( self.playerInformation.armor_level )
						self.eventTree['requires_player_comparison_armor_level_entry:%s:selection' % key_index] = self.playerInformation.armor_level
					else:
						requires_player_comparison_armor_level_entry.set_text( '0' )
						self.eventTree['requires_player_comparison_armor_level_entry:%s:selection' % key_index] = '0'
					requires_player_comparison_armor_level_vbox = self.create_event_widget_container(\
									'requires_player_comparison_armor_level', key_index, \
									'<Number>', requires_player_comparison_armor_level_entry, 'entry')


					requirement_toolbar.append_widget(requires_player_comparison_armor_level_vbox, "", "")



				elif ( self.eventTree['require_player_optionmenu:%i:selection' % key_index] == 'PlayerCurrentWeight' ):
					# Setup requires_player_comparison_current_weight_vbox
					requires_player_comparison_current_weight_entry = gtk.GtkEntry()
					if self.eventTree.has_key('requires_player_comparison_current_weight_entry:%i:selection' % key_index):
						requires_player_comparison_current_weight_entry.set_text( self.eventTree['requires_player_comparison_current_weight_entry:%i:selection' % key_index] )
					elif (self.playerInformation.current_weight != -1):
						requires_player_comparison_current_weight_entry.set_text( self.playerInformation.current_weight )
						self.eventTree['requires_player_comparison_current_weight_entry:%s:selection' % key_index] = self.playerInformation.current_weight
					else:
						requires_player_comparison_current_weight_entry.set_text( '0' )
						self.eventTree['requires_player_comparison_current_weight_entry:%s:selection' % key_index] = '0'
					requires_player_comparison_current_weight_vbox = self.create_event_widget_container(\
									'requires_player_comparison_current_weight', key_index, \
									'<Number>', requires_player_comparison_current_weight_entry, 'entry')


					requirement_toolbar.append_widget(requires_player_comparison_current_weight_vbox, "", "")



			elif ( self.eventTree['requirement_type_optionmenu:%i:selection' % key_index] == 'Room' ):
				# Setup requirement_room_reference_combo
				requirement_room_reference_combo = self.setup_event_builder_room_reference_combo('requirement_room_reference_combo:%s' % key_index)
				requirement_room_reference_vbox = self.create_event_widget_container(\
								'requirement_room_reference', key_index, \
								'<Room Reference>', requirement_room_reference_combo, 'combo')

				# Setup requires_room_property_optionmenu
				requires_room_property_menu = self.setup_event_builder_requires_room_property_menu('requires_room_property_optionmenu:%s' % key_index)
				requires_room_property_optionmenu = gtk.GtkOptionMenu()
				requires_room_property_optionmenu.set_menu( requires_room_property_menu )
				requires_room_property_vbox = self.create_event_widget_container(\
								'requires_room_property', key_index, \
								'<Room Property>', requires_room_property_optionmenu, 'optionmenu')


				requirement_toolbar.append_widget(requirement_room_reference_vbox, "", "")
				requirement_toolbar.append_widget(requires_room_property_vbox, "", "")



			elif ( self.eventTree['requirement_type_optionmenu:%i:selection' % key_index] == 'Item' ):
				# Setup requirement_item_reference_combo
				requirement_item_reference_combo = self.setup_event_builder_reference_combo(None, 'requirement_item_reference_combo:%s' % key_index, 'Item')
				requirement_item_reference_vbox = self.create_event_widget_container(\
								'requirement_item_reference', key_index, \
								'<Item Reference>', requirement_item_reference_combo, 'combo')

				# Setup requires_item_property_optionmenu
				requires_item_property_menu = self.setup_event_builder_requires_item_property_menu('requires_item_property_optionmenu:%s' % key_index)
				requires_item_property_optionmenu = gtk.GtkOptionMenu()
				requires_item_property_optionmenu.set_menu( requires_item_property_menu )
				requires_item_property_vbox = self.create_event_widget_container(\
								'requires_item_property', key_index, \
								'<Item Property>', requires_item_property_optionmenu, 'optionmenu')


				requirement_toolbar.append_widget(requirement_item_reference_vbox, "", "")
				requirement_toolbar.append_widget(requires_item_property_vbox, "", "")


				if ( self.eventTree['requires_item_property_optionmenu:%i:selection' % key_index] == 'ExistsInRoom' ):
					# Setup requires_exists_in_room_reference_combo
					requires_exists_in_room_reference_combo = self.setup_event_builder_room_reference_combo('requires_exists_in_room_reference_combo:%s' % key_index)
					requires_exists_in_room_reference_vbox = self.create_event_widget_container(\
									'requires_exists_in_room_reference', key_index, \
									'<Room Reference>', requires_exists_in_room_reference_combo, 'combo')


					requirement_toolbar.append_widget( requires_exists_in_room_reference_vbox, "", "" )


				elif ( self.eventTree['requires_item_property_optionmenu:%i:selection' % key_index] == 'Weight' ):

					# Setup requires_item_weight_comparison_vbox
					requires_item_weight_comparison_menu = self.setup_event_builder_comparison_menu('requires_item_weight_comparison_optionmenu:%s' % key_index)
					requires_item_weight_comparison_optionmenu = gtk.GtkOptionMenu()
					requires_item_weight_comparison_optionmenu.set_menu( requires_item_weight_comparison_menu )
					requires_item_weight_comparison_vbox = self.create_event_widget_container(\
									'requires_item_weight_comparison', key_index, \
									'<Comparison>', requires_item_weight_comparison_optionmenu, 'optionmenu')


					# Setup requires_item_comparison_weight_vbox
					requires_item_comparison_weight_entry = gtk.GtkEntry()
					if self.eventTree.has_key('requires_item_comparison_weight_entry:%i:selection' % key_index):
						requires_item_comparison_weight_entry.set_text( self.eventTree['requires_item_comparison_weight_entry:%i:selection' % key_index] )

					else:
						each = string.atoi( string.split( requirement_item_reference_combo.entry.get_text(), ' - ')[0] )
						if (self.itemData[each].weight != -1):
							requires_item_comparison_weight_entry.set_text( "%i" % self.itemData[each].weight )
							self.eventTree['requires_item_comparison_weight_entry:%s:selection' % key_index] = "%i" % self.itemData[each].weight
						else:
							requires_item_comparison_weight_entry.set_text( '0' )
							self.eventTree['requires_item_comparison_weight_entry:%s:selection' % key_index] = '0'

					requires_item_comparison_weight_vbox = self.create_event_widget_container(\
									'requires_item_comparison_weight', key_index, \
									'<Number>', requires_item_comparison_weight_entry, 'entry')


					requirement_toolbar.append_widget(requires_item_weight_comparison_vbox, "", "")
					requirement_toolbar.append_widget(requires_item_comparison_weight_vbox, "", "")


				elif ( self.eventTree['requires_item_property_optionmenu:%i:selection' % key_index] == 'Bulk' ):

					# Setup requires_item_bulk_comparison_vbox
					requires_item_bulk_comparison_menu = self.setup_event_builder_comparison_menu('requires_item_bulk_comparison_optionmenu:%s' % key_index)
					requires_item_bulk_comparison_optionmenu = gtk.GtkOptionMenu()
					requires_item_bulk_comparison_optionmenu.set_menu( requires_item_bulk_comparison_menu )
					requires_item_bulk_comparison_vbox = self.create_event_widget_container(\
									'requires_item_bulk_comparison', key_index, \
									'<Comparison>', requires_item_bulk_comparison_optionmenu, 'optionmenu')


					# Setup requires_item_comparison_bulk_vbox
					requires_item_comparison_bulk_entry = gtk.GtkEntry()
					if self.eventTree.has_key('requires_item_comparison_bulk_entry:%i:selection' % key_index):
						requires_item_comparison_bulk_entry.set_text( self.eventTree['requires_item_comparison_bulk_entry:%i:selection' % key_index] )

					else:
						each = string.atoi( string.split( requirement_item_reference_combo.entry.get_text(), ' - ')[0] )
						if (self.itemData[each].bulk != -1):
							requires_item_comparison_bulk_entry.set_text( "%i" % self.itemData[each].bulk )
							self.eventTree['requires_item_comparison_bulk_entry:%s:selection' % key_index] = "%i" % self.itemData[each].bulk
						else:
							requires_item_comparison_bulk_entry.set_text( '0' )
							self.eventTree['requires_item_comparison_bulk_entry:%s:selection' % key_index] = '0'

					requires_item_comparison_bulk_vbox = self.create_event_widget_container(\
									'requires_item_comparison_bulk', key_index, \
									'<Number>', requires_item_comparison_bulk_entry, 'entry')


					requirement_toolbar.append_widget(requires_item_bulk_comparison_vbox, "", "")
					requirement_toolbar.append_widget(requires_item_comparison_bulk_vbox, "", "")


			elif ( self.eventTree['requirement_type_optionmenu:%i:selection' % key_index] == 'Obstruction' ):

				# Setup requirement_obstruction_reference_combo
				requirement_obstruction_reference_combo = self.setup_event_builder_reference_combo(None, 'requirement_obstruction_reference_combo:%s' % key_index, 'Obstruction')
				requirement_obstruction_reference_vbox = self.create_event_widget_container(\
								'requirement_obstruction_reference', key_index, \
								'<obstruction Reference>', requirement_obstruction_reference_combo, 'combo')

				# Setup requires_obstruction_property_optionmenu
				requires_obstruction_property_menu = self.setup_event_builder_requires_obstruction_property_menu('requires_obstruction_property_optionmenu:%s' % key_index)
				requires_obstruction_property_optionmenu = gtk.GtkOptionMenu()
				requires_obstruction_property_optionmenu.set_menu( requires_obstruction_property_menu )
				requires_obstruction_property_vbox = self.create_event_widget_container(\
								'requires_obstruction_property', key_index, \
								'<Obstruction Property>', requires_obstruction_property_optionmenu, 'optionmenu')


				requirement_toolbar.append_widget(requirement_obstruction_reference_vbox, "", "")
				requirement_toolbar.append_widget(requires_obstruction_property_vbox, "", "")


				if ( self.eventTree['requires_obstruction_property_optionmenu:%i:selection' % key_index] == 'ExistsInRoom' ):
					# Setup requires_obstruction_exists_in_room_reference_combo
					requirement_obstruction_exists_in_room_reference_combo = self.setup_event_builder_room_reference_combo('requirement_obstruction_exists_in_room_reference_combo:%s' % key_index)
					requirement_obstruction_exists_in_room_reference_vbox = self.create_event_widget_container(\
									'requirement_obstruction_exists_in_room_reference', key_index, \
									'<Room Reference>', requirement_obstruction_exists_in_room_reference_combo, 'combo')

					requirement_toolbar.append_widget(requirement_obstruction_exists_in_room_reference_vbox, "", "")


				elif ( self.eventTree['requires_obstruction_property_optionmenu:%i:selection' % key_index] == 'ExistsInRoomDirection' ):
					# Setup requires_obstruction_exists_in_room_reference_combo
					requirement_obstruction_exists_in_room_reference_combo = self.setup_event_builder_room_reference_combo('requirement_obstruction_exists_in_room_reference_combo:%s' % key_index)
					requirement_obstruction_exists_in_room_reference_vbox = self.create_event_widget_container(\
									'requirement_obstruction_exists_in_room_reference', key_index, \
									'<Room Reference>', requirement_obstruction_exists_in_room_reference_combo, 'combo')

					# Setup requires_obstruction_exists_in_room_direction_reference_combo
					requirement_obstruction_exists_in_room_direction_reference_combo = self.setup_event_builder_direction_reference_combo('requirement_obstruction_exists_in_room_direction_reference_combo:%s' % key_index)
					requirement_obstruction_exists_in_room_direction_reference_vbox = self.create_event_widget_container(\
									'requirement_obstruction_exists_in_room_direction_reference', key_index, \
									'<Direction Reference>', requirement_obstruction_exists_in_room_direction_reference_combo, 'combo')


					requirement_toolbar.append_widget(requirement_obstruction_exists_in_room_reference_vbox, "", "")
					requirement_toolbar.append_widget(requirement_obstruction_exists_in_room_direction_reference_vbox, "", "")


			self.eventTree['requirement_toolbar:%i' % key_index ] = requirement_toolbar
			requirement_toolbar.show()


#####################################################################

def rebuild_yeilds_and_button_toolbars(self):

	import gtk

	# Setup yeilds label
	self.eventTree['yeilds_label:0'].destroy()
	yeilds_label = gtk.GtkLabel('->')
	self.eventTree['yeilds_label:0'] = yeilds_label
	yeilds_label.show()

	# Setup has_been_executed checkbutton
# 	has_been_executed_checkbutton = gtk.GtkCheckButton('Event has been executed')
# 	has_been_executed_checkbutton.set_active( self.eventTree['has_been_executed_checkbutton:0'].get_active() )
# 	self.eventTree['has_been_executed_checkbutton:0'].destroy()
# 	self.eventTree['has_been_executed_checkbutton:0'] = has_been_executed_checkbutton
# 	has_been_executed_checkbutton.show()

	# Setup add_event button
	self.eventTree['append_event_button:0'].destroy()
	append_event_button = gtk.GtkButton('Append Event')
	append_event_button.connect("clicked", self.on_append_event_button_clicked)
	self.eventTree['append_event_button:0'] = append_event_button
	append_event_button.show()

	# Setup button toolbar
	self.eventTree['button_toolbar:0'].destroy()
	button_toolbar = gtk.GtkToolbar(gtk.ORIENTATION_HORIZONTAL, gtk.TOOLBAR_BOTH)
#	button_toolbar.append_widget(has_been_executed_checkbutton, "", "")
	button_toolbar.append_widget(append_event_button, "", "")
	self.eventTree['button_toolbar:0'] = button_toolbar
	button_toolbar.show()


#####################################################################

def rebuild_effect_toolbars(self):

	import gtk, string

	eventTree_widgets = self.eventTree.keys()
	eventTree_widgets.sort()

	for each in eventTree_widgets:
		if ( string.find(each, 'effect_toolbar') != -1):

			key_index = string.split(each, ':')[1]

			self.eventTree[each].destroy()

			# Setup effect toolbar
			effect_toolbar = gtk.GtkToolbar(gtk.ORIENTATION_HORIZONTAL, gtk.TOOLBAR_BOTH)

			# Setup "and" label if necessary
			if ( string.atoi(key_index) > 0):
				and_label = gtk.GtkLabel(" and ")
				and_label.show()
				effect_toolbar.append_widget(and_label, "", "")


			# Setup effect vbox
			effect_menu = self.setup_event_builder_effect_menu('effect_optionmenu:%s' % key_index)
			effect_optionmenu = gtk.GtkOptionMenu()
			effect_optionmenu.set_menu(effect_menu)
			effect_vbox = self.create_event_widget_container(\
			                          'effect', key_index, \
			                          '<Effect>', effect_optionmenu, 'optionmenu')

			effect_toolbar.append_widget(effect_vbox, "", "")

			# Now handle individual components
			if ( self.eventTree['effect_optionmenu:%s:selection' % key_index] == 'Adds' ):
				# we have to check that an "adds" optionmenu exists because the first time
				# a new event builder is created no widget exists yet

				# Setup adds_object_vbox
				effect_adds_object_menu = self.setup_event_builder_object_menu('effect_adds_object_optionmenu:%s' % key_index)
				effect_adds_object_optionmenu = gtk.GtkOptionMenu()
				effect_adds_object_optionmenu.set_menu(effect_adds_object_menu)
				effect_adds_object_vbox = self.create_event_widget_container(\
				                          'effect_adds_object', key_index, \
				                          '<Object>', effect_adds_object_optionmenu, 'optionmenu')


				# Setup adds_reference_vbox
				effect_adds_reference_combo = self.setup_event_builder_reference_combo(None, 'effect_adds_reference_combo:%s' % key_index, self.eventTree['effect_adds_object_optionmenu:%s:selection' % key_index])
				effect_adds_reference_vbox = self.create_event_widget_container(\
				                             'effect_adds_reference', key_index, \
				                             '<Reference>', effect_adds_reference_combo, 'combo')


				# Setup adds_preposition_vbox
				effect_adds_preposition_combo = self.setup_event_builder_preposition_combo('effect_adds_preposition_combo:%s' % key_index)
				effect_adds_preposition_vbox = self.create_event_widget_container(\
				                          'effect_adds_preposition', key_index, \
				                          '<Preposition>', effect_adds_preposition_combo, 'combo')


				effect_toolbar.append_widget(effect_adds_object_vbox, "", "")
				effect_toolbar.append_widget(effect_adds_reference_vbox, "", "")
				effect_toolbar.append_widget(effect_adds_preposition_vbox, "", "")


				if ( self.eventTree['effect_adds_object_optionmenu:%s:selection' % key_index] == 'Item'):
					# Setup effect_adds_itemlocation_vbox
					effect_adds_itemlocation_menu = self.setup_event_builder_itemlocation_menu('effect_adds_itemlocation_optionmenu:%s' % key_index)
					effect_adds_itemlocation_optionmenu = gtk.GtkOptionMenu()
					effect_adds_itemlocation_optionmenu.set_menu(effect_adds_itemlocation_menu)
					effect_adds_itemlocation_vbox = self.create_event_widget_container(\
					              'effect_adds_itemlocation', key_index, \
					              '<Location>', effect_adds_itemlocation_optionmenu, 'optionmenu')


					effect_toolbar.append_widget(effect_adds_itemlocation_vbox, "", "")


					if (self.eventTree['effect_adds_itemlocation_optionmenu:%s:selection' % key_index] == 'Room' ):
						# If a room was selected as the location for an item, a room_reference_combo
						# vbox and a direction_reference_combo vbox needs to be handled
						effect_adds_itemlocation_room_reference_combo = self.setup_event_builder_room_reference_combo('effect_adds_itemlocation_room_reference_combo:%s' % key_index)
						effect_adds_itemlocation_room_reference_vbox = self.create_event_widget_container(\
										'effect_adds_itemlocation_room_reference', key_index, \
										'<Room Reference>', effect_adds_itemlocation_room_reference_combo, 'combo')


						effect_toolbar.append_widget(effect_adds_itemlocation_room_reference_vbox, "", "")


				elif ( self.eventTree['effect_adds_object_optionmenu:%s:selection' % key_index] == 'Obstruction'):
					# Setup effect_adds_obstruction_room_reference_vbox
					effect_adds_obstruction_room_reference_combo = self.setup_event_builder_room_reference_combo('effect_adds_obstruction_room_reference_combo:%s' % key_index)
					effect_adds_obstruction_room_reference_vbox = self.create_event_widget_container(\
									'effect_adds_obstruction_room_reference', key_index, \
									'<Room Reference>', effect_adds_obstruction_room_reference_combo, 'combo')


					# Setup effect_adds_direction_vbox
					effect_adds_direction_reference_menu = self.setup_event_builder_direction_reference_optionmenu('effect_adds_direction_reference_optionmenu:%s' % key_index)
					effect_adds_direction_reference_optionmenu = gtk.GtkOptionMenu()
					effect_adds_direction_reference_optionmenu.set_menu( effect_adds_direction_reference_menu )
					effect_adds_direction_reference_vbox = self.create_event_widget_container(\
									'effect_adds_direction_reference', key_index, \
									'<Direction>', effect_adds_direction_reference_optionmenu, 'optionmenu')


					effect_toolbar.append_widget(effect_adds_obstruction_room_reference_vbox, "", "")
					effect_toolbar.append_widget(effect_adds_direction_reference_vbox, "", "")


			elif ( self.eventTree['effect_optionmenu:%s:selection' % key_index] == 'Removes' ):
				# we have to check that an "removes" optionmenu exists because the first time
				# a new event builder is created no widget exists yet

				# Setup removes_object_vbox
				effect_removes_object_menu = self.setup_event_builder_object_menu('effect_removes_object_optionmenu:%s' % key_index)
				effect_removes_object_optionmenu = gtk.GtkOptionMenu()
				effect_removes_object_optionmenu.set_menu(effect_removes_object_menu)
				effect_removes_object_vbox = self.create_event_widget_container(\
								'effect_removes_object', key_index, \
								'<Object>', effect_removes_object_optionmenu, 'optionmenu')


				# Setup removes_reference_vbox
				effect_removes_reference_combo = self.setup_event_builder_reference_combo(None, 'effect_removes_reference_combo:%s' % key_index, self.eventTree['effect_removes_object_optionmenu:%s:selection' % key_index])
				effect_removes_reference_vbox = self.create_event_widget_container(\
								'effect_removes_reference', key_index, \
								'<Reference>', effect_removes_reference_combo, 'combo')


				# Setup removes_preposition_vbox
				effect_removes_preposition_combo = self.setup_event_builder_preposition_combo('effect_removes_preposition_combo:%s' % key_index)
				effect_removes_preposition_vbox = self.create_event_widget_container(\
								'effect_removes_preposition', key_index, \
								'<Preposition>', effect_removes_preposition_combo, 'combo')


				effect_toolbar.append_widget(effect_removes_object_vbox, "", "")
				effect_toolbar.append_widget(effect_removes_reference_vbox, "", "")
				effect_toolbar.append_widget(effect_removes_preposition_vbox, "", "")


				if ( self.eventTree['effect_removes_object_optionmenu:%s:selection' % key_index] == 'Item'):
					# Setup effect_removes_itemlocation_vbox
					effect_removes_itemlocation_menu = self.setup_event_builder_itemlocation_menu('effect_removes_itemlocation_optionmenu:%s' % key_index)
					effect_removes_itemlocation_optionmenu = gtk.GtkOptionMenu()
					effect_removes_itemlocation_optionmenu.set_menu(effect_removes_itemlocation_menu)
					effect_removes_itemlocation_vbox = self.create_event_widget_container(\
									'effect_removes_itemlocation', key_index, \
									'<Location>', effect_removes_itemlocation_optionmenu, 'optionmenu')


					effect_toolbar.append_widget(effect_removes_itemlocation_vbox, "", "")


					if (self.eventTree['effect_removes_itemlocation_optionmenu:%s:selection' % key_index] == 'Room' ):
						# If a room was selected as the location for an item, a room_reference_combo
						# vbox and a direction_reference_combo vbox needs to be handled
						effect_removes_itemlocation_room_reference_combo = self.setup_event_builder_room_reference_combo('effect_removes_itemlocation_room_reference_combo:%s' % key_index)
						effect_removes_itemlocation_room_reference_vbox = self.create_event_widget_container(\
										'effect_removes_itemlocation_room_reference', key_index, \
										'<Room Reference>', effect_removes_itemlocation_room_reference_combo, 'combo')


						effect_toolbar.append_widget(effect_removes_itemlocation_room_reference_vbox, "", "")


				elif ( self.eventTree['effect_removes_object_optionmenu:%s:selection' % key_index] == 'Obstruction'):
					# Setup effect_removes_obstruction_room_reference_vbox
					effect_removes_obstruction_room_reference_combo = self.setup_event_builder_room_reference_combo('effect_removes_obstruction_room_reference_combo:%s' % key_index)
					effect_removes_obstruction_room_reference_vbox = self.create_event_widget_container(\
									'effect_removes_obstruction_room_reference', key_index, \
									'<Room Reference>', effect_removes_obstruction_room_reference_combo, 'combo')


					# Setup effect_removes_direction_vbox
					effect_removes_direction_reference_menu = self.setup_event_builder_direction_reference_optionmenu('effect_removes_direction_reference_optionmenu:%s' % key_index)
					effect_removes_direction_reference_optionmenu = gtk.GtkOptionMenu()
					effect_removes_direction_reference_optionmenu.set_menu( effect_removes_direction_reference_menu )
					effect_removes_direction_reference_vbox = self.create_event_widget_container(\
									'effect_removes_direction_reference', key_index, \
									'<Room Reference>', effect_removes_direction_reference_optionmenu, 'optionmenu')


					effect_toolbar.append_widget(effect_removes_obstruction_room_reference_vbox, "", "")
					effect_toolbar.append_widget(effect_removes_direction_reference_vbox, "", "")


			# Modifies
			elif ( self.eventTree['effect_optionmenu:%s:selection' % key_index] == 'Modifies' ):

				# Setup effect_modifies_vbox
				effect_modifies_menu = self.setup_event_builder_modifies_menu('effect_modifies_optionmenu:%s' % key_index)
				effect_modifies_optionmenu = gtk.GtkOptionMenu()
				effect_modifies_optionmenu.set_menu( effect_modifies_menu )
				effect_modifies_vbox = self.create_event_widget_container(\
								'effect_modifies', key_index, \
								'<Modification>', effect_modifies_optionmenu, 'optionmenu')


				effect_toolbar.append_widget(effect_modifies_vbox, "", "")


				if ( self.eventTree['effect_modifies_optionmenu:%s:selection' % key_index] == 'Player' ):
					# Setup effect_modifies_player_vbox
					effect_modifies_player_menu = self.setup_event_builder_modifies_player_menu('effect_modifies_player_optionmenu:%s' % key_index)
					effect_modifies_player_optionmenu = gtk.GtkOptionMenu()
					effect_modifies_player_optionmenu.set_menu( effect_modifies_player_menu )
					effect_modifies_player_vbox = self.create_event_widget_container(\
									'effect_modifies_player', key_index, \
									'<Player Attributes>', effect_modifies_player_optionmenu, 'optionmenu')


					# Setup effect_modifies_expression_vbox
					effect_modifies_expression_menu = self.setup_event_builder_expression_menu('effect_modifies_expression_optionmenu:%s' % key_index)
					effect_modifies_expression_optionmenu = gtk.GtkOptionMenu()
					effect_modifies_expression_optionmenu.set_menu( effect_modifies_expression_menu )
					effect_modifies_expression_vbox = self.create_event_widget_container(\
									'effect_modifies_expression', key_index, \
									'<Expression>', effect_modifies_expression_optionmenu, 'optionmenu')


					# Setup effect_modifies_number_vbox
					effect_modifies_number_entry = gtk.GtkEntry()
					effect_modifies_number_entry.set_text('0')
					self.eventTree['effect_modifies_number_entry:%s:selection' % key_index] = '0'
					effect_modifies_number_vbox = self.create_event_widget_container(\
									'effect_modifies_number', key_index, \
									'<Number>', effect_modifies_number_entry, 'entry')


					effect_toolbar.append_widget(effect_modifies_player_vbox, "", "")
					effect_toolbar.append_widget(effect_modifies_expression_vbox, "", "")
					effect_toolbar.append_widget(effect_modifies_number_vbox, "", "")


				elif ( self.eventTree['effect_modifies_optionmenu:%s:selection' % key_index] == 'Room' ):
					# Setup effect_modifies_room_reference_vbox
					effect_modifies_room_reference_combo = self.setup_event_builder_room_reference_combo('effect_modifies_room_reference_combo:%s' % key_index)
					effect_modifies_room_reference_vbox = self.create_event_widget_container(\
									'effect_modifies_room_reference', key_index, \
									'<Room Reference>', effect_modifies_room_reference_combo, 'combo')


					# Setup effect_modifies_room_vbox
					effect_modifies_room_menu = self.setup_event_builder_modifies_room_menu('effect_modifies_room_optionmenu:%s' % key_index)
					effect_modifies_room_optionmenu = gtk.GtkOptionMenu()
					effect_modifies_room_optionmenu.set_menu( effect_modifies_room_menu )
					effect_modifies_room_vbox = self.create_event_widget_container(\
									'effect_modifies_room', key_index, \
									'<Modification>', effect_modifies_room_optionmenu, 'optionmenu')


					effect_toolbar.append_widget(effect_modifies_room_reference_vbox, "", "")
					effect_toolbar.append_widget(effect_modifies_room_vbox, "", "")


					if ( self.eventTree['effect_modifies_room_optionmenu:%s:selection' % key_index] == 'TextDescription(Long)' ):
						# Setup effect_modifies_room_textdescription_long_vbox
						effect_modifies_textdescription_long_entry = gtk.GtkEntry()
						each = string.atoi( string.split( effect_modifies_room_reference_combo.entry.get_text(), ' - ')[0] )
						if (self.roomData[each].description_long != None):
							effect_modifies_textdescription_long_entry.set_text(self.roomData[each].description_long)
							self.eventTree['effect_modifies_textdescription_long_entry:%s:selection' % key_index] = self.roomData[each].description_long
							effect_modifies_textdescription_long_entry.set_position(0)

						effect_modifies_textdescription_long_vbox = self.create_event_widget_container(\
										'effect_modifies_textdescription_long', key_index, \
										'<TextDescription(Long)>', effect_modifies_textdescription_long_entry, 'entry')


						effect_toolbar.append_widget(effect_modifies_textdescription_long_vbox, "", "")


					elif ( self.eventTree['effect_modifies_room_optionmenu:%s:selection' % key_index] == 'TextDescription(Short)' ):
						# Setup effect_modifies_room_textdescription_short_vbox
						effect_modifies_textdescription_short_entry = gtk.GtkEntry()
						each = string.atoi( string.split( effect_modifies_room_reference_combo.entry.get_text(), ' - ')[0] )
						if (self.roomData[each].description_short != None):
							effect_modifies_textdescription_short_entry.set_text(self.roomData[each].description_short)
							self.eventTree['effect_modifies_textdescription_short_entry:%s:selection' % key_index] = self.roomData[each].description_short
							effect_modifies_textdescription_short_entry.set_position(0)

						effect_modifies_textdescription_short_vbox = self.create_event_widget_container(\
										'effect_modifies_textdescription_short', key_index, \
										'<TextDescription(Short)>', effect_modifies_textdescription_short_entry, 'entry')


						effect_toolbar.append_widget(effect_modifies_textdescription_short_vbox, "", "")


					elif ( self.eventTree['effect_modifies_room_optionmenu:%s:selection' % key_index] == 'DirectionDescription' ):
						# Setup effect_modifies_room_direction_description_vbox
						effect_modifies_direction_description_entry = gtk.GtkEntry()
						each = string.atoi( string.split( effect_modifies_room_reference_combo.entry.get_text(), ' - ')[0] )
						if (self.roomData[each].direction_description != None):
							effect_modifies_direction_description_entry.set_text(self.roomData[each].direction_description)
							self.eventTree['effect_modifies_direction_description_entry:%s:selection' % key_index] = self.roomData[each].direction_description
							effect_modifies_direction_description_entry.set_position(0)

						effect_modifies_direction_description_vbox = self.create_event_widget_container(\
										'effect_modifies_direction_description', key_index, \
										'<DirectionDescription>', effect_modifies_direction_description_entry, 'entry')


						effect_toolbar.append_widget(effect_modifies_direction_description_vbox, "", "")


					elif ( self.eventTree['effect_modifies_room_optionmenu:%s:selection' % key_index] == 'GraphicURL' ):
						# Setup effect_modifies_room_graphic_url_vbox
						effect_modifies_graphic_url_entry = gtk.GtkEntry()
						each = string.atoi( string.split( effect_modifies_room_reference_combo.entry.get_text(), ' - ')[0] )
						if (self.roomData[each].graphic_url != None):
							effect_modifies_graphic_url_entry.set_text(self.roomData[each].graphic_url)
							self.eventTree['effect_modifies_graphic_url_entry:%s:selection' % key_index] = self.roomData[each].graphic_url
							effect_modifies_graphic_url_entry.set_position(0)

						effect_modifies_graphic_url_vbox = self.create_event_widget_container(\
										'effect_modifies_graphic_url', key_index, \
										'<GraphicURL>', effect_modifies_graphic_url_entry, 'entry')


						effect_toolbar.append_widget(effect_modifies_graphic_url_vbox, "", "")


					elif ( self.eventTree['effect_modifies_room_optionmenu:%s:selection' % key_index] == 'Visited' ):
						# Setup effect_modifies_room_visited_vbox

						each = string.atoi( string.split( effect_modifies_room_reference_combo.entry.get_text(), ' - ')[0] )
						truth_boolean = self.roomData[each].visited

						effect_modifies_room_visited_radiobutton_vbox = self.setup_radiobutton_vbox(\
						            'effect_modifies_room_visited', key_index, \
										truth_boolean)

						effect_modifies_room_visited_vbox = self.create_event_widget_container(\
										'effect_modifies_room_visited', key_index, \
										'<Boolean>', effect_modifies_room_visited_radiobutton_vbox, 'vbox')


						effect_toolbar.append_widget(effect_modifies_room_visited_vbox, "", "")


					elif ( self.eventTree['effect_modifies_room_optionmenu:%s:selection' % key_index] == 'DirectionObject' ):
						# Setup effect_modifies_room_direction_vbox
						effect_modifies_room_direction_reference_menu = self.setup_event_builder_direction_reference_optionmenu('effect_modifies_room_direction_reference_optionmenu:%s' % key_index)
						effect_modifies_room_direction_reference_optionmenu = gtk.GtkOptionMenu()
						effect_modifies_room_direction_reference_optionmenu.set_menu( effect_modifies_room_direction_reference_menu )
						effect_modifies_room_direction_reference_vbox = self.create_event_widget_container(\
										'effect_modifies_room_direction_reference', key_index, \
										'<Direction>', effect_modifies_room_direction_reference_optionmenu, 'optionmenu')


						# Setup effect_modifies_room_direction_vbox
						effect_modifies_room_direction_menu = self.setup_event_builder_modifies_room_direction_menu('effect_modifies_room_direction_optionmenu:%s' % key_index)
						effect_modifies_room_direction_optionmenu = gtk.GtkOptionMenu()
						effect_modifies_room_direction_optionmenu.set_menu( effect_modifies_room_direction_menu )
						effect_modifies_room_direction_vbox = self.create_event_widget_container(\
										'effect_modifies_room_direction', key_index, \
										'<DirectionAttribute>', effect_modifies_room_direction_optionmenu, 'optionmenu')


						effect_toolbar.append_widget(effect_modifies_room_direction_reference_vbox, "", "")
						effect_toolbar.append_widget(effect_modifies_room_direction_vbox, "", "")


						if ( self.eventTree['effect_modifies_room_direction_optionmenu:%s:selection' % key_index] == 'ToWhichRoom' ):
							# Setup effect_modifies_room_direction_to_which_room_reference_vbox
							effect_modifies_room_direction_to_which_room_reference_combo = self.setup_event_builder_nowhere_room_reference_combo('effect_modifies_room_direction_to_which_room_reference_combo:%s' % key_index)
							each = string.atoi( string.split( effect_modifies_room_reference_combo.entry.get_text(), ' - ')[0] )
							direction_name = self.eventTree['effect_modifies_room_direction_reference_optionmenu:%s:selection' % key_index]
							for direction in self.roomData[each].direction.keys():
								if ( direction_name == self.directionData[ direction ].name ):
									effect_modifies_room_direction_to_which_room_reference_combo.entry.set_text("%i - %s" % (each, self.roomData[self.roomData[each].direction[ direction ].to_which_room].name) )
									self.eventTree['effect_modifies_room_direction_to_which_room_entry:%s:selection' % key_index] = "%i - %s" % (each, self.roomData[self.roomData[each].direction[ direction ].to_which_room].name)

							effect_modifies_room_direction_to_which_room_reference_vbox = self.create_event_widget_container(\
											'effect_modifies_room_direction_to_which_room_reference', key_index, \
											'<Room Reference>', effect_modifies_room_direction_to_which_room_reference_combo, 'combo')

							effect_toolbar.append_widget(effect_modifies_room_direction_to_which_room_reference_vbox, "", "")


						elif ( self.eventTree['effect_modifies_room_direction_optionmenu:%s:selection' % key_index] == 'FirstTransitionText' ):
							# Setup effect_modifies_room_direction_firsttransitiontext_vbox
							effect_modifies_room_direction_firsttransitiontext_entry = gtk.GtkEntry()
							each = string.atoi( string.split( effect_modifies_room_reference_combo.entry.get_text(), ' - ')[0] )
							direction_name = self.eventTree['effect_modifies_room_direction_reference_optionmenu:%s:selection' % key_index]
							for direction in self.roomData[each].direction.keys():
								if ( ( direction_name == self.directionData[ direction ].name ) \
									and (self.roomData[each].direction[ direction ].first_transition_text != None) ):
									effect_modifies_room_direction_firsttransitiontext_entry.set_text(self.roomData[each].direction[ direction ].first_transition_text)
									self.eventTree['effect_modifies_room_direction_firsttransitiontext_entry:%s:selection' % key_index] = self.roomData[each].direction[ direction ].first_transition_text

							effect_modifies_room_direction_firsttransitiontext_vbox = self.create_event_widget_container(\
											'effect_modifies_room_direction_firsttransitiontext', key_index, \
											'<Text>', effect_modifies_room_direction_firsttransitiontext_entry, 'entry')


							effect_toolbar.append_widget(effect_modifies_room_direction_firsttransitiontext_vbox, "", "")


						elif ( self.eventTree['effect_modifies_room_direction_optionmenu:%s:selection' % key_index] == 'TransitionText' ):
							# Setup effect_modifies_room_direction_transitiontext_vbox
							effect_modifies_room_direction_transitiontext_entry = gtk.GtkEntry()
							each = string.atoi( string.split( effect_modifies_room_reference_combo.entry.get_text(), ' - ')[0] )
							direction_name = self.eventTree['effect_modifies_room_direction_reference_optionmenu:%s:selection' % key_index]
							for direction in self.roomData[each].direction.keys():
								if ( ( direction_name == self.directionData[ direction ].name ) \
									and (self.roomData[each].direction[ direction ].transition_text != None) ):
									effect_modifies_room_direction_transitiontext_entry.set_text(self.roomData[each].direction[ direction ].transition_text)
									self.eventTree['effect_modifies_room_direction_transitiontext_entry:%s:selection' % key_index] = self.roomData[each].direction[ direction ].transition_text
									effect_modifies_room_direction_transitiontext_entry.set_position(0)

							effect_modifies_room_direction_transitiontext_vbox = self.create_event_widget_container(\
											'effect_modifies_room_direction_transitiontext', key_index, \
											'<Text>', effect_modifies_room_direction_transitiontext_entry, 'entry')


							effect_toolbar.append_widget(effect_modifies_room_direction_transitiontext_vbox, "", "")


						elif ( self.eventTree['effect_modifies_room_direction_optionmenu:%s:selection' % key_index] == 'FirstTransitionGraphic' ):
							# Setup effect_modifies_room_direction_firsttransitiongraphic_vbox
							effect_modifies_room_direction_firsttransitiongraphic_entry = gtk.GtkEntry()
							each = string.atoi( string.split( effect_modifies_room_reference_combo.entry.get_text(), ' - ')[0] )
							direction_name = self.eventTree['effect_modifies_room_direction_reference_optionmenu:%s:selection' % key_index]
							for direction in self.roomData[each].direction.keys():
								if ( ( direction_name == self.directionData[ direction ].name ) \
									and (self.roomData[each].direction[ direction ].first_transition_graphic != None) ):
									effect_modifies_room_direction_firsttransitiongraphic_entry.set_text(self.roomData[each].direction[ direction ].first_transition_graphic)
									self.eventTree['effect_modifies_room_direction_firsttransitiongraphic_entry:%s:selection' % key_index] = self.roomData[each].direction[ direction ].first_transition_graphic
									effect_modifies_room_direction_firsttransitiongraphic_entry.set_position(0)

							effect_modifies_room_direction_firsttransitiongraphic_vbox = self.create_event_widget_container(\
											'effect_modifies_room_direction_firsttransitiongraphic', key_index, \
											'<URL>', effect_modifies_room_direction_firsttransitiongraphic_entry, 'entry')


							effect_toolbar.append_widget(effect_modifies_room_direction_firsttransitiongraphic_vbox, "", "")


						elif ( self.eventTree['effect_modifies_room_direction_optionmenu:%s:selection' % key_index] == 'TransitionGraphic' ):
							# Setup effect_modifies_room_direction_transitiongraphic_vbox
							effect_modifies_room_direction_transitiongraphic_entry = gtk.GtkEntry()
							each = string.atoi( string.split( effect_modifies_room_reference_combo.entry.get_text(), ' - ')[0] )
							direction_name = self.eventTree['effect_modifies_room_direction_reference_optionmenu:%s:selection' % key_index]
							for direction in self.roomData[each].direction.keys():
								if ( ( direction_name == self.directionData[ direction ].name ) \
									and (self.roomData[each].direction[ direction ].transition_graphic != None) ):
									effect_modifies_room_direction_transitiongraphic_entry.set_text(self.roomData[each].direction[ direction ].transition_graphic)
									self.eventTree['effect_modifies_room_direction_transitiongraphic_entry:%s:selection' % key_index] = self.roomData[each].direction[ direction ].transition_graphic
									effect_modifies_room_direction_transitiongraphic_entry.set_position(0)

							effect_modifies_room_direction_transitiongraphic_vbox = self.create_event_widget_container(\
											'effect_modifies_room_direction_transitiongraphic', key_index, \
											'<URL>', effect_modifies_room_direction_transitiongraphic_entry, 'entry')


							effect_toolbar.append_widget(effect_modifies_room_direction_transitiongraphic_vbox, "", "")


						elif ( self.eventTree['effect_modifies_room_direction_optionmenu:%s:selection' % key_index] == 'HasMovedThisWay' ):
							# Setup effect_modifies_room_direction_hasmovedthisway_vbox

							each = string.atoi( string.split( effect_modifies_room_reference_combo.entry.get_text(), ' - ')[0] )
							direction_name = self.eventTree['effect_modifies_room_direction_reference_optionmenu:%s:selection' % key_index]
							for direction in self.roomData[each].direction.keys():
								if ( direction_name == self.directionData[ direction ].name ):
									truth_boolean = self.roomData[each].direction[ direction].has_moved_this_way

							effect_modifies_room_direction_hasmovedthisway_radiobutton_vbox = self.setup_radiobutton_vbox(\
											'effect_modifies_room_direction_hasmovedthisway', key_index, \
											truth_boolean)

							effect_modifies_room_direction_hasmovedthisway_vbox = self.create_event_widget_container(\
											'effect_modifies_room_direction_hasmovedthisway', key_index, \
											'<Boolean>', effect_modifies_room_direction_hasmovedthisway_radiobutton_vbox, 'vbox')


							effect_toolbar.append_widget(effect_modifies_room_direction_hasmovedthisway_vbox, "", "")


				elif ( self.eventTree['effect_modifies_optionmenu:%s:selection' % key_index] == 'Item' ):
					# Setup effect_modifies_item_reference vbox
					effect_modifies_item_reference_combo = self.setup_event_builder_reference_combo(None, 'effect_modifies_item_reference_combo:0', 'Item')

					effect_modifies_item_reference_vbox = self.create_event_widget_container(\
									'effect_modifies_item_reference', key_index, \
									'<Reference>', effect_modifies_item_reference_combo, 'combo')


					# Setup effect_modifies_item_vbox
					effect_modifies_item_menu = self.setup_event_builder_modifies_item_menu('effect_modifies_item_optionmenu:%s' % key_index)
					effect_modifies_item_optionmenu = gtk.GtkOptionMenu()
					effect_modifies_item_optionmenu.set_menu( effect_modifies_item_menu )

					effect_modifies_item_vbox = self.create_event_widget_container(\
									'effect_modifies_item', key_index, \
									'<ItemAttribute>', effect_modifies_item_optionmenu, 'optionmenu')


					effect_toolbar.append_widget(effect_modifies_item_reference_vbox, "", "")
					effect_toolbar.append_widget(effect_modifies_item_vbox, "", "")


					if ( self.eventTree['effect_modifies_item_optionmenu:%s:selection' % key_index] == 'Equipped' ):
						# Setup effect_modifies_item_equipped_vbox

						each = string.atoi( string.split( effect_modifies_item_reference_combo.entry.get_text(), ' - ')[0] )
						truth_boolean = self.itemData[each].equipped

						effect_modifies_item_equipped_radiobutton_vbox = self.setup_radiobutton_vbox(\
										'effect_modifies_item_equipped', key_index, \
										truth_boolean)

						effect_modifies_item_equipped_vbox = self.create_event_widget_container(\
										'effect_modifies_item_equipped', key_index, \
										'<Boolean>', effect_modifies_item_equipped_radiobutton_vbox, 'vbox')


						effect_toolbar.append_widget(effect_modifies_item_equipped_vbox, "", "")


					elif ( self.eventTree['effect_modifies_item_optionmenu:%s:selection' % key_index] == 'Weight' ):
						# Setup effect_modifies_item_weight_vbox
						effect_modifies_item_weight_entry = gtk.GtkEntry()
						each = string.atoi( string.split( effect_modifies_item_reference_combo.entry.get_text(), ' - ')[0] )
						effect_modifies_item_weight_entry.set_text("%i" % self.itemData[each].weight)
						self.eventTree['effect_modifies_item_weight_entry:%s:selection' % key_index] = self.itemData[each].weight

						effect_modifies_item_weight_vbox = self.create_event_widget_container(\
										'effect_modifies_item_weight', key_index, \
										'<Number>', effect_modifies_item_weight_entry, 'entry')


						effect_toolbar.append_widget(effect_modifies_item_weight_vbox, "", "")


					elif ( self.eventTree['effect_modifies_item_optionmenu:%s:selection' % key_index] == 'Bulk' ):
						# Setup effect_modifies_item_bulk_vbox
						effect_modifies_item_bulk_entry = gtk.GtkEntry()
						each = string.atoi( string.split( effect_modifies_item_reference_combo.entry.get_text(), ' - ')[0] )
						effect_modifies_item_bulk_entry.set_text("%i" % self.itemData[each].bulk)
						self.eventTree['effect_modifies_item_bulk_entry:%s:selection' % key_index] = self.itemData[each].bulk

						effect_modifies_item_bulk_vbox = self.create_event_widget_container(\
										'effect_modifies_item_bulk', key_index, \
										'<Number>', effect_modifies_item_bulk_entry, 'entry')


						effect_toolbar.append_widget(effect_modifies_item_bulk_vbox, "", "")


					elif ( self.eventTree['effect_modifies_item_optionmenu:%s:selection' % key_index] == 'TextDescription' ):
						# Setup effect_modifies_item_textdescription_vbox
						effect_modifies_item_textdescription_entry = gtk.GtkEntry()
						each = string.atoi( string.split( effect_modifies_item_reference_combo.entry.get_text(), ' - ')[0] )
						if (self.itemData[each].description != None):
							effect_modifies_item_textdescription_entry.set_text(self.itemData[each].description)
							self.eventTree['effect_modifies_item_textdescription_entry:%s:selection' % key_index] = self.itemData[each].description
							effect_modifies_item_textdescription_entry.set_position(0)

						effect_modifies_item_textdescription_vbox = self.create_event_widget_container(\
										'effect_modifies_item_textdescription', key_index, \
										'<Text>', effect_modifies_item_textdescription_entry, 'entry')


						effect_toolbar.append_widget(effect_modifies_item_textdescription_vbox, "", "")


					elif ( self.eventTree['effect_modifies_item_optionmenu:%s:selection' % key_index] == 'Environment_GraphicURL' ):
						# Setup effect_modifies_item_environment_graphic_url_vbox
						effect_modifies_item_environment_graphic_url_entry = gtk.GtkEntry()
						each = string.atoi( string.split( effect_modifies_item_reference_combo.entry.get_text(), ' - ')[0] )
						if (self.itemData[each].environment_graphic_url != None):
							effect_modifies_item_environment_graphic_url_entry.set_text(self.itemData[each].environment_graphic_url)
							self.eventTree['effect_modifies_item_environment_graphic_url_entry:%s:selection' % key_index] = self.itemData[each].environment_graphic_url
							effect_modifies_item_environment_graphic_url_entry.set_position(0)

						effect_modifies_item_environment_graphic_url_vbox = self.create_event_widget_container(\
										'effect_modifies_item_environment_graphic_url', key_index, \
										'<URL>', effect_modifies_item_environment_graphic_url_entry, 'entry')


						effect_toolbar.append_widget(effect_modifies_item_environment_graphic_url_vbox, "", "")


					elif ( self.eventTree['effect_modifies_item_optionmenu:%s:selection' % key_index] == 'Environment_Graphic_Pos' ):
						# Setup effect_modifies_item_xpos_vbox
						effect_modifies_item_xpos_entry = gtk.GtkEntry()
						each = string.atoi( string.split( effect_modifies_item_reference_combo.entry.get_text(), ' - ')[0] )
						effect_modifies_item_xpos_entry.set_text("%i" % self.itemData[each].environment_graphic_Xpos)
						self.eventTree['effect_modifies_item_xpos_entry:%s:selection' % key_index] = self.itemData[each].environment_graphic_Xpos

						effect_modifies_item_xpos_vbox = self.create_event_widget_container(\
										'effect_modifies_item_xpos', key_index, \
										'<X-Coordinate>', effect_modifies_item_xpos_entry, 'entry')


						# Setup effect_modifies_item_ypos_vbox
						effect_modifies_item_ypos_entry = gtk.GtkEntry()
						each = string.atoi( string.split( effect_modifies_item_reference_combo.entry.get_text(), ' - ')[0] )
						effect_modifies_item_ypos_entry.set_text("%i" % self.itemData[each].environment_graphic_Ypos)
						self.eventTree['effect_modifies_item_ypos_entry:%s:selection' % key_index] = self.itemData[each].environment_graphic_Ypos

						effect_modifies_item_ypos_vbox = self.create_event_widget_container(\
										'effect_modifies_item_ypos', key_index, \
										'<Y-Coordinate>', effect_modifies_item_ypos_entry, 'entry')


						effect_toolbar.append_widget(effect_modifies_item_xpos_vbox, "", "")
						effect_toolbar.append_widget(effect_modifies_item_ypos_vbox, "", "")


					elif ( self.eventTree['effect_modifies_item_optionmenu:%s:selection' % key_index] == 'CloseUp_GraphicURL' ):
						# Setup effect_modifies_item_closeup_graphic_url_vbox
						effect_modifies_item_closeup_graphic_url_entry = gtk.GtkEntry()
						each = string.atoi( string.split( effect_modifies_item_reference_combo.entry.get_text(), ' - ')[0] )
						if (self.itemData[each].closeup_graphic_url != None):
							effect_modifies_item_closeup_graphic_url_entry.set_text(self.itemData[each].closeup_graphic_url)
							self.eventTree['effect_modifies_item_closeup_graphic_url_entry:%s:selection' % key_index] = self.itemData[each].closeup_graphic_url
							effect_modifies_item_closeup_graphic_url_entry.set_position(0)

						effect_modifies_item_closeup_graphic_url_vbox = self.create_event_widget_container(\
										'effect_modifies_item_closeup_graphic_url', key_index, \
										'<URL>', effect_modifies_item_closeup_graphic_url_entry, 'entry')


						effect_toolbar.append_widget(effect_modifies_item_closeup_graphic_url_vbox, "", "")


					elif ( self.eventTree['effect_modifies_item_optionmenu:%s:selection' % key_index] == 'Icon_GraphicURL' ):
						# Setup effect_modifies_item_icon_graphic_url_vbox
						effect_modifies_item_icon_graphic_url_entry = gtk.GtkEntry()
						each = string.atoi( string.split( effect_modifies_item_reference_combo.entry.get_text(), ' - ')[0] )
						if (self.itemData[each].icon_graphic_url != None):
							effect_modifies_item_icon_graphic_url_entry.set_text(self.itemData[each].icon_graphic_url)
							self.eventTree['effect_modifies_item_icon_graphic_url_entry:%s:selection' % key_index] = self.itemData[each].icon_graphic_url
							effect_modifies_item_icon_graphic_url_entry.set_position(0)

						effect_modifies_item_icon_graphic_url_vbox = self.create_event_widget_container(\
										'effect_modifies_item_icon_graphic_url', key_index, \
										'<URL>', effect_modifies_item_icon_graphic_url_entry, 'entry')


						effect_toolbar.append_widget(effect_modifies_item_icon_graphic_url_vbox, "", "")


					elif ( self.eventTree['effect_modifies_item_optionmenu:%s:selection' % key_index] == 'Equipped_GraphicURL' ):
						# Setup effect_modifies_item_equipped_graphic_url_vbox
						effect_modifies_item_equipped_graphic_url_entry = gtk.GtkEntry()
						each = string.atoi( string.split( effect_modifies_item_reference_combo.entry.get_text(), ' - ')[0] )
						if (self.itemData[each].equipped_graphic_url != None):
							effect_modifies_item_equipped_graphic_url_entry.set_text(self.itemData[each].equipped_graphic_url)
							self.eventTree['effect_modifies_item_equipped_graphic_url_entry:%s:selection' % key_index] = self.itemData[each].equipped_graphic_url
							effect_modifies_item_equipped_graphic_url_entry.set_position(0)

						effect_modifies_item_equipped_graphic_url_vbox = self.create_event_widget_container(\
										'effect_modifies_item_equipped_graphic_url', key_index, \
										'<URL>', effect_modifies_item_equipped_graphic_url_entry, 'entry')


						effect_toolbar.append_widget(effect_modifies_item_equipped_graphic_url_vbox, "", "")


				elif ( self.eventTree['effect_modifies_optionmenu:%s:selection' % key_index] == 'Obstruction' ):
					# Setup effect_modifies_obstruction_reference vbox
					effect_modifies_obstruction_reference_combo = self.setup_event_builder_reference_combo(None, 'effect_modifies_obstruction_reference_combo:0', 'Obstruction')
					effect_modifies_obstruction_reference_vbox = self.create_event_widget_container(\
										'effect_modifies_obstruction_reference', key_index, \
										'<Reference>', effect_modifies_obstruction_reference_combo, 'combo')


					# Setup effect_modifies_obstruction_vbox
					effect_modifies_obstruction_menu = self.setup_event_builder_modifies_obstruction_menu('effect_modifies_obstruction_optionmenu:%s' % key_index)
					effect_modifies_obstruction_optionmenu = gtk.GtkOptionMenu()
					effect_modifies_obstruction_optionmenu.set_menu( effect_modifies_obstruction_menu )
					effect_modifies_obstruction_vbox = self.create_event_widget_container(\
										'effect_modifies_obstruction', key_index, \
										'<ObstructionAttribute>', effect_modifies_obstruction_optionmenu, 'optionmenu')


					effect_toolbar.append_widget(effect_modifies_obstruction_reference_vbox, "", "")
					effect_toolbar.append_widget(effect_modifies_obstruction_vbox, "", "")


					if ( self.eventTree['effect_modifies_obstruction_optionmenu:%s:selection' % key_index] == 'Visible' ):
						# Setup effect_modifies_obstruction_visible_vbox

						each = string.atoi( string.split( effect_modifies_obstruction_reference_combo.entry.get_text(), ' - ')[0] )
						truth_boolean = self.obstructionData[each].visible

						effect_modifies_obstruction_visible_radiobutton_vbox = self.setup_radiobutton_vbox(\
										'effect_modifies_obstruction_visible', key_index, \
										truth_boolean)

						effect_modifies_obstruction_visible_vbox = self.create_event_widget_container(\
										'effect_modifies_obstruction_visible', key_index, \
										'<Boolean>', effect_modifies_obstruction_visible_radiobutton_vbox, 'vbox')


						effect_toolbar.append_widget(effect_modifies_obstruction_visible_vbox, "", "")


					elif ( self.eventTree['effect_modifies_obstruction_optionmenu:%s:selection' % key_index] == 'TextDescription' ):
						# Setup effect_modifies_obstruction_textdescription_vbox
						effect_modifies_obstruction_textdescription_entry = gtk.GtkEntry()
						each = string.atoi( string.split( effect_modifies_obstruction_reference_combo.entry.get_text(), ' - ')[0] )
						if (self.obstructionData[each].description != None):
							effect_modifies_obstruction_textdescription_entry.set_text(self.obstructionData[each].description)
							self.eventTree['effect_modifies_obstruction_textdescription_entry:%s:selection' % key_index] = self.obstructionData[each].description
							effect_modifies_obstruction_textdescription_entry.set_position(0)

						effect_modifies_obstruction_textdescription_vbox = self.create_event_widget_container(\
										'effect_modifies_obstruction_textdescription', key_index, \
										'<TextDescription>', effect_modifies_obstruction_textdescription_entry, 'entry')


						effect_toolbar.append_widget(effect_modifies_obstruction_textdescription_vbox, "", "")


					elif ( self.eventTree['effect_modifies_obstruction_optionmenu:%s:selection' % key_index] == 'Environment_GraphicURL' ):
						# Setup effect_modifies_obstruction_environment_graphic_url_vbox
						effect_modifies_obstruction_environment_graphic_url_entry = gtk.GtkEntry()
						each = string.atoi( string.split( effect_modifies_obstruction_reference_combo.entry.get_text(), ' - ')[0] )
						if (self.obstructionData[each].environment_graphic_url != None):
							effect_modifies_obstruction_environment_graphic_url_entry.set_text(self.obstructionData[each].environment_graphic_url)
							self.eventTree['effect_modifies_obstruction_environment_graphic_url_entry:%s:selection' % key_index] = self.obstructionData[each].environment_graphic_url
							effect_modifies_obstruction_environment_graphic_url_entry.set_position(0)

						effect_modifies_obstruction_environment_graphic_url_vbox = self.create_event_widget_container(\
										'effect_modifies_obstruction_environment_graphic_url', key_index, \
										'<URL>', effect_modifies_obstruction_environment_graphic_url_entry, 'entry')


						effect_toolbar.append_widget(effect_modifies_obstruction_environment_graphic_url_vbox, "", "")


					elif ( self.eventTree['effect_modifies_obstruction_optionmenu:%s:selection' % key_index] == 'Environment_Graphic_Pos' ):
						# Setup effect_modifies_obstruction_xpos_vbox
						effect_modifies_obstruction_xpos_entry = gtk.GtkEntry()
						each = string.atoi( string.split( effect_modifies_obstruction_reference_combo.entry.get_text(), ' - ')[0] )
						effect_modifies_obstruction_xpos_entry.set_text("%i" % self.obstructionData[each].environment_graphic_Xpos)
						self.eventTree['effect_modifies_obstruction_xpos_entry:%s:selection' % key_index] = self.obstructionData[each].environment_graphic_Xpos

						effect_modifies_obstruction_xpos_vbox = self.create_event_widget_container(\
										'effect_modifies_obstruction_xpos', key_index, \
										'<X-Coordinate>', effect_modifies_obstruction_xpos_entry, 'entry')


						# Setup effect_modifies_obstruction_ypos_vbox
						effect_modifies_obstruction_ypos_entry = gtk.GtkEntry()
						each = string.atoi( string.split( effect_modifies_obstruction_reference_combo.entry.get_text(), ' - ')[0] )
						effect_modifies_obstruction_ypos_entry.set_text("%i" % self.obstructionData[each].environment_graphic_Ypos)
						self.eventTree['effect_modifies_obstruction_ypos_entry:%s:selection' % key_index] = self.obstructionData[each].environment_graphic_Ypos

						effect_modifies_obstruction_ypos_vbox = self.create_event_widget_container(\
										'effect_modifies_obstruction_ypos', key_index, \
										'<Y-Coordinate>', effect_modifies_obstruction_ypos_entry, 'entry')


						effect_toolbar.append_widget(effect_modifies_obstruction_xpos_vbox, "", "")
						effect_toolbar.append_widget(effect_modifies_obstruction_ypos_vbox, "", "")


					elif ( self.eventTree['effect_modifies_obstruction_optionmenu:%s:selection' % key_index] == 'CloseUp_GraphicURL' ):
						# Setup effect_modifies_obstruction_closeup_graphic_url_vbox
						effect_modifies_obstruction_closeup_graphic_url_entry = gtk.GtkEntry()
						each = string.atoi( string.split( effect_modifies_obstruction_reference_combo.entry.get_text(), ' - ')[0] )
						if (self.obstructionData[each].closeup_graphic_url != None):
							effect_modifies_obstruction_closeup_graphic_url_entry.set_text(self.obstructionData[each].closeup_graphic_url)
							self.eventTree['effect_modifies_obstruction_closeup_graphic_url_entry:%s:selection' % key_index] = self.obstructionData[each].closeup_graphic_url
							effect_modifies_obstruction_closeup_graphic_url_entry.set_position(0)

						effect_modifies_obstruction_closeup_graphic_url_vbox = self.create_event_widget_container(\
										'effect_modifies_obstruction_closeup_graphic_url', key_index, \
										'<URL>', effect_modifies_obstruction_closeup_graphic_url_entry, 'entry')


						effect_toolbar.append_widget(effect_modifies_obstruction_closeup_graphic_url_vbox, "", "")


			# TextMessage
			elif ( self.eventTree['effect_optionmenu:%s:selection' % key_index] == 'TextMessage' ):
				if ( self.eventTree.has_key('effect_textmessage_entry:%s' % key_index) ):
					text_default = self.eventTree['effect_textmessage_entry:%s' % key_index].get_text()
				else:
					text_default = ""

				# Setup effect_textmessage_vbox
				effect_textmessage_entry = gtk.GtkEntry()
				effect_textmessage_entry.set_text(text_default)

				effect_textmessage_vbox = self.create_event_widget_container(\
								'effect_textmessage', key_index, \
								'<TextMessage>', effect_textmessage_entry, 'entry')


				effect_toolbar.append_widget(effect_textmessage_vbox, "", "")


			# GraphicMessage
			elif ( self.eventTree['effect_optionmenu:%s:selection' % key_index] == 'GraphicMessage' ):

				# Setup graphicmessage_url_vbox
				effect_graphicmessage_url_entry = gtk.GtkEntry()
				if self.eventTree.has_key('effect_graphicmessage_url_entry:%s:selection' % key_index):
					effect_graphicmessage_url_entry.set_text(self.eventTree['effect_graphicmessage_url_entry:%s:selection' % key_index])

				effect_graphicmessage_url_vbox = self.create_event_widget_container(\
								'effect_graphicmessage_url', key_index, \
								'<Graphic URL>', effect_graphicmessage_url_entry, 'entry')


				# Setup graphicmessage_x_vbox
				effect_graphicmessage_x_entry = gtk.GtkEntry()
				if self.eventTree.has_key('effect_graphicmessage_x_entry:%s:selection' % key_index):
					effect_graphicmessage_x_entry.set_text(self.eventTree['effect_graphicmessage_x_entry:%s:selection' % key_index])
				effect_graphicmessage_x_vbox = self.create_event_widget_container(\
								'effect_graphicmessage_x', key_index, \
								'<X-Coordinate>', effect_graphicmessage_x_entry, 'entry')


				# Setup graphicmessage_y_vbox
				effect_graphicmessage_y_entry = gtk.GtkEntry()
				if self.eventTree.has_key('effect_graphicmessage_y_entry:%s:selection' % key_index):
					effect_graphicmessage_y_entry.set_text(self.eventTree['effect_graphicmessage_y_entry:%s:selection' % key_index])
				effect_graphicmessage_y_vbox = self.create_event_widget_container(\
								'effect_graphicmessage_y', key_index, \
								'<Y-Coordinate>', effect_graphicmessage_y_entry, 'entry')


				effect_toolbar.append_widget(effect_graphicmessage_url_vbox, "", "")
				effect_toolbar.append_widget(effect_graphicmessage_x_vbox, "", "")
				effect_toolbar.append_widget(effect_graphicmessage_y_vbox, "", "")


			# PlaySoundFile
			elif ( self.eventTree['effect_optionmenu:%s:selection' % key_index] == 'PlaySoundFile' ):
				if ( self.eventTree.has_key('effect_playsoundfile_entry:%s' % key_index) ):
					text_default = self.eventTree['effect_playsoundfile_entry:%s' % key_index].get_text()
				else:
					text_default = ""

				# Setup effect_playsoundfile_vbox
				effect_playsoundfile_entry = gtk.GtkEntry()
				effect_playsoundfile_entry.set_text(text_default)

				effect_playsoundfile_vbox = self.create_event_widget_container(\
								'effect_playsoundfile', key_index, \
								'<PlaySoundFile>', effect_playsoundfile_entry, 'entry')


				effect_toolbar.append_widget(effect_playsoundfile_vbox, "", "")


			# Close current effect toolbar
			self.eventTree['effect_toolbar:%s' % key_index] = effect_toolbar
			effect_toolbar.show()


#####################################################################

def parse_action_toolbar_widgets(self):

	action = self.eventTree['action_optionmenu:0:selection']

	object_type = self.eventTree['object_optionmenu:0:selection']
	reference = self.eventTree['reference_combo:0:selection']

	object = object_type + '[' + reference + ']'

	return(action, object)


#####################################################################

def parse_object_toolbar_widgets(self):

	preposition = None
	object = None

	if self.eventTree.has_key('object_toolbar:0'):
		preposition = self.eventTree['object2_preposition_combo:0:selection']

		object_type = self.eventTree['object2_optionmenu:0:selection']
		reference = self.eventTree['object2_reference_combo:0:selection']

		object = object_type + '[' + reference + ']'

	return(preposition, object)


#####################################################################

def parse_requirement_toolbars(self):

	import gtk, string

	requirements = ''

	total_requirement_toolbars = 0

	for each in self.eventTree.keys():
		if ( string.find(each, 'requirement_toolbar') != -1):
			total_requirement_toolbars = total_requirement_toolbars + 1

	key_index = 0

	while ( key_index < total_requirement_toolbars ):

		requirement = ''

		# Handle "and/or" Operator if necessary
		if ( key_index > 0 ):
			operator = self.eventTree['requires_and_or_menu:%i:selection' % key_index]
			requirement = ' %s ' % operator

		# Handle "not" checkbutton
		requires_not_string = ''
		not_checkbutton = self.eventTree['requires_not_checkbutton:%i' % key_index]
  		if ( not_checkbutton.get_active() ):
			requires_not_string = '(Not) '

		requirement_type = self.eventTree['requirement_type_optionmenu:%i:selection' % key_index]
		requirement = '%s(Requires %s%s' % ( requirement, requires_not_string, requirement_type)

		if ( requirement_type == 'Player' ):
			player_attribute = self.eventTree['require_player_optionmenu:%i:selection' % key_index]
			# We want to overwrite the word "Player" so that it doesn't appear twice
			requirement = requirement + player_attribute[6:]

			comparison = self.eventTree['requires_player_comparison_optionmenu:%s:selection' % key_index]
			requirement = requirement + '[' + comparison + ']'

			if ( player_attribute == 'PlayerPoints' ):
				entry = self.eventTree['requires_player_comparison_points_entry:%i:selection' % key_index]

			elif ( player_attribute == 'PlayerExp' ):
				entry = self.eventTree['requires_player_comparison_exp_entry:%i:selection' % key_index]

			elif ( player_attribute == 'PlayerHP' ):
				entry = self.eventTree['requires_player_comparison_hp_entry:%i:selection' % key_index]

			elif ( player_attribute == 'PlayerMP' ):
				entry = self.eventTree['requires_player_comparison_mp_entry:%i:selection' % key_index]

			elif ( player_attribute == 'PlayerStr' ):
				entry = self.eventTree['requires_player_comparison_strength_entry:%i:selection' % key_index]

			elif ( player_attribute == 'PlayerIQ' ):
				entry = self.eventTree['requires_player_comparison_intelligence_entry:%i:selection' % key_index]

			elif ( player_attribute == 'PlayerDex' ):
				entry = self.eventTree['requires_player_comparison_dexterity_entry:%i:selection' % key_index]

			elif ( player_attribute == 'PlayerAgil' ):
				entry = self.eventTree['requires_player_comparison_agility_entry:%i:selection' % key_index]

			elif ( player_attribute == 'PlayerCharisma' ):
				entry = self.eventTree['requires_player_comparison_charisma_entry:%i:selection' % key_index]

			elif ( player_attribute == 'PlayerArmorLevel' ):
				entry = self.eventTree['requires_player_comparison_armor_level_entry:%i:selection' % key_index]

			elif ( player_attribute == 'PlayerCurrentWeight' ):
				entry = self.eventTree['requires_player_comparison_current_weight_entry:%i:selection' % key_index]

			requirement = requirement + '(' + entry + ')'


		elif ( requirement_type == 'Room' ):
			room_reference = self.eventTree['requirement_room_reference_combo:%s:selection' % key_index]
			requirement = requirement + '[' + room_reference + ']'

			required_state = self.eventTree['requires_room_property_optionmenu:%s:selection' % key_index]
			requirement = requirement + required_state


		elif ( requirement_type == 'Item' ):
			item_reference = self.eventTree['requirement_item_reference_combo:%s:selection' % key_index]
			requirement = requirement + '[' + item_reference + ']'

			requirement_state = self.eventTree['requires_item_property_optionmenu:%s:selection' % key_index]
			requirement = requirement + requirement_state

			if ( requirement_state == 'ExistsInRoom'):
				room_reference = self.eventTree['requires_exists_in_room_reference_combo:%s:selection' % key_index]
				requirement = requirement + '[' + room_reference + ']'

			elif ( requirement_state == 'Weight' ):
				weight_comparison = self.eventTree['requires_item_weight_comparison_optionmenu:%s:selection' % key_index]
				weight_comparison_entry = self.eventTree['requires_item_comparison_weight_entry:%i:selection' % key_index]

				requirement = requirement + '[' + weight_comparison + '](' + weight_comparison_entry + ')'

			elif ( requirement_state == 'Bulk' ):
				bulk_comparison = self.eventTree['requires_item_bulk_comparison_optionmenu:%s:selection' % key_index]
				bulk_comparison_entry = self.eventTree['requires_item_comparison_bulk_entry:%i:selection' % key_index]

				requirement = requirement + '[' + bulk_comparison + '](' + bulk_comparison_entry + ')'


		elif ( requirement_type == 'Obstruction' ):
			obstruction_reference = self.eventTree['requirement_obstruction_reference_combo:%s:selection' % key_index]
			requirement = requirement + '[' + obstruction_reference + ']'

			requirement_state = self.eventTree['requires_obstruction_property_optionmenu:%s:selection' % key_index]

			if ( requirement_state == 'ExistsInRoom' ):
				room_reference = self.eventTree['requirement_obstruction_exists_in_room_reference_combo:%s:selection' % key_index]
				requirement = requirement + 'ExistsInRoom[' + room_reference + ']'


			elif ( requirement_state == 'ExistsInRoomDirection' ):
				room_reference = self.eventTree['requirement_obstruction_exists_in_room_reference_combo:%s:selection' % key_index]
				requirement = requirement + 'ExistsInRoom[' + room_reference + ']'

				direction_reference = self.eventTree['requirement_obstruction_exists_in_room_direction_reference_combo:%s:selection' % key_index]
				requirement = requirement + 'Direction[' + direction_reference + ']'


			elif ( requirement_state == 'IsVisible' ):
				requirement = requirement + requirement_state



		# Close Requirement Parens
		requirement = requirement + ')'

		requirements = requirements + requirement

		key_index = key_index + 1

	return(requirements)


#####################################################################

def parse_effect_toolbars(self):

	import gtk, string

	effects = ''

	total_effect_toolbars = 0

	for each in self.eventTree.keys():
		if ( string.find(each, 'effect_toolbar') != -1):
			total_effect_toolbars = total_effect_toolbars + 1

	key_index = 0

	while ( key_index < total_effect_toolbars ):

		effect = ''

		effect_type = self.eventTree['effect_optionmenu:%i:selection' % key_index]
		effect = effect + effect_type

		if ( effect_type == 'Adds' ):
			object_type = self.eventTree['effect_adds_object_optionmenu:%i:selection' % key_index]
			effect = effect + ' ' + object_type

			reference = self.eventTree['effect_adds_reference_combo:%i:selection' % key_index]
			effect = effect + '[' + reference + ']'

			preposition = self.eventTree['effect_adds_preposition_combo:%i:selection' % key_index]
			effect = effect + ' ' + preposition

			if ( object_type == "Item" ):
				location = self.eventTree['effect_adds_itemlocation_optionmenu:%i:selection' % key_index]

				if ( location == "Room" ):
					location_reference = self.eventTree['effect_adds_itemlocation_room_reference_combo:%i:selection' % key_index]
					location = 'Room[%s]' % location_reference

				effect = effect + ' ' + location

			elif ( object_type == "Obstruction" ):
				room = self.eventTree['effect_adds_obstruction_room_reference_combo:%i:selection' % key_index]
				direction = self.eventTree['effect_adds_direction_reference_optionmenu:%i:selection' % key_index]

				effect = '%s Room[%s]Direction[%s]' % (effect, room, direction)

		elif ( effect_type == 'Removes' ):
			object_type = self.eventTree['effect_removes_object_optionmenu:%i:selection' % key_index]
			effect = effect + ' ' + object_type

			reference = self.eventTree['effect_removes_reference_combo:%i:selection' % key_index]
			effect = effect + '[' + reference + ']'

			preposition = self.eventTree['effect_removes_preposition_combo:%i:selection' % key_index]
			effect = effect + ' ' + preposition

			if ( object_type == "Item" ):
				location = self.eventTree['effect_removes_itemlocation_optionmenu:%i:selection' % key_index]

				if ( location == "Room" ):
					location_reference = self.eventTree['effect_removes_itemlocation_room_reference_combo:%i:selection' % key_index]
					location = 'Room[%s]' % location_reference

				effect = effect + ' ' + location

			elif ( object_type == "Obstruction" ):
				room = self.eventTree['effect_removes_obstruction_room_reference_combo:%i:selection' % key_index]
				direction = self.eventTree['effect_removes_direction_reference_optionmenu:%i:selection' % key_index]

				effect = '%s Room[%s]Direction[%s]' % (effect, room, direction)

		elif ( effect_type == 'Modifies' ):
			modification_type = self.eventTree['effect_modifies_optionmenu:%i:selection' % key_index]
			effect = effect + ' ' + modification_type

			if ( modification_type == 'Player' ):
				attribute = self.eventTree['effect_modifies_player_optionmenu:%i:selection' % key_index]
				expression = self.eventTree['effect_modifies_expression_optionmenu:%i:selection' % key_index]
				entry = self.eventTree['effect_modifies_number_entry:%i:selection' % key_index]

				effect = '%s %s[%s](%s)' % (effect, attribute, expression, entry)

			elif ( modification_type == 'Room' ) :
				room = self.eventTree['effect_modifies_room_reference_combo:%i:selection' % key_index]
				room_modification_type = self.eventTree['effect_modifies_room_optionmenu:%i:selection' % key_index]

				effect = '%s[%s] %s' % ( effect, room, room_modification_type )

				if ( room_modification_type == 'TextDescription(Long)' ):
					entry = self.eventTree['effect_modifies_textdescription_long_entry:%i:selection' % key_index]
					effect = effect + '[' + entry + ']'

				elif ( room_modification_type == 'TextDescription(Short)' ):
					entry = self.eventTree['effect_modifies_textdescription_short_entry:%i:selection' % key_index]
					effect = effect + '[' + entry + ']'

				elif ( room_modification_type == 'DirectionDescription' ):
					entry = self.eventTree['effect_modifies_direction_description_entry:%i:selection' % key_index]
					effect = effect + '[' + entry + ']'

				elif ( room_modification_type == 'GraphicURL' ):
					entry = self.eventTree['effect_modifies_graphic_url_entry:%i:selection' % key_index]
					effect = effect + '[' + entry + ']'

				elif ( room_modification_type == 'Visited' ):
					boolean = self.eventTree['effect_modifies_room_visited_true_radiobutton:%i:selection' % key_index]
					if (boolean):
						effect = effect + '(true)'
					else:
						effect = effect + '(false)'

				elif ( room_modification_type == 'DirectionObject' ):
					direction_reference = self.eventTree['effect_modifies_room_direction_reference_optionmenu:%i:selection' % key_index]
					direction_attribute = self.eventTree['effect_modifies_room_direction_optionmenu:%i:selection' % key_index]
					effect = effect + '[' + direction_reference + ']' + direction_attribute

					if ( direction_attribute == 'ToWhichRoom'):
						entry = self.eventTree['effect_modifies_room_direction_to_which_room_reference_combo:%i:selection' % key_index]
						effect = '%s[%s]' % ( effect, entry )

					elif ( direction_attribute == 'FirstTransitionText'):
						entry = self.eventTree['effect_modifies_room_direction_firsttransitiontext_entry:%i:selection' % key_index]
						effect = '%s[%s]' % ( effect, entry )

					elif ( direction_attribute == 'TransitionText'):
						entry = self.eventTree['effect_modifies_room_direction_transitiontext_entry:%i:selection' % key_index]
						effect = '%s[%s]' % ( effect, entry )

					elif ( direction_attribute == 'FirstTransitionGraphic'):
						entry = self.eventTree['effect_modifies_room_direction_firsttransitiongraphic_entry:%i:selection' % key_index]
						effect = '%s[%s]' % ( effect, entry )

					elif ( direction_attribute == 'TransitionGraphic'):
						entry = self.eventTree['effect_modifies_room_direction_transitiongraphic_entry:%i:selection' % key_index]
						effect = '%s[%s]' % ( effect, entry )

					elif ( direction_attribute == 'HasMovedThisWay'):
						boolean = self.eventTree['effect_modifies_room_direction_hasmovedthisway_true_radiobutton:%i:selection' % key_index]
						if (boolean):
							effect = effect + '(true)'
						else:
							effect = effect + '(false)'


			elif ( modification_type == 'Item' ):
				item = self.eventTree['effect_modifies_item_reference_combo:%i:selection' % key_index]
				item_modification_type = self.eventTree['effect_modifies_item_optionmenu:%i:selection' % key_index]

				effect = '%s[%s] %s' % ( effect, item, item_modification_type )

				if ( item_modification_type == 'Equipped'):
					boolean = self.eventTree['effect_modifies_item_equipped_true_radiobutton:%i:selection' % key_index]
					if (boolean):
						effect = effect + '(true)'
					else:
						effect = effect + '(false)'

				elif ( item_modification_type == 'Weight'):
					entry = self.eventTree['effect_modifies_item_weight_entry:%i:selection' % key_index]
					effect = '%s(%s)' % ( effect, entry )

				elif ( item_modification_type == 'Bulk'):
					entry = self.eventTree['effect_modifies_item_bulk_entry:%i:selection' % key_index]
					effect = '%s(%s)' % ( effect, entry )

				elif ( item_modification_type == 'TextDescription'):
					entry = self.eventTree['effect_modifies_item_textdescription_entry:%i:selection' % key_index]
					effect = '%s[%s]' % ( effect, entry )

				elif ( item_modification_type == 'Environment_GraphicURL'):
					entry = self.eventTree['effect_modifies_item_environment_graphic_url_entry:%i:selection' % key_index]
					effect = '%s[%s]' % ( effect, entry )

				elif ( item_modification_type == 'Environment_Graphic_Pos'):
					x_entry = self.eventTree['effect_modifies_item_xpos_entry:%i:selection' % key_index]
					y_entry = self.eventTree['effect_modifies_item_ypos_entry:%i:selection' % key_index]
					effect = '%s( %s, %s )' % ( effect, x_entry, y_entry )

				elif ( item_modification_type == 'CloseUp_GraphicURL'):
					entry = self.eventTree['effect_modifies_item_closeup_graphic_url_entry:%i:selection' % key_index]
					effect = '%s[%s]' % ( effect, entry )

				elif ( item_modification_type == 'Icon_GraphicURL'):
					entry = self.eventTree['effect_modifies_item_icon_graphic_url_entry:%i:selection' % key_index]
					effect = '%s[%s]' % ( effect, entry )

				elif ( item_modification_type == 'Equipped_GraphicURL'):
					entry = self.eventTree['effect_modifies_item_equipped_graphic_url_entry:%i:selection' % key_index]
					effect = '%s[%s]' % ( effect, entry )

			elif ( modification_type == 'Obstruction' ):
				obstruction = self.eventTree['effect_modifies_obstruction_reference_combo:%i:selection' % key_index]
				obstruction_modification_type = self.eventTree['effect_modifies_obstruction_optionmenu:%i:selection' % key_index]

				effect = '%s[%s] %s' % ( effect, obstruction, obstruction_modification_type )

				if ( obstruction_modification_type == 'Visible' ):
					boolean = self.eventTree['effect_modifies_obstruction_visible_true_radiobutton:%i:selection' % key_index]
					if (boolean):
						effect = effect + '(true)'
					else:
						effect = effect + '(false)'

				elif ( obstruction_modification_type == 'TextDescription' ):
					entry = self.eventTree['effect_modifies_obstruction_textdescription_entry:%i:selection' % key_index]
					effect = '%s[%s]' % ( effect, entry )

				elif ( obstruction_modification_type == 'Environment_GraphicURL' ):
					entry = self.eventTree['effect_modifies_obstruction_environment_graphic_url_entry:%i:selection' % key_index]
					effect = '%s[%s]' % ( effect, entry )

				elif ( obstruction_modification_type == 'Environment_Graphic_Pos' ):
					x_entry = self.eventTree['effect_modifies_obstruction_xpos_entry:%i:selection' % key_index]
					y_entry = self.eventTree['effect_modifies_obstruction_ypos_entry:%i:selection' % key_index]
					effect = '%s( %s, %s )' % ( effect, x_entry, y_entry )

				elif ( obstruction_modification_type == 'CloseUp_GraphicURL' ):
					entry = self.eventTree['effect_modifies_obstruction_closeup_graphic_url_entry:%i:selection' % key_index]
					effect = '%s[%s]' % ( effect, entry )


		elif ( effect_type == 'TextMessage' ):
			entry = self.eventTree['effect_textmessage_entry:%i:selection' % key_index]
			effect = 'TextMessage[%s]' % entry

		elif ( effect_type == 'GraphicMessage' ):
			url = self.eventTree['effect_graphicmessage_url_entry:%i:selection' % key_index]
			x = self.eventTree['effect_graphicmessage_x_entry:%i:selection' % key_index]
			y = self.eventTree['effect_graphicmessage_y_entry:%i:selection' % key_index]

			effect = 'GraphicMessage[ %s, %s, %s ]' % (url, x, y)

		elif ( effect_type == 'PlaySoundFile' ):
			entry = self.eventTree['effect_playsoundfile_entry:%i:selection' % key_index]
			effect = 'PlaySoundFile[%s]' % entry
			

		effects = effects + ' and ' + effect

		key_index = key_index + 1

	effects = effects[5:] # remove the leading "and" from the effects line

	return(effects)


#####################################################################

def read_event_builder_widgets_into_memory(self):

	event = self.EventObject()

	(event.action, event.object) = self.parse_action_toolbar_widgets()

	(event.preposition, event.object2) = self.parse_object_toolbar_widgets()

	event.requirements = self.parse_requirement_toolbars()

	event.effects = self.parse_effect_toolbars()


	return(event)


#####################################################################

def on_event_builder_add_object_button_clicked(self, obj):

	if not self.eventTree.has_key('object_toolbar:0'):
		self.add_object_toolbar()

		self.rebuild_action_toolbar()
		self.rebuild_object_toolbar()
		self.rebuild_requirement_toolbars()
		self.rebuild_yeilds_and_button_toolbars()
		self.rebuild_effect_toolbars()
		self.display_event_builder()


#####################################################################

def on_event_builder_remove_object_button_clicked(self, obj):

	if self.eventTree.has_key('object_toolbar:0'):
		self.remove_object_toolbar()

		self.rebuild_action_toolbar()
		self.rebuild_object_toolbar()
		self.rebuild_requirement_toolbars()
		self.rebuild_yeilds_and_button_toolbars()
		self.rebuild_effect_toolbars()
		self.display_event_builder()


#####################################################################

def on_event_builder_add_requirement_button_clicked(self, obj):

	self.add_new_requirement_toolbar()

	self.rebuild_action_toolbar()
	self.rebuild_object_toolbar()
	self.rebuild_requirement_toolbars()
	self.rebuild_yeilds_and_button_toolbars()
	self.rebuild_effect_toolbars()
	self.display_event_builder()


#####################################################################

def on_event_builder_remove_requirement_button_clicked(self, obj):
	self.remove_last_requirement_toolbar()


#####################################################################

def on_event_builder_add_effect_button_clicked(self, obj):

	self.add_new_effect_toolbar()

	self.rebuild_action_toolbar()
	self.rebuild_object_toolbar()
	self.rebuild_requirement_toolbars()
	self.rebuild_yeilds_and_button_toolbars()
	self.rebuild_effect_toolbars()
	self.display_event_builder()

#####################################################################

def on_event_builder_remove_effect_button_clicked(self, obj):
	self.remove_last_effect_toolbar()


#####################################################################

def on_append_event_button_clicked(self, obj):

	event = self.read_event_builder_widgets_into_memory()

	event_text = self.format_event_text(event)

	if( self.eventEditor.event_editor_display_reference_names_radiobutton.get_active() ):
		event_text = self.convert_reference_numbers_to_names(event_text)

	self.eventEditor.event_editor_textbox.insert_defaults(event_text)


#####################################################################
# Widgets
#####################################################################
# event_builder_viewport

#####################################################################
# Data Variables
#####################################################################
# self.action = ""
# self.object = ""
# self.preposition = ""
# self.object2 = ""
# self.requirements = "" # don't forget to error-check this while parsing!
# self.effects = "" # don't forget to error-check this while parsing!
# self.has_been_executed = 0 # boolean # Not currently implemented. Aids in point calculations

# EOF
