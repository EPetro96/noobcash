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
	
	#response = {'genesis': block.listOfTransactions[0].to_dict()}

	#return jsonify(response), 200

	# response = {'genesis_block': block.listOfTransactions}
    # return jsonify(response), 200
	return 'ok', 200

@app.route('/node/receivegenesis', methods=['GET'])
def receive_init_chain():
	received_block = request.get_json()
	self_node.chain.append(received_block)
	# index = received_block['block_index']
	# previousHash = received_block['previousHash']
	# listOfTransactions = received_block['listOfTransactions']

	# response = {'index':index, 'previousHash': previousHash, 'listOfTransactions': listOfTransactions}
	# return jsonify(response), 200

@app.route('/node/receivegenesistransactions', methods=['POST'])
def receivegenesistransactions():
	transaction_id = request.args.get('transaction_id')
	sender_address = request.args.get('sender_address')
	recipient_address = request.args.get('recipient_address')
	transaction_inputs = request.args.get('transaction_inputs')
	transaction_outputs_id_first = request.args.get('transaction_outputs_id_first')
	transaction_outputs_amount_first = request.args.get('transaction_outputs_amount_first')
	transaction_outputs_transid_first = request.args.get('transaction_outputs_transid_first')
	transaction_outputs_recipient_first = request.args.get('transaction_outputs_recipient_first')
	transaction_outputs_id_second = request.args.get('transaction_outputs_id_second')
	transaction_outputs_amount_second = request.args.get('transaction_outputs_amount_second')
	transaction_outputs_transid_second = request.args.get('transaction_outputs_transid_second')
	transaction_outputs_recipient_second = request.args.get('transaction_outputs_recipient_second')
	transaction_signature = request.args.get('transaction_signature')
	amount = request.args.get('amount')


@app.route('/node/create', methods=['POST'])
def create_node():
	identifier = request.args.get('id')
	#self_node = node(identifier,[],0),#nbcs)	#theloume kapws self_node prospelasimo apo olo to rest?
	self_node.identifier = identifier			#change my id. everything else is fine. now self_node is reachable everywhere in the rest

@app.route('/node/ring', methods=['POST'])
def register_ring():
	ring_dict = request.get_json() 	#{0: {stoixeia 0ou}, 1:{stoixeia 1ou}...}
	self_node.ring = [value for value in ring_dict.values()]
	
	response = {'key': self_node.ring[0]['public_key']}
	return jsonify(response),200
	
@app.route('/node/returnring', methods=['GET'])
def return_ring():

	#return jsonify(self_node.ring[5]), 200
	if (self_node.ring[0]['public_key'] is self_node.ring[5]['public_key']):
	 	return "OLA KOMPLE", 200
	else:
	 	return "SKATA", 404

@app.route('/test', methods=['GET'])
def test():
	id_ = request.args.get('genesis')
	#id2 = request.args.get('key2')
	return id_, 200


@app.route('/node/register', methods=['GET'])
def register_node():
	iterator = request.args.get('iterator')
	port = '5000' 	#deite to kai meta
	ip = request.remote_addr
	iterator = int(iterator)
	#public_key = request.args.get('public_key')

	public_key = self_node.wallet.public_key 	#this is strign
	self_node.register_node_to_ring(public_key, ip, port)	#node that runs the rest (bootstrap node here)
	#t = transaction(n.wallet.public_key(),n.wallet.private_key() ,public_key, 100)
	#signature = t.sign_transaction(n.wallet.private_key())
	#node.create_transaction(n.wallet.public_key(), public_key, signature, t)
	ring = self_node.ring[iterator]
	response = {'id':ring['id'],'ip_port':ring['ip_port'],'public_key':ring['public_key'],'amount':ring['amount']} 	
	return jsonify(response), 200

# get all transactions in the blockchain

@app.route('/transactions/get', methods=['GET'])
def get_transactions():
    transactions = blockchain.transactions

    response = {'transactions': transactions}
    return jsonify(response), 200

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
	
	# sender_address = RSA.importKey(base64.b64decode(sender_address))
	# recipient_address = RSA.importKey(base64.b64decode(recipient_address))
	# transaction_outputs_recipient_first = RSA.importKey(base64.b64decode(transaction_outputs_recipient_first))
	# transaction_outputs_recipient_second = RSA.importKey(base64.b64decode(transaction_outputs_recipient_second))

	transaction_outputs = [{'unique_UTXO_id':transaction_outputs_id_first,'amount':transaction_outputs_amount_first, 'transaction_id':transaction_outputs_transid_first ,'recipient':transaction_outputs_recipient_first}, 
							{'unique_UTXO_id':transaction_outputs_id_second,'amount':transaction_outputs_amount_second, 'transaction_id':transaction_outputs_transid_second ,'recipient':transaction_outputs_recipient_second}]

	t = Transaction(sender_address, None, recipient_address, amount, transaction_id, transaction_inputs, transaction_outputs)
	t.Signature = transaction_signature

	# response = {'trans_id': trans_id, 'amount': amount, 'sender_address':sender_address, 'transaction_inputs': transaction_inputs, 'transaction_outputs_transid_second': transaction_outputs_transid_second,
	# 			'transaction_outputs_amount_second': transaction_outputs_amount_second, 'transaction_outputs_id_second': transaction_outputs_id_second, 'transaction_outputs_transid_first':transaction_outputs_transid_first,
	# 			'transaction_outputs_amount_first': transaction_outputs_amount_first, 'transaction_outputs_id_first': transaction_outputs_id_first, 'transaction_signature': transaction_signature, 'transaction_outputs_recipient_first': transaction_outputs_recipient_first,
	# 			'recipient_address': recipient_address, 'transaction_outputs_recipient_second': transaction_outputs_recipient_second}
	#return jsonify(response), 200
	self_node.validate_transaction(t)

	#return jsonify(t.to_dict()), 200

@app.route('/block/receiveblock',methods=['POST'])
def validate_received_block():
	received_block = request.get_json()
	self_node.validate_block(received_block)
	#self_node.chain.append(received_block)

#dikia mas
@app.route('/blockchain/getLength', methods=['GET'])
def get_chain_length():
	response = {'length': len(self_node.chain)}
	return jsonify(response), 200

@app.route('/blockchain/getCertainBlock?blocknumber', methods=['GET'])
def getcertainblock():
	blocknumber = request.args.get('blocknumber')
	chain = self_node.chain 	#self = node
	response = {'block': chain[blocknumber]}	#check
	return jsonify(response), 200


#just a dummy implementation
@app.route('/transactions/create', methods=['POST'])
def create_trans():
	trans = create_transaction(sender, receiver, signature, ammount)



# run it once for every node

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port)
