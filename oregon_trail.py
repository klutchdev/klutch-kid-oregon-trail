#!/bin/python3

#*##############################| OREGON TRAIL by KLUTCH |################################
#?################################## DEVELOPMENT LIST ####################################
### TODO:
  # Difficulty setting
    ## Easy, Normal, Hard
    ## Adjust modifiers and starting values for each difficulty level
  # Travel cycles
    ## Random events
    ## Time passed
    ## Locations
    ## River crossings
    ## Terrain and weather variables
  # Game conditionals
    ## Travel pace
    ## Travel distance
    ## Health depletion
    ## Food depletion
    ## Sickness and death
  # Game menus:
    ## Title screen menu
    ## Settings menu
    ## Save and load game menu
  # Interaction
    ## Indians
    ## Townsfolk
    ## Other travelers
    ## Trading
    ## Randomization
  # Supplies and purchases
    ## Subtract balance on purchases
    ## Add to balance if money added 
  # Highscores
    ## Show "Original Top Ten" high scores list
    ## Show "Current Top Ten" high scores list
    ## Reset the "Current Top Ten" high scores list
    ## Add player name to current high scores list if player qualifies
  # Saving and loading game progress
    ## Generate a file to save progress data using key value pairs
    ## Export save file as text file (or csv?) and convert to "read only" 
    ## Export readable PDF with current and/or end of game stats
    ## Load saved game files to continure game
  # Hunting Module
    ## Animal and terrain selection and randomization
    ## How much food produced from a hunt
    ## Length of hunt in days
  # Game dialog and interactivity
    ## General info, in-game messages, and errors
    ## Text animation and loading spinners
    ## Facts about the Oregon Trail AND the original Oregon Trail games
#*  COMPLETED:
  #* [√] Get names of the wagon party
  #* [√] Display wagon party menu with player name(s), health %, and current status
  #* [√] Display "deceased" under players that perish during the game
  #* [√] Display player name, health %, and health status
#? #######################################################################################
# IMPORTS
import sys          # SYSTEM FUNCTIONS
import os           # OS FUNCTIONS
import random       # RANDOM NUMBERS
import datetime     # TIME AND DATE
import time         # TIMING FUNCTIONS

# GAME DIALOG
divider = '------'* 6
select_option = 'SELECT AN OPTION:'
help_option = '\nPress [?] for HELP'
quit_option = '\nPress [q] to QUIT'
continue_option = '\nPress [enter] to continue'
selection_error = '\nINVALID SELECTION! \nPress [enter]...'
when_to_start = 'WHEN DO YOU WANT TO START?'
ask_travel_pace = 'How fast do you want to travel?'

# Stopping points in the game
stops = (
  'Independence, Missouri','Big Blue River Crossing','Fort Kearney',
  'Chimney Rock','Fort Laramie','Independence Rock','South Pass',
  'Fort Bridger','Green River Crossing','Soda Springs','Fort Hall',
  'Snake River Crossing','Fort Boise','Grande Ronde in the Blue Mountains',
  'Fort Walla Walla','The Dalles','Willamette Valley',)

# Months
months = (
  'January','February','March','April','May','June','July',
  'August','September','October','November','December',)

# Travel pace
travel_pace = (
  'Steady','Strenuous','Grueling')

# Rations consumption
rations_consumption = (
  'Filling','Meager','Bare Bones')

# Health status
health_status = (
  'Good','Fair','Poor','Very Poor','Dying')

# Sickness
sickness = (
  'is suffering from exhaustion.','is sick with typhoid fever.',
  'has cholera.','has the measles.','has dysentery.','has a fever.')

# Other travelers and townspeople
people = (
  'Zeke','Jed','Anna','Mary','Joey','Beth',
  'John','Sara','Henry','Emily')


# Supply stops
supply_stops = (
  'Matt\'s General Store','Fort Kearney','Fort Laramie',
  'Fort Bridger','Fort Hall','Fort Boise','Fort Walla Wall')


# GLOBALS
LEADER = ''         # Leader name
LEADER_HEALTH = 100 # Leader health
LEADER_SICK = False # Leader sickness

PL_2 = ''           # Person 2 name
PL_2_HEALTH = 74     # Person 2 health
PL_2_SICK = False   # Person 2 sickness

PL_3 = ''           # Person 3 name
PL_3_HEALTH = 49    # Person 3 health
PL_3_SICK = True   # Person 3 sickness

PL_4 = ''           # Person 4 name
PL_4_HEALTH = 24     # Person 4 health
PL_4_SICK = True    # Person 4 sickness

PL_5 = ''           # Person 5 name
PL_5_HEALTH = 0     # Person 5 health
PL_5_SICK = False   # Person 5 sickness

MONEY = 800         # Current balance
CLOTHES = 0         # Sets of clothes
CLOTHES_COST = 25   # Cost of clothes
FOOD = 0            # Pounds of food
FOOD_COST = 2       # Cost of food
AMMO = 0            # Rounds of ammunition
AMMO_COST = 1       # Cost of ammunition
OXEN = 0            # Qty of oxen
OXEN_COST = 25      # Cost of oxen
WHEELS = 0          # Qty of wagon wheels
WHEEL_COST = 10     # Cost of wagon wheels
AXLES = 0           # Qty of wagon axles
AXLE_COST = 25      # Cost of wagon axles
TONGUES = 0         # Qty of wagon tongues
TONGUE_COST = 50    # Cost of wagon tongues

MILES_TRAVELED = 0  # Miles traveled
TRAVEL_DAYS = 0     # Days traveled
REST_DAYS = 0       # Days spent resting
HUNT_DAYS= 0        # Days spent hunting
DIFFICULTY_LEVEL = 2

# FUNCTIONS
def clearConsole():   # Clear the console
  os.system(command="clear")

def chooseDifficulty():
  global DIFFICULTY_LEVEL
  clearConsole()
  print('CHOOSE A DIFFICULTY LEVEL\n')
  print('-----' * 6) # Line break
  print('[1] EASY')
  print('[2] NORMAL')
  print('[3] HARD')
  print('-----' * 6) # Line break
  print('[?] SHOW HELP\n')
  print('SELECTION: ')
  selection = input()
  if selection == '1':
    DIFFICULTY_LEVEL = 1
    difficulty = 'EASY'
  elif selection == '2':
    DIFFICULTY_LEVEL = 2
    difficulty = 'NORMAL'
  elif selection == '3':
    DIFFICULTY_LEVEL = 3
    difficulty = 'HARD'
  print('YOU CHOSE {}. ARE YOU SURE?'.format(difficulty))
  response = input()
  if response == 'n':
    chooseDifficulty()

def tooltips():
  clearConsole()
  print('''\n
        [MENU AND NAVIGATION]
        ---------------------------------------
        THESE COMMANDS ARE COMMONLY USED WHILE
        NAVIGATING THE GAMES MENUS, SETTINGS, 
        DIALOGUE SCREENS, AND WHEN THE USER 
        NEEDS TO INPUT AND/OR CONFIRM DATA.
           
          ACTION(S)   |    [KEY] 
        ----------------------------
        YES/SKIP/NEXT |   [ENTER]
          RETURN      |     [B]
         QUIT GAME    |     [Q]''')
  input()

def welcomeMessage(): # Show welcome message
  print('''
    Welcome to The Oregon Trail!
    --------------------------------------------------------------------------

    You're about to begin a great adventure, traveling the Oregon Trail across
    the rugged landscape of North America.  Your covered wagon, pulled by a
    team of oxen, will travel from Independence, Missouri, to the fertile
    Willamette Valley of the Oregon Territory--a journey of approximately 
    2,000 miles.

    Before you set off on the trail, register your name, the names of the
    members of your wagon party, and your occupation. After that, you'll
    need to buy supplies and make other important decisions.
    
    --------------------------------------------------------------------------
    
    press ENTER to continue''')
  time.sleep(0.5)
  input()

def getLeaderName():  # Get name of wagon party leader
  global LEADER, LEADER_HEALTH, LEADER_SICK
  clearConsole()
  LEADER = input('ENTER THE NAME OF THE WAGON PARTY LEADER:\n')
  print('SAVE LEADER AS {}?'.format(LEADER))
  selection = input()
  if selection == 'n':
    getLeaderName()
  # elif selection != 'n' or 'y':
  #   clearConsole()
  #   input(selection_error)
  #   getLeaderName()

def getPerson2Name(): # Get the name of person 2
  global PL_2, PL_2_HEALTH, PL_2_SICK
  clearConsole()
  print('\nLEADER: {}'.format(LEADER))
  PL_2 = input('\nENTER PERSON #2: ')
  print('\nSAVE PERSON #2 AS {}?'.format(PL_2))
  selection = input()
  if selection == 'n':
    getPerson2Name()
  # elif selection != 'n' or 'y':
  #   clearConsole()
  #   input(selection_error)
  #   getPerson2Name()

def getPerson3Name(): # Get the name of person 3
  global PL_3, PL_3_HEALTH, PL_3_SICK
  clearConsole()
  print('\nLEADER: {}'.format(LEADER))
  print('PERSON #2: {}'.format(PL_2))
  PL_3 = input('\nENTER PERSON #3: ')
  print('\nSAVE PERSON #3 AS {}?'.format(PL_3))
  selection = input()
  if selection == 'n':
    getPerson3Name()
  # elif selection != 'n' or 'y':
  #   clearConsole()
  #   input(selection_error)
  #   getPerson3Name()

def getPerson4Name(): # Get the name of person 4
  global PL_4, PL_4_HEALTH, PL_4_SICK
  clearConsole()
  print('\nLEADER: {}'.format(LEADER))
  print('PERSON #2: {}'.format(PL_2))
  print('PERSON #3: {}'.format(PL_3))
  PL_4 = input('\nENTER PERSON #4: ')
  print('\nSAVE PERSON #4 AS {}?'.format(PL_4))
  selection = input()
  if selection == 'n':
    getPerson4Name()  
  # elif selection != 'n' or 'y':
  #   clearConsole()
  #   input(selection_error)
  #   getPerson4Name()

def getPerson5Name(): # Get the name of person 5 
  global PL_5, PL_5_HEALTH, PL_5_SICK
  clearConsole()
  print('\nLEADER: {}'.format(LEADER))
  print('PERSON #2: {}'.format(PL_2))
  print('PERSON #3: {}'.format(PL_3))
  print('PERSON #4: {}'.format(PL_4))
  PL_5 = input('\nENTER PERSON #5: ')
  print('\nSAVE PERSON #5 AS {}?'.format(PL_5))
  selection = input()
  if selection == 'n':
    getPerson5Name()
  # elif selection != 'n' or 'y':
  #   clearConsole()
  #   input(selection_error)
  #   getPerson5Name()
    
def show_names():     # Show the names and current status of the wagon party
  global LEADER, LEADER_HEALTH, LEADER_SICK,\
    PL_2, PL_2_HEALTH, PL_2_SICK, PL_3, PL_3_HEALTH, PL_3_SICK,\
    PL_4, PL_4_HEALTH, PL_4_SICK, PL_5, PL_5_HEALTH, PL_5_SICK
  clearConsole() # Clear console
  print('\nWAGON PARTY:') # Title
  print(divider) # Divider
  # Wagon party leader
  print('LEADER: ' +LEADER) 
  if LEADER_HEALTH >= 76 and LEADER_HEALTH <= 100:
    print('HEALTH STATUS: Excellent')
    print('HEALTH AMOUNT: ' +str(LEADER_HEALTH) +'%')
  elif LEADER_HEALTH >= 51 and LEADER_HEALTH <= 75:
    print('HEALTH STATUS: Good')
    print('HEALTH AMOUNT: ' +str(LEADER_HEALTH) +'%')
  elif LEADER_HEALTH >= 25 and LEADER_HEALTH <= 50:
    print('HEALTH STATUS: Fair')
    print('HEALTH AMOUNT: ' +str(LEADER_HEALTH) +'%')
  elif LEADER_HEALTH < 25 and LEADER_HEALTH >= 1:
    print('HEALTH STATUS: Poor')
    print('HEALTH AMOUNT: ' +str(LEADER_HEALTH) +'%')
  elif LEADER_HEALTH == 0 and LEADER_SICK == True or False:
    print('STATUS: Deceased')
  elif LEADER_SICK == True and LEADER_HEALTH > 0:
    print('√ CURRENTLY SICK')
  
  # Person 2
  print('')
  print('PERSON #2: ' +PL_2)
  if PL_2_HEALTH >= 76 and PL_2_HEALTH <= 100:
    print('HEALTH STATUS: Excellent')
    print('HEALTH AMOUNT: ' +str(PL_2_HEALTH) +'%')
  elif PL_2_HEALTH >= 51 and PL_2_HEALTH <= 75:
    print('HEALTH STATUS: Good')
    print('HEALTH AMOUNT: ' +str(PL_2_HEALTH) +'%')
  elif PL_2_HEALTH >= 25 and PL_2_HEALTH <= 50:
    print('HEALTH STATUS: Fair')
    print('HEALTH AMOUNT: ' +str(PL_2_HEALTH) +'%')
  elif PL_2_HEALTH < 25 and PL_2_HEALTH >= 1:
    print('HEALTH STATUS: Poor')
    print('HEALTH AMOUNT: ' +str(PL_2_HEALTH) +'%')
  elif PL_2_HEALTH == 0 and PL_2_SICK == True or False:
    print('Deceased')
  elif PL_2_SICK == True and PL_2_HEALTH > 0:
    print('√ CURRENTLY SICK')
  elif len(PL_2) == 0:
    print('')

  # Person 3
  print('')
  print('PERSON #3: ' +PL_3)
  if PL_3_HEALTH >= 76 and PL_3_HEALTH <= 100:
    print('HEALTH STATUS: Excellent')
    print('HEALTH AMOUNT: ' +str(PL_3_HEALTH) +'%')
  elif PL_3_HEALTH >= 51 and PL_3_HEALTH <= 75:
    print('HEALTH STATUS: Good')
    print('HEALTH AMOUNT: ' +str(PL_3_HEALTH) +'%')
  elif PL_3_HEALTH >= 25 and PL_3_HEALTH <= 50:
    print('HEALTH STATUS: Fair')
    print('HEALTH AMOUNT: ' +str(PL_3_HEALTH) +'%')
  elif PL_3_HEALTH < 25 and PL_3_HEALTH >= 1:
    print('HEALTH STATUS: Poor')
    print('HEALTH AMOUNT: ' +str(PL_3_HEALTH) +'%')
  elif PL_3_HEALTH == 0 and PL_3_SICK == True or False:
    print('STATUS: Deceased')
  elif PL_3_SICK == True and PL_3_HEALTH > 0:
    print('√ CURRENTLY SICK')
  elif len(PL_3) == 0:
    print('')  

  # Person 4
  print('')
  print('PERSON #4: ' +PL_4)
  if PL_4_HEALTH >= 76 and PL_4_HEALTH <= 100:
    print('HEALTH STATUS: Excellent')
    print('HEALTH AMOUNT: ' +str(PL_4_HEALTH) +'%')
  elif PL_4_HEALTH >= 51 and PL_4_HEALTH <= 75:
    print('HEALTH STATUS: Good')
    print('HEALTH AMOUNT: ' +str(PL_4_HEALTH) +'%')
  elif PL_4_HEALTH >= 25 and PL_4_HEALTH <= 50:
    print('HEALTH STATUS: Fair')
    print('HEALTH AMOUNT: ' +str(PL_4_HEALTH) +'%')
  elif PL_4_HEALTH < 25 and PL_4_HEALTH >= 1:
    print('HEALTH STATUS: Poor')
    print('HEALTH AMOUNT: ' +str(PL_4_HEALTH) +'%')
  elif PL_4_HEALTH == 0 and PL_4_SICK == True or False:
    print('STATUS: Deceased')
  elif PL_4_SICK == True and PL_4_HEALTH > 0:
    print('√ CURRENTLY SICK')
  elif len(PL_4) == 0:
    print('')  

  # Person 5
  print('')
  print('PERSON #5: ' +PL_5)
  if PL_5_HEALTH >= 76 and PL_5_HEALTH <= 100:
    print('HEALTH STATUS: Excellent [√√√]')
    print('HEALTH AMOUNT: ' +str(PL_5_HEALTH) +'%')
  elif PL_5_HEALTH >= 51 and PL_5_HEALTH <= 75:
    print('HEALTH STATUS: Good [√]')
    print('HEALTH AMOUNT: ' +str(PL_5_HEALTH) +'%')
  elif PL_5_HEALTH >= 25 and PL_5_HEALTH <= 50:
    print('HEALTH STATUS: Fair [!]')
    print('HEALTH AMOUNT: ' +str(PL_5_HEALTH) +'%')
  elif PL_5_HEALTH < 25 and PL_5_HEALTH >= 1:
    print('HEALTH STATUS: Poor[!!!]')
    print('HEALTH AMOUNT: ' +str(PL_5_HEALTH) +'%')
  elif PL_5_HEALTH == 0 and PL_5_SICK == True or False:
    print('STATUS: Deceased')
  elif PL_5_SICK == True and PL_5_HEALTH > 0:
    print('√ CURRENTLY SICK')
  elif len(PL_5) == 0:
    print('')
  input(continue_option)
  shopMenu()

def showSupplies():   # Show current amount of supplies
  global CLOTHES, FOOD, AMMO, OXEN, WHEELS, AXLES, TONGUES
  clearConsole()
  print('\nCURRENT SUPPLIES:')
  print('-----' * 6) # Line break
  print('CLOTHES: ' +str(CLOTHES) +' sets')
  print('AMMO: ' +str(AMMO) +' rounds')
  print('FOOD: ' +str(FOOD) +' lbs.')
  print('OXEN: ' +str(OXEN))

  print('\nWAGON PARTS:') # Wagon parts
  print('-----' * 6) # Line break
  print('WHEELS: ' +str(WHEELS))
  print('AXLES: ' +str(AXLES))
  print('TONGUES: ' +str(TONGUES))
  print('\nMONEY:')
  print('-----' * 6) # Line break
  print('CURRENT BALANCE: $' +str(MONEY))
  input()
  shopMenu()

def buyFood():        # Buy food
  global FOOD, MONEY, FOOD_COST
  clearConsole()
  print('CURRENT FOOD AMOUNT: {}'.format(FOOD))
  print('YOUR BALANCE: ${}'.format(MONEY))
  print('-----' * 6) # Line break
  print('FOOD IS ${} PER RATION'.format(FOOD_COST))
  print('HOW MANY RATIONS DO YOU WANT TO BUY?\n')
  amount_purchased = int(input())
  FOOD = FOOD + amount_purchased
  MONEY = MONEY - (amount_purchased * FOOD_COST)
  total_purchase = amount_purchased * FOOD_COST
  print('YOU BOUGHT {} '.format(amount_purchased) +'RATIONS FOR ${}'.format(total_purchase))
  print('-----' * 6) # Line break
  print('YOUR UPDATED BALANCE: ${}'.format(MONEY))
  print('-----' * 6) # Line break
  print('\n[1] TO BUY MORE')
  print('\n[Enter] TO RETURN')
  selection = input()
  if selection == '1':
    buyFood()
  else:  
    shopMenu()
  
def buyClothes():     # Buy clothes
  global CLOTHES, MONEY, CLOTHES_COST
  clearConsole()
  print('CURRENT SETS OF CLOTHES: {}'.format(CLOTHES))
  print('YOUR BALANCE: ${}'.format(MONEY))
  print('-----' * 6) # Line break
  print('CLOTHES COST ${} per set'.format(CLOTHES_COST))
  print('HOW MANY SETS OF CLOTHES DO YOU WANT TO BUY?\n')
  amount_purchased = int(input())
  CLOTHES = CLOTHES + amount_purchased
  MONEY = MONEY - (amount_purchased * CLOTHES_COST)
  total_purchase = amount_purchased * CLOTHES_COST
  print('YOU BOUGHT {} '.format(amount_purchased) +'SETS OFCLOTHES FOR ${}'.format(total_purchase))
  print('-----' * 6) # Line break
  print('YOUR UPDATED BALANCE: ${}'.format(MONEY))
  print('-----' * 6) # Line break
  print('\n[1] TO BUY MORE')
  print('\n[Enter] TO RETURN')
  selection = input()
  if selection == '1':
    buyClothes()
  else:  
    shopMenu()
  
def buyAmmo():        # Buy ammo
  global AMMO, MONEY, AMMO_COST
  clearConsole()
  print('CURRENT ROUNDS OF AMMUNITION: {}'.format(AMMO))
  print('YOUR BALANCE: ${}'.format(MONEY))
  print('-----' * 6) # Line break
  print('AMMO COSTS ${} PER ROUND'.format(AMMO_COST))
  print('HOW MANY ROUNDS OF AMMO DO YOU WANT TO BUY?\n')
  amount_purchased = int(input())
  AMMO = AMMO + amount_purchased
  MONEY = MONEY - (amount_purchased * AMMO_COST)
  total_purchase = amount_purchased * AMMO_COST
  print('YOU BOUGHT {} '.format(amount_purchased) +'ROUNDS OF AMMO FOR ${}'.format(total_purchase))
  print('-----' * 6) # Line break
  print('YOUR UPDATED BALANCE: ${}'.format(MONEY))
  print('-----' * 6) # Line break
  print('\n[1] TO BUY MORE')
  print('\n[Enter] TO RETURN')
  selection = input()
  if selection == '1':
    buyAmmo()
  else:  
    shopMenu()

def buyOxen():        # Buy oxen
  global OXEN, MONEY, OXEN_COST
  clearConsole()
  print('CURRENT OXEN: {}'.format(OXEN))
  print('YOUR BALANCE: ${}'.format(MONEY))
  print('-----' * 6) # Line break
  print('OXEN COSTS ${} EACH'.format(OXEN_COST))
  print('HOW MANY OXEN DO YOU WANT TO BUY?\n')
  amount_purchased = int(input())
  OXEN = OXEN + amount_purchased
  MONEY = MONEY - (amount_purchased * OXEN_COST)
  total_purchase = amount_purchased * OXEN_COST
  print('YOU BOUGHT {} '.format(amount_purchased) +'OXEN FOR ${}'.format(total_purchase))
  print('-----' * 6) # Line break
  print('YOUR UPDATED BALANCE: ${}'.format(MONEY))
  print('-----' * 6) # Line break
  print('\n[1] TO BUY MORE')
  print('\n[Enter] TO RETURN')
  selection = input()
  if selection == '1':
    buyOxen()
  else:  
    shopMenu()
  
def buyWheels():      # Buy wheels
  global WHEELS, MONEY, WHEEL_COST
  clearConsole()
  print('SPARE WAGON WHEELS: {}'.format(WHEELS))
  print('YOUR BALANCE: ${}'.format(MONEY))
  print('-----' * 6) # Line break
  print('WHEELS COST ${} EACH'.format(WHEEL_COST))
  print('HOW MANY WHEELS DO YOU WANT TO BUY?\n')
  amount_purchased = int(input())
  WHEELS = WHEELS + amount_purchased
  MONEY = MONEY - (amount_purchased * WHEEL_COST)
  total_purchase = amount_purchased * WHEEL_COST
  print('YOU BOUGHT {} '.format(amount_purchased) +'WHEELS FOR ${}'.format(total_purchase))
  print('-----' * 6) # Line break
  print('YOUR UPDATED BALANCE: ${}'.format(MONEY))
  print('-----' * 6) # Line break
  print('\n[1] TO BUY MORE')
  print('\n[Enter] TO RETURN')
  selection = input()
  if selection == '1':
    buyWheels()
  else:  
    shopMenu()
  
def buyAxles():       # Buy axles
  global AXLES, MONEY, AXLE_COST
  clearConsole()
  print('SPARE AXLES: {}'.format(AXLES))
  print('YOUR BALANCE: ${}'.format(MONEY))
  print('-----' * 6) # Line break
  print('AXLES COST ${} EACH'.format(AXLE_COST))
  print('HOW MANY AXLES DO YOU WANT TO BUY?\n')
  amount_purchased = int(input())
  AXLES = AXLES + amount_purchased
  MONEY = MONEY - (amount_purchased * AXLE_COST)
  total_purchase = amount_purchased * AXLE_COST
  print('YOU BOUGHT {} '.format(amount_purchased) +'AXLES FOR ${}'.format(total_purchase))
  print('-----' * 6) # Line break
  print('YOUR UPDATED BALANCE: ${}'.format(MONEY))
  print('-----' * 6) # Line break
  print('\n[1] TO BUY MORE')
  print('\n[Enter] TO RETURN')
  selection = input()
  if selection == '1':
    buyAxles()
  else:  
    shopMenu()
  
def buyTongues():     # Buy axles
  global TONGUES, MONEY, TONGUE_COST
  clearConsole()
  print('SPARE TONGUES: {}'.format(TONGUES))
  print('YOUR BALANCE: ${}'.format(MONEY))
  print('-----' * 6) # Line break
  print('TONGUES COST ${} EACH'.format(TONGUE_COST))
  print('HOW MANY TONGUES DO YOU WANT TO BUY?\n')
  amount_purchased = int(input())
  TONGUES = TONGUES + amount_purchased
  MONEY = MONEY - (amount_purchased * TONGUE_COST)
  total_purchase = amount_purchased * TONGUE_COST
  print('YOU BOUGHT {} '.format(amount_purchased) +'TONGUES FOR ${}'.format(total_purchase))
  print('-----' * 6) # Line break
  print('YOUR UPDATED BALANCE: ${}'.format(MONEY))
  print('-----' * 6) # Line break
  print('\n[1] TO BUY MORE')
  print('\n[Enter] TO RETURN')
  selection = input()
  if selection == '1':
    buyTongues()
  else:  
    shopMenu()

def mainMenu():       # Main game menu
  clearConsole()
  print('OREGON TRAIL: 2020 by KLUTCH\n')
  print('''
  [MAIN MENU]
  SELECT AN OPTION:
  -------------------------------------
  [1] START GAME
  [2] LOAD GAME
  -------------------------------------
  [3] VIEW THE ORIGINAL OREGON TOP TEN
  [4] VIEW THE CURRENT TOP TEN
  [5] CLEAR THE CURRENT TOP TEN
  -------------------------------------
  [6] LEARN ABOUT THE TRAIL
  [7] TRAIL DISEASES
  -------------------------------------
  [9] QUIT''')
  print('\nYour selection: ')
  selection = input()
  if selection == '1':
    clearConsole()
    print('STARTING A NEW GAME.')
    print('\n(or press [9] to load a saved game)')
    selection = input()
    # if selection == '9':
    #   loadGame()
    if selection == 'n':
      mainMenu()  
  elif selection == '2':
    clearConsole()
    print('Load game feature coming soon!')
    input()
    mainMenu()
  elif selection == '3':
    clearConsole()
    print('''
    ORIGINAL OREGON TOP TEN:
    -------------------------------------
    [1] Stephen Meek
    [2] David Hastings
    [3] Andrew Sublette
    [4] Celinda Hines
    [5] Ezra Meeker
    [6] William Vaughn
    [7] Mary Bartlett
    [8] William Wiggins
    [9] Charles Hopper
    [10] Elijah White
    ''')
    input(continue_option)
    mainMenu()
  elif selection == '4':
    clearConsole()
    print('''
    CURRENT OREGON TOP TEN:
    -------------------------------------
    [1] 
    [2] 
    [3] 
    [4] 
    [5] 
    [6]
    [7] 
    [8] 
    [9] 
    [10]
    ''')
    print('NO HIGH SCORES YET')
    input()
    mainMenu()
  elif selection == '5':
    clearConsole()
    input('\nNO SCORES TO RESET!')
    input()
    mainMenu()
  elif selection == '6':
    clearConsole()
    print('''
    INTRODUCTION
    -------------------------------------------------------------------------------
    What was it like to cross 2,000 miles of plains, rivers, and mountains in 1848?
    The Oregon Trail" allows you relive one of the greatest adventures in
    American history: the journey taken by thousands of emigrants on the
    Oregon Trail. It was a long, difficult journey--one that often resulted in
    failure and death. But for those who succeeded, it led to a new and better
    life in the rich, fertile Willamette Valley of Oregon.  

    How will you make life-and-death decisions? How will you cross the rivers?
    How much and what kind of supplies should you take along? If you run low on
    provisions, will you be able to hunt or trade to get the food you need? Will
    you overcome the dangers of disease and severe weather?

    "The Oregon Trail" poses these and other exciting challenges.

    If for some reason you don't survive--your wagon burns, thieves steal your 
    oxen, you run out of provisions, or you die of cholera--don't give up! Unlike
    the real-life pioneers of 1848, you can try again and again until you succeed 
    and your name is added to "The Oregon Trail List of Legends."

    The object of "The Oregon Trail" is for you to make it all the way from
    Independence, Missouri, to Oregon's Willamette Valley. Along the way, you'll
    have many decisions to make.''' )
    input()
    mainMenu()
  elif selection == '7':
    clearConsole()
    print('''
          DISEASES AND TRAIL SICKNESS
          -------------------------------------------------------------------------------
          Various types of disease are common threats on the trail, especially during the
          second half of the journey as supplies run low or travelers become exhausted.
          Among these diseases are measles, cholera, dysentery, and typhoid. When
          members of your party fall ill, you would be wise to stop and rest for several
          days in order to aid their recovery.\n''')
    print('''TYPHOID
          -------------------------------------------------------------------------------
          Typhoid is a serious disease caused by a bacterial infection of the
          bloodstream. It's usually spread by contaminated food or water. Early
          symptoms include fever, headache, and weakness, later followed by a red rash.
          Often there's also diarrhea, nosebleeding, and coughing. Good food, water, and
          rest help in recovery, which may take several weeks. Untreated, it can lead to
          massive organ failure and death.\n''')
    print('''MEASLES
          -------------------------------------------------------------------------------
          Measles is a highly contagious disease that usually strikes children, although
          adults can get it if they've never had it before. Its symptoms include fever,
          cold-like symptoms (such as a sore throat), and a splotchy red rash. If
          patients get good food and rest, they almost always recover after several days.
          If ignored, however, it can lead to pneumonia and death, especially among
          infants and the elderly.\n''')
    print('''DYSENTARY
          -------------------------------------------------------------------------------
          Cholera is caused by a bacterial infection of the small intestine, acquired
          from contaminated food or water. Its symptoms include severe diarrhea,
          vomiting, muscle cramps, and weakness. If left untreated, its victims can
          quickly become dehydrated, go into a coma, and die. It's vital that patients
          rest and replace the water and salt they've lost. Recovery takes place within
          two to seven days.''')
    input()
    mainMenu()
  elif selection == '0':
    quitGame()
  else:
    input(selection_error) 

def shopMenu():       # Open Matts general store
  clearConsole()
  print('WELCOME TO MATTS GENERAL STORE!')
  print('-----' * 6) # Line break
  print('\nYOUR CURRENT SUPPLIES:')
  print('-----' * 6) # Line break
  print('CLOTHES: ' +str(CLOTHES))
  print('RATIONS: ' +str(FOOD))
  print('ROUNDS OF AMMO: ' +str(AMMO))
  print('OXEN: ' +str(OXEN))
  print('WHEELS: ' +str(WHEELS))
  print('AXLES: ' +str(AXLES))
  print('TONGUES: ' +str(TONGUES))
  print('-----' * 6) # Line break
  print('YOUR BALANCE: $' +str(MONEY))
  print(divider)
  print('[1] BUY CLOTHES\n[2] BUY FOOD\n[3] BUY AMMO\n')
  print('-----' * 6) # Line break
  print('[4] BUY OXEN')
  print('-----' * 6) # Line break
  print('''[5] BUY WAGON WHEELS\n[6] BUY WAGON AXLES\n[7] BUY WAGON TONGUES\n''')
  print('-----' * 6) # Line break
  print('[8] VIEW SUPPLIES\n[9] QUIT\n')
  selection = input()
  if selection == '1':
    buyClothes()
  elif selection == '2':
    buyFood()
  elif selection == '3':
    buyAmmo()
  elif selection == '4':
    buyOxen()
  elif selection == '5':
    buyWheels()
  elif selection == '6':
    buyAxles()
  elif selection == '7':
    buyTongues()
  elif selection == '8':
    showSupplies()
  elif selection == 9:
    quitGame()
  else:
    pass  

def quitGame():       # Quit the game
  print('Exiting game')
  sys.exit(0)
  time.sleep(1.0)
  

######################################! GAME LOGIC !######################################
clearConsole()      # Start with a clean terminal
welcomeMessage()    # Welcome screen
tooltips()          # Tooltips
mainMenu()          # Load the main menu
chooseDifficulty()  # Choose difficulty level
getLeaderName()     # Get leader name
getPerson2Name()    # Get 2nd name
getPerson3Name()    # Get 3rd name
getPerson4Name()    # Get 4th name
getPerson5Name()    # Get 5th name
show_names()        # Show player names
shopMenu()          # Open the shop menu

