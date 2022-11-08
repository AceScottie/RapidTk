
from utils import SingletonMeta
import flags
#from tkinter.ttk import Style
#from ttk import Style
from ttkthemes import ThemedStyle


class _ThemeManager(object, metaclass=SingletonMeta):
	def __init__(self, root):
		flags.__theme_manager__ = True
		self.root = root
		#self.mystyle = style
		self.mystyle = ThemedStyle(root)
	def add_style(self, name, options):
		self.mystyle.configure(name, **options)
		return self.mystyle
	def set_style(self, style):
		self.mystyle.theme_use(style)