import bitstring as bt
import random as rand
from functools import reduce

def reverse_message(message):
	ascii_equivalent = [ord(x) for x in message]
	ascii_reversed = ascii_equivalent[::-1]
	return ascii_reversed

def generate_key(reversed):
	return rand.randint(len(reversed),max(reversed))

def increment_bits(reversed,increment):
	return list(map(lambda x: ((x+increment)%57)+65,reversed))

def encrypt_message(message):
	reverse = reverse_message(message)
	key = generate_key(reverse)
	print(key)
	inc_list = increment_bits(reverse,key)
	return (list(map(lambda x: chr(x), inc_list)),key)

if __name__ == '__main__':
	print(''.join(encrypt_message('hello world')[0]))
