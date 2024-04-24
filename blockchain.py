blockchain = [[0]]

def add_value(value):
    blockchain.append([blockchain[-1],value])
    print(blockchain)

add_value(3.14)
add_value(24.04)
add_value(2024)