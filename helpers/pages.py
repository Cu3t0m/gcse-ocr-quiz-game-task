"""
File Name: pages.py
Author: Diwan Mohamed Faheer
Last Edit: 17.11.22

File Description: This file contains all the code for the main UI of the program. It is basically the HQ of the program since it calls funtions from different files and they automatically fall back to here after they are finished.
"""

from art import *
import os
import sys
import time
from helpers.oauth import OAuth
from helpers.sessions import Session
from helpers.functions import *
from selectmenu import SelectMenu
from helpers.quiz import *
from functools import wraps
import getpass
from terminaltables import *
from helpers.encryption import Encryption
main_page = SelectMenu()
main_page.add_choices(["New User?", "Existing User?"])

page_1 = SelectMenu()
page_1.add_choices(["Start Game", "Quiz Shop", "Game History", "Leaderboard", "Credits", "Settings", "Logout"])

profile_page =  SelectMenu()
profile_page.add_choices(["Change Avatar", "Change Password"])

shop_page = SelectMenu()
shop_page.add_choices(["Buy Items", "My Inventory",])
count = 0
oauth = OAuth()
session = Session()

encrypter = Encryption(key=os.getenv("key"))
def counter(func):
    inv_counter = 0

    @wraps(func)
    def wrap_function(*args, **kwargs):
        nonlocal inv_counter
        inv_counter += 1
        func(*args, **kwargs)

    def count():
        return inv_counter

    def reset():
        inv_counter = 0

    wrap_function.reset = reset
    wrap_function.count = count
    return wrap_function


def welcome():
    clear()
    tprint("Welcome")
    styled_typing("Made by Diwan Mohamed Faheer", 0.01)
    time.sleep(5)


def creditz():
    clear()
    tprint("Credits")
    styled_typing("Made solely by Diwan Mohamed Faheer", 0.01)
    time.sleep(5)


def login():
    clear()
    tprint("Login")
    print("Please note that the password will be hidden for security reasons.\n")
    u = input("Username: ")
    p = getpass.getpass("Password:")

    res = oauth.login(u, p)

    if res == "Success":
        oauth.set(u)
        print("Login Successful")
        return
    else:
        print(res)
        c = input("Do you want to try again?")
        if c == "y":
            login()
        else:
            return



def register():
    clear()
    tprint("Register")

    print("Please note that the password will be hidden for security reasons.\n")
    u = input("Username: ")
    p = getpass.getpass("Password:")
    while len(p) < 8:
        print("Password must be at least 8 characters")
        p = getpass.getpass("Password: ")

    res = oauth.register(u, p)

    if res == "Success":
        oauth.set(u)
        print("Registration Successful")
        return
    else:
        print(res)
        return



def home():
    clear()
    topbar()
    tprint("Quiz")
    result = main_page.select("Please choose an option")
    if result == "New User?":
        register()
    elif result == "Existing User?":
        login()
    else:
        print("Invalid option")

def shop():
  clear()
  topbar()
  tprint("Shop")  
  result = shop_page.select("Please choose an option")
  if result == "Buy Items":
    listings()
  elif result == "My Inventory":
    bar()
  else:
    tom()

def listings():
  clear()
  topbar()
  tprint("Listings")   
  loop = True
  table_data = [
    ['Name', 'Ability', 'Price'],
    ['Custom Skin', 'Change Avatar', '🔘 50'],
    ['Hint', 'Lets you have hints', '🔘 45']
  ] 
  table = SingleTable(table_data, "Leaderboard")
  table.justify_columns[2] = 'right'
  print(table.table)  
  buy_check()
  input("Press enter to exit...")

def buy_check():
  clear()
  topbar()
  tprint("Listings")   
  loop = True
  table_data = [
    ['Name', 'Ability', 'Price'],
    ['Custom Skin', 'Change Avatar', '🔘 50'],
    ['Hint', 'Lets you have hints', '🔘 45']
  ] 
  table = SingleTable(table_data, "Leaderboard")
  table.justify_columns[2] = 'right'
  print(table.table)  
  
  check = input("Do you want to buy something now?(y/n) ").lower()
  if check == "y":

    item_id = input("Please enter the name of the item you want to buy as it is: ")
    numx = 1
    
    while loop == True:
      if numx > len(table_data):
        loop=False
        print("Invalid name, please try again.")
      else:
        if table_data[numx][0] == item_id:
          coins = int(session.get("coins"))
          price = table_data[numx][2].strip("🔘 ")
          price = int(price)
          if coins < price:
            print("Not enough coins. Please earn more")
            loop = False
      
          else:
            coins = coins - price
            inventory = session.get("inventory")
            inventory.append(table_data[numx][0])
            session.set("coins", coins)
            session.set("inventory", inventory)
            print("Success")
            loop = False
        else:
          numx += 1
          pass
    
  else:
    pass  



def profile_menu():
    clear()
    topbar()
    tprint("Settings")
    result = profile_page.select("Please choose an option")
    if result == "Change Avatar":
      clear()
      topbar()
      tprint("Settings")
      check_inv = session.get("inventory")
      for x in check_inv:
        if check_inv[x] == "Custom Skin":
          print("This functionality has been disabled until further notice...")
    elif result == "Change Password":
      clear()
      topbar()
      tprint("Settings")
      u = session.get("name")
      print(f"Current Password: {u}")      
      new_p = input("What is your new password?: (Press enter to exit) ")
      loop = True
      while loop==True:
        if new_p == "":
          loop = False
          return
        else:
          oauth.update("password", encrypter.encrypt(new_p))

          loop = False
          clear()
          tprint("Success")      
    else:
      print("Invalid option")
      time.sleep(2)  


      
def play_page():
    clear()
    topbar()
    tprint("Quiz")
    result = page_1.select("Please choose an option")
    if result == "Game History":
        history()
    elif result == "Start Game":
        new_game()
    elif result == "Leaderboard":
        leaderboard()
    elif result == "Credits":
        creditz()
    elif result == "Settings":
        profile_menu()      
    elif result == "Logout":
        clear()
        w = session.get("wins")
        gh = session.get("game_history")
        coins = session.get("coins")
        inventory = session.get("inventory")
        oauth.update("wins", w)
        oauth.update("game_history", gh)   
        oauth.update("coins", coins)      
        oauth.update("inventory", inventory)      
        session.swipe()
        tprint("Logging out")
        time.sleep(2)
        start()
    elif result == "Quiz Shop":
        shop()
    else:
        print("Invalid option")
        time.sleep(2)

def history():
  clear()
  topbar()
  tprint("History")
  game_hist = session.get("game_history")
  if game_hist==None:
    print("Play a game to find your history here!")
  else:
    for x in game_hist:
      print(x)
  input("Press enter to exit...")
  return


def leaderboard():
  clear()
  topbar()
  tprint("Leaderboard") 
  print("Note: You may have to log out to update your score\n")
  scores, names = oauth.lb()
  count = 0
  top = 5 if len(scores) >= 5 else len(scores)

  table_data = [
    ['No.', 'Name', 'Wins'],
  ]  
  temp = []
  
  for x in range(0, len(scores)):
    dat = []
    dat.append("")
    dat.append(names[x])
    dat.append(scores[x])
    temp.append(dat) # temporary list
    

  srtd = sorted(temp, key=lambda l:l[2], reverse=True) # sorting using inbuilt function
  
  for l in range(len(srtd)):
    count +=1
    srtd[l][0] = f"{count}{numvert(count)}"

  for z in range(0, top):
    table_data.append(srtd[z])

  table = SingleTable(table_data, "Leaderboard")
  table.justify_columns[2] = 'right'
  print(table.table)
  input("Press enter to go back...")
  return


def numvert(number): 
  """
  Suffix Adder - adds suffixes to numbers
  """
  suffix = ["th", "st", "nd", "rd"]

  if number % 10 in [1, 2, 3] and number not in [11, 12, 13]:
      return suffix[number % 10]
  else:
      return suffix[0]


@counter # custom wrapper that counts how many times a function is called
def start():
    """
    Starting function - Tells us of existing users ect.
    """
    rl = start.count() # starting counter
    if rl == 1: # display welcome only once
        welcome()
        if session.get("logged_in"):
            clear()
            tprint("Warning")
            print("There is already an existing session, please log out if it isn't yours")
            c = input("Do you wish to proceed? (y/n) ").lower()
            if c == "y":
                play_page()
            else:
                w = session.get("wins")
                gh = session.get("game_history")
                coins = session.get("coins")
                inventory = session.get("inventory")
                oauth.update("wins", w)
                oauth.update("game_history", gh)   
                oauth.update("coins", coins)      
                oauth.update("inventory", inventory)      
                session.swipe()  # swipes the session
                home()  # restarts function
        else:
            home()
    else:
        s = session.get("logged_in")
        if s == True:
          play_page()
        else:
          home()
