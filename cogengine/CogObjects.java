/******************************
The COG Engine
Object Class Files
Last Modified on 2000.03.18

		This code is released under the GPL (GNU Public License)
		For more information please refer to http://www.gnu.org/copyleft/gpl.html
		Copyright (2000) Steven M. Castellotti

******************************/

import java.io.Serializable;

class GameInfoOBJ implements Serializable {
	String Game_Title;
	String Version_Number; // this should remain a string
	String Game_Designer;
	String Game_Designer_Email_Address;
	String LastUpdate;
	boolean DebugMode;
	String GameURL;
	String DatabaseURL;
	int TotalRooms;
	int TotalDirections;
	int TotalItems;
	int TotalObstructions;
	int TotalVerbs;
	boolean ShowAllVerbs;
	String Introduction_Text;
	String ImageLoading_GraphicURL;
	String Introduction_GraphicURL;
	int PreferredGraphicSizeX;
	int PreferredGraphicSizeY;
	boolean ShowStats;
	boolean ShowInventory;
	boolean ShowCommandLine;
	boolean ShowCompass;
	boolean CenterButtonIndicatesItems;
	boolean LoadAllCompassImages;
	String MenuButton_GraphicURL;
	String GameInfoHeaderNotes;
	String DirectionsHeaderNotes;
	String RoomHeaderNotes;
	String ItemHeaderNotes;
	String ObstructionHeaderNotes;
	String EventHeaderNotes;
	String VerbHeaderNotes;
} // GameInfoOBJ

class DirectionInfoOBJ implements Serializable {
	// Note - DirectionInfoOBJ objects are used to
	// keep track of infomation relating to a particular
	// direction for the entire game (such as the
	// direction's name).  DirectionOBJ objects are used
	// to keep track of information relating to a particular
	// direction within a particular room.
	int Number;
	String Name;
	String Abbreviation;
	String CG_AvailableURL;
	String CG_UnavailableURL;
	String CG_SpecialURL;
} // DirectionInfoOBJ

class PlayerOBJ implements Serializable {
	String Name;
	String Email_Address;
	DirectionInfoOBJ Facing; // Direction which the player is facing
	int Points;
	int Exp; // Experience Points
	int HP; // Health Points
	int MP; // Magic Points
	int Str; // Strength
	int IQ; // Intelligence
	int Dex; // Dexterity
	int Agil; // Agility
	int Charisma; // Charisma
	int Armor_Level;
	int Max_Weight; // Maximum weight a player can carry at any one time (Managed by Get)
	int Max_Bulk; 
	int Current_Weight;
	int Current_Bulk;
	RoomOBJ CurrentRoom;
	boolean[] Items;
} // PlayerOBJ class

class RoomOBJ implements Serializable {
	int Number;
	String Name;
	boolean Visited; // this has been moved back to RoomOBJ
	String GraphicURL;
	String Description_Long;
	String Description_Short;
	String Direction_Description;
	DirectionOBJ[] DirectionArray;
	String Items;
	String Notes;
} // RoomOBJ class

class DirectionOBJ implements Serializable {
	// Note - DirectionOBJ objects are used to keep track of
	// information relating to a particular direction within
	// a particular room. DirectionInfoOBJ objects are used
	// to keep track of infomation relating to a particular
	// direction for the entire game (such as the direction's name)
	int ToWhichRoom;
	String Obstructions;
	boolean HasMovedThisWay;
	String FirstTransitionText;
	String TransitionText;
	String FirstTransitionGraphic;
	String TransitionGraphic;
	String State;
} // DirectionOBJ class

class ItemOBJ implements Serializable {
	int Number;
	String Name;
	String Aliases;
	String Environment_GraphicURL;
	int Environment_Graphic_Xpos, Environment_Graphic_Ypos; // Coordinates in relation to upper-left corner of room graphic
	String CloseUp_GraphicURL;
	String Icon_GraphicURL;
	String Equipped_GraphicURL;
	String Description;
	String Location;
	boolean Equipped;
	int Weight; // negative weight implies that object cannot be picked up
	int Bulk; // negative bulk indicates how much a "container" can hold
	String Notes;
} // ItemOBJ class

class ObstructionOBJ implements Serializable {
	int Number;
	String Name;
	String Aliases;
	String Environment_GraphicURL;
	int Environment_Graphic_Xpos, Environment_Graphic_Ypos; // Coordinates in relation to upper-left corner of room graphic
	String CloseUp_GraphicURL;
	String Description;
	String Type; // set to "Antagonist" or "Obstacle" etc.
	String Locations;
	boolean Visible;
	String Notes;
} // ObstructionOBJ class

class VerbOBJ implements Serializable { 
	int Number;
	String Name;
	String Aliases;
	EventOBJ[] Events;
	int TotalEvents;
	int EventsFilled;
} // VerbOBJ

class EventOBJ implements Serializable {
	String Action;
	String Object;
	String Preposition;
	String Object2;
	String Requirements; // Don't forget to error-check this while parsing!
	String EffectString; // Don't forget to error-check this while parsing!
	boolean HasBeenExecuted; // Not currently implemented. Aids in point calculations
} // EventOBJ
