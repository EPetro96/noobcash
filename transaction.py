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

    def __init__(self, sender_address, sender_private_key, recipient_address, value):


        ##set

        self.sender_address = sender_address
        self.receiver_address = recipient_address
        self.amount = value


        #self.sender_address: To public key του wallet από το οποίο προέρχονται τα χρήματα
        #self.receiver_address: To public key του wallet στο οποίο θα καταλήξουν τα χρήματα
        #self.amount: το ποσό που θα μεταφερθεί
        #self.transaction_id: το hash του transaction
        #self.transaction_inputs: λίστα από Transaction Input 
        #self.transaction_outputs: λίστα από Transaction Output 
        #selfSignature


    


    def to_dict(self):
        

    def sign_transaction(self, sender_private_key):
        #Sign transaction with private key
        message = str(self.sender_address) + str(self.receiver_address) + str(self.amount)
        key = sender_private_key	#key = RSA.import_key(open('private_key.der').read())	https://pycryptodome.readthedocs.io/en/latest/src/signature/pkcs1_v1_5.html
        h = SHA256.new(message)
        signature = PKCS1_v1_5.new(key).sign(h)
        return signature       