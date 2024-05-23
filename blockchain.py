from functools import reduce
import hashlib as hl
from collections import OrderedDict
from hash_util import hash_string_256, hash_block
import json
import pickle


# Initializing our blockchain list
MINING_REWARD = 10

genesis_block = {
    'previous_hash': '', 
    'index': 0, 
    'transactions': [],
    'proof': 100
}
blockchain = [genesis_block]
open_transactions = []
owner = 'Plam'
participants = {'Plam'}

def load_data():
    try:
        with open('blockchain.txt', mode='r') as f:
            # file_content = pickle.loads(f.read())
            # print(file_content)
            file_content = f.readlines()
            global blockchain
            global open_transactions
            # blockchain = file_content['chain']
            # open_transactions = file_content['ot']     
            blockchain = json.loads(file_content[0][:-1]) 
            updated_blockchain = []
            for block in blockchain:
                updated_block = {
                'previous_hash': block['previous_hash'],
                'index': block['index'],
                'proof': block['proof'],
                'transactions':[OrderedDict(
                    [('sender', tx['sender']), 
                     ('recipient', tx['recipient']), 
                     ('amount', tx['amount'])]) for tx in block['transactions']]
                }
            updated_blockchain.append(updated_block)
            blockchain = updated_blockchain
            open_transactions = json.loads(file_content[1]) 
            updated_transactions = []
            for tx in open_transactions:
                updated_transaction = OrderedDict(
                        [('sender', tx['sender']), 
                        ('recipient', tx['recipient']), 
                        ('amount', tx['amount'])])
                updated_transactions.append(updated_transaction)
            open_transactions = updated_transactions
    except IOError:
        print('Missing blockchain file!') 
    finally:
        print('Cleanup!')     

load_data() 

  
def save_data():
    with open('blockchain.txt', mode='w') as f:
        f.write(json.dumps(blockchain))
        f.write('\n')
        f.write(json.dumps(open_transactions))
        # save_data = {
        #     'chain': blockchain,
        #     'ot': open_transactions
        # }
        # f.write(pickle.dumps(save_data))      
        
        
def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    guess_hash = hash_string_256(guess)
    print(guess_hash)
    return guess_hash[0:2] == '00'


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def get_balance(participant):
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant]for block in blockchain]
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = reduce(lambda tx_sum, tx_amt:tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0,tx_sender, 0)
    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant]for block in blockchain]
    amount_received = reduce(lambda tx_sum, tx_amt:tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0,tx_recipient, 0)
    return amount_received - amount_sent

    
def get_last_blockchain_value():
    """ Returns the last value of the current blockchain """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']
        
    
def add_transaction(recipient,sender=owner, amount=1.0):
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
    transaction = OrderedDict([('sender', sender), ('recipient', recipient), ('amount', amount)])
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        save_data()
        return True
    return False
    
    
def mine_block():
    last_block = blockchain[-1]
    hashed_block =  hash_block(last_block)
    proof = proof_of_work()
    
    # reward_transaction = {
    #     'sender': 'MINING', 
    #     'recipient': owner, 
    #     'amount': MINING_REWARD
    #     }
    reward_transaction = OrderedDict([('sender', 'MINING'), ('recipient', owner), ('amount', MINING_REWARD)])
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = {
        'previous_hash': hashed_block, 
        'index': len(blockchain), 
        'transactions': copied_transactions,
        'proof': proof
        }
    blockchain.append(block)
    return True


def get_transaction_value():
    tx_recipient = input("Enter the recipient: ")
    tx_amount = float(input('Please, enter transaction amount: '))
    return (tx_recipient, tx_amount)
    
    
def get_user_choice():
    user_input = input('Your choice: ')
    return user_input


def print_blocks():
    for block in blockchain:
        print("Outputting block")
        print(block)
    else:
        print("-" * 20)


def verify_chain():
    """Verify the current blockchain and returns TRUE if it passes verification."""
    for (index,block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block['transactions'][:-1], block['previous_hash'], block['proof']):
            print("Invalid proof of work")
            return False
    return True

        
def verify_transactions():
    return all([verify_transactions(tx) for tx in open_transactions])

    # is_valid = True
    # for tx in open_transactions:
    #     if verify_transaction(tx):
    #         is_valid = True
    #     else:
    #         is_valid = False
    # return is_valid
 

waiting_for_input = True       

while waiting_for_input:
    print("Please, choose!")
    print("1: Add new transaction")
    print("2: Mine new blocks")
    print("3: Output the blocks")
    print("4: Output the participants")
    print("5: Check transaction validity")
    print("h: Manipulate the chain")
    print("q: Quit program")
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        if add_transaction(recipient, amount=amount):
            print('Transaction Added!')
        else:
            print('*' * 80)
            print('Transaction FAILED!')
            print('*' * 80)
        print(open_transactions)
    elif user_choice == '2':
        if mine_block():
            open_transactions = []
            save_data()
    elif user_choice == '3':
        print_blocks()
    elif user_choice == '4':
        print(participants)
    elif user_choice == '5':
        if verify_transactions():
            print('All transactions are valid')
        else:
            print('All transactions are NOT valid')
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '', 
                'index': 0, 
                'transactions': [{'sender': 'Max', 'recipient': 'Chris', 'amount':100}]
        }
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print("Invalid input!")
    if not verify_chain():
        print_blocks()
        print("Invalid blockchain!")
        break
    print('$' * 40)
    print('The balance of {} is: {:6.2f} coins.'.format(owner, get_balance(owner)))
    print('$' * 40)
    
else:
    print("User left.")


print("Done!")