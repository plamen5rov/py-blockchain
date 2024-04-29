# Initializing our blockchain list
blockchain = []

def get_last_blockchain_value():
    """ Returns the last value of the current blockchain """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(value, last_transaction):
    """ Appends new value of the current blockchain
    
    Arguments:
    :value: The new value
    :last_transaction: The last blockchain transaction (default [1])
    """
    if last_transaction == None:
        last_transaction = [1]
    blockchain.append([last_transaction,value])

def get_transaction_value():
    return float(input('Please, enter transaction number: '))
    



def get_user_choice():
    user_input = input('Your choice: ')
    return user_input

def print_blocks():
    for block in blockchain:
        print("Outputting block")
        print(block)

while True:
    print("Please, choose!")
    print("1: Add new transaction")
    print("2: Output the blocks")
    print("q: Quit program")
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_amount = get_transaction_value()
        add_transaction(tx_amount,get_last_blockchain_value())
    elif user_choice == '2':
        print_blocks()
    elif user_choice == 'q':
        break
    else:
        print("Invalid input!")




print("Done!")