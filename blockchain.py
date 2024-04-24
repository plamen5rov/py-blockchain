blockchain = [[0]]

def get_last_blockchain_value():
    return blockchain[-1]


def add_value(value):
    blockchain.append([get_last_blockchain_value(),value])
    

add_value(3.14)
add_value(24.04)
add_value(2024)

print(blockchain)