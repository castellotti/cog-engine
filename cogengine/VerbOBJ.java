/******************************
The COG Engine
Verb Object Class Files
Last Modified on 2001.01.10

This code is released under the GPL (GNU Public License)
For more information please refer to http://www.gnu.org/copyleft/gpl.html
Copyright (2000,2001) Steven M. Castellotti

******************************/

import java.io.Serializable;
import java.util.Hashtable;

public class VerbOBJ implements Serializable {
	public int Number;
	public String Name;
	public String Aliases;
	public EventOBJ[] Events;
	public Hashtable eventHash;
	public int TotalEvents;
	public int EventsFilled;
} // VerbOBJ
