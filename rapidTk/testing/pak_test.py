from xml.etree import cElementTree as ElementTree
from pathlib import Path
import struct
import io
import numpy
def serialize(f, content):
	for k,v in content.items():
		# write length of key, followed by key as string
		k_bstr = k.encode('utf-8')
		f.write(struct.pack('L', len(k_bstr)))
		f.write(k_bstr)
		# write length of value, followed by value in numpy.save format
		memfile = io.BytesIO()
		numpy.save(memfile, v)
		f.write(struct.pack('L', memfile.tell()))
		f.write(memfile.getvalue())
def deserialize(f):
	retval = {}
	while True:
		content = f.read(struct.calcsize('L'))
		if not content: break
		k_len = struct.unpack('L', content)[0]
		k_bstr = f.read(k_len)
		k = k_bstr.decode('utf-8')
		v_len = struct.unpack('L', f.read(struct.calcsize('L')))[0]
		v_bytes = io.BytesIO(f.read(v_len))
		v = numpy.load(v_bytes)
		retval[k] = v
	return retval


localpath = '../assets/local/'
infile = "../assets/local/en_gb.xml"
langs = {}
for language in list(Path(localpath).glob('*.xml')):
	l_name = Path(language).stem
	tree = ElementTree.parse(f"{localpath}{l_name}.xml")
	d = {}
	for child in tree.getroot():
		tmp = {}
		for c in child:
			tmp[c.attrib['name']] = c.text
		d[child.tag] =tmp
	langs[l_name] = d
print(langs)
out = 'out.file'
if __name__ == "__main__":
	with open(out, 'wb+') as f:
		content = langs['en_gb']['section1']
		print(content)
		serialize(f, content)
	with open(out, 'rb+') as f:
		print(deserialize(f))