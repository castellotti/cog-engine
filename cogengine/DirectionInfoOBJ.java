/******************************
The COG Engine
Direction Information Object Class Files
Last Modified on 2001.01.10

This code is released under the GPL (GNU Public License)
For more information please refer to http://www.gnu.org/copyleft/gpl.html
Copyright (2000,2001) Steven M. Castellotti

******************************/

import java.io.Serializable;

public class DirectionInfoOBJ implements Serializable {
	// Note - DirectionInfoOBJ objects are used to
	// keep track of infomation relating to a particular
	// direction for the entire game (such as the
	// direction's name).  DirectionOBJ objects are used
	// to keep track of information relating to a particular
	// direction within a particular room.
	public int Number;
	public String Name;
	public String Abbreviation;
	public String CG_AvailableURL;
	public String CG_UnavailableURL;
	public String CG_SpecialURL;
} // DirectionInfoOBJ
