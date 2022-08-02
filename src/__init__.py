#from rTk import rapidTk, manager, objects
#from errors import *
from .rapidTk import rapidTk
from .rapidTk import PackProcess
from .utils import coord, clipboard
from .objects import *
from .objects_ext import *
from .matchart import Chart
from .flags import *
#import types
#class rTk(types.ModuleType):
#	@property
#	def version(self):
#		version_info = (0, 0, 1)
#		return ".".join([str(x) for x in version_info])
#__all__ = ['.rapidTk.*', '.objects.*', '.utils.coord']
#version = "0.0.1"
