#####################################################################
#
# The Cog Engine Project - Festival Text-To-Speech Modules
#
# Copyright Steven M. Castellotti (2002)
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Last Update: 2002.05.31
#
# Note: Portions of this code were taken from Matthew Campbell's
#        Driver for the Festival speech synthesizer,
#        also released under the GPL
#
#####################################################################
import os, signal, socket

class Festival:
	pid = None
	con = None

	def __init__(self):

		if not(os.path.exists('/tmp/.esd/socket')):
			print "Waiting for ESD to initialize"
			import time
			time.sleep(5)

		result = os.fork()

		if result == 0:
			os.execlp("festival_server", "festival_server", "-c", "festival_server.config")
		else:
			self.pid = result


	def Speak(self, text):
	   
		import string

		if not self.con:
			self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			try:
				self.con.connect("localhost", 1314)
			except:
				try:
					print "Waiting for Festival server to initialize"
					import time
					time.sleep(3)
					self.con.connect("localhost", 1314)
				except:
					try:
						print "Waiting (longer) for Festival server to initialize"
						time.sleep(7)
						self.con.connect("localhost", 1314)
					except:
						print "Festival intialization timed out. Error connecting to port 1314."
      
		text = string.replace(text, '"', '\\"')

		self.con.send("(SayText \"" + text + "\")")

	def stop(self):
		pass

	def __del__(self):
		print "Killing Festival server"
		if self.con:
			self.con.close()
			self.con = None

		#os.kill(self.pid, signal.SIGTERM)
		os.system("killall -9 festival festival_server 2> /dev/null")
