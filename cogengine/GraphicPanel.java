import java.awt.*;
import java.net.URL;
import java.util.Vector; // Vectors are a cross between an array and a hash table.
                         // objects have a fixed position in the Vector, but new
                         // objects can be dynamically allocated.
import java.util.Enumeration;
import java.applet.Applet;

public class GraphicPanel extends Component {
	
	Image GlobalImage;
	Image newImage;
	URL ImageURL;
	Dimension size;
	Vector ImageLayers;
	ImageVectorEntry TempImageEntry;
	Applet app;
	
	GraphicPanel ( Applet app, URL ImageURL ) {
		setImage( app, ImageURL );
	}

	public void update( Graphics g ) {
		paint(g);
	}

	public void paint( Graphics g ) {
		g.drawImage( GlobalImage, 0, 0, this );		
		if (ImageLayers != null) {
			Enumeration e = ImageLayers.elements();
			while ( e.hasMoreElements() ) {
				TempImageEntry = (ImageVectorEntry)e.nextElement();
				g.drawImage( TempImageEntry.image, TempImageEntry.x, TempImageEntry.y, this );
			}
		}
	}

	public Dimension getPreferredSize() {
		return size;
	}

	public void setImage( Applet app, URL ImageURL ) {
		try {
			newImage = app.getImage(ImageURL);
			this.newImage = newImage;			
			MediaTracker mt = new MediaTracker(this);
			mt.addImage( newImage, 0 );
			mt.waitForAll();		
		}
		catch (Exception e) {
			System.err.println("Error downloading graphic in GraphicPanel!");
			System.err.println("Exception was:\n" + e);
		}
		size = new Dimension ( newImage.getWidth(null), newImage.getHeight(null) );
		setSize( size );
		GlobalImage = newImage;
		ImageLayers = null;
		repaint();	
	}

	public void addImageLayer( Applet app, URL ImageURL, int x, int y ) {
		try {
			newImage = app.getImage(ImageURL);
			MediaTracker mt = new MediaTracker(this);
			mt.addImage( newImage, 0 );
			mt.waitForAll();		
		}
		catch (Exception e) {
			System.err.println("Error downloading graphic in GraphicPanel!");
			System.err.println("Exception was:\n" + e);		
		}
		// Add this Image to the ImageVector
		TempImageEntry = new ImageVectorEntry();
		TempImageEntry.image = newImage;
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