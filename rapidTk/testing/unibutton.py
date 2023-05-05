from rapidTk import *

UNICODE_UP = '\u2191'
UNICODE_DOWN = '\u2193'
UNICODE_LEFT = '\u2190'
UNICODE_RIGHT = '\u2192'

UNICODE_UP = b'\xE2\x86\x91'
UNICODE_DOWN = b'\xE2\x86\x93'
UNICODE_LEFT = b'\xE2\x86\x90'
UNICODE_RIGHT = b'\xE2\x86\x92'

x = '\u2191'
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
		match self.utype:
			case "utf":
				return "what ?"
			case _:
				try:
					if len(self.utype) != 1:
						raise Exception("That is not a valid unicode type")
					return str(self.utype)
				except:
					raise Exception("That is not a valid unicode type")


root = rapidTk()

b = uButton(root, type="\u2195", side=TOP)
b = uButton(root, type=b'\x00\x00\x00', side=BOTTOM)
b = uButton(root, type=UNICODE_LEFT, side=LEFT)
b = uButton(root, type=UNICODE_RIGHT, side=RIGHT)

root.mainloop()