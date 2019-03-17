from collections import OrderedDict

import binascii

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import requests
from flask import Flask, jsonify, request, render_template


class Transaction:

    def __init__(self, sender_address, sender_private_key, recipient_address, value, identity, transaction_in, transaction_out):
        ##set

        self.sender_address = sender_address
        self.receiver_address = recipient_address
        self.amount = value
		self.transaction_id = identity
        self.transaction_inputs = transaction_in
        self.transaction_outputs = transaction_out
        self.Signature = self.sign_transaction()


    def to_dict(self):
    	return OrderedDict({'transaction_id': self.transaction_id,
    						'sender_address': self.sender_address,
                            'recipient_address': self.receiver_address,
							'ammount': self.ammount})
        

    def sign_transaction(self, sender_private_key):
        #Sign transaction with private key
        message = str(self.sender_address) + str(self.receiver_address) + str(self.amount)
        key = sender_private_key	#key = RSA.import_key(open('private_key.der').read())	https://pycryptodome.readthedocs.io/en/latest/src/signature/pkcs1_v1_5.html
        h = SHA256.new(message)
        signature = PKCS1_v1_5.new(key).sign(h)
        return signature       

    #DIKIA MOU
	def verify_signature(sender_public_key):
		#verify that the signature corresponds to senders public key
		verifier = PKCS1_v1_5.new(sender_public_key)
        h = SHA.new(str(transaction).encode('utf8'))
		return verifier.verify(h, binascii.unhexlify(signature))