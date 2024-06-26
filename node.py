from uuid import uuid4
from blockchain import Blockchain
from utility.verification import Verification
from wallet import Wallet

class Node:
    """Class Node"""
    def __init__(self):
        # self.wallet.public_key = str(uuid4())
        self.wallet = Wallet()
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)
        
    def get_transaction_value(self):
        """Returns the transaction value"""
        tx_recipient = input("Enter the recipient: ")
        tx_amount = float(input('Please, enter transaction amount: '))
        return (tx_recipient, tx_amount)
        
    
    def get_user_choice(self):
        """Returns the user choice"""
        user_input = input('Your choice: ')
        return user_input


    def print_blocks(self):
        """Prints blocks"""
        for block in self.blockchain.get_chain():
            print("Outputting block")
            print(block)
        print("-" * 20)
    
    def listen_for_input(self):
        
        waiting_for_input = True
        
        while waiting_for_input:
            print("Please, choose!")
            print("1: Add new transaction")
            print("2: Mine new blocks")
            print("3: Output the blocks")
            print("4: Check transaction validity")
            print("5: Create wallet")
            print("6: Load wallet")
            print("7: Save keys")
            # print("h: Manipulate the chain")
            print("q: Quit program")
            user_choice = self.get_user_choice()
            if user_choice == '1':
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data
                signature = self.wallet.sign_transaction(self.wallet.public_key, recipient, amount)
                if self.blockchain.add_transaction(recipient, self.wallet.public_key, signature, amount=amount):
                    print('Transaction Added!')
                else:
                    print('*' * 80)
                    print('Transaction FAILED!')
                    print('*' * 80)
                print(self.blockchain.get_open_transactions())
            elif user_choice == '2':
                if not self.blockchain.mine_block():
                    print('Mining failed! Got no wallet?')
            elif user_choice == '3':
                self.print_blocks()
            elif user_choice == '4':
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print('All transactions are valid')
                else:
                    print('All transactions are NOT valid')
            elif user_choice == '5':
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == '6':
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == '7':
                self.wallet.save_keys()
            elif user_choice == 'q':
                waiting_for_input = False
            else:
                print("Invalid input!")
            
            if not Verification.verify_chain(self.blockchain.get_chain()):
                self.print_blocks()
                print("Invalid blockchain!")
                break
            print('$' * 40)
            print('The balance of {} is: {:6.2f} coins.'.format(self.wallet.public_key, self.blockchain.get_balance()))
            print('$' * 40)
            
        else:
            print("User left.")


    print("Done!")

if __name__ == '__main__':
    node = Node()
    node.listen_for_input()

print(__name__)