import blockchain


class Block:
	def __init__(self, previousHash, timestamp, nonce, listOfTransactions):
		##set

		self.previousHash = previousHash
		self.timestamp = timestamp
		self.hash = self.myHash
		self.nonce = nonce
		self.listOfTransactions = listOfTransactions
	
	def myHash:
		#calculate self.hash


	def add_transaction(transaction transaction, blockchain blockchain):
		#add a transaction to the block