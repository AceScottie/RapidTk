
##layout methods
layout_pack = """
after=widget - pack it after you have packed widget
anchor=NSEW (or subset) - position widget according to
                          given direction
before=widget - pack it before you will pack widget
expand=bool - expand widget if parent size grows
fill=NONE or X or Y or BOTH - fill widget if widget grows
in=master - use master to contain this widget
in_=master - see 'in' option description
ipadx=amount - add internal padding in x direction
ipady=amount - add internal padding in y direction
padx=amount - add padding in x direction
pady=amount - add padding in y direction
side=TOP or BOTTOM or LEFT or RIGHT -  where to add this widget.
"""
layout_place = """
Place a widget in the parent widget. Use as options:
in=master - master relative to which the widget is placed
in_=master - see 'in' option description
x=amount - locate anchor of this widget at position x of master
y=amount - locate anchor of this widget at position y of master
relx=amount - locate anchor of this widget between 0.0 and 1.0
              relative to width of master (1.0 is right edge)
rely=amount - locate anchor of this widget between 0.0 and 1.0
              relative to height of master (1.0 is bottom edge)
anchor=NSEW (or subset) - position anchor according to given direction
width=amount - width of this widget in pixel
height=amount - height of this widget in pixel
relwidth=amount - width of this widget between 0.0 and 1.0
                  relative to width of master (1.0 is the same width
                  as the master)
relheight=amount - height of this widget between 0.0 and 1.0
                   relative to height of master (1.0 is the same
                   height as the master)
bordermode="inside" or "outside" - whether to take border width of
                                   master widget into account
"""


layout_grid = """
Position a widget in the parent widget in a grid. Use as options:
column=number - use cell identified with given column (starting with 0)
columnspan=number - this widget will span several columns
in=master - use master to contain this widget
in_=master - see 'in' option description
ipadx=amount - add internal padding in x direction
ipady=amount - add internal padding in y direction
padx=amount - add padding in x direction
pady=amount - add padding in y direction
row=number - use cell identified with given row (starting with 0)
rowspan=number - this widget will span several rows
sticky=NSEW - if cell is larger on which sides will this
              widget stick to the cell boundary
"""
_global_layout = ["in", "anchor", "ipady", "ipadx", "padx", "pady", "in_"]
_pack_add = ["after", "before", "side", "fill", "expand"]
_grid_add = ["column", "columnspan", "row", "rowspan", "sticky"]
_place_add = ["x", "y", "relx", "rely", "relwidth", "relheight", "bordermode", "xsize", "ysize"]

##unicode constants
UNICODE_UP = b'\xE2\x86\x91'
UNICODE_DOWN = b'\xE2\x86\x93'
UNICODE_LEFT = b'\xE2\x86\x90'
UNICODE_RIGHT = b'\xE2\x86\x92'
UNICODE_HELP = b'\xF0\x9F\x9B\x88'


LINK='#0000EE'
LINKVISIT='#551A8B'
IELINK='#0066CC'
IELINKVISIT='#800080'
GOOGLELINK= "#6eb4f8"
GOOGLELINKVISIT = '#c58af9'
GOOGLE_DARKMODE_BG = '#202124'

if __name__ == "__main__":
    print(UNICODE_UP.decode('utf-8'))
    print(UNICODE_HELP.decode('utf-8'))

    from tkinter import *
    root = Tk()
    fontsize='15'
    font_special='underline'
    root.tk_setPalette(background=GOOGLE_DARKMODE_BG)
    Label(root, text="Link", font=(f'Helvetica {fontsize} {font_special}'), fg = LINK).pack(side=TOP)
    Label(root, text="Link_Visited", font=(f'Helvetica {fontsize} {font_special}'), fg = LINKVISIT).pack(side=TOP)
    Label(root, text="IE Link", font=(f'Helvetica {fontsize} {font_special}'), fg = IELINK).pack(side=TOP)
    Label(root, text="IE Link_Visited", font=(f'Helvetica {fontsize} {font_special}'), fg = IELINKVISIT).pack(side=TOP)
    Label(root, text="Get a PCR test to check if you have COVID-19", font=(f'Helvetica {fontsize} {font_special}'), fg = GOOGLELINK).pack(side=TOP)
    Label(root, text="Testing for COVID-19", font=(f'Helvetica {fontsize} {font_special}'), fg = GOOGLELINKVISIT).pack(side=TOP)

    root.mainloop()