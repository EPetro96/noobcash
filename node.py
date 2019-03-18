import block
import wallet
import blockchain


class node:
	def __init__(self, identifier, chain, current_id_count, NBCs):
		self.id = identifier
		# self.NBC=100;
		##set

		#self.transaction_pool = [] of transactions
		self.chain = chain
		self.current_id_count = current_id_count
		#self.NBCs = NBCs
		self.wallet = self.create_wallet()
		
		self.UTXOs = []	#list of dictionairies
		self.utxo_unique_id = 0
		
		#create a block???
		#self.block = create_new_block

		self.ring[] #???  #here we store information for every node, as its id, its address (ip:port) its public key and its balance 
		#list of dictionaries {'id', 'ip_port', 'public_key', 'balance'}




	def create_new_block(listOfTransactions):
		lastblock = self.chain[-1]
		previousHash = lastblock.hash 	#STEKEI?
		timestamp = time()

		b = block(previousHash, timestamp, 0, listOfTransactions)
		# for transaction in listOfTransactions:
		# 	b.add_transaction(transaction)
		return b

	def create_wallet(self):
		#create a wallet for this node, with a public key and a private key
		random_gen = Crypto.Random.new().read
		private_key = RSA.generate(1024, random_gen)
		public_key = private_key.publickey()		#check for binascii
		return wallet(public_key, private_key, [])


	def register_node_to_ring(self, public_key, ip, port):
		if (self.id == 0):		#if i'm the bootstrap node
			identifier = self.current_id_count
			ring.append({'id':identifier,'ip_port':ip_port,'public_key':public_key,'balance':balance})
			self.current_id_count++
			if(self.current_id_count == 5):
				#broadcast the ring


		#add this node to the ring, only the bootstrap node can add a node to the ring after checking his wallet and ip:port address
		#bottstrap node informs all other nodes and gives the request node an id and 100 NBCs


	def create_transaction(self, sender, receiver, signature, amount): 	#sender-receiver ids
		sender_public_key = ring{'id' }	#tbd
		recv_public_key = ring{str(receiver)}	#tbd
		
		acc = 0
		transaction_in = []
		for utxo in self.UTXOs:
			acc += utxo['amount']
			transaction_in.append(utxo['unique_UTXO_id'])
			if (acc >= amount):
				break
		if (acc < amount):
			return null	#null?

		identity = 42	#check again

		#utxo_for_sender = {'unique_UTXO_id':__, 'transaction_id': identity, 'recipient': sender_public_key, 'amount':self.wallet.balance(self) - amount}
		# self.UTXOs.append(utxo_for_sender)
		#utxo_for_receiver = {'unique_UTXO_id':___ , 'transaction_id': identity, 'recipient': recv_public_key, 'amount':amount}
		#self.UTXOs.append(utxo_for_receiver)
		#transaction_out = [utxo_for_sender, utxo_for_receiver]
		transaction_out = []
		t = Transaction(sender_public_key, sender_private_key, recv_public_key, amount, identity, transaction_in, transaction_out)
		validate_transaction(t)	#if we don't receive our own transaction from broadcast 
		return t  #from rest --> broadcast it

	def broadcast_transaction():
		return list_of_ips



	def validate_transaction(self, transaction):		#it's called from rest when receiving a transaction
		#use of signature and NBCs balance
		#a)verify signature
		sender_public_key = transaction.sender_address
		if (transaction.verify_signature(sender_public_key)):
			if (all(elem in self.UTXOs  for elem in transaction.transaction_inputs)):	#check MY utxos for transaction.inputs. 
				for utxo in transaction.transaction_inputs:
					self.UTXOs.remove(utxo)		#If valid, take trans_inputs out of my UTXOS.

				#Create two new utxos for THIS transaction and add them to my utxos
				utxo_for_sender = {'unique_UTXO_id':__, 'transaction_id': identity, 'recipient': sender_public_key, 'amount':self.wallet.balance(self) - amount}
				self.UTXOs.append(utxo_for_sender)
				utxo_for_receiver = {'unique_UTXO_id':___ , 'transaction_id': identity, 'recipient': recv_public_key, 'amount':amount}
				self.UTXOs.append(utxo_for_receiver)
				transaction_out = [utxo_for_sender, utxo_for_receiver]
				transaction.transaction_outputs = transaction_out
				add_transaction_to_block(transaction)
			

	def add_transaction_to_block(self, transaction):		
		#if enough transactions  mine
		transaction_pool.append(transaction)
		utxo_for_receiver = transaction.transaction_outputs[1]
		# if (utxo_for_receiver['recipient'] == self.wallet.public_key):	#if trans_out is about me, append it to my utxos
		self.UTXOs.append(utxo_for_receiver)
		if (len(transaction_pool) == capacity):
			block = create_new_block(self.transaction_pool)
			mined_block = mine_block(block)
			return mined_block		#then broadcast_block from rest_api



	def mine_block(block):
		nonce = 0
        while self.valid_proof(nonce, block) is False:
            nonce += 1
		block.nonce = nonce
		self.chain.append(block)
		return block


	def broadcast_block():
		return list_of_ips

		

	def valid_proof(nonce, block, difficulty=MINING_DIFFICULTY):
		transactions = block.listOfTransactions
		last_hash = block.previousHash
		timestamp = block.timestamp
		guess = (str(transactions)+str(last_hash)+str(nonce)+str(timestamp)).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
		if (guess_hash[:difficulty] == '0'*difficulty):
			block.hash = guess_hash
			return True
		else:
			return False




	#concencus functions

	def valid_chain(self, chain):
		#check for the longer chain accroose all nodes


	def resolve_conflicts(self):
		#resolve correct chain



