#! /usr/bin/python
import npyscreen
class myForm(npyscreen.Form):
	def create(self):			# OVERRIDE THE METHOD
		self.myName=self.add(npyscreen.TitleText, name='Name')
		self.myDepartment=self.add(npyscreen.TitleSelectOne, max_height=4,
								name='Options',
								values = ['Profile', 'Connections', 'Search','Job'],
								scroll_exit = True  # Let the user move out of the widget by pressing the down arrow instead of tab.  Try it without
													# to see the difference.
								)
		self.myDate= self.add(npyscreen.TitleDateCombo, name='Date Employed')
def myFunction(*args):
	F=myForm(name="PyLify")
	F.edit()
	return F.myName.value

	

if __name__ == '__main__':
	print npyscreen.wrapper_basic(myFunction)
	