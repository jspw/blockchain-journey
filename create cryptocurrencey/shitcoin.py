#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Module -2 : Creating a cryptocurrencey

"""
Created on Thu Jan 13 17:06:02 2022

@author: shifat
"""

# a simple general blockchain 

import datetime
import hashlib
import json
from flask import Flask,jsonify,request
import requests
from uuid import uuid4
from urllib.parse import urlparse


# building blockchain 
class Blockhain:
    def __init__(self):
        self.chain=[]
        self.transactions=[]
        self.create_block(proof = 1,previous_hash='0')
        self.nodes = set()
        
        
    def  create_block(self,proof,previous_hash):
        block = {'index' :  len(self.chain) + 1 , 
                 'timestamp' :  str(datetime.datetime.now()),
                 'proof' : proof,
                 'previous_hash': previous_hash ,
                 'transactions' : self.transactions
                 }
        self.chain.append(block)
        self.transactions = []
        return block
            
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self,previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if(hash_operation[:4]) == '0000':
                check_proof = True
            else :
                new_proof+=1
                
        return new_proof
    
    def hash(self,block):
        encoded_block = json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self,chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if(hash_operation[:4]) != '0000':
                return False
            previous_block = block
            block_index +=1
        return True
        
        return True
         
    def add_transactions(self,sender,receiver,amount):
        self.transactions.append({
            'sender' : sender,
            'receiver' : receiver,
            'amount' : amount
            })
        
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1
    

    def add_node(self,address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        
    def replace_chain(self):
        network=self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if(response.status_code == 200):
                length = response.json()["length"]
                chain = response.json()['chain']
                if(length > max_length and self.is_chain_valid(chain)):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
    
# creating a Web application
app = Flask(__name__)
    
    
# creating a blockchain
blockchain =  Blockhain()



# mining a new blockchain
@app.route("/mine_block",methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof= blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof,previous_hash)
    response = {'message' : 'Congratulations you just mined a block!',
                'index':block['index'],
                'timestamp' : block['timestamp'],
                'proof' : block['proof'],
                'previous_hash' : block['previous_hash']
                }
    
    return jsonify(response),201
    
    
# getting the full blockchain
@app.route('/get_chain',methods=['GET'])
def get_chain():
    response = {
        'chain' : blockchain.chain,
        'length' : len(blockchain.chain)
        }
    
    return jsonify(response),200


### check if the chain is valid
@app.route("/is_chain_valid",methods=["GET"])
def check_if_chain_valid():
    chain = blockchain.chain
    is_valid = blockchain.is_chain_valid(chain)
    return jsonify({
        "is chain valid" : is_valid
        }),200
    


# running the app
app.run(host='localhost',port=8081)

"""
Created on Tue Feb  8 11:33:20 2022

@author: shifat
"""

# cryptocurrencey shitcoin building 

# decentralizing our blockchain   
























