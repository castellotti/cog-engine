#####################################################################
#
# The Cog Engine Project - Utilities
#
# Copyright Steven M. Castellotti (2001, 2002)
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Last Update: 2002.06.07
#
# Note: Portions of this code were taken from SQmaiL (version 0.1.1-alpha)
#        by David Given (dtrg@users.sourceforge.net), also
#        released under the GPL
#
#####################################################################


#####################################################################
# Classes
#####################################################################

class WidgetStore:

	# WidgetStore is an interface to a Glade tree
	def __init__(self, tree):
		self._tree = tree


	def __getattr__(self, attr):
		w = self._tree.get_widget(attr)
		if not w:
			raise AttributeError("Widget "+attr+" not found")
		self.__dict__[attr] = w
		return w


	__getitem__ = __getattr__


#####################################################################

class _callback:

	def __init__(self, dest, method):
		self.dest = dest
		self.method = method


	def __call__(self, *args):
		try:
			return apply(self.method, (self.dest,) + args)
		except TypeError:
			print "Exception while calling", self.method.__name__, "on", self.dest
			print "Args:", args
			raise


#####################################################################

class Callback:

	#Callback is a wrapper to allow you to send callbacks to a specific object.

	def __init__(self, dest):
		self.dest = dest
		self.dict = {}
		for i in self.dest.__class__.__bases__:
			self.dict.update(i.__dict__)
		self.dict.update(self.dest.__class__.__dict__)


	def items(self):

		import types

		l = []
		for key, value in self.dest.__class__.__dict__.items():
			if (type(value) == types.FunctionType):
				l.append((key, _callback(self.dest, value)))
		return l


	def __getitem__(self, name):
		return _callback(self.dest, self.dict[name])


#####################################################################
# Functions
#####################################################################

def load_data_file(filename):

	try:
		import cPickle
		pickle = cPickle
	except:
		import pickle

	from CogObjects import *
	file = open(filename, 'r')
	file_format_version_number = pickle.load(file)
	gameInformation = pickle.load(file)
	playerInformation = pickle.load(file)
	directionData = pickle.load(file)
	roomData = pickle.load(file)
	itemData = pickle.load(file)
	obstructionData = pickle.load(file)
	verbData = pickle.load(file)
	file.close()

	return(file_format_version_number, \
	       gameInformation, playerInformation, \
	       directionData, roomData, \
	       itemData, obstructionData, verbData)
                                                                     

#####################################################################

def save_data_file(filename, file_format_version_number, \
                   gameInformation, playerInformation, \
                   directionData, roomData, \
                   itemData, obstructionData, verbData):

	try:
		import cPickle
		pickle = cPickle
	except:
		import pickle

	from CogObjects import *
	file = open(filename, 'w')
	pickle.dump(file_format_version_number, file)
	pickle.dump(gameInformation, file)
	pickle.dump(playerInformation, file)
	pickle.dump(directionData, file)
	pickle.dump(roomData, file)
	pickle.dump(itemData, file)
	pickle.dump(obstructionData, file)
	pickle.dump(verbData, file)
	file.close()

# EOF
