import logging
import inspect 
    
RTKLOG = 1
RTKDEBUG = 9
RTKNFO = 19
RTKWARNING = 29
RTKERROR = 39
RTKCRITICAL = 49
RTKVERBOSE = 99
RTKUNITS = 100

class rTkLogger(logging.Logger):
    logging.addLevelName(RTKLOG, 'rTk_Log')
    logging.addLevelName(RTKDEBUG, 'rTk_Debug')
    logging.addLevelName(RTKNFO, 'rTk_Info')
    logging.addLevelName(RTKWARNING, 'rTk_Warning')
    logging.addLevelName(RTKERROR, 'rTk_Error')
    logging.addLevelName(RTKCRITICAL, 'rTk_CRITICAL')
    logging.addLevelName(RTKVERBOSE, 'rapidTk')
    logging.addLevelName(RTKUNITS, 'unit')

    def __init__(self, name):
        super(rTkLogger, self).__init__(name)
        self.logLevel = 0
        self.handler = logging.NullHandler()
        self.fmat = logging.Formatter('%(asctime)s %(levelname)s %(filename)s(%(lineno)d) - %(message)s')
        self.handler.setFormatter(self.fmat)
        self.hndlr = self.addHandler(self.handler)

    def __state(self, s, mod):
        if s:
            self.handler = logging.StreamHandler()
        else:
            print('rapidTk Logging disabled')
            self.handler = logging.NullHandler()
        self.handler.setFormatter(self.fmat)
        self.addHandler(self.handler)
        self.rtklog(f'rapidTk Logging enabled at level {self.logLevel} set by {mod}')

    def setLevel(self, level: int):
        frm = inspect.stack()[1]
        mod = inspect.getmodule(frm[0])
        self.logLevel = level
        super().setLevel(self.logLevel)
        if level < 0:
            self.__state(False, mod)
        else:
            self.__state(True, mod)

    def rtklog(self, msg, *args, **kwargs):
        if self.getEffectiveLevel() >= RTKLOG and self.isEnabledFor(self.getEffectiveLevel()):
            super()._log(RTKLOG, msg, args, **kwargs)
    def rtkdebug(self, msg, *args, **kwargs):
        print(self.getEffectiveLevel())
        if self.getEffectiveLevel() >= RTKDEBUG and self.isEnabledFor(self.getEffectiveLevel()):
            super()._log(RTKDEBUG, msg, args, **kwargs)
    def rtkinfo(self, msg, *args, **kwargs):
        if self.getEffectiveLevel() >= RTKNFO and self.isEnabledFor(self.getEffectiveLevel()):
            super()._log(RTKNFO, msg, args, **kwargs)
    def rtkwarning(self, msg, *args, **kwargs):
        if self.getEffectiveLevel() >= RTKWARNING and self.isEnabledFor(self.getEffectiveLevel()):
            super()._log(RTKWARNING, msg, args, **kwargs)
    def rtkerror(self, msg, *args, **kwargs):
        if self.getEffectiveLevel() >= RTKERROR and self.isEnabledFor(self.getEffectiveLevel()):
            super()._log(RTKERROR, msg, args, **kwargs)
    def rtkcritical(self, msg, *args, **kwargs):
        if self.getEffectiveLevel() >= RTKCRITICAL and self.isEnabledFor(self.getEffectiveLevel()):
            super()._log(RTKCRITICAL, msg, args, **kwargs)
    def rtkverbose(self, msg, *args, **kwargs):
        if self.getEffectiveLevel() >= RTKVERBOSE and self.isEnabledFor(self.getEffectiveLevel()):
            super()._log(RTKVERBOSE, msg, args, **kwargs)
    def rtkunit(self, msg, *args, **kwargs):
        if self.getEffectiveLevel() >= RTKUNITS and self.isEnabledFor(self.getEffectiveLevel()):
            super()._log(RTKUNITS, msg, args, **kwargs)
            assert msg == 'pass'