import time


class Document():
	def __init__(self, path):
		self.path = path
		self.deepth = 0
		self.flag_if = False
		self.flag_class = False
		self.flag_loop = False
	
	def on_change_deepth(self):
		if (self.flag_class):
			self.deepth += 1
			pass
		if ( self.flag_if):
			pass
		if (self.flag_loop):
			pass