/*	Text-to-COG Database Converter 
	------------------------------
	   This program will read in game information from a plaintext document
	that can be created and edited with any plaintext editor. The input file
	is read and parsed into an array of objects. Those objects are then
	serialized and written to data file. The data file will be read directly
	by the COG Engine during runtime. This program will later be incorporated
	into an independent Game Module Editor.

	Last Modified on 2000.03.18 by Steven M. Castellotti

		This code is released under the GPL (GNU Public License)
		For more information please refer to http://www.gnu.org/copyleft/gpl.html
		Copyright (2000) Steven M. Castellotti


	To-Do List
	----------
	 - Remove EventsFilled from VerbOBJ and use local variable only
	 - Remove TotalEvents from VerbOBJ and use local variable only (should be implicit by length 
	 	of event array)
	 - FileInputStreams should not be opened until it is time to parse the particular file. 
	 	Furthermore, files should not be opened if no objects of that type are indicated in the 
		Info Text File

*/

import java.io.*;
import java.util.*;
import java.net.URL;

public class Text2Cog {

   LineNumberReader InfoStream, DirectionsStream, RoomStream, ItemStream, ObstructionStream, EventStream, VerbStream;  // Sets up all the I/O stream
   ObjectOutputStream COG_OutStream;                                      // Variables this class will use
   int CurrentStreamLine;                                      // This will always be the last line read in of a stream 
   int initialRoom;                                                         // It is optionally used and initialized by methods
  
   public static void main(String argv[]) throws IOException, FileNotFoundException {
    
      Text2Cog Text2CogOBJ = new Text2Cog();

      String FileNames[] = Text2CogOBJ.parseCommandLine(argv);
      
      Text2CogOBJ.parseCommandLine(argv);      
      
      GameInfoOBJ gameInfo = new GameInfoOBJ();
      PlayerOBJ player = new PlayerOBJ();
      // Step 1 - Parse Info File
      System.out.println("Parsing \"" + FileNames[0] + "\"\n");   // Let the user know Info file is being parsed
      Text2CogOBJ.parseInfoFile(gameInfo, player); 

      DirectionInfoOBJ directionArray[] = new DirectionInfoOBJ[gameInfo.TotalDirections + 1];
      // Parse Directions File
      System.out.println("Parsing \"" + FileNames[1] + "\"\n");   // Let the user know Directions file is being parsed
      Text2CogOBJ.parseDirectionsFile(directionArray, gameInfo);

      RoomOBJ roomArray[] = new RoomOBJ[gameInfo.TotalRooms + 1];
      // Step 2 - Parse Rooms File
      System.out.println("Parsing \"" + FileNames[2] + "\"\n");   // Let the user know Room's file is being parsed
      Text2CogOBJ.parseRoomsFile(roomArray, gameInfo, directionArray);

      player.CurrentRoom = roomArray[Text2CogOBJ.initialRoom];     // Now set the initial room for player

      ItemOBJ itemArray[] = new ItemOBJ[gameInfo.TotalItems + 1];
      // Step 3 - Parse Items File
      System.out.println("Parsing \"" + FileNames[3] + "\"\n");   // Let the user know Item's file is being parsed
      Text2CogOBJ.parseItemsFile(itemArray, gameInfo);
      
      ObstructionOBJ obstructionArray[] = new ObstructionOBJ[gameInfo.TotalObstructions + 1];
      // Step 4 - Parse Obstructions File
      System.out.println("Parsing \"" + FileNames[4] + "\"\n");   // Let the user know Obstructions file is being parsed
      Text2CogOBJ.parseObstructionFile(obstructionArray, gameInfo);
     
      VerbOBJ verbArray[] = new VerbOBJ[gameInfo.TotalVerbs + 1];
      // Step 5 - Parse Verbs File
      System.out.println("Parsing \"" + FileNames[5] + "\"\n");   // Let the user know Verbs file is being parsed
      Text2CogOBJ.parseVerbsFile(verbArray, gameInfo);
      
      // Step 6 - Parse Events File
      System.out.println("Parsing \"" + FileNames[6] + "\"\n");   // Let the user know Events file is being parsed
      Text2CogOBJ.parseEventsFile(gameInfo, FileNames[6], itemArray, obstructionArray, roomArray, verbArray, directionArray);
             
      // Now change reduce items, locations, and obstructions to their pure numeric form
      Text2CogOBJ.enumObjects(gameInfo, directionArray, roomArray, itemArray, obstructionArray);
      
      // Now serialize these 6 Objects
      System.out.println("Preparing \"" + FileNames[7] + "\"\n");   // Let the user know the serialized file is being parsed
      Text2CogOBJ.COG_OutStream.writeObject(gameInfo);
      Text2CogOBJ.COG_OutStream.writeObject(directionArray);
      Text2CogOBJ.COG_OutStream.writeObject(player);
      Text2CogOBJ.COG_OutStream.writeObject(roomArray);
      Text2CogOBJ.COG_OutStream.writeObject(itemArray);
      Text2CogOBJ.COG_OutStream.writeObject(obstructionArray);
      Text2CogOBJ.COG_OutStream.writeObject(verbArray);
      Text2CogOBJ.COG_OutStream.close();     
   }  
   
   String replaceObjects(String objectStr, DirectionInfoOBJ directionArray[], RoomOBJ roomArray[], ItemOBJ itemArray[], ObstructionOBJ obstructionArray[]) {

      int startIdx = 0;
      int endIdx = 0;
      int nameIdx = 0;
      int objNum = 0;
      String tempStr = "";
      String topHalf = "";
      String bottomHalf = "";

      if (objectStr == null)
         return null;

      while ((startIdx = objectStr.indexOf("Item[")) != -1) {

         endIdx = objectStr.indexOf("]", startIdx);
         tempStr = objectStr.substring(startIdx, endIdx + 1);

         objNum = identifyItem(tempStr, itemArray);
         if (objNum == -1)
            return null;
         
         tempStr = "Item(" + objNum + ")";
         
         topHalf = objectStr.substring(0, startIdx);
         bottomHalf = objectStr.substring(endIdx + 1); 
         
         objectStr = topHalf + tempStr + bottomHalf;
      }
      
      while ((startIdx = objectStr.indexOf("Obstruction[")) != -1) {

         endIdx = objectStr.indexOf("]", startIdx);
         tempStr = objectStr.substring(startIdx, endIdx + 1);

         objNum = identifyObstruction(tempStr, obstructionArray);
         if (objNum == -1)
            return null;
         
         tempStr = "Obstruction(" + objNum + ")";
         
         topHalf = objectStr.substring(0, startIdx);
         bottomHalf = objectStr.substring(endIdx + 1); 
         
         objectStr = topHalf + tempStr + bottomHalf;
      }
      
      while ((startIdx = objectStr.indexOf("Room[")) != -1) {

         endIdx = objectStr.indexOf("]", startIdx);
         tempStr = objectStr.substring(startIdx, endIdx + 1);

         objNum = identifyRoom(tempStr, roomArray);
         if (objNum == -1)
            return null;
         
         tempStr = "Room(" + objNum + ")";
         
         topHalf = objectStr.substring(0, startIdx);
         bottomHalf = objectStr.substring(endIdx + 1); 
         
         objectStr = topHalf + tempStr + bottomHalf;
      }
      
      while ((startIdx = objectStr.indexOf("Direction[")) != -1) {

         endIdx = objectStr.indexOf("]", startIdx);
         tempStr = objectStr.substring(startIdx + 10, endIdx);

         objNum = enumerateDirection(tempStr, directionArray);
         if (objNum == 0)
            return null;
         
         tempStr = "Direction(" + objNum + ")";
         
         topHalf = objectStr.substring(0, startIdx);
         bottomHalf = objectStr.substring(endIdx + 1); 
         
         objectStr = topHalf + tempStr + bottomHalf;
      }
            
      // This code validates Objects already in an numeric format
      startIdx = 0;
      while ((nameIdx = objectStr.indexOf("Item(", startIdx)) != -1) {

         endIdx = objectStr.indexOf(")", nameIdx);
         tempStr = objectStr.substring(nameIdx, endIdx + 1);

         objNum = identifyItem(tempStr, itemArray);
         if (objNum == -1)
            return null;
         
         startIdx = endIdx + 1;         
      }
      
      startIdx = 0;
      while ((nameIdx = objectStr.indexOf("Obstruction(", startIdx)) != -1) {

         endIdx = objectStr.indexOf(")", nameIdx);
         tempStr = objectStr.substring(nameIdx, endIdx + 1);

         objNum = identifyObstruction(tempStr, obstructionArray);
         if (objNum == -1)
            return null;
         
         startIdx = endIdx + 1;         
      }
     
      startIdx = 0;
      while ((nameIdx = objectStr.indexOf("Room(", startIdx)) != -1) {

         endIdx = objectStr.indexOf(")", nameIdx);
         tempStr = objectStr.substring(nameIdx, endIdx + 1);

         objNum = identifyRoom(tempStr, roomArray);
         if (objNum == -1)
            return null;
         
         startIdx = endIdx + 1;         
      }
      
      startIdx = 0;
      while ((nameIdx = objectStr.indexOf("Direction(", startIdx)) != -1) {

         endIdx = objectStr.indexOf(")", nameIdx);
         tempStr = objectStr.substring(nameIdx + 10, endIdx);
         objNum = Integer.parseInt(tempStr.trim());
                  
         if ((objNum < 0) || (objNum > 11))
            return null;
         
         startIdx = endIdx + 1;
      }
      
      return objectStr;
   }   
   
   void enumObjects(GameInfoOBJ gameInfo, DirectionInfoOBJ directionArray[], RoomOBJ roomArray[], ItemOBJ itemArray[], ObstructionOBJ obstructionArray[]) {

      // Handle Room's array with items 

      for (int ctr = 1; ctr <= gameInfo.TotalRooms; ctr++) {
         
         if((roomArray[ctr].Items != null) && !roomArray[ctr].Items.equals("")) {

            String newItemStr = "";
            int itemNum = 0;
            StringTokenizer itemTokens = new StringTokenizer(roomArray[ctr].Items, ",");
         
            while(itemTokens.hasMoreTokens()) {

               itemNum = identifyItem(itemTokens.nextToken().trim(), itemArray ); 
               if (itemNum == -1)
                  returnError("There is an invalid item in room # " + ctr);
               
               if (itemTokens.hasMoreTokens())
                  newItemStr += (itemNum + ", ");
               else
                  newItemStr += itemNum;
            }
            roomArray[ctr].Items = newItemStr;
         }   
      }
     
      // Handle Item's array with locations

      for (int ctr = 1; ctr <= gameInfo.TotalItems; ctr++) {
      
         if((!itemArray[ctr].Location.equals("0") ) && !itemArray[ctr].Location.equals("")) {

            String newLocationStr = "";
            StringTokenizer roomTokens = new StringTokenizer(itemArray[ctr].Location, ",");
            int roomNum = 0;

            while(roomTokens.hasMoreTokens()) {
               String tempRoom = roomTokens.nextToken().trim(); 
               roomNum = identifyRoom(tempRoom, roomArray); 
               if (roomNum == -1)
                  returnError("There is an invalid room named: " + tempRoom + " in item # " + ctr);
                 
               if (roomTokens.hasMoreTokens())
                  newLocationStr += (roomNum + ", ");
               else
                  newLocationStr += roomNum;
            }
            itemArray[ctr].Location = newLocationStr;
         }   
      }
       
      // Handle Obstructions's array with locations

      for (int ctr = 1; ctr <= gameInfo.TotalObstructions; ctr++) {
      
         if((obstructionArray[ctr].Locations != null) && !obstructionArray[ctr].Locations.equals("")) {

            String newLocationStr = "";
            StringTokenizer roomTokens = new StringTokenizer(obstructionArray[ctr].Locations, ",");
            int roomNum = 0;
            int dirNum = 0;

            while(roomTokens.hasMoreTokens()) {

               String tempRoom = roomTokens.nextToken().trim();
               
               // Handle room number
               String room = "";
               int indexOfClose = 0;

               if(tempRoom.startsWith("Room[")) {
                  indexOfClose = tempRoom.indexOf("]"); 
                  room = tempRoom.substring(0, indexOfClose + 1);
               }
               else if(tempRoom.startsWith("Room(")) {
                  indexOfClose = tempRoom.indexOf(")"); 
                  room = tempRoom.substring(0, indexOfClose + 1);                  
               }

               roomNum = identifyRoom(room, roomArray);
               if (roomNum == -1)
                     returnError("There is an invalid room named: " + tempRoom + " in obstruction # " + ctr);
               
               // Now handle directions 

               String direction = tempRoom.substring(indexOfClose + 1);
               
               if(direction.startsWith("Direction[")) {
                  String DirName = direction.substring(direction.indexOf("[") + 1, direction.indexOf("]"));
                  dirNum = enumerateDirection(DirName.trim(), directionArray);               
               }
               else if(direction.startsWith("Direction(")) {
                  String DirName = direction.substring(direction.indexOf("(") + 1, direction.indexOf(")"));
                  dirNum = Integer.parseInt(DirName.trim());               
               }               
               if (roomNum == -1)
                  returnError("There is an invalid Direction Name in obstruction # " + ctr);
               
               if (roomTokens.hasMoreTokens())
                  newLocationStr += (roomNum + "-" + dirNum + ", ");
               else
                  newLocationStr += (roomNum + "-" + dirNum);
            }
            obstructionArray[ctr].Locations = newLocationStr;
         }   
      }
     
      // Now handle all directional Objects Obstructions field   
      String tempObstr = "";      
      for (int ctr = 1; ctr <= gameInfo.TotalRooms; ctr++) {

         for(int dirOBJCtr = 1; dirOBJCtr <= (roomArray[ctr].DirectionArray.length - 1); dirOBJCtr++) {
            
            if (roomArray[ctr].DirectionArray[dirOBJCtr] != null) {
               String obstrStr = roomArray[ctr].DirectionArray[dirOBJCtr].Obstructions;
               if (obstrStr != null) {
                  
                  StringTokenizer dirOBJTokens = new StringTokenizer(obstrStr, ",");
                  while (dirOBJTokens.hasMoreTokens()) {
                     int obstrNum = identifyObstruction(dirOBJTokens.nextToken().trim(), obstructionArray);
                     if (obstrNum == -1)
                        returnError("There is an invalid Obstruction named: " + obstrStr + " in Room: " + ctr);
                     if (dirOBJTokens.hasMoreTokens()) 
                        tempObstr += obstrNum + ", ";   
                     else
                        tempObstr += obstrNum; 
                  }                
                     roomArray[ctr].DirectionArray[dirOBJCtr].Obstructions = tempObstr;
                     tempObstr = "";      
               }
            }
         }
      }     
            
      // Now here is code for consistency cross checking   
   
      int tempOBJNum1, tempOBJNum2, tempOBJNum3;
      boolean hasMatch;

      // Check if all items listed in a particular room in room's file are actually listed as being in that room in item's file
      for (int room = 1; room <= roomArray.length - 1; room++) {

         if (roomArray[room].Items != null) {
            StringTokenizer itemTokens = new StringTokenizer(roomArray[room].Items, ",");            
            while(itemTokens.hasMoreTokens()) {
         
               tempOBJNum1 = Integer.parseInt(itemTokens.nextToken().trim());

               hasMatch = false;
               if (itemArray[tempOBJNum1].Location == null)
                  returnError("Consistency error in Room # " + room + ".  Item # " + tempOBJNum1 + 
                              " is listed as being in this room in the room's file but not in the item's file.");
               else {
                  StringTokenizer roomTokens = new StringTokenizer(itemArray[tempOBJNum1].Location, ",");  
                  while(roomTokens.hasMoreTokens()) {

                     tempOBJNum2 = Integer.parseInt(roomTokens.nextToken().trim());             
                     if (room == tempOBJNum2)
                        hasMatch = true;
                  }
                  if (hasMatch == false)
                     returnError("Consistency error in Room # " + room + ".  Item # " + tempOBJNum1 + 
                                 " is listed as being in this room in the room's file but not in the item's file.");
               }
            }
         }

         // Now Check for Obstruction consistency in directional objects
         for (int dir = 1; dir <= gameInfo.TotalDirections; dir++) {

            if ((roomArray[room].DirectionArray[dir] != null) && (roomArray[room].DirectionArray[dir].Obstructions != null)) {
         
               StringTokenizer obstructionTokens = new StringTokenizer(roomArray[room].DirectionArray[dir].Obstructions, ",");            
               while(obstructionTokens.hasMoreTokens()) {
         
                  tempOBJNum1 = Integer.parseInt(obstructionTokens.nextToken().trim());
                  hasMatch = false;
                  if (obstructionArray[tempOBJNum1].Locations == null)
                     returnError("Consistency error in Room # " + room + ".  Obstruction # " + tempOBJNum1 + 
                                 " is listed as being in this room in Direction # " + dir + " in the room's file but not in the obstruction's file.");
                  
                  else {
                     StringTokenizer dirOBJTokens = new StringTokenizer(obstructionArray[tempOBJNum1].Locations, ",");  
                     while(dirOBJTokens.hasMoreTokens()) {

                        StringTokenizer dirOBJTokens2 = new StringTokenizer(dirOBJTokens.nextToken(), "-");
                        tempOBJNum2 = Integer.parseInt(dirOBJTokens2.nextToken().trim()); 
                        tempOBJNum3 = Integer.parseInt(dirOBJTokens2.nextToken().trim());
                        
                        if (room == tempOBJNum2 && dir == tempOBJNum3)
                           hasMatch = true;                           
                     }
                     if (hasMatch == false)
                        returnError("Consistency error in Room # " + room + ".  Obstruction # " + tempOBJNum1 + 
                                    " is listed as being in this room in Direction # " + dir + " in the room's file but not in the obstruction's file.");
                  }                           
               }
            }
         }
      }
      
      // Check if all obstructions being listed in a particular room is a particular direction in the obstruction's files are also listed as being so in the room's file
      for (int obstruction = 1; obstruction <= obstructionArray.length - 1; obstruction++) {
         
         if (obstructionArray[obstruction].Locations != null) {
            
            StringTokenizer dirOBJTokens = new StringTokenizer(obstructionArray[obstruction].Locations, ",");            
            while(dirOBJTokens.hasMoreTokens()) {
               
               StringTokenizer dirOBJTokens2 = new StringTokenizer(dirOBJTokens.nextToken(), "-");
               tempOBJNum1 = Integer.parseInt(dirOBJTokens2.nextToken().trim()); 
               tempOBJNum2 = Integer.parseInt(dirOBJTokens2.nextToken().trim());
                       
               hasMatch = false;
                       
               if((roomArray[tempOBJNum1].DirectionArray[tempOBJNum2] == null) || (roomArray[tempOBJNum1].DirectionArray[tempOBJNum2].Obstructions == null))
                  returnError("Consistency error in Obstruction # " + obstruction + ".  Room # " + tempOBJNum1 + 
                              " is listed as being a location for this obstruction in Direction # " + tempOBJNum2 + " in the obstruction's file but not in the room's file.");
               else {
                  StringTokenizer ObstructionTokens = new StringTokenizer(roomArray[tempOBJNum1].DirectionArray[tempOBJNum2].Obstructions, ",");
                  while(ObstructionTokens.hasMoreTokens()) {
                                         
                     tempOBJNum3 = Integer.parseInt(ObstructionTokens.nextToken().trim());
                        
                     if (obstruction == tempOBJNum3)
                        hasMatch = true;                           
                  }
                  if (hasMatch == false)
                     returnError("Consistency error in Obstruction # " + obstruction + ".  Room # " + tempOBJNum1 + 
                              " is listed as being a location for this obstruction in Direction # " + tempOBJNum2 + " in the obstruction's file but not in the room's file.");
               }                             
            }           
         }
      }

      // Check if all rooms being listed as the location of a particular item in items file are actually listed as being the location of the item in room's file
      for (int item = 1; item <= itemArray.length - 1; item++) {
        
         if ((itemArray[item].Location != null) && (!itemArray[item].Location.trim().equals("0"))) {
            StringTokenizer roomTokens = new StringTokenizer(itemArray[item].Location, ",");            
            while(roomTokens.hasMoreTokens()) {
              
               tempOBJNum1 = Integer.parseInt(roomTokens.nextToken().trim());

               hasMatch = false;
                       
               if(roomArray[tempOBJNum1].Items == null)
                  returnError("Consistency error in Item # " + item + ".  Room # " + tempOBJNum1 + 
                              " is listed as being a location for this item in the item's file but not in the room's file.");  
               else {
                  
                  StringTokenizer itemTokens = new StringTokenizer(roomArray[tempOBJNum1].Items, ",");  
                  while(itemTokens.hasMoreTokens()) {
                  
                     tempOBJNum2 = Integer.parseInt(itemTokens.nextToken().trim());             
                     if (item == tempOBJNum2)
                        hasMatch = true;
                  }
                 
                  if (hasMatch == false)
                     returnError("Consistency error in Item # " + item + ".  Room # " + tempOBJNum1 + 
                                 " is listed as being a location for this item in the item's file but not in the room's file.");
               }
            }
         }
      }




      
   }
   
   void parseEventsFile(GameInfoOBJ gameInfo, String eventFileName, ItemOBJ[] itemArray, ObstructionOBJ[] obstructionArray, RoomOBJ[] roomArray, VerbOBJ [] verbArray, DirectionInfoOBJ directionArray[]) throws IOException {
      
      int numEvents = 0;
      String returnedString;
     
      // This is for the first pass through the Events file - determines # of Events and Events per Action
      LineNumberReader TempEventStream = new LineNumberReader(new FileReader(eventFileName));
      
      gameInfo.EventHeaderNotes = skipComments(TempEventStream, "---------------");       // Move past file comments            
     
      while ( (returnedString = TempEventStream.readLine()) != null) {
         
         while(returnedString.trim().equals("")) {      // Eliminate blank lines between of Events
            returnedString = TempEventStream.readLine();
            if(returnedString == null)
               break;
         }
           
         if(returnedString == null)
            break;
         
         while(!returnedString.trim().endsWith(";")) 
            returnedString += TempEventStream.readLine();         
   
         returnedString = returnedString.trim();
         numEvents++;
         
         // Now a complete Event String is inside returnedString
         StringTokenizer actionToken = new StringTokenizer(returnedString);
         String action = actionToken.nextToken();
         
         if(identifyVerb(action, verbArray) == -1)
            returnError("Error on line: " + TempEventStream.getLineNumber() + "\n" + 
                        "Action: \"" + action + "\" does not resolved to previously defined verb.");
         else 
            verbArray[identifyVerb(action, verbArray)].TotalEvents++;
         
      }
      // End first pass
      
      // Now for each unique action, set the Events array to the number of unique events for that action
      for (int i = 1; i <= verbArray.length - 1; i++) 
         verbArray[i].Events = new EventOBJ[verbArray[i].TotalEvents + 1];
            
      // Now begin 2nd pass - Actually read in each Event and parse it into appropriate fields in EventArray

      gameInfo.EventHeaderNotes = skipComments(EventStream, "---------------");       // Move past file comments            
      
      for (int eventCtr = 1; eventCtr <= numEvents; eventCtr++) {
               
         do {                                               // Eliminate blank lines between Events
            returnedString = EventStream.readLine();
         }
         while ( returnedString.trim().equals("") );
               
         while(!returnedString.trim().endsWith(";")) 
            returnedString += EventStream.readLine();
                          
         // Now we have a full Event string inside returnedString
         returnedString = returnedString.trim(); 
         int indexOfMark = returnedString.indexOf("->"); 
       
         String command = returnedString.substring(0, indexOfMark).trim();
         String yields = returnedString.substring(indexOfMark + 2).trim();
                      
         // Get the array indexes set up
         StringTokenizer commandTokens = new StringTokenizer(command);
         String action = commandTokens.nextToken().trim();

         int verbNum = identifyVerb(action, verbArray);
         int eventIndex = verbArray[verbNum].EventsFilled + 1;
         verbArray[verbNum].Events[eventIndex] = new EventOBJ();
         verbArray[verbNum].EventsFilled++;
         
         // Now we have all array indexes, we can load the needed EventOBJ object
                                              
         // Load the EffectString
         verbArray[verbNum].Events[eventIndex].EffectString = yields.substring(0, yields.lastIndexOf(";"));  
              
         // Load the Action String
         verbArray[verbNum].Events[eventIndex].Action = action;
                   
         // Take care of first object
         String Object = commandTokens.nextToken().trim();
     
         if (Object.indexOf("[") != -1) {

            while(!Object.endsWith("]"))
               Object += (" " + commandTokens.nextToken());
            verbArray[verbNum].Events[eventIndex].Object = Object;
         }
         else if (Object.indexOf("(") != -1) {
            verbArray[verbNum].Events[eventIndex].Object = Object;
         }
         
         // Now handle preps, Object2, and reqs
         if (commandTokens.hasMoreTokens()) {

            String requirementsStr = commandTokens.nextToken(); 
            if (!requirementsStr.equals("(Requires")) {
            
               verbArray[verbNum].Events[eventIndex].Preposition = requirementsStr;   
            
               String Object2 = commandTokens.nextToken().trim();

               if (Object2.indexOf("[") != -1) {

                  while(!Object2.endsWith("]"))
                     Object2 += (" " + commandTokens.nextToken());
                  verbArray[verbNum].Events[eventIndex].Object2 = Object2;
               }
               else if (Object2.indexOf("(") != -1) {
            
                  verbArray[verbNum].Events[eventIndex].Object2 = Object2;
               }
                                 
               // Now see if there are Requirements to handle
               if (commandTokens.hasMoreTokens()) {
                  String reqStr = commandTokens.nextToken(""); 
                  
                  if (reqStr.startsWith("(Requires")) {

                     verbArray[verbNum].Events[eventIndex].Requirements = reqStr.trim();      
                  }
               }              
            }       
            // Do if there are only Requirements to handle and not Object 2 and prep to handle
            else if (requirementsStr.equals("(Requires")) {

               requirementsStr += commandTokens.nextToken("");
               requirementsStr = requirementsStr.trim();

               verbArray[verbNum].Events[eventIndex].Requirements = requirementsStr;                        
           }           
         }
         
         // Now convert all fields in EventObj to the numeric format Object()
         String temp;

         temp = verbArray[verbNum].Events[eventIndex].Object;
         if (temp != null) { 

            temp = replaceObjects(temp, directionArray, roomArray, itemArray, obstructionArray);
            if (temp == null)
               returnError("Error before line: " + EventStream.getLineNumber() + "\n" + 
                           "There is an invalid room, item, obstruction, or direction entered in Object 1");
            else
               verbArray[verbNum].Events[eventIndex].Object = temp.trim();
         }
                  
         temp = verbArray[verbNum].Events[eventIndex].Object2;
         if (temp != null) { 

            temp = replaceObjects(temp, directionArray, roomArray, itemArray, obstructionArray);
            if (temp == null)
               returnError("Error before line: " + EventStream.getLineNumber() + "\n" + 
                           "There is an invalid room, item, obstruction, or direction entered in Object 2");
            else
               verbArray[verbNum].Events[eventIndex].Object2 = temp.trim();
         }
         
         temp = verbArray[verbNum].Events[eventIndex].Requirements;
         if (temp != null) { 

            temp = replaceObjects(temp, directionArray, roomArray, itemArray, obstructionArray);
            if (temp == null)
               returnError("Error before line: " + EventStream.getLineNumber() + "\n" + 
                           "There is an invalid room, item, obstruction, or direction entered in the requirements string");
            else
               verbArray[verbNum].Events[eventIndex].Requirements = temp.trim();
         }

         temp = verbArray[verbNum].Events[eventIndex].EffectString;
         if (temp != null) { 
            
            temp = replaceObjects(temp, directionArray, roomArray, itemArray, obstructionArray);
            if (temp == null)
               returnError("Error before line: " + EventStream.getLineNumber() + "\n" + 
                           "There is an invalid room, item, obstruction, or direction entered in the effect string");
            else
               verbArray[verbNum].Events[eventIndex].EffectString = temp.trim();
         }                  
      }
   }
   
   int identifyRoom(String roomName, RoomOBJ roomArray[]) {

      int stopIndex = 0; 
      String Name = ""; 
      int Number = -1;

      if (roomName.toLowerCase().startsWith("room[")) {
         
         stopIndex = roomName.lastIndexOf("]");
         Name = roomName.substring(5, stopIndex);      
         
         for (int i = 1; i <= roomArray.length - 1; i++)         
            if (roomArray[i].Name.equals(Name))
               return roomArray[i].Number;
      }
      else if (roomName.toLowerCase().startsWith("room(")) {
         stopIndex = roomName.lastIndexOf(")");
         Number = Integer.parseInt(roomName.substring(5, stopIndex).trim());     
         if (( Number < 0) || (Number > roomArray.length - 1))
            return -1;
         else
            return Number;   
      }
      return -1;   
   }
  
   int identifyItem(String itemName, ItemOBJ itemArray[]) {
      
      int stopIndex = 0; 
      String Name = ""; 
      int Number = -1;

      if (itemName.toLowerCase().startsWith("item[")) {
         
         stopIndex = itemName.lastIndexOf("]");
         Name = itemName.substring(5, stopIndex);      
         
         for (int i = 1; i <= itemArray.length - 1; i++)         
            if (itemArray[i].Name.equals(Name))
               return itemArray[i].Number;
      }
      else if (itemName.toLowerCase().startsWith("item(")) {
         stopIndex = itemName.lastIndexOf(")");
         Number = Integer.parseInt(itemName.substring(5, stopIndex).trim());     
        if (( Number < 1) || (Number > itemArray.length - 1))
            return -1;
         else
            return Number;      
      }
      return -1;     
   }

  int identifyObstruction(String obstructionName, ObstructionOBJ obstructionArray[]) {
      int stopIndex = 0; 
      String Name = ""; 
      int Number = -1;

      if (obstructionName.toLowerCase().startsWith("obstruction[")) {
         
         stopIndex = obstructionName.lastIndexOf("]");
         Name = obstructionName.substring(12, stopIndex);      
         
         for (int i = 1; i <= obstructionArray.length - 1; i++)         
            if (obstructionArray[i].Name.equals(Name))
               return obstructionArray[i].Number;
      }
      else if (obstructionName.toLowerCase().startsWith("obstruction(")) {
         stopIndex = obstructionName.lastIndexOf(")");
         Number = Integer.parseInt(obstructionName.substring(12, stopIndex).trim());     
         if (( Number < 1) || (Number > obstructionArray.length - 1))
            return -1;
         else
            return Number;      
      }
      return -1;        
   }

   int identifyVerb(String verbName, VerbOBJ[] verbArray) {
    
      for (int i = 1; i <= verbArray.length - 1; i++) {
         if (verbArray[i].Name.equals(verbName))
            return verbArray[i].Number;
         
         if (verbArray[i].Aliases != null) {
            StringTokenizer verbTokens = new StringTokenizer(verbArray[i].Aliases, ",");
            while (verbTokens.hasMoreTokens()) {
         
               if(verbName.equals(verbTokens.nextToken().trim()))
                  return verbArray[i].Number;
            }
         }
      }      
      return -1;   
   }

   void printCommandLineHelp() {
      System.out.println("Usage: java Text2Cog [OPTION] <filename> {[OPTION] <filename>}");      
      System.out.println("OPTION choices:");
      System.out.println("-n  use <filename> as input info file        (Default: \"Cycon-Info.txt\")");
      System.out.println("-d  use <filename> as input directions file  (Default: \"Cycon-Directions.txt\")");
      System.out.println("-r  use <filename> as input room file        (Default: \"Cycon-Rooms.txt\")");
      System.out.println("-i  use <filename> as input item file        (Default: \"Cycon-Items.txt\")");
      System.out.println("-b  use <filename> as input obstruction file (Default: \"Cycon-Obstructions.txt\")");
      System.out.println("-e  use <filename> as input event file       (Default: \"Cycon-Events.txt\")");
      System.out.println("-v  use <filename> as input verbs file       (Default: \"Cycon-Verbs.txt\")");
      System.out.println("-o  use <filename> as output data file       (Default: \"Cycon-COG.dat\")");
      System.out.println();
      System.out.println("  ex: java Text2Cog -r rooms.txt -o output.dat");
      System.out.println();
   }

   String[] parseCommandLine(String argv[]) throws FileNotFoundException, IOException {

      final int NumberOfFiles = 8;

      if ((argv.length == 1) && ( (argv[0].equals("-?")) || (argv[0].equals("-help")) || (argv[0].equals("/?")) ) ) {
         // The user is asking for help with Command-Line arguments
         printCommandLineHelp();
         System.exit(1); // Aborts Program
      }

      // Check to see if a proper number of arguments were entered
      if( (argv.length > 0) && ( (argv.length % 2) != 0) ) {
         System.err.println("Invalid number of arguments entered - program ending");
         System.exit(1);  // Aborts Program
      }

      // Parsing all command line arguments

      String[] FileNames = new String[NumberOfFiles]; // Array that holds whether or not the user specified a unique filename
                                                      // Automatically initialized to all **null**
      final int Info = 0, Directions = 1, Room = 2, Item = 3, Obstruction = 4, Verb = 5, Event = 6, COG_Out = 7; // Constants for ths IsSpecified Array

      // Will run loop until all arguments are handled
      // If no filename is entered, then default names are use
      // If the user enters an option (ex -i), then the next argument is taken to be a filename, even if unintended
   
      try {  // Catches errors in opening non-existant files

         for(int arg_num = 0; arg_num < argv.length; arg_num += 2) {

            if(!argv[arg_num].equals("-n") && !argv[arg_num].equals("-r") && !argv[arg_num].equals("-i") && !argv[arg_num].equals("-d") &&
               !argv[arg_num].equals("-b") && !argv[arg_num].equals("-e") && !argv[arg_num].equals("-v") && !argv[arg_num].equals("-o")) {
               System.err.println("Invalid option entered \"" + argv[arg_num] + "\" program ending");
               System.exit(1);
            }
            if(argv[arg_num].equals("-n")) {
               InfoStream = new LineNumberReader(new FileReader(argv[arg_num + 1]));
               FileNames[Info] = argv[arg_num + 1];
            }
            else if(argv[arg_num].equals("-d")) {
               DirectionsStream = new LineNumberReader(new FileReader(argv[arg_num + 1]));
               FileNames[Directions] = argv[arg_num + 1];
            }
            else if(argv[arg_num].equals("-r")) {
               RoomStream = new LineNumberReader(new FileReader(argv[arg_num + 1]));   
               FileNames[Room] = argv[arg_num + 1];
            }
            else if(argv[arg_num].equals("-i")) {
               ItemStream = new LineNumberReader(new FileReader(argv[arg_num + 1]));
               FileNames[Item] = argv[arg_num + 1];
            }
            else if(argv[arg_num].equals("-b")) {
               ObstructionStream = new LineNumberReader(new FileReader(argv[arg_num + 1]));
               FileNames[Obstruction] = argv[arg_num + 1];
            }
            else if(argv[arg_num].equals("-e")) {
               EventStream = new LineNumberReader(new FileReader(argv[arg_num + 1]));
               FileNames[Event] = argv[arg_num + 1];
            }
            else if(argv[arg_num].equals("-v")) {
               VerbStream = new LineNumberReader(new FileReader(argv[arg_num + 1]));
               FileNames[Verb] = argv[arg_num + 1];
            }
            else if(argv[arg_num].equals("-o")) {
               COG_OutStream = new ObjectOutputStream(new FileOutputStream(argv[arg_num + 1]));
               FileNames[COG_Out] = argv[arg_num + 1];
            }
         }
         // Finally use default input files for files the user did not specify

         if(FileNames[Info] == null) {
            InfoStream = new LineNumberReader(new FileReader("Cycon-Info.txt"));
            FileNames[Info] = "Cycon-Info.txt";
         }
         if(FileNames[Directions] == null) {
            DirectionsStream = new LineNumberReader(new FileReader("Cycon-Directions.txt"));
            FileNames[Directions] = "Cycon-Directions.txt";
         }
         if(FileNames[Room] == null) {
            RoomStream = new LineNumberReader(new FileReader("Cycon-Rooms.txt"));
            FileNames[Room] = "Cycon-Rooms.txt";
         }
         if(FileNames[Item] == null) {
            ItemStream = new LineNumberReader(new FileReader("Cycon-Items.txt"));
            FileNames[Item] = "Cycon-Items.txt";
         }
         if(FileNames[Obstruction] == null) {
            ObstructionStream = new LineNumberReader(new FileReader("Cycon-Obstructions.txt"));
            FileNames[Obstruction] = "Cycon-Obstructions.txt";
         }
         if(FileNames[Event] == null) {
            EventStream = new LineNumberReader(new FileReader("Cycon-Events.txt"));
            FileNames[Event] = "Cycon-Events.txt";
         }
         if(FileNames[Verb] == null) {
            VerbStream = new LineNumberReader(new FileReader("Cycon-Verbs.txt"));
            FileNames[Verb] = "Cycon-Verbs.txt";
         }
         if(FileNames[COG_Out] == null) {
            COG_OutStream = new ObjectOutputStream(new FileOutputStream("Cycon-COG.dat"));
            FileNames[COG_Out] = "Cycon-COG.dat";
         }
      } catch(FileNotFoundException file_error) {
           System.err.println(file_error);
           System.exit(1);
      } catch(IOException IO_error) {
           System.err.println(IO_error);
           System.exit(1);
      }
      
      return FileNames;
   }
   
   // This method will parse the Info input file  
   void parseInfoFile(GameInfoOBJ gameInfo, PlayerOBJ player) throws IOException {
         
      String lineArray[] = new String[512];
      int numLines = 0;  
      int currentLine[] = {0};   // This is only an array so it can be passed to a method and changed in the method
      String returnedString;
      CurrentStreamLine = 0;
                 
      numLines = 0;
      currentLine[0] = 1;
     
      gameInfo.GameInfoHeaderNotes = skipComments(InfoStream, "---------------");       // Move past file comments            
     
      do {                                               // Eliminate blank lines between Rooms
         returnedString = InfoStream.readLine();
         CurrentStreamLine++;
      }
      while ( returnedString.trim().equals("") );
       
      int ctr = 1;
      while ( (returnedString != null) && !(returnedString.trim().equals("")) ) {   // Now read in complete info data
         lineArray[ctr] = returnedString;
         ctr++;
         numLines++;
         returnedString = InfoStream.readLine();
         CurrentStreamLine++;
      }      
      
      // Begin Step 1 - Read in Game Title
      returnedString = 
         parseMultiLines(lineArray, numLines, currentLine, "Game Title :", "Version Number :", ":");
      if (returnedString != null)
         gameInfo.Game_Title = returnedString;
      else
         returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                     "Required field \"Game Title :\" missing");

      // Begin Step 2 - Read in Version Number
      returnedString = 
         parseMultiLines(lineArray, numLines, currentLine, "Version Number :", "Game Designer :", ":");
      if (returnedString != null)
         gameInfo.Version_Number = returnedString;
      else
         returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                     "Required field \"Version Number :\" missing");
      
      // Begin Step 3 - Read in Game Designer
      returnedString =
         parseMultiLines(lineArray, numLines, currentLine, "Game Designer :", "Game Designer's Email Address :", ":");
      if (returnedString != null)
         gameInfo.Game_Designer = returnedString;
      else
         returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                     "Required field \"Game Designer :\" missing");

      // Begin Step 4 - Read in Game Designer's Email Address
      returnedString =
         parseMultiLines(lineArray, numLines, currentLine, "Game Designer's Email Address :", "Last Update :", ":");
      if (returnedString != null)
         gameInfo.Game_Designer_Email_Address = returnedString;
      else
         returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                     "Required field \"Game Designer's Email Address :\" missing");

      // Begin Step 5 - Read in Last Update
      returnedString =
         parseMultiLines(lineArray, numLines, currentLine, "Last Update :", "DebugMode :", ":");
      if (returnedString != null)
         gameInfo.LastUpdate = returnedString;
      else
         returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                     "Required field \"Last Update :\" missing");

      // Read in DebugMode
      returnedString =
         parseMultiLines(lineArray, numLines, currentLine, "DebugMode :", "Game URL :", ":");
      if (returnedString != null) {
         if(returnedString.equals("true"))
            gameInfo.DebugMode = true;
         else if(returnedString.equals("false"))
            gameInfo.DebugMode = false;
      }         
      else
         returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                     "Required field \"DebugMode :\" missing");

      // Begin Step 6 - Read in Game URL
      returnedString =
         parseMultiLines(lineArray, numLines, currentLine, "Game URL :", "Database URL :", ":");
      if (returnedString != null)
         gameInfo.GameURL = returnedString;
      else
         returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                     "Required field \"Game URL :\" missing");

      // Begin Step 7 - Read in Database URL
      returnedString =
         parseMultiLines(lineArray, numLines, currentLine, "Database URL :", "Total Directions :", ":");
      if (returnedString != null)
         gameInfo.DatabaseURL = returnedString;
      else
         returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                     "Required field \"Database URL :\" missing");

      // Begin Step 8 - Read in Total Directions
      returnedString =
         parseMultiLines(lineArray, numLines, currentLine, "Total Directions :", "Total Rooms :", ":");
      try {
         if (returnedString != null)
            gameInfo.TotalDirections = Integer.parseInt(returnedString);
         else
            returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                        "Required field \"Total Directions :\" missing");
      } catch(NumberFormatException error) {
              returnError("Error around line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                          "A number could not be properly parsed.\n" + "This may mean a required field is missing");
        }
      // Begin Step 9 - Read in Total Rooms
      returnedString =
         parseMultiLines(lineArray, numLines, currentLine, "Total Rooms :", "Total Items :", ":");
      try {
         if (returnedString != null)
            gameInfo.TotalRooms = Integer.parseInt(returnedString);
         else
            returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                        "Required field \"Total Rooms :\" missing");
      } catch(NumberFormatException error) {
              returnError("Error around line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                          "A number could not be properly parsed.\n" + "This may mean a required field is missing");
        }
      // Begin Step 10 - Read in Total Items
      returnedString =
         parseMultiLines(lineArray, numLines, currentLine, "Total Items :", "Total Obstructions :", ":");
      try {
         if (returnedString != null)
            gameInfo.TotalItems = Integer.parseInt(returnedString);
         else
            returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                        "Required field \"Total Items :\" missing");
      } catch(NumberFormatException error) {
              returnError("Error around line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                          "A number could not be properly parsed.\n" + "This may mean a required field is missing");
        }

      // Begin Step 11 - Read in Total Obstructions
      returnedString =
         parseMultiLines(lineArray, numLines, currentLine, "Total Obstructions :", "Total Verbs :", ":");
      try {
         if (returnedString != null)
            gameInfo.TotalObstructions = Integer.parseInt(returnedString);
         else
            returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                        "Required field \"Total Obstructions :\" missing");
      } catch(NumberFormatException error) {
              returnError("Error around line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                          "A number could not be properly parsed.\n" + "This may mean a required field is missing");
        }

      // Read in Total Verbs
      returnedString =
         parseMultiLines(lineArray, numLines, currentLine, "Total Verbs :", "Show All Verbs :", ":");
      try {
         if (returnedString != null)
            gameInfo.TotalVerbs = Integer.parseInt(returnedString);
         else
            returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                        "Required field \"Total Verbs :\" missing");
      } catch(NumberFormatException error) {
              returnError("Error around line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                          "A number could not be properly parsed.\n" + "This may mean a required field is missing");
        }      

      // Read in Show All Verbs
      returnedString =
         parseMultiLines(lineArray, numLines, currentLine, "Show All Verbs :", "Image Loading Graphic :", ":");
      if (returnedString != null) {
         if(returnedString.equals("true"))
            gameInfo.ShowAllVerbs = true;
         else if(returnedString.equals("false"))
            gameInfo.ShowAllVerbs = false;
      }         
      else
         returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                     "Required field \"Show All Verbs :\" missing");      

      
      
        // Begin Step 11 - Read in Introduction Graphic
      returnedString =
         parseMultiLines(lineArray, numLines, currentLine, "Image Loading Graphic :", "Introduction Graphic :", ":");
      if (returnedString != null)
         gameInfo.ImageLoading_GraphicURL = returnedString;
      else
         returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" +
                     "Required field \"Introduction Graphic :\" missing");

        // Begin Step 11 - Read in Introduction Graphic
      returnedString =
         parseMultiLines(lineArray, numLines, currentLine, "Introduction Graphic :", "Introduction (Text) :", ":");
      if (returnedString != null)
         gameInfo.Introduction_GraphicURL = returnedString;
      else
         returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" +
                     "Required field \"Introduction Graphic :\" missing");


      // Begin Step 12 - Read in Introduction (Text)
      returnedString =
         parseMultiLines(lineArray, numLines, currentLine, "Introduction (Text) :", "", ":");
      if (returnedString != null)
         gameInfo.Introduction_Text = returnedString;
      else
         returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                     "Required field \"Introduction (Text) :\" missing");

		// Now begin reading in Layout Defaults

      numLines = 0;
      currentLine[0] = 1;
      
      do {   // Move past Layout header  
         returnedString = InfoStream.readLine();
         CurrentStreamLine++;
      }
      while (!returnedString.trim().startsWith("---------------"));        
      
      do {    // Eliminate blank lines before fields start
         returnedString = InfoStream.readLine();
         CurrentStreamLine++;
      }
      while ( returnedString.trim().equals("") );
       
      ctr = 1;
      while ( (returnedString != null) && !(returnedString.trim().equals("")) ) {   // Now read in complete info data
         lineArray[ctr] = returnedString;
         ctr++;
         numLines++;
         returnedString = InfoStream.readLine();
         CurrentStreamLine++;
      }

		// Read in Preferred Room Graphic Dimensions (x,y) :
      returnedString =
         parseMultiLines(lineArray, numLines, currentLine, "Preferred Room Graphic Dimensions (x,y) :", "Show Statistal Display :", ":");
      try {
         if (returnedString != null) {
            StringTokenizer numTokens = new StringTokenizer(returnedString, ",");
            gameInfo.PreferredGraphicSizeX = Integer.parseInt(numTokens.nextToken().trim());
            gameInfo.PreferredGraphicSizeY = Integer.parseInt(numTokens.nextToken().trim());
         }
         else
            returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                        "Required field \"Preferred Room Graphic Dimensions (x,y) :\" missing");
      } catch(NumberFormatException error) {
              returnError("Error around line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                          "A number could not be properly parsed.\n" + "This may mean a required field is missing");
        }

		// Read in Statistal Display
      returnedString =
         parseMultiLines(lineArray, numLines, currentLine, "Show Statistal Display :", "Show Inventory Display :", ":");
      if (returnedString != null) {
         if(returnedString.equals("true"))
            gameInfo.ShowStats = true;
         else if(returnedString.equals("false"))
            gameInfo.ShowStats = false;
      }         
      else
         returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                     "Required field \"Show Statistal Display :\" missing");
  
		// Read in Inventory Display
      returnedString =
         parseMultiLines(lineArray, numLines, currentLine, "Show Inventory Display :", "Show Command Line :", ":");
      if (returnedString != null) {
         if(returnedString.equals("true"))
            gameInfo.ShowInventory = true;
         else if(returnedString.equals("false"))
            gameInfo.ShowInventory = false;
      }         
      else
         returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                     "Required field \"Show Inventory Display :\" missing"); 

		// Read in Command Line Display
      returnedString =
         parseMultiLines(lineArray, numLines, currentLine, "Show Command Line :", "Show Compass :", ":");
      if (returnedString != null) {
         if(returnedString.equals("true"))
            gameInfo.ShowCommandLine = true;
         else if(returnedString.equals("false"))
            gameInfo.ShowCommandLine = false;
      }         
      else
         returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                     "Required field \"Show Command Line :\" missing"); 

		// Read in Compass Display
      returnedString =
         parseMultiLines(lineArray, numLines, currentLine, "Show Compass :", "Menu Button Graphic URL :" +
						"Center Button Indicates Items :", ":");
      if (returnedString != null) {
         if(returnedString.equals("true"))
            gameInfo.ShowCompass = true;
         else if(returnedString.equals("false"))
            gameInfo.ShowCompass = false;
      }
      else
         returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" +
                     "Required field \"Show Compass :\" missing");

		// Begin Step 4 - Read in CompassGraphicURL [Available]
			returnedString =
				parseMultiLines(lineArray, numLines, currentLine, "Menu Button Graphic URL :", "Center Button Indicates Items :", ":");

			if(returnedString != null)
				gameInfo.MenuButton_GraphicURL = returnedString;

		// Read in CenterButtonIndicates Items Preference
      returnedString =
         parseMultiLines(lineArray, numLines, currentLine, "Center Button Indicates Items :", "Load All Compass Images :", ":");
      if (returnedString != null) {
         if(returnedString.equals("true"))
            gameInfo.CenterButtonIndicatesItems = true;
         else if(returnedString.equals("false"))
            gameInfo.CenterButtonIndicatesItems = false;
      }
      else
         returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" +
                     "Required field \"Center Button Indicates Items :\" missing");

		// Read in CenterButtonIndicates Items Preference
      returnedString =
         parseMultiLines(lineArray, numLines, currentLine, "Load All Compass Images :", "", ":");
      if (returnedString != null) {
         if(returnedString.equals("true"))
            gameInfo.LoadAllCompassImages = true;
         else if(returnedString.equals("false"))
            gameInfo.CenterButtonIndicatesItems = false;
      }
      else
         returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" +
                     "Required field \"Load All Compass Images :\" missing");


      // Now begin reading in Player Defaults

      numLines = 0;
      currentLine[0] = 1;
      
      do {                                                                     // Move past player header  
         returnedString = InfoStream.readLine();
         CurrentStreamLine++;
      }
      while (!returnedString.trim().startsWith("---------------"));        
      
      do {                                               // Eliminate blank lines before fields start
         returnedString = InfoStream.readLine();
         CurrentStreamLine++;
      }
      while ( returnedString.trim().equals("") );
       
      ctr = 1;
      while ( (returnedString != null) && !(returnedString.trim().equals("")) ) {   // Now read in complete info data
         lineArray[ctr] = returnedString;
         ctr++;
         numLines++;
         returnedString = InfoStream.readLine();
         CurrentStreamLine++;
      }
                          
      try { //// This will catch any Invalid numbers entered in Steps 1 - 10

      // Begin Step 1 - Read in Name
      returnedString =
         parseMultiLines(lineArray, numLines, currentLine, "Name :", "Initial Room # :", ":");
      if (returnedString != null)
         player.Name = returnedString;
      else
         returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                     "Required field \"Name :\" missing");

      // Begin Step 2 - Read in Initial Room #
      returnedString =
         parseMultiLines(lineArray, numLines, currentLine, "Initial Room # :", "Initial Inventory Items :", ":");
      if (returnedString != null)
         initialRoom = Integer.parseInt(returnedString);
      else
         returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                     "Required field \"Initial Room # :\" missing");
      

      // Begin Step 3 - Read in Initial Inventory Items
      player.Items = new boolean[gameInfo.TotalItems + 1];
      returnedString =
         parseMultiLines(lineArray, numLines, currentLine, "Initial Inventory Items :", "Experience :", ":");
      // Read in the item numbers in the format of numbers example: 6, 7, 4
      if (returnedString != null) {
         if(!returnedString.trim().equals("")) {
            StringTokenizer itemNumber = new StringTokenizer(returnedString, ",");
            while(itemNumber.hasMoreTokens()) {
               player.Items[Integer.parseInt(itemNumber.nextToken().trim())] = true;
            }
         }
      }
      else
         returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                     "Required field \"Initial Inventory Items :\" missing");

      // Begin Step 4 - Read in Experience
      returnedString =
         parseMultiLines(lineArray, numLines, currentLine, "Experience :", "Health Points (HP) :", ":");
      if (returnedString != null)
         player.Exp = Integer.parseInt(returnedString);
      else
         returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                     "Required field \"Experience :\" missing");

      // Begin Step 5 - Read in Health Points (HP)
      returnedString =
         parseMultiLines(lineArray, numLines, currentLine, "Health Points (HP) :", "Magic Points (MP) :", ":");
      if (returnedString != null)
         player.HP = Integer.parseInt(returnedString);
      else
         returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                     "Required field \"Health Points (HP) :\" missing");

      // Begin Step 6 - Read in Magic Points (MP)
      returnedString =
         parseMultiLines(lineArray, numLines, currentLine, "Magic Points (MP) :", "Strength (Str) :", ":");
      if (returnedString != null)
         player.MP = Integer.parseInt(returnedString);
      else
         returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                     "Required field \"Magic Points (MP) :\" missing");

      // Begin Step 7 - Read in Strength (Str)
      returnedString =
         parseMultiLines(lineArray, numLines, currentLine, "Strength (Str) :", "Intelligence :", ":");
      if (returnedString != null)
         player.Str = Integer.parseInt(returnedString);
      else
         returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                     "Required field \"Strength (Str) :\" missing");
      
      // Begin Step 8 - Read in Intelligence
      returnedString =
         parseMultiLines(lineArray, numLines, currentLine, "Intelligence :", "Armor Level :", ":");
      if (returnedString != null)
         player.IQ = Integer.parseInt(returnedString);
      else
         returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                     "Required field \"Intelligence :\" missing");

      // Begin Step 9 - Read in Armor Level
      returnedString =
         parseMultiLines(lineArray, numLines, currentLine, "Armor Level :", "Max Weight :", ":");
      if (returnedString != null)
         player.Armor_Level = Integer.parseInt(returnedString);
      else
         returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                     "Required field \"Armor Level :\" missing");

      // Begin Step 10 - Read in Max Weight
      returnedString =
         parseMultiLines(lineArray, numLines, currentLine, "Max Weight :", "Max Bulk :", ":");
      if (returnedString != null)
         player.Max_Weight = Integer.parseInt(returnedString);
      else
         returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                     "Required field \"Max Weight :\" missing");
      } catch(NumberFormatException error) {
              returnError("Error around line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                          "A number could not be properly parsed.\n" + "This may mean a required field is missing");
       }

      // Begin Step 11 - Read in Max Bulk
      returnedString =
         parseMultiLines(lineArray, numLines, currentLine, "Max Bulk :", "", ":");
      try {
         if (returnedString != null)
            player.Max_Bulk = Integer.parseInt(returnedString);
         else
            returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                        "Required field \"Max Bulk :\" missing");
      } catch(NumberFormatException error) {
              returnError("Error around line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                          "A number could not be properly parsed.\n" + "This may mean a required field is missing");
       }
   }

   void parseVerbsFile(VerbOBJ verbArray[], GameInfoOBJ gameInfo) throws IOException {

      String lineArray[] = new String[512];
      int numLines = 0;  
      int currentLine[] = {0}; // This is only an array so it can be passed to a method and changed in the method
      String returnedString;
   
      gameInfo.VerbHeaderNotes = skipComments(VerbStream, "---------------");
      
      for (int currentVerb = 1; currentVerb <= gameInfo.TotalVerbs; currentVerb++) {

         verbArray[currentVerb] = new VerbOBJ();
         numLines = 0;
         currentLine[0] = 1;
                  
         do {                                            // Eliminate blank lines between Verbs
            returnedString = VerbStream.readLine();
         }
         while ( returnedString.trim().equals("") );
          
         int ctr = 1;
         while ( (returnedString != null) && !(returnedString.trim().equals("")) ) {   // Now read in one complete verb to lineArray
            lineArray[ctr] = returnedString;
            ctr++;
            numLines++;
            returnedString = VerbStream.readLine();            
         }
      
         // Begin Step 1 - Read in Verb Number
         returnedString =
            parseMultiLines(lineArray, numLines, currentLine, "Verb # :", "Verb Name :", ":");
         try {
            if(returnedString != null)
               verbArray[currentVerb].Number = Integer.parseInt(returnedString);
            else
               returnError("Error on line: " + (VerbStream.getLineNumber() - (numLines - currentLine[0])) + "\n" + 
                           "Required field \"Verb # :\" missing");
         } catch(NumberFormatException error) {
              returnError("Error around line: " + (VerbStream.getLineNumber() - (numLines - currentLine[0])) + "\n" + 
                          "A number could not be properly parsed.\n" + "This may mean a required field is missing");
           }

         if (verbArray[currentVerb].Number != currentVerb) 
            returnError("Error on line: " + (VerbStream.getLineNumber() - (numLines - currentLine[0])) + "\n" +    
                        "Verb #" + currentVerb + " is missing from verb's file.");
           
         // Begin Step 2 - Read in Verb Name
         returnedString =
            parseMultiLines(lineArray, numLines, currentLine, "Verb Name :", "Aliases :", ":");
       
            if(returnedString != null)
               verbArray[currentVerb].Name = returnedString;
            else
               returnError("Error on line: " + (VerbStream.getLineNumber() - (numLines - currentLine[0])) + "\n" + 
                           "Required field \"Verb Name :\" missing");
        
         // Begin Step 3 - Read in Aliases
         returnedString =
            parseMultiLines(lineArray, numLines, currentLine, "Aliases :", "", ":");
       
            if(returnedString != null)
               verbArray[currentVerb].Aliases = returnedString;
      }
   }   
   
   void parseDirectionsFile(DirectionInfoOBJ directionArray[], GameInfoOBJ gameInfo) throws IOException {

      String lineArray[] = new String[512];
      int numLines = 0;  
      int currentLine[] = {0}; // This is only an array so it can be passed to a method and changed in the method
      String returnedString;
      CurrentStreamLine = 0;

      gameInfo.DirectionsHeaderNotes = skipComments(DirectionsStream, "---------------");

      for (int currentDirection = 1; currentDirection <= gameInfo.TotalDirections; currentDirection++) {

         directionArray[currentDirection] = new DirectionInfoOBJ();
         numLines = 0;
         currentLine[0] = 1;
                  
         do {                                            // Eliminate blank lines between Directions
            returnedString = DirectionsStream.readLine();
         }
         while ( returnedString.trim().equals("") );
          
         int ctr = 1;
         while ( (returnedString != null) && !(returnedString.trim().equals("")) ) {   // Now read in one complete verb to lineArray
            lineArray[ctr] = returnedString;
            ctr++;
            numLines++;
            returnedString = DirectionsStream.readLine();            
         }
      
         // Begin Step 1 - Read in Direction Number
         returnedString =
            parseMultiLines(lineArray, numLines, currentLine, "Direction # :", "Direction Name :", ":");
         try {
            if(returnedString != null)
               directionArray[currentDirection].Number = Integer.parseInt(returnedString);
            else
               returnError("Error on line: " + (DirectionsStream.getLineNumber() - (numLines - currentLine[0])) + "\n" + 
                           "Required field \"Direction # :\" missing");
         } catch(NumberFormatException error) {
              returnError("Error around line: " + (DirectionsStream.getLineNumber() - (numLines - currentLine[0])) + "\n" + 
                          "A number could not be properly parsed.\n" + "This may mean a required field is missing");
           }

         if (directionArray[currentDirection].Number != currentDirection) 
            returnError("Error on line: " + (DirectionsStream.getLineNumber() - (numLines - currentLine[0])) + "\n" +    
                        "Direction #" + currentDirection + " is missing from Directions file.");
           
         // Begin Step 2 - Read in Direction Name
         returnedString =
            parseMultiLines(lineArray, numLines, currentLine, "Direction Name :", "Direction Abbreviation :", ":");
       
            if(returnedString != null)
               directionArray[currentDirection].Name = returnedString;
            else
               returnError("Error on line: " + (DirectionsStream.getLineNumber() - (numLines - currentLine[0])) + "\n" + 
                           "Required field \"Direction Name :\" missing");
        
         // Begin Step 3 - Read in Direction Abbreviation 
         returnedString =
            parseMultiLines(lineArray, numLines, currentLine, "Direction Abbreviation :", "CompassGraphicURL [Available] :", ":");
       
            if(returnedString != null)
               directionArray[currentDirection].Abbreviation = returnedString;

         // Begin Step 4 - Read in CompassGraphicURL [Available]
         returnedString =
            parseMultiLines(lineArray, numLines, currentLine, "CompassGraphicURL [Available] :", "CompassGraphicURL [Unavailable] :", ":");

            if(returnedString != null)
               directionArray[currentDirection].CG_AvailableURL = returnedString;

         // Begin Step 5 - Read in CompassGraphicURL [Unavailable] 
         returnedString =
            parseMultiLines(lineArray, numLines, currentLine, "CompassGraphicURL [Unavailable] :", "CompassGraphicURL [Special] :", ":");
       
            if(returnedString != null)
               directionArray[currentDirection].CG_UnavailableURL = returnedString;

         // Begin Step 6 - Read in CompassGraphicURL [Special]
         returnedString =
            parseMultiLines(lineArray, numLines, currentLine, "CompassGraphicURL [Special] :", "", ":");
       
            if(returnedString != null)
               directionArray[currentDirection].CG_SpecialURL = returnedString;
      }

   }

   void parseRoomsFile(RoomOBJ roomArray[], GameInfoOBJ gameInfo, DirectionInfoOBJ directionArray[]) throws IOException {
            
      String lineArray[] = new String[512];
      int numLines = 0;  
      int currentLine[] = {0}; // This is only an array so it can be passed to a method and changed in the method
      String returnedString;
      CurrentStreamLine = 0;

      gameInfo.RoomHeaderNotes = skipComments(RoomStream, "---------------");
      
      for (int currentRoom = 1; currentRoom <= gameInfo.TotalRooms; currentRoom++) {
         
         roomArray[currentRoom] = new RoomOBJ();

			roomArray[currentRoom].DirectionArray = new DirectionOBJ[gameInfo.TotalDirections + 1];

         numLines = 0;
         currentLine[0] = 1;																					   
                  
         do {                                            // Eliminate blank lines between Rooms
            returnedString = RoomStream.readLine();
            CurrentStreamLine++;
         }
         while ( returnedString.trim().equals("") );
          
         int ctr = 1;
         while ( (returnedString != null) && !(returnedString.trim().equals("")) ) {   // Now read in one complete room to lineArray
            lineArray[ctr] = returnedString;
            ctr++;
            numLines++;
            returnedString = RoomStream.readLine();
            CurrentStreamLine++;
         }
         
         // Set Room visited to false for every room
         roomArray[currentRoom].Visited = false;

         // Begin Step 1 - Read in Room #
         returnedString = 
            parseMultiLines(lineArray, numLines, currentLine, "Room # :", "Room Name :" + "GraphicURL :" +
                            "Text Description (Long) :" + "Text Description (Short) :" + "Direction Description :" +
                            "Directions :", ":");
         try {
            if(returnedString != null)
               roomArray[currentRoom].Number = Integer.parseInt(returnedString);
            else
               returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                           "Required field \"Room # :\" missing");
         } catch(NumberFormatException error) {
              returnError("Error around line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                          "A number could not be properly parsed.\n" + "This may mean a required field is missing");
           }


         if (roomArray[currentRoom].Number != currentRoom) 
            returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" +    
                        "Room #" + currentRoom + " is missing from room's file.");
          
         // Begin Step 2 - Read in Room Name
         returnedString =
            parseMultiLines(lineArray, numLines, currentLine, "Room Name :", "GraphicURL :" + 
                            "Text Description (Long) :", ":");
         if(returnedString != null)
            roomArray[currentRoom].Name = returnedString;
         else
            returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                        "Required field \"Room Name :\" missing");
         boolean hasGraphicURL = false;
         int descriptionsCtr = 0;
         
         // Begin Step 3 - Read in GraphicURL
         returnedString =
            parseMultiLines(lineArray, numLines, currentLine, "GraphicURL :", "Text Description (Long) :" + 
                       "Text Description (Short) :" + "Direction Description :" + "Directions :", ":");
         if(returnedString != null) {
            roomArray[currentRoom].GraphicURL = returnedString;
            hasGraphicURL = true;
         }

         // Begin Step 4 - Read in Text Description (Long)
         returnedString =
            parseMultiLines(lineArray, numLines, currentLine, "Text Description (Long) :", 
                            "Text Description (Short) :" + "Direction Description :" + "Directions :", ":");
         if(returnedString != null) {
            roomArray[currentRoom].Description_Long = returnedString;
            descriptionsCtr++;
         }
         
         // Begin Step 5 - Read in Text Description (Short)
         returnedString =
            parseMultiLines(lineArray, numLines, currentLine, "Text Description (Short) :",
                            "Direction Description :" + "Directions :", ":");
         if(returnedString != null) {
            roomArray[currentRoom].Description_Short = returnedString;
            descriptionsCtr++;
         }
         
         // Begin Step 6 - Read in Direction Description
         returnedString =
            parseMultiLines(lineArray, numLines, currentLine, "Direction Description :", "Directions :" , ":");
         if(returnedString != null) {
            roomArray[currentRoom].Direction_Description = returnedString;
            descriptionsCtr++;
         }
         
         // Now determine whether the proper number of description fields have been entered
         if (hasGraphicURL && (descriptionsCtr > 0)) {
            if (descriptionsCtr < 3)
               returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                           "You must enter all 3 Description fields or no Description fields");
         }
         if (!hasGraphicURL && (descriptionsCtr < 3)) {
            returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                        "You must enter all 3 Description fields");
         }
                    
         // Begin Step 7 - Read in Directions
         returnedString =
            parseMultiLines(lineArray, numLines, currentLine, "Directions :",
                               "Items :" + "Directional Object :" + "Notes :", ":");
         if(returnedString != null) {
            StringTokenizer dirToken = new StringTokenizer(returnedString, ",");
            
            while (dirToken.hasMoreElements()) {
               StringTokenizer cardToken = new StringTokenizer(dirToken.nextToken().trim(), "(", true);   
               String direction = cardToken.nextToken().trim();
               cardToken.nextToken();
               String toRoom = cardToken.nextToken(")").trim();
               int dirNum = enumerateDirection(direction, directionArray);
               if(dirNum == 0)
                  returnError("Invalid direction \"" + direction + "\" entered on line " + CurrentStreamLine);   
               roomArray[currentRoom].DirectionArray[dirNum] = new DirectionOBJ();
               try {
                  roomArray[currentRoom].DirectionArray[dirNum].ToWhichRoom = Integer.parseInt(toRoom);
               } catch(NumberFormatException error) {
                    returnError("Error around line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                                "A number could not be properly parsed.\n" + "This may mean a required field is missing");
                 }
            }
         }
         else if (returnedString == null) {
            returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                        "Required field \"Directions :\" missing");
         }
            
         // Begin Step 8 - Read in Items
         returnedString =
               parseMultiLines(lineArray, numLines, currentLine, "Items :", 
                               "Directional Object :" + "Notes :", ":");
         if(returnedString != null)
            roomArray[currentRoom].Items = returnedString;         
                
         // Begin Step 9 - Read in Directional Objects
         while((currentLine[0] <= numLines) && lineArray[currentLine[0]].trim().startsWith("Directional Object :")) {
            boolean fieldsAssigned = false;   
            
            returnedString =
               parseMultiLines(lineArray, numLines, currentLine, "Directional Object :", 
                               "Obstruction :" + "Transition (Text) :" + "First Transition (Text) :" + 
                               "Transition (Graphic) :" + "First Transition (Graphic) :" +
                               "Directional Object :" + "Notes :", ":");
            
            int dirNum = enumerateDirection(returnedString, directionArray);
            if (dirNum == 0)
               returnError("Invalid direction \"" + returnedString + "\" entered on line " + CurrentStreamLine);
            if(roomArray[currentRoom].DirectionArray[dirNum] == null) {
               roomArray[currentRoom].DirectionArray[dirNum] = new DirectionOBJ();
//	            int dirNum = enumerateDirection(returnedString, directionArray);
//		         if (dirNum == 0)
//	               returnError("Invalid direction \"" + returnedString + "\" entered on line " + CurrentStreamLine);
//             returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
//                         "You have assigned a directional object for a non-listed direction");
				}

            // Read in Obstruction
            returnedString =
               parseMultiLines(lineArray, numLines, currentLine, "Obstruction :",
                               "Transition (Text) :" + "First Transition (Text) :" + "Transition (Graphic) :" +
                               "First Transition (Graphic) :" + "Directional Object :" + "Notes :", ":");
            if(returnedString != null) {
               roomArray[currentRoom].DirectionArray[dirNum].Obstructions = returnedString;
               fieldsAssigned = true;
            }
            
            // Read in Transition (Text)
            returnedString =
               parseMultiLines(lineArray, numLines, currentLine, "Transition (Text) :",
                               "First Transition (Text) :" + "Transition (Graphic) :" + 
                               "First Transition (Graphic) :" + "Directional Object :" + "Notes :", ":");
            if(returnedString != null) {
               roomArray[currentRoom].DirectionArray[dirNum].TransitionText = returnedString;
               fieldsAssigned = true;
            }
             
            // Read in First Transition (Text)
            returnedString =
               parseMultiLines(lineArray, numLines, currentLine, "First Transition (Text) :",
                               "Transition (Graphic) :" + "First Transition (Graphic) :" + 
                               "Directional Object :" + "Notes :", ":");
            if(returnedString != null) {
               roomArray[currentRoom].DirectionArray[dirNum].FirstTransitionText = returnedString;
               fieldsAssigned = true;
            }
            
            // Read in Transition (Graphic)
            returnedString =
               parseMultiLines(lineArray, numLines, currentLine, "Transition (Graphic) :",
                               "First Transition (Graphic) :" + "Directional Object :" + "Notes :", ":");
            if(returnedString != null) {
               roomArray[currentRoom].DirectionArray[dirNum].TransitionGraphic = returnedString;
               fieldsAssigned = true;
            }
            
            // Read in First Transition (Graphic)
            returnedString =
               parseMultiLines(lineArray, numLines, currentLine, "First Transition (Graphic) :",
                               "Directional Object :" + "Notes :", ":");
            if(returnedString != null) {
               roomArray[currentRoom].DirectionArray[dirNum].FirstTransitionGraphic = returnedString;          
               fieldsAssigned = true;
            }
         
            if(fieldsAssigned == false) {
               returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                           "You must enter at least one field for a Directional Object");
            }               
         }                               
        
         // Begin Step 10 - Read in Notes
         returnedString = 
            parseMultiLines(lineArray, numLines, currentLine, "Notes :", "", ":");
         
         if(returnedString != null)
            roomArray[currentRoom].Notes = returnedString;         
      }      
   }

   void parseItemsFile(ItemOBJ itemArray[], GameInfoOBJ gameInfo) throws IOException {

      String lineArray[] = new String[512];
      int numLines = 0;  
      int currentLine[] = {0}; // This is only an array so it can be passed to a method and changed in the method
      
      String returnedString;
      CurrentStreamLine = 0;

      gameInfo.ItemHeaderNotes = skipComments(ItemStream, "---------------");
      
      for (int currentItem = 1; currentItem <= gameInfo.TotalItems; currentItem++) {
         
         itemArray[currentItem] = new ItemOBJ();
         numLines = 0;
         currentLine[0] = 1;
                  
         do {                                            // Eliminate blank lines between Items
            returnedString = ItemStream.readLine();
            CurrentStreamLine++;
         }
         while ( returnedString.trim().equals("") );
          
         int ctr = 1;
         while ( (returnedString != null) && !(returnedString.trim().equals("")) ) {   // Now read in one complete item to lineArray
            lineArray[ctr] = returnedString;
            ctr++;
            numLines++;
            returnedString = ItemStream.readLine();
            CurrentStreamLine++;
         }

         // Step 1 - Read in Item #
         returnedString = 
            parseMultiLines(lineArray, numLines, currentLine, "Item # :", "Item Name :" + "Aliases :" + 
                            "Environment GraphicURL :" + "Environment Graphic Coordinates (X,Y) :" + 
                            "CloseUp GraphicURL :" + "Icon GraphicURL :" + "Equipped GraphicURL :" + 
                            "Text Description :", ":");
         try {
            if(returnedString != null)
               itemArray[currentItem].Number = Integer.parseInt(returnedString);
            else
               returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                           "Required field \"Item # :\" missing");
         } catch(NumberFormatException error) {
              returnError("Error around line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                          "A number could not be properly parsed.\n" + "This may mean a required field is missing");
           }
                  
         if (itemArray[currentItem].Number != currentItem) 
            returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" +    
                        "Item #" + currentItem + " is missing from item's file.");

         // Step 2 - Read in Item Name
         returnedString = 
            parseMultiLines(lineArray, numLines, currentLine, "Item Name :", "Aliases :" + 
                            "Environment GraphicURL :" + "Environment Graphic Coordinates (X,Y) :" + 
                            "CloseUp GraphicURL :" + "Icon GraphicURL :" + "Equipped GraphicURL :" + 
                            "Text Description :", ":");
         if(returnedString != null)
            itemArray[currentItem].Name = returnedString;
         else
            returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                        "Required field \"Item Name :\" missing");
         
         // Step 3 - Read in Aliases
         returnedString = 
            parseMultiLines(lineArray, numLines, currentLine, "Aliases :", "Environment GraphicURL :" + 
                            "Environment Graphic Coordinates (X,Y) :" + 
                            "CloseUp GraphicURL :" + "Icon GraphicURL :" + "Equipped GraphicURL :" + 
                            "Text Description :", ":");
         if(returnedString != null)
            itemArray[currentItem].Aliases = returnedString;
         
         // Step 4 - Read in Environment GraphicURL
         returnedString = 
            parseMultiLines(lineArray, numLines, currentLine, "Environment GraphicURL :",
                            "Environment Graphic Coordinates (X,Y) :", ":");
         if(returnedString != null) {
            itemArray[currentItem].Environment_GraphicURL = returnedString;            
         }

         // Step 5 - Read in Environment Graphic Coordinates (X,Y)
         returnedString =
            parseMultiLines(lineArray, numLines, currentLine, "Environment Graphic Coordinates (X,Y) :", 
                            "CloseUp GraphicURL :" + "Icon GraphicURL :" + "Equipped GraphicURL :" + 
                            "Text Description :" + "Location :" + "Weight :" + "Bulk :" + "Notes :" + "Usage :", ":");
         if(returnedString != null) {
            StringTokenizer posToken = new StringTokenizer(returnedString, ",");
            try {        
               itemArray[currentItem].Environment_Graphic_Xpos = Integer.parseInt(posToken.nextToken().trim());            
               itemArray[currentItem].Environment_Graphic_Ypos = Integer.parseInt(posToken.nextToken().trim());
            } catch(NumberFormatException error) {
                 returnError("Error around line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                             "A number could not be properly parsed.\n" + "This may mean a required field is missing");
              }

         }
         else if(returnedString == null) {
            if (itemArray[currentItem].Environment_GraphicURL != null)
               returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                           "Required field \"Environment Graphic Coordinates (X,Y) :\" missing");
         }

         // Step 6 - Read in CloseUp GraphicURL
         returnedString =
            parseMultiLines(lineArray, numLines, currentLine, "CloseUp GraphicURL :", "Icon GraphicURL :" + "Equipped GraphicURL :" + 
                            "Text Description :" + "Location :" + "Weight :" + "Bulk :" + "Notes :" + "Usage :", ":");
         if(returnedString != null)
            itemArray[currentItem].CloseUp_GraphicURL = returnedString; 
   
         // Step 7 - Read in Icon GraphicURL
         returnedString =
            parseMultiLines(lineArray, numLines, currentLine, "Icon GraphicURL :", "Equipped GraphicURL :" + 
                            "Text Description :" + "Location :" + "Weight :" + "Bulk :" + "Notes :" + "Usage :", ":");
         if(returnedString != null)
            itemArray[currentItem].Icon_GraphicURL = returnedString;

         // Step 8 - Read in Equipped GraphicURL
         returnedString =
            parseMultiLines(lineArray, numLines, currentLine, "Equipped GraphicURL :", "Text Description :" + 
                            "Location :" + "Weight :" + "Bulk :" + "Notes :" + "Usage :", ":");
         if(returnedString != null)
            itemArray[currentItem].Equipped_GraphicURL = returnedString;

         // Step 9 - Read in Text Description
         returnedString =
            parseMultiLines(lineArray, numLines, currentLine, "Text Description :",
            "Location :" + "Weight :" + "Bulk :" + "Notes :" + "Usage :", ":");
         if(returnedString != null)
            itemArray[currentItem].Description = returnedString;
                      
         if((itemArray[currentItem].Description == null) && (itemArray[currentItem].Environment_GraphicURL == null))
            returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                        "You must enter at least GraphicURL or Text Description");
         
         // Step 10 - Read in Location
         returnedString =
            parseMultiLines(lineArray, numLines, currentLine, "Location :", 
                            "Weight :" + "Bulk :" + "Notes :" + "Usage :", ":");
         if(returnedString != null)
            itemArray[currentItem].Location = returnedString;
         else
            itemArray[currentItem].Location = "0";
                      
         // Step 11 - Read in Weight
         returnedString =
            parseMultiLines(lineArray, numLines, currentLine, "Weight :", "Bulk :" + "Notes :" + "Usage :", ":");
         try {   
            if(returnedString != null)
               itemArray[currentItem].Weight = Integer.parseInt(returnedString);
         } catch(NumberFormatException error) {
              returnError("Error around line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                          "A number could not be properly parsed.\n" + "This may mean a required field is missing");
           }

         // Step 11 - Read in Bulk
         returnedString =
            parseMultiLines(lineArray, numLines, currentLine, "Bulk :", "Notes :" + "Usage :", ":");
         try {
            if(returnedString != null)
               itemArray[currentItem].Bulk = Integer.parseInt(returnedString);
         } catch(NumberFormatException error) {
              returnError("Error around line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                          "A number could not be properly parsed.\n" + "This may mean a required field is missing");
           }
            
         // Step 12 - Read in Notes and Usage
         returnedString = 
            parseMultiLines(lineArray, numLines, currentLine, "Notes :", "Usage :", ":");
         if(returnedString != null) 
            itemArray[currentItem].Notes = returnedString;

         returnedString = 
            parseMultiLines(lineArray, numLines, currentLine, "Usage :", "Notes :", ":");
         if(returnedString != null) {
            if(itemArray[currentItem].Notes == null) 
               itemArray[currentItem].Notes = returnedString;
            else
               itemArray[currentItem].Notes += ("\nUsage: " + returnedString);   
         }   
      }   
   }
       
   void parseObstructionFile(ObstructionOBJ obstructionArray[], GameInfoOBJ gameInfo) throws IOException {
   
      String lineArray[] = new String[512];
      int numLines = 0;  
      int currentLine[] = {0}; // This is only an array so it can be passed to a method and changed in the method
      
      String returnedString;
      CurrentStreamLine = 0;

      gameInfo.ObstructionHeaderNotes = skipComments(ObstructionStream, "---------------");
      
      for (int currentObstruction = 1; currentObstruction <= gameInfo.TotalObstructions; currentObstruction++) {
         
         obstructionArray[currentObstruction] = new ObstructionOBJ();
         numLines = 0;
         currentLine[0] = 1;
                  
         do {   // Eliminate blank lines between Obstructions
            returnedString = ObstructionStream.readLine();
            CurrentStreamLine++;
         }
         while ( returnedString.trim().equals("") );
          
         int ctr = 1;
         while ( (returnedString != null) && !(returnedString.trim().equals("")) ) {   // Now read in one complete obstruction to lineArray
            lineArray[ctr] = returnedString;
            ctr++;
            numLines++;
            returnedString = ObstructionStream.readLine();
            CurrentStreamLine++;
         }
                 
         // Step 1 - Read in Obstruction #
         returnedString = 
            parseMultiLines(lineArray, numLines, currentLine, "Obstruction # :", "Obstruction Name :" + "Aliases :" +
                            "Environment GraphicURL :" + "Environment Graphic Coordinates (X,Y) :" +
                            "CloseUp GraphicURL :" + "Text Description :", ":");
         try {
            if(returnedString != null)
               obstructionArray[currentObstruction].Number = Integer.parseInt(returnedString);
            else
               returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                           "Required field \"Obstruction # :\" missing");
         } catch(NumberFormatException error) {
              returnError("Error around line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                          "A number could not be properly parsed.\n" + "This may mean a required field is missing");
         }

         // Make sure all Obstructions appear in order sequentially
         if (obstructionArray[currentObstruction].Number != currentObstruction) 
            returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" +    
                        "Item #" + currentObstruction + " is missing from item's file.");

         // Step 2 - Read in Obstruction Name
         returnedString = 
            parseMultiLines(lineArray, numLines, currentLine, "Obstruction Name :", "Aliases :" +
                            "Environment GraphicURL :" + "Environment Graphic Coordinates (X,Y) :" +
                            "CloseUp GraphicURL :" + "Text Description :", ":");
         if(returnedString != null)
            obstructionArray[currentObstruction].Name = returnedString;
         else
            returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                        "Required field \"Obstruction Name :\" missing");
         
         // Step 3 - Read in Aliases
         returnedString = 
            parseMultiLines(lineArray, numLines, currentLine, "Aliases :", "Environment GraphicURL :" + 
                            "Environment Graphic Coordinates (X,Y) :" +
                            "CloseUp GraphicURL :" + "Text Description :", ":");
         if(returnedString != null)
            obstructionArray[currentObstruction].Aliases = returnedString;
         
         // Step 4 - Read in Environment GraphicURL
         returnedString = 
            parseMultiLines(lineArray, numLines, currentLine, "Environment GraphicURL :", 
                            "Environment Graphic Coordinates (X,Y) :", ":");
         if(returnedString != null)
            obstructionArray[currentObstruction].Environment_GraphicURL = returnedString;
         
         // Step 5 - Read in Environment Graphic Coordinates (X,Y)
         returnedString = 
            parseMultiLines(lineArray, numLines, currentLine, "Environment Graphic Coordinates (X,Y) :", 
                            "CloseUp GraphicURL :" + "Text Description :" + "Type :" + "Locations :" + "Visible :", ":");
         if(returnedString != null) {
            StringTokenizer posToken = new StringTokenizer(returnedString, ",");
            try {        
               obstructionArray[currentObstruction].Environment_Graphic_Xpos = Integer.parseInt(posToken.nextToken().trim());            
               obstructionArray[currentObstruction].Environment_Graphic_Ypos = Integer.parseInt(posToken.nextToken().trim());
            } catch(NumberFormatException error) {
              returnError("Error around line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                          "A number could not be properly parsed.\n" + "This may mean a required field is missing");
         }
         }
         else {
            if (obstructionArray[currentObstruction].Environment_GraphicURL != null)
               returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                           "Required field \"Initial Graphic Coordinates (X,Y) :\" missing");
         }

         // Step 6 - Read in CloseUp GraphicURL
         returnedString = 
            parseMultiLines(lineArray, numLines, currentLine, "CloseUp GraphicURL :", "Text Description :" +
                            "Type :" + "Locations :" + "Visible :", ":");
         if(returnedString != null)
            obstructionArray[currentObstruction].CloseUp_GraphicURL = returnedString;
         


         // Step 7 - Read in Text Description
         returnedString = 
            parseMultiLines(lineArray, numLines, currentLine, "Text Description :", "Type :" + "Locations :" + "Visible :", ":");
         if(returnedString != null)
            obstructionArray[currentObstruction].Description = returnedString; 
   
         if((obstructionArray[currentObstruction].Description == null) && (obstructionArray[currentObstruction].Environment_GraphicURL == null))
            returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                        "You must enter at least Environment GraphicURL or Text Description");

         // Step 8 - Read in Type 
         returnedString = 
            parseMultiLines(lineArray, numLines, currentLine, "Type :", "Locations :" + "Visible :", ":");
         if(returnedString != null)
            obstructionArray[currentObstruction].Type = returnedString;
         
         // Step 9 - Read in Locations 
         returnedString = 
            parseMultiLines(lineArray, numLines, currentLine, "Locations :", "Visible :", ":");
         if(returnedString != null)
            obstructionArray[currentObstruction].Locations = returnedString;
                  
         // Step 10 - Read in Visible 
         returnedString = 
            parseMultiLines(lineArray, numLines, currentLine, "Visible :", "Notes :", ":");
         if(returnedString != null) {
            if(returnedString.toLowerCase().equals("yes"))          
               obstructionArray[currentObstruction].Visible = true;
            else if(returnedString.toLowerCase().equals("no"))          
               obstructionArray[currentObstruction].Visible = false;
         }
         else 
            returnError("Error on line: " + (CurrentStreamLine - (numLines - currentLine[0])) + "\n" + 
                        "Required field \"Visible :\" missing");

         // Step 11 - Read in Notes 
         returnedString = 
            parseMultiLines(lineArray, numLines, currentLine, "Notes :", "", ":");
         if(returnedString != null)
            obstructionArray[currentObstruction].Notes = returnedString;
      }   
   }
   
   String parseMultiLines(String lineArray[], int numLines, int currentLine[], String beginsWith, String stopAt, 
                          String delim) throws IOException {
      
      String tempStr = "";                // For initialization purposes only
      boolean stopReading = false;        // This will tell whether to stop reading lines
       
      if ((currentLine[0] <= numLines) && lineArray[currentLine[0]].trim().startsWith(beginsWith)) { // Check to see if the current line starts with the proper heading
         // The following code breaks the current line into tokens delimeted by delim
         StringTokenizer token = new StringTokenizer(lineArray[currentLine[0]], delim, true); // Delimeters now count as tokens
         token.nextToken();               // Advance line past 1st token(this should be the field name)
         token.nextToken();               // Advance line past 1st token(this is the actual delimeter)
        
         if(token.hasMoreTokens())
            tempStr = token.nextToken("");   // Now set delimeter to nothing and grab the whole rest of the current line
         else
            tempStr = "";
         currentLine[0]++;                // Advance to the next line
            
         while (!stopReading) {           // Ends only when there are no more lines to be read
            StringTokenizer stopToken = new StringTokenizer(stopAt, delim);
            
            if ((currentLine[0]) > numLines)       // If all the lines available have been read, stop reading
                  stopReading = true;
            else {
               while (stopToken.hasMoreTokens()) { // Else check if the current should be read in or if it is the stop line
                  if ( lineArray[currentLine[0]].trim().startsWith(stopToken.nextToken()) ) { //take out delim later ?????Check for problems
                     stopReading = true;
                     break;                        // Ends early if a match occurs before all stop tokens have been tried
                  }               
               }
            }
            if (!stopReading) {                       // If there are still lines to be read in
               tempStr += lineArray[currentLine[0]];  // Add current line to tempStr
               currentLine[0]++;                      // Advance to next line
            }
         }             
      }
      else {   // Runs only if the current line coming into this method did not start with the proper text (beginsWith)
         return null;
      }
      
      return tempStr.trim(); // Finally return the complete string trimmed  
   }
   
   String skipComments(LineNumberReader stream, String marker) throws IOException {

      int commentMarker = 0;
      String line;
      String comments = "";

      while (commentMarker < 2) {
         line = stream.readLine();
         CurrentStreamLine++;
         
         if (line.startsWith(marker))
            commentMarker++;
      
         if ((commentMarker < 2) && (commentMarker >= 1 )) {
            if (!line.startsWith(marker))   
               comments += (line + "\n");
         }
      }
      return comments;
   }

   int enumerateDirection(String direction, DirectionInfoOBJ directionArray[]) {
   
      boolean FoundDirection = false;
      int DirectionNumber = 0;

      for ( int dirCounter = 1; dirCounter <= directionArray.length - 1; dirCounter++ )
         if ( direction.equalsIgnoreCase( directionArray[dirCounter].Name ) )
            if ( !(FoundDirection) ) {
               FoundDirection = true;
               DirectionNumber = dirCounter;
            }
            else {
               System.out.println("Error! Bad Direction Names!");
               System.out.println("Direction #" + dirCounter + " conflicts with Direction #" + DirectionNumber + "!");
               FoundDirection = false;
               DirectionNumber = 0;
            }

      return(DirectionNumber);
   } //enumerateDirection


   void returnError(String error) {
      System.err.println(error);
      System.err.println("\n\nPlease correct error and try again\n");
      System.exit(1);
   }
} // Main - Text2Cog class

/**	Contributors:
	Dave Sivieri
	Steven M. Castellotti
*/ 
