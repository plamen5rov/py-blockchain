class Node:
    def __init__(self):
        self.blockchain = []
        
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
        for block in self.blockchain:
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
            # print("h: Manipulate the chain")
            print("q: Quit program")
            user_choice = self.get_user_choice()
            if user_choice == '1':
                tx_data = self.get_transaction_value()
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
                self.print_blocks()
            elif user_choice == '4':
                verifier = Verification()
                if verifier.verify_transactions(open_transactions, get_balance):
                    print('All transactions are valid')
                else:
                    print('All transactions are NOT valid')
            # elif user_choice == 'h':
            #     if len(blockchain) >= 1:
            #         blockchain[0] = {
            #             'previous_hash': '', 
            #             'index': 0, 
            #             'transactions': [{'sender': 'Max', 'recipient': 'Chris', 'amount':100}]
            #     }
            elif user_choice == 'q':
                waiting_for_input = False
            else:
                print("Invalid input!")
            verifier = Verification()
            if not verifier.verify_chain(blockchain):
                self.print_blocks()
                print("Invalid blockchain!")
                break
            print('$' * 40)
            print('The balance of {} is: {:6.2f} coins.'.format(tx_owner, get_balance(tx_owner)))
            print('$' * 40)
            
        else:
            print("User left.")


    print("Done!")