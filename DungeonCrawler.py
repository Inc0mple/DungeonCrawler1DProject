"""
F04 Group 2: Bryan Tan, Ryan Kaw Zheng Da, Colin Teoh, Xu Muzi, Joseph Lai
"""
# Python modules
import math
from colorama import Fore, Style
from random import randint, choice
from copy import deepcopy, copy
from time import sleep

# Custom modules
from mapLoot import mapLoot
from classes import classes
from maps import maps
from nonPlayableCharacters import nonPlayableCharacters
from items import weapon,armor,trinket,consumables,priceSheet
from statusSkill import *

# use this function to print map in human-readable format
def printMap(map):
    #Prints line surrounding map headings
    print("_"*(len(map[0])-2)+"Map:"+"_"*(len(map[0])-2))
    for row in map:
        print(' '.join(row))
    print("_"*2*len(map[0]))

# Use this whenever you want player input.
def playerAction(availableActions):
    # Takes in a dictionary with key/value pair corresponding with control/action
    # Input will be convereted to upperCase. Output will be lower case.
    availableActionsList = [(key,val) for key,val in availableActions.items()]
    # The tup in the code below stands for tuple (But i cant use tuple cause its already part of python)
    print(f"Available actions: {Fore.GREEN}{' '.join(f'[{tup[0]}: {tup[1].capitalize()}]' for tup in availableActionsList)}{Style.RESET_ALL}")
    # If player doesnt give valid action, continue the loop of prompting player
    while True:
        playerInput = input("Enter your action: ").upper()
        if playerInput not in availableActions:
            print(f"{playerInput} is an {Fore.RED}invalid action{Style.RESET_ALL}. Please try again.")
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
    inputMap[inputY][inputX] = f"{Fore.GREEN}P{Style.RESET_ALL}"
    return inputMap

# Handles viewing of inventory items
def handleInventoryDescription(inputCharacter):
    print("\nUsable/Equippable items in your inventory:\n")
    message = ""
    for item in inputCharacter['inventory']:
        if item in weapon:
            message += f"Weapon: {Fore.CYAN}{item}{Style.RESET_ALL} ({Fore.GREEN}+{weapon[item][0]}-{weapon[item][1]}{Style.RESET_ALL} attack when equipped)\n"
        elif item in armor:
            message += f"Armor: {Fore.CYAN}{item}{Style.RESET_ALL} ({Fore.GREEN}+{armor[item]}{Style.RESET_ALL} defence when equipped)\n"
        elif item in trinket:
            message += f"Trinket: {Fore.CYAN}{item}{Style.RESET_ALL} ({Fore.YELLOW} {trinket[item]}{Style.RESET_ALL} stat modifier when equipped)\n"
        elif item in consumables:
            message += f"Consumable: {Fore.YELLOW}{item}{Style.RESET_ALL} (restores {Fore.GREEN}{consumables[item]}{Style.RESET_ALL} when used)\n"
    print(message)

# Prints out player skill in readable format
def handleSkillDescription(inputCharacter):
    print("\nSkills in your skillset:\n")
    message = ""
    for skillKey in inputCharacter['skills']:
        message += f"{Fore.GREEN}{skillKey.capitalize()}{Style.RESET_ALL}: {skills[skillKey]['description']}\n"
        message += f"\t{Fore.YELLOW}Power{Style.RESET_ALL}: {inputCharacter['skills'][skillKey]['magnitude']}\n"
        message += f"\t{Fore.YELLOW}Duration{Style.RESET_ALL}: {inputCharacter['skills'][skillKey]['duration']}\n"
        message += f"\t{Fore.YELLOW}Cooldown{Style.RESET_ALL}: {inputCharacter['skills'][skillKey]['cooldown']}\n"
        message += f"\t{Fore.YELLOW}Turns till ready{Style.RESET_ALL}: {inputCharacter['skills'][skillKey]['turnsTillReady']}\n"
    print(message)

# Invokes input skill's function on target character, make caster skill go on CD
def handleSkill(castedSkill,casterCharacter,targetCharacter):
    skills[castedSkill]['function'](casterCharacter,targetCharacter,casterCharacter['skills'][castedSkill]['duration'],casterCharacter['skills'][castedSkill]['magnitude'])
    casterCharacter['skills'][castedSkill]["turnsTillReady"] = casterCharacter['skills'][castedSkill]['cooldown']

# Handles using of inventory items
def handleUse(inputCharacter, inputItem):
    # First removes the used item from the inventory
    inputCharacter["inventory"].remove(inputItem)
    # Check what type of item is used/equipped, with different behaviours for each.
    if inputItem in consumables:
        for effect in consumables[inputItem]:
            # Calculate difference between current and max to prevent over-restoration of stat.
            difference = inputCharacter[effect]["max"] - inputCharacter[effect]["current"]
            # Take the smaller number between restorative effect of consumable and amount that CAN be restored
            amountRestored = min(consumables[inputItem][effect], difference)
            inputCharacter[effect]["current"] += amountRestored
            print(f"{Fore.GREEN}Restored {inputCharacter['name']}'s {effect} by {amountRestored}.{Style.RESET_ALL}")

    # Check which slot equipment belongs. If current equipment slot not empty, remove current equipment first before replacing with new equipment
    elif inputItem in weapon:
        if inputCharacter["equipments"]["weapon"] != "empty":
            inputCharacter["inventory"].append(inputCharacter["equipments"]["weapon"])
            print(f"You remove your {Fore.CYAN}{inputCharacter['equipments']['weapon']}{Style.RESET_ALL} and put it in your inventory.")
        inputCharacter["equipments"]["weapon"] = inputItem
        print(f"You equipped your {Fore.CYAN}{inputItem.capitalize()}{Style.RESET_ALL} in your {Fore.YELLOW}Weapon{Style.RESET_ALL} slot ( + {Fore.GREEN}{weapon[inputItem][0]}-{weapon[inputItem][1]}{Style.RESET_ALL} attack ).")

    elif inputItem in armor:
        if inputCharacter["equipments"]["armor"] != "empty":
            inputCharacter["inventory"].append(inputCharacter["equipments"]["armor"])
            print(f"You remove your {Fore.CYAN}{inputCharacter['equipments']['armor']}{Style.RESET_ALL} and put it in your inventory.")
        inputCharacter["equipments"]["armor"] = inputItem
        print(f"You equipped your {Fore.CYAN}{inputItem.capitalize()}{Style.RESET_ALL} in your {Fore.YELLOW}Armor{Style.RESET_ALL} slot ( + {Fore.GREEN}{armor[inputItem]}{Style.RESET_ALL} defence ).")

    elif inputItem in trinket:
        if inputCharacter["equipments"]["trinket"] != "empty":
            inputCharacter["inventory"].append(inputCharacter["equipments"]["trinket"])
            print(f"You remove your {Fore.CYAN}{inputCharacter['equipments']['trinket']}{Style.RESET_ALL} and put it in your inventory.")
        inputCharacter["equipments"]["trinket"] = inputItem
        print(f"You equipped your {Fore.CYAN}{inputItem.capitalize()}{Style.RESET_ALL} in your {Fore.YELLOW}Trinket{Style.RESET_ALL} slot  ({Fore.GREEN}{trinket[inputItem]}{Style.RESET_ALL} stat modifier)")
    
    # In case you use dungeon key
    else:
        print("You can't use that item!")
        inputCharacter["inventory"].append(inputItem)

def handleTurnStart(inputCharacter):
    #handle attack modifier calculations
    inputCharacter['attack']['current'][0] = max(0,inputCharacter['attack']['max'][0] + inputCharacter['attack']['modifier'][0])
    inputCharacter['attack']['current'][1] = max(0,inputCharacter['attack']['max'][1] + inputCharacter['attack']['modifier'][1])
    temporaryCombatStats = ['defence','speed','accuracy','dodge']
    #handle stat modifier calculations
    for stat in temporaryCombatStats:
        inputCharacter[stat]['current'] = max(0,inputCharacter[stat]['max'] + inputCharacter[stat]['modifier'])

#
def handleTurnEnd(inputCharacter):
    #reset attack modifier calculations
    inputCharacter['attack']['modifier'] = [0,0]
    inputCharacter['attack']['current'] = copy(inputCharacter['attack']['max'])

    #Reset stat modifiers
    temporaryCombatStats = ['defence','speed','accuracy','dodge']
    for stat in temporaryCombatStats:
        #reset modifier and current stat
        inputCharacter[stat]['modifier'] = 0
        inputCharacter[stat]['current'] = copy(inputCharacter[stat]['max'])
        
    expiredStatusList = []
    # We cannot delete keys in the dictionary that we are iterating on, hence the need to append expired statuses to list
    for key,val in inputCharacter['status'].items():
        #print(key,val)
        # Runs status effect functions on character's stats
        statusEffects[key](inputCharacter,inputCharacter['status'][key]['magnitude'])
        inputCharacter['status'][key]['duration'] -= 1
        if inputCharacter['status'][key]['duration'] <= 0:
            expiredStatusList.append((key,val))

    #handle removing of expired statuses
    for expiredStatusTuple in expiredStatusList:
        expiredEffectName = expiredStatusTuple[0]
        inputCharacter['status'].pop(expiredEffectName)
        print(f"{Fore.CYAN}{inputCharacter['name']}{Style.RESET_ALL} is no longer {Fore.YELLOW}{expiredEffectName}{Style.RESET_ALL}!")

    # handle skill cooldown
    for skill in inputCharacter['skills']:
        if inputCharacter['skills'][skill]["turnsTillReady"] > 0:
            inputCharacter['skills'][skill]["turnsTillReady"] -= 1

def handleMerchant(inputPlayer, startOfGame=False):
    shopInput = ""
    # Sell price = buy price/5
    # Interacts differently depending on whether it is the start of game or not
    if startOfGame:
        print(f"{Fore.CYAN}Merchant: Welcome to my shop! Before you embark, please consider buying some items from my shop!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Merchant: If you are a beginner, consider pressing 'B' to buy the recommended consumables!{Style.RESET_ALL}\n")
    else:
        print(f"{Fore.CYAN}Merchant: Hi there! Which category would you like to browse?{Style.RESET_ALL}")
    while shopInput != "leave":
        if startOfGame:
            shopControls = {"1":"Weapon","2":"Armor","3":"Trinket","4":"Consumables","5":"Sell","B":"Buy recommended consumables","X":"Leave"}
        else:
            shopControls = {"1":"Weapon","2":"Armor","3":"Trinket","4":"Consumables","5":"Sell","X":"Leave"}
        print(f"Gold: {inputPlayer['gold']}")
        shopInput = playerAction(shopControls)
        if shopInput == "leave":
            print(f"{Fore.CYAN}Merchant: Thanks for your patronage, good luck!{Style.RESET_ALL}")
            break
        elif shopInput == "buy recommended consumables":
            startOfGame == False
            # Put only consumables here
            recommendedStarter = ["small health potion","small torch fuel","small food ration"]
            for item in recommendedStarter:
                if inputPlayer['gold'] >= priceSheet['consumables'][item]:
                    print(f"You bought {Fore.CYAN}{item}{Style.RESET_ALL} for {Fore.YELLOW}{priceSheet['consumables'][item]}{Style.RESET_ALL} Gold!")
                    inputPlayer['gold'] -= priceSheet['consumables'][item]
                    inputPlayer['inventory'].append(item)
                else:
                    print(f"{Fore.RED}You need {priceSheet['consumables'][item] - inputPlayer['gold']} more Gold to buy the {item}!{Style.RESET_ALL}")

        elif shopInput != "sell":
            print(f"\n{Fore.CYAN}Merchant: What would you like to buy?{Style.RESET_ALL}")
            buyControls = {"X": "Go Back"}
            print("_____________________________________________________________________________________")
            for idx,item in enumerate(priceSheet[shopInput], start = 1):
                buyControls[str(idx)] = str(item)
                # Eval() converts a string like "weapon" to the weapon variable (which is a dict)
                # This is required here as shopInput is a string.
                costPrice = priceSheet[shopInput][item]
                print(f"{item.capitalize()}: {Fore.GREEN}+{eval(shopInput)[item]}.{Style.RESET_ALL} {Fore.YELLOW}Cost Price: {costPrice} Gold.{Style.RESET_ALL}")
            print("_____________________________________________________________________________________")
            buyInput = playerAction(buyControls)
            if buyInput != "go back":
                if inputPlayer['gold'] >= priceSheet[shopInput][buyInput]:
                    print(f"You bought {Fore.CYAN}{buyInput}{Style.RESET_ALL} for {Fore.YELLOW}{priceSheet[shopInput][buyInput]}{Style.RESET_ALL} Gold!")
                    inputPlayer['gold'] -= priceSheet[shopInput][buyInput]
                    inputPlayer['inventory'].append(buyInput)
                else:
                    print(f"{Fore.RED}You need {priceSheet[shopInput][buyInput] - inputPlayer['gold']} more Gold to buy the {buyInput}!{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}What would you like to sell?{Style.RESET_ALL}")
            sellControls = {"X": "Go Back"}
            print("_____________________________________________________________________________________")
            for idx,item in enumerate(list(inputPlayer['inventory']), start = 1):
                sellControls[str(idx)] = str(item)
                if item in weapon:
                    sellPrice = math.floor(priceSheet["weapon"][item]/5)
                    print(f"{item.capitalize()}: {Fore.GREEN}{weapon[item]}.{Style.RESET_ALL} {Fore.YELLOW}Sell Price: {sellPrice} Gold.{Style.RESET_ALL}")
                elif item in armor:
                    sellPrice = math.floor(priceSheet["armor"][item]/5)
                    print(f"{item.capitalize()}: {Fore.GREEN}{armor[item]}.{Style.RESET_ALL} {Fore.YELLOW}Sell Price: {sellPrice} Gold.{Style.RESET_ALL}")
                elif item in trinket:
                    sellPrice = math.floor(priceSheet["trinket"][item]/5)
                    print(f"{item.capitalize()}: {Fore.GREEN}{trinket[item]}.{Style.RESET_ALL} {Fore.YELLOW}Sell Price: {sellPrice} Gold.{Style.RESET_ALL}")
                elif item in consumables:
                    sellPrice = math.floor(priceSheet["consumables"][item]/5)
                    print(f"{item.capitalize()}: {Fore.GREEN}{consumables[item]}.{Style.RESET_ALL} {Fore.YELLOW}Sell Price: {sellPrice} Gold.{Style.RESET_ALL}")
                else:
                    print(f"{item.capitalize()}: {Fore.RED}This item can't be sold.{Style.RESET_ALL}")
            print("_____________________________________________________________________________________")
            sellInput = playerAction(sellControls)
            if sellInput in weapon:
                soldItemType = "weapon"
            elif sellInput in armor:
                soldItemType = "armor"
            elif sellInput in trinket:
                soldItemType = "trinket"
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
        "0":f"{Fore.YELLOW}a solid wall{Style.RESET_ALL}",
        "G":f"{Fore.RED}a hideous goblin{Style.RESET_ALL}",
        "H":f"{Fore.RED}a brawny hobgoblin{Style.RESET_ALL}",
        "D":f"{Fore.RED}an agile dire wolf{Style.RESET_ALL}",
        "S":f"{Fore.RED}a glob of slime{Style.RESET_ALL}",
        "R":f"{Fore.RED}the dungeon boss, a dangerous undead revenant,{Style.RESET_ALL}",
        "E":f"{Fore.GREEN}the exit{Style.RESET_ALL}",
        ".":f"{Fore.YELLOW}nothing{Style.RESET_ALL}",
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
        enemyInitiative = True if enemy['speed']['current'] > player['speed']['current'] else False

        #Reset skill cooldown before combat
        for skill in player['skills']:
            player['skills'][skill]['turnsTillReady'] = 0

        #Reset status effects of player
        player['status'] = {}

        #ANY player action that doesnt consume a turn should set this to false
        consumeTurn = True
        # We set consumeTrun to be true in first turn so that equipment modifiers are calulcated by the start of the first turn
        # Reset modifier by items
        handleTurnEnd(player)
        while inCombat:
            
            # Handles stat modifier from equipments if turn is consumed
            # These calculation are specific only to player characters
            # as only the player will equip items
            if consumeTurn:
                #Trinket modifier:
                playerTrinket = player["equipments"]["trinket"]
                for stat in trinket[playerTrinket]:
                    player[stat]["modifier"] += trinket[playerTrinket][stat]
                #Armor modifier:
                playerArmor = player["equipments"]["armor"]
                player['defence']["modifier"] += armor[playerArmor]
                #Weapon modifier:
                playerWeapon = player["equipments"]["weapon"]
                player['attack']["modifier"][0] += weapon[playerWeapon][0]
                player['attack']["modifier"][1] += weapon[playerWeapon][1]

                #These function calculates current stat from max stat + modifier
                handleTurnStart(player)
                handleTurnStart(enemy)
            message = ""
            combatLog =  (
                f"\n"
                f"{player['name']}\'s health: {Fore.RED if player['health']['current'] < 15 else Fore.WHITE}{player['health']['current']}/{player['health']['max']}{Style.RESET_ALL}\n"
                f"{enemy['name']}\'s health: {Fore.RED if enemy['health']['current'] < 10 else Fore.WHITE}{enemy['health']['current']}/{enemy['health']['max']}{Style.RESET_ALL}\n"
                f"{player['name']}\'s chance to hit: {max(math.floor(((player['accuracy']['current'] - enemy['dodge']['current'])/player['accuracy']['current'])*100) + (player['speed']['current'] - enemy['speed']['current']),5)}%\n"
                f"{player['name']}\'s chance to dodge: {100 - max(math.floor(((enemy['accuracy']['current'] - player['dodge']['current'])/enemy['accuracy']['current'])*100) + (enemy['speed']['current'] - player['speed']['current']),5)}%\n"
                f"{player['name']}\'s damage: {player['attack']['current'][0]} - {player['attack']['current'][1]}\n"
                f"{player['name']}\'s defence: {player['defence']['current']}\n"

            )
            print("______________________________________")
            print(combatLog)
            print("______________________________________")
            
            combatControls = {
                "A": "Attack",
                "W": "Wait", 
                "S": "Skill",
                "D": "Describe",
                "I": "Inventory",
                "C": "Character",
                "E": "Equipment",
                "R": "Run"
            }
            # Player's turn
            
            # Allow player input if enemy is not acting first, else enemy acts first
            if not enemyInitiative:
                playerInput = playerAction(combatControls)
                print("______________________________________")
            else:
                playerInput = "enemyInitiative"

            # Handle player inputs
            if playerInput == "attack":
                consumeTurn = True
                # Hit chance formula modified from https://www.gamedev.net/forums/topic/685930-the-simplest-but-most-effective-and-intuitive-way-to-implement-accuracy-and-dodge-chance-in-an-rpg/
                chanceToHit = max(math.floor(((player['accuracy']['current'] - enemy['dodge']['current'])/player['accuracy']['current'])*100) + (player['speed']['current'] - enemy['speed']['current']),5)
                print(f"\n({chanceToHit}%) You attempt to strike...")
                if randint(0,100) < chanceToHit:
                    # Calculates lower and upper bound of damage based on base attack + main weapon dmg 
                    
                    lowerBoundDamage = player['attack']['current'][0] 
                    upperBoundDamage = player['attack']['current'][1]

                    # max is to prevent negative damage from being dealt
                    damage = max(randint(lowerBoundDamage,upperBoundDamage) - (enemy['defence']['current']),0)
                    enemy['health']['current'] -= damage
                    print(f"{Fore.CYAN}You hit the {enemy['name']} for {damage} damage!{Style.RESET_ALL}")
                
                else:
                    print(f"{Fore.RED}You missed!{Style.RESET_ALL}")
                    
            # This is a dumb move now, mostly used for debugging, but its possible
            # that future updates can make this a viable strat
            if playerInput == "wait":
                consumeTurn = True
                print("You skipped your turn...")

            if playerInput == "run":
                consumeTurn = True
                # minimum chance to run away is 10%
                chanceToRun = max(math.floor((player['speed']['current']/enemy['speed']['current'])*100),10)
                print(f"({chanceToRun}%) You try to run...")
                if randint(0,100) < chanceToRun:
                    print(f"{Fore.GREEN}...and retreated succesfully!{Style.RESET_ALL}")
                    return "retreated"
                else:
                    print(f"{Fore.RED}...but you were unsuccessful...{Style.RESET_ALL}")

            # Print description of your character
            if playerInput == "character":
                consumeTurn = False
                print(f"{Fore.WHITE}_____________________________________________________________________________________")
                message = ""
                for info in player:
                    #print(type(player[info]), player[info])
                    if type(player[info]) is dict:
                        message += f"{Fore.GREEN}{str(info).capitalize()}{Style.RESET_ALL}: \n"
                        for nestedInfo in player[info]:
                            message += f"\t{Fore.YELLOW}{str(nestedInfo).capitalize()}{Style.RESET_ALL}:{player[info][nestedInfo]}\n"
                    else:
                        message += f"{Fore.GREEN}{str(info).capitalize()}{Style.RESET_ALL}: {str(player[info]).capitalize()}\n"
                print(message)
                print(f"_____________________________________________________________________________________{Style.RESET_ALL}")
                input("Press enter to continue...")

            # Print description of your enemy
            if playerInput == "describe":
                consumeTurn = False
                print(f"{Fore.WHITE}_____________________________________________________________________________________")
                message = ""
                for info in enemy:
                    #print(type(enemy[info]), enemy[info])
                    if type(enemy[info]) is dict:
                        message += f"{Fore.GREEN}{str(info).capitalize()}{Style.RESET_ALL}: \n"
                        for nestedInfo in enemy[info]:
                            message += f"\t{Fore.YELLOW}{str(nestedInfo).capitalize()}{Style.RESET_ALL}:{enemy[info][nestedInfo]}\n"
                    else:
                        message += f"{Fore.GREEN}{str(info).capitalize()}{Style.RESET_ALL}: {str(enemy[info]).capitalize()}\n"
                print(message)
                print(f"_____________________________________________________________________________________{Style.RESET_ALL}")
                input("Press enter to continue...")

            if playerInput == "inventory":
                consumeTurn = False
                #Print description of player inventory
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

            if playerInput == "skill":
                consumeTurn = False
                skillInput = ""
                # Prints available skills you can use in a nice format
                handleSkillDescription(player)
                skillControls = {'X':"Go Back"}
                # Adds skills to the control dictionary
                for idx,skill in enumerate(player['skills'], start = 1):
                    skillControls[str(idx)] = skill
                print("Select skill to use: \n")
                # Ask for player input on what skill to use
                skillInput = playerAction(skillControls)
                # If player selects go back, turn is not consumed.
                # If go back not selected and skill is ready, proceed with target selection
                if skillInput != "go back":
                    if player['skills'][skillInput]["turnsTillReady"] > 0:
                        print (f"Skill is not ready! {player['skills'][skillInput]['turnsTillReady']} more turns needed!")
                    else:
                        targetControls = {'1':player['name'],'2':enemy['name'],'X':"Go back"}
                        print('\nSelect your target: \n')
                        targetInput = playerAction(targetControls)
                        if targetInput != "go back":
                            #Consumes a turn in combat if player decides to use a skill
                            consumeTurn = True
                            #print(targetInput,enemy['name'])
                            target = enemy if targetInput.lower() == enemy['name'].lower() else player
                            handleSkill(skillInput,player,target)

            if playerInput == "equipment":
                consumeTurn = False
                for slot in player['equipments']:
                    if slot != 'trinket':
                        print(f"{slot.capitalize()} slot: {Fore.CYAN if player['equipments'][slot] != 'empty' else Fore.YELLOW }{player['equipments'][slot]}{Style.RESET_ALL}{Fore.GREEN} ({eval(slot)[player['equipments'][slot]]} {'attack' if slot == 'weapon' else 'defence'} ){Style.RESET_ALL} ")
                    else:
                        print(f"{slot.capitalize()} slot: {Fore.CYAN if player['equipments'][slot] != 'empty' else Fore.YELLOW }{player['equipments'][slot]}{Style.RESET_ALL}{Fore.YELLOW} ({eval(slot)[player['equipments'][slot]]} stats ){Style.RESET_ALL} ")
                equipmentsControls = {'X':"Go Back"}
                for idx,slot in enumerate(player['equipments'], start = 1):
                    if player['equipments'][slot] != "empty":     
                        equipmentsControls[str(idx)] = player['equipments'][slot]
                print(f"Select item to unequip.")
                equipmentsInput = playerAction(equipmentsControls)
                if equipmentsInput != "go back":
                    #Consumes a turn in combat if player decides to unequip an item
                    consumeTurn = True
                    # Handles unequipping
                    for slot in player['equipments']:
                        if player['equipments'][slot] == equipmentsInput:
                            print(f"You remove your {Fore.CYAN}{player['equipments'][slot]}{Style.RESET_ALL} from your {slot} slot and put it in your inventory.")
                            player['inventory'].append(equipmentsInput)
                            player['equipments'][slot] = "empty"
                            input("Press enter to continue...")

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
                    chanceToHit = max(math.floor(((enemy['accuracy']['current'] - player['dodge']['current'])/enemy['accuracy']['current'])*100) + (enemy['speed']['current'] - player['speed']['current']),5)
                    print(f"({chanceToHit}%) The {enemy['name']} attempts to attack you...")
                    if randint(0,100) < chanceToHit:
                        lowerBoundDamage = enemy['attack']['current'][0]
                        upperBoundDamage = enemy['attack']['current'][1]
                        
                        damage = max(randint(lowerBoundDamage,upperBoundDamage) - (player['defence']['current']),0)
                        player['health']['current'] -= damage
                        print(f"{Fore.YELLOW if damage > 0 else Fore.CYAN}The {enemy['name']} hits you for {damage} damage!{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.GREEN}You dodged the {enemy['name']}'s attack!{Style.RESET_ALL}")

                elif enemyInput == "wait":
                    print("The enemy skipped their turn!")

                # Handle end of turn effect for enemy
                handleTurnEnd(enemy)
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
                # Handle end of turn effect for player, decrement duration and remove statuses, restore stat to max, cooldown,check death etc.
                handleTurnEnd(player)
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
    # Normal methods of copy does not work if list itself contains lists.
    # Hence, deep copy required to prevent lists within old list from being overwritten.
    outputMap = deepcopy(inputMap)
    for idxY, row in enumerate(outputMap):
        for idX, pos in enumerate(row):
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

    However, the dungeon is foggy, and despite having a torch, you can only reveal a small area
    around you. There will be monsters and loot scattered across the play area.

    Pay close attention to your health, food and torch level as you traverse the Dungeon.

    Find loot on the map and slay enemies to recieve gold, supplies and equipments.
    Also look out for Merchants to buy and sell items.
    _______________________________________________________________________________________
    
    """
    print(welcomeText)
    input("Press enter to continue...")

    playerName = False
    while not playerName or len(playerName) > 20 or len(playerName) < 3:
        print("_____________________________________________________________________________________")
        playerName = input('''
        Please enter a valid name for your character (between 3 and 20 characters): 
        ''')
    sleep(1)

    print("""
    That's a fine name!
    """)

    sleep(1)
    # Ask player to choose map
    mapSelectControls = {}
    for idx,mapChoice in enumerate(maps, start = 1):    
        mapSelectControls[str(idx)] = mapChoice
    print("_____________________________________________________________________________________")
    print('''
    Please select a map by entering the corresponding digits: 
    ''')
    selectedMap = playerAction(mapSelectControls)
    currentMap = maps[selectedMap]
    print(f"{Fore.GREEN}Map selected: {selectedMap.capitalize()}!{Style.RESET_ALL}")

    # Creates fogged version of the actual map.
    # This fogged version is the one shown to players
    playerMap = fogMap(currentMap)
    sleep(1)
    # CLASS SELECT

    classSelectText = """
    _____________________________________________________________________________________
    Available classes:

    Warrior: Good all-rounder. Can use Guard and Disarm.
    Ranger: Dextrous at the sacrifice of power and durability. Casts Poison and Inner Focus.
    Beserker: Powerful in combat but neglects defences and supplies. Can use Empower.
    Survivalist: Durable and starts with more supplies. Can Daze and Slow.
    _____________________________________________________________________________________
    
    """
    print(classSelectText)
    classSelected = False
    # Loop continues until class is selected and confirmed by player
    while not classSelected:
        classesControls = {}
        for idx,classChoice in enumerate(classes,start = 1):    
            classesControls[str(idx)] = classChoice
        print('''
        Please select a character class by entering the corresponding digit: 
        ''')
        classesInput = playerAction(classesControls)
        classes[classesInput]['name'] = playerName
        print(f"{Fore.GREEN}Class selected: {classesInput}!{Style.RESET_ALL}")
        print(f"{Fore.WHITE}_____________________________________________________________________________________")
        message = ""
        for info in classes[classesInput]:
            # Handles formatting of 1-level-deep dictionaries for display
            if type(classes[classesInput][info]) is dict:
                message += f"{Fore.GREEN}{str(info).capitalize()}{Style.RESET_ALL}: \n"
                for nestedInfo in classes[classesInput][info]:
                    message += f"\t{Fore.YELLOW}{str(nestedInfo).capitalize()}{Style.RESET_ALL}:{classes[classesInput][info][nestedInfo]}\n"
            else:
                message += f"{Fore.GREEN}{str(info).capitalize()}{Style.RESET_ALL}: {str(classes[classesInput][info]).capitalize()}\n"
        print(message)
        print(f"_____________________________________________________________________________________{Style.RESET_ALL}")
        confirmClassControl = {"Y":"Yes","N":"No"}
        print(f"Are you sure you want to select {Fore.CYAN}{classesInput.capitalize()}{Style.RESET_ALL}?")
        decision = playerAction(confirmClassControl)
        if decision == 'yes':
            player = classes[classesInput]
            classSelected = True
        else:
            continue

    print("\nWise choice.")
    sleep(1)

    input('''
    You may now buy some items from the shop to prepare for the journey ahead.
    
    Try to prioritise consumables as they will restore your health, food and torch levels.

    It is recommeded that you use the 'Buy recommended consumables' option by
    pressing 'B' in the next menu if you are a beginner

    Press enter to continue...\n''')
    handleMerchant(player, startOfGame=True)
    sleep(2)
    input('''
    You are now ready for your journey out of the Dungeon.

    Remember to equip any weapon and armor that you bought from the shop!!
    
    Good luck! Press enter to continue...''')

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
    # Calls update fog at start of game so that the 8 tiles around the player are initially revealed.
    playerMap = updateFog(playerMap,currentMap,x,y,prevX,prevY,2)
    # Shows map to player at start of game
    printMap(playerMap)
    print("_____________________________________________________________________________________")
    print("""
    See that "P" on the map? That represents you, the Player.
    "0" represents impassable walls while "." represents unrevealed terrain.
    There are various other objects which will be described as you move next to them.

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
    #Initialise torchLit
    torchLit = 2
    while playerInput != "quit":
        prevX = x
        prevY = y

        # Whichever action that doesnt consume a turn should set this as false
        consumeTurn = True

        #Prompt player for input
        playerInput = playerAction(mapControls)

        #Handle stat modifiers 
        playerTrinket = player["equipments"]["trinket"]
        for stat in trinket[playerTrinket]:
            player[stat]["modifier"] = trinket[playerTrinket][stat]
            player[stat]["current"] = player[stat]["max"] + player[stat]["modifier"] 
        #Armor modifier:
        playerArmor = player["equipments"]["armor"]
        player['defence']["modifier"] = armor[playerArmor]
        player['defence']["current"] = player['defence']["max"] + player['defence']["modifier"] 
        #Weapon modifier:
        playerWeapon = player["equipments"]["weapon"]
        player['attack']["modifier"][0] = weapon[playerWeapon][0]
        player['attack']["modifier"][1] = weapon[playerWeapon][1]
        player['attack']["current"][0] = player['attack']["max"][0] + player['attack']["modifier"][0]
        player['attack']["current"][1] = player['attack']["max"][1] + player['attack']["modifier"][1]  

        if playerInput == "quit":
            print(f"{Fore.RED}You succumbed to the dangers of the Dungeon...Game Over.{Style.RESET_ALL}")
            break

        if playerInput == "map":
            consumeTurn = False
            printMap(playerMap)

        if playerInput == "character":
            consumeTurn = False
            print(f"{Fore.WHITE}_____________________________________________________________________________________")
            message = ""
            for info in player:
                #print(type(player[info]), player[info])
                if type(player[info]) is dict:
                    message += f"{Fore.GREEN}{str(info).capitalize()}{Style.RESET_ALL}: \n"
                    for nestedInfo in player[info]:
                        message += f"\t{Fore.YELLOW}{str(nestedInfo).capitalize()}{Style.RESET_ALL}:{player[info][nestedInfo]}\n"
                else:
                    message += f"{Fore.GREEN}{str(info).capitalize()}{Style.RESET_ALL}: {str(player[info]).capitalize()}\n"
            print(message)
            print(f"_____________________________________________________________________________________{Style.RESET_ALL}")
            input("Press enter to continue...")

        if playerInput == "inventory":
            consumeTurn = False
            handleInventoryDescription(player)
            inventoryControls = {'X':"Go Back"}
            for idx,item in enumerate(player['inventory'],start = 1):
                inventoryControls[str(idx)] = item
            print("Select item to equip/consume.")
            inventoryInput = playerAction(inventoryControls)
            if inventoryInput != "go back":
                handleUse(player, inventoryInput)
                # Updates torch levels so that area around player is lit immediately if they refueled.
                if player['torch']['current'] >= 10:
                    torchLit = 2
                elif 1 < player['torch']['current'] < 10: 
                    torchLit = 1
                else:
                    torchLit = 0
                playerMap = updateFog(playerMap,currentMap,x,y,prevX,prevY,torchLit)
                input("Press enter to continue...")

        if playerInput == "equipment":
            consumeTurn = False
            # Displays information regarding player's equipments
            for slot in player['equipments']:
                print(f"{slot.capitalize()} slot: {Fore.CYAN if player['equipments'][slot] != 'empty' else Fore.YELLOW }{player['equipments'][slot]}{Style.RESET_ALL}{Fore.GREEN} (+ {eval(slot)[player['equipments'][slot]]} {'attack' if slot == 'weapon' else 'defence'} ){Style.RESET_ALL} ")
            equipmentsControls = {'X':"Go Back"}
            for idx,slot in enumerate(player['equipments'],start = 1):
                if player['equipments'][slot] != "empty":     
                    # Add a userInput:value pair to the equipment controls if equipment slot is taken by an equipment
                    equipmentsControls[str(idx)] = player['equipments'][slot]
            print(f"Select item to unequip.")
            equipmentsInput = playerAction(equipmentsControls)
            if equipmentsInput != "go back":
                # Handles unequipping
                for slot in player['equipments']:
                    if player['equipments'][slot] == equipmentsInput:
                        print(f"You remove your {Fore.CYAN}{player['equipments'][slot]}{Style.RESET_ALL} from your {Fore.YELLOW}{slot}{Style.RESET_ALL} slot and put it in your inventory.")
                        player['inventory'].append(equipmentsInput)
                        player['equipments'][slot] = "empty"
                        input("Press enter to continue...")

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

        # M is a merchant
        if currentMap[y][x] == "M":

            print(f"{Fore.YELLOW}You meet the Merchant and start trading!{Style.RESET_ALL}")
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
            
# Starts Game.

main()

