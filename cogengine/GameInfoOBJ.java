/******************************
The COG Engine
Game Information Object Class Files
Last Modified on 2001.01.10

This code is released under the GPL (GNU Public License)
For more information please refer to http://www.gnu.org/copyleft/gpl.html
Copyright (2000,2001) Steven M. Castellotti

******************************/

import java.io.Serializable;

public class GameInfoOBJ implements Serializable {
	public String Game_Title;
	public String Version_Number; // this should remain a string
	public String Game_Designer;
	public String Game_Designer_Email_Address;
	public String LastUpdate;
	public boolean DebugMode;
	public String GameURL;
	public String DatabaseURL;
	public int TotalRooms;
	public int TotalDirections;
	public int TotalItems;
	public int TotalObstructions;
	public int TotalVerbs;
	public boolean ShowAllVerbs;
	public String Introduction_Text;
	public String Image_Directory;
	public String ImageLoading_GraphicURL;
	public String Introduction_GraphicURL;
	public int PreferredGraphicSizeX;
	public int PreferredGraphicSizeY;
	public boolean ShowStats;
	public boolean ShowInventory;
	public boolean ShowCommandLine;
	public boolean ShowCompass;
	public boolean CenterButtonIndicatesItems;
	public boolean LoadAllCompassImages;
	public String MenuButton_GraphicURL;
	public String GameInfoHeaderNotes;
	public String DirectionsHeaderNotes;
	public String RoomHeaderNotes;
	public String ItemHeaderNotes;
	public String ObstructionHeaderNotes;
	public String EventHeaderNotes;
	public String VerbHeaderNotes;
} // GameInfoOBJ
