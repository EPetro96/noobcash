#import blockchain
from transaction import *
import json

import hashlib

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


class Block:
	def __init__(self, index, previousHash, timestamp, nonce, listOfTransactions):
		##set
		self.index = index
		self.previousHash = previousHash
		self.timestamp = timestamp
		self.hash = 42 					#dummy initializer
		self.nonce = nonce
		self.listOfTransactions = listOfTransactions

	def __eq__(self,other):
		return sorted(self.listOfTransactions) == sorted(other.listOfTransactions)


	def to_dict(self):
		newlist = []
		for trans in self.listOfTransactions:
			newlist.append(trans.to_dict())
		#newlist = json.dumps(newlist)
		return OrderedDict({'block_index': self.index,
							'previousHash': self.previousHash,
							'timestamp': self.timestamp,
							'hash': self.hash,
							'nonce': self.nonce,
							'listOfTransactions': newlist,
							})
		
	
	def myHash(self):
		#CHECK AGAIN IF THAT"S WHAT WE WANT
		#calculate self.hash
		guess = (str(self.previousHash)+str(self.nonce)+str(self.timestamp)).encode()
		return hashlib.sha256(guess).hexdigest()
        


	# def add_transaction(self, transaction transaction, blockchain blockchain):
	# 	#add a transaction to the block
		

	# 	self.listOfTransactions.append(transaction)
