from PIL import ImageTk, Image
from functools import partial
import tkinter as tk
from filerecoveryfunctions import *


class CreateToolTip(object):

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
        self.tw = tk.Toplevel(self.widget)
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

		self.file_deletion_frame = tk.Frame(self.parent,highlightthickness=2,highlightbackground='black')
		self.clean_sector_frame = tk.Frame(self.parent)
		self.format_drive_frame = tk.Frame(self.parent)

		self.file_deletion_init()
		self.clean_sector_init()
		self.format_drive_init()
		
		self.file_deletion_frame.pack()
		self.clean_sector_frame.pack()
		self.format_drive_frame.pack()		


	def file_deletion_init(self):
		self.alignment_frames = []
		self.select_value = tk.IntVar()
		self.is_advanced = tk.IntVar()

		self.advanced_settings_frame = tk.Frame(self.file_deletion_frame)
		self.alignment_frames.append(tk.Frame(self.parent))
		self.alignment_frames.append(tk.Frame(self.file_deletion_frame))
		self.alignment_frames.append(tk.Frame(self.advanced_settings_frame))
		self.set_drives_menu()
		self.scan_drive_button = tk.Button(self.alignment_frames[0],text='Scan Drive',command=self.scan_drive)
		self.delete_files_label = tk.Label(self.file_deletion_frame,text='File Deletion')
		self.files_list = tk.Listbox(self.file_deletion_frame,selectmode=tk.MULTIPLE,height=7,width=100)
		self.select_deselect = tk.Checkbutton(self.alignment_frames[1],text='Select/Deselect All',variable=self.select_value,command=self.select_deselect_files)
		self.advanced_button = tk.Checkbutton(self.alignment_frames[1],text='Advanced',variable=self.is_advanced,command=self.advanced_settings)
		self.delete_files_button = tk.Button(self.file_deletion_frame,text='Delete Files',command=self.delete_files)
		self.set_algorithms()

		self.files_list.xview()
		self.files_list.yview()

		self.alignment_frames[0].pack(side=tk.TOP,pady=10)
		self.choose_drive_menu.pack(side=tk.LEFT,pady=5)
		self.scan_drive_button.pack(side=tk.LEFT,padx=3)
		self.delete_files_label.pack()
		self.files_list.pack(pady=5)
		self.alignment_frames[1].pack(side=tk.TOP)
		self.select_deselect.pack(side=tk.LEFT,padx=3)
		self.advanced_button.pack(side=tk.LEFT,padx=3)
		self.delete_files_button.pack(side=tk.TOP,padx=3)
		self.alignment_frames[2].pack()


	def clean_sector_init(self):
		self.clean_sector_label = tk.Label(self.clean_sector_frame,text='')


	def format_drive_init(self):
		pass


	def set_drives_menu(self):
		self.get_drives()
		self.default_drive = tk.StringVar(self.parent)
		self.default_drive.set(self.drives[0])
		self.choose_drive_menu = tk.OptionMenu(self.alignment_frames[0],self.default_drive,*self.drives)
		self.choose_drive_menu.config(width=35)
		self.choose_drive_tooltip = CreateToolTip(self.choose_drive_menu,'Choose a drive')

		self.choose_drive_menu.pack()


	def set_algorithms(self):
		self.wiping_algorithms = ['Zero fill','Secure Erase','Schneier','Random Data']
		self.default_algorithm = tk.StringVar()
		self.default_algorithm.set(self.wiping_algorithms[0])
		self.choose_algorithm_label = tk.Label(self.alignment_frames[2],text='Choose an Algorithm: ')
		self.choose_algorithm_menu = tk.OptionMenu(self.alignment_frames[2],self.default_algorithm,*self.wiping_algorithms)

		self.choose_algorithm_label.pack(side=tk.LEFT,padx=3)
		self.choose_algorithm_menu.pack(side=tk.LEFT,padx=3)


	def get_drives(self):
		self.drives = get_drivesWin()


	def scan_drive(self):
		for x in range(30):
			self.files_list.insert(x,x)


	def delete_files(self):
		pass 


	def format_drive(self):
		pass


	def advanced_settings(self):
		if self.is_advanced.get() == 1:
			self.delete_files_button.pack_forget()
			self.advanced_settings_frame.pack()
			self.delete_files_button.pack()
		else:
			self.advanced_settings_frame.pack_forget()


	def select_deselect_files(self):
		if self.select_value.get() == 1:
			self.files_list.select_set(0,tk.END)
		else:
			self.files_list.selection_clear(0,tk.END)						