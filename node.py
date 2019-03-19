import block
import wallet
import transaction
#import blockchain

import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS


class node:
	def __init__(self, identifier, chain, current_id_count, NBCs):	#chain = []
		self.id = identifier
		# self.NBC=100;
		##set

		self.transaction_pool = []  #list of transactions
		self.chain = chain			#blockchain
		self.current_id_count = current_id_count
		#self.NBCs = NBCs
		self.wallet = self.create_wallet()
		
		self.UTXOs = []	#list of dictionairies
		self.next_utxo_unique_id = 0
		
		#create a block???
		#self.block = create_new_block

		self.ring[]#{'id':0,'ip_port':bootstrap_ip,'public_key':bootstrap_public_key}] #???  #here we store information for every node, as its id, its address (ip:port) its public key and its balance 
		#list of dictionaries {'id', 'ip_port', 'public_key', 'balance'}




	def create_new_block(listOfTransactions):
		lastblock = self.chain[-1]
		previousHash = lastblock.hash 	
		timestamp = time()
		block_index = len(self.chain) + 1

		b = block(block_index, previousHash, timestamp, 0, listOfTransactions)
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
			ip_port = ip + ':' + port
			ring.append({'id':identifier,'ip_port':ip_port,'public_key':public_key,'balance':balance})
			self.current_id_count++
			if(self.current_id_count == 5):
				#broadcast the ring
				for node in range(1,len(ring)):
					uri = ring[node]['ip_port']
					broad_ring = {'ring': ring} 	#??
					jsonify(broad_ring) 			#??
					requests.post('http://' + uri + '/node/ring?' + broad_ring)
			if (not(identifier == 0) && self.current_id_count < 5):
				requests.post('http://' + ip_port + '/node/create?' + identifier)
				#maybe requests for first (100 NBCs) transactions ?


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

		identity = len(self.transaction_pool) + 1	#check again

		#utxo_for_sender = {'unique_UTXO_id':__, 'transaction_id': identity, 'recipient': sender_public_key, 'amount':self.wallet.balance(self) - amount}
		# self.UTXOs.append(utxo_for_sender)
		#utxo_for_receiver = {'unique_UTXO_id':___ , 'transaction_id': identity, 'recipient': recv_public_key, 'amount':amount}
		#self.UTXOs.append(utxo_for_receiver)
		#transaction_out = [utxo_for_sender, utxo_for_receiver]
		transaction_out = []
		t = Transaction(sender_public_key, sender_private_key, recv_public_key, amount, identity, transaction_in, transaction_out)
		validate_transaction(t)	#if we don't receive our own transaction from broadcast 
		broadcast_transaction(t)

	def broadcast_transaction(self, transaction):
		for node in self.ring:
			uri = node['ip_port']
			trans = jsonify(transaction) 			#??
			requests.post('http://' + uri + '/transaction/receivetransaction?' + trans)
		



	def validate_transaction(self, transaction):		#it's called from rest when receiving a transaction
		#use of signature and NBCs balance
		#a)verify signature
		sender_public_key = transaction.sender_address
		if (transaction.verify_signature(sender_public_key)):
			if (all(elem in self.UTXOs  for elem in transaction.transaction_inputs)):	#check MY utxos for transaction.inputs. 
				for utxo in transaction.transaction_inputs:
					self.UTXOs.remove(utxo)		#If valid, take trans_inputs out of my UTXOS.

				#Create two new utxos for THIS transaction and add them to my utxos
				if (self.UTXOs[-1][unique_UTXO_id] >= self.next_utxo_unique_id):
					self.next_utxo_unique_id = self.UTXOs[-1][unique_UTXO_id] + 1
				utxo_for_sender = {'unique_UTXO_id':self.next_utxo_unique_id, 'transaction_id': transaction.transaction_id, 'recipient': sender_public_key, 'amount':self.wallet.balance(self) - amount}
				self.UTXOs.append(utxo_for_sender)
				self.next_utxo_unique_id += 1
				utxo_for_receiver = {'unique_UTXO_id':self.next_utxo_unique_id, 'transaction_id': transaction.transaction_id, 'recipient': recv_public_key, 'amount':amount}
				self.UTXOs.append(utxo_for_receiver)
				self.next_utxo_unique_id += 1
				transaction_out = [utxo_for_sender, utxo_for_receiver]
				transaction.transaction_outputs = transaction_out
				add_transaction_to_block(transaction)
			

	def add_transaction_to_block(self, transaction):		
		#if enough transactions  mine
		self.transaction_pool.append(transaction)
		#utxo_for_receiver = transaction.transaction_outputs[1]
		# if (utxo_for_receiver['recipient'] == self.wallet.public_key):	#if trans_out is about me, append it to my utxos
		#self.UTXOs.append(utxo_for_receiver) #<-- is this necessary ?
		if (len(self.transaction_pool) == TRANS_CAPACITY):
			block = create_new_block(self.transaction_pool)
			self.transaction_pool = []		#may not be right ?
			mined_block = mine_block(block)
			#return mined_block		
			#then broadcast_block from rest_api
			broadcast_block(mined_block)



	def mine_block(self, block):
		nonce = 0
        while self.valid_proof(nonce, block) is False:
            nonce += 1
		block.nonce = nonce
		self.chain.append(block)
		return block


	def broadcast_block(self, mined_block):
		for node in self.ring:
			uri = node['ip_port']
			block = jsonify(mined_block) 			#??
			requests.post('http://' + uri + '/block/receiveblock?' + block)
		#return list_of_ips

		

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

	def valid_chain(self, chain):	#checks for the longer chain accross all nodes. returns ip:port of the longest chain owner
		max_length = len(chain)
		my_dict = list(filter(lambda me: me['public_key'] == (self.wallet).public_key, ring))
		node_with_max_chain = my_dict[0]['ip_port']
		flag = 1
		for node in self.ring:
			uri = node['ip_port']
			response = requests.get('http://' + uri + '/blockchain/getLength')

			if response.status_code == 200:
				length = response.json()['length']

				if ((length > max_length) && (length > len(chain))):
					max_length = length
					node_with_max_chain = uri
					flag = 0
		if (flag == 1):
			return ['0',0]	#i'm the one with the longest chain
		return [node_with_max_chain,max_length]


	def resolve_conflicts(self):
		#resolve correct chain

		node_with_max_chain = valid_chain(self.chain)
		if (node_with_max_chain[0] == '0'):	#my chain is the longest
			#do nothing
		else:
			number_of_needed_blocks = node_with_max_chain[1] - len(self.chain)
			for i in range (number_of_needed_blocks, node_with_max_chain[1]):
				response = requests.get('http://' + node_with_max_chain[0] + '/blockchain/getCertainBlock?' + i)
				if response.status_code == 200:
					block = response.json()['block'] 	#check how to transfer object through http requests
					if (not(validate_block(block))):	#our blockchain is entirely wrong. need to get the whole chain
						#return False
						break
					#fix our utxos
					for trans in block.listOfTransactions:
						if trans in self.transaction_pool:	#if transaction in our pool
							self.transaction_pool.remove(trans) 	#remove it
						self.UTXOs = self.UTXOs + trans.transaction_outputs
		#return True





	def validate_block(self, block):	#except for genesis block. Called when receiving a (mined) block
		lastblock = self.chain[-1]
		last_hash = lastblock.hash
		prev_hash = block.previousHash
		if (prev_hash != last_hash):
			resolve_conflicts()
		else
			#transactions = block.listOfTransactions
			#timestamp = block.timestamp
			myHash = block.myHash()
			#guess = (str(transactions)+str(prev_hash)+str(nonce)+str(timestamp)).encode()
   			#guess_hash = hashlib.sha256(guess).hexdigest()
        	if (myHash == block.hash):
				self.chain.append(block)
			# 	return True
			# else:
			# 	return False
				#POULO
		#return block

