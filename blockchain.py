"""Outer imports"""
import json
# import pickle
from functools import reduce
from block import Block
from transaction import Transaction
from hash_util import hash_block
from verification import Verification

# Initializing our blockchain list
MINING_REWARD = 10
blockchain = []
open_transactions = []
tx_owner = 'Plam'


def load_data():
    """Loading data from the blockchain"""
    global blockchain
    global open_transactions
    try:
        with open('blockchain.txt', mode='r') as f:
            # file_content = pickle.loads(f.read())
            # print(file_content)
            file_content = f.readlines()
            # blockchain = file_content['chain']
            # open_transactions = file_content['ot']     
            blockchain = json.loads(file_content[0][:-1]) 
            updated_blockchain = []
            for block in blockchain:
                converted_tx = [Transaction(tx['sender'],tx['recipient'],tx['amount']) for tx in block['transactions']]
                # converted_tx = [OrderedDict(
                #     [('sender', tx['sender']), 
                #      ('recipient', tx['recipient']), 
                #      ('amount', tx['amount'])]) for tx in block['transactions']]
                updated_block = Block(block['index'], block['previous_hash'], converted_tx,block['proof'], block['timestamp'])
                # updated_block = {
                # 'previous_hash': block['previous_hash'],
                # 'index': block['index'],
                # 'proof': block['proof'],
                # 'transactions':[OrderedDict(
                #     [('sender', tx['sender']), 
                #      ('recipient', tx['recipient']), 
                #      ('amount', tx['amount'])]) for tx in block['transactions']]
                # }
                updated_blockchain.append(updated_block)
            blockchain = updated_blockchain
            open_transactions = json.loads(file_content[1]) 
            updated_transactions = []
            for tx in open_transactions:
                updated_transaction = [Transaction(tx['sender'],tx['recipient'],tx['amount'])]
                # updated_transaction = OrderedDict(
                #         [('sender', tx['sender']), 
                #         ('recipient', tx['recipient']), 
                #         ('amount', tx['amount'])])
                updated_transactions.append(updated_transaction)
            open_transactions = updated_transactions
    except (IOError, IndexError):
        print('Missing or empty blockchain file!')
        genesis_block = Block(0,'',[], 100, 0)
        # genesis_block = {
        #     'previous_hash': '', 
        #     'index': 0, 
        #     'transactions': [],
        #     'proof': 100
        # }
        blockchain = [genesis_block]
        open_transactions = []
    finally:
        print('Cleanup!')     

load_data() 

  
def save_data():
    """Saves data in the database file."""
    try:
        with open('blockchain.txt', mode='w') as f:
            savable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash,[tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in blockchain]]
            f.write(json.dumps(savable_chain))
            f.write('\n')
            savable_tx = [tx.__dict__ for tx in open_transactions]
            f.write(json.dumps(savable_tx))
            # save_data = {
            #     'chain': blockchain,
            #     'ot': open_transactions
            # }
            # f.write(pickle.dumps(save_data))     
    except IOError: 
        print("Saving data failed!")


def proof_of_work():
    """Returns the proof of work"""
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    verifier = Verification()
    while not verifier.valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def get_balance(participant):
    """Returns the balance of the participant"""
    tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant]for block in blockchain]
    open_tx_sender = [tx.amount for tx in open_transactions if tx.sender == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = reduce(lambda tx_sum, tx_amt:tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0,tx_sender, 0)
    tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant]for block in blockchain]
    amount_received = reduce(lambda tx_sum, tx_amt:tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0,tx_recipient, 0)
    return amount_received - amount_sent

    
def get_last_blockchain_value():
    """ Returns the last value of the current blockchain """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]
        
    
def add_transaction(recipient,sender=tx_owner, amount=1.0):
    """ Appends new value of the current blockchain
    
    Arguments:
    :sender: The sender of the transaction
    :recipient: The recipient of the transaction
    :amount: The amount sent (default is 1.0)
    """
    # transaction = {
    #     'sender': sender, 
    #     'recipient': recipient, 
    #     'amount': amount
    #     }
    transaction = Transaction(sender, recipient, amount)
    # transaction = OrderedDict([('sender', sender), ('recipient', recipient), ('amount', amount)])
    verifier = Verification()
    if verifier.verify_transaction(transaction, get_balance):
        open_transactions.append(transaction)
        # participants.add(sender)
        # participants.add(recipient)
        save_data()
        return True
    return False
    
    
def mine_block():
    """Mining block"""
    last_block = blockchain[-1]
    hashed_block =  hash_block(last_block)
    proof = proof_of_work()
    
    # reward_transaction = {
    #     'sender': 'MINING', 
    #     'recipient': tx_owner, 
    #     'amount': MINING_REWARD
    #     }
    reward_transaction = Transaction('MINING', tx_owner, MINING_REWARD)
    # reward_transaction = OrderedDict([('sender', 'MINING'), ('recipient', tx_owner), ('amount', MINING_REWARD)])
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = Block(len(blockchain), hashed_block, copied_transactions, proof)
    # block = {
    #     'previous_hash': hashed_block, 
    #     'index': len(blockchain), 
    #     'transactions': copied_transactions,
    #     'proof': proof
    #     }
    blockchain.append(block)
    return True

