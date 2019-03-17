import block
import wallet
import blockchain


class node:
	def __init__(self, identifier, chain, current_id_count, NBCs):
		self.id = identifier
		# self.NBC=100;
		##set

		self.chain = chain
		self.current_id_count = current_id_count
		self.NBCs = NBCs
		self.wallet = self.create_wallet()

		#create a block???
		#self.block = create_new_block

		self.ring[] #???  #here we store information for every node, as its id, its address (ip:port) its public key and its balance 
		#list of dictionaries {'id', 'ip_port', 'public_key', 'balance'}




	def create_new_block(previousHash, timestamp, nonce, listOfTransactions):
		lastblock = self.chain[-1]
		previousHash = lastblock.hash 	#STEKEI?
		timestamp = time()

		b = block(previousHash, timestamp, nonce, listOfTransactions)
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


	def create_transaction(sender, receiver, signature, ammount): 	#sender-receiver ids
		sender_public_key = ring{'id' }	#tbd
		recv_public_key = ring{str(receiver)}	#tbd
		
		#transaction_in = UTXO_list.ids

		utxo_for_sender = self.wallet.balance() - ammount
		utxo_for_receiver = ammount
		transaction_out = [utxo_for_sender, utxo_for_receiver]
		identity = 42
		t = Transaction(sender_public_key, sender_private_key, recv_public_key, ammount, identity, transaction_in, transaction_out)
		return t

	def broadcast_transaction():
		return list_of_ips



	def validdate_transaction(transaction):
		#use of signature and NBCs balance
		#a)verify signature
		sender_public_key = transaction.sender_address
		if (transaction.verify_signature(sender_public_key)):
			#check MY utxos for transaction.inputs. If valid, take trans_inputs out of my UTXOS. Create two new utxos for THIS transaction and add them to my utxos


	def add_transaction_to_block():
		#if enough transactions  mine
		



	def mine_block():



	def broadcast_block():
		return list_of_ips

		

	def valid_proof(.., difficulty=MINING_DIFFICULTY):




	#concencus functions

	def valid_chain(self, chain):
		#check for the longer chain accroose all nodes


	def resolve_conflicts(self):
		#resolve correct chain



