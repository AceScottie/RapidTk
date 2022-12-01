import logging
RTKLOG = 1
RTKDEBUG = 9
RTKNFO = 19
RTKWARNING = 29
RTKERROR = 39
RTKCRITICAL = 49
RTKVERBOSE = 99
RTKUNITS = 100

class rTkLogger(logging.Logger):
    #logging.getLogger('rapidTk')
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
        handler = logging.StreamHandler()
        fmat = logging.Formatter('%(asctime)s %(levelname)s %(filename)s(%(lineno)d) - %(message)s')
        handler.setFormatter(fmat)
        hndlr = self.addHandler(handler)
        self.setLevel(0)

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