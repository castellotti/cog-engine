#####################################################################
#
# COG Engine Development Application - Utils
#
# Copyright Steven M. Castellotti (2000)
# This code is released under the GNU Pulic License (GPL) version 2
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Last Update: 2001.09.22
#
# Note: Portions of this code was take from SQmaiL (version 0.1.1-alpha)
#        by David Given (dtrg@users.sourceforge.net), also
#        released under the GPL
#
#####################################################################

import types

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

class Callback:
	#Callback is a wrapper to allow you to send callbacks to a specific object.
	def __init__(self, dest):
		self.dest = dest
		self.dict = {}
		for i in self.dest.__class__.__bases__:
			self.dict.update(i.__dict__)
		self.dict.update(self.dest.__class__.__dict__)

	def items(self):
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
# 	if (self.debug_mode):
# 		print "Loading: " + filename + "...",
	import cPickle
	from CogObjects import *
	file = open(filename, 'r')
	gameInformation = cPickle.load(file)
	playerInformation = cPickle.load(file)
	directionData = cPickle.load(file)
	roomData = cPickle.load(file)
	itemData = cPickle.load(file)
	obstructionData = cPickle.load(file)
	verbData = cPickle.load(file)
	file.close()
# 	if (self.debug_mode):
# 		print "done"
	return(gameInformation, playerInformation, \
	       directionData, roomData, \
	       itemData, obstructionData, verbData)

def save_data_file(filename, \
                   gameInformation, playerInformation, \
                   directionData, roomData, \
                   itemData, obstructionData, verbData):
# 	if (self.debug_mode):
# 		print "Saving: " + filename + "...",
	import cPickle
	from CogObjects import *
	file = open(filename, 'w')
	cPickle.dump(gameInformation, file)
	cPickle.dump(playerInformation, file)
	cPickle.dump(directionData, file)
	cPickle.dump(roomData, file)
	cPickle.dump(itemData, file)
	cPickle.dump(obstructionData, file)
	cPickle.dump(verbData, file)
	file.close()
# 	if (self.debug_mode):
# 		print "done"

# EOF