/******************************
The COG Engine
Room Object Class Files
Last Modified on 2001.01.10

This code is released under the GPL (GNU Public License)
For more information please refer to http://www.gnu.org/copyleft/gpl.html
Copyright (2000,2001) Steven M. Castellotti

******************************/

import java.io.Serializable;
import java.util.Hashtable;

public class RoomOBJ implements Serializable {
	public int Number;
	public String Name;
	public boolean Visited; // this has been moved back to RoomOBJ
	public String GraphicURL;
	public String Description_Long;
	public String Description_Short;
	public String Direction_Description;
	public DirectionOBJ[] DirectionArray;
	public Hashtable directionHash;
	public String Items;
	public String Notes;
} // RoomOBJ class
