/**************************
 *   Cog Engine Message Box
 * by Steven M. Castellotti
 *
 * This software is released under the GNU GPL (General Public License)
 * Copyright (2000) Steven M. Castellotti
 *
 *
 * To use this object in your applets/applications make a call to MessageBox
 * in the following format:
 * new MessageBox(this, "This is my text Message", "Message Box Title", wrapLength, fontSize).show();
 *
 * where
 * "This is my Message" gets replaced by the actual String you wish to appear in the MessageBox
 * "Message Box Title" is the title you want set to the Message Box window
 * wrapLength is how many characters wide you want the box set to
 *   (wrapLength may be set to zero if you want there to only be one line, containing your message)
 * fontSize is the size font you want your messag to appear with (I usually use 15)
 */

import java.awt.*;
import java.awt.event.*;
import java.util.StringTokenizer;

public class MessageBox extends Dialog implements ActionListener {

	MessageBox( Frame frame, String message, String title, String fontName, int fontSize ) {
	
		// Set as Modal
		super(frame, true);

		// Set Window Title
		setTitle(title);
		
		// Setup Layout
		setLayout( new GridBagLayout() );
		GridBagConstraints constraints = new GridBagConstraints();
		constraints.anchor = GridBagConstraints.CENTER;	
				
		// Setup Font
		if (fontSize <= 0)
			fontSize = 15;
		setFont ( new Font(fontName,Font.PLAIN,fontSize) );
		
		// Setup Label
		StringTokenizer labelToken = new StringTokenizer( message, "\n" );
		String currentLine;
		constraints.fill = GridBagConstraints.BOTH;
		constraints.weightx = 1.0;
		constraints.weighty = 1.0;
		constraints.gridx = 0;
		int gridy = 0;
						
		while ( labelToken.hasMoreTokens() ) {
			currentLine = labelToken.nextToken().trim();
			constraints.gridy = gridy;
			Label messageLabel = new Label(currentLine, Label.CENTER);
			add( messageLabel, constraints);
			gridy++;
		}
		
		// Setup OK Button
		Button okButton = new Button("OK");
		okButton.addActionListener( this );
		constraints.fill = GridBagConstraints.NONE;
		constraints.weightx = 0.0;
		constraints.weighty = 0.0;
		constraints.gridx = 0;
		constraints.gridy = gridy;
		add( okButton, constraints);
		okButton.requestFocus();
		
		// Set Window Size
		pack();
	}
	
	synchronized public void actionPerformed ( ActionEvent e ) {
		dispose();
	}

	public static void main() {
		Frame f = new Frame();
		f.pack();
	}

} // MessageBox