import math
from colorama import Fore, Style, Back
from random import randint
from random import choice
from copy import deepcopy, copy
from time import sleep
from mapLoot import mapLoot
from classes import classes
from maps import maps
from nonPlayableCharacters import nonPlayableCharacters
from items import weapon,armor,trinket,consumables,priceSheet
from statusSkill import *



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
    print(f"Available actions: {f' '.join(f'[{Fore.GREEN if idx%2==0 else Fore.YELLOW}{tup[0]}: {tup[1].capitalize()}{Style.RESET_ALL}] ' for idx,tup in enumerate(availableActions.items()))}")
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
        if item in weapon:
            message += f"Weapon: {Fore.CYAN}{item}{Style.RESET_ALL} ({Fore.GREEN}+{weapon[item][0]}-{weapon[item][1]}{Style.RESET_ALL} attack when equipped)\n"
        elif item in armor:
            message += f"Armor: {Fore.CYAN}{item}{Style.RESET_ALL} ({Fore.GREEN}+{armor[item]}{Style.RESET_ALL} defence when equipped)\n"
        elif item in trinket:
            message += f"Trinket: {Fore.CYAN}{item}{Style.RESET_ALL} ({Fore.YELLOW} {trinket[item]}{Style.RESET_ALL} stat modifier when equipped)\n"
        elif item in consumables:
            message += f"Consumable: {Fore.YELLOW}{item}{Style.RESET_ALL} (restores {Fore.GREEN}{consumables[item]}{Style.RESET_ALL} when used)\n"
    print(message)

#Copy inventory description for skilldescription
def handleSkillDescription(inputCharacter):
    print("\nSkills in your skillset:\n")
    message = ""
    for skillKey in inputCharacter['skills']:
        message += f"{skillKey.capitalize()}: {skills[skillKey]['description']}\n"
        message += f"\tPower: {inputCharacter['skills'][skillKey]['magnitude']}\n"
        message += f"\tDuration: {inputCharacter['skills'][skillKey]['duration']}\n"
        message += f"\tCooldown: {inputCharacter['skills'][skillKey]['cooldown']}\n"
        message += f"\tTurns till ready: {inputCharacter['skills'][skillKey]['turnsTillReady']}\n"
    print(message)

def handleSkill(castedSkill,casterCharacter,targetCharacter):
    print(targetCharacter['name'])
    skills[castedSkill]['function'](casterCharacter,targetCharacter,casterCharacter['skills'][castedSkill]['duration'],casterCharacter['skills'][castedSkill]['magnitude'])
    casterCharacter['skills'][castedSkill]["turnsTillReady"] = casterCharacter['skills'][castedSkill]['cooldown']
    #print(f"{casterCharacter['name']} casts {castedSkill} of power {casterCharacter['skills'][castedSkill]['magnitude']} on {targetCharacter['name']} for {casterCharacter['skills'][castedSkill]['duration']} turns!")

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


    # To implement choice of equipping in either weapon or off hand (perhaps)
    # Check which slot equipment belongs. If current equipment slot not empty, remove current equipment first before replacing with new equipment
    elif inputItem in weapon:
        if inputCharacter["equipments"]["weapon"] != "empty":
            inputCharacter["inventory"].append(inputCharacter["equipments"]["weapon"])
            print(f"You remove your {inputCharacter['equipments']['weapon']} and put it in your inventory.")
        inputCharacter["equipments"]["weapon"] = inputItem
        print(f"You equipped your {inputItem} in your weapon slot ( + {weapon[inputItem][0]}-{weapon[inputItem][1]} attack ).")

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

def handleTurnStart(inputCharacter):
    #handle attack modifier calculations
    inputCharacter['attack']['current'][0] = max(0,inputCharacter['attack']['max'][0] + inputCharacter['attack']['modifier'])
    inputCharacter['attack']['current'][1] = max(0,inputCharacter['attack']['max'][1] + inputCharacter['attack']['modifier'])
    temporaryCombatStats = ['defence','speed','accuracy','dodge']
    for stat in temporaryCombatStats:
        inputCharacter[stat]['current'] = max(0,inputCharacter[stat]['max'] + inputCharacter[stat]['modifier'])

def handleTurnEnd(inputCharacter):
    #handle attack modifier calculations
    inputCharacter['attack']['modifier'] = 0
    inputCharacter['attack']['current'] = copy(inputCharacter['attack']['max'])

    temporaryCombatStats = ['defence','speed','accuracy','dodge']
    for stat in temporaryCombatStats:
        inputCharacter[stat]['modifier'] = 0
        inputCharacter[stat]['current'] = copy(inputCharacter[stat]['max'])
        
    expiredStatusList = []
    
    for key,val in inputCharacter['status'].items():
        #print(key,val)
        statusEffects[key](inputCharacter,inputCharacter['status'][key]['magnitude'])
        inputCharacter['status'][key]['duration'] -= 1
        if inputCharacter['status'][key]['duration'] <= 0:
            expiredStatusList.append((key,val))

    for expiredStatusTuple in expiredStatusList:
        expiredEffectName = expiredStatusTuple[0]
        inputCharacter['status'].pop(expiredEffectName)
        print(f"{inputCharacter['name']} is no longer {expiredEffectName}!")

    for skill in inputCharacter['skills']:
        if inputCharacter['skills'][skill]["turnsTillReady"] > 0:
            inputCharacter['skills'][skill]["turnsTillReady"] -= 1

def handleMerchant(inputPlayer, startOfGame=False):
    shopInput = ""
    #Sell price = buy price/5
    if startOfGame:
        print(f"{Fore.CYAN}Merchant: Welcome to my shop! Before you embark, please consider buying some items from my shop!{Style.RESET_ALL}")
    else:
        print(f"{Fore.CYAN}Merchant: Hi there! Which category would you like to browse?{Style.RESET_ALL}")
    while shopInput != "leave":
        if startOfGame:
            shopControls = {"1":"Weapon","2":"Armor","3":"Consumables","4":"Trinket","5":"Sell","B":"Buy recommended consumables","X":"Leave"}
        else:
            shopControls = {"1":"Weapon","2":"Armor","3":"Consumables","4":"Trinket","5":"Sell","X":"Leave"}
        print(f"Gold: {inputPlayer['gold']}")
        shopInput = playerAction(shopControls)
        if shopInput == "leave":
            print(f"{Fore.CYAN}Merchant: Thanks for your patronage, good luck!{Style.RESET_ALL}")
            break
        elif shopInput == "buy recommended consumables":
            startOfGame == False
            #So far, only consumables can be entered here
            recommendedStarter = ["small health potion","small torch fuel","small food ration"]
            for item in recommendedStarter:
                if inputPlayer['gold'] >= priceSheet['consumables'][item]:
                    print(f"You bought {item} for {priceSheet['consumables'][item]} Gold!")
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
                # Eval() converts a string like "weapon" to the variable weapon
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
                    sellPrice = math.floor(priceSheet["armor"][item]/5)
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

# Function to handle status effects ( TO DO )
def handleStatus(inputCharacter):
    return None
    #for key,val in inputCharacter["status"]:


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

        while inCombat:
            #Handle trinket stat modifier
            playerTrinket = player["equipments"]["trinket"]
            for stat in trinket[playerTrinket]:
                player[stat]["modifier"] += trinket[playerTrinket][stat]
            
            handleTurnStart(player)
            handleTurnStart(enemy)

            combatLog =  (
                f"\n"
                f"{player['name']}\'s health: {Fore.RED if player['health']['current'] < 15 else Fore.WHITE}{player['health']['current']}/{player['health']['max']}{Style.RESET_ALL}\n"
                f"{enemy['name']}\'s health: {Fore.RED if enemy['health']['current'] < 10 else Fore.WHITE}{enemy['health']['current']}/{enemy['health']['max']}{Style.RESET_ALL}\n"
                f"{player['name']}\'s chance to hit: {max(math.floor(((player['accuracy']['current'] - enemy['dodge']['current'])/player['accuracy']['current'])*100) + (player['speed']['current'] - enemy['speed']['current']),10)}%\n"
                f"{player['name']}\'s chance to dodge: {100 - max(math.floor(((enemy['accuracy']['current'] - player['dodge']['current'])/enemy['accuracy']['current'])*100) + (enemy['speed']['current'] - player['speed']['current']),5)}%\n"
                f"{player['name']}\'s damage: {player['attack']['current'][0] + weapon[player['equipments']['weapon']][0]} - {player['attack']['current'][1] + weapon[player['equipments']['weapon']][1]}\n"
                f"{player['name']}\'s defence: {player['defence']['current'] + armor[player['equipments']['armor']]}\n"

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
                "S": "Skill",
                "D": "Describe",
                "I": "Inventory",
                "C": "Character",
                "E": "Equipment",
                "R": "Run"
            }
            # Player's turn
            
            # Allow player input if enemy is not acting first
            if not enemyInitiative:
                playerInput = playerAction(combatControls)
                print("______________________________________")
            else:
                playerInput = "enemyInitiative"

            #handle status effects here

            # Handle player inputs
            if playerInput == "attack":
                # Maybe calculate dodge and accuracy, whether attack hits, here.
                # Hit chance formula modified from https://www.gamedev.net/forums/topic/685930-the-simplest-but-most-effective-and-intuitive-way-to-implement-accuracy-and-dodge-chance-in-an-rpg/
                chanceToHit = max(math.floor(((player['accuracy']['current'] - enemy['dodge']['current'])/player['accuracy']['current'])*100) + (player['speed']['current'] - enemy['speed']['current']),10)
                print(f"\n({chanceToHit}%) You attempt to strike...")
                if randint(0,100) < chanceToHit:
                    # Calculates lower and upper bound of damage based on base attack + main weapon dmg 
                    lowerBoundDamage = player['attack']['current'][0] + weapon[player["equipments"]["weapon"]][0] # + math.floor(weapon[player["equipments"]["offHand"]][0]/2)
                    upperBoundDamage = player['attack']['current'][1] + weapon[player["equipments"]["weapon"]][1] # + math.floor(weapon[player["equipments"]["offHand"]][1]/2)

                    # max is to prevent negative damage from being dealt
                    damage = max(randint(lowerBoundDamage,upperBoundDamage) - (enemy['defence']['current']),0)
                    enemy['health']['current'] -= damage
                    print(f"{Fore.CYAN}You hit the {enemy['name']} for {damage} damage!{Style.RESET_ALL}")
                
                else:
                    print(f"{Fore.RED}You missed!{Style.RESET_ALL}")
                    

            # This is a dumb move now, but maybe can be made useful in the future
            if playerInput == "wait":
                print("You skipped your turn...")

            if playerInput == "run":
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

            if playerInput == "skill":
                consumeTurn = False
                skillInput = ""
                #while skillInput != "go back":
                #To implement skill description
                handleSkillDescription(player)
                skillControls = {'X':"Go Back"}
                for idx,skill in enumerate(player['skills'], start = 1):
                    skillControls[str(idx)] = skill
                print("Select skill to use: \n")
                skillInput = playerAction(skillControls)
                if skillInput != "go back":
                    if player['skills'][skillInput]["turnsTillReady"] > 0:
                        print (f"Skill is not ready! {player['skills'][skillInput]['turnsTillReady']} more turns needed!")
                    else:
                        targetControls = {'1':player['name'],'2':enemy['name'],'X':"Go back"}
                        print('Select your target: \n')
                        targetInput = playerAction(targetControls)
                        if targetInput != "go back":
                            #Consumes a turn in combat if player decides to use a skill
                            consumeTurn = True
                            print(targetInput,enemy['name'])
                            target = enemy if targetInput.lower() == enemy['name'].lower() else player
                            handleSkill(skillInput,player,target)

            if playerInput == "equipment":
                consumeTurn = False
                for slot in player['equipments']:
                    print(f"{slot.capitalize()} slot: {Fore.CYAN if player['equipments'][slot] != 'empty' else Fore.YELLOW }{player['equipments'][slot]}{Style.RESET_ALL}{Fore.GREEN if slot != 'trinket' else Fore.YELLOW} ({eval(slot)[player['equipments'][slot]]} {'attack' if slot == 'weapon' else 'defence'} ){Style.RESET_ALL} ")
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
                    chanceToHit = max(math.floor(((enemy['accuracy']['current'] - player['dodge']['current'])/enemy['accuracy']['current'])*100) + (enemy['speed']['current'] - player['speed']['current']),5)
                    print(f"({chanceToHit}%) The {enemy['name']} attempts to attack you...")
                    if randint(0,100) < chanceToHit:
                        lowerBoundDamage = enemy['attack']['current'][0]
                        upperBoundDamage = enemy['attack']['current'][1]
                        damage = max(randint(lowerBoundDamage,upperBoundDamage) - (player['defence']['current'] + armor[player["equipments"]["armor"]]),0)
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
    playerName = input('''
    Please enter a name for your character: 
    ''')
    sleep(1)
    print("""
    That's a fine name!
    """)
    sleep(1)
    # INITIALISE MAP
    mapSelectControls = {}
    for idx,mapChoice in enumerate(maps, start = 1):    
        mapSelectControls[str(idx)] = mapChoice
    print("_____________________________________________________________________________________")
    print('''
    Please select a map by entering the corresponding digits: 
    ''')
    selectedMap = playerAction(mapSelectControls)
    currentMap = maps[selectedMap]
    # Go back functionality not yet implemented
    if currentMap != "go back":
        print(f"{Fore.GREEN}Map selected: {selectedMap.capitalize()}!{Style.RESET_ALL}")

    playerMap = fogMap(currentMap)
    sleep(1)
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
    print('''
    Please select a character class by entering the corresponding digit: 
    ''')
    classesInput = playerAction(classesControls)
    # Go back functionality not yet implemented
    if classesInput != "go back":
        classes[classesInput]['name'] = playerName
        print(f"{Fore.GREEN}Class selected: {classesInput}!{Style.RESET_ALL}")
        print(f"{Fore.WHITE}_____________________________________________________________________________________")
        for info in classes[classesInput]:
            print(f"{str(info).capitalize()}: {str(classes[classesInput][info]).capitalize()}")
        print(f"_____________________________________________________________________________________{Style.RESET_ALL}")
        classSelected = True
        player = classes[classesInput]
    sleep(2)


    # To give player chance to read the stats
    input('''
    You may now buy some items from the shop to prepare for the journey ahead.
    
    Try to prioritise consumables as they will restore your health, food and torch levels.

    Press enter to continue...''')
    handleMerchant(player, startOfGame=True)
    sleep(2)
    input('''
    You are now ready for your journey out of the Dungeon.

    Remember to equip any weapon and armor that you bought from the shop!!
    
    Good luck! Press enter to continue...''')
    
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

        #Handle tricket stat modifier (Need test this part for bugs)
        playerTrinket = player["equipments"]["trinket"]
        for stat in trinket[playerTrinket]:
            player[stat]["current"] = player[stat]["max"] + trinket[playerTrinket][stat]

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
            if inventoryInput != "go back":
                handleUse(player, inventoryInput)
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
            for slot in player['equipments']:
                print(f"{slot.capitalize()} slot: {Fore.CYAN if player['equipments'][slot] != 'empty' else Fore.YELLOW }{player['equipments'][slot]}{Style.RESET_ALL}{Fore.GREEN} (+ {eval(slot)[player['equipments'][slot]]} {'attack' if slot == 'weapon' else 'defence'} ){Style.RESET_ALL} ")
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

