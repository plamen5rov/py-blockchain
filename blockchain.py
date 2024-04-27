# Initializing our blockchain list
blockchain = []

def get_last_blockchain_value():
    """ Returns the last value of the current blockchain """
    return blockchain[-1]


def add_value(value, last_transaction=[1]):
    """ Appends new value of the current blockchain
    
    Arguments:
    :value: The new value
    :last_transaction: The last blockchain transaction (default [1])
    """
    blockchain.append([last_transaction,value])

def get_user_input():
    return float(input('Please, enter transaction number: '))
    
tx_amount = get_user_input()
add_value(tx_amount)



while True:
    tx_amount = get_user_input()
    add_value(tx_amount,get_last_blockchain_value())
    for block in blockchain:
        print("Outputting block")
        print(block)




print("Done!")