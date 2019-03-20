import binascii

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4



class wallet:

	def __init__(self, public_key, private_key, transactions):
		##set

		self.public_key = public_key
		self.private_key = private_key
		self.address = public_key
		self.transactions = transactions

	def balance(self, node):	#add all UTXOs concerning me
		acc = 0
		for utxo in node.UTXOs:
			if (utxo['recipient'] == self.public_key):
				acc += utxo['amount']
		return acc
