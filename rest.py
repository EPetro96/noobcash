import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS


import block
import node
import blockchain
import wallet
import transaction
import wallet


### JUST A BASIC EXAMPLE OF A REST API WITH FLASK




app = Flask(__name__)
CORS(app)
#blockchain = Blockchain()		#??? etsi ???
blockchain = []
n = node(0, blockchain, 0, 0)		#identifier symfwna me to poio node eimaste


#.......................................................................................

# @app.route('/node', methods=['POST'])
# def init():			#params that we need: id,
# 	identifier = request.args.get('id') 
# 		#id, chain, current_id_count, NBCs

@app.route('/node/genesis', methods=['POST'])
def create_genesis():
	listOfTransactions = []
	t = transaction(0, 0, n.wallet.public_key(), 5*100)		#sender_address = 0, sender_private_key = 0 (emeis authaireta), node.wallet.kati pws?
	listOfTransactions.append(t)
	block = n.create_new_block(1, 0.0, 0, listOfTransactions)			#create_new_block(previousHash, timestamp, nonce, listOfTransactions)
	blockchain.append(block)
	#return 200

@app.route('/node/register', methods=['POST'])
def register_node():
	port = 5000 	#deite to kai meta
	ip = request.remote_addr
	public_key = request.args.get('public_key')
	n.register_node_to_ring(public_key, ip, port)
	#t = transaction(n.wallet.public_key(),n.wallet.private_key() ,public_key, 100)
	signature = t.sign_transaction(n.wallet.private_key())
	n.create_transaction(n.wallet.public_key(), public_key, signature, t)

# get all transactions in the blockchain

@app.route('/transactions/get', methods=['GET'])
def get_transactions():
    transactions = blockchain.transactions

    response = {'transactions': transactions}
    return jsonify(response), 200

#just a dummy implementation
@app.route('transactions/create', methods=['POST'])
def create_trans():
	trans = create_transaction(sender, receiver, signature, ammount)
	list_of_ips_ports = broadcast_transaction()
	#broadcast(trans, list_of_ips_ports)



# run it once for every node

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port)