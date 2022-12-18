"""
File Name: oauth.py
Author: Diwan Mohamed Faheer
Last Edit: 17.11.22

File Description: This file contains all the code for the authentication system in the program. This contains the login and register system. This file is responsible for the long term secure storage of user data where all passwords are also encrypted.
"""

import json
from helpers.encryption import Encryption
from helpers.sessions import Session
import time
import os
import uuid

encrypter = Encryption(key=os.getenv("key"))
session = Session()

def read():
  """
  Read the credentials info from a file.
  """
  try:
  # Read the credentials info from a file.
    with open('./database/credentials.json', 'r') as f:
      cred = json.load(f)

  except json.decoder.JSONDecodeError:
    return None
  return cred

def edit(u, name, value):
  """
  Edit the credentials info in a file.
  """
  try:
    with open('./database/credentials.json', 'r+') as f:
      credentials = json.load(f)
      creds = credentials['users']
      creds[u][name] = value 
      f.seek(0)
      json.dump(credentials, f, indent=4)
      f.truncate()  
    # Return message.
    return "Successfully edited credentials."
  except:
    return "Error storing credentials."
    
class OAuth:
    """
    OAuth helper class.
    """
  
    def __init__(self):
      self.salt = os.getenv("key")
      size = os.path.getsize("./database/credentials.json")
      if size > 0:
        pass
      else:
        obj = {
          "users": {}
        }
        with open('./database/credentials.json', 'w') as f:
          json.dump(obj, f, indent=4)

    def login(self, username, password):
      """
      Login to the quiz.
      """
      read_file = read()
      if read_file == None:
        return "Error reading credentials."
      
      try:
        credentials = read_file["users"][username]
      except KeyError:
        return "Not Found"      
        
      if not credentials:
        return "Not Found"
        
      salted_password = read_file["users"][username]["password"]
      check = encrypter.compare(salted_password, password)
      
      if check == "Success":
        session.set("name", username)
        session.set("logged_in", True)
        return f"Success"
      else:
        return "Invalid username or password"

    def set(self, username):
      """
      Get the info for a user.
      """
      read_file = read()
      if read_file == None:
        return "Error reading credentials."
            
      try:
        credentials = read_file["users"][username]
      except KeyError:
        return "Not Found"
        
      if not credentials:
        return "Not Found"
        
      session.set("wins", credentials["wins"])
      session.set("game_history", credentials["game_history"])
      session.set("inventory", credentials["inventory"])
      session.set("coins", credentials["coins"])
      return "Success"

    def update(self, name, value):  
      """
      Update a user's info.
      """
      read_file = edit(session.get("name"), name, value)
      return read_file

    def get(self, value, name=session.get("name")):
      """
      Get the info for a user.
      """
      read_file = read()
      
      try:
        credentials = read_file["users"][name][value]
      except KeyError:
        return "Not Found"

    def lb(self):
      read_file= read()
      usr = read_file["users"].keys()
      score = []
      names = []
      for x in usr:
        score.append(read_file["users"][x]["wins"])
        names.append(read_file["users"][x]["name"])
      return score, names
      
    def register(self, username, password):
      """
      Register a new user.
      """
      # Store the credentials in a file.

      with open('./database/credentials.json', 'r+') as f:
        users = json.load(f)
        users["users"][username] = {
          "name": username,
          "password": encrypter.encrypt(password),
          "wins": 0,
          "game_history": [],
          "user_id": f"{uuid.uuid4().hex}", 
          "coins": 0,
          "inventory": []
        }        
        f.seek(0)
        json.dump(users, f, indent=4)
        f.truncate()            

      time.sleep(1)
      self.login(username, password)
      # Return the credentialss.
      return "Success"      