#####################################################################
#
# The Cog Engine Project - Festival Text-To-Speech Modules
#
# Copyright Steven M. Castellotti (2002)
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Last Update: 2002.06.20
#
#
#####################################################################

import os, signal, socket

#####################################################################

class Festival_TTS:

	server_process_id = None
	test_server_connection = None

	def __init__(self, debug_mode):

		self.debug_mode = debug_mode
		self.text_output_filepath = '/tmp/cogengine_outputtext.txt'
		self.wav_output_filepath = '/tmp/cogengine_outputtext.wav'

		pid = os.fork()

		if pid == 0:
			os.execlp("festival_server", "festival_server", "-c", "festival_server.config")
		else:
			self.server_process_id = pid


	#####################################################################

	def Speak(self, text, mixer):

		if not self.test_server_connection:
			self.test_server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			try:
				self.test_server_connection.connect(("localhost", 1314))
			except:
				try:
					print "Waiting for Festival server to initialize"
					import time
					time.sleep(3)
					self.test_server_connection.connect(("localhost", 1314))
				except:
					try:
						print "Waiting (longer) for Festival server to initialize"
						time.sleep(7)
						self.test_server_connection.connect(("localhost", 1314))
					except:
						print "Festival intialization timed out. Error connecting to port 1314."

		
		if (os.access(self.text_output_filepath, os.W_OK)):
			if (os.access(self.wav_output_filepath, os.W_OK)):


				output_file = open(self.text_output_filepath, 'w')
				output_file.write(text)
				output_file.close()


				result = os.fork()

				if result == 0:

					os.execlp("festival_client", "festival_client", \
								"--server", "localhost", \
								"--ttw", \
								"--output", self.wav_output_filepath, \
								"--otype", "riff", \
								self.text_output_filepath)

				else:
					childpid, exit_code = os.waitpid(result, 0)
					if (not exit_code):
						self.notify_web_audio()

			else:
				if (self.debug_mode):
					print "File Access Error - File is not writable:", self.wav_output_filepath
		else:
			if (self.debug_mode):
				print "File Access Error - File is not writable:", self.text_output_filepath


	#####################################################################

	def notify_web_audio(self):

		# Publish the generated WAV to the NoVNC web root so the browser
		# can play it via the Web Audio API (no host audio setup required).
		import shutil
		web_audio_dir = '/usr/share/novnc/audio'
		if not os.path.isdir(web_audio_dir):
			return
		try:
			shutil.copy2(self.wav_output_filepath, os.path.join(web_audio_dir, 'latest.wav'))
			counter_path = os.path.join(web_audio_dir, 'counter.txt')
			try:
				count = int(open(counter_path).read().strip()) + 1
			except:
				count = 1
			open(counter_path, 'w').write(str(count))
		except:
			if self.debug_mode:
				print "Error updating web audio"


	#####################################################################

	def stop(self):
		pass


	#####################################################################

	def __del__(self):
		print "Killing Festival server"
		if self.test_server_connection:
			self.test_server_connection.close()
			self.test_server_connection = None

		#os.kill(self.pid, signal.SIGTERM)
		os.system("killall -9 festival festival_server festival_client 2> /dev/null")

