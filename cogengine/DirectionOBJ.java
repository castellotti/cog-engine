/******************************
The COG Engine
Direction Object Class Files
Last Modified on 2001.01.10

This code is released under the GPL (GNU Public License)
For more information please refer to http://www.gnu.org/copyleft/gpl.html
Copyright (2000,2001) Steven M. Castellotti

******************************/

import java.io.Serializable;
import java.util.Hashtable;

public class DirectionOBJ implements Serializable {
	// Note - DirectionOBJ objects are used to keep track of
	// information relating to a particular direction within
	// a particular room. DirectionInfoOBJ objects are used
	// to keep track of infomation relating to a particular
	// direction for the entire game (such as the direction's name)
	public int ToWhichRoom;
	public String Obstructions;
	public boolean HasMovedThisWay;
	public String FirstTransitionText;
	public String TransitionText;
	public String FirstTransitionGraphic;
	public String TransitionGraphic;
	public String State;
} // DirectionOBJ class
