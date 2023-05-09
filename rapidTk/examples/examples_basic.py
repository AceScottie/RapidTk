import sys
from tkinter import Event, PhotoImage
from tkinter import Scrollbar as tkScrollbar
from tkinter import Frame as tkFrame
import PIL
from rapidTk import *
import logging
rtklog = logging.getLogger('rapidTk')
rtklog.setLevel(0)

import sys
print(f"Python version:{sys.version}")


"""
rapdTk Log Levels:
|   1| Standard User Logging (meant for user code)
|   9| Dedug Logging
|  19| Information Logging
|  29| Warning Logs
|  39| Error Logs
|  49| Critical Logs
|  99| Verbose Logs (all logs, all timers, all function calls)
| 100| Unit Logs (used for unit testing to assert True if test succees)
"""



##Functions used for examples, Do not modify! -----
@time_it
def example_basic_logging_timed_widgets(pp, master, count): ##used as part of example_basic_logging()
	widgets = []
	for i in range(count):
		widgets.append(pp.add(cLabel(master, text=f'{i} :: {__name__}'), side=TOP))
	return widgets
def example_get_runner(event, options, start, end, widgets, out): ##used as part of example_get()
	out.configure(text=widgets[options.get()].get(start.get(), end.get()))
def example_set_runner(event, options, index, inp, widgets, out): ##used as part of example_set()
	widgets[options.get()].set(index.get(), inp.get())
def switch_language(e:Event, _l:localization, b:cButton, lb:cLabel): ##used as part of example_basic_language()
	if _l.get_local() == 'en_gb':
		_l.set_local('fr') ##sets the local language strings present in fr.xml
	else:
		_l.set_local('en_gb')
	lb.configure(text=_l.example.hello) ##changes the string to the new fr.xml -> resource.example.hello string
	b.configure(text=_l.example.changeLanguage) ##changes the string to the new fr.xml -> resource.example.changeLanguage string
def uuid_printer(event, widget):##used as part of example_uuids()
	print(f"This button has the UUID: {widget.uid}")
def uuid_print_all(event, widget):##used as part of example_uuids()
	print(widget.get_root().uid)
def example_spinbox_trigger(event, widget):##used as part of example_spinbox()
	print(f"current: {widget.get()}, next:{widget.next()}, previous:{widget.previous()}")
def example_spinbox_callback(widget, direction:bool):##used as part of example_spinbox()
	print(f"value={widget.get()}")
	print(f"stringvar={widget.var.get()}")
	print(f"{direction=}")
def example_text_print(event, a, b, c, sv):##used as part of example_text()
	print(f'output: {sv.get()}')
def example_text_checkvar(event, widget):##used as part of example_text()
	print(widget.get())
def example_text_add_image(event, scrolledtext, text, content):##used as part of example_text()
	img = PhotoImage(file = "../assets/example.png")
	scrolledtext.image_create(END, image = img)
	text.image_create(END, image = img)
	content.window_create(END, window = cLabel(content, image = img)) # Example 2
	content.image_create(END, image = img)
##-------------------------------------------------


def example_basic_objects():
	doc = """
	To create a rapidTk instance use the rapidTk() method which overwires the Tk() method and returns the Tk() method.
	As it returns the Tk() method all commands on root are still valid if they are valid on a Tk() object.
	rTk only uses Pack() methods over grid() and place(). grid() may be added in the future however place() will not be supported due to bad design useage.

	PackProcess() is a class that lets you create all objecst in the correct order and the pack them in that order later.
	to use, initilise the class and use the add() method to add widgets to the list and finally call the pack() method.
	add() acceps all standard .pack() options and returns the widget unlike the original pack() method.
	e.g. myFrame = pp.add(cFrame(root), side=TOP) #accepts rapidTk Widgets
		 myFrame2 = pp.add(Frame(root), side=TOP) #accepts Tkinter Widgets

	c(Widget) is a class that overwites the original widget while keeping the widget accessible.
	There may be addition options avaibleble in the cWidget however all original options are kept too keep it as compatible as possible.
	All cWidgets, reWidgets and extended Widgets will have the methods of get_self(), get_parent() and get_root().
	These methods will return the Widget, the widgets parent or the root Widget.

	cLabel has 2 additional methods of get() and set() which get and set the text option.

	cEntry() has an addition option of value which automatically sets up a StringVar textvariable and sets that to the value.
	It also creates a popup rightclick menu for cut, copy, select all and paste.

	"""
	print(f"-----\n\n{doc}\n\n-----")
	root = rapidTk()
	pp = PackProcess()
	main = pp.add(cFrame(root), side=TOP, fill=BOTH, expand=1)
	x = pp.add(cLabel(main, text="This is a basic rapidTk Label."), side=TOP, fill=X)
	print(x.get())
	pp.add(cButton(main, text="This is an Example Button"), side=TOP)
	pp.add(cEntry(main, value="Some Default Text"), side=TOP, fill=X)
	pp.pack()
	root.mainloop()

def example_basic_objects2():
	doc = """
	cCanvas (WIP) is just a canvas widget with no special functions yet.

	cTreeview is an TreeView widget with automatic row-highligh, colour options and sort options.
	It can also be linked to a checkbox to hide data automatically, this is shown in the opts.var.trace method.

	cScrolledText() has a default value that can be set. It also has the same menu as cEntry with cut, copy, selectall and paste options

	cCheckbutton() has get() and set() methods which use the IntVar built into the class.

	cOptionMenu() has a defautl value, a list of valid options and a list of none valid options if needed.
	If the default value is part of the options it will not duplicate it in the options.
	non_valid is just a safe way to remove options over time without adjusting code. This can be used if options is gathered from an external source.

	"""
	print(f"-----\n\n{doc}\n\n-----")
	root = rapidTk()
	pp = PackProcess()
	
	cv = pp.add(cCanvas(root), side=TOP, fill=BOTH, expand=1)
	##example TreeView
	treeFrame = pp.add(cFrame(cv), side=TOP, fill=X, expand=1)
	myTree = pp.add(cTreeview(treeFrame), side=LEFT, fill=X)
	vsb = pp.add(tkScrollbar(treeFrame, orient="vertical",command=myTree.yview), side=LEFT, fill=Y) 
	myTree.configure(yscrollcommand=vsb.set)
	myTree.set_cols(['Test1', 'Test2'])
	for i in range(0, 30, 2):
		rc = myTree.insert(values=[str(i), str(i+1)])
		if i%3 == 0 and i != 0:
			myTree.detached_data.append(rc)

	myText = pp.add(cScrolledText(cv, value="This is a test Value\nWith Multiple\nLines"), side=TOP)
	f2 = pp.add(cFrame(cv), side=TOP, fill=BOTH, expand=1)
	myCheck = pp.add(cCheckbutton(f2), side=TOP)
	myOptions = pp.add(cOptionMenu(f2, default='Hello', options=['Hello', 'World', 'How', 'are', 'you', '?'], non_valid=['are']), side=TOP)
	
	myCheck.var.trace('w', lambda a, b, c, e=Event(), v=myCheck:myTree.hide(a, b, c, e, v))
	pp.pack()
	root.mainloop()

def example_no_Process():
	doc = """
	PackProcess(), GridProcess() and PlaceProcess() are an optional extra, all cWidgets support inline layouts along with the standard layout methods.
	The down side to inline packing is it creates and packs widgets 1 at a time making layouts be created in the order coded.

	To use inline layouts add the layout keywords into the same string.
	Note: 
		keywords detected by multiple layouts: "in", "anchor", "ipady", "ipadx", "padx", "pady", "in_"
		
		If these are included please use the 'method' keyword as 'pack', 'place' or 'grid' to prevent issues with auto-detecting of layouts.
		Or ensure they are at the end of the keywords as it will determin the layout from the first availbe keyword that matches.

		keywords for place: 'width' and 'height' have been replace with 'xsize' and 'ysize' to avoid conflicting with the widget keywords.
		This may be changed in the future to cover other conflictions.

		layout keywords:
			pack = "after", "before", "side", "fill", "expand"
			grid = "column", "columnspan", "row", "rowspan", "sticky"
			place = "x", "y", "relx", "rely", "relwidth", "relheight", "bordermode", "xsize"(width), "yzise"(height)

	Standard layouts are done as normal in tkinter standard.
	"""
	print(f"-----\n\n{doc}\n\n-----")
	root = rapidTk()
	main = cFrame(root, side=TOP, fill=BOTH, expand=1)
	cLabel(main, text="This is a basic rapidTk Label.", side=TOP, fill=X)
	cButton(main, text="cButton", side=TOP) ## side keyword present in pack layout so automatically packs.
	cEntry(main, value="Some Default Text").pack(side=TOP, fill=X) ##example using the standard .pack() method
	root.mainloop()

def example_basic_global_functions_test(event, root, w):
	for widget in w:
		print(widget)
		widget.set(0, 'Hello')
		widget.set('end', ' World!')
		#widget.set(0, 'Test: ')
		widget.update()

def tester(var, index, mode, root):
	print(var, index, mode)
	print(root.globalgetvar(var))
def example_basic_global_functions():
	doc = """
		Global functions are attatched to all rapidTk widgets. These include new version of get(), set(), insert() and delete()
		All arguments are optional.
		get(index, end) -> gets text from StringVar between index->0 and end->len(var). Gets value from Variables when not using StringVar
		set(index, text) -> sets the Variable at insert->0 position. Delets everything past index before inserting text.
		insert(index, text) -> sets the Variable at insert->0 position. Shifts text to make room for text.
		delete() clears the entire content of the Variable.
	"""
	print(f"-----\n\n{doc}\n\n-----")
	logging.getLogger('rapidTk').setLevel(90)
	root = rapidTk()
	main = cFrame(root, side=TOP, fill=BOTH, expand=1)
	w = []
	w.append(cEntry(main, side=TOP, fill=X))
	w.append(cScrolledText(main, height=3, side=TOP, fill=X))
	w.append(cLabel(main, width=10, side=TOP, fill=X))
	w.append(cText(main, height=3, side=TOP, fill=X))
	w.append(cOptionMenu(main, width=10, options=['test', 'Hello', 'World! ', 'Test: ', 'Hello World!'], side=TOP, fill=X)) ##requires modifacations
	w[4].var.trace('wu', lambda v, i, m, r=root:tester(v, i, m, r))
	w[4].set('testing')
	cButton(main, text="Test", side=TOP, command = lambda e=Event, r=root, w=w:example_basic_global_functions_test(e, r, w))
	root.mainloop()

@time_it
def example_basic_logging():
	doc = """
	rapidTk contains its own logging options.
	To enable logging simply call logging.getLogger('rapidTk').setLevel(level) with level > 0
	To disable logging set level to 0

	most logging will be handled internally by rapidTk, however a custom log method has been included to replace normal print() statements.
	to use simply get the logger and use the rtklog('message') method as shown in the below example.
	rapidTk also implements a performance timer wrapper to easlily identify how long widget creating is taking.
	add the @time_it wrapper to any function and set log level to 99 to start collecting timers.
	"""
	print(f"-----\n\n{doc}\n\n-----")
	rtklogger = logging.getLogger('rapidTk') ##get the rapidTk logger
	rtklogger.setLevel(99) # sets log level to 99 for verbose logging.
	#rtklogger.setLevel(1) # sets log level to  1 for user logging

	#Create a basic window
	root = rapidTk()
	root.geometry('320x150')
	pp = PackProcess()
	main = pp.add(cFrame(root), side=TOP, fill=BOTH, expand=1)

	widgets = example_basic_logging_timed_widgets(pp, main, 100)
	#rtklogger.rtklog(widgets)

	rtklogger.rtklog('all widgets have been created, starting packing')
	pp.pack()
	rtklogger.rtklog('widgets have been packed | starting mainloop')
	root.mainloop()
	
def example_basic_menu():
	doc = """
	cMenu is a quick and efficent way to make simple menus.
	The only thing you need to provide is context on creation.
	context is a dictionary of {Menu(.submenu(s)).Label : command}
	example:
	context={"Menu.Submenu1.Submenu2.options":lambda m="test":print(m)}
	will create a main menu called "Menu" with a submenu called Submenu1 with a submenu called "Submenu2" with an option called "options"
	The "options" option will run the command when clicked.

	Note: subtree paths do not stack.
	"Menu.Submenu1.Submenu2" is not the same as "Submenu1.Submenu2".
	This will create 2 menus called "Menu" and "Submenu1"

	all submenus and options can be accessed though the cMenu.sub_menus and cMenu.options dictionarys.
	"""
	print(f"-----\n\n{doc}\n\n-----")
	root = rapidTk()
	root.geometry('320x150')
	main = cFrame(root, bg="red", side=TOP, fill=BOTH, expand=1)
	menu_context = {
	'File.Open': lambda m="Open":print(m),
	'File.System.Advanced.Close': lambda m="Close":print(m),
	'File.Quit': lambda m="Quit":print(m),
	'System.Kill': lambda m="Kill":print(m),
	'Exit': lambda m="Exit":print(m)
	}
	myMenu = ContexMenu(root, context=menu_context)
	log = logging.getLogger('rapidTk')
	log.rtklog(myMenu.sub_menus) ## this retuns a dictionary of 'contextname':widget for each menu item created from context
	log.rtklog(myMenu.options) ## TODO: add value for options ## This returns a dictionary of 'contextname':value for each item created with context.

	root.config(menu=myMenu) ##standard tkinter menu
	root.bind("<Button-3>", myMenu._do_popup) #bind to right click when widget clicked.
	root.mainloop()

def example_get():##Requires fixing
	doc = """
	cWidgets that have text values support the get() method.
	get(start, end) or get() are both valid options for all widgets that support the get() method.
	!This overwrites the standard tk get() method. 

	"""
	print(f"-----\n\n{doc}\n\n-----")
	root = rapidTk(log_level=0)
	pp = PackProcess()
	main = pp.add(cFrame(root), side=TOP, fill=BOTH, expand=1)

	config = pp.add(cFrame(main, borderwidth=3, relief='raised'), side=TOP, fill=BOTH, expand=1)
	holder = pp.add(cFrame(main, borderwidth=3, relief='groove'), side=TOP, fill=BOTH, expand=1)
	w={}
	w['cLabel'] = pp.add(cLabel(holder, text="This is a basic rapidTk Label."), side=TOP, fill=X)
	w['cButton'] = pp.add(cButton(holder, text="This is an Example Button"), side=TOP)
	w['cEntry'] = pp.add(cEntry(holder, value="Some Default Text"), side=TOP, fill=X)

	options = pp.add(cOptionMenu(config, options=['cLabel', 'cButton', 'cEntry']), side=LEFT, fill=X)
	start = pp.add(cEntry(config, value=""), side=LEFT, fill=X)
	start.set(None, "Some Text")
	end = pp.add(cEntry(config, value=""), side=LEFT, fill=X)

	output = pp.add(cLabel(holder, text="This will be the output"), side=TOP)
	pp.add(cButton(config, text="Check Output", command=lambda e=Event, o=options, s=start, ed=end, w=w, out=output: example_get_runner(e, o, s, ed, w, out)), side=TOP)

	
	pp.pack()
	root.mainloop() 

def example_basic_set():##Requires fixing
	doc = """
	!WIP! This feature is currently a WIP and only works for cButton, cLable, cEntry, cScrolledText and their subclasses (e.g. reEntry, ImageLabel, iButton)
	As with get() all widgets with text values will support the set() method.
	set(index, text) and set(text) are both valid options.
	set(index, text) will get the origial text valie and append the text from the index position (this will remove any additional text beyond index+text length)
	set(text) will clear the current text and replace it with the specified text

	!This overwrites the tkinter set() method.
	"""
	print(f"-----\n\n{doc}\n\n-----")
	root = rapidTk(log_level=0)
	pp = PackProcess()
	main = pp.add(cFrame(root), side=TOP, fill=BOTH, expand=1)

	config = pp.add(cFrame(main, borderwidth=3, relief='raised'), side=TOP, fill=BOTH, expand=1)
	holder = pp.add(cFrame(main, borderwidth=3, relief='groove'), side=TOP, fill=BOTH, expand=1)
	w={}
	w['cLabel'] = pp.add(cLabel(holder, text="This is a basic rapidTk Label."), side=TOP, fill=X)
	w['cButton'] = pp.add(cButton(holder, text="This is an Example Button", cursor='@../assets/cur.cur'), side=TOP)
	w['cEntry'] = pp.add(cEntry(holder, value="Some Default Text"), side=TOP, fill=X)

	options = pp.add(cOptionMenu(config, options=['cLabel', 'cButton', 'cEntry']), side=LEFT, fill=X)
	ind = pp.add(cEntry(config, value=""), side=LEFT, fill=X)
	set_input = pp.add(cEntry(config, value=""), side=LEFT, fill=X)
	set_input.set(None, "Some Text")

	output = pp.add(cLabel(holder, text="This will be the output"), side=TOP)
	pp.add(cButton(config, text="Set text", command=lambda e=Event, o=options, i=ind, inp=set_input, w=w, out=output: example_set_runner(e, o, i, inp, w, out)), side=TOP)

	
	pp.pack()
	root.mainloop()

def example_baisc_language():
	doc = """
	A global language string subsystem.
	This allows you to configure xml files (format found in assets/local/) and create a sequence of strings.
	having multiple xml files allows the user to switch between different string definitions or languages by calling the set_local() method with the filename of the xml.

	it is recommended to set the call on a global scope and use _l or similar to access it throughout your code.

	this can also be used to replace long string values into simple dot notated refrences making code look cleaner.
	"""
	print(f"-----\n\n{doc}\n\n-----")
	_l = localization(lang='en_gb', localpath='../assets/local/') ## initilise the string resources using the en_gb.xml file found in the ../assets/local/ path.
	
	root = rapidTk()
	lb = cLabel(root, text=_l.example.hello, side=TOP) ## use the string found in en_gb.xml -> resrouces.example.hello 
	change = cButton(root, text=_l.example.changeLanguage, side=TOP) ## use the string found in en_gb.xml -> resrouces.example.changeLanguage 
	change.configure(command=lambda e=Event(), _l=_l, lb=lb, b=change:switch_language(e, _l, b, lb)) 
	root.mainloop()

def example_uuids():
	doc = """
	All basic widgets in rapidTk have a Unique Identifier which is stored in the metaclass _UniqueIdentifiers()
	You can generate a new uuid by calling `uuid = _UniqueIdentifiers().new()
	Also you can add your own unique identifieds with `_UniqueIdentifiers().append('[UniqueIdentifier]')`
	Attemping to manually add an existing identifier will raise a duiplicateIDError
	You can see all used UUIDs by calling get_root().uid on any widget to get a list of UUIDs
	"""
	print(f"-----\n\n{doc}\n\n-----")
	root = rapidTk()
	pp = PackProcess()
	main = pp.add(cFrame(root), side=TOP, fill=BOTH, expand=1)
	b1 = pp.add(cButton(main, text="Button 1"), side=TOP, fill=X)
	b2 = pp.add(cButton(main, text="Button 2"), side=TOP)
	b3 = pp.add(cButton(main, text="Button 3"), side=TOP, fill=X)

	b4 = pp.add(cButton(main, text="Print all UUID"), side=TOP, fill=X)

	b1.configure(command=lambda e=Event(), w=b1:uuid_printer(e, w))
	b2.configure(command=lambda e=Event(), w=b2:uuid_printer(e, w))
	b3.configure(command=lambda e=Event(), w=b3:uuid_printer(e, w))
	b4.configure(command=lambda e=Event(), w=b3:uuid_print_all(e, w))
	pp.pack()
	root.mainloop()

def example_spinbox():
	doc = """
	cSpinbox is modified version of the overridden Spinbox (see rTkOverrides).
	It automatically binds the mousewheel if root is an instance of rapidTk.
	It automatically sets the `command` keyword to perform the same action as the mousewheel (which can be overriden by the user).
	It automatically handels wrapping if the `wrap` keyword is set to 1 or True.
	The 'callback' keyword acceps a function with widget and direction args which will be called after a (scroll/button) event is performed.
	"""
	print(f"-----\n\n{doc}\n\n-----")
	root = rapidTk()
	sp1 = cSpinbox(root, values=[str(x) for x in range(10)], wrap=1, callback=example_spinbox_callback, side=TOP)
	sp1.bind('<Return>', lambda e=Event(), w=sp1: example_spinbox_trigger(e, w))
	root.mainloop()
	"""
	The overriden Spinbox has a few additional methods.
	next(wrap:bool) -> returns the next item in the values (if not wrap and item is last index returns last index item).
	previous(wrap:bool) -> returns the previous item in the values (if not wrap and item is 0th index returns 0th index item).
	spin(direction:bool) -> configures the Spinbox to the next/previous item based on the input direction (True:up, False:down)
	configure(**kwargs) -> calls the configure() method of the super class. if one of the keywords is `values` sets the attribute values to the keyword `values`
	"""


def example_text():
	doc = """
		Text and ScrolledText widgets have been remade to allow for the use of StringVar as a textvariable.
		This puts both these objects inline with the global methods of get(), set(), insert() and delete()

		NOTICE: Text is compatible with tkinter.Text however a replacement of that has been included as tkoverride.Content
				Content only contains the super() change and does not include the textvariable.
				Text textvariable does not include images in its content.
				I dont know why but # Example 2 only works on Content and errors on Text.
				Too many images will cause render errors, probably a memory allocation issue. Also having all 3 adding images using image_create doesnt work?
	"""
	print(f"-----\n\n{doc}\n\n-----")
	root = Tk()
	f = Frame(root)
	f.pack(side=TOP)
	t = cScrolledText(f, height=4, side=TOP)
	t2 = cText(f, height=4, side=TOP)
	t.var.trace('w', lambda  a, b, c, e=Event, v=t.var:example_text_print(e, a, b, c, v))
	t2.var.trace('w', lambda  a, b, c, e=Event, v=t2.var:example_text_print(e, a, b, c, v))
	c= Content(f, height=4)
	c.pack(side=TOP)
	cButton(f, text='test', command=lambda e=Event, w=t2:example_text_checkvar(e, w), side=BOTTOM)
	cButton(f, text='Add Image', command=lambda e=Event, w1=t, w2=t2, w3=c:example_text_add_image(e, w1, w2, w3), side=BOTTOM)
	root.mainloop()

if __name__ == "__main__":
	#example_basic_objects()
	#example_basic_objects2()
	example_no_Process()
	#example_basic_global_functions()
	#example_basic_logging()
	#example_basic_menu()
	#example_get()
	#example_basic_set()
	#example_baisc_language()
	#example_uuids()
	#example_spinbox()
	#example_text()
	pass