/******************************
The COG Engine
Player Object Class Files
Last Modified on 2001.01.10

This code is released under the GPL (GNU Public License)
For more information please refer to http://www.gnu.org/copyleft/gpl.html
Copyright (2000,2001) Steven M. Castellotti

******************************/

import java.io.Serializable;
import java.util.Hashtable;

public class PlayerOBJ implements Serializable {
	public String Name;
	public String Email_Address;
	public DirectionInfoOBJ Facing; // Direction which the player is facing
	public int Points;
	public int Exp; // Experience Points
	public int experienceLevel; // Experience Level
	public int HP; // Health Points
	public int MP; // Magic Points
	public int Str; // Strength
	public int IQ; // Intelligence
	public int Dex; // Dexterity
	public int Agil; // Agility
	public int Charisma; // Charisma
	public int Armor_Level;
	public int Max_Weight; // Maximum weight a player can carry at any one time (Managed by Get)
	public int Max_Bulk;
	public int Current_Weight;
	public int Current_Bulk;
	public RoomOBJ CurrentRoom;
	public boolean[] Items;
	public Hashtable inventory;
} // PlayerOBJ class
