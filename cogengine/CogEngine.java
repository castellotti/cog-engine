/**	The COG Engine
		--------------
		The Cycon Online Gaming Engine.

		Conceived, Created, and Coded by
			Steven M. Castellotti
			(SteveC@innocent.com)

		This program is released under the GPL (GNU Public License) Version 2
		For more information please refer to http://www.gnu.org/copyleft/gpl.html
		Copyright (1999-2001) Steven M. Castellotti

		Version : 0.92
		Last Update : 2001.09.22


	Bug List
	--------
		 - "Looking around, you see a leaves."
		 - If you click in the OutputArea, it will no longer scroll automatically,
			unless you scroll down manually and click at the end of the last
			line of output (Under certain implementations of Java)

	To-Do List
	----------
		 - Add DisplayRoomDetails routine for Debug Mode
		 - Add more useful command line error messages ("I don't understand your command." vs. "You can't do that!")
		 - Insert more try-catch sequences around all places that the
			program could possibly break ( Mainly I/O Routines )
		 - Add amusing jokes and quotes so that people don't get bored while reading over the source (c:

	Future Feature Wish List
	------------------------
		 - Multiple GUI's (Underway)


	Method Headers
	--------------
	public class CogEngine extends Applet implements ActionListener {
	public void init() {
	public void start() {
	public void stop() {
	public void destroy() {
	public void paint(Graphics g) {
	public void actionPerformed(ActionEvent ActionOccured) {
	public void DisplayImage( String GraphicURLString, int Xpos, int Ypos ) {
	public void DisplayIntroduction() {
	public void DisplayRoom(RoomOBJ Room) {
	public void CommandLineParser(String Command) {
	public void DisplayVerbs() {
	public void RoomMover(int Direction) {
	public void ExamineObject(String ObjectName) {
	public void GetItem(String ItemName) {
	public void DropItem(String ItemName) {
	public void RoomWarp(String Word) {
	public void ExecuteEffect( String Effect ) {
	public boolean RequirementsMet( String Requirements ) {
	public void AddItemToRoom( int RoomNumber, int ItemNumber ) {
	public void RemoveItemFromRoom( int RoomNumber, int ItemNumber ) {
	public void AddObstructionToRoom( int ObstructionNumber, int RoomNumber, int DirectionNumber ) {
	public void RemoveObstructionFromRoom( int ObstructionNumber, int RoomNumber, int DirectionNumber ) {
	public boolean RoomContainsItem( int RoomNumber, int ItemNumber ) {
	public boolean RoomContainsObstruction( int RoomNumber, int ObstructionNumber ) {
	public int ResolveDirectionName( String DirectionName ) {
	public boolean VerbMatches( String VerbName, int VerbIndex ) {
	public String ResolveVerb( String VerbAlias ) {
	public String ParseCommandLineObjects( String Remainder ) {
	public String ParseObject( String Phrase, String SearchFrom ) {
	public int ResolveItemName(String ItemName, String WhereToLook) {
	public int ResolveObstructionName(String ObstructionName, String WhereToLook) {
	public int FindItemAlias (String ItemName, String WhereToLook) {
	public int FindObstructionAlias (String ObstructionName, String WhereToLook) {
	public String ResolveEvent( String Action, String Object, String Object2 ) {
	public void CheckEmptyDirection( int RoomNumber, int DirectionNumber ) {
	public boolean MakeComparison( String Comparison, int val1, int val2 ) {
	public int EvaluateExpression( String Expression, int val1, int val2 ) {
	public boolean StartsWithVowel(String InputString) {
	public void InitializeGUI() {
	public void addGB( Container container, Component component, int x, int y  ) {
	public String GetDirectionState(int DirectionNumber ) {

*/

import java.applet.Applet;
import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.net.URL;
import java.util.StringTokenizer;

public class CogEngine extends Applet implements ActionListener {

	// Global Variables

	private URL DatabaseURL;
	private GameInfoOBJ GameInfo;
	private PlayerOBJ Player;
	private DirectionInfoOBJ[] DirectionInfoArray;
	private RoomOBJ[] RoomArray;
	private ItemOBJ[] ItemArray;
	private ObstructionOBJ[] ObstructionArray;
	private VerbOBJ[] VerbArray;

	private URL CurrentURL;
	private Cursor MouseCursor;
	private String Command;
	private String LastCommand;

	private Panel Top;
	private Panel Bottom;
	private Panel Menu;
	private Panel Control;
	private Panel Compass;
	private GraphicPanel GraphicArea;

	private TextArea EditorArea;

	private TextArea OutputArea;
	private TextArea InfoArea;
	private TextArea InventoryArea;
	private TextField CommandLine;
	private GraphicButton NW,N,NE,W,C,E,SW,S,SE,U,D,CompassMenuGraphic;
	private String[] DirectionStates; // Used to remember which graphic is currently being
	                                  // displayed within each graphic button
	private Button CompassMenuText;

	GridBagConstraints constraints = new GridBagConstraints();

	
	public void init() {

		// This first method downloads the Game Database File, as specified by an HTML parameter thrown to the applet.
		// Next, init deserializes the information contained in that file, writing the information into memory
		// Finally, the GUI Initialization method is called


		// Database Download
		try {
			DatabaseURL = new URL( getCodeBase() + (getParameter("DatabaseFilename")) );
			// DatabaseURL = new URL( getParameter("DatabaseFilename") );
			System.err.println("DatabaseURL : (" + DatabaseURL + ")\n"); // For debugging purposes
		} catch (Exception Database_Access_Error) {
			System.err.println("Error Downloading Database");			
			System.err.println(Database_Access_Error + "\n");
		} // catch

		// Database Initialization
		try {
			ObjectInputStream COG_In = new ObjectInputStream( DatabaseURL.openStream() );

			GameInfo = ( GameInfoOBJ )COG_In.readObject(); // breaks on this line
			DirectionInfoArray = ( DirectionInfoOBJ[] )COG_In.readObject();
			Player = ( PlayerOBJ )COG_In.readObject();
			RoomArray = ( RoomOBJ[] )COG_In.readObject();
			ItemArray = ( ItemOBJ[] )COG_In.readObject();
			ObstructionArray = ( ObstructionOBJ[] )COG_In.readObject();
			VerbArray = ( VerbOBJ[] )COG_In.readObject();
		} catch (Exception Database_Initialization_Error) {
			System.err.println("Error Initializing Database");
			System.err.println(Database_Initialization_Error + "\n");
		}

		if (GameInfo.DebugMode)
			System.err.println("Debug Mode Enabled.\n");

		if ( GameInfo.TotalRooms != (RoomArray.length - 1) )
			System.err.println("Warning: TotalRooms Discrepancy!\n");
		// Do the same thing for DatabaseURL (parameter <-> GameInfo)

		// Make certain that Image Directory values have been entered correctly
		if ( GameInfo.Image_Directory.valueOf( GameInfo.Image_Directory.length() - 1 ) != "/" ) {
			GameInfo.Image_Directory = GameInfo.Image_Directory + "/";
		}

		InitializeGUI(); // Sets up the Graphic Interface

	} // init


	public void start() {

		// This method first makes a call to Display the Game's Introduction,
		// and then displays the first room that the player starts out in

		if ( Player.CurrentRoom == null ) {
			Player.CurrentRoom = RoomArray[1];
		}

		if ( ( Player.CurrentRoom.Number == 1 ) && ( Player.CurrentRoom.Visited == false ) ) {
			DisplayIntroduction();
			// OutputArea.append("Press Enter to Begin.\n");
		}

		DisplayRoom(Player.CurrentRoom);
		repaint();// if i dont do this, i won't see the graphics correctly. (Why?)

	} // start


	public void stop() {

		// This method gets called when a user stops the applet.
		// As it is also called whenever an appletview window is shaded,
      // the following two lines are commented out

		//OutputArea.append("\n\n");
		//OutputArea.append("Thank you for playing " + GameInfo.Game_Title + ".\n");
	} // stop


	public void destroy() {

		// This method doesn't do a damn thing.

	} // destroy


//	public void paint(Graphics g) {
//	} // paint


	public void actionPerformed(ActionEvent ActionOccured) {

		// This method basically takes control after start finishes executing.
		// It is called whenever a carriage return is entered into the command line
		// or whenever a button is depressed.

		Command = ActionOccured.getActionCommand();

		if ( Command.equalsIgnoreCase("Center") )
			Command = "Look";

		CommandLineParser(Command);
	} // actionPerformed


	public void DisplayImage( String GraphicURLString, int Xpos, int Ypos ) {

		String PreviousCommandLine = "";

		// Sequence to display Graphics
		if (GameInfo.ShowCommandLine)
			PreviousCommandLine = CommandLine.getText(); // use this to return to original command line after displaying graphic
		try {
			CurrentURL = new URL(getCodeBase() + GameInfo.Image_Directory + GraphicURLString);
		} catch (Exception BadURL) {
			System.err.println("Graphic URL \"");
			System.err.println( GraphicURLString );
			System.err.println("\" is Malformed!\n");
		}
		if ( (Xpos == 0) && (Ypos== 0) )
			GraphicArea.setImage(this, CurrentURL );
		if (GameInfo.ShowCommandLine)
			CommandLine.setText( PreviousCommandLine ); // see above; use this to maintain original command line
	} //DisplayImage


	public void DisplayIntroduction() {

		// DisplayIntroduction begins by displaying the game's title and the Introduction Text,
		// as defined in the Game-Info text file. The Introduction Graphic is already displayed
		// as part of the InitializeGUI routine.

		try {
			CurrentURL = new URL(getCodeBase() + GameInfo.Image_Directory + GameInfo.Introduction_GraphicURL);
		} catch (Exception e) {
			System.err.println("Bad URL for Introduction Graphic:");
			System.err.println(GameInfo.Introduction_GraphicURL);
		}
		GraphicArea.setImage(this, CurrentURL);
		OutputArea.append(GameInfo.Game_Title + "\n\n");
		OutputArea.append("  " + GameInfo.Introduction_Text); // Displays Games Intro Text

	} // DisplayIntroduction


	public void DisplayRoom(RoomOBJ Room) {

		// DisplayRoom is a very useful method, and gets called at the beggining of the game
		// or after pretty much any action takes place in the game. In the future, a new thread
		// will be created to download and then display each room's graphic. That way, if a player
		// wants to move before the graphic has finished downloading (a very reasonable desire for
		// slow connections) the thread can be killed and a new one will be created by the new
		// DisplayRoom method.

		int TempInt;
		String TempStr;
		StringTokenizer RoomToken;
		boolean DisplayedSomething;

		DisplayImage( Room.GraphicURL, 0, 0 ); // Displays the room's graphic
		MouseCursor = MouseCursor.getPredefinedCursor(Cursor.DEFAULT_CURSOR);
		this.setCursor(MouseCursor);

		// Sequence to display Player Statistics
		if (GameInfo.ShowStats) {
			InfoArea.setText("");
			InfoArea.append(GameInfo.Game_Title + "\n\n");
			InfoArea.append("Player's Name : " + Player.Name + "\n");
			if (GameInfo.DebugMode)
				InfoArea.append("Current Room # : " + Player.CurrentRoom.Number + "\n"); // comment this out unless debugging
			if (Player.Points != -1)
				InfoArea.append("Points : " + Player.Points + "\n");
			if (Player.Exp != -1)
				InfoArea.append("Experience : " + Player.Exp + "\n");
			if (Player.HP != -1)
				InfoArea.append("Health : " + Player.HP + "\n");
			if (Player.MP != -1)
				InfoArea.append("Magic : " + Player.MP + "\n");
			if (Player.Str != -1)
				InfoArea.append("Strength : " + Player.Str + "\n");
			if (Player.IQ != -1)
				InfoArea.append("Intelligence : " + Player.IQ);// 10th line down
		}

		// Sequence to display Player's Inventory
		if (GameInfo.ShowInventory) {
			InventoryArea.setText("");
			InventoryArea.append("Inventory: \n\n");
			for (int TempCount = 1; TempCount <= Player.Items.length-1; TempCount++)
				if (Player.Items[TempCount])
				   if (ItemArray[TempCount].Equipped) {
					   InventoryArea.append(ItemArray[TempCount].Name + " (equipped)\n");
					} else {
					   InventoryArea.append(ItemArray[TempCount].Name + "\n");
					}
		}

		// Sequence to display Current Room
		if (!Player.CurrentRoom.Visited) {
			OutputArea.append("\n\n");
			OutputArea.append("  " + Room.Description_Long + "\n");
			OutputArea.append("  " + Room.Direction_Description);
			Player.CurrentRoom.Visited = true;
		}
		else {
			OutputArea.append("\n\n");
			OutputArea.append(Room.Description_Short);
		}

		// Sequence to Update CompassButton Graphics
		// Graphics should only be downloaded (by calling setImage) if
		// a different graphic is used that the one currently displayed

		for(TempInt = 1; TempInt <= GameInfo.TotalDirections; TempInt++) {
			TempStr = GetDirectionState(TempInt);
			if ( !(DirectionStates[TempInt].equals(TempStr))
			&& !( (GameInfo.CenterButtonIndicatesItems) && (TempInt == 5) ) )
				try {
					if (TempStr.equals("Available")) {
						CurrentURL = new URL( getCodeBase() + GameInfo.Image_Directory + DirectionInfoArray[TempInt].CG_AvailableURL );
						DirectionStates[TempInt] = "Available";
					}
					else if (TempStr.equals("Unavailable")) {
						CurrentURL = new URL( getCodeBase() + GameInfo.Image_Directory + DirectionInfoArray[TempInt].CG_UnavailableURL );
						DirectionStates[TempInt] = "Unavailable";
					}
					else if (TempStr.equals("Obstructed")) {
						CurrentURL = new URL( getCodeBase() + GameInfo.Image_Directory + DirectionInfoArray[TempInt].CG_SpecialURL );
						DirectionStates[TempInt] = "Obstructed";
					}
					switch (TempInt) {
						case (1) :
							NW.setImage(this, CurrentURL); break;
						case (2) :
							N.setImage(this, CurrentURL); break;
						case (3) :
							NE.setImage(this, CurrentURL); break;
						case (4) :
							W.setImage(this, CurrentURL); break;
						case (5) :
							// The center button is special, if CenterButtonIndicatesItems is
							// turned on, graphics are used not to indicate the presence of an
							// obstruction, but to indicate the presence of items in the Current Room
							if ( !(GameInfo.CenterButtonIndicatesItems) )
								C.setImage(this, CurrentURL);
							break;
						case (6) :
							E.setImage(this, CurrentURL); break;
						case (7) :
							SW.setImage(this, CurrentURL); break;
						case (8) :
							S.setImage(this, CurrentURL); break;
						case (9) :
							SE.setImage(this, CurrentURL); break;
						case (10) :
							U.setImage(this, CurrentURL); break;
						case (11) :
							D.setImage(this, CurrentURL); break;
					}
				} catch (Exception e) {
					System.err.println("Error setting new Image for Compass Button #" + TempInt + "!");
				}
		} // for loop


		// Sequence for displaying Obstrucions in Current Room
		for (int TempCount = 1; TempCount <= Player.CurrentRoom.DirectionArray.length-1; TempCount++)
			if ( ( Player.CurrentRoom.DirectionArray[TempCount] != null )
			&& ( (Player.CurrentRoom.DirectionArray[TempCount].Obstructions != null) ) ) {
				DisplayedSomething = false; // keeps track of whether or not any "Visible" obstructions are present
				RoomToken = new StringTokenizer(Player.CurrentRoom.DirectionArray[TempCount].Obstructions, ",");
				TempStr = RoomToken.nextToken().trim();
				TempInt = Integer.parseInt(TempStr);
				if ( ObstructionArray[TempInt].Visible ) {
					DisplayedSomething = true;
					OutputArea.append("\nA");
					if (StartsWithVowel( ObstructionArray[TempInt].Name ) )
						OutputArea.append("n");
					// We first want to output any Environmental Item Graphics
    			if (ObstructionArray[TempInt].Environment_GraphicURL != null) {
						try {
							CurrentURL = new URL ( getCodeBase() + GameInfo.Image_Directory + ObstructionArray[TempInt].Environment_GraphicURL );
							GraphicArea.addImageLayer(this, CurrentURL,
							ObstructionArray[TempInt].Environment_Graphic_Xpos,
							ObstructionArray[TempInt].Environment_Graphic_Ypos);
						} catch (Exception e) { System.err.println("Obstruction Display broke"); }
					}
				OutputArea.append( " " + ObstructionArray[TempInt].Name.toLowerCase() );
				} // (2)
				while ( RoomToken.hasMoreTokens() ) {
					TempStr = RoomToken.nextToken().trim();
					TempInt = Integer.parseInt(TempStr);
					if ( ObstructionArray[TempInt].Visible ) {
						if (DisplayedSomething) {
							OutputArea.append(", and a");
							if (StartsWithVowel( ObstructionArray[TempInt].Name ) )
								OutputArea.append("n");
						}
						else {
							DisplayedSomething = true;
							OutputArea.append("\nA ");
							if (StartsWithVowel( ObstructionArray[TempInt].Name ) )
								OutputArea.append("n");
		} // for-loop
						OutputArea.append( " " + ObstructionArray[TempInt].Name.toLowerCase() );
					}  // then (3)
				} // while
				if (DisplayedSomething) {
					OutputArea.append(" prevents you from moving ");
					OutputArea.append( DirectionInfoArray[TempCount].Name.toLowerCase() );
					OutputArea.append(".");
				} // then (2)
			} // then (1)


		// Sequence to display Items in Current Room
		if ( Player.CurrentRoom.Items != null ) {
			if ( (GameInfo.CenterButtonIndicatesItems)
			&& (DirectionStates[5].equals("ItemsNotPresent")) )
				// We want to change the center button's image to the special image
				// only if it's not already set to that image (and this feature is turned on!)
				try {
					CurrentURL = new URL ( getCodeBase() + GameInfo.Image_Directory + DirectionInfoArray[5].CG_SpecialURL );
					C.setImage(this, CurrentURL);
					DirectionStates[5] = "ItemsPresent";
				} catch (Exception e) {
					System.err.println("Error setting new image for Center Compass Button!");
				}
			OutputArea.append("\nLooking around, you see a");
			RoomToken = new StringTokenizer(Player.CurrentRoom.Items, ","); // shouldn't we look for ", " - possible bug here
			while ( RoomToken.hasMoreTokens() ) {
				TempStr = RoomToken.nextToken().trim();
				TempInt = Integer.parseInt(TempStr);
				if (StartsWithVowel( ItemArray[TempInt].Name ) )
					OutputArea.append("n");
					// We first want to output any Environmental Item Graphics
    			if (ItemArray[TempInt].Environment_GraphicURL != null) {
					try {
						CurrentURL = new URL ( getCodeBase() + GameInfo.Image_Directory + ItemArray[TempInt].Environment_GraphicURL );
						GraphicArea.addImageLayer(this, CurrentURL,
							ItemArray[TempInt].Environment_Graphic_Xpos,
							ItemArray[TempInt].Environment_Graphic_Ypos);
					} catch (Exception e) { System.err.println("Item Environment Display broke"); }
				}
				OutputArea.append( " " + ItemArray[TempInt].Name.toLowerCase() );
				if ( RoomToken.hasMoreTokens() ) {
					OutputArea.append(", and a");
					if (StartsWithVowel( ItemArray[TempInt].Name ) )
						OutputArea.append("n");
				}
			}
			OutputArea.append(".");
		}
		else
			if ( (GameInfo.CenterButtonIndicatesItems)
			&&  (DirectionStates[5].equals("ItemsPresent")) )
				try {
					CurrentURL = new URL ( getCodeBase() + GameInfo.Image_Directory + DirectionInfoArray[5].CG_AvailableURL );
					C.setImage(this,CurrentURL);
					DirectionStates[5] = ("ItemsNotPresent");
				} catch (Exception e) {
					System.err.println("Error setting new image for Center Compass Button!");
				}
		// End of Item display sequence

	} // DisplayRoom


	public void CommandLineParser(String Command) {

		// This method gets called after an ActionEvent occurs, which is whenever a carriage return
		// is entered into the command line and whenever a button is depressed. It takes the first
		// word of the command line, assumes it to be the verb, and stores the rest into the Remainder
		// variable. A Legal Command line is of the form: <Verb> [ <Object> [ <Preposition> ] [ <Object> ] ]
		// A <Preposition> can be any word or phrase, and may include spaces. The <Object>'s may
		// be entered as either the literal object's name, or it's alias (as long as the alias is unique
		// as far the the current room and player's inventory are concerned).
		// This method's code may be fairly messy, but it works.

		StringTokenizer CommandLineToken;
		int Direction = 0;
		String Verb = ""; // protects against null command lines
		String Remainder = "";
		boolean CommandExecuted = false; // determines whether or not to clear the command line
		boolean TempBoolean;

		if (GameInfo.DebugMode)
			System.err.println("\n - Command: \"" + Command + "\"");

		Command = Command.trim();
		if ( Command.endsWith(".") )
			Command = Command.substring( 0, Command.length() - 1 ); // removes trailing period, if one exists
		CommandLineToken = new StringTokenizer ( Command, " " );
		if ( CommandLineToken.hasMoreTokens() )
			Verb = CommandLineToken.nextToken();
		Verb = Verb.toLowerCase(); // very cool way of reducing number of conditionals

		while ( CommandLineToken.hasMoreTokens() )
			Remainder += " " + CommandLineToken.nextToken().trim();
		Remainder = Remainder.trim(); // we would end up with a space before the first item number if we didn't do this

		// Begin Parsing

		// ----------------
		// Hard-Wired Verbs
		// ----------------

		if ( (Verb.equals("look")) || (Verb.equals("l")) ) {
			TempBoolean = Player.CurrentRoom.Visited;
			Player.CurrentRoom.Visited = false;
			DisplayRoom(Player.CurrentRoom);
			Player.CurrentRoom.Visited = TempBoolean;
			CommandExecuted = true;
		} // look

		if ( (Verb.equals("examine")) || (Verb.equals("ex")) || (Verb.equals("read")) ) {
			ExamineObject( Remainder );
			CommandExecuted = true;
		} // examine

		if ( (Verb.equals("help")) || (Verb.equals("verblist")) || (Verb.equals("listverbs")) ) {
			DisplayVerbs();
			CommandExecuted = true;
		} // VerbList

		if ( (Verb.equals("quit")) || (Verb.equals("exit")) ) {
			CommandExecuted = true;
			stop();
		}

		Direction = ResolveDirectionName(Verb);

		if ( (Direction != 0) && (Direction != 5) ) { // 5 Means Center. Won't be used until later
			CommandExecuted = true;
			RoomMover(Direction);
		}

		// ----------------
		// Debug Mode Verbs
		// ----------------

		if ( (GameInfo.DebugMode)
		&& ( (Verb.equals("warp")) || (Verb.equals("xyzzy")) )
		&& !(Remainder.equals("")) ) {
			CommandExecuted = true;
			RoomWarp( Remainder );
		} // Warp

		if ( (GameInfo.DebugMode) && (Verb.equals( "execute" ) ) ) {

			ExecuteEffect(Remainder);
			DisplayRoom(Player.CurrentRoom);
			CommandExecuted = true;
		} // Execute

		// ------------------
		// User Defined Verbs
		// ------------------

		if ( !(CommandExecuted) )
			Verb = ResolveVerb(Verb); // If this command line's verb is another alias, we will replace it with the correct one

		if ( Verb.equals("get") ) {
			GetItem( Remainder );
			DisplayRoom( Player.CurrentRoom );
			CommandExecuted = true;
		}

		if ( Verb.equals("drop") ) {
			DropItem( Remainder );
			DisplayRoom( Player.CurrentRoom );
			CommandExecuted = true;
		}

		if ( !(CommandExecuted) )
			for( int VerbIndex = 1; VerbIndex <= VerbArray.length - 1; VerbIndex++ )
				if ( !(Verb.equals("get") ) && !(Verb.equals("drop") ) && ( VerbMatches( Verb, VerbIndex ) ) ) {
					String ReturnedObjects = ParseCommandLineObjects( Remainder );
					if ( !( ReturnedObjects.startsWith( "0" ) ) ) {
						StringTokenizer VerbToken = new StringTokenizer( ReturnedObjects, " |" );
						VerbToken.nextToken(); // points to number of objects returned - which we can ignore
						String Object1 = VerbToken.nextToken().trim();
						String Object2 = null;
						if ( ReturnedObjects.startsWith( "2" ) )
							Object2 = VerbToken.nextToken().trim();
						String EffectString = ResolveEvent( Verb, Object1, Object2 );
						if ( EffectString != null ) {
							ExecuteEffect( EffectString );
							CommandExecuted = true;
							DisplayRoom(Player.CurrentRoom);
						}
						else {
								OutputArea.append("\n\nYou can't do that.");
								CommandExecuted = true;
						}
					}
				}

		if (GameInfo.ShowCommandLine)
			CommandLine.setText(""); // This clears the command line after a permissable command has been entered

		if ( (Verb.equals("last")) || (Verb.equals("repeat")) ) {
			if (GameInfo.ShowCommandLine)
				CommandLine.setText(LastCommand);
			Command = LastCommand;
			CommandExecuted = true;
		}

		if ( !(CommandExecuted) )
			OutputArea.append("\n\nI don't understand your command.");

		LastCommand = Command;

	} // CommandLineParser


	public void DisplayVerbs() {

		// Note: Don't forget to modify this routine if any further verbs are hard-wired into the Engine!

		boolean ShowGet = true;
		boolean ShowDrop = true;

		// We begin by displaying the hard-wired verbs used by the COG Engine
		OutputArea.append("\n\n");
		OutputArea.append("Verbs built into the COG Engine: ");
		OutputArea.append(" Look, Examine, Help, Quit");

		// We don't want to diplay Get and Drop here unless the game author
		//  has not already included them as special verbs
		for( int VerbIndex = 1; VerbIndex <= VerbArray.length - 1; VerbIndex++ ) {
			if ( VerbMatches( "Get", VerbIndex ) );
				ShowGet = false;
			if ( VerbMatches( "Drop", VerbIndex ) );
				ShowDrop = false;
		} // for
		if ( !(ShowGet) && !(ShowDrop) )
			OutputArea.append(", and Last");
		if ( (ShowGet) && !(ShowDrop) )
			OutputArea.append(", Last, and Get");
		if ( (ShowDrop) && !(ShowGet) )
			OutputArea.append(", Last, and Drop");
		if ( (ShowGet) && (ShowDrop) )
			OutputArea.append(", Last, Get, and Drop");
		OutputArea.append(".");

		// If Debug Mode is enabled, we want to show all of the available debugging verbs
		if (GameInfo.DebugMode)
			OutputArea.append("\nAvailable Debugging Verbs: Warp, and Execute.");

		// Finally we display the verbs the game author has decided to add into the Engine
		// (as long as either DebugMode is enabled, or the author has set ShowAllVerbs to true)

		if ( (GameInfo.DebugMode) || (GameInfo.ShowAllVerbs) ){
			OutputArea.append("\nOther verbs available in this game include: ");
			for (int TempCount = 1; TempCount <= VerbArray.length-2; TempCount++)
				OutputArea.append(VerbArray[TempCount].Name + ", ");
			if ( ( VerbArray.length - 2 ) > 1 )
				OutputArea.append("and ");
			OutputArea.append(VerbArray[ VerbArray.length - 1 ].Name + ".");
		}

	} // DisplayVerbs


	public void RoomMover(int Direction) {

		// This method takes in the desired direction that the player would like to move
		// and figures out whether or not they are allowed to move in that direction.
		// If not it prints out the appropriate error message, otherwise it moves them
		// in the desired direction.

		int TempInt;
		String TempStr;
		StringTokenizer RoomToken;
		boolean DisplayedSomething;

		if ( ( Player.CurrentRoom.DirectionArray[Direction] != null)
		&& ( ( Player.CurrentRoom.DirectionArray[Direction].ToWhichRoom > 0 )
		&& ( Player.CurrentRoom.DirectionArray[Direction].ToWhichRoom <= GameInfo.TotalRooms ) ) ) {
		// We first make sure that the directional object exists (meaning that you can move in that
    // direction) and then we check and see if the room to which it points is a legal room number.

			if ( Player.CurrentRoom.DirectionArray[Direction].Obstructions != null ) {

				DisplayedSomething = false; // keeps track of whether or not any "Visible" obstructions are present
				OutputArea.append("\n\nYou can't move ");
				OutputArea.append( DirectionInfoArray[Direction].Name.toLowerCase() );

				RoomToken = new StringTokenizer(Player.CurrentRoom.DirectionArray[Direction].Obstructions, ",");
				TempStr = RoomToken.nextToken().trim();
				TempInt = Integer.parseInt(TempStr);
				if ( ObstructionArray[TempInt].Visible ) {
					DisplayedSomething = true;
					OutputArea.append(" because your path is blocked by a ");
					OutputArea.append( ObstructionArray[TempInt].Name.toLowerCase() );
				} // then (2)

				while ( RoomToken.hasMoreTokens() ) {
					TempStr = RoomToken.nextToken().trim();
					TempInt = Integer.parseInt(TempStr);
					if ( ObstructionArray[TempInt].Visible ) {
						if (DisplayedSomething)
							OutputArea.append(", and a ");
						else {
							DisplayedSomething = true;
							OutputArea.append("\n\nYour path ");
							OutputArea.append( DirectionInfoArray[Direction].Name.toLowerCase() );
							OutputArea.append(" because your path is blocked by a ");
						}
						OutputArea.append( ObstructionArray[TempInt].Name.toLowerCase() );
					}  // then (3)
				} // while

				OutputArea.append(".");

			} // then (2)
			else {
				OutputArea.append("\n\n");
				OutputArea.append("You move ");
				OutputArea.append( DirectionInfoArray[Direction].Name );
				OutputArea.append(".");
				if ( ( Player.CurrentRoom.DirectionArray[Direction].FirstTransitionText != null )
				&& ( !(Player.CurrentRoom.DirectionArray[Direction].HasMovedThisWay) ) )
						OutputArea.append(" " + Player.CurrentRoom.DirectionArray[Direction].FirstTransitionText);
				if ( Player.CurrentRoom.DirectionArray[Direction].TransitionText != null )
					OutputArea.append(" " + Player.CurrentRoom.DirectionArray[Direction].TransitionText);
				Player.CurrentRoom.DirectionArray[Direction].HasMovedThisWay = true;

				// Set Player.CurrentRoom to the new Room
				Player.CurrentRoom = RoomArray[Player.CurrentRoom.DirectionArray[Direction].ToWhichRoom];

			} // else (2)
		} // then (1)
		else {
			OutputArea.append("\n\n");
			OutputArea.append("You can't move ");
			OutputArea.append( DirectionInfoArray[Direction].Name.toLowerCase() );
			OutputArea.append(".");
		} // else (1)

		DisplayRoom(Player.CurrentRoom);

	} // RoomMover


	public void ExamineObject(String ObjectName) {

		String ResolvedObject = ParseObject( " " + ObjectName, "End" ); // We parse from the end in order to allow a preposition
		                                                                // between the word "examine" and the object. The extra
		                                                                // space inserted before it is to get around a ParseObject
		                                                                // issue.
		if ( ResolvedObject != null) {

			if ( ResolvedObject.startsWith( "Item" ) ) {

				int ItemNumber = Integer.parseInt( ResolvedObject.substring( 5, ResolvedObject.indexOf( ")" ) ) ); // ...talk about nesting!
				if ( ItemArray[ItemNumber].Description != null )
					OutputArea.append( "\n\n" + ItemArray[ItemNumber].Description );
				if ( ItemArray[ItemNumber].CloseUp_GraphicURL != null )
					DisplayImage( ItemArray[ItemNumber].CloseUp_GraphicURL, 0, 0 );

			} // Item

			if ( ResolvedObject.startsWith( "Obstruction" ) ) {

				int ObstructionNumber = Integer.parseInt( ResolvedObject.substring( 12, ResolvedObject.indexOf( ")" ) ) ); // ...talk about nesting!
				if ( ( ObstructionArray[ObstructionNumber].Description != null )
				&& (ObstructionArray[ObstructionNumber].Visible) )
					OutputArea.append( "\n\n" + ObstructionArray[ObstructionNumber].Description );
				if ( ( ObstructionArray[ObstructionNumber].CloseUp_GraphicURL != null )
				&& (ObstructionArray[ObstructionNumber].Visible) )
					DisplayImage( ObstructionArray[ObstructionNumber].CloseUp_GraphicURL, 0, 0 );

			} // Obstruction

		}
		else {
			OutputArea.append("\n\nYou don't see anything like that here.");
		}

	} // ExamineObject


	public void GetItem(String ItemName) {

		//   This Action begins by searching to see if you are referring to a legal itemname.
		// The "Name" field of all Items is searched first, followed by the "Aliases" field.
		// In the case that two permissable aliases are found, an error is returned, prompting
		// the Player for more specific input. Next, the Player's Current Room is searched
		// to make sure that the item exists in it. Finally, the "Get" Action's Event Array
		// is searched (if it exists) to see if some Event other than the default should occur.
		// If there is no such exception, the default Event is to add the item to the Player's
		// Inventory, and remove the item from the Current Room.

		int ItemNumber = 0;
		String EffectString;
		boolean OkToPickUp = true;
		StringTokenizer ItemToken;
		boolean GetAll = false;

		if ( ( ItemName.equalsIgnoreCase("All") ) || ( ItemName.equalsIgnoreCase("Everything") ) ) {
			GetAll = true;
			if ( Player.CurrentRoom.Items == null )
				ItemNumber = -2;
			else {
				ItemToken = new StringTokenizer(Player.CurrentRoom.Items, ",");
				while ( ItemToken.hasMoreTokens() ) {
					String ItemWord = ItemToken.nextToken().trim();
					GetItem( ItemArray[ Integer.parseInt(ItemWord) ].Name );
				}
			} // else
		} // all

		if ( ItemNumber != -2 )
			ItemNumber = ResolveItemName( ItemName, "CurrentRoom" );
		if ( ( ItemNumber == 0 ) && !(GetAll) )
			ItemNumber = FindItemAlias( ItemName, "CurrentRoom" );
		if ( ( ItemNumber != 0 ) && ( ItemNumber != -2 ) && !( RoomContainsItem( Player.CurrentRoom.Number, ItemNumber ) ) )
			ItemNumber = 0;

		// We have figured out which Item the Player is talking about (whether they referred to it by name or alias)
		// and now begin to decide what happens next.

		switch( ItemNumber ) {
			case 0 :
				if ( !(GetAll) )
					OutputArea.append("\n\nYou don't see anything like that here."); // we don't want to display this if we are getting all
				break;
			case -1 :
				OutputArea.append("\n\nI'm not sure precisely what you are referring to. Please be more specific.");
				break;
			case -2 :
				OutputArea.append("\n\nThere's nothing to get in this room.");
				break;
			default :
				EffectString = ResolveEvent( "Get", "Item(" + ItemNumber + ")", null );
				if ( EffectString != null )
					// An Event exists for this Item
					ExecuteEffect( EffectString );
				else {
					// No Event exists for this Item, so we execute the default Actions
					if ( ItemArray[ItemNumber].Weight == -1 ) {
						OutputArea.append("\n\nYou can't pick up the " + ItemArray[ItemNumber].Name + ".");
						OkToPickUp = false;
					}
					if ( ( Player.Max_Weight != -1 ) && ( ItemArray[ItemNumber].Weight + Player.Current_Weight > Player.Max_Weight ) ) {
						OutputArea.append("\n\nThe " + ItemArray[ItemNumber].Name + " is too heavy for you to pick up.");
						OkToPickUp = false;
					}
					if ( ( Player.Max_Bulk != -1 ) && ( ItemArray[ItemNumber].Bulk + Player.Current_Bulk > Player.Max_Bulk ) ) {
						OutputArea.append("\n\nThe " + ItemArray[ItemNumber].Name + " is to bulky for you to carry.");
						OkToPickUp = false;
					}
					if ( OkToPickUp ) {
						if ( (GameInfo.DebugMode) && ( Player.Items[ItemNumber] ) )
							System.err.println("Warning! Player's Inventory already includes " + ItemNumber + "!");
						OutputArea.append("\n\nYou pick up the " + ItemArray[ItemNumber].Name + ".");
						RemoveItemFromRoom( Player.CurrentRoom.Number, ItemNumber );
						Player.Items[ItemNumber] = true;
					}
				} // else
				break;
		} // switch

	} // GetItem


	public void DropItem(String ItemName) {

		//   This Action begins by searching to see if you are referring to a legal itemname.
		// The "Name" field of all Items is searched first, followed by the "Aliases" field.
		// In the case that two permissable aliases are found, an error is returned, prompting
		// the player for more specific input. Next, the player's inventory is searched
		// to make sure that the item exists in it. Finally, the "Drop" Action's Event Array
		// is searched (if it exists) to see if some Event other than the default should occur.
		// If there is no such exception, the default Event is to de-equip the item (if it is
		// currently eqipped), and then remove the item from the player's inventory and add it
		//  to the current room.
		//
		// Note: If there is a special event that should be executed when the item is de-equipped
		// it will not be executed if a player attempts to drop an equipped item. Under such
		// a circumstance, a separate "Drop" event should be written.

		int ItemNumber = 0;
		String EffectString;
		boolean DropAll = false;

		if ( ( ItemName.equalsIgnoreCase("All") ) || ( ItemName.equalsIgnoreCase("Everything") ) ) {
			boolean HasDroppedAnything = false;
			DropAll = true;
			for( int InventoryIndex = 1; InventoryIndex <= Player.Items.length - 1; InventoryIndex++ )
				if ( Player.Items[InventoryIndex] ) {
					DropItem( ItemArray[InventoryIndex].Name );
					HasDroppedAnything = true;
				}
			if ( !(HasDroppedAnything) )
				ItemNumber = -2;
		} // drop all

		if ( ItemNumber != -2 )
			ItemNumber = ResolveItemName( ItemName, "Inventory" );
		if ( ( ItemNumber == 0 ) && !(DropAll) ) {
			ItemNumber = FindItemAlias( ItemName, "Inventory" );
			System.err.println("Search for Alias \"" + ItemName + "\" returned " + ItemNumber);
		}
		if ( ( ItemNumber != 0 ) && (ItemNumber != -2) && !( Player.Items[ItemNumber] ) )
			ItemNumber = 0;

		// We have figured out which Item the Player is talking about (whether they referred to it by name or alias)
		// and now begin to decide what happens next.

		switch( ItemNumber ) {
			case 0 :
				if ( !(DropAll) )
					OutputArea.append("\n\nYou don't anything like that here in your inventory."); // we don't want to display this if we are getting all
				break;
			case -1 :
				OutputArea.append("\n\nI'm not sure precisely what you are referring to. Please be more specific.");
				break;
			case -2 :
				OutputArea.append("\n\nYou don't have anything in your inventory to drop!");
				break;
			default :
				EffectString = ResolveEvent( "Drop", "Item(" + ItemNumber + ")", null );
				if ( EffectString != null )
					// An Event exists for this Item
					ExecuteEffect( EffectString );
				else {
					// No Event exists for this Item, so we execute the default Actions
					if (ItemArray[ItemNumber].Equipped) {
						ItemArray[ItemNumber].Equipped = false;
						OutputArea.append("\n\nYou de-equip the " + ItemArray[ItemNumber].Name + ".");
					}
					if ( (GameInfo.DebugMode) && ( RoomContainsItem( Player.CurrentRoom.Number, ItemNumber ) ) )
						System.err.println("Warning! CurrentRoom already includes " + ItemNumber + "!");
					OutputArea.append("\n\nYou drop the " + ItemArray[ItemNumber].Name + ".");
					AddItemToRoom( Player.CurrentRoom.Number, ItemNumber );
					Player.Items[ItemNumber] = false;
				} // else
				break;
		} // switch

	} // DropItem


	public void RoomWarp(String Word) {

		// This method, otherwise known as the "Xyzzy feature" allows the player to jump into
		// any room in the game. CommandLineParser makes sure that Debug Mode is turned
		// on in order for this feature to be used.

		try {
			// Set Player.CurrentRoom to the new Room
			Player.CurrentRoom = RoomArray[ Integer.parseInt(Word) ];
			DisplayRoom(Player.CurrentRoom);
		} catch (Exception BadRoomNumber) {
			OutputArea.append ( "That is not a valid room number!\n" );
		}
	} // RoomWarp


	public void ExecuteEffect( String Effect ) {

		// ExecuteEffect works as a recursive method that executes an event's effect field.
		// The first effect found is executed, and if an "and" is found instead of a semicolon
		// at the end of that effect (indicating that another effect is supposed to take place)
		// the method recursively calls itself, feeding the new instance the remainder of the
		// current event's effect string. Damn I'm good.

		String Word;
		String Remainder = "";
		StringTokenizer EffectToken;
		int RoomNumber;
		int DirectionNumber;
		int ItemNumber;
		int ObstructionNumber;
		int TempIndex;

		if (GameInfo.DebugMode)
			System.err.println("Executing : \"" + Effect + "\"");

		EffectToken = new StringTokenizer(Effect, " "); // Sidenote: default tokenizer is by whitespace and tabs
		Word = EffectToken.nextToken().trim();

		if ( Word.equals("Adds") ) {
			Word = EffectToken.nextToken().trim();
			if ( Word.startsWith("Item") ) {
				// We're adding an Item
				ItemNumber = Integer.parseInt( Word.substring( 5, Word.length() - 1 ) );
				Word = EffectToken.nextToken().trim();
				if ( !( Word.equals("Inventory") ) && !( Word.equals("CurrentRoom") ) && !( Word.startsWith("Room") ) )
					Word = EffectToken.nextToken().trim();
				if ( Word.equals("Inventory") ) {
					if ( ( GameInfo.DebugMode ) && ( Player.Items[ItemNumber] ) )
						System.err.println("Warning! Player already has Item #" + ItemNumber + " in their inventory!");
					Player.Items[ItemNumber] = true;
				} // Inventory
				if ( Word.equals("CurrentRoom") )
					AddItemToRoom( Player.CurrentRoom.Number, ItemNumber );
				if ( Word.startsWith("Room") ) {
					RoomNumber = Integer.parseInt( Word.substring( 5, Word.length() -1 ) );
					AddItemToRoom( RoomNumber, ItemNumber );
				} // Room
			} // Item
			else {
				// We're adding an Obstruction
				ObstructionNumber = Integer.parseInt( Word.substring( 12, Word.length() -1 ) );
				Word = EffectToken.nextToken().trim();
				if ( !( Word.startsWith( "Room(" ) ) )
					Word = EffectToken.nextToken().trim();
				TempIndex = Word.indexOf( ")" );
				RoomNumber = Integer.parseInt( Word.substring( 5, TempIndex ) );
				TempIndex = Word.lastIndexOf( "(" );
				DirectionNumber = Integer.parseInt( Word.substring( TempIndex + 1, Word.length() - 1 ) );
				AddObstructionToRoom( ObstructionNumber, RoomNumber, DirectionNumber );
			} // Obstruction
		} // Adds

		if ( Word.equals("Removes") ) {
			Word = EffectToken.nextToken().trim();
			if ( Word.startsWith("Item") ) {
				// We're adding an Item
				ItemNumber = Integer.parseInt( Word.substring( 5, Word.length() - 1 ) );
				Word = EffectToken.nextToken().trim();
				if ( !( Word.equals("Inventory") ) && !( Word.equals("CurrentRoom") ) && !( Word.startsWith("Room") ) )
					Word = EffectToken.nextToken().trim();
				if ( Word.equals("Inventory") ) {
					if ( ( GameInfo.DebugMode ) && ( !( Player.Items[ItemNumber] ) ) )
						System.err.println("Warning! Player did not have Item #" + ItemNumber + " in their inventory!");
					Player.Items[ItemNumber] = false;
				} // Inventory
				if ( Word.equals("CurrentRoom") )
					RemoveItemFromRoom( Player.CurrentRoom.Number, ItemNumber );
				if ( Word.startsWith("Room") ) {
					RoomNumber = Integer.parseInt( Word.substring( 5, Word.length() -1 ) );
					RemoveItemFromRoom( RoomNumber, ItemNumber );
				} // Room
			} // Item
			else {
				// We're adding an Obstruction
				ObstructionNumber = Integer.parseInt( Word.substring( 12, Word.length() -1 ) );
				Word = EffectToken.nextToken().trim();
				if ( !( Word.startsWith( "Room(" ) ) )
					Word = EffectToken.nextToken().trim();
				TempIndex = Word.indexOf( ")" );
				RoomNumber = Integer.parseInt( Word.substring( 5, TempIndex ) );
				TempIndex = Word.lastIndexOf( "(" );
				DirectionNumber = Integer.parseInt( Word.substring( TempIndex + 1, Word.length() - 1 ) );
				RemoveObstructionFromRoom( ObstructionNumber, RoomNumber, DirectionNumber );
			} // Obstruction
		} // Removes

		if ( Word.equals("Modifies") ) {

			String TempString = "";
			String TempWord = "";
			StringTokenizer TempToken;

			Word = EffectToken.nextToken().trim();
			if ( Word.equals( "Player" ) ) {
				Word = EffectToken.nextToken().trim();
				TempToken = new StringTokenizer( Word, "[]" );
				TempToken.nextToken(); // now points to everything before open bracket
				TempWord = TempToken.nextToken().trim(); // We now know which expression to use
				TempString = Word.substring( Word.lastIndexOf( "(" ) + 1, Word.length() - 1 );
					if ( Word.startsWith( "PlayerPoints" ) )
						Player.Points = EvaluateExpression( TempWord, Player.Points, Integer.parseInt( TempString ) );
					if ( Word.startsWith( "PlayerExp" ) )
						Player.Exp = EvaluateExpression( TempWord, Player.Exp, Integer.parseInt( TempString ) );
					if ( Word.startsWith( "PlayerHP" ) )
						Player.HP = EvaluateExpression( TempWord, Player.HP, Integer.parseInt( TempString ) );
					if ( Word.startsWith( "MP" ) )
						Player.MP = EvaluateExpression( TempWord, Player.MP, Integer.parseInt( TempString ) );
					if ( Word.startsWith( "PlayerStr" ) )
						Player.Str = EvaluateExpression( TempWord, Player.Str, Integer.parseInt( TempString ) );
					if ( Word.startsWith( "PlayerIQ" ) )
						Player.IQ = EvaluateExpression( TempWord, Player.IQ, Integer.parseInt( TempString ) );
					if ( Word.startsWith( "PlayerDex" ) )
						Player.Dex = EvaluateExpression( TempWord, Player.Dex, Integer.parseInt( TempString ) );
					if ( Word.startsWith( "PlayerAgil" ) )
						Player.Agil = EvaluateExpression( TempWord, Player.Agil, Integer.parseInt( TempString ) );
					if ( Word.startsWith( "PlayerCharisma" ) )
						Player.Charisma = EvaluateExpression( TempWord, Player.Charisma, Integer.parseInt( TempString ) );
					if ( Word.startsWith( "PlayerArmorLevel" ) )
						Player.Armor_Level = EvaluateExpression( TempWord, Player.Armor_Level, Integer.parseInt( TempString ) );
					if ( Word.startsWith( "PlayerCurrentWeight" ) )
						Player.Current_Weight = EvaluateExpression( TempWord, Player.Current_Weight, Integer.parseInt( TempString ) );
			} // Player

			if ( Word.startsWith( "Room" ) ) {
				TempString = Word.substring( 5, Word.length() - 1 );
				RoomNumber = Integer.parseInt( TempString );
				Word = EffectToken.nextToken().trim();

				if ( Word.startsWith( "TextDescription(Long)" ) ) {
					TempToken = new StringTokenizer( Word, "[]" );
					TempToken.nextToken(); // now points to everything before open bracket
					TempWord = TempToken.nextToken();
					while ( ( EffectToken.hasMoreTokens() ) && !( TempWord.endsWith("]") ) )
						TempWord += " " + EffectToken.nextToken().trim();
					if ( TempWord.endsWith( "]" ) )
						TempWord = TempWord.substring( 0, TempWord.length() - 1 ); // Remove the closing bracket
					if ( TempWord.equals("null") )
						TempWord = null;
					RoomArray[RoomNumber].Description_Long = TempWord;
				}

				if ( Word.startsWith( "TextDescription(Short)" ) ) {
					TempToken = new StringTokenizer( Word, "[]" );
					TempToken.nextToken(); // now points to everything before open bracket
					TempWord = TempToken.nextToken();
					while ( ( EffectToken.hasMoreTokens() ) && !( TempWord.endsWith("]") ) )
						TempWord += " " + EffectToken.nextToken().trim();
					if ( TempWord.endsWith( "]" ) )
						TempWord = TempWord.substring( 0, TempWord.length() - 1 ); // Remove the closing bracket
					if ( TempWord.equals("null") )
						TempWord = null;
					RoomArray[RoomNumber].Description_Short = TempWord;
				}

				if ( Word.startsWith( "DirectionDescription" ) ) {
					TempToken = new StringTokenizer( Word, "[]" );
					TempToken.nextToken(); // now points to everything before open bracket
					TempWord = TempToken.nextToken();
					while ( ( EffectToken.hasMoreTokens() ) && !( TempWord.endsWith("]") ) )
						TempWord += " " + EffectToken.nextToken().trim();
					if ( TempWord.endsWith( "]" ) )
						TempWord = TempWord.substring( 0, TempWord.length() - 1 ); // Remove the closing bracket
					if ( TempWord.equals("null") )
						TempWord = null;
					RoomArray[RoomNumber].Direction_Description = TempWord;
				}

				if ( Word.startsWith( "GraphicURL" ) ) {
					TempToken = new StringTokenizer( Word, "[]" );
					TempToken.nextToken(); // now points to everything before open bracket
					TempWord = TempToken.nextToken();
					while ( ( EffectToken.hasMoreTokens() ) && !( TempWord.endsWith("]") ) )
						TempWord += " " + EffectToken.nextToken().trim();
					if ( TempWord.endsWith( "]" ) )
						TempWord = TempWord.substring( 0, TempWord.length() - 1 ); // Remove the closing bracket
					if ( TempWord.equals("null") )
						TempWord = null;
					if (GameInfo.DebugMode)
						System.err.println("Setting GraphicURL for Room #" + RoomNumber + " to \"" + TempWord + "\"");
					RoomArray[RoomNumber].GraphicURL = TempWord;
				}

				if ( Word.startsWith( "Visited" ) )
					RoomArray[RoomNumber].Visited = ( ( Word.endsWith( "(true)" ) ) || ( Word.endsWith( "(1)" ) ) );

				if ( Word.startsWith( "DirectionObject" ) ) {
					DirectionNumber = Integer.parseInt( Word.substring( Word.indexOf( "(" ) + 1, Word.indexOf( ")" ) ) );
					if ( RoomArray[RoomNumber].DirectionArray[DirectionNumber] == null )
						RoomArray[RoomNumber].DirectionArray[DirectionNumber] = new DirectionOBJ();
					TempString = Word.substring( Word.indexOf( ")" ) + 1, Word.length() );

					if ( TempString.startsWith( "ToWhichRoom" ) ) {
						TempWord = ( TempString.substring( TempString.indexOf( "(" ) + 1, TempString.indexOf( ")" ) ) );
						RoomArray[RoomNumber].DirectionArray[DirectionNumber].ToWhichRoom = Integer.parseInt( TempWord );
					}

					if ( TempString.startsWith( "FirstTransitionText" ) ) {
						TempToken = new StringTokenizer( Word, "[]" );
						TempToken.nextToken(); // now points to everything before open bracket
						TempWord = TempToken.nextToken();
						while ( ( EffectToken.hasMoreTokens() ) && !( TempWord.endsWith("]") ) )
							TempWord += " " + EffectToken.nextToken().trim();
						if ( TempWord.endsWith( "]" ) )
							TempWord = TempWord.substring( 0, TempWord.length() - 1 ); // Remove the closing bracket
						if ( TempWord.equals("null") )
							TempWord = null;
						RoomArray[RoomNumber].DirectionArray[DirectionNumber].FirstTransitionText = TempWord;
					}

					if ( TempString.startsWith( "TransitionText" ) ) {
						TempToken = new StringTokenizer( Word, "[]" );
						TempToken.nextToken(); // now points to everything before open bracket
						TempWord = TempToken.nextToken();
						while ( ( EffectToken.hasMoreTokens() ) && !( TempWord.endsWith("]") ) )
							TempWord += " " + EffectToken.nextToken().trim();
						if ( TempWord.endsWith( "]" ) )
							TempWord = TempWord.substring( 0, TempWord.length() - 1 ); // Remove the closing bracket
						if ( TempWord.equals("null") )
							TempWord = null;
						RoomArray[RoomNumber].DirectionArray[DirectionNumber].TransitionText = TempWord;
					}

					if ( TempString.startsWith( "FirstTransitionGraphic" ) ) {
						TempToken = new StringTokenizer( Word, "[]" );
						TempToken.nextToken(); // now points to everything before open bracket
						TempWord = TempToken.nextToken();
						while ( ( EffectToken.hasMoreTokens() ) && !( TempWord.endsWith("]") ) )
							TempWord += " " + EffectToken.nextToken().trim();
						if ( TempWord.endsWith( "]" ) )
							TempWord = TempWord.substring( 0, TempWord.length() - 1 ); // Remove the closing bracket
						if ( TempWord.equals("null") )
							TempWord = null;
						RoomArray[RoomNumber].DirectionArray[DirectionNumber].FirstTransitionText = TempWord;
					}

					if ( TempString.startsWith( "FirstTransitionGraphic" ) ) {
						TempToken = new StringTokenizer( Word, "[]" );
						TempToken.nextToken(); // now points to everything before open bracket
						TempWord = TempToken.nextToken();
						while ( ( EffectToken.hasMoreTokens() ) && !( TempWord.endsWith("]") ) )
							TempWord += " " + EffectToken.nextToken().trim();
						if ( TempWord.endsWith( "]" ) )
							TempWord = TempWord.substring( 0, TempWord.length() - 1 ); // Remove the closing bracket
						if ( TempWord.equals("null") )
							TempWord = null;
						RoomArray[RoomNumber].DirectionArray[DirectionNumber].FirstTransitionText = TempWord;
					}

					if ( TempString.startsWith( "HasMovedThisWay" ) )
						RoomArray[RoomNumber].DirectionArray[DirectionNumber].HasMovedThisWay =
							( ( Word.endsWith( "(true)" ) ) || ( Word.endsWith( "(1)" ) ) );

					CheckEmptyDirection( RoomNumber, DirectionNumber );

				} // DirectionObject

				// Set Player.CurrentRoom to the new Room
				Player.CurrentRoom = RoomArray[Player.CurrentRoom.Number];

			} // Room

			if ( Word.startsWith( "Item" ) ) {
				TempString = Word.substring( 5, Word.length() - 1 );
				ItemNumber = Integer.parseInt( TempString );
				Word = EffectToken.nextToken().trim();

				if ( Word.startsWith( "Equipped" ) )
					ItemArray[ItemNumber].Equipped = ( ( Word.endsWith( "(true)" ) ) || ( Word.endsWith( "(1)" ) ) );

				if ( Word.startsWith( "Weight" ) ) {
					TempWord = ( Word.substring( Word.indexOf( "(" ) + 1, Word.indexOf( ")" ) ) );
					ItemArray[ItemNumber].Weight = Integer.parseInt( TempWord );
				}

				if ( Word.startsWith( "Bulk" ) ) {
					TempWord = ( Word.substring( Word.indexOf( "(" ) + 1, Word.indexOf( ")" ) ) );
					ItemArray[ItemNumber].Bulk = Integer.parseInt( TempWord );
				}

				if ( Word.startsWith( "TextDescription" ) ) {
					TempToken = new StringTokenizer( Word, "[]" );
					TempToken.nextToken(); // now points to everything before open bracket
					TempWord = TempToken.nextToken();
					while ( ( EffectToken.hasMoreTokens() ) && !( TempWord.endsWith("]") ) )
						TempWord += " " + EffectToken.nextToken().trim();
					if ( TempWord.endsWith( "]" ) )
						TempWord = TempWord.substring( 0, TempWord.length() - 1 ); // Remove the closing bracket
					if ( TempWord.equals("null") )
						TempWord = null;
					ItemArray[ItemNumber].Description = TempWord;
				}

				if ( Word.startsWith( "Environment_GraphicURL" ) ) {
					TempToken = new StringTokenizer( Word, "[]" );
					TempToken.nextToken(); // now points to everything before open bracket
					TempWord = TempToken.nextToken();
					while ( ( EffectToken.hasMoreTokens() ) && !( TempWord.endsWith("]") ) )
						TempWord += " " + EffectToken.nextToken().trim();
					if ( TempWord.endsWith( "]" ) )
						TempWord = TempWord.substring( 0, TempWord.length() - 1 ); // Remove the closing bracket
					if ( TempWord.equals("null") )
						TempWord = null;
					ItemArray[ItemNumber].Environment_GraphicURL = TempWord;
				}

				if ( Word.startsWith( "Environment_GraphicPos" ) ) {
					// int Environment_Graphic_Xpos, Environment_Graphic_Ypos;
					TempString = ( Word.substring( Word.indexOf( "(" ) + 1, Word.indexOf( ")" ) ) );
					TempToken = new StringTokenizer( TempString, "," );
					TempWord = TempToken.nextToken().trim();
					ItemArray[ItemNumber].Environment_Graphic_Xpos = Integer.parseInt( TempWord );
					TempWord = TempToken.nextToken().trim();
					ItemArray[ItemNumber].Environment_Graphic_Ypos = Integer.parseInt( TempWord );
				}

				if ( Word.startsWith( "CloseUp_GraphicURL" ) ) {
					TempToken = new StringTokenizer( Word, "[]" );
					TempToken.nextToken(); // now points to everything before open bracket
					TempWord = TempToken.nextToken();
					while ( ( EffectToken.hasMoreTokens() ) && !( TempWord.endsWith("]") ) )
						TempWord += " " + EffectToken.nextToken().trim();
					if ( TempWord.endsWith( "]" ) )
						TempWord = TempWord.substring( 0, TempWord.length() - 1 ); // Remove the closing bracket
					if ( TempWord.equals("null") )
						TempWord = null;
					ItemArray[ItemNumber].CloseUp_GraphicURL = TempWord;
				}

				if ( Word.startsWith( "Icon_GraphicURL" ) ) {
					TempToken = new StringTokenizer( Word, "[]" );
					TempToken.nextToken(); // now points to everything before open bracket
					TempWord = TempToken.nextToken();
					while ( ( EffectToken.hasMoreTokens() ) && !( TempWord.endsWith("]") ) )
						TempWord += " " + EffectToken.nextToken().trim();
					if ( TempWord.endsWith( "]" ) )
						TempWord = TempWord.substring( 0, TempWord.length() - 1 ); // Remove the closing bracket
					if ( TempWord.equals("null") )
						TempWord = null;
					ItemArray[ItemNumber].Icon_GraphicURL = TempWord;
				}

				if ( Word.startsWith( "Equipped_GraphicURL" ) ) {
					TempToken = new StringTokenizer( Word, "[]" );
					TempToken.nextToken(); // now points to everything before open bracket
					TempWord = TempToken.nextToken();
					while ( ( EffectToken.hasMoreTokens() ) && !( TempWord.endsWith("]") ) )
						TempWord += " " + EffectToken.nextToken().trim();
					if ( TempWord.endsWith( "]" ) )
						TempWord = TempWord.substring( 0, TempWord.length() - 1 ); // Remove the closing bracket
					if ( TempWord.equals("null") )
						TempWord = null;
					ItemArray[ItemNumber].Equipped_GraphicURL = TempWord;
				}

			} // Item

			if ( Word.startsWith( "Obstruction" ) ) {
				TempString = Word.substring( 5, Word.length() - 1 );
				ObstructionNumber = Integer.parseInt( TempString );
				Word = EffectToken.nextToken().trim();

				if ( Word.startsWith( "Visible" ) )
					ObstructionArray[ObstructionNumber].Visible = ( ( Word.endsWith( "(true)" ) ) || ( Word.endsWith( "(1)" ) ) );

				if ( Word.startsWith( "TextDescription" ) ) {
					TempToken = new StringTokenizer( Word, "[]" );
					TempToken.nextToken(); // now points to everything before open bracket
					TempWord = TempToken.nextToken();
					while ( ( EffectToken.hasMoreTokens() ) && !( TempWord.endsWith("]") ) )
						TempWord += " " + EffectToken.nextToken().trim();
					if ( TempWord.endsWith( "]" ) )
						TempWord = TempWord.substring( 0, TempWord.length() - 1 ); // Remove the closing bracket
					if ( TempWord.equals("null") )
						TempWord = null;
					ObstructionArray[ObstructionNumber].Description = TempWord;
				}

				if ( Word.startsWith( "Environment_GraphicURL" ) ) {
					TempToken = new StringTokenizer( Word, "[]" );
					TempToken.nextToken(); // now points to everything before open bracket
					TempWord = TempToken.nextToken();
					while ( ( EffectToken.hasMoreTokens() ) && !( TempWord.endsWith("]") ) )
						TempWord += " " + EffectToken.nextToken().trim();
					if ( TempWord.endsWith( "]" ) )
						TempWord = TempWord.substring( 0, TempWord.length() - 1 ); // Remove the closing bracket
					if ( TempWord.equals("null") )
						TempWord = null;
					ObstructionArray[ObstructionNumber].Environment_GraphicURL = TempWord;
				}

				if ( Word.startsWith( "Environment_GraphicPos" ) ) {
					// int Environment_Graphic_Xpos, Environment_Graphic_Ypos;
					TempString = ( Word.substring( Word.indexOf( "(" ) + 1, Word.indexOf( ")" ) ) );
					TempToken = new StringTokenizer( TempString, "," );
					TempWord = TempToken.nextToken().trim();
					ObstructionArray[ObstructionNumber].Environment_Graphic_Xpos = Integer.parseInt( TempWord );
					TempWord = TempToken.nextToken().trim();
					ObstructionArray[ObstructionNumber].Environment_Graphic_Ypos = Integer.parseInt( TempWord );
				}

				if ( Word.startsWith( "CloseUp_GraphicURL" ) ) {
					TempToken = new StringTokenizer( Word, "[]" );
					TempToken.nextToken(); // now points to everything before open bracket
					TempWord = TempToken.nextToken();
					while ( ( EffectToken.hasMoreTokens() ) && !( TempWord.endsWith("]") ) )
						TempWord += " " + EffectToken.nextToken().trim();
					if ( TempWord.endsWith( "]" ) )
						TempWord = TempWord.substring( 0, TempWord.length() - 1 ); // Remove the closing bracket
					if ( TempWord.equals("null") )
						TempWord = null;
					ObstructionArray[ObstructionNumber].CloseUp_GraphicURL = TempWord;
				}

			} // Obstruction

		} // Modifies

		if ( Word.startsWith("TextMessage[") ) {
			OutputArea.append("\n\n");
			if ( Word.endsWith("]") ) {
				Word = Word.substring( 12, Word.length() - 1 ); // Here's our easy-out
				OutputArea.append( Word );
			}
			else {
				Word = Word.substring(12, Word.length() );
				OutputArea.append( Word );
				Word = EffectToken.nextToken().trim();
				while ( !( Word.endsWith("]") ) ) {
					OutputArea.append(" " + Word);
					Word = EffectToken.nextToken().trim();
				}
				Word = Word.substring( 0, Word.length() - 1 );
				OutputArea.append( " " + Word );
			} // else
		} // "TextMessage" Effect

		if ( Word.startsWith("GraphicMessage[") ) {

			try {
				CurrentURL = new URL( getCodeBase() + GameInfo.Image_Directory + Word.substring( 15, Word.length() - 2 ) ); // the 2 removes the comma
			} catch (Exception BadURL) {
				System.err.println("GraphicMessageURL is Malformed!\n");
			}
			Word = EffectToken.nextToken().trim();
			int x = Integer.parseInt( Word.substring( 0, Word.length() - 1 ) );
			Word = EffectToken.nextToken().trim();
			int y = Integer.parseInt( Word.substring( 0, Word.length() - 1 ) );
			GraphicArea.addImageLayer(this, CurrentURL, x, y);

		} // "GraphicMessage" Effect

		// This next sequence makes the recursive call to ExecuteEffect if there are more Effects for this Event
		if ( EffectToken.hasMoreTokens() ) {
			Word = EffectToken.nextToken().trim();
			if ( Word.equalsIgnoreCase("and") ) {
				while ( EffectToken.hasMoreTokens() ) {
					Word = EffectToken.nextToken().trim();
					Remainder += ( Word + " ") ;
				}
				ExecuteEffect( Remainder );
			}
		} // if

	} // ExecuteEffect


	public boolean RequirementsMet( String Requirements ) {

		// Another wicked recursive method
		// The order of logical operations should be (in decreasing precedence) : NOT, AND, OR
		// I'm not really sure whether or not the OR is handled correctly, but NOT and AND should be cool
		// This method follows the EBNF grammar followed by the Events Text file.

		String Word;
		String Remainder = "";
		StringTokenizer RequirementToken;
		boolean AllGood = false;
		boolean ContainsNot = false;
		int TempInt, TempIndex;
		StringTokenizer TempToken;
		String TempString;
		String TempWord;

		if ( Requirements == null )
			AllGood = true;
		else {
			if ( GameInfo.DebugMode )
				System.err.println( "I am checking the following: " + Requirements );
			RequirementToken = new StringTokenizer( Requirements, " " );
			RequirementToken.nextToken(); // now points to "(Requires"
			Word = RequirementToken.nextToken().trim();
			if ( ( Word.equalsIgnoreCase( "(Not)" ) ) || ( Word.equals( "!" ) ) ) {
				ContainsNot = true;
				Word = RequirementToken.nextToken().trim();
			} // check for "not"

			if ( Word.startsWith( "Player" ) ) {
				TempToken = new StringTokenizer( Word, "[]" );
				TempToken.nextToken(); // now points to everything before open bracket
				TempWord = TempToken.nextToken().trim(); // We now know which comparison to make
				TempString = Word.substring( Word.lastIndexOf( "(" ) + 1, Word.length() - 2 );
				if ( Word.startsWith( "PlayerPoints" ) )
					AllGood = MakeComparison( TempWord, Player.Points, Integer.parseInt(TempString) );
				if ( Word.startsWith( "PlayerExp" ) )
					AllGood = MakeComparison( TempWord, Player.Exp, Integer.parseInt(TempString) );
				if ( Word.startsWith( "PlayerHP" ) )
					AllGood = MakeComparison( TempWord, Player.HP, Integer.parseInt(TempString) );
				if ( Word.startsWith( "PlayerMP" ) )
					AllGood = MakeComparison( TempWord, Player.MP, Integer.parseInt(TempString) );
				if ( Word.startsWith( "PlayerStr" ) )
					AllGood = MakeComparison( TempWord, Player.Str, Integer.parseInt(TempString) );
				if ( Word.startsWith( "PlayerIQ" ) )
					AllGood = MakeComparison( TempWord, Player.IQ, Integer.parseInt(TempString) );
				if ( Word.startsWith( "PlayerDex" ) )
					AllGood = MakeComparison( TempWord, Player.Dex, Integer.parseInt(TempString) );
				if ( Word.startsWith( "PlayerAgil" ) )
					AllGood = MakeComparison( TempWord, Player.Agil, Integer.parseInt(TempString) );
				if ( Word.startsWith( "PlayerCharisma" ) )
					AllGood = MakeComparison( TempWord, Player.Charisma, Integer.parseInt(TempString) );
				if ( Word.startsWith( "PlayerArmorLevel" ) )
					AllGood = MakeComparison( TempWord, Player.Armor_Level, Integer.parseInt(TempString) );
				if ( Word.startsWith( "PlayerCurrentWeight" ) )
					AllGood = MakeComparison( TempWord, Player.Current_Weight, Integer.parseInt(TempString) );
			} // Player

			if ( Word.startsWith( "Room" ) ) {
				TempIndex = Word.indexOf( ")" );
				TempInt = Integer.parseInt( Word.substring( 5, TempIndex ) );
				if ( Word.endsWith( "IsCurrentRoom)" ) )
					AllGood = ( Player.CurrentRoom.Number == TempInt );
				if ( Word.endsWith( "HasVisited)" ) )
					AllGood = ( RoomArray[TempInt].Visited );
			} // Room

			if ( Word.startsWith( "Item" ) ) {
				TempIndex = Word.indexOf( ")" );
				TempInt = Integer.parseInt( Word.substring( 5, TempIndex ) ); // this is the Item to which we are referring

				if ( Word.endsWith( "InInventory)" ) )
					AllGood = ( Player.Items[TempInt] );

				if ( Word.endsWith( "IsEquipped)" ) )
					AllGood = ( ItemArray[TempInt].Equipped );

				if ( Word.regionMatches( TempIndex + 1, "ExistsInRoom", 0, 12 ) ) {
					TempString = Word.substring( Word.lastIndexOf( "(" ) + 1 , Word.length() - 2 ); // TempString now points to the Room Number
					AllGood = RoomContainsItem( Integer.parseInt( TempString ), TempInt );
				}

				if ( Word.regionMatches( TempIndex + 1, "Weight", 0, 6 ) ) {
					// This one was pretty tricky
					TempToken = new StringTokenizer( Word, "[]" );
					TempToken.nextToken(); // now points to everything before open bracket
					TempWord = TempToken.nextToken().trim(); // We now know which comparison to make
					TempString = Word.substring( Word.lastIndexOf( "(" ) + 1, Word.length() - 2 );
					AllGood = MakeComparison( TempWord, ItemArray[TempInt].Weight, Integer.parseInt(TempString) );
				}

				if ( Word.regionMatches( TempIndex + 1, "Bulk", 0, 4 ) ) {
					// This one was pretty tricky
					TempToken = new StringTokenizer( Word, "[]" );
					TempToken.nextToken(); // now points to everything before open bracket
					TempWord = TempToken.nextToken().trim(); // We now know which comparison to make
					TempString = Word.substring( Word.lastIndexOf( "(" ) + 1, Word.length() - 2 );
					AllGood = MakeComparison( TempWord, ItemArray[TempInt].Bulk, Integer.parseInt(TempString) );
				}

			} //  Item

			if ( Word.startsWith( "Obstruction" ) ) {
				TempIndex = Word.indexOf( ")" );
				TempInt = Integer.parseInt( Word.substring( 12, TempIndex ) ); // this is the Obstrucion to which we are referring

				if ( Word.endsWith( "IsVisible" ) )
					AllGood = ObstructionArray[TempInt].Visible;

				if ( Word.regionMatches( TempIndex + 1, "ExistsInRoom", 0, 12 ) ) {

					int RoomNumber;
					int DirectionNumber;
					String ObstructionWord;
					StringTokenizer ObstructionToken;

					TempToken = new StringTokenizer( Word, "()" );
					TempToken.nextToken(); // now points to "Obstruction"
					TempToken.nextToken(); // now points to <Ref> (1)
					TempToken.nextToken(); // now points to "ExistsInRoom"
					TempWord = TempToken.nextToken().trim(); // Room<Ref> (2)
					RoomNumber = Integer.parseInt( TempWord );
					if ( TempToken.hasMoreTokens() ) {
						// We are referring to a specific direction
						TempToken.nextToken(); // now points to "Direction"
						DirectionNumber = Integer.parseInt( TempToken.nextToken().trim() );
						if ( ( RoomArray[ RoomNumber ].DirectionArray[ DirectionNumber ] ) != null )
							if ( ( RoomArray[ RoomNumber ].DirectionArray[ DirectionNumber ].Obstructions ) != null ) {
								ObstructionToken = new StringTokenizer( RoomArray[ RoomNumber ].DirectionArray[ DirectionNumber ].Obstructions, "," );
								while ( ObstructionToken.hasMoreTokens() ) {
									ObstructionWord = ObstructionToken.nextToken().trim();
									if ( Integer.parseInt( ObstructionWord ) == TempInt )
										AllGood = true;
								} // while
							} // then
					}
					else
						// We are referring to any direction
						AllGood = RoomContainsObstruction( RoomNumber, TempInt);

				} // ExistsInRoom
			} // Obstruction

			if ( RequirementToken.hasMoreTokens() ) {
				Word = RequirementToken.nextToken().trim();
				if ( Word.equalsIgnoreCase( "AND" ) ) {
					while ( RequirementToken.hasMoreTokens() ) {
						Word = RequirementToken.nextToken().trim();
						Remainder += ( Word + " " );
					}
					if ( ContainsNot )
						AllGood = !(AllGood);
					AllGood = ( AllGood && RequirementsMet( Remainder ) );
				} // AND
				else
					if ( Word.equalsIgnoreCase( "OR" ) ) {
						while ( RequirementToken.hasMoreTokens() ) {
							Word = RequirementToken.nextToken().trim();
							Remainder += ( Word + " " );
						}
						if ( ContainsNot )
							AllGood = !(AllGood);
						AllGood = ( AllGood || RequirementsMet( Remainder ) );
					} // OR
			} // if
			else
				if ( ContainsNot )
					AllGood = !(AllGood);
		} //else

		return(AllGood);

	} // RequirementsMet


	public void AddItemToRoom( int RoomNumber, int ItemNumber ) {

		String NewItemList = "";
		String Item;
		StringTokenizer ItemToken;
		boolean ItemAlreadyPresent = false;

		if ( RoomArray[RoomNumber].Items == null )
			NewItemList += ItemNumber; // If there was nothing in the room before, then this will be easy.
		else {
			NewItemList = RoomArray[RoomNumber].Items;
			ItemToken = new StringTokenizer(RoomArray[RoomNumber].Items, ",");
			// Let's check to see if the items is already present in the room
			while ( ItemToken.hasMoreTokens() ) {
				Item = ItemToken.nextToken().trim();
				if ( Integer.parseInt(Item) == ItemNumber ) {
					System.err.println("Warning! Room # " + RoomNumber + " already contains Item #" + ItemNumber + "!");
					ItemAlreadyPresent = true;
				}
			} //while
			if ( !(ItemAlreadyPresent) )
				NewItemList += ", " + ItemNumber;
		} // else

		RoomArray[RoomNumber].Items = NewItemList;

	} // AddItemToRoom


	public void RemoveItemFromRoom( int RoomNumber, int ItemNumber ) {

		String NewItemList = "";
		String Item;
		StringTokenizer ItemToken;
		boolean WrittenSomething = false;

		ItemToken = new StringTokenizer(RoomArray[RoomNumber].Items, ",");
		Item = ItemToken.nextToken().trim();
		if ( Integer.parseInt(Item) != ItemNumber ) {
			NewItemList += Integer.parseInt(Item);
			WrittenSomething = true;
		} // then
		while ( ItemToken.hasMoreTokens() ) {
			Item = ItemToken.nextToken().trim();
			if ( Integer.parseInt(Item) != ItemNumber ) {
				if (WrittenSomething) // watch this really slick code! (C:
					NewItemList += ", ";
				NewItemList += Integer.parseInt(Item);
				WrittenSomething = true;
			} // then (2)
		} // while
		if ( NewItemList.equals("") )
			NewItemList = null;
		RoomArray[RoomNumber].Items = NewItemList;

	} // RemoveItemFromRoom


	public void AddObstructionToRoom( int ObstructionNumber, int RoomNumber, int DirectionNumber ) {

		String NewObstructionList = "";
		String Obstruction;
		StringTokenizer ObstructionToken;
		boolean ObstructionAlreadyPresent = false;

		if ( RoomArray[RoomNumber].DirectionArray[DirectionNumber] == null )
			RoomArray[RoomNumber].DirectionArray[DirectionNumber] = new DirectionOBJ(); // Create Direction Object if it doesn't already exist
		if ( RoomArray[RoomNumber].DirectionArray[DirectionNumber].Obstructions == null )
			NewObstructionList += ObstructionNumber; // If there were no previous obstructions, life is simple.
		else {
			NewObstructionList += RoomArray[RoomNumber].DirectionArray[DirectionNumber].Obstructions;
			ObstructionToken = new StringTokenizer(RoomArray[RoomNumber].DirectionArray[DirectionNumber].Obstructions, ",");
			// We better check to make sure that the obstruction isn't already present.
			while ( ObstructionToken.hasMoreTokens() ) {
				Obstruction = ObstructionToken.nextToken().trim();
				if ( Integer.parseInt(Obstruction) == ObstructionNumber ) {
					System.err.print("Warning! Room # " + RoomNumber);
					System.err.print(", Direction [" + DirectionInfoArray[DirectionNumber].Name);
					System.err.println("] already contains Obstruction # " + ObstructionNumber);
					ObstructionAlreadyPresent = true;
				}
			} // while
			if ( !(ObstructionAlreadyPresent) )
				NewObstructionList += ", " + ObstructionNumber;
		} // else

		RoomArray[RoomNumber].DirectionArray[DirectionNumber].Obstructions = NewObstructionList;

	} // AddObstructionToRoom


	public void RemoveObstructionFromRoom( int ObstructionNumber, int RoomNumber, int DirectionNumber ) {

		String NewObstructionList = "";
		String Obstruction;
		StringTokenizer ObstructionToken;
		boolean WrittenSomething = false;

		if ( (RoomArray[RoomNumber].DirectionArray[DirectionNumber] == null)
		|| (RoomArray[RoomNumber].DirectionArray[DirectionNumber].Obstructions == null) ) {
			if (GameInfo.DebugMode)
				System.err.println("Warning! Error in Room #" + RoomNumber + ": No Direction Object or Obstruction String Exists! (RemoveObstructionFromRoom)");
		}
		else {
			ObstructionToken = new StringTokenizer(RoomArray[RoomNumber].DirectionArray[DirectionNumber].Obstructions, ",");
			Obstruction = ObstructionToken.nextToken().trim();
			if ( Integer.parseInt(Obstruction) != ObstructionNumber ) {
				NewObstructionList += Integer.parseInt(Obstruction);
				WrittenSomething = true;
			} // then
			while ( ObstructionToken.hasMoreTokens() ) {
				Obstruction = ObstructionToken.nextToken().trim();
				if ( Integer.parseInt(Obstruction) != ObstructionNumber ) {
					if (WrittenSomething)
						NewObstructionList += ", ";
					NewObstructionList += Integer.parseInt(Obstruction);
					WrittenSomething = true;
				} // then (2)
			} // while
			if ( NewObstructionList.equals("") )
				NewObstructionList = null;
			RoomArray[RoomNumber].DirectionArray[DirectionNumber].Obstructions = NewObstructionList;
			CheckEmptyDirection(RoomNumber, DirectionNumber);
		} // else

	} // RemoveObstructionFromRoom


	public boolean RoomContainsItem( int RoomNumber, int ItemNumber ) {

		boolean ItemExistsInRoom = false;
		String Word;
		StringTokenizer ItemToken;

		if ( RoomArray[RoomNumber].Items != null ) {
			ItemToken = new StringTokenizer( RoomArray[RoomNumber].Items, "," );
			while ( ItemToken.hasMoreTokens() ) {
				Word = ItemToken.nextToken().trim();
				if ( Integer.parseInt( Word ) == ItemNumber )
					ItemExistsInRoom = true;
			} // while
		} // then

		return(ItemExistsInRoom);

	} // RoomContainsItem


	public boolean RoomContainsObstruction( int RoomNumber, int ObstructionNumber ) {

		boolean ObstructionExistsInRoom = false;
		int DirectionNumber;
		String ObstructionWord;
		StringTokenizer ObstructionToken;

		for ( DirectionNumber = 1; DirectionNumber <= DirectionInfoArray.length -1; DirectionNumber++ )
			if ( ( RoomArray[ RoomNumber ].DirectionArray[ DirectionNumber ] ) != null )
				if ( ( RoomArray[ RoomNumber ].DirectionArray[ DirectionNumber ].Obstructions ) != null ) {
					ObstructionToken = new StringTokenizer( RoomArray[ RoomNumber ].DirectionArray[ DirectionNumber ].Obstructions, "," );
					while ( ObstructionToken.hasMoreTokens() ) {
						ObstructionWord = ObstructionToken.nextToken().trim();
						if ( Integer.parseInt( ObstructionWord ) == ObstructionNumber )
							ObstructionExistsInRoom = true;
					} // while
				} // then

		return(ObstructionExistsInRoom);

	} // RoomContainsObstruction


	public int ResolveDirectionName( String DirectionName ) {

	boolean FoundDirection = false;
	int DirectionNumber = 0;

	for ( int dirCounter = 1; dirCounter <= DirectionInfoArray.length - 1; dirCounter++ )
		if ( ( DirectionName.equalsIgnoreCase( DirectionInfoArray[dirCounter].Name ) )
		|| ( DirectionName.equalsIgnoreCase( DirectionInfoArray[dirCounter].Abbreviation ) ) )
			if ( !(FoundDirection) ) {
				FoundDirection = true;
				DirectionNumber = dirCounter;
			}

		return(DirectionNumber);

	} //ResolveDirectionName


	public boolean VerbMatches( String VerbName, int VerbIndex ) {

		boolean FoundVerb = false;
		String Alias;
		StringTokenizer AliasToken;

		if ( VerbName.equalsIgnoreCase( VerbArray[VerbIndex].Name ) )
			FoundVerb = true;
		else
			if ( VerbArray[VerbIndex].Aliases != null ) {
				AliasToken = new StringTokenizer( VerbArray[VerbIndex].Aliases, "," );
				while ( AliasToken.hasMoreTokens() ) {
					Alias = AliasToken.nextToken().trim().toLowerCase();
					if ( !(FoundVerb) )
						FoundVerb = ( VerbName.equals( Alias ) );
				} // while
			}

		return(FoundVerb);

	} // VerbMatches


	public String ResolveVerb( String VerbAlias ) {

		String VerbName = VerbAlias;
		boolean FoundVerb = false;

		for( int VerbIndex = 1; VerbIndex <= VerbArray.length - 1; VerbIndex++ )
			if ( VerbMatches( VerbAlias, VerbIndex ) )
				if ( !(FoundVerb) )
					VerbName = VerbArray[VerbIndex].Name;
				else {
					if (GameInfo.DebugMode)
						System.err.println("Warning! Multiple Matching Verb Aliases Detected!");
					VerbName = VerbAlias;
				}

		VerbName = VerbName.toLowerCase();

		return(VerbName);

	} // ResolveVerb


	public String ParseCommandLineObjects( String Remainder ) {

		String Object1;
		String Object2 = null;
		String ParsedObjects = null;
		int ObjectNumber;

		Object1 = ParseObject( Remainder + " ", "Beginning" );
		if ( Object1 != null ) {
			if (GameInfo.DebugMode)
				System.err.println("Object1 = \"" + Object1 + "\"");

			int TempIndex = Object1.indexOf( "[" );

			TempIndex = Integer.parseInt( Object1.substring( TempIndex + 1, Object1.length() - 1 ) );
			Remainder = Remainder.substring( TempIndex, Remainder.length() );

			Object2 = ParseObject( Remainder, "End" );
		}

		if ( Object2 != null ) {
			Object1 = Object1.substring( 0, Object1.indexOf( "[" ) );
			Object2 = Object2.substring( 0, Object2.indexOf( "[" ) );
			if (GameInfo.DebugMode)
				System.err.println("Object2 = \"" + Object2 + "\"");
			ParsedObjects = "2 | " + Object1 + " | " + Object2 + " | ";
		}
		else
			if (Object1 != null ) {
				Object1 = Object1.substring( 0, Object1.indexOf( "[" ) );
				ParsedObjects = "1 | " + Object1 + " | ";
			}
			else
				ParsedObjects = "0";

		if (GameInfo.DebugMode)
			System.err.println("ParsedObjects = \"" + ParsedObjects + "\"");

		return ( ParsedObjects );

	} // ParseComandLineObjects


	public String ParseObject( String Phrase, String SearchFrom ) {

		String ObjectString = null;
		String Scratch;
		int StringIndex = Phrase.length();
		int ObjectNumber;
		boolean ObjectFound = false;

		// look at whole string
		// check if whole string matches an obstruction's name (in the current room)
		// check if whole string matches an item's name (either in current room or player's inventory)
		// if nothing is found, removed the last word from the string and begin again
		// spit back the results, first the object's number, then the length of the name used

		if ( !( ( SearchFrom.equalsIgnoreCase( "Beginning" ) ) || ( SearchFrom.equalsIgnoreCase( "Start" ) ) ) )
			StringIndex = 0;

		Scratch = Phrase;

		if (GameInfo.DebugMode)
			System.err.println("Searching \"" + Scratch + "\"");

		while( ( Scratch != null ) && !(ObjectFound) ) {
			if ( ( SearchFrom.equalsIgnoreCase( "Beginning" ) ) || ( SearchFrom.equalsIgnoreCase( "Start" ) ) ) {
				StringIndex = Scratch.lastIndexOf( " ", StringIndex );
				if ( StringIndex == -1 )
					Scratch = null;
				else
					Scratch = Scratch.substring( 0, StringIndex );
			}
			else {
				StringIndex = Scratch.indexOf( " ", StringIndex );
				if ( StringIndex == -1 )
					Scratch = null;
				else
					Scratch = Scratch.substring( StringIndex + 1, Scratch.length() );
			}
			if (GameInfo.DebugMode)
				System.err.println("Current Scratch: \"" + Scratch + "\"");
			if ( ( Scratch ==  null ) || ( Scratch.equals("") ) )
				Scratch = null; // We didn't find any usable names
			else {
				// let's look for obstruction matches first, since we don't have to worry about the inventory
				ObjectNumber = ResolveObstructionName( Scratch, "CurrentRoom" );
				if ( ObjectNumber == 0 )
					ObjectNumber = FindObstructionAlias( Scratch, "CurrentRoom" );
				if ( ( ObjectNumber > 0 ) && !( RoomContainsObstruction( Player.CurrentRoom.Number, ObjectNumber ) ) ) {
					ObjectNumber = 0; // we found the name, but the obstruction is not in the current room.
				}
				else
					if ( ObjectNumber > 0 ) {
						ObjectFound = true;
						ObjectString = "Obstruction(" + ObjectNumber + ")";
						ObjectString += "[" + Scratch.length() + "]"; // we need this to see how much of the
						                                              // command line we can skip over
					}


				// At this point, we should know if an obstruction name matching the current Scratch string has been found.
				// If nothing matching has been found, we move on to searching for a matching item name.

				if ( ObjectNumber == 0 )
					ObjectNumber = ResolveItemName( Scratch, "Inventory" );
				if ( ObjectNumber == 0 )
					ObjectNumber = ResolveItemName( Scratch, "CurrentRoom" );
				if ( ObjectNumber == 0 )
					ObjectNumber = FindItemAlias( Scratch, "Inventory" );
				if ( ObjectNumber == 0 )
					ObjectNumber = FindItemAlias( Scratch, "CurrentRoom" );

				if ( ( !(ObjectFound) )
				&& ( ObjectNumber > 0 )
				&& ( !( RoomContainsItem( Player.CurrentRoom.Number, ObjectNumber) ) )
				&& ( !( Player.Items[ObjectNumber] ) ) )
					ObjectNumber = 0;
				else
					if ( ( ObjectNumber > 0 ) && ( !(ObjectFound) ) ) {
						ObjectFound = true;
						ObjectString = "Item(" + ObjectNumber + ")";
						ObjectString += "[" + Scratch.length() + "]"; // we need this to see how much of the
						                                              // command line we can skip over
					}


				if ( ObjectNumber == -1 ) {
					// If we've found more than one valid alias, we want to print out an error and stop parsing the phrase
					OutputArea.append("\n\nI'm not sure precisely what you are referring to. Please be more specific.");
					ObjectString = null;
					Scratch = null;
				}

			if ( ( ObjectString != null ) && ( ObjectString.equals( "Item(0)" ) || ObjectString.equals( "Obstruction(0) " ) ) ) {
				System.err.println("ObjectString: " + ObjectString);
				ObjectFound = false;
			}

			} // else
		} // while

	return(ObjectString);

	} // ParseFirstObject


	public int ResolveItemName(String ItemName, String WhereToLook) {

		int ItemNumber = 0;
		boolean FoundItem = false;

		for( int ItemCounter = 1; ItemCounter <= ItemArray.length - 1; ItemCounter++ )
			if ( ItemName.equalsIgnoreCase(ItemArray[ItemCounter].Name) ) {

				// We've found a matching name for the item
				// Now we must check to see if the location is correct

				if ( WhereToLook.equalsIgnoreCase( "CurrentRoom" ) && RoomContainsItem( Player.CurrentRoom.Number, ItemCounter ) ) {
					if (GameInfo.DebugMode)
						System.err.println("Item \"" + ItemArray[ItemCounter].Name + "\" found.");
					if ( (GameInfo.DebugMode) && (FoundItem) )
						System.err.println("Item #" + ItemCounter + " and Item # " + ItemNumber + " have duplicate names!");
					else {
						FoundItem = true;
						ItemNumber = ItemCounter;
					}
				} // CurrentRoom

				if ( WhereToLook.equalsIgnoreCase( "Inventory" ) && ( Player.Items[ItemCounter] ) ) {
					if (GameInfo.DebugMode)
						System.err.println("Item \"" + ItemArray[ItemCounter].Name + "\" found.");
					if ( (GameInfo.DebugMode) && (FoundItem) )
						System.err.println("Item #" + ItemCounter + " and Item # " + ItemNumber + " have duplicate names!");
					else {
						FoundItem = true;
						ItemNumber = ItemCounter;
					}
				} // CurrentRoom

				if ( WhereToLook.equalsIgnoreCase( "ItemArray" ) && RoomContainsItem( Player.CurrentRoom.Number, ItemCounter ) ) {
					if (GameInfo.DebugMode)
						System.err.println("Item \"" + ItemArray[ItemCounter].Name + "\" found.");
					if ( (GameInfo.DebugMode) && (FoundItem) )
						System.err.println("Item #" + ItemCounter + " and Item # " + ItemNumber + " have duplicate names!");
					else {
						FoundItem = true;
						ItemNumber = ItemCounter;
					}
				}

			} // if

		return(ItemNumber);

	} // ResolveItemName


	public int ResolveObstructionName(String ObstructionName, String WhereToLook ) {

		int ObstructionNumber = 0;
		boolean FoundObstruction = false;

		for( int ObstructionCounter = 1; ObstructionCounter <= ObstructionArray.length - 1; ObstructionCounter++ )
			if ( ObstructionName.equalsIgnoreCase(ObstructionArray[ObstructionCounter].Name) ) {

				// We've found a matching name for the obstruction
				// Now we must check to see if the location is correct

				if ( WhereToLook.equalsIgnoreCase( "CurrentRoom" ) && RoomContainsObstruction( Player.CurrentRoom.Number, ObstructionCounter ) ) {
					if (GameInfo.DebugMode)
						System.err.println("Obstruction \"" + ObstructionArray[ObstructionCounter].Name + "\" found.");
					if ( (GameInfo.DebugMode) && (FoundObstruction) )
						System.err.println("Obstruction #" + ObstructionCounter + " and Obstruction # " + ObstructionNumber + " have duplicate names!");
					else {
						FoundObstruction = true;
						ObstructionNumber = ObstructionCounter;
					}
				} // CurrentRoom

				if ( WhereToLook.equalsIgnoreCase( "ObstructionArray" ) && RoomContainsObstruction( Player.CurrentRoom.Number, ObstructionCounter ) ) {
					if (GameInfo.DebugMode)
						System.err.println("Obstruction \"" + ObstructionArray[ObstructionCounter].Name + "\" found.");
					if ( (GameInfo.DebugMode) && (FoundObstruction) )
						System.err.println("Obstruction #" + ObstructionCounter + " and Obstruction # " + ObstructionNumber + " have duplicate names!");
					else {
						FoundObstruction = true;
						ObstructionNumber = ObstructionCounter;
					}
				}

			} // if

		return(ObstructionNumber);

	} // ResolveObstrucionName


	public int FindItemAlias (String ItemName, String WhereToLook) {

		// WhereToLook designated whether or not to check only items that exist in the CurrentRoom
		// returns 0 if Item Name does not match an Alias
		// returns -1 if Item Name matches multiple Aliases
		// returns Item Number of legitimate Item

		int ItemNumber = 0;
		boolean FoundItem = false;
		String Alias;
		StringTokenizer AliasToken;

		if (GameInfo.DebugMode)
			System.err.println("Seaching " + WhereToLook + " for Item with Alias \"" + ItemName + "\"");

		for (int ItemCounter = 1; ItemCounter <= ItemArray.length - 1; ItemCounter++ )
			if (ItemArray[ItemCounter].Aliases != null ) {
				AliasToken = new StringTokenizer(ItemArray[ItemCounter].Aliases, ",");
				while ( AliasToken.hasMoreTokens() ) {
					Alias = AliasToken.nextToken().trim();
					if ( Alias.equalsIgnoreCase(ItemName) ) {

						// We've found a matching Alias for the current item
						// Now we must check to see if the location is correct

							if ( !(FoundItem) && RoomContainsItem( Player.CurrentRoom.Number, ItemCounter ) ) {
								if (GameInfo.DebugMode)
									System.err.println("Item \"" + ItemArray[ItemCounter].Name + "\" found.");
								FoundItem = true;
								ItemNumber = ItemCounter;
							}
							else
								if ( RoomContainsItem( Player.CurrentRoom.Number, ItemCounter ) ) {
									// More than one items in the CurrentRoom have the same Alias
									if (GameInfo.DebugMode)
										System.err.println("More than one items in the CurrentRoom have this Alias!");
									ItemNumber = -1;
								}
						// End CurrentRoom Search

						if ( WhereToLook.equalsIgnoreCase( "Inventory" ) ) // Only look at items that exist in the player's inventory
							if ( !(FoundItem) && Player.Items[ItemCounter] ) {
								if (GameInfo.DebugMode)
									System.err.println("Item \"" + ItemArray[ItemCounter].Name + "\" found.");
								FoundItem = true;
								ItemNumber = ItemCounter;
							}
							else
								if ( Player.Items[ItemCounter] ) {
									// More than one item in the player's inventory have this Alias
									if (GameInfo.DebugMode)
										System.err.println("More than one item in the player's inventor have this Alias!");
									ItemNumber = -1;
								}
						// End Inventory Search

						if ( WhereToLook.equalsIgnoreCase( "ItemArray" ) ) // We want to look at all of the Items in ItemArray
							if ( !(FoundItem) ) {
								if (GameInfo.DebugMode)
									System.err.println("Item \"" + ItemArray[ItemCounter].Name + "\" found.");
								FoundItem = true;
								ItemNumber = ItemCounter;
							}
							else {
								// More than one items in the ItemArray have this Alias
								if (GameInfo.DebugMode)
									System.err.println("More than one items in the ItemArray have this Alias!");
								ItemNumber = -1;
							}
						// End ItemArray Search
					}
				} // while
			} // if

	return(ItemNumber);

	} // FindItemAlias


	public int FindObstructionAlias (String ObstructionName, String WhereToLook) {

		// WhereToLook designated whether or not to check only obstruction that exist in the CurrentRoom
		// returns 0 if Obstruction Name does not match an Alias
		// returns -1 if Obstruction Name matches multiple Aliases

		int ObstructionNumber = 0;
		boolean FoundObstruction = false;
		String Alias;
		StringTokenizer AliasToken;

		if (GameInfo.DebugMode)
			System.err.println("Seaching " + WhereToLook + " for Obstruction with Alias \"" + ObstructionName + "\"");

		for (int ObstructionCounter = 1; ObstructionCounter <= ObstructionArray.length - 1; ObstructionCounter++ )
			if (ObstructionArray[ObstructionCounter].Aliases != null ) {
				AliasToken = new StringTokenizer(ObstructionArray[ObstructionCounter].Aliases, ",");
				while ( AliasToken.hasMoreTokens() ) {
					Alias = AliasToken.nextToken().trim();
					if ( Alias.equalsIgnoreCase(ObstructionName) ) {

						// We've found a matching Alias for the current obstruction
						// Now we must check to see if the location is correct

						if ( WhereToLook.equalsIgnoreCase( "CurrentRoom" ) ) // Only look at obstruction that exist in the current room
							if ( !(FoundObstruction) && RoomContainsObstruction( Player.CurrentRoom.Number, ObstructionCounter ) ) {
								if (GameInfo.DebugMode)
									System.err.println("Obstruction \"" + ObstructionArray[ObstructionCounter].Name + "\" found.");
								FoundObstruction = true;
								ObstructionNumber = ObstructionCounter;
							}
							else
								if ( RoomContainsObstruction( Player.CurrentRoom.Number, ObstructionCounter ) ) {
									// More than one obstructions in the CurrentRoom have the same Alias
									if (GameInfo.DebugMode)
										System.err.println("More than one obstructions in the CurrentRoom have this Alias!");
									ObstructionNumber = -1;
								}
						// End CurrentRoom Search

						if ( WhereToLook.equalsIgnoreCase( "ObstructionArray" ) ) // We want to look at all of the Obstructions in ObstructionArray
							if ( !(FoundObstruction) ) {
								if (GameInfo.DebugMode)
									System.err.println("Obstruction \"" + ObstructionArray[ObstructionCounter].Name + "\" found.");
								FoundObstruction = true;
								ObstructionNumber = ObstructionCounter;
							}
							else {
								// More than one obstructions in the ObstructionArray have this Alias
								if (GameInfo.DebugMode)
									System.err.println("More than one obstructions in the ItemArray have this Alias!");
								ObstructionNumber = -1;
							}
					}
				} // while
			} // if

		return(ObstructionNumber);

	} // FindObstructionAlias


	public String ResolveEvent( String Action, String Object, String Object2 ) {

		// This method searches through all of the possible event strings and picks which
		// one we want to use. It is possible that we can always just assume that which ever event
		// appears first in the cog script, that one will take presedence.

		boolean EventFound = false;
		String EffectString = null;

		// Verb aliases have already been converted into the correct verb

 		for( int VerbIndex = 1; VerbIndex <= VerbArray.length - 1; VerbIndex++ )
 			if( (VerbArray[VerbIndex] != null) && (VerbArray[VerbIndex].Name.equalsIgnoreCase( Action ) ) )
 				for( int EventIndex = 1; EventIndex <= VerbArray[VerbIndex].Events.length - 1; EventIndex++ )

					if ( ( !( EventFound ) )
					&& ( VerbArray[VerbIndex].Events[EventIndex] != null )

					&& ( ( ( ( VerbArray[VerbIndex].Events[EventIndex].Object == null )
						|| ( VerbArray[VerbIndex].Events[EventIndex].Object.equalsIgnoreCase( Object ) ) )
					&& ( ( VerbArray[VerbIndex].Events[EventIndex].Object2 == null )
						|| ( VerbArray[VerbIndex].Events[EventIndex].Object2.equalsIgnoreCase( Object2 ) ) ) )

					|| ( ( ( VerbArray[VerbIndex].Events[EventIndex].Object2 == null )
						|| ( VerbArray[VerbIndex].Events[EventIndex].Object2.equalsIgnoreCase( Object ) ) )
					&& ( ( VerbArray[VerbIndex].Events[EventIndex].Object == null )
						|| ( VerbArray[VerbIndex].Events[EventIndex].Object.equalsIgnoreCase( Object2 ) ) ) ) )

					&& ( RequirementsMet ( VerbArray[VerbIndex].Events[EventIndex].Requirements ) ) ) {
						EventFound = true;
						EffectString = VerbArray[VerbIndex].Events[EventIndex].EffectString;
					}


		return(EffectString);

	} // ResolveEvent


	public void CheckEmptyDirection( int RoomNumber, int DirectionNumber ) {
		// This method checks to see if a Direction Object should be set to null
		if ( (RoomArray[RoomNumber].DirectionArray[DirectionNumber].ToWhichRoom == 0)
		&& (RoomArray[RoomNumber].DirectionArray[DirectionNumber].Obstructions == null)
		&& (RoomArray[RoomNumber].DirectionArray[DirectionNumber].HasMovedThisWay == false)
		&& (RoomArray[RoomNumber].DirectionArray[DirectionNumber].FirstTransitionText == null)
		&& (RoomArray[RoomNumber].DirectionArray[DirectionNumber].TransitionText == null)
		&& (RoomArray[RoomNumber].DirectionArray[DirectionNumber].FirstTransitionGraphic == null)
		&& (RoomArray[RoomNumber].DirectionArray[DirectionNumber].TransitionGraphic == null) )
			RoomArray[RoomNumber].DirectionArray[DirectionNumber] = null;
	} // CheckEmptyDirection


	public boolean MakeComparison( String Comparison, int val1, int val2 ) {

		boolean result = false;

		if ( Comparison.equals( "==" ) )
			result = ( val1 == val2 );
		if ( Comparison.equals( "!=" ) )
			result = ( val1 != val2 );
		if ( Comparison.equals( ">" ) )
			result = ( val1 > val2 );
		if ( Comparison.equals( "<" ) )
			result = ( val1 < val2 );
		if ( Comparison.equals( ">=" ) )
			result = ( val1 >= val2 );
		if ( Comparison.equals( "<=" ) )
			result = ( val1 <= val2 );
		return(result);
	} // MakeComparison


	public int EvaluateExpression( String Expression, int val1, int val2 ) {

		if ( Expression.equals( "=" ) )
			val1 = val2;
		if ( Expression.equals( "+" ) )
			val1 += val2;
		if ( Expression.equals( "-" ) )
			val1 -= val2;
		return( val1 );
	} //EvaluateExpression


	public boolean StartsWithVowel(String InputString) {
		InputString = InputString.toLowerCase();
		if ( (InputString.startsWith("a")) || (InputString.startsWith("e"))
		|| (InputString.startsWith("i")) || (InputString.startsWith("o"))
		|| (InputString.startsWith("u")) )
				return(true);
			else
				return(false);
	} // StartsWithVowel


	public void InitializeGUI() {
		/** Panel Reference
		 (0,0) (1,0) (2,0)
		 (0,1) (1,1) (2,1)
		 (0,2) (1,2) (2,2)
		*/

		// Panel Settings
		// --------------

		constraints.fill = GridBagConstraints.BOTH;

		// Setup for Top Panel
		// (includes Graphic Area and Menu Panel)
		constraints.weightx = 1.0;
		constraints.weighty = 0.0;
		addGB( this, Top = new Panel(), 0,0);

		// Setup for Bottom Panel
		// (includes Control Panel and Text Display Output Area
		constraints.weightx = 1.0;
		constraints.weighty = 1.0;
		addGB( this, Bottom = new Panel(), 0, 1);

		// Setup for Menu Panel
		if ( (GameInfo.ShowStats) || (GameInfo.ShowInventory) ) { // (only necessary if either is going to be used)
			constraints.weightx = 1.0;
			constraints.weighty = 0.0;
			addGB( Top, Menu = new Panel(), 0, 0);
		}

		// Setup for Control Panel
		constraints.weightx = 0.0;
		constraints.weighty = 1.0;
		addGB( Bottom, Control = new Panel(), 0, 0);

		// Setup for Navigation Panel
		// (inclues Compass Area)
		if (GameInfo.ShowCompass) {
			constraints.fill = GridBagConstraints.NONE;
			constraints.weightx = 0.0;
			constraints.weighty = 1.0;
			addGB ( Control, Compass = new Panel(), 0, 1);
		}

		// Component Settings
		// ------------------

		// Setup for the GraphicArea (Canvas)
		constraints.anchor = GridBagConstraints.CENTER;
		constraints.fill = GridBagConstraints.NONE;
		constraints.weightx = 0.0;
		constraints.weighty = 0.0;

		try {
			CurrentURL = new URL(getCodeBase() + GameInfo.Image_Directory + GameInfo.ImageLoading_GraphicURL);
		} catch (Exception BadURL) {
			System.err.println("Graphic URL \"");
			System.err.println( GameInfo.ImageLoading_GraphicURL );
			System.err.println("\" is Malformed!\n");
		}
		addGB( Top, GraphicArea = new GraphicPanel(this, CurrentURL, GameInfo.DebugMode), 1, 0);
		//GraphicArea.setSize(GameInfo.PreferredGraphicSizeX, GameInfo.PreferredGraphicSizeY);
		//GraphicArea.validate();


		// The follow section was removed due to an error experienced under Internet Explorer
		//
		//addGB( Top, EditorArea = new TextArea("InfoArea",1,1,TextArea.SCROLLBARS_VERTICAL_ONLY), 0, 0 );
		//EditorArea.setEditable(false);
		//EditorArea.setText("Insert Graphics Here");


		// Setup for the Statistical Text Area
		if (GameInfo.ShowStats) {
			constraints.anchor = GridBagConstraints.CENTER;
			constraints.fill = GridBagConstraints.BOTH;
			constraints.weightx = 1.0;
			constraints.weighty = 1.0;
			addGB( Menu, InfoArea = new TextArea("InfoArea",1,1,TextArea.SCROLLBARS_NONE), 0, 0 );
			InfoArea.setEditable(false);
			InfoArea.setText("");
		}

		// Setup for The Inventory Text Area
		if (GameInfo.ShowInventory) {
			constraints.anchor = GridBagConstraints.CENTER;
			constraints.fill = GridBagConstraints.BOTH;
			constraints.weightx = 1.0;
			constraints.weighty = 1.0;
			addGB( Menu, InventoryArea = new TextArea("InventoryArea",1,1,TextArea.SCROLLBARS_VERTICAL_ONLY), 0, 1);
			InventoryArea.setEditable(false);
			InventoryArea.setText("");
		}

		// Setup for the Text Display Area
		constraints.anchor = GridBagConstraints.CENTER;
		constraints.fill = GridBagConstraints.BOTH;
		constraints.weightx = 1.0;
		constraints.weighty = 1.0;
		addGB( Bottom, OutputArea = new TextArea("OutputArea",1,1,TextArea.SCROLLBARS_VERTICAL_ONLY), 1, 0 );
		OutputArea.setEditable(false);
		OutputArea.setText("");

		// Setup for the Command Line
		if (GameInfo.ShowCommandLine) {
			constraints.anchor = GridBagConstraints.CENTER;
			constraints.fill = GridBagConstraints.HORIZONTAL;
			constraints.weightx = 1.0;
			constraints.weighty = 0.0;
			addGB( Control, CommandLine = new TextField(), 0, 0 );
			CommandLine.addActionListener ( this );
			CommandLine.requestFocus();
		}

		/** Panel Reference
		 (0,0) (1,0) (2,0) (3,0)
		 (0,1) (1,1) (2,1) (3,1)
		 (0,2) (1,2) (2,2) (3,2)
		*/

		// Setup for the Compass

		if (GameInfo.ShowCompass) {
			constraints.anchor = GridBagConstraints.CENTER;
			constraints.fill = GridBagConstraints.BOTH;
			constraints.weightx = 1.0;
			constraints.weighty = 1.0;

			if (GameInfo.MenuButton_GraphicURL != null) {
				try {
					CurrentURL = new URL( getCodeBase() + GameInfo.Image_Directory + GameInfo.MenuButton_GraphicURL );
				} catch (Exception e) { System.err.println(" Uhm... no."); };
				addGB( Compass, CompassMenuGraphic = new GraphicButton( this, CurrentURL ), 0, 0);
				CompassMenuGraphic.setActionCommand( "Help" );
				CompassMenuGraphic.addActionListener( this );
			} else {
				addGB( Compass, CompassMenuText = new Button( "Help" ), 0, 0);
				CompassMenuText.addActionListener ( this );
			}

			if (GameInfo.LoadAllCompassImages) {
				// Loading all of the compass button graphics during game
				// initialization will help to speed up gameplay later
				MediaTracker tracker;
				Image TempImage;

				if (GameInfo.DebugMode)
					System.err.print("Downloading Compass Button Graphic Images...");

				for (int TempCounter = 1; TempCounter <= GameInfo.TotalDirections; TempCounter++) {
					try {
						CurrentURL = new URL( getCodeBase() + GameInfo.Image_Directory + DirectionInfoArray[TempCounter].CG_AvailableURL );
						TempImage = getImage(CurrentURL);
						tracker = new MediaTracker(this);
						tracker.addImage( TempImage, 0);
						tracker.waitForID( 0 );

						CurrentURL = new URL( getCodeBase() + GameInfo.Image_Directory + DirectionInfoArray[TempCounter].CG_UnavailableURL );
						TempImage = getImage(CurrentURL);
						tracker = new MediaTracker(this);
						tracker.addImage( TempImage, 0);
						tracker.waitForID( 0 );

						CurrentURL = new URL( getCodeBase() + GameInfo.Image_Directory + DirectionInfoArray[TempCounter].CG_SpecialURL );
						TempImage = getImage(CurrentURL);
						tracker = new MediaTracker(this);
						tracker.addImage( TempImage, 0);
						tracker.waitForID( 0 );
					}
					catch (Exception e) {
						System.err.println("Error Downloading Compass Button Graphic!");
						System.err.println("Exception was:\n" + e);
					}
				}
				System.err.println("Done.");
				TempImage = null;
				tracker = null;
			} // LoadAllCompassImages


			if (GameInfo.TotalDirections >= 3) {

				// NorthWest
				try {
					CurrentURL = new URL( getCodeBase() + GameInfo.Image_Directory + DirectionInfoArray[1].CG_AvailableURL );
				} catch (Exception e) { System.err.println(" Uhm... no."); };
				addGB( Compass, NW = new GraphicButton( this, CurrentURL ), 1, 0);
				NW.setActionCommand( DirectionInfoArray[1].Name );
				NW.addActionListener( this );

				// North
				try {
					CurrentURL = new URL( getCodeBase() + GameInfo.Image_Directory + DirectionInfoArray[2].CG_AvailableURL );
				} catch (Exception e) { System.err.println(" Uhm... no."); };
				addGB( Compass, N = new GraphicButton( this, CurrentURL ), 2, 0);
				N.setActionCommand( DirectionInfoArray[2].Name );
				N.addActionListener( this );

				// NorthEast
				try {
					CurrentURL = new URL( getCodeBase() + GameInfo.Image_Directory + DirectionInfoArray[3].CG_AvailableURL );
				} catch (Exception e) { System.err.println(" Uhm... no."); };
				addGB( Compass, NE = new GraphicButton( this, CurrentURL ), 3, 0);
				NE.setActionCommand( DirectionInfoArray[3].Name );
				NE.addActionListener( this );

			}

			if (GameInfo.TotalDirections >= 9) {

				// West
				try {
					CurrentURL = new URL( getCodeBase() + GameInfo.Image_Directory + DirectionInfoArray[4].CG_AvailableURL );
				} catch (Exception e) { System.err.println(" Uhm... no."); };
				addGB( Compass, W = new GraphicButton( this, CurrentURL ), 1, 1);
				W.setActionCommand( DirectionInfoArray[4].Name );
				W.addActionListener( this );

				// Center
				try {
					CurrentURL = new URL( getCodeBase() + GameInfo.Image_Directory + DirectionInfoArray[5].CG_AvailableURL );
				} catch (Exception e) { System.err.println(" Uhm... no."); };
				addGB( Compass, C = new GraphicButton( this, CurrentURL ), 2, 1);
				C.setActionCommand( DirectionInfoArray[5].Name );
				C.addActionListener( this );

				// East
				try {
					CurrentURL = new URL( getCodeBase() + GameInfo.Image_Directory + DirectionInfoArray[6].CG_AvailableURL );
				} catch (Exception e) { System.err.println(" Uhm... no."); };
				addGB( Compass, E = new GraphicButton( this, CurrentURL ), 3, 1);
				E.setActionCommand( DirectionInfoArray[6].Name );
				E.addActionListener( this );

				// SouthWest
				try {
					CurrentURL = new URL( getCodeBase() + GameInfo.Image_Directory + DirectionInfoArray[7].CG_AvailableURL );
				} catch (Exception e) { System.err.println(" Uhm... no."); };
				addGB( Compass, SW = new GraphicButton( this, CurrentURL ), 1, 2);
				SW.setActionCommand( DirectionInfoArray[7].Name );
				SW.addActionListener( this );

				// South
				try {
					CurrentURL = new URL( getCodeBase() + GameInfo.Image_Directory + DirectionInfoArray[8].CG_AvailableURL );
				} catch (Exception e) { System.err.println(" Uhm... no."); };
				addGB( Compass, S = new GraphicButton( this, CurrentURL ), 2, 2);
				S.setActionCommand( DirectionInfoArray[8].Name );
				S.addActionListener( this );

				// SouthEast
				try {
					CurrentURL = new URL( getCodeBase() + GameInfo.Image_Directory + DirectionInfoArray[9].CG_AvailableURL );
				} catch (Exception e) { System.err.println(" Uhm... no."); };
				addGB( Compass, SE = new GraphicButton( this, CurrentURL ), 3, 2);
				SE.setActionCommand( DirectionInfoArray[9].Name );
				SE.addActionListener( this );

			}

			if (GameInfo.TotalDirections >= 11) {

				// Up
				try {
					CurrentURL = new URL( getCodeBase() + GameInfo.Image_Directory + DirectionInfoArray[10].CG_AvailableURL );
				} catch (Exception e) { System.err.println(" Uhm... no."); };
				addGB( Compass, U = new GraphicButton( this, CurrentURL ), 0, 1);
				U.setActionCommand( DirectionInfoArray[10].Name );
				U.addActionListener( this );

				// Down
				try {
					CurrentURL = new URL( getCodeBase() + GameInfo.Image_Directory + DirectionInfoArray[11].CG_AvailableURL );
				} catch (Exception e) { System.err.println(" Uhm... no."); };
					addGB( Compass, D = new GraphicButton( this, CurrentURL ), 0, 2);
					D.setActionCommand( DirectionInfoArray[11].Name );
					D.addActionListener( this );
				
			} // TotalDirections >= 11
																
		} // ShowCompass

		// All graphic buttons get set to the Available graphic first, so we want to reflect this here
		DirectionStates = new String[GameInfo.TotalDirections + 1];
		for(int TempIndex = 1; TempIndex <= GameInfo.TotalDirections; TempIndex++)
			DirectionStates[TempIndex] = "Available";
		if ((GameInfo.TotalDirections >= 5) && (GameInfo.CenterButtonIndicatesItems))
			DirectionStates[5] = "ItemsNotPresent";


      // Font Setting
		setFont( new Font("CogEngineText", Font.PLAIN, 10) );

	} //InitializeGUI


	public void addGB( Container container, Component component, int x, int y  ) {
		if ( ! (container.getLayout() instanceof GridBagLayout) )
			container.setLayout( new GridBagLayout() );
		constraints.gridx = x;
		constraints.gridy = y;
		container.add( component, constraints );
	}

	public String GetDirectionState(int DirectionNumber ) {
		// This method takes in a Direction number, and returns which state that direction
		// can be considered to be in. It is used to decide which compass button graphic
		// to use.
		String State;
		
			if ( ( Player.CurrentRoom.DirectionArray[DirectionNumber] != null)
			&& ( ( Player.CurrentRoom.DirectionArray[DirectionNumber].ToWhichRoom > 0 )
			&& ( Player.CurrentRoom.DirectionArray[DirectionNumber].ToWhichRoom <= GameInfo.TotalRooms ) ) ) {
				if ( Player.CurrentRoom.DirectionArray[DirectionNumber].Obstructions != null )
					State = "Obstructed";
				else
					State = "Available";
			}
			else
				State = "Unavailable";
		return (State);
	} // GetDirectionState
	
} // CogEngine class

/**

Contributors:

Steven M. Castellotti (Author, Maintainer, Coder)
Dr. John Lewis (dispenser of indispensable advice)
Dave Sivieri (debugging)

*/
