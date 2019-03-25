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

		self.public_key = public_key 	#string
		self.private_key = private_key 	#string
		self.address = public_key 		#string
		self.transactions = transactions

	def balance(self, UTXOs, public_key):	#add all UTXOs concerning occupant of public_key
		acc = 0
		for utxo in UTXOs:
			if (utxo['recipient'] == public_key):
				acc += int(utxo['amount'])
		return acc
