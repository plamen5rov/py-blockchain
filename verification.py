from hash_util import hash_string_256, hash_block

class Verification():
    """Verification methods collection"""
    
    def valid_proof(self, transactions, last_hash, proof):
        """Checks if the proof is valid"""
        guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(last_hash) + str(proof)).encode()
        guess_hash = hash_string_256(guess)
        print(guess_hash)
        return guess_hash[0:2] == '00'
    
    
    def verify_chain(self, blockchain):
        """Verify the current blockchain and returns TRUE if it passes verification."""
        for (index,block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != hash_block(blockchain[index - 1]):
                return False
            if not self.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print("Invalid proof of work")
                return False
        return True
    
    
    def verify_transaction(self, transaction, get_balance):
        """ Verifies a transaction"""
        sender_balance = get_balance()
        return sender_balance >= transaction.amount
    
    
    def verify_transactions(self, open_transactions, get_balance):
        """Verifies transactions"""
        return all([self.verify_transaction(tx, get_balance) for tx in open_transactions])

        # is_valid = True
        # for tx in open_transactions:
        #     if verify_transaction(tx):
        #         is_valid = True
        #     else:
        #         is_valid = False
        # return is_valid
 