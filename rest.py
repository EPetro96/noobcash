import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS


import block
import node
#import blockchain
import wallet
import transaction
import wallet
import time


### JUST A BASIC EXAMPLE OF A REST API WITH FLASK




app = Flask(__name__)
CORS(app)
#blockchain = Blockchain()		#??? etsi ???
#blockchain = []	
self_node = node(0,[],0)#,500 nbcs)	#identifier symfwna me to poio node eimaste. arxikopoihmeno pantou ston bootstrap. oi ypoloipoi kanoun set ta pedia otan
									#xtypane sthn create



#.......................................................................................

# @app.route('/node', methods=['POST'])
# def init():			#params that we need: id,
# 	identifier = request.args.get('id') 
# 		#id, chain, current_id_count, NBCs

@app.route('/node/genesis', methods=['POST'])
def create_genesis():
	listOfTransactions = []
	genesis_outs = [{'unique_UTXO_id':-1, 'transaction_id': 0, 'recipient': 0, 'amount':0}, {'unique_UTXO_id': self_node.next_utxo_unique_id, 'transaction_id': 0, 'recipient': (self_node.wallet).public_key, 'amount': 5*100}]
	self_node.next_utxo_unique_id += 1
	t = transaction(0, 0, self_node.wallet.public_key(), 5*100, 0, [], genesis_outs)		#sender_address = 0, sender_private_key = 0 (emeis authaireta), amount n*100 (edw n = 5)
	listOfTransactions.append(t)
	timestamp = time()
	block = block(0, 1, timestamp, 0, listOfTransactions)			#create_new_block(previousHash, timestamp, nonce, listOfTransactions)
	(self_node.chain).append(block)
	#return 200

@app.route('/node/receivegenesis?chain', methods=['POST'])
def receive_init_chain():
	init_chain = request.args.get('chain')
	self_node.chain = init_chain

@app.route('/node/create?id', methods=['POST'])
def create_node():
	identifier = request.args.get('id')
	#self_node = node(identifier,[],0),#nbcs)	#theloume kapws self_node prospelasimo apo olo to rest?
	self_node.identifier = identifier			#change my id. everything else is fine. now self_node is reachable everywhere in the rest

@app.route('/node/ring?ring', methods=['POST'])
def register_ring():
	ring = request.args.get('ring')
	self_node.ring = ring

@app.route('/node/register', methods=['POST'])
def register_node():
	port = 5000 	#deite to kai meta
	ip = request.remote_addr

	#public_key = request.args.get('public_key')

	public_key = self_node.wallet.public_key
	self_node.register_node_to_ring(public_key, ip, port)	#node that runs the rest (bootstrap node here)
	#t = transaction(n.wallet.public_key(),n.wallet.private_key() ,public_key, 100)
	#signature = t.sign_transaction(n.wallet.private_key())
	#node.create_transaction(n.wallet.public_key(), public_key, signature, t)

# get all transactions in the blockchain

@app.route('/transactions/get', methods=['GET'])
def get_transactions():
    transactions = blockchain.transactions

    response = {'transactions': transactions}
    return jsonify(response), 200

@app.route('/transaction/receivetransaction?trans', methods=['POST'])
def validate_received_transaction():
	transaction = request.args.get('trans')		#??
	self_node.validate_transaction(transaction)

@app.route('block/receiveblock?block',methods=['POST'])
def validate_received_block():
	block = request.args.get('block')
	self_node.validate_block(block)

#dikia mas
@app.route('/blockchain/getLength', methods=['GET'])
def get_chain_length():
	response = {'length': len(self_node.chain)}
	return jsonify(response), 200

@app.route('blockchain/getCertainBlock?blocknumber', methods=['GET'])
def getcertainblock():
	blocknumber = request.args.get('blocknumber')
	chain = self_node.chain 	#self = node
	response = {'block': chain[blocknumber]}	#check
	return jsonify(response), 200


#just a dummy implementation
@app.route('transactions/create', methods=['POST'])
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