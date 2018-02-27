from stegano import lsb
from stegano import exifHeader
import wave as wv
import struct
import array
import shutil


def png_encode(file_name, message, mfile_name):
	secret = lsb.hide(file_name, message)
	secret.save(mfile_name)

def png_decode(mfile_name):
	return lsb.reveal(mfile_name)

def jpg_tiff_encode(file_name, message, mfile_name):
	secret = exifHeader.hide(file_name, mfile_name, secret_message=message)

def jpg_tiff_decode(mfile_name):
	return exifHeader.reveal(mfile_name).decode()

def sample():
	audio = wv.open('C:\\Users\\fritz\\Downloads\\sample.wav','rb')
	total_frames = audio.getnframes()
	audio.setpos(5000)
	temp = audio.readframes(total_frames)
	samp = [byte for byte in temp]
	print(total_frames)
	print(len(samp)/4)
	#array.array('B',samp).tostring()
	audio.close()

	message = 'hello world'
	msg_list = [ord(x) for x in message]

def get_audio_frames(file):
	audio = wv.open(file,'rb')
	total_frames = audio.getnframes()
	frames = audio.readframes(total_frames)
	audio.close()
	return frames

def frames_to_info(frames):
	return [x for x in frames]

def message_to_bytes(message):
	msg_list = [ord(x) for x in message]
	byte_message = [x.to_bytes(1,byteorder='little') for x in msg_list]
	return byte_message

def message_size_bits(message):
	num_bytes = bin(len([x for x in message]))[2:].zfill(8)
	bits = []
	for x in range(len(num_bytes)):
		for bit in num_bytes[x]:
			bits.append(int(bit))
	return bits

def message_to_bits(message):
	msg_list = [bin(ord(x))[2:].zfill(8) for x in message]
	bits = []
	for x in range(len(msg_list)):
		for bit in msg_list[x]:
			bits.append(int(bit))
	return bits

def get_parameters(file):
	audio = wv.open(file,'rb')
	params = audio.getparams()
	audio.close()
	return audio.getparams()

def write_new_frame(file,outputfile,frame):
	audio = wv.open(outputfile,'wb')
	audio.setparams(get_parameters(file))
	audio.writeframes(frame)
	audio.close()

def encrypt_wav(file,msg,output):
	shutil.copyfile(file,output)
	frames = frames_to_info(get_audio_frames(file))
	size_bits = message_size_bits(msg) 
	for x in range(8):
		if size_bits[x] == 0:
			if frames[x] % 2 != 0:
				frames[x] += 1
		else:
			if frames[x] % 2 == 0:
				frames[x] += 1
	message_bits = message_to_bits(msg)
	for x in range(8,len(frames)):
		try:
			if message_bits[x-8] == 0:
				if frames[x] % 2 != 0:
					frames[x] += 1
			else:
				if frames[x] % 2 == 0:
					frames[x] += 1
		except IndexError:
			break
	bytes_frame = array.array('B',frames).tostring()
	write_new_frame(file,output,bytes_frame)

def decrypt_wav(output):
	frames = frames_to_info(get_audio_frames(output))
	size_bits = []
	for x in range(8):
		size_bits.append(bin(frames[x])[2:].zfill(8)[7])
	message_size = int(''.join(size_bits),2)
	message_bits = []
	for x in range(8,message_size*8+8):
		message_bits.append(bin(frames[x])[2:].zfill(8)[7])
	temp_message = []
	for x in range(message_size):
		temp_message.append([])
	ctr = 0
	for x in range(len(message_bits)):
		temp_message[ctr].append(message_bits[x])
		if (x + 1) % 8 == 0:
			ctr += 1
	message = [''.join(x) for x in temp_message]
	message = ''.join([chr(int(x,2)) for x in message])
	return message

if __name__ == '__main__':
	pass