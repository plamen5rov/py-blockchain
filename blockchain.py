# Initializing our blockchain list
genesis_block = {
    'previous_hash': '', 
    'index': 0, 
    'transactions': []
}
blockchain = []
open_transactions = []
owner = 'Plam'


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
    
    
def mine_block():
    last_block = blockchain[-1]
    block = {
        'previous_hash': 'XYZ', 
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
    #block_index = 0
    is_valid = True
    for block_index in range(len(blockchain)):
        if block_index == 0:
            continue
        elif blockchain[block_index][0] == blockchain[block_index - 1]:
            is_valid = True
        else:
            is_valid = False
            break
        block_index += 1
    return is_valid
        
    # for block in blockchain:
    #     if block_index == 0:
    #         block_index += 1
    #         continue
    #     elif block[0] == blockchain[block_index - 1]:
    #         is_valid = True
    #     else:
    #         is_valid = False
    #         break
    #     block_index += 1
    # return is_valid

waiting_for_input = True       

while waiting_for_input:
    print("Please, choose!")
    print("1: Add new transaction")
    print("2: Output the blocks")
    print("h: Manipulate the chain")
    print("q: Quit program")
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        add_transaction(recipient, amount=amount)
        print(open_transactions)
    elif user_choice == '2':
        print_blocks()
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print("Invalid input!")
    if not verify_chain():
        print("Invalid blockchain!")
        break
    
else:
    print("User left.")



print("Done!")