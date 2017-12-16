from functools import partial
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from steganographyfunctions import *

class Steganography(tk.Frame):

	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		self.controller = controller
		self.parent = parent

		self.encryption_frame = tk.Frame(self.parent,bd=2,relief=tk.SUNKEN)
		self.decryption_frame = tk.Frame(self.parent,bd=2,relief=tk.SUNKEN)
		self.alignment_frames = []

		self.encryption_init()
		self.decryption_init()

		self.encryption_frame.pack(fill=tk.X)
		self.decryption_frame.pack(fill=tk.X)


	def choose_file(self):
		self.file = filedialog.askopenfilename(initialdir=self.file,title='Select Directory',filetypes=(('PNG files','*.png'),
																										     ('JPG files','*.jpg;*.jpeg'),
																										     ('WAV files','*.wav')))
		self.choose_file_label.config(text=self.file)


	def choose_output(self):
		self.output = filedialog.askopenfilename(initialdir=self.output,title='Select Directory',filetypes=(('PNG files','*.png'),
																										     ('JPG files','*.jpg;*.jpeg'),
																										     ('WAV files','*.wav')))
		self.choose_crypto_label.config(text=self.output)


	def encrypt(self):
		if self.message_box.get('1.0','end-1c') != '':
			if self.file != '' and self.file != '/':
				if '.png' in self.file:
					self.output_file = filedialog.asksaveasfilename(initialdir=self.file,title='Select Directory',filetypes=(('PNG files','*.png'),))
					if self.output_file != '':
						png_encode(self.file,self.message_box.get('1.0','end-1c'),self.output_file + '.png')
						self.message_box.delete('1.0',tk.END)
						self.file = '/'
						self.choose_file_label.config(text=self.file)
					else:
						messagebox.showwarning('Error','Invalid File Destination!')
				elif '.jpg' in self.file or '.jpeg' in self.file:
					self.output_file = filedialog.asksaveasfilename(initialdir=self.file,title='Select Directory',filetypes=(('JPG files','*.jpg;*.jpeg'),))
					if self.output_file != '':
						jpg_tiff_encode(self.file,self.message_box.get('1.0','end-1c'),self.output_file + '.jpg')
						self.message_box.delete('1.0',tk.END)
						self.file = '/'
						self.choose_file_label.config(text=self.file)
					else:
						messagebox.showwarning('Error','Invalid File Destination!')
				elif '.wav' in self.file:
					self.output_file = filedialog.asksaveasfilename(initialdir=self.file,title='Select Directory',filetypes=(('WAV files','*.wav'),))
					print(self.output_file)
				else:
					messagebox.showwarning('Error','Invalid File!')
			else:
				messagebox.showwarning('Error','Choose a file first!')
		else:
			messagebox.showwarning('Error','Please input a message!')


	def decrypt(self):
		if self.output != '' and self.output != '/':
			if '.png' in self.output:
				try:
					msg = png_decode(self.output)
				except:
					messagebox.showwarning('Error','Nothing to decrypt!')
				else:
					self.cipher_box.config(state=tk.NORMAL)
					self.cipher_box.delete('1.0',tk.END)
					self.cipher_box.insert(tk.END,msg)
					self.cipher_box.config(state=tk.DISABLED)
				self.output = '/'
				self.choose_crypto_label.config(text=self.output)
			elif '.jpg' in self.output or '.jpeg' in self.output:
				try:
					msg = jpg_tiff_decode(self.output)
				except:
					messagebox.showwarning('Error','Nothing to decrypt!')
				else:
					self.cipher_box.config(state=tk.NORMAL)
					self.cipher_box.delete('1.0',tk.END)
					self.cipher_box.insert(tk.END,msg)
					self.cipher_box.config(state=tk.DISABLED)
				self.output = '/'
				self.choose_crypto_label.config(text=self.output)
			elif '.wav' in self.output:
				pass
			else:
				messagebox.showwarning('Error','Invalid File!')
		else:
			messagebox.showwarning('Error','Choose a file first!')


	def encryption_init(self):
		self.file = '/'
		self.alignment_frames.append(tk.Frame(self.encryption_frame))
		self.encryption_label = tk.Label(self.encryption_frame,text='Encryption',font='Helvetica 11 bold')
		self.choose_file_label = tk.Label(self.alignment_frames[0],text=self.file)
		self.choose_file_button = tk.Button(self.alignment_frames[0],text='Choose a file',command=self.choose_file)
		self.message_label = tk.Label(self.encryption_frame,text='Enter Message:')
		self.message_box = tk.Text(self.encryption_frame,height=5)
		self.encrypt_button = tk.Button(self.encryption_frame,text='Encrypt',command=self.encrypt)

		self.encryption_label.pack(side=tk.TOP,pady=3)
		self.alignment_frames[0].pack(side=tk.TOP,pady=10)
		self.choose_file_label.pack(side=tk.TOP)
		self.choose_file_button.pack(side=tk.TOP)
		self.message_label.pack(side=tk.TOP,padx=8)
		self.message_box.pack(side=tk.TOP,fill=tk.X,pady=9)
		self.encrypt_button.pack()


	def decryption_init(self):
		self.output = '/'
		self.alignment_frames.append(tk.Frame(self.decryption_frame))
		self.decryption_label = tk.Label(self.decryption_frame,text='Decryption',font='Helvetica 11 bold')
		self.choose_crypto_label = tk.Label(self.alignment_frames[1],text=self.output)
		self.choose_crypto_button = tk.Button(self.alignment_frames[1],text='Choose a file',command=self.choose_output)
		self.cipher_label = tk.Label(self.decryption_frame,text='Message:')
		self.cipher_box = tk.Text(self.decryption_frame,height=5)
		self.cipher_box.config(state=tk.DISABLED)
		self.decrypt_button = tk.Button(self.decryption_frame,text='Decrypt',command=self.decrypt)

		self.decryption_label.pack(side=tk.TOP,pady=3)
		self.alignment_frames[1].pack(side=tk.TOP,pady=8)
		self.choose_crypto_label.pack(side=tk.TOP)
		self.choose_crypto_button.pack(side=tk.TOP)
		self.cipher_label.pack(side=tk.TOP,padx=8)
		self.cipher_box.pack(side=tk.TOP,fill=tk.X,pady=9)
		self.decrypt_button.pack()