"""
File Name: encryption.py
Author: Diwan Mohamed Faheer
Last Edit: 17.11.22

File Description: This file contains all the code for the encryption system in the program. This is responsible for the encryption of user passwords and the matching of them.
"""

import uuid
import hashlib

class Encryption(object):
  """
  This class provides methods for encrypting and decrypting strings.
  """
  
  def __init__(self, key):
    """
    Initializes the encryption class.
    
    Key is the encryption key.
    """
    self.salt = key
    
  def encrypt(self, string):
    """
    Encrypts the given plaintext.
    Returns the encrypted string.
    """
    return hashlib.sha256(self.salt.encode() + string.encode()).hexdigest()

    
  def compare(self, hashedPass, password):
    """
    Decrypts the given cipher
    Returns the decrypted string.
    """
    if hashlib.sha256(self.salt.encode() + password.encode()).hexdigest() == hashedPass:
      return "Success"
    return "Failed"
