/******************************
The COG Engine
GraphicButton Component
Last Modified on 2000.03.18

		This code is released under the GPL (GNU Public License)
		For more information please refer to http://www.gnu.org/copyleft/gpl.html
		Copyright (2000) Steven M. Castellotti

******************************/

import java.awt.*;
import java.awt.event.*;
import java.net.URL;
import java.applet.*;

public class GraphicButton extends Canvas {

	URL ImageURL;
	Image image;
	boolean pressed = false;
	ActionListener actionListener;
	String actionCommand;

	GraphicButton(Applet app, URL ImageURL) {
		setImage(app, ImageURL);
		enableEvents( AWTEvent.MOUSE_EVENT_MASK );
	}

	public void setImage( Applet app, URL ImageURL ) {
		try {
		  image = app.getImage(ImageURL);
		} catch (Exception e) {
			System.err.println("Error downloading Graphic Button Image!");
		}
		this.image = image;
		MediaTracker mt = new MediaTracker(this);
		mt.addImage( image, 0 );
		try {
			mt.waitForAll();
		} catch (InterruptedException e) {
			System.err.println("Error Caught in GraphicButton!");
		};
		setSize( image.getWidth(null), image.getHeight(null) );
		repaint();
	}

	public void update( Graphics g ) {
		paint(g);
	}

	public void paint( Graphics g ) {
		g.setColor(Color.white);
		setSize( image.getWidth(null), image.getHeight(null) );
		int width = getSize().width, height = getSize().height;
		int offset = pressed ? -2 : 0;  // fake depth
		g.drawImage( image, offset, offset, width, height, this );
		g.draw3DRect(0, 0, width-1, height-1, !pressed);
		g.draw3DRect(1, 1, width-3, height-3, !pressed);
	}

	public Dimension getPreferredSize() {
		return getSize();
	}

	public void processEvent( AWTEvent e ) {
		if ( e.getID() == MouseEvent.MOUSE_PRESSED ) {
			pressed = true;
			repaint();
		}
		else if ( e.getID() == MouseEvent.MOUSE_RELEASED ) {
			pressed = false;
			repaint();
			fireEvent();
		}
		super.processEvent(e);
	}

	public void setActionCommand( String actionCommand ) {
		this.actionCommand = actionCommand;
	}

	public void addActionListener(ActionListener l) {
		actionListener = AWTEventMulticaster.add(actionListener, l);
	}

	public void removeActionListener(ActionListener l) {
		actionListener = AWTEventMulticaster.remove(actionListener, l);
	}

	private void fireEvent() {
		if (actionListener != null) {
			ActionEvent event = new ActionEvent( this,
			ActionEvent.ACTION_PERFORMED, actionCommand );
			actionListener.actionPerformed( event );
		}
	}

} // GraphicButton
