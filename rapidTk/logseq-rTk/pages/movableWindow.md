public:: true

- inherits #cCanvas #widegBase
- uses #cFrame #cButton #cLabel
- Description:
	- Creates a floating window above the tk window. Adds a title Label and close/minimize/popout buttons.
	- The window Titlebar can be dragged with the mouse to any position on the Tk window that does not result in the window being out of bounds.
	- The minimize button compresses the Canvas to just have the title bar and stacks it along the bottom left of the window.
- kword:
-
- {{renderer :todomaster}}
- TODO implement layout manager from #rTkUtils
- Methods:
	- `__init__`
	- `_create`
	- `_click`
	- `_move`
	- `_calc_move`
	- `_drop`
	- `_popout` TODO popout the Canvas and rebuild into a new window, requires #rWindowManager
	- `_drop`
	- `_minimize`
	- `_maximize`
	- `_close`
	- TODO `destroy` add this method to clean up all objects.
	  :LOGBOOK:
	  CLOCK: [2023-02-02 Thu 10:26:16]
	  :END:
	- `__del__`