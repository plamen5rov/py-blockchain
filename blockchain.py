blockchain = []

def get_last_blockchain_value():
    return blockchain[-1]


def add_value(value, last_transaction=[1]):
    blockchain.append([last_transaction,value])
    

add_value(3.14)
add_value(24.04,get_last_blockchain_value())
add_value(2024,get_last_blockchain_value())

print(blockchain)