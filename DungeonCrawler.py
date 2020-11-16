"""

1D Project Brief:
https://docs.google.com/document/d/14Yq8YuP0RxB080rZlBmDTTOS-8_ds3UmV0gc3L_Sv4s/edit

Dungeon Crawler Game Tutorial:
https://www.youtube.com/watch?v=G17XPI6t6kg

Deliverables:
  1) Game description
  2) Code Documentation
  3) Code itself
  4) 3 minute video

DESCRIPTION

<Insert game description here>

Dungeon Crawler Game?

DOCUMENTATION


Controls: WASD. Press M to view map, I to access inventory and C to check player profile/stats.

We can write stuff here to fulfil the documentation requirement


FEATURES TO IMPLEMENT:

ESSENTIALS (done):
map
input interface
controllable character
win condition

IMPORTANT:
fog-of-war (done)
health, monsters and combat system (done)
inventory system (done)
script writing and flavor texts (basically done)

GOOD TO HAVE:
loot system (somewhat done)
random events from chests/object interactions
character creation (partially done)
variable torch level (done)
hunger (done)



IF GOT TIME:
more attributes and damage calculations (partially done)
character classes (partially done)
load/save system
powerups
status effects
experience/lvl up
multiple levels
scaling enemies
skills and abilities


COLIN TIER:
smart enemy behaviours
procedually generated maps
procedually generated item effects
torchlight radius system


player stats ideas:
attack, defence,speed,vision,dodge,accuracy

item ideas:
torch fuel -> refuel torch when used
health potion -> restore 20 health
glow ring trinket -> increase light radius, if not acts as permanent torch (Idk how to implement scaling light radius yet tho)
some powerup that permanently increases a stat when used? (also a version that increases stat temporarily...idk how to implement yet )
"""

import math
from random import randint
from random import choice
from copy import deepcopy
from time import sleep

testMap = [
["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
["0", "P", " ", "G", "0", " ", " ", " ", " ", "0"],
["0", " ", "K", " ", "0", " ", "0", " ", " ", "0"],
["0", "C", "S", " ", " ", " ", " ", " ", " ", "0"],
["0", "C", "0", "G", " ", "0", " ", " ", " ", "0"],
["0", "C", "0", " ", " ", "0", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", "0", "0", " ", " ", " ", " ", " ", "0"],
["0", "H", " ", "S", " ", " ", "0", " ", "G", "E"],
["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
]

testMap2 = [
["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
["0", "P", " ", "0", "D", "S", "0", "C", "0", "0", "K", "0"],
["0", " ", " ", " ", " ", " ", " ", "G", " ", "D", " ", "0"],
["0", " ", " ", "S", "0", "0", "0", " ", " ", "0", "G", "0"],
["0", " ", "G", " ", "G", "0", " ", " ", "S", "0", " ", "0"],
["0", "S", " ", " ", " ", "C", " ", "0", " ", "S", " ", "0"],
["0", " ", "0", "0", " ", " ", " ", " ", " ", "C", " ", "0"],
["0", "C", "0", "C", "D", "0", "G", " ", "S", "0", "H", "0"],
["0", "0", "0", "0", "0", "0", "0", "0", " ", "D", " ", "0"],
["0", "C", "D", " ", " ", " ", "0", "C", "S", "C", "S", "0"],
["0", "G", "0", "0", "0", " ", "G", "H", " ", " ", " ", "0"],
["0", "C", "H", " ", "S", "S", "C", "S", "G", "0", " ", "0"],
["0", "0", "0", " ", "C", " ", " ", " ", " ", "0", " ", "0"],
["0", "E", "R", "D", "0", " ", "0", "H", " ", "0", "D", "0"],
["0", "0", "H", " ", "0", "C", "0", "C", " ", "0", "C", "0"],
["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
]

testMap3 = [
["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
["0", "P", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
]


"""
player stats ideas:
attack, defence,speed,vision,dodge,accuracy

"dagger","chainmail","short sword","small health potion","small food ration","torch fuel"

"""
#

weapons = {
    # Structured by how much they increase lower and upper dmg bound
    "empty":(0,0),
    "dagger":(1,1),
    "gladius":(2,1),
    "short sword":(1,3),
    "sword":(2,3),
    "spear":(1,5),
    "halberd":(2,6),
    "longsword":(3,5)
}

armor = {
    # Structured by how much they increase defence
    "empty":0,
    "leather armor":1,
    "chainmail":2,
    "scale armor":3,
    "plate armor":4,
    "dragonscale armor":5
}

# To be done?
trinket = {

}

consumables = {
    # Structured by the stat they restore and by how much
    "small health potion": {
        "health": 15,
    },
    "health potion": {
        "health": 25,
    },
    "large health potion": {
        "health": 35,
    },
    "small torch fuel": {
        "torch": 5,
    },
    "torch fuel": {
        "torch": 10,
    },
    "large torch fuel": {
        "torch": 20,
    },
    "small food ration": {
        "food": 8,
        "health": 2
    },
    "food ration": {
        "food": 16,
        "health": 4
    },
    "large food ration": {
        "food": 24,
        "health": 6
    },
}


mapLoot = {
    # Strucured by the type of lootbox u can find and what is inside them, with gold by range its loot by possibility in perecentage
    "treasure chest": {
        "gold": [25,100],
        "possible loot": {
            "scale armor":5,
            "dragonscale armor":1,
            "plate armor":2,
            "chainmail":5,
            "gladius":5,
            "large torch fuel":10,
            "large health potion":10,
            "large food ration":10,
            "health potion":10,
            "torch fuel":10,
            "food ration":10,
            "small torch fuel":15,
            "small health potion":15,
            "small food ration":15,
            "health potion":10,
            "torch fuel":10,
            "food ration":10
        }
    },

    "box of supplies": {
        "gold": [1,10],
        "possible loot": {
            "large torch fuel":10,
            "large health potion":10,
            "large food ration":10,
            "health potion":25,
            "torch fuel":25,
            "food ration":25,
            "small torch fuel":50,
            "small health potion":50,
            "small food ration":50
        }
        
    },
    "box of equipment": {
        "gold": [1,5],
        "possible loot": {
            "dagger":55,
            "short sword":30,
            "spear":15,
            "gladius":15,
            "sword":10,
            "halberd":5,
            "longsword":5,
            "leather armor":55,
            "chainmail":15,
            "scale armor":7,
            "plate armor":3
        }
    },
    "fuel box": {
        "gold": [1,5],
        "possible loot": {
            "small torch fuel":50,
            "small torch fuel":40,
            "small torch fuel":20,
            "torch fuel":40,
            "large torch fuel":30,
        }  
        
    },
    
    "potion pouch": {
        "gold": [1,5],
        "possible loot": {
            "small health potion":90,
            "small health potion":50,
            "small health potion":30,
            "health potion":40,
            "health potion":20,
            "large health potion":20,
        }       
    }
}

# CHARACTER CLASSES:
classes = {
    "warrior": {
        "name": "Aragon",
        "class":"warrior",
        "health": {
            "max":50,
            "current":50
        },
        "attack": [4,6],
        "defence": 1,
        "speed": 7,
        "accuracy": 80,
        "dodge": 7,
        "equipments": {
            "armor":"empty",
            "main hand":"empty",
            "trinket":"empty"
        },
        "status": [],
        "inventory": ["small health potion"],
        "gold": 0,
        "torch":{
            "max":20,
            "current":15
        },
        "food": {
            "max":25,
            "current":20
        }
    },

    "ranger": {
        "name": "PlaceholderName",
        "class":"ranger",
        "health": {
            "max":35,
            "current":35
        },
        "attack": [3,6],
        "defence": 0,
        "speed": 11,
        "accuracy": 90,
        "dodge": 20,
        "equipments": {
            "armor":"empty",
            "main hand":"empty",
            "trinket":"empty"
        },
        "status": [],
        "inventory": ["small health potion"],
        "gold": 0,
        "torch":{
            "max":25,
            "current":20
        },
        "food": {
            "max":25,
            "current":20
        }
    },

    "beserker": {
        "name": "PlaceholderName",
        "class":"beserker",
        "health": {
            "max":40,
            "current":40
        },
        "attack": [3,8],
        "defence": 0,
        "speed": 6,
        "accuracy": 75,
        "dodge": 5,
        "equipments": {
            "armor":"empty",
            "main hand":"empty",
            "trinket":"empty"
        },
        "status": [],
        "inventory": ["small health potion"],
        "gold": 0,
        "torch":{
            "max":15,
            "current":15
        },
        "food": {
            "max":20,
            "current":20
        }
    },

    "survivalist": {
        "name": "PlaceholderName",
        "class":"survivalist",
        "health": {
            "max":55,
            "current":55
        },
        "attack": [3,5],
        "defence": 1,
        "speed": 10,
        "accuracy": 80,
        "dodge": 15,
        "equipments": {
            "armor":"empty",
            "main hand":"empty",
            "trinket":"empty"
        },
        "status": [],
        "inventory": ["small health potion","small torch fuel","small health potion"],
        "gold": 0,
        "torch":{
            "max":30,
            "current":25
        },
        "food": {
            "max":35,
            "current":30
        }
    }

}

# Add new monsters/encounters here
nonPlayableCharacters = {
    "G": {
        "name": "Goblin",
        "health": {
            "max":23,
            "current":23
        },
        "attack": [2,6],
        "defence": 0,
        "speed": 7,
        "accuracy": 75,
        "dodge": 10,
        "status": [],
        "possible loot": {
            # Structured by loot and loot chance
            "small food ration":45,
            "small torch fuel":20,
            "food ration":10,
            "small health potion":20,
            "health potion":5,
            "dagger":20,
            "leather armor":10,
            "gladius":5,
            "short sword":2
        },
        "gold": [4,12],
        "intent": "hostile",
        "behaviour": "simple"
    },

    "S": {
        "name": "Slime",
        "health": {
            "max":30,
            "current":30
        },
        "attack": [2,4],
        "defence": 0,
        "speed": 4,
        "accuracy": 65,
        "dodge": 0,
        "status": [],
        "possible loot": {
            "small torch fuel":50,
            "torch fuel":10,
            "large torch fuel":5,
            "small food ration":5,
            "small health potion":5
        },
        "gold": [2,8],
        "intent": "hostile",
        "behaviour": "simple"
    },

    "D": {
        "name": "Dire Wolf",
        "health": {
            "max":20,
            "current":20
        },
        "attack": [4,7],
        "defence": 0,
        "speed": 12,
        "accuracy": 75,
        "dodge": 16,
        "status": [],
        "possible loot": {
            # Structured by loot and loot chance
            "small food ration":85,
            "food ration":40,
            "large food ration":20,
            "small food ration":5,
            "small health potion":5
        },
        "gold": [8,20],
        "intent": "hostile",
        "behaviour": "simple"
    },

    "H": {
        "name": "Hobgoblin",
        "health": {
            "max":40,
            "current":40
        },
        "attack": [4,8],
        "defence": 1,
        "speed": 10,
        "accuracy": 80,
        "dodge": 10,
        "status": [],
        "possible loot": {
            "small food ration":95,
            "food ration":25,
            "small health potion":45,
            "health potion":25,
            "dagger":75,
            "leather armor":55,
            "chainmail":5,
            "gladius":10,
            "short sword":15,
            "spear":5,
        },
        "gold": [10,25],
        "intent": "hostile",
        "behaviour": "simple"
    },

    "R": {
        "name": "Revenant",
        "health": {
            "max":50,
            "current":50
        },
        "attack": [5,10],
        "defence": 2,
        "speed": 7,
        "accuracy": 75,
        "dodge": 5,
        "status": [],
        "possible loot": {
            "small torch fuel":50,
            "torch fuel":10,
            "small health potion":90,
            "health potion":30,
            "large health potion":10,
            "dagger":75,
            "leather armor":60,
            "chainmail":40,
            "gladius":20,
            "short sword":20,
            "spear":15
        },
        "gold": [10,25],
        "intent": "hostile",
        "behaviour": "simple"
    }
    
}


# use this function to print map in human-readable format
def printMap(map):
    for row in map:
        print(' '.join(row))


# Use this whenever you want player input
def playerAction(availableActions):
    print(f"Available actions: {availableActions}")
    while True:
        playerInput = input("Enter your action: ").upper()
        if playerInput not in availableActions:
            print(f"{playerInput} is an invalid action. Please try again.")
        else:
            break
    return availableActions[playerInput].lower()

# Used to determine enemy actions
def enemyAction(inputEnemy):
    # Add smart enemy behaviours and logic here in the future perhaps
    if inputEnemy["behaviour"] == "simple":
        return "attack"

# Updates current map after movement
def updateMap(inputMap, inputX, inputY, inputPrevX, inputPrevY):
    # replaces player's prev position with a whitespace
    inputMap[inputPrevY][inputPrevX] = " "
    # moves player to latest coordinate
    inputMap[inputY][inputX] = "P"
    return inputMap

# Handles using of inventory items
def handleUse(inputCharacter, inputItem):
    inputCharacter["inventory"].remove(inputItem)
    # Possible optimisation with a for loop?
    
    if inputItem in consumables:
        for effect in consumables[inputItem]:
            #offset = 0
            #inputCharacter[effect]["current"] += consumables[inputItem][effect]
            #if inputCharacter[effect]["current"] > inputCharacter[effect]["max"]:
                #offset = inputCharacter[effect]["current"] - inputCharacter[effect]["max"]
                #inputCharacter[effect]["current"] -= offset
            difference = inputCharacter[effect]["max"] - inputCharacter[effect]["current"]
            amountRestored = min(consumables[inputItem][effect], difference)
            inputCharacter[effect]["current"] += amountRestored
            print(f"Restored {inputCharacter['name']}'s {effect} by {amountRestored}.")


    # To implement choice of equipping in either main hand or off hand (perhaps)
    # First, check which slot equipment belongs. If current equipment slot not empty, remove current equipment first before replacing with new equipment
    elif inputItem in weapons:
        if inputCharacter["equipments"]["main hand"] != "empty":
            inputCharacter["inventory"].append(inputCharacter["equipments"]["main hand"])
            print(f"You remove your {inputCharacter['equipments']['main hand']} and put it in your inventory.")
        inputCharacter["equipments"]["main hand"] = inputItem
        print(f"You equipped your {inputItem} in your Main Hand slot ( + {weapons[inputItem][0]}-{weapons[inputItem][0]} attack ).")

    elif inputItem in armor:
        if inputCharacter["equipments"]["armor"] != "empty":
            inputCharacter["inventory"].append(inputCharacter["equipments"]["armor"])
            print(f"You remove your {inputCharacter['equipments']['armor']} and put it in your inventory.")
        inputCharacter["equipments"]["armor"] = inputItem
        print(f"You equipped your {inputItem} in your Armor slot ( + {armor[inputItem]} defence ).")

    elif inputItem in trinket:
        if inputCharacter["equipments"]["trinket"] != "empty":
            inputCharacter["inventory"].append(inputCharacter["equipments"]["trinket"])
            print(f"You remove your {inputCharacter['equipments']['trinket']} and put it in your inventory.")
        inputCharacter["equipments"]["trinket"] = inputItem
        print(f"You equipped your {inputItem} in your Trinket slot")
    
    else:
        print("You can't use that item!")
        inputCharacter["inventory"].append(inputItem)

def describeSurroundings(inputPlayerMap,x,y):

    # Add object descriptions here
    objectDescriptions = {
        "0":"a solid wall",
        "G":"a hidious goblin",
        "H":"a mischievous hobgoblin",
        "D":"an agile dire wolf",
        "S":"a glob of slime",
        "R":"a dangerous undead revenant",
        "E":"a way out",
        ".":"nothing",
        "K":"the dungeon key",
        "C":"some dungeon loot",
        " ":"an empty room"
    }
    north = inputPlayerMap[y-1][x]
    east = inputPlayerMap[y][x+1]
    south = inputPlayerMap[y+1][x]
    west = inputPlayerMap[y][x-1]

    # Possible optimisation with a for loop?
    
    if north in objectDescriptions:
        print(f"You see {objectDescriptions[north]} to your North.")
    else: #Handles unknown object
        print(f"You see an undocumented/unknown object '{north}' to your North.")

    if east in objectDescriptions:
        print(f"You see {objectDescriptions[east]} to your East.")
    else:
        print(f"You see an undocumented/unknown object '{east}' to your East.")

    if south in objectDescriptions:
        print(f"You see {objectDescriptions[south]} to your South.")
    else:
        print(f"You see an undocumented/unknown object '{south}' to your South.")

    if west in objectDescriptions:
        print(f"You see {objectDescriptions[west]} to your West.")
    else:
        print(f"You see an undocumented/unknown object '{west}' to your West.")

    

#Future update may include handling encounters with neutral or friendly characters that you can interact with.
def handleEncounter(inputCharacter, inputNPC):
    player = inputCharacter
    print(
        f"{player['name']} has encountered a {inputNPC['intent']} {inputNPC['name']}!")

    if inputNPC['intent'] == "hostile":
        inCombat = True
        playerDefeat = False
        print("Combat Start!")

        #Copies NPC. This means that state of NPC wont be saved after running away from them
        enemy = deepcopy(inputNPC)

        #Compare speed to see if enemy will act first
        enemyInitiative = True if enemy['speed'] > player['speed'] else False

        while inCombat:
            combatLog =  (
                f"\n"
                f"{player['name']}\'s health: {player['health']['current']}/{player['health']['max']}\n"
                f"{enemy['name']}\'s health: {enemy['health']['current']}/{enemy['health']['max']}\n"
                f"{player['name']}\'s chance to hit: {max(math.floor(((player['accuracy'] - enemy['dodge'])/player['accuracy'])*100) + (player['speed'] - enemy['speed']),10)}%\n"
                f"{player['name']}\'s chance to dodge: {100 - max(math.floor(((enemy['accuracy'] - player['dodge'])/enemy['accuracy'])*100) + (enemy['speed'] - player['speed']),5)}%\n"
                f"{player['name']}\'s damage: {player['attack'][0] + weapons[player['equipments']['main hand']][0]} - {player['attack'][1] + weapons[player['equipments']['main hand']][1]}\n"
                f"{player['name']}\'s defence: {player['defence'] + armor[player['equipments']['armor']]}\n"

            )
            print(combatLog)
            #print(f"{player['name']}\'s health: {player['health']['current']}.")
            #print(f"{enemy['name']}\'s health: {enemy['health']['current']}.")

            consumeTurn = True

            combatControls = {
                "A": "Attack",
                "W": "Wait", 
                "D": "Describe",
                "I": "Inventory",
                "C": "Character",
                "E": "Equipment",
                "R": "Run",
            }
            # Player's turn
            
            # Allow player input if enemy is not acting first
            if not enemyInitiative:
                playerInput = playerAction(combatControls)
            else:
                playerInput = "enemyInitiative"

            # Handle player inputs
            if playerInput == "attack":
                # Maybe calculate dodge and accuracy, whether attack hits, here.
                # Hit chance formula modified from https://www.gamedev.net/forums/topic/685930-the-simplest-but-most-effective-and-intuitive-way-to-implement-accuracy-and-dodge-chance-in-an-rpg/
                chanceToHit = max(math.floor(((player['accuracy'] - enemy['dodge'])/player['accuracy'])*100) + (player['speed'] - enemy['speed']),10)
                print(f"\n({chanceToHit}%) You attempt to strike...")
                if randint(0,100) < chanceToHit:
                    # Calculates lower and upper bound of damage based on base attack + main weapon dmg 
                    lowerBoundDamage = player['attack'][0] + weapons[player["equipments"]["main hand"]][0] # + math.floor(weapons[player["equipments"]["offHand"]][0]/2)
                    upperBoundDamage = player['attack'][1] + weapons[player["equipments"]["main hand"]][1] # + math.floor(weapons[player["equipments"]["offHand"]][1]/2)

                    # max is to prevent negative damage from being dealt
                    damage = max(randint(lowerBoundDamage,upperBoundDamage) - (enemy['defence']),0)
                    enemy['health']['current'] -= damage
                    print(f"You hit the {enemy['name']} for {damage} damage!")
                
                else:
                    print("You missed!")

            if playerInput == "wait":
                print("You bide your time...")

            if playerInput == "run":
                # minimum chance to run away is 10%
                chanceToRun = max(math.floor((player['speed']/enemy['speed'])*100),10)
                print(f"({chanceToRun}%) You try to run...")
                if randint(0,100) < chanceToRun:
                    print("...and retreated succesfully!")
                    return "retreated"
                else:
                    print("...but you were unsuccessful...")

            
            if playerInput == "character":
                consumeTurn = False
                print("______________________________________")
                for info in player:
                    print(f"{str(info).capitalize()}: {str(player[info]).capitalize()}")
                print("______________________________________")

            if playerInput == "describe":
                consumeTurn = False
                print("______________________________________")
                for info in enemy:
                    print(f"{str(info).capitalize()}: {str(enemy[info]).capitalize()}")
                print("______________________________________")

            if playerInput == "inventory":
                consumeTurn = False
                inventoryControls = {'X':"Go Back"}
                for idx,item in enumerate(player['inventory']):
                    inventoryControls[str(idx)] = item
                print("Select item to equip/consume.")
                inventoryInput = playerAction(inventoryControls)
                if inventoryInput != "go back":
                    #Consumes a turn in combat if player decides to use/equip an item
                    consumeTurn = True
                    handleUse(player, inventoryInput)

            if playerInput == "equipment":
                consumeTurn = False
                equipmentsControls = {'X':"Go Back"}
                for idx,slot in enumerate(player['equipments']):
                    if player['equipments'][slot] != "empty":     
                        equipmentsControls[str(idx)] = player['equipments'][slot]
                print(f"Select item to unequip.")
                equipmentsInput = playerAction(equipmentsControls)
                if equipmentsInput != "go back":
                    #Consumes a turn in combat if player decides to unequip an item
                    consumeTurn = True
                    # Handles unequipping (consider replacing with a function to make it neater?)
                    for slot in player['equipments']:
                        if player['equipments'][slot] == equipmentsInput:
                            print(f"You remove your {player['equipments'][slot]} from your {slot} slot and put it in your inventory.")
                            player['inventory'].append(equipmentsInput)
                            player['equipments'][slot] = "empty"

            # Handle killing of enemy
            if enemy['health']['current'] <= 0:
                inCombat = False
                print("______________________________________")
                print(f"You slew the {enemy['name']}!")
                for loot in enemy['possible loot']:
                    if randint(0,100) < enemy['possible loot'][loot]:
                        player['inventory'].append(loot)
                        print(f"You take the {loot} from the dead {enemy['name']}.")
                goldReceived = randint(enemy['gold'][0],enemy['gold'][1]) 
                player['gold'] += goldReceived
                print(f"You received {goldReceived} gold from the dead {enemy['name']}.")
                break

            #Informs player that enemy acted first due to them having higher speed
            if playerInput == "enemyInitiative":
                print(f"The enemy {enemy['name']} acted first!")

            if consumeTurn:
                # Enemy's turn
                enemyInput = enemyAction(enemy)
                enemyInitiative = False

                # Handle enemy inputs
                if enemyInput == "attack":
                    chanceToHit = max(math.floor(((enemy['accuracy'] - player['dodge'])/enemy['accuracy'])*100) + (enemy['speed'] - player['speed']),5)
                    print(f"({chanceToHit}%) The {enemy['name']} attempts to attack you...")
                    if randint(0,100) < chanceToHit:
                        lowerBoundDamage = enemy['attack'][0]
                        upperBoundDamage = enemy['attack'][1]
                        damage = max(randint(lowerBoundDamage,upperBoundDamage) - (player['defence'] + armor[player["equipments"]["armor"]]),0)
                        player['health']['current'] -= damage
                        print(f"The {enemy['name']} hit you for {damage} damage!")
                    else:
                        print(f"You dodged the {enemy['name']}'s attack!")

            # Handle combat-ending event
            if player['health']['current'] <= 0:
                inCombat = False
                playerDefeat = True
                print(f"You were slain by the {enemy['name']}!")
                break

    return "defeat" if playerDefeat else "victory"

# Updates player-visible map. When vision is True, reveal 1 tile around player for each movement
def updateFog(inputPlayerMap, inputCurrentMap, inputX, inputY, inputPrevX, inputPrevY, vision=False):

    #Replace tile player was previously on with an empty space
    inputPlayerMap[inputPrevY][inputPrevX] = inputCurrentMap[inputPrevY][inputPrevX]
    
    #Reveal player's current tile
    inputPlayerMap[inputY][inputX] = inputCurrentMap[inputY][inputX]

    

    if vision:
        #Reveals surounding tiles by setting those tiles in player map to be equal to the actual map
        inputPlayerMap[inputY+1][inputX] = inputCurrentMap[inputY+1][inputX]
        inputPlayerMap[inputY-1][inputX] = inputCurrentMap[inputY-1][inputX]
        inputPlayerMap[inputY][inputX+1] = inputCurrentMap[inputY][inputX+1]
        inputPlayerMap[inputY][inputX-1] = inputCurrentMap[inputY][inputX-1]

    #returns updated map
    return inputPlayerMap

#Initialises a fogged version of the current Map
def fogMap(inputMap):
    # normal methods of copy does not work if list contains objects (in this case it contains lists which I guess are objects). Hence, deep copy required to prevent old list from being overwritten.
    outputMap = deepcopy(inputMap)
    for idxY, row in enumerate(outputMap):
        for idX, pos in enumerate(row[:]):
            if pos != "P":
                outputMap[idxY][idX] = "."
    return outputMap

# Main game 
def main(inputMap):

    # INITIALISE MAP
    currentMap = inputMap
    playerMap = fogMap(currentMap)

    # NAME SELECT
    welcomeText = """
    _____________________________________________________________________________________

    Welcome! The goal is to escape the Dungeon by finding the key and unlocking the exit.

    Howver, the dungeon is foggy, and despite having a torch, you can only reveal a small area
    around you. There will be monsters and loot scattered across the play area.

    Pay close attention to your health, food and torch level as you traverse the Dungeon.
    _____________________________________________________________________________________
    
    Is this your first time playing? (Enter 1 for 'Yes' or 0 for 'No')
    """
    print(welcomeText)
    tutorialInput =  playerAction({"0":"No","1":"Yes"})

    if tutorialInput.lower() == "yes" :
        # tutorial goes here
        print("Too bad the tutorial isn't done yet. Pick it up as you go along.")
        sleep(1)
    else:
        print("Great! lets go!")
        
    
    sleep(1)
    playerName = input("Please select a name for your character: ")

    # CLASS SELECT

    classSelectText = """
    _____________________________________________________________________________________
    Available classes:

    Warrior: Good all-rounder.
    Ranger: Dextrous and survival-savvy but sacrifices power and durability.
    Beserker: Powerful in combat but neglects defences and supplies.
    Survivalist: Durable and start with more supplies, less combat oriented.
    _____________________________________________________________________________________
    
    """
    print(classSelectText)
    classSelected = False
    classesControls = {}
    for idx,classChoice in enumerate(classes):    
        classesControls[str(idx)] = classChoice
    print("Please select a character class by entering the corresponding digit: ")
    classesInput = playerAction(classesControls)
    if classesInput != "go back":
        classes[classesInput]['name'] = playerName
        print(f"Class selected: {classesInput}!")
        print("_____________________________________________________________________________________")
        for info in classes[classesInput]:
            print(f"{str(info).capitalize()}: {str(classes[classesInput][info]).capitalize()}")
        print("_____________________________________________________________________________________")
        classSelected = True
        player = classes[classesInput]
    sleep(1)
    input("Press enter to continue.")
    
    #Shows map to player at start of game
    

    playerInput = ""

    # MAP CONTROLS
    mapControls = {
        "W": "Up",
        "A": "Left",
        "S": "Down",
        "D": "Right",
        "M": "Map",
        "I": "Inventory",
        "E": "Equipment",
        "C": "Character",
        "Q": "Quit"
        }

    # INITIALISE POSITION AND TURN COUNTER
    x = 1
    y = 1
    turn = 1
    prevX = x
    prevY = y
    playerMap = updateFog(playerMap,currentMap,x,y,prevX,prevY,True)
    printMap(playerMap)

    while playerInput != "quit":
        prevX = x
        prevY = y

        # Whichever action that doesnt consume a turn should set this as false
        consumeTurn = True

        #Prompt player for input
        playerInput = playerAction(mapControls)

        if playerInput == "quit":
            print("You succumbed to the dangers of the Dungeon...Game Over.")
            break

        if playerInput == "map":
            consumeTurn = False
            printMap(playerMap)

        if playerInput == "character":
            consumeTurn = False
            print("______________________________________")
            for info in player:
                print(f"{str(info).capitalize()}: {str(player[info]).capitalize()}")
            print("______________________________________")

        if playerInput == "inventory":
            consumeTurn = False
            inventoryControls = {'X':"Go Back"}
            for idx,item in enumerate(player['inventory']):
                inventoryControls[str(idx)] = item
            print("Select item to equip/consume.")
            inventoryInput = playerAction(inventoryControls)
            if inventoryInput != "go back":
                handleUse(player, inventoryInput)
                torchLit = True if player['torch']['current'] > 0 else False
                playerMap = updateFog(playerMap,currentMap,x,y,prevX,prevY,torchLit)
                sleep(1)

        if playerInput == "equipment":
            consumeTurn = False
            equipmentsControls = {'X':"Go Back"}
            for idx,slot in enumerate(player['equipments']):
                if player['equipments'][slot] != "empty":     
                    equipmentsControls[str(idx)] = player['equipments'][slot]
            print(f"Select item to unequip.")
            equipmentsInput = playerAction(equipmentsControls)
            if equipmentsInput != "go back":
                # Handles unequipping (consider replacing with a function to make it neater?)
                for slot in player['equipments']:
                    if player['equipments'][slot] == equipmentsInput:
                        print(f"You remove your {player['equipments'][slot]} from your {slot} slot and put it in your inventory.")
                        player['inventory'].append(equipmentsInput)
                        player['equipments'][slot] = "empty"
                        

        if playerInput == "up":
            y -= 1

        elif playerInput == "left":
            x -= 1

        elif playerInput == "down":
            y += 1

        elif playerInput == "right":
            x += 1

        # HANDLE MAP EVENTS HERE
        if currentMap[y][x] == " ":
            if player['torch']['current'] > 5 :
                print("Your torch shines brightly, illuminating the room with its radiance.")
            elif player['torch']['current'] > 0:
                print("Your torch reveals the room as it flickers and wavers...")
            else:
                print("You grope your way into a dark room.")

        if currentMap[y][x] == "K":
            player['inventory'].append('dungeon key')
            print("\n")
            print("You found the Dungeon Key! You pick it up and place it in your inventory.")
            sleep(1)
            input("Press enter to continue")

        if currentMap[y][x] == "C":
            #returns random element from maploot
            lootType = choice(list(mapLoot))
            print(f"You found a {lootType}!")
            lootFound = False
            goldReceived = randint(mapLoot[lootType]['gold'][0],mapLoot[lootType]['gold'][1]) 
            player['gold'] += goldReceived
            print(f"You looted {goldReceived} gold from the {lootType}.")
            for loot in mapLoot[lootType]['possible loot']:
                if randint(0,100) < mapLoot[lootType]['possible loot'][loot]:
                    lootFound = True
                    player['inventory'].append(loot)
                    print(f"You found a {loot} from the {lootType}.")
            if lootFound == False:
                print(f"You found nothing else from the {lootType}. Bummer...")
            sleep(1)
            input("Press enter to continue")

        # 0 is a wall
        if currentMap[y][x] == "0":

            print("You bumped into a wall. Ouch!")
            #Reveals the wall that player hit (in case they lacked vision)
            playerMap[y][x] = currentMap[y][x]

            #Teleports player back to previous position due to them hitting the wall
            x = prevX
            y = prevY
            sleep(1)

        # E is an exit
        if currentMap[y][x] == "E":

            if "dungeon key" in player['inventory']:
                currentMap = updateMap(currentMap,x,y,prevX,prevY)
                printMap(currentMap)
                print(f"You reached the exit at turn {turn} and escaped from the Dungeon with {player['gold']} Gold! You win!")
                break
            else:
                #Reveals the exit that player hit (in case they lacked vision)
                playerMap[y][x] = currentMap[y][x]
                print("You reached the exit, but the door is locked...Find the key first!")
                x = prevX
                y = prevY

        # Starts encounter if tile is an NPC
        if currentMap[y][x] in nonPlayableCharacters:
            outcome = handleEncounter(player, nonPlayableCharacters[currentMap[y][x]])
            if outcome == "defeat":
                print("You were defeated by a denizen of the Dungeon. Game Over.")
                sleep(1)
                input("Press enter to leave the game.")
                break
            elif outcome == "retreated":
                #Reveals the character that player retreated from
                playerMap[y][x] = currentMap[y][x]
                x = prevX
                y = prevY
            elif outcome == "victory":
                print("You emerged victorious in combat!")
            print(f"You have {player['health']['current']} health left.")
            sleep(1)
            input("Press enter to continue")

        #Update map and player states below if turn is consumed
        if consumeTurn:
            turn += 1
            print("______________________________________")
            print(f"Turn {turn}:")
            print("______________________________________")
            currentMap = updateMap(currentMap,x,y,prevX,prevY)

            # Handles player's torch level
            if player['torch']['current'] > 0 :
                torchLit = True
                player['torch']['current'] -= 1
                if player['torch']['current'] == 0:
                    print("Your torch has ran out of fuel!")
            else: 
                torchLit = False

            playerMap = updateFog(playerMap,currentMap,x,y,prevX,prevY,torchLit)
            printMap(playerMap)

            # Descriptions below
            # Handles player's food level
            if player['food']['current'] > 0 :
                player['food']['current'] -= 1
                if player['food']['current'] < 10:
                    print("You are feeling hungry...")
            else: 
                print("You are starving!!!")
                player['health']['current'] -= 1
                if player['health']['current'] <= 0:
                    print("You starved to death...Game Over.")
                    break
        else:
            printMap(playerMap)

        # Describes current state and surroundings, regardless if turn is consumed
        if (0 < player['torch']['current'] < 6) and torchLit:
            print("Your torch is flickering...")
            
        if not torchLit:
            print("Darkness surrounds you...You can't see through the fog.")
            
        # Describes what player sees
        describeSurroundings(playerMap,x,y)
        print(f"Player position: x = {x}, y = {y}. Health: {player['health']['current']}/{player['health']['max']}. Food: {player['food']['current']}/{player['food']['max']}. Torch: {player['torch']['current']}/{player['torch']['max']}.")

            
# Starts Game. Takes in


main(testMap2)

