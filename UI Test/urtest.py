import urwid
class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

choices = u'Profile Notifications Connections Jobs Search'.split()
def menu(title,choices):
	body = [urwid.Text(title), urwid.Divider()]
	for c in choices:
		button = urwid.Button(c)
		urwid.connect_signal(button, 'click', item_chosen, c)
		body.append(urwid.AttrMap(button, None, focus_map='dark cyan'))
	return urwid.ListBox(urwid.SimpleFocusListWalker(body))
def item_chosen(button,choice):
	response = urwid.Text([u'You chose ', choice, u'\n'])
    	done = urwid.Button(u'Ok')
    	urwid.connect_signal(done, 'click', exit_program)
    	main.original_widget = urwid.Filler(urwid.Pile([response,
        urwid.AttrMap(done, None, focus_map='yellow')]))
def exit_program(button):
	raise urwid.ExitMainLoop()
main = urwid.Padding(menu(u'LinkedIn', choices), left=2, right=2)
top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
    align='center', width=('relative', 60),
    valign='middle', height=('relative', 60),
    min_width=20, min_height=9)
urwid.MainLoop(top, palette=[(None, 'dark blue', '')]).run()


