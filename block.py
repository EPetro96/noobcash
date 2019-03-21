#import blockchain
from transaction import *
import json


class Block:
	def __init__(self, index, previousHash, timestamp, nonce, listOfTransactions):
		##set
		self.index = index
		self.previousHash = previousHash
		self.timestamp = timestamp
		self.hash = 42 					#dummy initializer
		self.nonce = nonce
		self.listOfTransactions = listOfTransactions


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
		
	
	def myHash():
		#CHECK AGAIN IF THAT"S WHAT WE WANT
		#calculate self.hash
		guess = (str(self.listOfTransactions)+str(self.previousHash)+str(self.nonce)+str(self.timestamp)).encode()
		return hashlib.sha256(guess).hexdigest()
        


	# def add_transaction(self, transaction transaction, blockchain blockchain):
	# 	#add a transaction to the block
		

	# 	self.listOfTransactions.append(transaction)
