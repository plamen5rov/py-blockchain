from collections import OrderedDict
from utility.printable import Printable

class Transaction(Printable):
    """Transaction added to a block in blockchain"""
    def __init__(self, sender, recipient, signature, amount):
        self.sender = sender
        self.recipient = recipient
        self.signature = signature
        self.amount = amount
              
    def to_ordered_dict(self):
        return OrderedDict([('sender', self.sender), ('recipient', self.recipient), ('amount', self.amount)])