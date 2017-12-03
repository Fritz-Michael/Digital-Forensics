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


def emoji_encrypt(message):
	dictionary = [':)', ':D', ':(', 'XD', '>_<', '-_-', ';(', 'o_O', 'xC', ';D',
	'xP', 'xb', 'B-)', 'B-(', 'X)', 'X(', ':3', ':*', ';)', '>:(',
	'>:)', ":'(", 'XO', 'D:', '(:', ':/']

	ciphertext = ''
	cipher = 3
	isCaps = False
	sub = 0
	for char in message:
		value = ord(char)
		if value != 32:
			if value < 95:
				isCaps = True
				sub = 65
			else:
				isCaps = False
				sub = 97
			temp = (value - sub + cipher) % len(dictionary)
			ciphertext = ciphertext + dictionary[temp]
		else:
			ciphertext = ciphertext + ' '

	return ciphertext


if __name__ == '__main__':
	temp = emoji_encrypt('Lorem Ipsum')
	print(temp)