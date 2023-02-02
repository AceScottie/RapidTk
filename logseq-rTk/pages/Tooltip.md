public:: true

- uses #cFrame #cLabel
- Description:
	- Creates a small window with some text to be used as an onHover tooltip
- kword: waittime -> time in ms before tooltip is shown DEFAULT 400
- kword pad -> tuple of the padding around the inside of the tooltip text. DEFAULT (5, 3, 5, 3)
- Methods:
	- `__init__`
	- `onEnter`
	- `onLeave`
	- `schedule`
	- `unschedule`
	- `show`
	- `hide`