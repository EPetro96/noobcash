# noobcash
Distributed Systems project 2018-2019

## ---- TO DO ----
## NA TO TREKSOUME PANW STA VMS  (GIA EPALHTHEYSH OTI GINETAI TO NODE)
## STA VMS NA FTIAKSOUME IPS STH MAIN TOU REST
## SEE WHEN TO REMOVE UTXOS 	DONE(?)
## FIX TRANSFERS OF OBJECTS	    !!! PENDING-HIGH PRIORITY   ***
## CHECK THREADS 				PENDING
# PREPEI NA MHN AXRHSTEYOYME TA APOMEINARIA TOU transaction 	DONE mesw UTXOs for sender
## I REGISTER_NODE_TO_RING XREIAZETE ENA EXTRA REQUEST GIA NA KANEI BROADCAST TO RING KAI TO GENESIS OPOS TIN EXOYME 	(MALLON oxi provlhma, pros to paron)
## TA THREADS EINAI KOMPLE KAI PREPEI NA EISAGOYME LOCKS SE OSA KOMMATIA THEORISOYME 	LOCKS PENDING
## QUEUE GIA APOTHIKEYSI BLOCKS OSTE NA TA EKSIPIRETOUME OLA 	PENDING
## NUMBER OF NODES TO PERNAME SA PARAMETRO 						PENDING
## -------BACKEND--------
	1)UTXOs (dictionary. (unique_UTXO_id, transaction_id, sender/receiver_addres, ammount_of_coins))	MAYBE DONE(!)
	----REMEMBER: Update UTXOs in case of conflict!!	DONE!
	2)Complete validate_transaction proccess	MAYBE DONE (!)
	3)Consensus		DONE!
	4)Wallet Balance	DONE!
	5)figure out transaction_ids and utxo_ids, and more....  DONE!
	6)check myhash in block 	(not wrong right now)
	7)finish register_node_to_ring	DONE!
	8)Genesis block 	(When creating bootstrap node, as a http request) DONE(!)
	9)when a new node is inserted transmit blockchain to him  	COMMENT| ETOIMO AN FTIAXOUME TO ***
	10)what happens with first transactions (should they be mined? should we treat them specially?) logika afou mpoun oloi stelnoume transactions
	   kai ta kanoume APLWS validate 		oxi. ta stelnoume, ta kanoume validate kai tha mpoun telika se blocks opou tha ginoyn mine

## -----REST------
	1)identifiers gia to poios node eimaste (vlepe panw panw grammes 21-23) 	MAYBE DONE (!)
	2)otan mpainei node, request gia valid_chain 	LOGIKA KALYPTETAI AN TOY METAFEROYME APLWS TO CHAIN (?)
	3)check that we have all the app routes needed  PENDING
	4)fix create transaction: should take arguments from input file 	TELIKA STH MAIN. PENDING
	5)


## ---Since Last Commit---
	1)resolve_conflicts -> see fix our utxos comment
	2)all broadcasts in backend
	3)ids for utxos, transactions, blocks
	4)corresponding app.routes at rest.py
	5)