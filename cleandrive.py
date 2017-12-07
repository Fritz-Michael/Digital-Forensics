from PIL import ImageTk, Image
from functools import partial
import tkinter as tk
from tkinter import *
from tkinter import ttk
from filerecoveryfunctions import *
from formatdrivefunctions import *
from deletev2 import *


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


class Wait(tk.Tk):

	def __init__(self,*args,**kwargs):
		tk.Tk.__init__(self,*args,**kwargs)
		
		self.label = tk.Label(self,text='Done!')
		self.label.pack()

	def exit(self):
		self.quit()


class CleanDrive(tk.Frame):

	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		self.controller = controller
		self.parent = parent

		self.file_deletion_frame = tk.Frame(self.parent,highlightthickness=2,highlightbackground='black')
		self.clean_sector_frame = tk.Frame(self.parent,highlightthickness=2,highlightbackground='black')
		self.format_drive_frame = tk.Frame(self.parent,highlightthickness=2,highlightbackground='black')

		self.file_deletion_init()
		self.clean_sector_init()
		self.format_drive_init()
		
		self.file_deletion_frame.pack()
		self.clean_sector_frame.pack(fill=tk.X)
		self.format_drive_frame.pack(fill=tk.BOTH)		


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
		#self.files_list = tk.Listbox(self.file_deletion_frame,selectmode=tk.MULTIPLE,height=7,width=100)

		self.files_list = ttk.Treeview(self.file_deletion_frame,height=5)
		self.files_list['columns'] = ('written','accessed','created')
		self.files_list.column('written',width=100)
		self.files_list.column('accessed',width=100)
		self.files_list.column('created',width=100)
		self.files_list.heading('written',text='Written')
		self.files_list.heading('accessed',text='Accessed')
		self.files_list.heading('created',text='Created')
		self.files_list.insert('',0,text='Sample',values=('1','2','3'))
		self.files_list.insert('',0,text='Sample',values=('2','3','4'))

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
		self.alignment_frames.append(tk.Frame(self.clean_sector_frame))
		self.clean_sector_label = tk.Label(self.clean_sector_frame,text='Delete Sector')
		self.sector_number_label = tk.Label(self.alignment_frames[3],text='Sector Number: ')
		self.sector_number_entry = tk.Entry(self.alignment_frames[3])
		self.delete_sector_button = tk.Button(self.clean_sector_frame,text='Delete Sector',command=self.delete_sector)

		self.clean_sector_label.pack(pady=10)
		self.alignment_frames[3].pack(side=tk.TOP)
		self.sector_number_label.pack(side=tk.LEFT)
		self.sector_number_entry.pack(side=tk.LEFT)
		self.delete_sector_button.pack(pady=10)


	def format_drive_init(self):
		self.format_drive_label = tk.Label(self.format_drive_frame,text='Format Drive')
		self.format_drive_button = tk.Button(self.format_drive_frame,text='Format',command=self.format_drive)
		self.format_drive_label.pack(pady=10)

		self.set_file_formats()
		self.format_drive_button.pack(pady=5)


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


	def set_file_formats(self):
		self.alignment_frames.append(tk.Frame(self.format_drive_frame))

		self.file_format = ['NTFS','FAT32','exFAT']
		self.default_file_format = tk.StringVar()
		self.default_file_format.set(self.file_format[0])
		self.choose_format_label = tk.Label(self.alignment_frames[4],text='Choose Filesystem: ')
		self.choose_format_menu = tk.OptionMenu(self.alignment_frames[4],self.default_file_format,*self.file_format)

		self.alignment_frames[4].pack(pady=5)
		self.choose_format_label.pack(side=tk.LEFT)
		self.choose_format_menu.pack(side=tk.LEFT)


	def get_drives(self):
		self.drives = get_drivesWin()


	def scan_drive(self):
		self.disable_buttons()
		# path = '\\\\.\\' + self.default_drive.get() + ':'
		# rootPath = self.default_drive.get()
		# mft_location = mftlocation(path,roothPath)
		self.enable_buttons()


	def delete_files(self):
		pass 


	def format_drive(self):
		self.disable_buttons()
		path = self.default_drive.get() + ':\\'
		if self.default_file_format.get() == 'NTFS':
			format_drive_to_NTFS(path)
		elif self.default_file_format.get() == 'FAT32':
			format_drive_to_FAT32(path)
		elif self.default_file_format.get() == 'exFAT':
			format_drive_to_exFAT(path)
		self.enable_buttons()
		temp = Wait()
		temp.mainloop()


	def advanced_settings(self):
		if self.is_advanced.get() == 1:
			self.delete_files_button.pack_forget()
			self.advanced_settings_frame.pack()
			self.delete_files_button.pack()
		else:
			self.advanced_settings_frame.pack_forget()


	def select_deselect_files(self):
		if self.select_value.get() == 1:
			print(self.files_list.get_children()[0].text)
		else:
			self.files_list.selection_clear(0,tk.END)			


	def delete_sector(self):
		pass			


	def disable_buttons(self):
		self.delete_files_button.config(state=tk.DISABLED)
		self.format_drive_button.config(state=tk.DISABLED)
		self.delete_sector_button.config(state=tk.DISABLED)
		self.scan_drive_button.config(state=tk.DISABLED)


	def enable_buttons(self):
		self.delete_files_button.config(state=tk.ACTIVE)
		self.format_drive_button.config(state=tk.ACTIVE)
		self.delete_sector_button.config(state=tk.ACTIVE)
		self.scan_drive_button.config(state=tk.ACTIVE)		
