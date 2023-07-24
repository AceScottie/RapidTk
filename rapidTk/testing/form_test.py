from tkinter.constants import *
from rapidTk import *
import sys, os
print(sys.platform)
_WIN=False
_LIN=False
_MAC=False
if sys.platform == "win32":
	_WIN = True
	_usr_documents = str(os.environ['USERPROFILE'])+"\\Documents"
	_no_cursor = "no"
elif sys.platform == "linux":
	_LIN = True
	_usr_documents = str(os.path.expanduser('~/Documents'))
	_no_cursor = "X_cursor"
elif sys.platform == "macos":
	_MAC = True
_l = localization("en_gb", localpath=os.path.join(_usr_documents, "OEPR", "local"))


rq0 = '.*'
##standard regex
rq1 = '^.{1}.*$' ##requires minimum 1 characters
rq3 = '^.{3}.*$' ##recuires minimum 3 characters
rq1_or_blank = '^(?:.{1}.*)?$' ##recuires minimum 1 characters or empty
rq3_or_blank = '^(?:.{3}.*)?$' ##recuires minimum 3 characters or empty
email = '''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'''
##Date UK format ##/##/####
date_valid_re = '^([0-2][0-9]|3[01])\/(0[0-9]|1[01])\/(19[0-9][0-9]|20[0-9][0-9])$'
##PostCode UK format
postcode_valid_re = '^[a-zA-Z]{1,2}[0-9]{1,2}\s[0-9]{1,2}[a-zA-Z]{1,2}$'
##Zip Code US Format

##Phone number Mobile UK format
phone = '(((07|\+447)\s*(?:\d\s*?){9})|(?:\+44\s?|0)[1238]\d\s?(?:\d\s?){7,8})$' ## accepts mobile or landline numbers (requies testing.)


context = {
			_l.main.basic_info:{
				"Entryfn":{"name":"fname", "label":_l.main.fname, "textwidth":15, "width":30, "text":"", 're':rq3},
				"Entrysn":{"name":"sname", "label":_l.main.sname, "textwidth":15, "width":30, "text":"", 're':rq3},
				"Entryrl":{"name":"relation", "label":"Relation:", "textwidth":15, "width":30, "text":"", 're':rq3}
			},
			_l.main.contact_info:{
				"Entrycd":{"name":"contactd", "label":_l.main.contact_day, "textwidth":15, "width":30, "text":"", 're':phone},
				"Entryce":{"name":"contacte", "label":_l.main.contact_eve, "textwidth":15, "width":30, "text":"", 're':phone},
				"Entryem":{"name":"email", "label":_l.main.email, "textwidth":15, "width":30, "text":"", 're':email}
			},
			_l.main.address_info:{
				"Entrya1":{"name":"address1", "label":_l.main.address1, "textwidth":15, "width":30, "text":"", 're':rq3_or_blank},
				"Entrya2":{"name":"address2", "label":_l.main.address2, "textwidth":15, "width":30, "text":"", 're':rq3_or_blank},
				"Entrycn":{"name":"postcode", "label":_l.main.addresspost, "textwidth":15, "width":30, "text":"", 're':postcode_valid_re},
				"Entryps":{"name":"county", "label":_l.main.addresscounty, "textwidth":15, "width":30, "text":"", 're':rq3}
			},
			_l.main.priority_info:{
				"Optionpr":{"name":"priority", "label":_l.main.priority, "textwidth":15, "width":30, "options":list(range(1, 11))},
			}
		}

root = rapidTk()

f= qForm()
f.create_questions(root, context)

root.mainloop()