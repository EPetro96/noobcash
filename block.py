import blockchain
import json


class Block:
	def __init__(self, index, previousHash, timestamp, nonce, listOfTransactions):
		##set
		self.index = index
		self.previousHash = previousHash
		self.timestamp = timestamp
		self.hash = self.myHash()
		self.nonce = nonce
		self.listOfTransactions = listOfTransactions
	
	def myHash:
		#CHECK AGAIN IF THAT"S WHAT WE WANT
		#calculate self.hash
		# We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        
		return hashlib.sha256(block_string).hexdigest()


	def add_transaction(self, transaction transaction, blockchain blockchain):
		#add a transaction to the block
		

		self.listOfTransactions.append(transaction)