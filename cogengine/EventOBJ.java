/******************************
The COG Engine
Event Object Class Files
Last Modified on 2001.01.10

This code is released under the GPL (GNU Public License)
For more information please refer to http://www.gnu.org/copyleft/gpl.html
Copyright (2000,2001) Steven M. Castellotti

******************************/

import java.io.Serializable;

public class EventOBJ implements Serializable {
	public String Action;
	public String Object;
	public String Preposition;
	public String Object2;
	public String Requirements; // Don't forget to error-check this while parsing!
	public String EffectString; // Don't forget to error-check this while parsing!
	public boolean HasBeenExecuted; // Not currently implemented. Aids in point calculations
} // EventOBJ
