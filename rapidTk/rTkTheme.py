from tkinter.ttk import Style
#from ttk import Style
from ttkthemes import ThemedStyle

from .rTkUtils import SingletonMeta
from .flags import __theme_manager__

class _ThemeManager(object, metaclass=SingletonMeta):
	def __init__(self, root):
		print('tm called')
		__theme_manager__ = True
		self.root = root
		self.style = Style()
		self.set_theme('clam')
		#self.style = ThemedStyle(root)
	def add_style(self, name, options):
		self.style.configure(name, **options)
		return self.style
	def set_theme(self, theme):
		self.style.theme_use(theme)