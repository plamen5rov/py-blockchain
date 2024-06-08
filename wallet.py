"""Wallet Class for using with blockchain transactions"""
import binascii
from Crypto.PublicKey import RSA
import Crypto.Random

class Wallet:
    def __init__(self):
        self.private_key = None
        self.public_key = None
        
        
    def generate_keys(self):
        private_key = RSA.generate(1024, Crypto.Random.new().read)
        public_key = private_key.public_key()
        return (binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'), binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii'))
    
    def create_keys(self):
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key
        
        
    def load_keys(self):
        pass
        