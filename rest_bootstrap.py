import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


from block import *
from node import *
#import blockchain
from wallet import *
from transaction import *
from time import time


### JUST A BASIC EXAMPLE OF A REST API WITH FLASK




app = Flask(__name__)
CORS(app)
#blockchain = Blockchain()		#??? etsi ???
#blockchain = []	
self_node = node(0,[],0) #,500 nbcs)	#identifier symfwna me to poio node eimaste. arxikopoihmeno pantou ston bootstrap. oi ypoloipoi kanoun set ta pedia otan
									#xtypane sthn create
#list_of_current_block_transactions = []



#.......................................................................................

# @app.route('/node', methods=['POST'])
# def init():			#params that we need: id,
# 	identifier = request.args.get('id') 
# 		#id, chain, current_id_count, NBCs


@app.route('/thesemyutxos', methods=['GET'])
def return_utxos():
	response = {}
	i = 1
	for utxo in self_node.UTXOs:
		key = str(i)
		receiver = '42'
		for node in self_node.ring:
			if utxo['recipient'] == node['public_key']:
				receiver = node['ip_port']
		temp = {'amount': utxo['amount'], 'transaction_id': utxo['transaction_id'], 'unique_UTXO_id': utxo['unique_UTXO_id'], 'receiver': receiver}
		response.update({i: temp})
		i += 1
	return jsonify(response), 200

@app.route('/node/genesis', methods=['POST'])
def create_genesis():
	listOfTransactions = []
	another_random_gen = Crypto.Random.new().read
	another_private_key = RSA.generate(1024, another_random_gen)
	another_private_key_string = private_key_string = str(base64.b64encode(another_private_key.exportKey(format='DER')),'utf-8')
	genesis_outs = [{'unique_UTXO_id':-1, 'transaction_id': 0, 'recipient': another_private_key_string, 'amount':0}, {'unique_UTXO_id': self_node.next_utxo_unique_id, 'transaction_id': 0, 'recipient': (self_node.wallet).public_key, 'amount': 5*100}]
	self_node.next_utxo_unique_id += 2
	self_node.UTXOs = self_node.UTXOs + genesis_outs
	random_gen = Crypto.Random.new().read
	private_key = RSA.generate(1024, random_gen)
	private_key_string = str(base64.b64encode(private_key.exportKey(format='DER')),'utf-8')
	#p_string = str(private_key)
	t = Transaction(0, private_key_string, self_node.wallet.public_key, 5*100, 0, [], genesis_outs)		#sender_address = 0, sender_private_key = 0 (emeis authaireta), amount n*100 (edw n = 5)
	listOfTransactions.append(t)
	timestamp = time()
	block = Block(0, 1, timestamp, 0, listOfTransactions)			#create_new_block(previousHash, timestamp, nonce, listOfTransactions)
	(self_node.chain).append(block)

	uri = '192.168.1.3:5000'		#GIA VMS THELEI ALLAGI
	my_public_key = self_node.wallet.public_key
	self_node.put_me_in(uri,my_public_key, '5000')
	
	return 'ok', 200

@app.route('/node/receivegenesis', methods=['POST'])	#PREPEI NA PARO TOY EYGE
def receive_init_chain():
	received_block = request.get_json()
	self_node.chain.append(received_block)
	return 'ok', 200



@app.route('/node/create', methods=['POST'])
def create_node():
	identifier = request.args.get('id')
	self_node.identifier = identifier			#change my id. everything else is fine. now self_node is reachable everywhere in the rest
	return 'ok', 200

@app.route('/node/ring', methods=['POST'])
def register_ring():
	ring_dict = request.get_json() 	#{0: {stoixeia 0ou}, 1:{stoixeia 1ou}...}
	self_node.ring = [value for value in ring_dict.values()]
	
	response = {'key': self_node.ring[0]['public_key']}
	return jsonify(response),200
	


@app.route('/node/register', methods=['POST'])
def register_node():
	
	ip = request.remote_addr
	
	pub_key_dict = request.get_json()
	public_key = pub_key_dict['pkey']
	port = pub_key_dict['port']

	self_node.register_node_to_ring(public_key, ip, port)	#node that runs the rest (bootstrap node here)
	
	return 'ok', 200

# get all transactions in the blockchain

# @app.route('/transactions/get', methods=['GET'])
# def get_transactions():
#     transactions = blockchain.transactions

#     response = {'transactions': transactions}
#     return jsonify(response), 200

@app.route('/transaction/receivetransaction', methods=['POST'])
def validate_received_transaction():
	transaction = request.get_json()		#??
	transaction_id = transaction['transaction_id']
	amount = transaction['amount']
	transaction_inputs = transaction['transaction_inputs']
	transaction_outputs_id_first = transaction['transaction_outputs_id_first']
	transaction_outputs_amount_first = transaction['transaction_outputs_amount_first']
	transaction_outputs_transid_first = transaction['transaction_outputs_transid_first']
	transaction_outputs_id_second = transaction['transaction_outputs_id_second']
	transaction_outputs_amount_second = transaction['transaction_outputs_amount_second']
	transaction_outputs_transid_second = transaction['transaction_outputs_transid_second']
	transaction_signature = transaction['transaction_signature']
	transaction_outputs_recipient_first = transaction['transaction_outputs_recipient_first']
	sender_address = transaction['sender_address']
	recipient_address = transaction['recipient_address']
	transaction_outputs_recipient_second = transaction['transaction_outputs_recipient_second']
	

	transaction_outputs = [{'unique_UTXO_id':transaction_outputs_id_first,'amount':transaction_outputs_amount_first, 'transaction_id':transaction_outputs_transid_first ,'recipient':transaction_outputs_recipient_first}, 
							{'unique_UTXO_id':transaction_outputs_id_second,'amount':transaction_outputs_amount_second, 'transaction_id':transaction_outputs_transid_second ,'recipient':transaction_outputs_recipient_second}]

	t = Transaction(sender_address, None, recipient_address, amount, transaction_id, transaction_inputs, transaction_outputs)

	self_node.next_trans_id = transaction_id + 1
	
	t.Signature = transaction_signature

	self_node.validate_transaction(t, transaction_signature)

	return 'ok', 200

@app.route('/block/receiveblock',methods=['POST'])
def validate_received_block():
	received_block = request.get_json()

	block_index = received_block['block_index']
	previousHash = received_block['previousHash']
	timestamp = received_block['timestamp']
	hash_ = received_block['hash']
	nonce = received_block['nonce']

	newlist = []
	# index = received_block['block_index']
	# previousHash = received_block['previousHash']
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

		self_node.next_utxo_unique_id += 2


		t = Transaction(sender_address, None, recipient_address, amount, transaction_id, transaction_inputs, transaction_outputs)

		self_node.next_trans_id = transaction_id + 1
		
		newlist.append(t)

	newlist_sorted = sorted(newlist)

	for trans in newlist_sorted:
		if not(trans in self_node.transaction_pool):
			for utxo_id in transaction_inputs:
				self_node.UTXOs = [utxo for utxo in self_node.UTXOs if utxo['unique_UTXO_id'] != utxo_id]

			for utxo in transaction_outputs :
				if not(utxo in self_node.UTXOs):
					self_node.UTXOs = self_node.UTXOs + transaction_outputs

	new_block = Block(block_index, previousHash, timestamp, nonce, newlist_sorted)
	new_block.hash = hash_
	self_node.validate_block(new_block)	

	return "OK", 200

# @app.route('/block/manytimes', methods=['GET'])
# def many_times():
# 	acc = 0
# 	for b in range(2, len(self_node.chain)-1):
# 		if (self_node.chain[b] == self_node.chain[b+1]):
# 			acc += 1
# 	response = {'acc': acc}
# 	return jsonify(response), 200

# @app.route('/block/blockchain_contents', methods = ['GET'])
# def return_blocks():
# 	response = {}
# 	i = 1
# 	for block in self_node.chain:
# 		d = {i: block.to_dict()}
# 		i += 1
# 		response.update(d)
# 	return jsonify(response), 200

@app.route('/transaction/transpoollength', methods = ['GET'])
def get_pool_length():
	response = {'length': len(self_node.transaction_pool)}
	return jsonify(response), 200

#dikia mas
@app.route('/blockchain/getLength', methods=['GET'])
def get_chain_length():
	response = {'length': len(self_node.chain)}
	return jsonify(response), 200

@app.route('/blockchain/getCertainBlock?blocknumber', methods=['GET'])
def getcertainblock():
	blocknumber = request.args.get('blocknumber')
	chain = self_node.chain 	#self = node
	response = {'block': chain[blocknumber].to_dict()}	#check
	return jsonify(response), 200



@app.route('/transactions/createtransaction', methods=['POST'])
def create_trans():
	recv_id = request.args.get('receiver')
	amount = request.args.get('amount')
	sender = self_node.wallet.public_key
	for node in self_node.ring:
		if (node['id'] == int(recv_id)):
			receiver = node['public_key']
	self_node.create_transaction(sender, receiver, int(amount))
	return 'ok', 200

@app.route('/node/balance', methods=['GET'])
def return_balance():
	balance = self_node.wallet.balance(self_node.UTXOs, self_node.wallet.public_key)
	response = {'balance': balance}
	return jsonify(response), 200


# run it once for every node

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port


    app.run(host='192.168.1.3', port=port)
