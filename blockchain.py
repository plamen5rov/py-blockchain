# Initializing our blockchain list
genesis_block = {
    'previous_hash': '', 
    'index': 0, 
    'transactions': []
}
blockchain = [genesis_block]
open_transactions = []
owner = 'Plam'
participants = {'Plam'}


def hash_block(block):
    return '-'.join([str(block[key]) for key in block])


def get_last_blockchain_value():
    """ Returns the last value of the current blockchain """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(recipient,sender=owner, amount=1.0):
    """ Appends new value of the current blockchain
    
    Arguments:
    :sender: The sender of the transaction
    :recipient: The recipient of the transaction
    :amount: The amount sent (default is 1.0)
    """
    transaction = {
        'sender': sender, 
        'recipient': recipient, 
        'amount': amount
        }
    
    open_transactions.append(transaction)
    participants.add(sender)
    participants.add(recipient)
    
    
def mine_block():
    last_block = blockchain[-1]
    hashed_block =  hash_block(last_block)
    print(hashed_block)
    block = {
        'previous_hash': hashed_block, 
        'index': len(blockchain), 
        'transactions': open_transactions
        }
    blockchain.append(block)


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
    return True

        
    

waiting_for_input = True       

while waiting_for_input:
    print("Please, choose!")
    print("1: Add new transaction")
    print("2: Mine new blocks")
    print("3: Output the blocks")
    print("4: Output the participants")
    print("h: Manipulate the chain")
    print("q: Quit program")
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        add_transaction(recipient, amount=amount)
        print(open_transactions)
    elif user_choice == '2':
        mine_block()
    elif user_choice == '3':
        print_blocks()
    elif user_choice == '4':
        print(participants)
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
    
else:
    print("User left.")


print("Done!")