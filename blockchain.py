#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 04:52:30 2021

@author: abhishek.ka
"""
# Create a blockchain

from datetime import datetime
import hashlib
import json
from flask import Flask, jsonify
from flask.wrappers import Response

# Part 1: Build a blockchain


class Blockchain:

    def __init__(self):
        self.chain = []
        self.createBlock(proof=1, previousHash="0")

    def createBlock(self, proof, previousHash):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.now()),
            "proof": proof,
            "previousHash": previousHash,
        }

        self.chain.append(block)
        return block

    def getPreviousBlock(self):
        return self.chain[-1]

    def proofOfWork(self, previousProof):
        newProof = 1
        checkProof = False
        while checkProof is False:
            hashOperation = hashlib.sha256(
                str(newProof**2 - previousProof**2).encode()
            ).hexdigest()
            if hashOperation.startswith("0000"):
                checkProof = True
            else:
                newProof += 1

        return newProof

    def generateHash(self, block):
        encodedBlock = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encodedBlock).hexdigest()

    def isChainValid(self, chain):
        previousBlock = chain[0]
        blockIndex = 1
        while blockIndex < len(chain):
            currBlock = chain[blockIndex]
            if currBlock["previousHash"] != self.generateHash(previousBlock):
                return False

            previousProof = previousBlock["proof"]
            currentProof = currBlock["proof"]
            hashOperation = hashlib.sha256(
                str(currentProof**2 - previousProof**2).encode()
            ).hexdigest()
            if not hashOperation.startswith("0000"):
                return False

            previousBlock = currBlock
            blockIndex += 1

        return True


# Part 2: Mine the blockchain
# Create a Web App
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
# Create a blockchain
blockchain = Blockchain()


@app.route('/health-check', methods=['GET'])
def healthCheck():
    return jsonify({"Response": "Hello World!"}), 200


@app.route('/mine', methods=['GET'])
def mineBlock():
    previousBlock = blockchain.getPreviousBlock()
    previousProof = previousBlock["proof"]
    proof = blockchain.proofOfWork(previousProof=previousProof)
    previousHash = blockchain.generateHash(previousBlock)
    generatedBlock = blockchain.createBlock(
        proof=proof, previousHash=previousHash)

    response = {
        "message": "Block mining successful",
        "blockNumber": generatedBlock["index"],
        "createdAt": generatedBlock["timestamp"],
        "proof": generatedBlock["proof"],
        "previousHash": generatedBlock["previousHash"]
    }
    return jsonify(response), 200


@app.route('/display', methods=['GET'])
def displayFullChain():
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route('/valid', methods=['GET'])
def checkChainValidty():
    response = {
        "valid": blockchain.isChainValid(blockchain.chain)
    }
    return jsonify(response), 200


app.run(host="0.0.0.0", port=5001)
