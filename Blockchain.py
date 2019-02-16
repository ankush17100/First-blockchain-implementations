#Implementing a basic, simple blockchain
import datetime #for embding timestamp
import hashlib #For the cryptographic links
import json #To transfer the data in the blocks through web
from flask import Flask, jsonify #Flask to create the web app, jsonify to convert data into json format

# Part 1 - Building a Blockchain

class Blockchain:

    def __init__(self): #Constructor
        self.chain = [] #Initiating the chain as an empty list
        self.create_block(proof = 1, previous_hash = '0') #Genesis block

    def create_block(self, proof, previous_hash): #To create a block
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof, 
                 'previous_hash': previous_hash}
        self.chain.append(block) #Adding of a new block
        return block

    def get_previous_block(self): #Get last mined block
        return self.chain[-1] #Return last block

    def proof_of_work(self, previous_proof): #To get a proof of work for a block
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1 #try again with incremented value
        return new_proof
    
    def hash(self, block): #To get the hash of a block
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain): #To check if chain is valid
        previous_block = chain[0] # Genesis block
        block_index = 1
        while block_index < len(chain): #Checking for every block
            block = chain[block_index] #Current block
            if block['previous_hash'] != blockchain.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True



#Creating a web app
app = Flask(__name__)

#Creating a blockchain
blockchain = Blockchain()

#Mining the blockchain
@app.route('/mine_block', methods = ['GET'])
#To mine a block
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congratulations on mining a block',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200

#To get the chain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

#To check if the block is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    result = blockchain.is_chain_valid(blockchain.chain)
    if result:
        response = {'message': 'valid'}
    else:
        response = {'message': 'not valid'}
    
    return jsonify(response), 200

#Running the app
app.run(host = '0.0.0.0', port = 5000)