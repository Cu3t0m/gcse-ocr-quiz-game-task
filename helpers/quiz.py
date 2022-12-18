"""
File Name: quiz.py
Author: Diwan Mohamed Faheer
Last Edit: 17.11.22

File Description: This file contains all the code for the most crucial part of the project- the quiz. It also updates the wins and game history each game. 
"""

import json
from helpers.functions import *
from helpers.sessions import *
import helpers.pages as pages
from art import *
import datetime
import re
from colored import *
import random

session = Session()
red = fg("red")
green = fg("green")
reset = attr('reset')

questions = json.load(open("./database/questions.json"))
options = [
["A.Guido van Rossum", "B.Bill Gates", "C.Linus Torvalds", "D.Mark Zuckerberg"],
["A.1989", "B.1991", "C.1995", "D.2000"],
["A.Monty Python", "B.The Marx Brothers", "C.The Three Stooges", "D.The Kids in the Hall"],
["A.A portion of a computer's hard drive that is used to simulate additional RAM", "B.Additional RAM that is physically installed in a computer", "C.A type of software that allows multiple operating systems to run on a single computer", "D.A feature that allows a computer to access data from the internet more quickly"],
["A.Storage devices that hold data that is not actively being used by the computer, such as hard drives and external storage devices", "B.The primary storage location for a computer's operating system and applications", "C.A type of storage that is used for backing up important data", "D.A type of storage that is used for temporary files"],
["A.A set of characters and symbols that a computer uses to represent text", "B.A set of characters and symbols that are used in programming languages", "C.A set of characters and symbols that are used for formatting documents", "D.A set of characters and symbols that are used for creating graphics and images"],
["A.7", "B.8", "C.16", "D.32"],
["A.16 or 32", "B.8 or 16", "C.32 or 64", "D.64 or 128"],
["A.Hertz (Hz)", "B.Kilobytes (KB)", "C.Megabytes (MB)", "D.Gigabytes (GB)"],
["A.The process of temporarily storing data in a buffer to allow for smooth playback of media", "B.A problem with the internet connection", "C.A problem with the media player software", "D.A problem with the media file itself"]
]

def new_game():
  guesses = []
  correct_guesses = 0
  question_num = 1

  for key in questions:
    time.sleep(0.5)
    clear()
    topbar()
    tprint(f"Quiz - Q{question_num}")
    print("-------------------")
    print(key)
    for i in options[question_num - 1]:
      print(i)
    guess = input("Enter (A,B,C, or D):").upper()

    while not re.match("^[A-D]*$", guess):  # Trying out regex for the first time
      clear()
      topbar()
      tprint(f"Quiz - Q{question_num}")
      print("-------------------")
      print(key)
      for i in options[question_num - 1]:
        print(i)
      print(red + f"Invalid Input '{guess}', Please try again" + reset)
      guess = input("Enter (A,B,C, or D):").upper()

    guesses.append(guess)

    correct_guesses += check_answer(questions.get(key), guess)

    question_num += 1

  display_score(correct_guesses, guesses)

  # --------------------------------


def check_answer(answer, guess):
  if answer == guess:
    print(green + "Correct!" + reset)
    return 1
  else:
    print(red + "Wrong!" + reset)
    return 0


# --------------------------------
def display_score(correct_guesses, guesses):
  clear()
  tprint(f"{session.get('name')}'s Results")
  print("Answers: ", end=" ")
  for i in questions:
    print(questions.get(i), end=" ")
  print()

  print("Guesses: ", end="")
  for i in guesses:
    print(i, end=" ")
  print()

  score = int((correct_guesses / len(questions)) * 100)
  if score >= 50:
    w = session.get("wins")
    coins = session.get("coins")
    coins += 23
    session.set("coins", coins)
    w += 1
    session.set("wins", w)
    gh = session.get("game_history")
    gh.append(f"Won a game on {datetime.datetime.utcnow()}")
    session.set("game_history", gh)
  else:
    gh = session.get("game_history")
    gh.append(
      f"Lost a game on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    session.set("game_history", gh)
  print("Your score is:" + str(score) + "%")
  play_again()


# --------------------------------
def play_again():
  response = input("Do you want to play again? (yes or no): ")
  response = response.lower()
  if response == "yes":
    new_game()
  else:
    pages.play_page()
