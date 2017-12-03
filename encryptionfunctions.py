import bitstring as bt
import random as rand
from functools import reduce


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
			num -= key

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
	return translated


if __name__ == '__main__':
	temp = caesar_cipher('Lorem Ipsum')
	print(temp)
	print(decrypt_caesar_cipher(temp[0],temp[1]))