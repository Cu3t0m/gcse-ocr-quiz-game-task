"""
File Name: functions.py
Author: Diwan Mohamed Faheer
Last Edit: 17.11.22

File Description: This file contains all the code for the extra functions in the program such as the topbar and the clear function.
"""
from art import *
import os
import sys
import time
from helpers.oauth import OAuth
from helpers.sessions import Session
from helpers.functions import *
import keyboard
import sys

oauth = OAuth()
session = Session()

def textload(text, num, loops):
    shell = sys.stdout
    shell.write(text,'stdout')
    dotes = int(num) * '.'
    for last in range(0,loops):
        for dot in dotes:
            keyboard.write('.')
            time.sleep(0.1)
        for dot in dotes:
            keyboard.write('\x08')
            time.sleep(0.1)
          
def topbar():
    logged_in = session.get("logged_in")  # inspired by flask_sessions

    size = os.get_terminal_size().columns

    if logged_in:
        user = session.get("name")
        print(f"| 👤 {user} | 🔘 {session.get('coins')} | 👑 {session.get('wins')} |")
    else:
        print("| 👤 Guest |")

    print("-" * size)


def styled_typing(text, speed):
    words = text
    for char in words:
        time.sleep(speed)
        sys.stdout.write(char)
        sys.stdout.flush()


def clear():
    os.system("cls" if os.name == "nt" else "clear")
