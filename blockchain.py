"""Outer imports"""
import json
from functools import reduce
from block import Block
from transaction import Transaction
from utility.hash_util import hash_block
from utility.verification import Verification
from wallet import Wallet

MINING_REWARD = 10

class Blockchain:
    """Blockchain implementation as a class"""
    def __init__(self, hosting_node_id):
        genesis_block = Block(0,'',[], 100, 0)
        self.__chain = [genesis_block]
        self.__open_transactions = []
        self.load_data() 
        self.hosting_node = hosting_node_id
        
    def get_chain(self):
        return self.__chain[:]
    
    def get_open_transactions(self):
        return self.__open_transactions


    def load_data(self):
        """Loading data from the blockchain"""
        try:
            with open('blockchain.txt', mode='r') as f:
                file_content = f.readlines() 
                blockchain = json.loads(file_content[0][:-1]) 
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(tx['sender'],tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']]
                    updated_block = Block(block['index'], block['previous_hash'], converted_tx,block['proof'], block['timestamp'])
                    updated_blockchain.append(updated_block)
                self.__chain = updated_blockchain
                open_transactions = json.loads(file_content[1]) 
                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = [Transaction(tx['sender'],tx['recipient'],tx['signature'],tx['amount'])]
                    updated_transactions.append(updated_transaction)
                self.__open_transactions = updated_transactions
        except (IOError, IndexError):
            pass          
        finally:
            print('Cleanup!')     


    def save_data(self):
        """Saves data in the database file."""
        try:
            with open('blockchain.txt', mode='w') as f:
                savable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash,[tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in self.__chain]]
                f.write(json.dumps(savable_chain))
                f.write('\n')
                savable_tx = [tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(savable_tx))
                 
        except IOError: 
            print("Saving data failed!")


    def proof_of_work(self):
        """Returns the proof of work"""
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        open_transactions = self.__open_transactions
        while not Verification.valid_proof(open_transactions, last_hash, proof):
            proof += 1
        return proof


    def get_balance(self):
        """Returns the balance of the participant"""
        participant = self.hosting_node
        tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant]for block in self.__chain]
        open_tx_sender = [tx.amount for tx in self.__open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        amount_sent = reduce(lambda tx_sum, tx_amt:tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0,tx_sender, 0)
        tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant]for block in self.__chain]
        amount_received = reduce(lambda tx_sum, tx_amt:tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0,tx_recipient, 0)
        return amount_received - amount_sent

    
    def get_last_blockchain_value(self):
        """ Returns the last value of the current blockchain """
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]
        
    
    def add_transaction(self, recipient,sender, signature, amount=1.0):
        """ Appends new value of the current blockchain
        
        Arguments:
        :sender: The sender of the transaction
        :recipient: The recipient of the transaction
        :amount: The amount sent (default is 1.0)
        """
        
        if self.hosting_node is None:
            return False
        transaction = Transaction(sender, recipient, signature, amount)
        
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            
            self.save_data()
            return True
        return False
    
    
    def mine_block(self):
        """Mining block"""
        if self.hosting_node is None:
            return False
        last_block = self.__chain[-1]
        hashed_block =  hash_block(last_block)
        proof = self.proof_of_work()
        
        reward_transaction = Transaction('MINING', self.hosting_node, '', MINING_REWARD)
        
        copied_transactions = self.__open_transactions[:]
        for tx in copied_transactions:
            if not Wallet.verify_transaction(tx):
                return False
        copied_transactions.append(reward_transaction)
        block = Block(len(self.__chain), hashed_block, copied_transactions, proof)
        
        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        return True