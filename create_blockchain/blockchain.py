# Create Blockchain

from crypt import methods
import datetime
import hashlib
import json
from os import environ
from flask import Flask, jsonify


# Part 1 : Building a Blockchain

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash="0")

    def create_block(self, proof, previous_hash):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.datetime.now()),
            "proof": proof,
            "previous_hash": previous_hash
        }

        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def hash_generate(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):

            block = chain[block_index]
            if block["previous_block"] != self.hash_generate(previous_block):
                return False
            previous_proof = previous_block["proof"]
            proof = block["proof"]
            hash_operation = hashlib.sha256(
                str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] != "0000":
                return False
            previous_block = block
            block_index += 1

        return True

    def proof_of_work(self, previous_proof):
        new_proof = 1
        isNewProofCreated = False
        while isNewProofCreated is False:
            hash_operation = hashlib.sha256(
                str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] == "0000":
                isNewProofCreated = True
            else:
                new_proof += 1

        return new_proof


# Create a web application

app = Flask(__name__)

# create the blockchain

blockchain = Blockchain()


# Part 2 : Mining Our Blockchain with web application

@app.route("/heart_beat", methods=["GET"])
def heart_beat():
    message = "I'm alive here"
    return jsonify(message)


@app.route("/mine_block", methods=["GET"])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block["proof"]
    proof = blockchain.proof_of_work(previous_proof)
    print(proof)
    previous_hash = blockchain.hash_generate(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {
        "message": "Congratulation you have just mined a block!!",
        "index": block["index"],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 201


@app.route("/get_chain", methods=["GET"])
def get_chain():
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route("/is_chain_valid",  methods=["GET"])
def check_if_chain_valid():
    chain = blockchain.chain
    is_valid = blockchain.is_chain_valid(chain)
    response = {
        "is chain valid": is_valid
    }
    return jsonify(response), 200


app.debug = True
app.run(host="localhost",  port=5001)
