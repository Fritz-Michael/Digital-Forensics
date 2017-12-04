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

	ciphertext = ''
	cipher = rand.randint(1,26)
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

	return (ciphertext,cipher)


def emoji_decrypt(message,key):
	dictionary = [':)', ':D', ':(', 'XD', '>_<', '-_-', ';(', 'o_O', 'xC', ';D',
	'xP', 'xb', 'B-)', 'B-(', 'X)', 'X(', ':3', ':*', ';)', '>:(',
	'>:)', ":'(", 'XO', 'D:', '(:', ':/']
	print(message)
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
	num2 = list(map(lambda x: (x-key)%len(dictionary),num))
	print(num2)



if __name__ == '__main__':
	temp = emoji_encrypt('hello world')
	emoji_decrypt(temp[0],temp[1])