"""
File Name: sessions.py
Author: Diwan Mohamed Faheer
Last Edit: 17.11.22

File Description: This file contains all the code for the sessions feature for my project. The sessions feature lets the user quickly fetch crucial information like Wins and Game History aswell as keeping the user logged in even while the program is off.
"""
import json
import uuid
import os
import time
import datetime
import requests

def edit(name, value):
  """
  Edit the Session info in a file.
  """
  try:
    with open('./database/session.json', 'r+') as f:
      session = json.load(f)
      session[name] = value 
      f.seek(0)
      json.dump(session, f, indent=4)
      f.truncate()  
    # Return message.
    return "Successfully edited session."
  except:
    return "Error storing session."

def read():
  """
  Read the Session info from a file.
  """
  
  # Read the session info from a file.
  with open('./database/session.json', 'r') as f:
    session = json.load(f)
  # Return the credentials.
  return session

def delete():
  """
  Delete the Session info from a file.
  """
  
  # Delete the session info from a file.
  with open('./database/session.json', 'w') as f:
    json.dump({}, f, indent=4)
    
  obj = {
    "name": "",
    "game_history": [],
    "session_id": f"{uuid.uuid4().hex}",
    "logged_in": False,
    "coins": 0,
    "inventory": []
  }
  with open('./database/session.json', 'w') as f:
    json.dump(obj, f, indent=4)  
  # Return the credentials.
  return "Successfully deleted session."
  
class Session:
  """
  Session class.
  """
  
  def __init__(self):
    """
    Initialize the Session class.
    """
    size = os.path.getsize("./database/session.json")
    if size > 0:
      pass
    else:
      obj = {
        "name": "",
        "game_history": [],
        "wins": 0,
        "session_id": f"{uuid.uuid4().hex}",
        "logged_in": False,
        "coins": 0,
        "inventory": []
      }
      with open('./database/session.json', 'w') as f:
        json.dump(obj, f, indent=4)

    # Return the credentials.
   

  def get(self, name):
    """
    Get the session.
    """
    obj = read()
    #print(obj) 
    return obj[name]
  
  def set(self, name, value):
    """
    Set the session.
    """
    r = edit(name, value)
    
#    if name == "game_history" or "wins":
#      oauth.update(name, value)
    if r != "Successfully edited session.":
      raise ValueError(r)
      
    return "Done"

  def swipe(self):
    """
    Swipe the session.
    """
    r = delete()
    if r!= "Successfully deleted session.":
      raise ValueError(r)
      
    return "Done"