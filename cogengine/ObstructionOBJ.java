/******************************
The COG Engine
Obstruction Object Class Files
Last Modified on 2001.01.10

This code is released under the GPL (GNU Public License)
For more information please refer to http://www.gnu.org/copyleft/gpl.html
Copyright (2000,2001) Steven M. Castellotti

******************************/

import java.io.Serializable;

public class ObstructionOBJ implements Serializable {
	public int Number;
	public String Name;
	public String Aliases;
	public String Environment_GraphicURL;
	public int Environment_Graphic_Xpos, Environment_Graphic_Ypos; // Coordinates in relation to upper-left corner of room graphic
	public String CloseUp_GraphicURL;
	public String Description;
	public String Type; // set to "Antagonist" or "Obstacle" etc.
	public String Locations;
	public boolean Visible;
	public String Notes;
} // ObstructionOBJ class
