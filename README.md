# noobcash
Distributed Systems project 2018-2019, NTUA.

Aim of this project is to create "noobcash", a simple blockhain system, in which all transactions between users will be tracked and consensus will be guaranteed through the usage of "Proof-of-Work"

A small description of the system is given below:
1) Every user has a "noobcash wallet" in order to make transactions. Every wallet consists of (i) a private key and (ii) a public key.
2) Each wallet owner can make a transaction, sending NBC (noobcash coins) to someone and signing the transaction with his/her private key.
3) Every transaction is broadcasted to the network.
4) Miners receive the transaction and verify it. They check that the sender did indeed send the transaction, using his/her public key. Then they check whether the sender has the necessary NBC balance in his/her wallet. If all this is true, the transaction is added to the current block. In this system an assumption is made that every user is also a miner listening for transactions.
5) When the current block gets full miners begin mining it using Proof-of-Work. When a miner finds the correct nonce he/she broadcasts the verified block to all users.
6) If two or more miners mine a block simultaneously and broadcast it, users add the first block they received to their blockchain. This could lead to different blockchains. When this occurs users run a consensus algorithm, according to which if there is a conflict the larger chain is obtained.
