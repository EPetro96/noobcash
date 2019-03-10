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

		self.ring[] #???  #here we store information for every node, as its id, its address (ip:port) its public key and its balance 
		#maybe dictionary with public_key as key values?




	def create_new_block(previousHash, timestamp, nonce, listOfTransactions):
		b = block(previousHash, timestamp, nonce, listOfTransactions)
		return b

	def create_wallet(self):
		#create a wallet for this node, with a public key and a private key

	def register_node_to_ring(self, public_key, ip, port):
		if (self.id == 0):		#if i'm the bootstrap node
			identifier = self.current_id_count
			ring.append((identifier,ip_port,public_key,balance))
			self.current_id_count++
			if(self.current_id_count == 5):
				#broadcast the ring


		#add this node to the ring, only the bootstrap node can add a node to the ring after checking his wallet and ip:port address
		#bottstrap node informs all other nodes and gives the request node an id and 100 NBCs


	def create_transaction(sender, receiver, signature, transaction):
		tuple_sender = ring{str(sender)}	#tbd
		tuple_recv = ring{str(receiver)}	#tbd
		


	def broadcast_transaction():





	def validdate_transaction():
		#use of signature and NBCs balance


	def add_transaction_to_block():
		#if enough transactions  mine



	def mine_block():



	def broadcast_block():


		

	def valid_proof(.., difficulty=MINING_DIFFICULTY):




	#concencus functions

	def valid_chain(self, chain):
		#check for the longer chain accroose all nodes


	def resolve_conflicts(self):
		#resolve correct chain



