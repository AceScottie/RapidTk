import logging
#logging.basicConfig(level=10)


from rapidTk import *
from rapidTk.rTkUtils import time_it
rtklog = logging.getLogger('rapidTk')
rtklog.setLevel(0)
import time

#log.info('test')
@time_it
def tester():
	print("Hello")
	time.sleep(1)
	print("World")

if __name__ == "__main__":
	tester()
	print('done')