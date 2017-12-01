import bitstring as bt
import random as rand
from functools import reduce

def reverse_message(message):
	ascii_equivalent = [ord(x) for x in message]
	ascii_reversed = ascii_equivalent[::-1]
	return ascii_reversed

def generate_key(reversed):
	return rand.randint(len(reversed),max(reversed))

def increment_message(reversed,key):
	return list(map(lambda x: ((x+key)%57)+66,reversed))

def reverse_to_char(message):
	temp = message[::-1]
	return list(map(lambda x: chr(x), temp))

def to_ascii(message):
	return [ord(x) for x in message]

def decrement_message(message, key):
	temp = list(map(lambda x: x-65,message))
	return list(map(lambda x: (x-key)%57,temp))

def encrypt_message(message):
	reverse = reverse_message(message)
	key = generate_key(reverse)
	inc_list = increment_message(reverse,key)
	return (list(map(lambda x: chr(x), inc_list)),key)

def decrypt_message(message, key):
	message = to_ascii(message)
	dec_list = decrement_message(message,key)
	return reverse_to_char(dec_list)



if __name__ == '__main__':
	pass