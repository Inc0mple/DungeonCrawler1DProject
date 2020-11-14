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
health, monsters and combat system (somewhat done)
inventory system
script writing and flavor texts

GOOD TO HAVE:
variable torch level (torch runs out of fuel = cannot reveal fog)
hunger
random events from chests/object interactions


IF GOT TIME:
more attributes and damage calculations
load/save system
powerups
status effects
experience/lvl up
multiple levels
scaling enemies
character classes
skills and abilities


COLIN TIER:
smart enemy behaviours
procedually generated maps
procedually generated item effects



player stats ideas:
attack, defence,speed,vision,dodge,accuracy
"""

import math
from random import randint
from copy import deepcopy

testMap = [
["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
["0", "P", " ", "G", "0", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", "0", " ", "0", " ", " ", "0"],
["0", " ", "S", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", "0", " ", " ", "0", " ", " ", " ", "0"],
["0", " ", "0", " ", " ", "0", " ", " ", " ", "0"],
["0", " ", "0", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", "0", "0", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", "S", " ", " ", " ", " ", "G", "E"],
["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
]

testMap2 = [
["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
["0", "P", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "E"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
]

"""
player stats ideas:
attack, defence,speed,vision,dodge,accuracy


"""
#
weapons = {
    "empty":(0,0),
    "dagger":(2,1),
    "short sword":(1,3),
    "spear":(1,5)
}

armor = {
    "empty":0,
    "leather armor":1,
    "chainmail":2,
    "plate armor":3
}

trinket = {

}

yourCharacterOrClass = {
    "name": "Prof. Zheng Kai",
    "health": 50,
    "attack": (4,6),
    "defence": 0,
    "speed": 1,
    "equipments": {
        "armor":"empty",
        "main hand":"empty",
        #"offHand":"empty",
        "trinket":"empty"
    },
    "status": [],
    "inventory": ["dagger","chainmail","short sword"],
    "gold": 0,
    "torch":10
}

nonPlayableCharacters = {
    "G": {
        "name": "Goblin",
        "health": 25,
        "attack": (1,6),
        "defence": 1,
        "speed": 2,
        "status": [],
        "inventory": [],
        "gold": 0,
        "intent": "hostile",
        "behaviour": "simple"
    },
    "S": {
        "name": "Slime",
        "health": 40,
        "attack": (1,3),
        "defence": 0,
        "speed": 0,
        "status": [],
        "inventory": [],
        "gold": 0,
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

# Used to determine enemy aictions
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

def handleEquip(inputCharacter, inputItem):
    inputCharacter["inventory"].remove(inputItem)
    
    # To implement choice of equipping in either main hand or off hand (perhaps)
    if inputItem in weapons:
        if inputCharacter["equipments"]["main hand"] != "empty":
            inputCharacter["inventory"].append(inputCharacter["equipments"]["main hand"])
            print(f"You remove your {inputCharacter['equipments']['main hand']} and put it in your inventory.")
        inputCharacter["equipments"]["main hand"] = inputItem
        print(f"You equipped your {inputItem} in your Main Hand slot")
    if inputItem in armor:
        if inputCharacter["equipments"]["armor"] != "empty":
            inputCharacter["inventory"].append(inputCharacter["equipments"]["armor"])
            print(f"You remove your {inputCharacter['equipments']['armor']} and put it in your inventory.")
        inputCharacter["equipments"]["armor"] = inputItem
        print(f"You equipped your {inputItem} in your Armor slot")
    if inputItem in trinket:
        if inputCharacter["equipments"]["trinket"] != "empty":
            inputCharacter["inventory"].append(inputCharacter["equipments"]["trinket"])
            print(f"You remove your {inputCharacter['equipments']['trinket']} and put it in your inventory.")
        inputCharacter["equipments"]["trinket"] = inputItem
        print(f"You equipped your {inputItem} in your Trinket slot")

def describeSurroundings(inputPlayerMap,x,y):

    objectDescriptions = {
        "0":"a solid wall",
        "G":"a hidious goblin",
        "S":"a glob of slime",
        "E":"a way out",
        ".":"nothing",
        " ":"an empty room"
    }
    north = inputPlayerMap[y-1][x]
    east = inputPlayerMap[y][x+1]
    south = inputPlayerMap[y+1][x]
    west = inputPlayerMap[y][x-1]

    if north in objectDescriptions:
        print(f"You see {objectDescriptions[north]} to your North.")
    else:
        print(f"You see an undocumented object '{north}' to your North.")
    if east in objectDescriptions:
        print(f"You see {objectDescriptions[east]} to your East.")
    else:
        print(f"You see an undocumented object '{east}' to your East.")
    if south in objectDescriptions:
        print(f"You see {objectDescriptions[south]} to your South.")
    else:
        print(f"You see an undocumented object '{south}' to your South.")
    if west in objectDescriptions:
        print(f"You see {objectDescriptions[west]} to your West.")
    else:
        print(f"You see an undocumented object '{west}' to your West.")
    
    

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
            print(f"{player['name']}\'s health: {player['health']}.")
            print(f"{enemy['name']}\'s health: {enemy['health']}.")

            combatControls = {
                "A": "Attack",
                "W":"Wait",
                #"D": "Defend",
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
                # Calculates lower and upper bound of damage based on base attack + main weapon dmg ( + half of offhand Weapon dmg rounded down if its ever reimplemented)
                lowerBoundDamage = player['attack'][0] + weapons[player["equipments"]["main hand"]][0] # + math.floor(weapons[player["equipments"]["offHand"]][0]/2)
                upperBoundDamage = player['attack'][1] + weapons[player["equipments"]["main hand"]][1] # + math.floor(weapons[player["equipments"]["offHand"]][1]/2)
                damage = max(randint(lowerBoundDamage,upperBoundDamage) - (enemy['defence']),0)

                enemy['health'] -= damage
                print(f"You attacked the {enemy['name']} for {damage} damage!")

            if playerInput == "wait":
                print("You bide your time...")

            if playerInput == "run":
                chanceToRun = max(35 + 7 * (player['speed'] - enemy['speed']),10)
                print(f"({chanceToRun}%) You try to run...")
                if randint(0,100) < chanceToRun:
                    print("...and retreated succesfully!")
                    return "retreated"
                else:
                    print("...but you were unsuccessful...")

            if playerInput == "enemyInitiative":
                print(f"The enemy {enemy['name']} acted first!")

            # Handle combat-ending event
            if enemy['health'] <= 0:
                inCombat = False
                print(f"You slew the {enemy['name']}.")
                break

            # Enemy's turn
            enemyInput = enemyAction(enemy)
            enemyInitiative = False
            # Handle enemy inputs
            if enemyInput == "attack":
                # Calculate damage, hit, dodge etc?
                lowerBoundDamage = enemy['attack'][0]
                upperBoundDamage = enemy['attack'][1]
                damage = max(randint(lowerBoundDamage,upperBoundDamage) - (player['defence'] + armor[player["equipments"]["armor"]]),0)

                player['health'] -= damage
                print(f"The {enemy['name']} attacked you for {damage} damage!")

            # Handle combat-ending event
            if player['health'] <= 0:
                inCombat = False
                playerDefeat = True
                print(f"You were slain by the {enemy['name']}!")
                break

    return "defeat" if playerDefeat else "victory"

# Updates player-visible map. When vision is True, reveal 1 tile around player for each movement
def updateFog(inputPlayerMap, inputCurrentMap, inputX, inputY, inputPrevX, inputPrevY, vision=False):

    #Reveal player's current tile
    inputPlayerMap[inputY][inputX] = inputCurrentMap[inputY][inputX]

    #Replace tile player was previously on with an empty space
    inputPlayerMap[inputPrevY][inputPrevX] = inputCurrentMap[inputPrevY][inputPrevX]

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


def main(inputMap, inputCharacter):

    # INITIALISE MAP
    currentMap = inputMap
    playerMap = fogMap(currentMap)

    #Shows map to player at start of game
    printMap(playerMap)

    # INITIALISE PLAYER
    player = inputCharacter
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
        "Q": "Quit"
        }

    # INITIALISE POSITION
    x = 1
    y = 1
    # prevX = x
    # prevY = y

    while playerInput != "quit":
        prevX = x
        prevY = y
        consumeTurn = True
        #Prompt player for input
        playerInput = playerAction(mapControls)

        if playerInput == "quit":
            print("Game Over")
            break

        if playerInput == "map":
            consumeTurn = False
            printMap(playerMap)

        if playerInput == "inventory":
            consumeTurn = False
            inventoryControls = {'X':"Go Back"}
            for idx,item in enumerate(player['inventory']):
                inventoryControls[str(idx)] = item
            print("Select item to equip.")
            inventoryInput = playerAction(inventoryControls)
            if inventoryInput != "go back":
                handleEquip(player, inventoryInput)

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
            if player['torch'] > 0 :
                print("Your torch shines brightly, illuminating the room")
            else:
                print("You grope your way into a dark room")

        # 0 is a wall
        if currentMap[y][x] == "0":

            print("You bumped into a wall. Ouch!")
            #Reveals the wall that player hit (in case they lacked vision)
            playerMap[y][x] = currentMap[y][x]

            #Teleports player back to previous position due to them hitting the wall
            x = prevX
            y = prevY

        # E is an exit
        if currentMap[y][x] == "E":
            playerMap[y][x] = currentMap[y][x]
            printMap(playerMap)
            print("You reached the exit! You win!")
            break

        # Starts encounter if tile is an NPC
        if currentMap[y][x] in nonPlayableCharacters:
            outcome = handleEncounter(player, nonPlayableCharacters[currentMap[y][x]])
            if outcome == "defeat":
                "You were defeated. Game Over."
                break
            elif outcome == "retreated":
                x = prevX
                y = prevY
            elif outcome == "victory":
                print("You emerged victorious in combat!")


        #Update map and player states below if turn is consumed
        if consumeTurn:
            currentMap = updateMap(currentMap,x,y,prevX,prevY)

            # Handles player's torch level
            if player['torch'] > 0 :
                torchLit = True
                player['torch'] -= 1
                if player['torch'] == 0:
                    print("Your torch has ran out!")
            else: 
                print("Darkness surrounds you...")
                torchLit = False

            playerMap = updateFog(playerMap,currentMap,x,y,prevX,prevY,torchLit)

            
            #Describe what player sees
            describeSurroundings(playerMap,x,y)
            printMap(playerMap)
            # printMap(playerMap)
            print(f"Player position: x = {x}, y = {y}. Health: {player['health']} Torch level: {player['torch']}.")



# printMap(fogMap(testMap))

# Starts Game. Takes in
main(testMap, yourCharacterOrClass)

