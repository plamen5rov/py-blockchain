blockchain = []

def get_last_blockchain_value():
    return blockchain[-1]


def add_value(value, last_transaction=[1]):
    blockchain.append([last_transaction,value])

def get_user_input():
    return float(input('Please, enter transaction number: '))
    
tx_amount = get_user_input()
add_value(tx_amount)

tx_amount = get_user_input()
add_value(tx_amount,get_last_blockchain_value())

tx_amount = get_user_input()
add_value(tx_amount,get_last_blockchain_value())

print(blockchain)