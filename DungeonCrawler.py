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
from colorama import Fore, Style
from random import randint
from random import choice
from copy import deepcopy
from time import sleep
from mapLoot import mapLoot
from classes import classes
from maps import maps,testMap, testMap2, testMap3
from nonPlayableCharacters import nonPlayableCharacters
from items import weapons,armor,trinket,consumables



# use this function to print map in human-readable format
def printMap(map):
    print("_"*(len(map[0])-2)+"Map:"+"_"*(len(map[0])-2))
    #print("_"*2*len(map[0]))
    for row in map:
        print(' '.join(row))
    print("_"*2*len(map[0]))


# Use this whenever you want player input.
def playerAction(availableActions):
    # Takes in a dictionary with key/value pair corresponding with control/action
    # Input will be convereted to upperCase. Output will be lower case.
    print(f"Available actions: {availableActions}")
    # If player doesnt give valid action, continue the loop of prompting player
    while True:
        playerInput = input("Enter your action: ").upper()
        if playerInput not in availableActions:
            print(f"{playerInput} is an invalid action. Please try again.")
        else:
            break
    # Outputs an action in the form of a lowercase string
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


# Handles viewing of inventory items
def handleInventoryDescription(inputCharacter):
    print("\nUsable/Equippable items in your inventory:\n")
    message = ""
    for item in inputCharacter['inventory']:
        if item in weapons:
            message += f"Weapon: {Fore.CYAN}{item}{Style.RESET_ALL} ({Fore.GREEN}+{weapons[item][0]}-{weapons[item][1]}{Style.RESET_ALL} attack when equipped)\n"
        elif item in armor:
            message += f"Armor: {Fore.CYAN}{item}{Style.RESET_ALL} ({Fore.GREEN}+{armor[item]}{Style.RESET_ALL} defence when equipped)\n"
        elif item in consumables:
            message += f"Consumable: {Fore.YELLOW}{item}{Style.RESET_ALL} (restores {Fore.GREEN}{consumables[item]}{Style.RESET_ALL} when used)\n"
    print(message)

# Handles using of inventory items
def handleUse(inputCharacter, inputItem):
    # First removes the used item from the inventory
    inputCharacter["inventory"].remove(inputItem)
    # Possible optimisation with a for loop?
    # Check what type of item is used/equipped, with different behaviours for each.
    if inputItem in consumables:
        for effect in consumables[inputItem]:
            # Calculate difference between current and max to prevent over-restoration of stat.
            difference = inputCharacter[effect]["max"] - inputCharacter[effect]["current"]
            # Take the smaller number between effect of consumable and 
            amountRestored = min(consumables[inputItem][effect], difference)
            inputCharacter[effect]["current"] += amountRestored
            print(f"{Fore.GREEN}Restored {inputCharacter['name']}'s {effect} by {amountRestored}.{Style.RESET_ALL}")


    # To implement choice of equipping in either main hand or off hand (perhaps)
    # Check which slot equipment belongs. If current equipment slot not empty, remove current equipment first before replacing with new equipment
    elif inputItem in weapons:
        if inputCharacter["equipments"]["main hand"] != "empty":
            inputCharacter["inventory"].append(inputCharacter["equipments"]["main hand"])
            print(f"You remove your {inputCharacter['equipments']['main hand']} and put it in your inventory.")
        inputCharacter["equipments"]["main hand"] = inputItem
        print(f"You equipped your {inputItem} in your Main Hand slot ( + {weapons[inputItem][0]}-{weapons[inputItem][1]} attack ).")

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

def handleMerchant(inputPlayer):
    shopInput = ""
    #Sell price = buy price/5
    priceSheet = {
        "weapons": {
            "dagger":50,
            "gladius":85,
            "short sword":100,
            "sword":140,
            "spear":190,
            "longsword":275,
            "halberd":275
        },
        "armor": {
            "leather armor":70,
            "chainmail":140,
            "scale armor":210,
            "plate armor":280,
            "dragonscale armor":350

        },
        "consumables": {
            "small torch fuel":30,
            "small food ration":40,
            "small health potion":50,
            "torch fuel":65,
            "food ration":80,
            "health potion":90,
            "large torch fuel":100,
            "large food ration":150,
            "large health potion":190
        }

    }
    print(f"{Fore.CYAN}Merchant: Welcome to my shop! Which category would you like to browse?{Style.RESET_ALL}")
    while shopInput != "leave":
        
        shopControls = {"1":"Weapons","2":"Armor","3":"Consumables","4":"Sell","X":"Leave"}
        print(f"Gold: {inputPlayer['gold']}")
        shopInput = playerAction(shopControls)
        if shopInput == "leave":
            print(f"{Fore.CYAN}Merchant: Thanks for your patronage, please come again!{Style.RESET_ALL}")
            break
        elif shopInput != "sell":
            print(f"\n{Fore.CYAN}Merchant: What would you like to buy?{Style.RESET_ALL}")
            buyControls = {"X": "Go Back"}
            print("_____________________________________________________________________________________")
            for idx,item in enumerate(priceSheet[shopInput], start = 1):
                buyControls[str(idx)] = str(item)
                # Eval() converts a string like "weapons" to the variable weapons
                costPrice = priceSheet[shopInput][item]
                print(f"{item.capitalize()}: {Fore.GREEN}+{eval(shopInput)[item]}.{Style.RESET_ALL} {Fore.YELLOW}Cost Price: {costPrice} Gold.{Style.RESET_ALL}")
            print("_____________________________________________________________________________________")
            buyInput = playerAction(buyControls)
            if buyInput != "go back":
                if inputPlayer['gold'] >= priceSheet[shopInput][buyInput]:
                    print(f"You bought {buyInput} for {priceSheet[shopInput][buyInput]} Gold!")
                    inputPlayer['gold'] -= priceSheet[shopInput][buyInput]
                    inputPlayer['inventory'].append(buyInput)
                else:
                    print(f"{Fore.RED}You need {priceSheet[shopInput][buyInput] - inputPlayer['gold']} more Gold to buy the {buyInput}!{Style.RESET_ALL}")
        else:
            print(f"What would you like to sell?")
            sellControls = {"X": "Go Back"}
            print("_____________________________________________________________________________________")
            for idx,item in enumerate(list(inputPlayer['inventory']), start = 1):
                sellControls[str(idx)] = str(item)
                if item in weapons:
                    sellPrice = math.floor(priceSheet["weapons"][item]/5)
                    print(f"{item.capitalize()}: {Fore.GREEN}{weapons[item]}.{Style.RESET_ALL} {Fore.YELLOW}Sell Price: {sellPrice} Gold.{Style.RESET_ALL}")
                elif item in armor:
                    sellPrice = math.floor(priceSheet["armor"][item]/5)
                    print(f"{item.capitalize()}: {Fore.GREEN}{armor[item]}.{Style.RESET_ALL} {Fore.YELLOW}Sell Price: {sellPrice} Gold.{Style.RESET_ALL}")
                elif item in consumables:
                    sellPrice = math.floor(priceSheet["consumables"][item]/5)
                    print(f"{item.capitalize()}: {Fore.GREEN}{consumables[item]}.{Style.RESET_ALL} {Fore.YELLOW}Sell Price: {sellPrice} Gold.{Style.RESET_ALL}")
                else:
                    print(f"{item.capitalize()}: {Fore.RED}This item can't be sold.{Style.RESET_ALL}")
            print("_____________________________________________________________________________________")
            sellInput = playerAction(sellControls)
            if sellInput in weapons:
                soldItemType = "weapons"
            elif sellInput in armor:
                soldItemType = "armor"
            elif sellInput in consumables:
                soldItemType = "consumables"
            else:
                soldItemType = "unsellable"
            if sellInput != "go back":
                if soldItemType != "unsellable":
                    print(f"{Fore.GREEN}You sold {sellInput} for {math.floor(priceSheet[soldItemType][sellInput]/5)} Gold!{Style.RESET_ALL}")
                    inputPlayer['gold'] += math.floor(priceSheet[soldItemType][sellInput]/5)
                    inputPlayer['inventory'].remove(sellInput)
                else:
                    print(f"{Fore.CYAN}Merchant. Sorry, I don't accept this item.{Style.RESET_ALL}")

def describeSurroundings(inputPlayerMap,x,y):
    # Add object descriptions
    objectDescriptions = {
        "0":f"a solid wall",
        "G":f"{Fore.YELLOW}a hideous goblin{Style.RESET_ALL}",
        "H":f"{Fore.YELLOW}a brawny hobgoblin{Style.RESET_ALL}",
        "D":f"{Fore.YELLOW}an agile dire wolf{Style.RESET_ALL}",
        "S":f"{Fore.YELLOW}a glob of slime{Style.RESET_ALL}",
        "R":f"{Fore.RED}the dungeon boss, a dangerous undead revenant,{Style.RESET_ALL}",
        "E":f"{Fore.GREEN}the exit{Style.RESET_ALL}",
        ".":f"nothing",
        "K":f"{Fore.GREEN}the dungeon key{Style.RESET_ALL}",
        "C":f"{Fore.CYAN}some dungeon loot{Style.RESET_ALL}",
        "M":f"{Fore.CYAN}a merchant{Style.RESET_ALL}",
        " ":f"an empty room"
    }
    northObject = inputPlayerMap[y-1][x]
    eastObject = inputPlayerMap[y][x+1]
    southObject = inputPlayerMap[y+1][x]
    westObject = inputPlayerMap[y][x-1]

    # Possible optimisation with a for loop?
    
    if northObject in objectDescriptions:
        print(f"You see {objectDescriptions[northObject]} to your North.")
    else: #Handles unknown object
        print(f"You see an undocumented/unknown object '{northObject}' to your North.")

    if eastObject in objectDescriptions:
        print(f"You see {objectDescriptions[eastObject]} to your East.")
    else:
        print(f"You see an undocumented/unknown object '{eastObject}' to your East.")

    if southObject in objectDescriptions:
        print(f"You see {objectDescriptions[southObject]} to your South.")
    else:
        print(f"You see an undocumented/unknown object '{southObject}' to your South.")

    if westObject in objectDescriptions:
        print(f"You see {objectDescriptions[westObject]} to your West.")
    else:
        print(f"You see an undocumented/unknown object '{westObject}' to your West.")

    

#Future update may include handling encounters with neutral or friendly characters that you can interact with.
def handleEncounter(inputCharacter, inputNPC):
    player = inputCharacter
    print(
        f"{Fore.YELLOW}{player['name']} has encountered a {inputNPC['intent']} {inputNPC['name']}!{Style.RESET_ALL}")

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
                f"{player['name']}\'s health: {Fore.RED if player['health']['current'] < 15 else Fore.WHITE}{player['health']['current']}/{player['health']['max']}{Style.RESET_ALL}\n"
                f"{enemy['name']}\'s health: {Fore.RED if enemy['health']['current'] < 10 else Fore.WHITE}{enemy['health']['current']}/{enemy['health']['max']}{Style.RESET_ALL}\n"
                f"{player['name']}\'s chance to hit: {max(math.floor(((player['accuracy'] - enemy['dodge'])/player['accuracy'])*100) + (player['speed'] - enemy['speed']),10)}%\n"
                f"{player['name']}\'s chance to dodge: {100 - max(math.floor(((enemy['accuracy'] - player['dodge'])/enemy['accuracy'])*100) + (enemy['speed'] - player['speed']),5)}%\n"
                f"{player['name']}\'s damage: {player['attack'][0] + weapons[player['equipments']['main hand']][0]} - {player['attack'][1] + weapons[player['equipments']['main hand']][1]}\n"
                f"{player['name']}\'s defence: {player['defence'] + armor[player['equipments']['armor']]}\n"

            )
            print("______________________________________")
            print(combatLog)
            print("______________________________________")
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
                print("______________________________________")
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
                    print(f"{Fore.CYAN}You hit the {enemy['name']} for {damage} damage!{Style.RESET_ALL}")
                
                else:
                    print(f"{Fore.RED}You missed!{Style.RESET_ALL}")
                    

            # This is a dumb move now, but maybe can be made useful in the future
            if playerInput == "wait":
                print("You bide your time...")

            if playerInput == "run":
                # minimum chance to run away is 10%
                chanceToRun = max(math.floor((player['speed']/enemy['speed'])*100),10)
                print(f"({chanceToRun}%) You try to run...")
                if randint(0,100) < chanceToRun:
                    print(f"{Fore.GREEN}...and retreated succesfully!{Style.RESET_ALL}")
                    return "retreated"
                else:
                    print(f"{Fore.RED}...but you were unsuccessful...{Style.RESET_ALL}")

            # Print description of your character
            if playerInput == "character":
                consumeTurn = False
                print("______________________________________")
                for info in player:
                    print(f"{Fore.CYAN}{str(info).capitalize()}: {str(player[info]).capitalize()}{Style.RESET_ALL}")
                print("______________________________________")
                input("Press enter to continue...")

            # Print description of your enemy
            if playerInput == "describe":
                consumeTurn = False
                print("______________________________________")
                for info in enemy:
                    print(f"{Fore.CYAN}{str(info).capitalize()}: {str(enemy[info]).capitalize()}{Style.RESET_ALL}")
                print("______________________________________")
                input("Press enter to continue...")

            if playerInput == "inventory":
                consumeTurn = False
                handleInventoryDescription(player)
                inventoryControls = {'X':"Go Back"}
                for idx,item in enumerate(player['inventory'], start = 1):
                    inventoryControls[str(idx)] = item
                print("Select item to equip/consume:")
                inventoryInput = playerAction(inventoryControls)
                if inventoryInput != "go back":
                    #Consumes a turn in combat if player decides to use/equip an item
                    consumeTurn = True
                    handleUse(player, inventoryInput)

            if playerInput == "equipment":
                consumeTurn = False
                equipmentsControls = {'X':"Go Back"}
                for idx,slot in enumerate(player['equipments'], start = 1):
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
                print(f"{Fore.GREEN}You slew the {enemy['name']}!{Style.RESET_ALL}")
                for loot in enemy['possible loot']:
                    if randint(0,100) < enemy['possible loot'][loot]:
                        player['inventory'].append(loot)
                        print(f"{Fore.CYAN}You take the {loot} from the dead {enemy['name']}.{Style.RESET_ALL}")
                goldReceived = randint(enemy['gold'][0],enemy['gold'][1]) 
                player['gold'] += goldReceived
                print(f"{Fore.WHITE}You received {goldReceived} gold from the dead {enemy['name']}.{Style.RESET_ALL}")
                break

            #Informs player that enemy acted first due to them having higher speed
            if playerInput == "enemyInitiative":
                print(f"{Fore.YELLOW}The enemy {enemy['name']} acted first!{Style.RESET_ALL}")

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
                        print(f"{Fore.YELLOW if damage > 0 else Fore.CYAN}The {enemy['name']} hits you for {damage} damage!{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.GREEN}You dodged the {enemy['name']}'s attack!{Style.RESET_ALL}")
            
            # Handle combat-ending event
            if player['health']['current'] <= 0:
                inCombat = False
                playerDefeat = True
                print(f"{Fore.RED}You were slain by the {enemy['name']}!{Style.RESET_ALL}")
                break

    return "defeat" if playerDefeat else "victory"

# Updates player-visible map. When vision is  2, reveal 1 tile around player for each movement
# When vision is 1, reveal only 1 tile north, south, east and west of player
# Requires player map, current map, current position, previous position and a vision level
def updateFog(inputPlayerMap, inputCurrentMap, inputX, inputY, inputPrevX, inputPrevY, vision=0):

    # Replace tile player was previously on with an empty space
    inputPlayerMap[inputPrevY][inputPrevX] = inputCurrentMap[inputPrevY][inputPrevX]
    
    # Reveal player's current tile
    inputPlayerMap[inputY][inputX] = inputCurrentMap[inputY][inputX]
    # When vision > 1 , reveal 8 surrounding tiles around player for each movement
    if vision > 1:
        inputPlayerMap[inputY+1][inputX+1] = inputCurrentMap[inputY+1][inputX+1]
        inputPlayerMap[inputY-1][inputX-1] = inputCurrentMap[inputY-1][inputX-1]
        inputPlayerMap[inputY-1][inputX+1] = inputCurrentMap[inputY-1][inputX+1]
        inputPlayerMap[inputY+1][inputX-1] = inputCurrentMap[inputY+1][inputX-1]
    # When vision = 1 , reveal 4 surrounding tiles around player for each movement   
    if vision > 0:
        # Reveals surounding tiles by setting those tiles in player map to be equal to the actual map
        inputPlayerMap[inputY+1][inputX] = inputCurrentMap[inputY+1][inputX]
        inputPlayerMap[inputY-1][inputX] = inputCurrentMap[inputY-1][inputX]
        inputPlayerMap[inputY][inputX+1] = inputCurrentMap[inputY][inputX+1]
        inputPlayerMap[inputY][inputX-1] = inputCurrentMap[inputY][inputX-1]
        

    # returns updated map
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
def main():

    # NAME SELECT
    welcomeText = """
    _______________________________________________________________________________________

    Welcome! The goal is to escape the Dungeon by finding the key to unlock the exit
    in the least amount of turns while looting as much gold as possible!

    Howver, the dungeon is foggy, and despite having a torch, you can only reveal a small area
    around you. There will be monsters and loot scattered across the play area.

    Pay close attention to your health, food and torch level as you traverse the Dungeon.

    Find loot on the map and slay enemies to recieve gold, supplies and equipments.
    Also look out for Merchants to buy and sell items.
    _______________________________________________________________________________________
    
    """
    print(welcomeText)
    input("Press enter to continue...")

    """
    tutorialInput =  playerAction({"0":"No","1":"Yes"})
    if tutorialInput.lower() == "yes" :
        # tutorial goes here
        print("Too bad the tutorial isn't done yet. Pick it up as you go along.")
        sleep(1)
    else:
        print("Great! lets go!")
    """ 
    
    print("_____________________________________________________________________________________")
    playerName = input("Please enter a name for your character: ")

    # INITIALISE MAP
    mapSelectControls = {}
    for idx,mapChoice in enumerate(maps, start = 1):    
        mapSelectControls[str(idx)] = mapChoice
    print("_____________________________________________________________________________________")
    print("Please select a map by entering the corresponding digits: ")
    selectedMap = playerAction(mapSelectControls)
    currentMap = maps[selectedMap]
    # Go back functionality not yet implemented
    if currentMap != "go back":
        print(f"map selected: {selectedMap}!")

    playerMap = fogMap(currentMap)

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
    for idx,classChoice in enumerate(classes,start = 1):    
        classesControls[str(idx)] = classChoice
    print("Please select a character class by entering the corresponding digit: ")
    classesInput = playerAction(classesControls)
    # Go back functionality not yet implemented
    if classesInput != "go back":
        classes[classesInput]['name'] = playerName
        print(f"Class selected: {classesInput}!")
        print(f"{Fore.GREEN}_____________________________________________________________________________________")
        for info in classes[classesInput]:
            print(f"{str(info).capitalize()}: {str(classes[classesInput][info]).capitalize()}")
        print(f"_____________________________________________________________________________________{Style.RESET_ALL}")
        classSelected = True
        player = classes[classesInput]
    sleep(1)

    # To give player chance to read the stats
    input("Press enter to continue...")
    
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
    playerMap = updateFog(playerMap,currentMap,x,y,prevX,prevY,2)
    printMap(playerMap)
    print("_____________________________________________________________________________________")
    print("""
    See that "P" on the map? That represents you, the Player.
    "0" represents impassable walls while "." represents unrevealed terrain.

    Commands inputted are case insensitive.
    Input WASD and enter to move in the corresponding directions.
    Useful information will be shown below the map as your character moves.

    Enter "M", "I", "E" and "C" to check your Map, Inventory, Equipment and Character respectively.
    Remember to use/equip items in your inventory to restore your vitals.
    Always check your available actions to see what you can do.
    Controls are different for different events (Map, Combat, Shop etc.)

    Hint: 
    Try to be efficient with your movements to prevent wasting resources (Torch and Food).
    Low torch levels impedes vision while low food levels prevents regeneration and leads to starvation.
    You can always run away from a tough battle and regenerate your health.
    
    Try entering one of the available actions below to proceed. Good luck!
    """)
    print("_____________________________________________________________________________________")
    while playerInput != "quit":
        prevX = x
        prevY = y

        # Whichever action that doesnt consume a turn should set this as false
        consumeTurn = True

        #Prompt player for input
        playerInput = playerAction(mapControls)

        if playerInput == "quit":
            print(f"{Fore.RED}You succumbed to the dangers of the Dungeon...Game Over.{Style.RESET_ALL}")
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
            input("Press enter to continue...")

        if playerInput == "inventory":
            consumeTurn = False
            handleInventoryDescription(player)
            inventoryControls = {'X':"Go Back"}
            for idx,item in enumerate(player['inventory'],start = 1):
                inventoryControls[str(idx)] = item
            print("Select item to equip/consume.")
            inventoryInput = playerAction(inventoryControls)
            if player['torch']['current'] >= 10:
                torchLit = 2
            elif 1 < player['torch']['current'] < 10: 
                torchLit = 1
            else:
                torchLit = 0
            if inventoryInput != "go back":
                handleUse(player, inventoryInput)
                playerMap = updateFog(playerMap,currentMap,x,y,prevX,prevY,torchLit)
                input("Press enter to continue...")

        if playerInput == "equipment":
            consumeTurn = False
            equipmentsControls = {'X':"Go Back"}
            for idx,slot in enumerate(player['equipments'],start = 1):
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
        message = ""
        if currentMap[y][x] == " ":
            if player['torch']['current'] >= 10 :
                message += (f"{Fore.GREEN}Your torch shines brightly, illuminating the room with its radiance.{Style.RESET_ALL}")
            elif player['torch']['current'] > 0:
                message += (f"{Fore.YELLOW}Your torch reveals the room as it flickers and wavers...{Style.RESET_ALL}")
            else:
                message += (f"{Fore.RED}You grope your way into a dark room.{Style.RESET_ALL}")

        if currentMap[y][x] == "K":
            player['inventory'].append('dungeon key')
            print("\n")
            print(f"{Fore.GREEN}You found the Dungeon Key! You pick it up and place it in your inventory.{Style.RESET_ALL}")
            sleep(1)
            input("Press enter to continue...")

        if currentMap[y][x] == "C":
            #returns random element from maploot
            lootType = choice(list(mapLoot))
            print(f"{Fore.CYAN}You found a {lootType}!{Style.RESET_ALL}")
            lootFound = False
            goldReceived = randint(mapLoot[lootType]['gold'][0],mapLoot[lootType]['gold'][1]) 
            player['gold'] += goldReceived
            print(f"{Fore.WHITE}You looted {goldReceived} gold from the {lootType}.{Style.RESET_ALL}")
            for loot in mapLoot[lootType]['possible loot']:
                if randint(0,100) < mapLoot[lootType]['possible loot'][loot]:
                    lootFound = True
                    player['inventory'].append(loot)
                    print(f"{Fore.GREEN}You take the {loot} from the {lootType}.{Style.RESET_ALL}")
            if lootFound == False:
                print(f"{Fore.YELLOW}You found nothing else from the {lootType}. Bummer...{Style.RESET_ALL}")
            sleep(1)
            input("Press enter to continue...")

        # 0 is a wall
        if currentMap[y][x] == "0":

            print(f"{Fore.YELLOW}You bumped into a wall. Ouch!{Style.RESET_ALL}")
            #Reveals the wall that player hit (in case they lacked vision)
            playerMap[y][x] = currentMap[y][x]

            #Teleports player back to previous position due to them hitting the wall
            x = prevX
            y = prevY
            sleep(1)

        if currentMap[y][x] == "M":

            print(f"{Fore.CYAN}You meet the Merchant and start trading!{Style.RESET_ALL}")
            #Reveals the wall that player hit (in case they lacked vision)
            playerMap[y][x] = currentMap[y][x]
            handleMerchant(player)

            #Teleports player back to previous position
            x = prevX
            y = prevY
            sleep(1)

        # E is an exit
        if currentMap[y][x] == "E":

            if "dungeon key" in player['inventory']:
                currentMap = updateMap(currentMap,x,y,prevX,prevY)
                printMap(currentMap)
                print(f"{Fore.GREEN}You reached the exit at turn {turn} and escaped from the Dungeon with {player['gold']} Gold! You win!{Style.RESET_ALL}")
                print(f"{Fore.CYAN}Your score: {1000-turn+player['gold']}{Style.RESET_ALL}")
                break
            else:
                #Reveals the exit that player hit (in case they lacked vision)
                playerMap[y][x] = currentMap[y][x]
                print(f"{Fore.YELLOW}You reached the exit, but the door is locked...Find the key first!{Style.RESET_ALL}")
                x = prevX
                y = prevY

        # Starts encounter if tile is an NPC
        if currentMap[y][x] in nonPlayableCharacters:
            outcome = handleEncounter(player, nonPlayableCharacters[currentMap[y][x]])
            if outcome == "defeat":
                print(f"{Fore.RED}You were defeated by a denizen of the Dungeon. Game Over.{Style.RESET_ALL}")
                sleep(1)
                input("Press enter to leave the game.")
                break
            elif outcome == "retreated":
                #Reveals the character that player retreated from
                playerMap[y][x] = currentMap[y][x]
                x = prevX
                y = prevY
            elif outcome == "victory":
                print(f"{Fore.GREEN}You emerged victorious in combat!{Style.RESET_ALL}")
            print(f"You have {player['health']['current']} health left.")
            sleep(1)
            input("Press enter to continue...")

        #Update map and player states below if turn is consumed
        if consumeTurn:
            turn += 1
            print("______________________________________")
            print(f"Turn {turn}:")
            print("______________________________________\n")
            currentMap = updateMap(currentMap,x,y,prevX,prevY)

            # Handles player's torch level
            if player['torch']['current'] >= 10 :
                torchLit = 2
                player['torch']['current'] -= 1
                if player['torch']['current'] == 0:
                    print(f"{Fore.RED}Your torch has ran out of fuel!{Style.RESET_ALL}")
            elif 0 < player['torch']['current'] < 10: 
                torchLit = 1
                player['torch']['current'] -= 1
            else:
                torchLit = 0

            playerMap = updateFog(playerMap,currentMap,x,y,prevX,prevY,torchLit)
            printMap(playerMap)

            # Descriptions below
            # Handles player's food level
            if player['food']['current'] > 0 :
                player['food']['current'] -= 1
                if player['food']['current'] >= 10 and player['health']['current'] < player['health']['max']:
                    player['health']['current'] += 1
                    print(f"{Fore.GREEN}Regenerated 1 health from being satiated{Style.RESET_ALL}.")
                elif player['food']['current'] < 10:
                    print(f"{Fore.YELLOW}You are feeling hungry...no longer regenerating health...{Style.RESET_ALL}")
            else: 
                print(f"{Fore.RED}You are starving!!!{Style.RESET_ALL}")
                player['health']['current'] -= 1
                if player['health']['current'] <= 0:
                    print(f"{Fore.RED}You starved to death...Game Over.{Style.RESET_ALL}")
                    break
        else:
            printMap(playerMap)

        # Describes current state and surroundings, regardless if turn is consumed
        if (0 < player['torch']['current'] < 10) and torchLit > 0:
            print(f"{Fore.YELLOW}Your torch is flickering...you can't see as far as before...{Style.RESET_ALL}")
        
        if torchLit == 0:
            print(f"{Fore.RED}Darkness surrounds you...You can't see through the fog.{Style.RESET_ALL}")

        if player['health']['current'] < 15:
            print(f"{Fore.RED}You feel weak...Find some way to restore your health!{Style.RESET_ALL}")
            
        
        # Describes what player sees
        describeSurroundings(playerMap,x,y)
        print(message)

        print("")
        print(f"{Fore.YELLOW if player['health']['current'] < 15 else Fore.WHITE}   Health:{Style.RESET_ALL}{player['health']['current']}/{player['health']['max']}.")
        print(f"{Fore.YELLOW if player['food']['current'] < 10 else Fore.WHITE}   Food:{Style.RESET_ALL}{player['food']['current']}/{player['food']['max']}.")
        print(f"{Fore.YELLOW if player['torch']['current'] < 10 else Fore.WHITE}   Torch:{Style.RESET_ALL}{player['torch']['current']}/{player['torch']['max']}.")
        print(f"   Gold: {player['gold']}. ")
        print("_____________________________________________________________________________________")
            
# Starts Game. Takes in


main()

