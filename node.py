from block import *
#from node import *
#import blockchain
from wallet import *
from transaction import *

import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

import base64

import hashlib

import threading

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

MINING_DIFFICULTY = 5
TRANS_CAPACITY = 5


#chainLock.acquire()
#chainLock.release()

class node:
	def __init__(self, identifier, chain, current_id_count):	#chain = []
		self.id = identifier
		# self.NBC=100;
		##set

		self.transaction_pool = []  #list of transactions
		self.chain = chain			#blockchain
		self.current_id_count = current_id_count
		#self.NBCs = NBCs
		self.wallet = self.create_wallet()
		
		self.chainLock = threading.Lock() 
		self.poolLock = threading.Lock()
		self.utxoLock = threading.Lock()

		#self.transLock = threading.Lock()
		
		self.UTXOs = []	#list of dictionairies
		self.next_utxo_unique_id = 0
		self.next_trans_id = 0
		
		#create a block???
		#self.block = create_new_block

		self.ring = [] #{'id':0,'ip_port':bootstrap_ip,'public_key':bootstrap_public_key}] #???  #here we store information for every node, as its id, its address (ip:port) its public key and its balance 
		#list of dictionaries {'id', 'ip_port', 'public_key', 'balance'}


	def put_me_in(self, uri, pkey, port):
		pkey_dict = {'pkey':pkey, 'port': port}
		r = requests.post('http://' + uri + '/node/register', json=pkey_dict)


	def create_new_block(self, listOfTransactions):
		#self.chainLock.acquire()
		lastblock = self.chain[-1]
		previousHash = lastblock.hash 	
		timestamp = time()
		block_index = len(self.chain) + 1

		b = Block(block_index, previousHash, timestamp, 0, listOfTransactions)
		#self.chainLock.release()
		return b

	def create_wallet(self):
		#create a wallet for this node, with a public key and a private key
		random_gen = Crypto.Random.new().read
		private_key = RSA.generate(1024, random_gen)
		public_key = private_key.publickey()		#check for binascii
		public_key_string = str(base64.b64encode(public_key.exportKey(format='DER')),'utf-8')
		private_key_string = str(base64.b64encode(private_key.exportKey(format='DER')),'utf-8')
		return wallet(public_key_string, private_key_string, [])


	def register_node_to_ring(self, public_key, ip, port):
		if (self.id == 0):		#if i'm the bootstrap node
			identifier = self.current_id_count
			ip_port = ip + ':' + port
			self.ring.append({'id':identifier,'ip_port':ip_port,'public_key':public_key,'amount':100}) 	#sketo public_key edw
			self.current_id_count += 1
			if(self.current_id_count == 5):
				#broadcast the ring
				for node in range(1,5):
					#lock ??
					uri = self.ring[node]['ip_port']
					dict_ring = {item['id']:item for item in self.ring}
					requests.post('http://' + uri + '/node/ring', json = dict_ring)
				for node in range(1,5):
					uri = self.ring[node]['ip_port']
					genesis_block = self.chain[0]
					g_block = genesis_block.to_dict()
					requests.post('http://' + uri + '/node/receivegenesis', json = g_block)

				for node in range(1,5):	

					t = self.create_transaction(self.wallet.public_key, self.ring[node]['public_key'], 100)
					
					#unlock ??
			if (not(identifier == 0) and self.current_id_count < 5):
				requests.post('http://' + ip_port + '/node/create?id=' + str(identifier))
				#maybe requests for first (100 NBCs) transactions ?


		#add this node to the ring, only the bootstrap node can add a node to the ring after checking his wallet and ip:port address
		#bottstrap node informs all other nodes and gives the request node an id and 100 NBCs


	def create_transaction(self, sender_public_key, recv_public_key, amount):

		#self.transLock.acquire()

		sender_private_key = self.wallet.private_key
		acc = 0
		transaction_in = []

		self.utxoLock.acquire()
		for utxo in self.UTXOs:
			if (utxo['recipient'] == self.wallet.public_key):
				acc += utxo['amount']
				transaction_in.append(utxo['unique_UTXO_id'])
				if (acc >= amount):
					break
		
		self.utxoLock.release()

		if (acc < amount):
			print("DEN MOU FTANOUN TA GKAFRA :( \n")
			transaction_in = []
			return None	#null?

		#identity = len(self.transaction_pool) + 1	#check again
		identity = self.next_trans_id
		self.next_trans_id += 1

		transaction_out = []
		t = Transaction(sender_public_key, sender_private_key, recv_public_key, amount, identity, transaction_in, transaction_out)

		#self.chainLock.release()
		
		if (self.validate_transaction(t, t.Signature)):	#if we don't receive our own transaction from broadcast 
			self.broadcast_transaction(t)

		#self.transLock.release()

	def broadcast_transaction(self, transaction):
		#self.chainLock.acquire()
		
		for node in self.ring:
			if (node['id'] != self.id):		#do not broadcast to myself

				uri = node['ip_port']
				
				dict_trans = transaction.to_dict() 			
				requests.post('http://' + uri + '/transaction/receivetransaction', json = dict_trans)
		#self.chainLock.release()



	def validate_transaction(self, transaction, signature):		#it's called from rest when receiving a transaction
		#use of signature and NBCs balance
		#a)verify signature

		#self.chainLock.acquire()

		sender_public_key = transaction.sender_address
		recv_public_key = transaction.receiver_address
		if (transaction.verify_signature(sender_public_key, signature)):
			found = 0
			print("VALIDATE TRANSACTION: Ekana verify signature\n")
			
			self.utxoLock.acquire()
			for utxo in self.UTXOs: 	#check MY utxos for transaction.inputs. 
				if (utxo['unique_UTXO_id'] in transaction.transaction_inputs):
					found += 1
			self.utxoLock.release()

			if (found == len(transaction.transaction_inputs)):

				print("VALIDATE TRANSACTION: Komple ta inputs\n")

				balance = 0

				self.utxoLock.acquire()
				for utxo_id in transaction.transaction_inputs:
					for utxo in self.UTXOs:
						if (utxo['unique_UTXO_id'] == utxo_id):
							balance += utxo['amount']
				#balance = self.wallet.balance(self.UTXOs, sender_public_key)



				for utxo_id in transaction.transaction_inputs:
					self.UTXOs = [utxo for utxo in self.UTXOs if utxo['unique_UTXO_id'] != utxo_id]		#If valid, take trans_inputs out of my UTXOS.


				

				utxo_for_sender = {'unique_UTXO_id':str(transaction.transaction_id) + str(balance - transaction.amount) + str(sender_public_key), 'transaction_id': transaction.transaction_id, 'recipient': sender_public_key, 'amount': (balance - transaction.amount)}
				if (not(utxo_for_sender in self.UTXOs)):
					self.UTXOs.append(utxo_for_sender)

				
				
				utxo_for_receiver = {'unique_UTXO_id':str(transaction.transaction_id) + str(transaction.amount) + str(recv_public_key), 'transaction_id': transaction.transaction_id, 'recipient': recv_public_key, 'amount':transaction.amount}
				if (not(utxo_for_receiver in self.UTXOs)):
					self.UTXOs.append(utxo_for_receiver)
				
				
				self.utxoLock.release()


				transaction_out = [utxo_for_sender, utxo_for_receiver]
				transaction.transaction_outputs = transaction_out

				#self.chainLock.release()

				#self.next_trans_id = transaction.transaction_id + 1

				self.add_transaction_to_block(transaction)
				return True
			return False

		

	def add_transaction_to_block(self, transaction):		
		#if enough transactions  mine

		#self.transLock.acquire()

		self.poolLock.acquire()

		self.transaction_pool.append(transaction)

		self.poolLock.release()
		
		if (len(self.transaction_pool) >= TRANS_CAPACITY):

			self.poolLock.acquire() 	
			block = self.create_new_block(self.transaction_pool[0:TRANS_CAPACITY]) 	#take TRANS_CAPACITY from pool

			self.poolLock.release()

			#self.transaction_pool = []		#may not be right ?
			mined_block = self.mine_block(block)

			#self.chainLock.release()
			#return mined_block		
			#then broadcast_block from rest_api
			if (mined_block.nonce != 0):
				self.broadcast_block(mined_block)




	def mine_block(self, block):
		nonce = 0
		while (self.valid_proof(nonce, block) is False):
			nonce += 1
		block.nonce = nonce

		self.chainLock.acquire()

		lastblock = self.chain[-1]
		last_hash = lastblock.hash

		prev_hash = block.previousHash
		if (prev_hash != last_hash):
			block.nonce = 0
			self.chainLock.release()
			return block

		self.chain.append(block)
		self.chainLock.release()

		self.poolLock.acquire()
		self.transaction_pool = self.transaction_pool[TRANS_CAPACITY:len(self.transaction_pool)]

		self.poolLock.release()

		# for trans in block.listOfTransactions:
		# 	if trans in self.transaction_pool:	#if transaction in our pool
		# 		self.transaction_pool.remove(trans)
		return block


	def broadcast_block(self, mined_block):
		for node in self.ring:
			if (node['id'] != self.id):		#do not broadcast to myself
				uri = node['ip_port']
				dict_block = mined_block.to_dict()
				requests.post('http://' + uri + '/block/receiveblock', json = dict_block)
				
		#return list_of_ips


	def valid_proof(self, nonce, block, difficulty=MINING_DIFFICULTY):
		last_hash = block.previousHash
		timestamp = block.timestamp
		guess = (str(last_hash)+str(nonce)+str(timestamp)).encode()
		guess_hash = hashlib.sha256(guess).hexdigest()
		if (guess_hash[:difficulty] == '0'*difficulty):
			block.hash = guess_hash
			return True
		else:
			return False


	#concencus functions

	def get_longest_chain(self, chain):	#checks for the longer chain accross all nodes. returns ip:port of the longest chain owner
		max_length = len(chain)
		my_dict = list(filter(lambda me: me['public_key'] == (self.wallet).public_key, self.ring))
		node_with_max_chain = my_dict[0]['ip_port']
		flag = 1
		for node in self.ring:
			uri = node['ip_port']
			response = requests.get('http://' + uri + '/blockchain/getLength')

			if response.status_code == 200:
				length = response.json()['length']

				if ((length > max_length) and (length > len(chain))):
					max_length = length
					node_with_max_chain = uri
					flag = 0
		if (flag == 1):
			return ['0',0]	#i'm the one with the longest chain
		return [node_with_max_chain,max_length]


	def valid_chain(self, chain):
		prev_hash = 42
		for block in chain:
			if (block.previousHash != prev_hash):
				return False
			else:
				prev_hash = block.previousHash
				myHash = block.myHash()
				if (myHash != block.hash): 	
					return False 				#this should never happen (maybe?)
				return True


	def resolve_conflicts(self):
		#resolve correct chain

		print("EIMAI STH RESOLVE CONFILCTS")

		#self.chainLock.acquire()

		node_with_max_chain = self.get_longest_chain(self.chain)
		if (node_with_max_chain[0] != '0'):	#my chain is not the longest
			
			#new_blocks_transactions = {}
			newblock = 1

			candidate_chain = self.chain
			new_utxos = self.UTXOs
			new_transactions_pool = self.transaction_pool
			temp_next_trans_id = self.next_trans_id

			# number_of_needed_blocks = node_with_max_chain[1] - len(self.chain)

			self.chainLock.acquire()
			for i in range (len(self.chain), node_with_max_chain[1]): 	#maybe number_of_needed_blocks + 1
				
				
				
				response = requests.get('http://' + node_with_max_chain[0] + '/blockchain/getCertainBlock?blocknumber=' + str(i))
				if response.status_code == 200:

					#self.chainLock.acquire()					

					received_block = response.json()


					block_index = received_block['block_index']
					previousHash = received_block['previousHash']
					timestamp = received_block['timestamp']
					hash_ = received_block['hash']
					nonce = received_block['nonce']

					newlist = []
					
					listOfTransactions = received_block['listOfTransactions']

					for trans in listOfTransactions:
						transaction_inputs = trans['transaction_inputs']
						sender_address = trans['sender_address']
						recipient_address = trans['recipient_address']
						transaction_id = trans['transaction_id']
						amount = trans['amount']
						transaction_outputs_id_first = trans['transaction_outputs_id_first']
						transaction_outputs_amount_first = trans['transaction_outputs_amount_first']
						transaction_outputs_transid_first = trans['transaction_outputs_transid_first']
						transaction_outputs_id_second = trans['transaction_outputs_id_second']
						transaction_outputs_amount_second = trans['transaction_outputs_amount_second']
						transaction_outputs_transid_second = trans['transaction_outputs_transid_second']
						transaction_signature = trans['transaction_signature']
						transaction_outputs_recipient_first = trans['transaction_outputs_recipient_first']
						transaction_outputs_recipient_second = trans['transaction_outputs_recipient_second']

						transaction_outputs = [{'unique_UTXO_id':transaction_outputs_id_first,'amount':transaction_outputs_amount_first, 'transaction_id':transaction_outputs_transid_first ,'recipient':transaction_outputs_recipient_first}, 
											   {'unique_UTXO_id':transaction_outputs_id_second,'amount':transaction_outputs_amount_second, 'transaction_id':transaction_outputs_transid_second ,'recipient':transaction_outputs_recipient_second}]

						self.next_utxo_unique_id += 2


						t = Transaction(sender_address, None, recipient_address, amount, transaction_id, transaction_inputs, transaction_outputs)
						temp_next_trans_id = transaction_id + 1
						
						newlist.append(t)

					newlist_sorted = sorted(newlist)

					#new_blocks_transactions.update({newblock: newlist_sorted})

					newblock += 1

					for trans in newlist_sorted:
						if trans in new_transactions_pool:	#if transaction in our pool
							new_transactions_pool.remove(trans)
						self.poolLock.acquire()
						if not(trans in self.transaction_pool):
							for utxo_id in transaction_inputs:
								new_utxos = [utxo for utxo in new_utxos if utxo['unique_UTXO_id'] != utxo_id]

							for utxo in transaction_outputs :
								if not(utxo in new_utxos):
									new_utxos = new_utxos + transaction_outputs
						self.poolLock.release()

					new_block = Block(block_index, previousHash, timestamp, nonce, newlist_sorted)
					new_block.hash = hash_

					

					candidate_chain.append(new_block)

					#self.chainLock.release()

					#self.validate_block(new_block)
			

			if (self.valid_chain(candidate_chain)):
				self.chain = candidate_chain 		#candidate chain is correct. i must obtain it

				self.utxoLock.acquire()
				self.UTXOs = new_utxos  			#update my utxos accordingly
				self.utxoLock.release()

				self.poolLock.acquire()
				self.transaction_pool = new_transactions_pool 	#update my transaction pool as well
				self.poolLock.release()

				self.next_trans_id = temp_next_trans_id 		#update next_trans_id



			self.chainLock.release()




	def validate_block(self, block):	#except for genesis block. Called when receiving a (mined) block
		self.chainLock.acquire()
		
		lastblock = self.chain[-1]
		last_hash = lastblock.hash
		
		self.chainLock.release()

		prev_hash = block.previousHash
		if (prev_hash != last_hash):
			self.resolve_conflicts()
			return False
		else:
			myHash = block.myHash()
			if (myHash == block.hash):
				
				return True
			else:
				return False