import bitstring as bt
import random as rand
from functools import reduce
import struct

def caesar_cipher(message):
	key = rand.randint(1,26)
	translated = ''
	for symbol in message:
		if symbol.isalpha():
			num = ord(symbol)
			num += key

			if symbol.isupper():
				if num > ord('Z'):
					num -= 26
				elif num < ord('A'):
					num += 26
			elif symbol.islower():
				if num > ord('z'):
					num -= 26
				elif num < ord('a'):
					num += 26

			translated += chr(num)
		else:
			translated += symbol
	return (translated,key)


def decrypt_caesar_cipher(message,key):
	translated = ''
	for symbol in message:
		if symbol.isalpha():
			num = ord(symbol)
			num -= int(key)

			if symbol.isupper():
				if num > ord('Z'):
					num -= 26
				elif num < ord('A'):
					x = ord('A') - num
					y = ord('Z') - x
					num = y + 1
			elif symbol.islower():
				if num > ord('z'):
					num -= 26
				elif num < ord('a'):
					x = ord('a') - num
					y = ord('z') - x
					num = y + 1

			translated += chr(num)
		else:
			translated += symbol
	return translated


def emoji_encrypt(message):
	dictionary = [':)', ':D', ':(', 'XD', '>_<', '-_-', ';(', 'o_O', 'xC', ';D',
	'xP', 'xb', 'B-)', 'B-(', 'X)', 'X(', ':3', ':*', ';)', '>:(',
	'>:)', ":'(", 'XO', 'D:', '(:', ':/']
	message = message.lower()
	ciphertext = ''
	cipher = rand.randint(1,15)
	isCaps = False
	sub = 97
	for char in message:
		value = ord(char)
		if value != 32:
			if value < 95:
				isCaps = True
				#sub = 65
			else:
				isCaps = False
				#sub = 97
			temp = (value - sub + cipher) % len(dictionary)
			ciphertext = ciphertext + dictionary[temp]
		else:
			ciphertext = ciphertext + ' '

	return (ciphertext,cipher)


def emoji_decrypt(message,key):
	dictionary = [':)', ':D', ':(', 'XD', '>_<', '-_-', ';(', 'o_O', 'xC', ';D',
	'xP', 'xb', 'B-)', 'B-(', 'X)', 'X(', ':3', ':*', ';)', '>:(',
	'>:)', ":'(", 'XO', 'D:', '(:', ':/']
	temp = list(message)
	num = []
	num2 = []
	x = 0
	while x < len(message):
		if ord(temp[x]) == 32:
			num.append(32)
		for y in range(len(dictionary)):
			max = x+1
			if max > len(message)-1:
				pass
			else:
				if str(temp[x]+temp[x+1]) == dictionary[y]:
					x += 1
					num.append(y)
					break
			max = x+2
			if max > len(message)-1:
				pass
			else:
				if str(temp[x]+temp[x+1]+temp[x+2]) == dictionary[y]:
					x += 2
					num.append(y)
		x += 1

	num2 = []
	for x in num:
		if x == 32:
			num2.append(32)
		else:
			num2.append((int(x)-int(key))%len(dictionary))
	characters = []
	for x in num2:
		if x == 32:
			characters.append(' ')
		else:
			characters.append(chr(x+97))
	return ''.join(characters)


def encrypt_XOR(message):
	key = bin(rand.randint(1,26))[2::]
	temp = [bin(ord(x))[2::] for x in message]
	encrypted = list(map(lambda x: int(x,2) ^ int(key,2),temp))
	encrypted = [bin(x)[2::].zfill(8) for x in encrypted]
	return (''.join(encrypted),key)


def decrypt_XOR(crypto,key):
	temp = [crypto[x:x+8] for x in range(0,len(crypto),8)]
	xor = list(map(lambda x: int(x,2) ^ int(key,2),temp))
	message = [chr(x) for x in xor]
	return ''.join(message)

def encrypt_fritz(message):
	key = rand.randint(97,122)
	passes = rand.randint(1,9)
	text = chr(key) + message
	rotate_text = text[passes:] + text[:passes]
	cipher_text = ''.join([chr((ord(x)^key) + 65) for x in rotate_text])
	passes = chr(passes+65)
	key = chr(key) + passes
	return (cipher_text,key)

def decrypt_fritz(crypto,key):
	passes = (ord(key[1]) - 65) * -1
	key = key[0]
	text = ''.join([chr( (ord(x)-65) ^ ord(key) ) for x in crypto])
	rotate_text = text[passes:] + text[:passes]
	return rotate_text[1:]

def encrypt_sample(message):
	key = rand.randint(1,9)
	temp = [ord(x)-65 for x in message]
	xor = [x^key for x in temp]
	cipher_text = [chr(x+65) for x in xor]
	return (''.join(cipher_text),key)

def decrypt_sample(crypto,key):
	temp = [ord(x)-65 for x in crypto]
	xor = [x^int(key) for x in temp]
	return ''.join([chr(x+65) for x in xor])

if __name__ == '__main__':
	temp = encrypt_sample('panget si pepeds')
	print(decrypt_sample(temp[0],temp[1]))
	