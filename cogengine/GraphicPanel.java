/******************************
The COG Engine
GraphicPanel Component
Last Modified on 2001.09.25

		This code is released under the GPL (GNU Public License)
		For more information please refer to http://www.gnu.org/copyleft/gpl.html
		Copyright (2000) Steven M. Castellotti

******************************/

import java.awt.*;
import java.net.URL;
import java.util.Vector; // Vectors are a cross between an array and a hash table.
                         // objects have a fixed position in the Vector, but new
                         // objects can be dynamically allocated.
import java.util.Enumeration;
import java.applet.Applet;

public class GraphicPanel extends Component implements Runnable {
	
	boolean DebugMode;		
	URL ThreadURL;
	Applet app;
	Image LoadingImage;
	Image GlobalImage;
	Dimension size;
	Vector ImageLayers;      // We use this vector to keep track of all of the
	                         // images that we will draw on top of the room's
	                         // image (images such as items, obstructions, etc.)
	ImageVectorEntry TempImageEntry;
	Thread FetchImageThread;
	boolean DownloadInProgress = false;
	int CurrentImageID = 0;
	MediaTracker tracker;

		
	GraphicPanel ( Applet app, URL InitURL, boolean DebugMode ) {
		this.app = app;
		this.DebugMode = DebugMode;
		LoadingImage = DownloadImage(InitURL, CurrentImageID);
		size = new Dimension ( LoadingImage.getWidth(null), LoadingImage.getHeight(null) );
		setSize( size );
		GlobalImage = LoadingImage;
	}
	
	public Image DownloadImage(URL MyURL, int ID) {
		Image TempImage = null;
		repaint();
		try {
			if (DebugMode)
				System.err.println("Downloading ImageID #" + ID + " - URL: " + MyURL.toString() + " ...");
			TempImage = app.getImage(MyURL);
			tracker = new MediaTracker(this);
			tracker.addImage( TempImage, ID );
			tracker.waitForID( ID );		
			if (DebugMode)
				System.err.println("Download Complete. (Image ID #" + ID + ")");
		}
		catch (Exception e) {
			System.err.println("Error downloading graphic in GraphicPanel!");
			System.err.println("Exception was:\n" + e);
		}
		if (tracker.isErrorID( ID )) {
			System.err.println("Error in Image ID #" + ID);
			TempImage = null;
		}
		return TempImage;
	}
	
	public void run() {
		int MyThreadID = CurrentImageID;
		DownloadInProgress = true;
		Image MyImage = DownloadImage(ThreadURL, CurrentImageID);
		synchronized (this) {
			if (DebugMode)
				System.err.println("(Thread) I entered the synchronized block. MyID - " + MyThreadID + " CurrentID - " + CurrentImageID);
			if ( MyThreadID == CurrentImageID ) {
				DownloadInProgress = false;
				GlobalImage = MyImage;
		  repaint();
		  }
		}
	}
		
	public void update( Graphics g ) {
		paint(g);
	}

	public void paint( Graphics g ) {
		if ( DownloadInProgress ) { // A Thread exists, and it is currenlty downloading
			if (DebugMode)
				System.err.println("GlobalImage is still downloading.");
			GlobalImage = LoadingImage;
		}
		if ( GlobalImage != null) {
			size = new Dimension ( GlobalImage.getWidth(null), GlobalImage.getHeight(null) );
			setSize( size );
			g.drawImage( GlobalImage, 0, 0, this );
			if ( ImageLayers != null && !(DownloadInProgress) ) {
				Enumeration e = ImageLayers.elements();
				while ( e.hasMoreElements() ) {
					TempImageEntry = (ImageVectorEntry)e.nextElement();
					g.drawImage( TempImageEntry.image, TempImageEntry.x, TempImageEntry.y, this );
				}
			}
		}
	} // paint()

	public Dimension getPreferredSize() {
		return size;
	}

	public void setImage( Applet app, URL ThreadURL ) {
		this.app = app;
		this.ThreadURL = ThreadURL;
		CurrentImageID++;
		if (CurrentImageID == 1024) {
		// This section is run whenever we find that the total number of graphic
		// download threads has grown too large. It is highly unlikely that a
		// thread from 1024 calls back would still be running, but just be certain,
		// this block incorporates a mediatracker to wait for that thread to finish
		// downloading. Better safe than sorry, no matter how unlikely the circumstance.
			try {
				tracker.waitForID( 0 );
			} catch (Exception e) {
				System.err.println("Error while waiting for ID #0 in setImage");
			}
			CurrentImageID = 0;
		}
		FetchImageThread = new Thread(this);
		FetchImageThread.start();
		ImageLayers = null;
	}

	public void addImageLayer( Applet app, URL ImageLayerURL, int x, int y ) {
		Image LayerImage = null;
	
		try {
			LayerImage = app.getImage(ImageLayerURL);
			MediaTracker mt = new MediaTracker(this);
			mt.addImage( LayerImage, 0 );
			mt.waitForAll();		
		}
		catch (Exception e) {
			System.err.println("Error downloading graphic in GraphicPanel!");
			System.err.println("Exception was:\n" + e);		
		}
		// Add this Image to the ImageVector
		TempImageEntry = new ImageVectorEntry();
		TempImageEntry.image = LayerImage;
		TempImageEntry.x = x;
		TempImageEntry.y = y;
		if (ImageLayers == null)
			ImageLayers = new Vector();
		ImageLayers.addElement( TempImageEntry );
		repaint();
	}
		
} // GraphicPanel

class ImageVectorEntry {
	Image image;
	int x;
	int y;
}