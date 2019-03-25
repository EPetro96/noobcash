from collections import OrderedDict

import binascii

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import base64

import requests
from flask import Flask, jsonify, request, render_template


class Transaction:

	def __init__(self, sender_address = None, sender_private_key = None, recipient_address = None, value = None, identity = None, transaction_in = None, transaction_out = None):
		if (not( sender_address is None)):
			self.sender_address = sender_address
		if (not( recipient_address is None)):
			self.receiver_address = recipient_address
		if (not( value is None)):
			self.amount = value
		if (not( identity is None)):
			self.transaction_id = identity
		if (not( transaction_in is None)):
			self.transaction_inputs = transaction_in
		if (not( transaction_out is None)):
			self.transaction_outputs = transaction_out
		if (not(sender_private_key is None)):
			self.Signature = self.sign_transaction(sender_private_key)

	def __eq__(self,other):
		return self.transaction_id == other.transaction_id

	def __lt__(self, other):
		return self.transaction_id < other.transaction_id

	def to_dict(self):
		return OrderedDict({'transaction_id': self.transaction_id,
							'sender_address': self.sender_address,
							'recipient_address': self.receiver_address ,
							'transaction_inputs': self.transaction_inputs,
							'transaction_outputs_id_first': self.transaction_outputs[0]['unique_UTXO_id'],
							'transaction_outputs_amount_first': self.transaction_outputs[0]['amount'],
							'transaction_outputs_transid_first': self.transaction_outputs[0]['transaction_id'],
							'transaction_outputs_recipient_first': self.transaction_outputs[0]['recipient'],
							'transaction_outputs_id_second': self.transaction_outputs[1]['unique_UTXO_id'],
							'transaction_outputs_amount_second': self.transaction_outputs[1]['amount'],
							'transaction_outputs_transid_second': self.transaction_outputs[1]['transaction_id'],
							'transaction_outputs_recipient_second': self.transaction_outputs[1]['recipient'],
							'transaction_signature':self.Signature,
							'amount': self.amount})
		

	def sign_transaction(self, sender_private_key):
		#Sign transaction with private key
		#private_key = RSA.importKey(binascii.unhexlify(sender_private_key)) PREPEI NA BEI!!1!!1!!!11!FILIA STIN OIKOGENEIA
		actual_private_key = RSA.importKey(base64.b64decode(sender_private_key))
		
		#actual_sender_address = RSA.importKey(base64.b64decode(self.sender_address))
		#actual_receiver_address = RSA.importKey(base64.b64decode(self.receiver_address))

		signer = PKCS1_v1_5.new(actual_private_key)
		#h = SHA.new(str(self.to_dict()).encode('utf8'))
		#message = {'transaction_id':self.transaction_id, 'sender_address': self.sender_address, 'recipient_address': self.receiver_address, 'amount':self.amount}
		message = {'elare':'reee'}
		h = SHA.new(str(message).encode('utf8'))
		return binascii.hexlify(signer.sign(h)).decode('ascii')
		# message = (str(self.sender_address) + str(self.receiver_address) + str(self.amount)).encode()
		# key = sender_private_key	#key = RSA.import_key(open('private_key.der').read())	https://pycryptodome.readthedocs.io/en/latest/src/signature/pkcs1_v1_5.html
		# h = SHA256.new((message).encode('utf8'))
		# signature = PKCS1_v1_5.new(key).sign(h)
		# return signature       

	def verify_signature(self, sender_public_key, signature):
		#verify that the signature corresponds to sender's public key
		#public_key = RSA.importKey(binascii.unhexlify(sender_public_key))
		actual_sender_public_key = RSA.importKey(base64.b64decode(sender_public_key))
		verifier = PKCS1_v1_5.new(actual_sender_public_key)
		#h = SHA.new(str(self.to_dict()).encode('utf8'))
		#message = {'transaction_id':self.transaction_id, 'sender_address': self.sender_address, 'recipient_address': self.receiver_address, 'amount':self.amount}
		message = {'elare':'reee'}
		h = SHA.new(str(message).encode('utf8'))
		return verifier.verify(h, binascii.unhexlify(signature))
