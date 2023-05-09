from rapidTk import *

#from rapidTk.assets import constants


x = '\u2193'
print(x)

class uButton(cButton):
	def __init__(self, master, **kwargs):
		self.utype = kwargs.pop('type', None)
		if self.utype is None:
			raise Exception("Error")
		kwargs['text'] = self._uni_type()
		super(uButton, self).__init__(master, **kwargs)

	def _uni_type(self):
		if isinstance(self.utype, bytes):
			print("is valid bytes")
			try:
				return self.utype.decode('utf-8')
			except:
				raise Exception(f" {self.utype} is not valid unicode")
		else:
			try:
				if len(self.utype) != 1:
					raise Exception("That is not a valid unicode type")
				return str(self.utype)
			except:
				raise Exception("That is not a valid unicode type")


root = rapidTk()

b = uButton(root, type=constants.UNICODE_UP, side=TOP)
b = uButton(root, type=constants.UNICODE_DOWN, side=BOTTOM)
b = uButton(root, type=constants.UNICODE_LEFT, side=LEFT)
b = uButton(root, type=constants.UNICODE_RIGHT, side=RIGHT)

root.mainloop()