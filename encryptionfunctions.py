import bitstring as bt
import random as rand
from functools import reduce

def reverse_message_bits(message):
	bits = [bin(ord(x))[2:].zfill(8) for x in message]
	print(bits)
	bits = [bin(ord(x))[:1:-1].zfill(8) for x in message]
	#for decryption: bits = [x[::-1] for x in bits]
	return bits

def random_increment(bits):
	zero = reduce(lambda x,y: x+y, list(map(lambda x: x.count('0'),bits)))
	one = reduce(lambda x,y: x+y, list(map(lambda x: x.count('1'),bits)))
	random_number = rand.randint(0,max(one,zero))
	return (zero**random_number) % one

def increment_bits(bits,increment):
	temp = int(bits[0],2) + 10
	encrypted = [bin((int(bit,2)+increment)%255)[2:].zfill(8) for bit in bits]
	encrypted.insert(0,bin(increment)[2:].zfill(8))
	#print(encrypted)
	encrypted = list(map(lambda x: chr(int(x,2)),encrypted))
	return encrypted
	#for decryption: print(bin(ord(encrypted[0]))[2:].zfill(8))

if __name__ == '__main__':
	#print(random_increment(reverse_message_bits('hello world')))
	#(x+y)mod a = b
	#(b-y)mod a = x
	#print((1-10)%255)
	bits = reverse_message_bits('*r:: F:21')
	increment = random_increment(bits)
	encrypted = increment_bits(bits,increment)
	string = ''
	for x in encrypted:
		string += x
	print(string)
