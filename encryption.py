from PIL import ImageTk, Image
from functools import partial
import tkinter as tk
from encryptionfunctions import *

class Encryption(tk.Frame):

	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		self.controller = controller
		self.parent = parent
		
		self.alignment_frames = []
		self.encryption_frame = tk.Frame(self.parent,highlightthickness=2,highlightbackground='black')
		self.decryption_frame = tk.Frame(self.parent,highlightthickness=2,highlightbackground='black')

		self.set_algorithms()

		self.encryption_init()
		self.decryption_init()

		self.encryption_frame.pack(fill=tk.X)
		self.decryption_frame.pack(fill=tk.X)


	def encryption_init(self):
		self.encryption_label = tk.Label(self.encryption_frame,text='Encryption')
		self.enter_message_label = tk.Label(self.encryption_frame,text='Enter Message: ')
		self.enter_message_text = tk.Text(self.encryption_frame,height=5)
		self.encrypt_button = tk.Button(self.encryption_frame,text='Encrypt',command=self.encrypt)

		self.encryption_label.pack()
		self.enter_message_label.pack()
		self.enter_message_text.pack()
		self.encrypt_button.pack(pady=5)


	def set_algorithms(self):
		self.algorithms = ['Caesar Cipher','Emoji','3DES','Sample','Sample']
		self.default_algorithm = tk.StringVar(self.parent)
		self.default_algorithm.set(self.algorithms[0])
		self.choose_algorithm_menu = tk.OptionMenu(self.parent,self.default_algorithm,*self.algorithms)
		self.choose_algorithm_menu.config(width=35)
		
		self.choose_algorithm_menu.pack()


	def decryption_init(self):
		self.alignment_frames.append(tk.Frame(self.decryption_frame))
		self.decryption_label = tk.Label(self.decryption_frame,text='Decryption')
		self.enter_crypto_label = tk.Label(self.decryption_frame,text='Enter Crypto Message: ')
		self.enter_crypto_text = tk.Text(self.decryption_frame,height=5)
		self.enter_key_label = tk.Label(self.alignment_frames[0],text='Key:')
		self.enter_key_entry = tk.Entry(self.alignment_frames[0])
		self.decrypt_button = tk.Button(self.decryption_frame,text='Decrypt',command=self.decrypt)

		self.decryption_label.pack()
		self.enter_crypto_label.pack()
		self.enter_crypto_text.pack()
		self.alignment_frames[0].pack()
		self.enter_key_label.pack(side=tk.LEFT)
		self.enter_key_entry.pack(side=tk.LEFT)
		self.decrypt_button.pack(pady=5)


	def encrypt(self):
		if self.default_algorithm.get() == 'Caesar Cipher':
			tk.tkMessageBox.showinfo('Result',caesar_cipher(self.enter_message_text.get('1.0','end-1c'))[0])



	def decrypt(self):
		pass