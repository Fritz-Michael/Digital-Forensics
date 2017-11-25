from PIL import ImageTk, Image
from functools import partial
import tkinter as tk
from filerecoveryfunctions import *


class CreateToolTip(object):
    '''
    create a tooltip for a given widget
    '''
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)
    def enter(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background=None, relief='solid', borderwidth=0.5,
                       font=("times", "8", "normal"))
        label.pack(ipadx=1)
    def close(self, event=None):
        if self.tw:
            self.tw.destroy()


class CleanDrive(tk.Frame):

	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		self.controller = controller
		self.parent = parent
		self.settings_frame = tk.Frame(self.parent,bg=None,highlightthickness=2,highlightbackground='red')
		self.alignment_frames = []

		self.set_drives_menu()
		self.alignment_frames.append(tk.Frame(self.parent))
		self.quick_format_button = tk.Button(self.alignment_frames[0],text='Quick Format',command=self.quick_format)
		self.advanced_settings_button = tk.Button(self.alignment_frames[0],text='Advanced Settings',command=self.advanced_settings)

		self.settings_frame.pack(fill=tk.X)
		self.alignment_frames[0].pack(side=tk.TOP,pady=10)
		self.choose_drive_menu.pack(pady=5)
		self.advanced_settings_button.pack(side=tk.LEFT,padx=3)
		self.quick_format_button.pack(side=tk.LEFT,padx=3)


	def set_drives_menu(self):
		self.get_drives()
		self.default_drive = tk.StringVar(self.parent)
		self.default_drive.set(self.drives[0])
		self.choose_drive_menu = tk.OptionMenu(self.settings_frame,self.default_drive,*self.drives)
		self.choose_drive_menu.config(width=35)
		self.choose_drive_tooltip = CreateToolTip(self.choose_drive_menu,'Choose a drive')

	def set_algorithms(self):
		self.wiping_algorithms = ['Zero fill','Secure Erase','Schneier','Random Data']
		self.default_algorithm = tk.StringVar()
		self.default_algorithm.set(self.wiping_algorithms[0])

	def get_drives(self):
		self.drives = get_drivesWin()

	def advanced_settings(self):
		self.advanced_settings_button.pack_forget()
		self.quick_format_button.pack_forget()

		self.set_algorithms()
		self.alignment_frames.append(tk.Frame(self.settings_frame))
		self.choose_algorithm_menu = tk.OptionMenu(self.settings_frame,self.default_algorithm,*self.wiping_algorithms)
		self.choose_algorithm_menu.config(width=35)
		self.choose_algorithm_tooltip = CreateToolTip(self.choose_algorithm_menu,'Choose an algorithm')
		self.other_settings()

		self.choose_algorithm_menu.pack(pady=5)

	def other_settings(self):
		self.sector_number = tk.IntVar()
		self.sector_number.set(0)

		self.other_settings_frame = tk.Frame(self.parent,bg=None,highlightthickness=2,highlightbackground='red')
		self.alignment_frames.append(tk.Frame(self.other_settings_frame))
		self.delete_sector_label = tk.Label(self.alignment_frames[1],text='Sector No:')
		self.delete_sector_entry = tk.Entry(self.alignment_frames[1],textvariable=self.sector_number)

		self.other_settings_frame.pack(fill=tk.X,pady=5)
		self.alignment_frames[1].pack(side=tk.TOP)
		self.delete_sector_label.pack()
		self.delete_sector_entry.pack()


	def quick_format(self):
		pass