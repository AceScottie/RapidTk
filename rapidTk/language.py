from pathlib import Path
from types import SimpleNamespace
from xml.etree import cElementTree as ElementTree
import os
class languages(SimpleNamespace):
	def __init__(self, lang="en_gb", localpath='./assets/local/'):
		langs = {}
		for language in list(Path(localpath).glob('*.xml')):
			l_name = Path(language).stem
			tree = ElementTree.parse(f"{localpath}{l_name}.xml")
			d = {}
			for child in tree.getroot():
				tmp = {}
				for c in child:
					tmp[c.attrib['name']] = c.text
				d[child.tag] = SimpleNamespace(**tmp)
			langs[l_name] = SimpleNamespace(**d)
		super().__init__(**langs)
class localization(object):
	def __init__(self, lang="en_gb", localpath='./assets/local/'):
		if os.path.isfile(f"{localpath}{lang}.xml"):
			self.languages = languages(lang=lang, localpath=localpath)
			self.set_language = lang
		else:
			raise Exception(f"{localpath}{lang}.xml is not a valid file")
	def set_local(self, lang="en_gb"):
		self.set_language = lang
	def get_local(self):
		return self.set_language
	def __getattr__(self, at):
		return getattr(getattr(self.languages, self.set_language), at)


if __name__ == "__main__":
	language = localization()
	print(language.section1.hello)
	language.set_local("fr")
	print(language.section1.hello)

