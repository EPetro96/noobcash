#import blockchain
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
	
	def myHash:
		#CHECK AGAIN IF THAT"S WHAT WE WANT
		#calculate self.hash
		guess = (str(self.listOfTransactions)+str(self.previousHash)+str(self.nonce)+str(self.timestamp)).encode()
        return hashlib.sha256(guess).hexdigest()
        


	# def add_transaction(self, transaction transaction, blockchain blockchain):
	# 	#add a transaction to the block
		

	# 	self.listOfTransactions.append(transaction)