# noobcash
Distributed Systems project 2018-2019

## ---- TO DO ----
## SEE WHEN TO REMOVE UTXOS
## GENIKA NA KATALAVOUME PWS METAFERONTAI TA JSONIFY KTL
## CHECK THREADS
## -------BACKEND--------
	1)UTXOs (dictionary. (unique_UTXO_id, transaction_id, sender/receiver_addres, ammount_of_coins))	MAYBE DONE(!)
	----REMEMBER: Update UTXOs in case of conflict!!	DONE!
	2)Complete validate_transaction proccess	MAYBE DONE (!)
	3)Consensus		DONE!
	4)Wallet Balance	DONE!
	5)figure out transaction_ids and utxo_ids, and more....  DONE!
	6)check myhash in block 	(not wrong right now)
	7)finish register_node_to_ring	DONE!
	8)Genesis Block
	9)when a new node is inserted transmit blockchain to him
	10)what happens with first transactions (should they be mined? should we treat them specially?) logika afou mpoun oloi stelnoume transactions
	   kai ta kanoume APLWS validate

## -----REST------
	1)identifiers gia to poios node eimaste (vlepe panw panw grammes 21-23) 	MAYBE DONE (!)
	2)otan mpainei node, request gia valid_chain
	3)check that we have all the app routes needed
	4)fix create transaction: should take arguments from input file
	5)


## ---Since Last Commit---
	1)resolve_conflicts -> see fix our utxos comment
	2)all broadcasts in backend
	3)ids for utxos, transactions, blocks
	4)corresponding app.routes at rest.py
	5)