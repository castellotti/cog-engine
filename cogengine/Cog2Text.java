/*	COG-to-Text Database Converter
	------------------------------
		This program will read in the game database created with Text2Cog
	The program will then proceed to recreate the original text files using
	either the defaul filenames or the names provided by command line parameters.
	This program, like Text2Cog will eventually be incorporated into a separte
	Game Creation Application

	Bug List
	--------
		Cycon-Info.txt
		 - Notes text lines are not same length as headings (refer to original file)
		 - Email address lacks spaces and colon before email address
		 - space after comma missing for Preferred Graphic Dimenions
		 - Line wrapping missing for introduction text
		 - "[Unavailable]" Direction names not printed out 
		 - Inital Room Number and Initial Items lines are not printed out
		 - "Weight" spelled wrong
		 - "Maximum" weight and bulk should be just "Max"
		Cycon-Rooms.txt
		 - "LONG" and "SHORT" should not be capitalized
		 - the word "text" in "Transistion (text)" should have a capital "T"
		 - all transition text fields should be line wrapped
		 - Individual Room's Notes should be line-wrapped
		Cycon-Items.txt
		 - missing space after comma for graphic coordinates
		 - Locations are not formatted correctly (refer to original)
		 - Negative weight fields not outputted (what about bulk)
		 - Text Descriptions should be line-wrapped
		 - Individual Item's Notes should be line-wrapped
		Cycon-Obstructions.txt
		 - missing space after comma for graphic coordinates
		 - Text Descriptions should be line-wrapped
		 - Locations should be written out in string format by default (direction names in GameInfo.Directions)
		 - Individual Obstruction's Notes should be line-wrapped
		Cycon-Verbs.txt
		 - Wrong filename (should be "Verbs")
		Cycon-Events.txt
		 - Should print out string names by default
		 - Should wrap at space before each "(Requires"'s
		 - Effects should be wrapped at space before all "and"'s		

	To-Do List
	----------

*/

import java.io.*;
import java.util.StringTokenizer;
import java.net.URL;
import java.lang.reflect.Array;

public class Cog2Text {

	public static void main(String argv[]) throws IOException, FileNotFoundException, ClassNotFoundException
        { 
           Cog2Text Cog2TextOBJ = new Cog2Text();
           
           String FileNames[] = Cog2TextOBJ.parseCommandLine(argv);

           // Parse the Command Line 
           Cog2TextOBJ.parseCommandLine(argv);

          // Set up input stream for Database File
          FileInputStream COG_DataIn;
          COG_DataIn = new FileInputStream(FileNames[5]);
  
          ObjectInputStream COG_In = new ObjectInputStream(COG_DataIn);

          GameInfoOBJ GameInfo = (GameInfoOBJ)COG_In.readObject();
          PlayerOBJ Player = (PlayerOBJ)COG_In.readObject();
          RoomOBJ[] RoomArray = (RoomOBJ[])COG_In.readObject();
	    ItemOBJ[] ItemArray = (ItemOBJ[])COG_In.readObject();
          ObstructionOBJ[] ObstructionArray = (ObstructionOBJ[])COG_In.readObject();
          VerbOBJ[] VerbArray = (VerbOBJ[])COG_In.readObject();
     
          Cog2TextOBJ.writeinfofile( GameInfo, Player, FileNames[0]);
          Cog2TextOBJ.writeRoomfile( GameInfo, RoomArray, FileNames[1]);
	    Cog2TextOBJ.writeItemfile( GameInfo, ItemArray, FileNames[2]);
	    Cog2TextOBJ.writeObstructionfile( GameInfo, ObstructionArray, FileNames[3]);
	    Cog2TextOBJ.writeVerbfile( GameInfo, VerbArray, FileNames[6]);
	    Cog2TextOBJ.writeEventfile( GameInfo, VerbArray, FileNames[4] );
        }

       void printCommandLineHelp() 
       { 
           System.out.println("Usage: java Cog2Text [OPTION] <FileName> { [OPTION] <FileName>}");
           System.out.println("OPTION choices:");
           System.out.println("-i use <FileName> as output for info file    ( Default: \"Cycon-info.txt\")");
           System.out.println("-r use <FileName> as output for room file    ( Default: \"Cycon-room.txt\")");
           System.out.println("-t use <FileName> as output for item file    ( Default: \"Cycon-items.txt\")");
           System.out.println("-o use <FileName> as output for obstruction file    ( Default: \"Cycon-obstructions.txt\")");
           System.out.println("-e use <FileName> as output for event file    ( Default: \"Cycon-event.txt\")");
           System.out.println("-d use <FileName> as input for database file    ( Default: \"Cycon-COG.dat\")");
	     System.out.println("-v use <Filename> as output for verb file       ( Default: \"Cycon-verb.txt\")");
           System.out.println();
           System.out.println(" ex: java Cog2text -i info.txt -d cog.dat");
   
        }
        String[] parseCommandLine( String argv[]) throws IOException, FileNotFoundException 
        {
          int NumberofFiles = 7;

          // Check to See if he requested help 
          if( ( argv.length == 1 ) && ( ( argv[0].equals("-?") ) || ( argv[0].equals("-help") ) ) )
          {   printCommandLineHelp();
              System.exit(1); // Exits Program
          }
        
         // Parse Command Line

         final int Info = 0, Room = 1, Item = 2, Obstruc = 3, Events = 4, Dat = 5, Verb = 6;
         String[] Filenames = new String[NumberofFiles];

         for( int arg_num = 0; arg_num < argv.length; arg_num += 2 )
         { // check to see if the arg is correct
           if( !argv[arg_num].equals("-i") && !argv[arg_num].equals("-r")
               && !argv[arg_num].equals("-t") && !argv[arg_num].equals("-o") 
               && !argv[arg_num].equals("-e") && !argv[arg_num].equals("-d") 
               && !argv[arg_num].equals("-v") ) 
           { System.err.println("Invalid option entered \"" + argv[arg_num] + "\" program ending"); 
             System.exit(1);
           }
           if( argv[arg_num].equals("-i") )
             Filenames[Info] = argv[arg_num + 1];
           if( argv[arg_num].equals("-r") )
             Filenames[Room] = argv[arg_num + 1];
           if( argv[arg_num].equals("-t") )
             Filenames[Item] = argv[arg_num + 1];
           if( argv[arg_num].equals("-o") )
             Filenames[Obstruc] = argv[arg_num + 1];
           if( argv[arg_num].equals("-e") )
             Filenames[Events] = argv[arg_num + 1];
           if( argv[arg_num].equals("-d") )
             Filenames[Dat] = argv[arg_num + 1];
	     if( argv[arg_num].equals("-v") )
             Filenames[Verb] = argv[arg_num + 1];

         } // End of For Loop

         // If Filenames is still Null ... set Default

         if(Filenames[Info] == null )
            Filenames[Info] = "Cycon-Info.txt";
         if(Filenames[Room] == null )
            Filenames[Room] = "Cycon-Rooms.txt";
         if(Filenames[Item] == null )
            Filenames[Item] = "Cycon-Items.txt";
         if(Filenames[Obstruc] == null )
            Filenames[Obstruc] = "Cycon-Obstruc.txt";
         if(Filenames[Events] == null )
            Filenames[Events] = "Cycon-Events.txt";
         if(Filenames[Dat] == null )
            Filenames[Dat] = "Cycon-COG.dat";
	   if(Filenames[Verb] == null )
            Filenames[Verb] = "Cycon-Verb.txt";
         return Filenames;
        }
        void writeinfofile( GameInfoOBJ GameInfo, PlayerOBJ Player, String Info_file) throws IOException, FileNotFoundException
        {

         // Open up file to write to 
         FileWriter Info_Dataout = new FileWriter( Info_file );
         PrintWriter Info_Out = new PrintWriter( Info_Dataout );

         Info_Out.println("COG Engine Game Module - Info File ");
         Info_Out.println("----------------------------------------");
         Info_Out.println("----------------------------------------");
	 Info_Out.println(" ");
         Info_Out.println("Game Title : " + GameInfo.Game_Title);
         Info_Out.println("Version Number: " + GameInfo.Version_Number);
         Info_Out.println("Game Designer : " + GameInfo.Game_Designer);
         Info_Out.println("Game Designer's Email Address" + GameInfo.Game_Designer_Email_Address);
         Info_Out.println("Last Update : " + GameInfo.LastUpdate);
         Info_Out.println("DebugMode : " + GameInfo.DebugMode);
         Info_Out.println("Game URL : " + GameInfo.GameURL);
         Info_Out.println("Database URL : " + GameInfo.DatabaseURL);
         Info_Out.println("Total Rooms : " + GameInfo.TotalRooms);
         Info_Out.println("Total Items : " + GameInfo.TotalItems);
         Info_Out.println("Total Obstructions : " + GameInfo.TotalObstructions);
	   Info_Out.println("Total Verbs : " + GameInfo.TotalVerbs);
	 Info_Out.println("Preferred Room Graphic Dimensions (x,y) : " + GameInfo.PreferredGraphicSizeX + "," + GameInfo.PreferredGraphicSizeY );
         Info_Out.println("Introduction Graphic : " + GameInfo.Introduction_GraphicURL);
         Info_Out.println("Introduction Text : " + GameInfo.Introduction_Text);
  
         String[] Headings = new String[12];
         Headings[1] = "(NW)";
         Headings[2] = "(N)";
         Headings[3] = "(NE)";
         Headings[4] = "(W)";
         Headings[5] = "(Center)";
         Headings[6] = "(E)";
         Headings[7] = "(SW)";
         Headings[8] = "(S)";
         Headings[9] = "(SE)";
         Headings[10] = "(Up)";
         Headings[11] = "(Down)";

         for ( int graphic_count=1; graphic_count < 12; graphic_count++)
         {
            Info_Out.println("Compass Graphic " + Headings[graphic_count] + " : " + GameInfo.CompassGraphics[graphic_count]);
            Info_Out.println("Compass Graphic [Unavailable] : " + GameInfo.CompassGraphicsUnavailable[graphic_count]);
         }


         // Player Stats

         Info_Out.println(" ");
         Info_Out.println("Player Defaults");
         Info_Out.println("----------------------------");
       
         if( Player.Name != null )
            Info_Out.println("Name : " + Player.Name);
         if( Player.Email_Address != null )
            Info_Out.println("Email Address : " + Player.Email_Address);
         if( Player.Points > 0 )
            Info_Out.println("Points : " + Player.Points);
         if( Player.Exp >= 0 )
            Info_Out.println("Experience : " + Player.Exp);
         if( Player.HP > 0 )
            Info_Out.println("Health Points (HP) : " + Player.HP);
         if( Player.MP > 0 )
            Info_Out.println("Magic Points (MP) : " + Player.MP);
         if( Player.Str > 0 )
            Info_Out.println("Strength (Str) : " + Player.Str);
         if( Player.IQ  > 0 )
            Info_Out.println("Intelligence : " + Player.IQ);
         if( Player.Agil > 0  )
            Info_Out.println("Agility : " + Player.Agil);
         if( Player.Charisma > 0 )
            Info_Out.println("Charisma : " + Player.Charisma);
         if( Player.Armor_Level > 0)
            Info_Out.println("Armor Level : " + Player.Armor_Level);
         if( Player.Max_Weight > 0 )
            Info_Out.println("Maximum Weigth : " + Player.Max_Weight);
	   if( Player.Max_Weight == -1 )
            Info_Out.println("Maximum Weigth : " + Player.Max_Weight);
         if( Player.Max_Bulk > 0 )
            Info_Out.println("Maximum Bulk  : " + Player.Max_Bulk);
         if( Player.Max_Bulk == -1 )
            Info_Out.println("Maximum Bulk  : " + Player.Max_Bulk);
         if( Player.Current_Weight > 0 )         
            Info_Out.println("Current Weight  : " + Player.Current_Weight);


         Info_Out.println("Current Room : " + Player.CurrentRoom.Name + " (" + Player.CurrentRoom.Number + ")" );



         Info_Out.close();

        }
        void writeRoomfile( GameInfoOBJ Info, RoomOBJ[] RoomArray, String Room_file ) throws IOException
        {

         FileWriter Room_Dataout = new FileWriter( Room_file );
         PrintWriter Room_Out = new PrintWriter( Room_Dataout );

         Room_Out.println("COG Engine Game Module - Room File");
         Room_Out.println("----------------------------------");
	   Room_Out.println(Info.RoomHeaderNotes);
         Room_Out.println("----------------------------------");
	   Room_Out.println();	   

	   int room_index = Info.TotalRooms;  
         for( int index = 1; index <= room_index; index++ )
         {
           Room_Out.println("Room # : " + RoomArray[index].Number);
           Room_Out.println("Room Name : " + RoomArray[index].Name);
           Room_Out.println("GraphicURL : " + RoomArray[index].GraphicURL);
           Room_Out.println("Text Description (LONG) : " + RoomArray[index].Description_Long);
           Room_Out.println("Text Description (SHORT) : " + RoomArray[index].Description_Short);
           Room_Out.println("Direction Description : " + RoomArray[index].Direction_Description);
           Room_Out.print("Directions : ");
           if( RoomArray[index].DirectionArray[1] != null )
             Room_Out.print("NorthWest(" + RoomArray[index].DirectionArray[1].ToWhichRoom + "), ");
           if( RoomArray[index].DirectionArray[2] != null )
           Room_Out.print("North(" + RoomArray[index].DirectionArray[2].ToWhichRoom + "), ");
           if( RoomArray[index].DirectionArray[3] != null )
           Room_Out.print("NorthEast(" + RoomArray[index].DirectionArray[3].ToWhichRoom + "), ");
           if( RoomArray[index].DirectionArray[4] != null )
           Room_Out.print("West(" + RoomArray[index].DirectionArray[4].ToWhichRoom + "), ");
           if( RoomArray[index].DirectionArray[5] != null )
           Room_Out.print("Center(" + RoomArray[index].DirectionArray[5].ToWhichRoom + "), ");
           if( RoomArray[index].DirectionArray[6] != null )
           Room_Out.print("East(" + RoomArray[index].DirectionArray[6].ToWhichRoom + "), ");
           if( RoomArray[index].DirectionArray[7] != null )
           Room_Out.print("SouthWest(" + RoomArray[index].DirectionArray[7].ToWhichRoom + "), ");
           if( RoomArray[index].DirectionArray[8] != null )
           Room_Out.print("South(" + RoomArray[index].DirectionArray[8].ToWhichRoom + "), ");
           if( RoomArray[index].DirectionArray[9] != null )
           Room_Out.print("SouthEast(" + RoomArray[index].DirectionArray[9].ToWhichRoom + "), ");
           if( RoomArray[index].DirectionArray[10] != null )
           Room_Out.print("Up(" + RoomArray[index].DirectionArray[10].ToWhichRoom + "), ");
           if( RoomArray[index].DirectionArray[11] != null )
           Room_Out.print("Down(" + RoomArray[index].DirectionArray[11].ToWhichRoom + ") ");
           Room_Out.println("");
           if( RoomArray[index].Items != null )
               Room_Out.println("Items : " + RoomArray[index].Items);
           String[] Direct = new String[12];
           Direct[1] = "North West";
           Direct[2] = "North";
           Direct[3] = "North East";
           Direct[4] = "West";
           Direct[5] = "Center";
	   Direct[6] = "East";  
	   Direct[7] = "South West";  
	   Direct[8] = "South";  
	   Direct[9] = "South East";  
	   Direct[10] = "Up";  
	   Direct[11] = "Down";  
      
         for ( int index_d = 1; index_d < 12; index_d++ )
         { if( RoomArray[index].DirectionArray[index_d] != null )
           {
           if( RoomArray[index].DirectionArray[index_d].TransitionText != null 
              || RoomArray[index].DirectionArray[index_d].Obstructions != null )
           { 
             Room_Out.println("Direction Object : " + Direct[index_d]);
             if( RoomArray[index].DirectionArray[index_d].TransitionText != null ) 
               Room_Out.println("Transition (text) : " + RoomArray[index].DirectionArray[index_d].TransitionText);
             if( RoomArray[index].DirectionArray[index_d].Obstructions != null ) 
               Room_Out.println("Obstruction : " + RoomArray[index].DirectionArray[index_d].Obstructions);
           }
           }
         }
           if( RoomArray[index].Notes != null )
               Room_Out.println("Notes : " + RoomArray[index].Notes);
           Room_Out.println();
         }

         Room_Out.close();
        }
        void writeItemfile( GameInfoOBJ Info, ItemOBJ[] ItemArray, String Item_file ) throws IOException
        {
         FileWriter Item_Dataout = new FileWriter( Item_file );
         PrintWriter Item_Out = new PrintWriter( Item_Dataout );

         Item_Out.println("Cog Engine Game Module - Item File ");
         Item_Out.println("-----------------------------------");

	   Item_Out.println(Info.ItemHeaderNotes);
         Item_Out.println("-----------------------------------");
	   Item_Out.println();
	   int item_total = Info.TotalItems;
         for( int index = 1; index <= item_total; index++ )
         {
          Item_Out.println("Item # : " + ItemArray[index].Number);
          if( ItemArray[index].Name != null )
            Item_Out.println("Item Name : " + ItemArray[index].Name);
          if( ItemArray[index].Aliases != null )
            Item_Out.println("Aliases : " + ItemArray[index].Aliases);
          if( ItemArray[index].Environment_GraphicURL != null )
          {  Item_Out.println("Environment GraphicURL : " + ItemArray[index].Environment_GraphicURL);
             Item_Out.println("Environment Graphic Coordinates (X,Y) : " + ItemArray[index].Environment_Graphic_Xpos + "," + ItemArray[index].Environment_Graphic_Ypos );
          }
          if( ItemArray[index].CloseUp_GraphicURL != null )
             Item_Out.println("CloseUp GraphicURL : " + ItemArray[index].CloseUp_GraphicURL );
          if( ItemArray[index].Icon_GraphicURL != null )
             Item_Out.println("Icon GraphicURL : " + ItemArray[index].Icon_GraphicURL );
          if( ItemArray[index].Equipped_GraphicURL != null )
             Item_Out.println("Equipped GraphicURL : " + ItemArray[index].CloseUp_GraphicURL );
          if( ItemArray[index].Description != null )
	     Item_Out.println("Text Description : " + ItemArray[index].Description );
          if( !(ItemArray[index].Location.equals("0") ))
	     Item_Out.println("Location : " + ItemArray[index].Location );
          if( ItemArray[index].Equipped != false )
	     Item_Out.println("Equipped : " + ItemArray[index].Equipped );
 	  if( ItemArray[index].Weight > 0 )
             Item_Out.println("Weight : " + ItemArray[index].Weight );
 	  if( ItemArray[index].Bulk > 0 )
             Item_Out.println("Bulk : " + ItemArray[index].Weight );
 	  if( ItemArray[index].Notes != null )
 	     Item_Out.println("Notes : " + ItemArray[index].Notes );
          
          Item_Out.println();
         }
         Item_Out.close();
        } // End of Writeinfofile     
        void writeObstructionfile( GameInfoOBJ Info, ObstructionOBJ[] ObsArray, String Obs_file ) throws IOException
        {
         FileWriter Obs_Dataout = new FileWriter( Obs_file );
         PrintWriter Obs_Out = new PrintWriter( Obs_Dataout );
		
         Obs_Out.println("COG Engine Game Module - Obstruction File ");
         Obs_Out.println("------------------------------------------");
	   Obs_Out.println();
	   Obs_Out.println(Info.ObstructionHeaderNotes);
         Obs_Out.println("------------------------------------------");
	   Obs_Out.println();

	   int Obs_total = Info.TotalObstructions;

         for ( int index = 1; index <= Obs_total; index++ )
         {
           Obs_Out.println("Obstruction # : " + ObsArray[index].Number);
           if ( ObsArray[index].Name != null )
	   Obs_Out.println("Obstruction Name : " + ObsArray[index].Name );
           if ( ObsArray[index].Aliases != null )
	   Obs_Out.println("Aliases : " + ObsArray[index].Aliases );
	   if (ObsArray[index].Environment_GraphicURL != null )
           {   Obs_Out.println("Environment GraphicURL : " + ObsArray[index].Environment_GraphicURL);
	       Obs_Out.println("Environment Graphic Coordinates (X,Y) : " + ObsArray[index].Environment_Graphic_Xpos + "," + ObsArray[index].Environment_Graphic_Ypos);
           }
	   if (ObsArray[index].CloseUp_GraphicURL != null )
	       Obs_Out.println("CloseUp GraphicURL : " + ObsArray[index].CloseUp_GraphicURL );
	   if (ObsArray[index].Description != null )
               Obs_Out.println("Text Description : " + ObsArray[index].Description );
	   if (ObsArray[index].Type != null )
               Obs_Out.println("Type : " + ObsArray[index].Type );
	   if (ObsArray[index].Locations != null )
	   {    Obs_Out.print("Locations : ");
		StringTokenizer obs_token = new StringTokenizer( ObsArray[index].Locations, "-, ");
	       Obs_Out.print("Room(" + obs_token.nextToken() + ")Direction["  + obs_token.nextToken() + "]"); 
		while( obs_token.hasMoreTokens() )
	       Obs_Out.print(", Room(" + obs_token.nextToken() + ")Direction["  + obs_token.nextToken() + "]"); 
		Obs_Out.println();
	   }
	   if (ObsArray[index].Visible != false )
	       Obs_Out.println("Visible : Yes");
	   if (ObsArray[index].Visible == false )
	       Obs_Out.println("Visible : No");
           if (ObsArray[index].Notes != null )
	       Obs_Out.println("Notes : " + ObsArray[index].Notes );
           
 	   Obs_Out.println();
         }

         Obs_Out.close();
        } // End of WriteObstructionFile
        void writeVerbfile( GameInfoOBJ Info, VerbOBJ[] VerbArray, String Verb_file ) throws IOException
	  {
         FileWriter Verb_Data = new FileWriter( Verb_file );
	    PrintWriter Verb_Out = new PrintWriter( Verb_Data );


 	    int verb_total = Info.TotalVerbs;	  
	    Verb_Out.println("COG Engine Game Module - Verb List File");
	    Verb_Out.println("---------------------------------------");
	    Verb_Out.println(Info.VerbHeaderNotes);
	    Verb_Out.println("---------------------------------------");
	    Verb_Out.println();
	    for( int i = 1; i <= verb_total; i++)
         {
             Verb_Out.println("Verb #: " + VerbArray[i].Number );
 		Verb_Out.println("Verb Name: " + VerbArray[i].Name );
		if( VerbArray[i].Aliases != null )
		   Verb_Out.println("Aliases: " + VerbArray[i].Aliases );
        	Verb_Out.println();
	    }         
	   Verb_Out.close();
	  } // End writeVerbfile
        void writeEventfile( GameInfoOBJ Info, VerbOBJ[] VerbArray, String Event_file ) throws IOException
	  {
         FileWriter Event_Data = new FileWriter( Event_file );
	   PrintWriter Event_Out = new PrintWriter( Event_Data );

	   Event_Out.println("COG Engine Game Module - Event List File");
	   Event_Out.println("-----------------------------------------");
	   Event_Out.println(Info.EventHeaderNotes);
	   Event_Out.println("-----------------------------------------");
	   Event_Out.println();
     
         int verb_total = Info.TotalVerbs; 
	   for( int i = 1; i <= verb_total; i++ )
	   {  if ( VerbArray[i].TotalEvents > 0 )
	      { // Verb has events go through it events
               int event_total = VerbArray[i].TotalEvents;
		  for( int j = 1; j <= event_total; j++ )
		  { // Print out it Actions and Events
			Event_Out.print(VerbArray[i].Events[j].Action + " " + VerbArray[i].Events[j].Object);
			if( VerbArray[i].Events[j].Preposition != null )
			     Event_Out.print(" " + VerbArray[i].Events[j].Preposition + " " + VerbArray[i].Events[j].Object2);
			if( VerbArray[i].Events[j].Requirements != null )
			{    Event_Out.println();
			     Event_Out.print(VerbArray[i].Events[j].Requirements);	
			}
			Event_Out.println("  ->");
			Event_Out.println(VerbArray[i].Events[j].EffectString);
			Event_Out.println();
		  }
		}
	   } // End of For Loop
         Event_Out.close();
	  } // End of writeEventfile
} // End of Program

