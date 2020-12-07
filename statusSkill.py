"""
F04 Group 2: Bryan Tan, Ryan Kaw Zheng Da, Colin Teoh, Xu Muzi, Joseph Lai
"""

from colorama import Fore, Style, Back

# Status effect functions
def poisoned(targetCharacter,magnitude):
    targetCharacter["health"]["current"] -=  magnitude
    print(f"{Fore.CYAN}{targetCharacter['name']}{Style.RESET_ALL} is {Fore.RED}Poisoned{Style.RESET_ALL} for {magnitude} health! ({targetCharacter['status']['poisoned']['duration']} turns remaining)")

def dazed(targetCharacter,magnitude):
    targetCharacter["accuracy"]["modifier"] -= magnitude * 5
    print(f"{Fore.CYAN}{targetCharacter['name']}{Style.RESET_ALL} is {Fore.YELLOW}Dazed{Style.RESET_ALL}! Accuracy reduced by {magnitude * 5}! ({targetCharacter['status']['dazed']['duration']} turns remaining)")

def slowed(targetCharacter,magnitude):
    targetCharacter["dodge"]["modifier"] -= magnitude * 5 
    targetCharacter["speed"]["modifier"] -= magnitude
    print(f"{Fore.CYAN}{targetCharacter['name']}{Style.RESET_ALL} is {Fore.YELLOW}Slowed{Style.RESET_ALL}! Dodge reduced by {magnitude * 5} and speed reduced by {magnitude}! ({targetCharacter['status']['slowed']['duration']} turns remaining)")

def focused(targetCharacter,magnitude):
    targetCharacter["accuracy"]["modifier"] += magnitude * 5
    targetCharacter["dodge"]["modifier"] += magnitude * 5
    print(f"{Fore.CYAN}{targetCharacter['name']}{Style.RESET_ALL} is {Fore.GREEN}Focused{Style.RESET_ALL}! Accuracy increased by {magnitude * 5}  and dodge increased by {magnitude * 5}! ({targetCharacter['status']['focused']['duration']} turns remaining)")

def empowered(targetCharacter,magnitude):
    targetCharacter["attack"]["modifier"][0] += magnitude
    targetCharacter["attack"]["modifier"][1] += magnitude
    print(f"{Fore.CYAN}{targetCharacter['name']}{Style.RESET_ALL} is {Fore.GREEN}Empowered{Style.RESET_ALL}! Attack increased by ({magnitude},{magnitude})! ({targetCharacter['status']['empowered']['duration']} turns remaining)")

def sturdy(targetCharacter,magnitude):
    targetCharacter["defence"]["modifier"] += magnitude
    print(f"{Fore.CYAN}{targetCharacter['name']}{Style.RESET_ALL} is {Fore.GREEN}Sturdy{Style.RESET_ALL}! Defence increased by {magnitude}! ({targetCharacter['status']['sturdy']['duration']} turns remaining)")

def disarmed(targetCharacter,magnitude):
    targetCharacter["attack"]["modifier"][0] -= magnitude
    targetCharacter["attack"]["modifier"][1] -= magnitude
    print(f"{Fore.CYAN}{targetCharacter['name']}{Style.RESET_ALL} is {Fore.YELLOW}Disarmed{Style.RESET_ALL}! Attack decreased by ({magnitude},{magnitude})! ({targetCharacter['status']['disarmed']['duration']} turns remaining)")

def resistant(targetCharacter,magnitude):
    negativeStatus = ['poisoned','dazed','slowed','disarmed','stunned']
    for statusKey in targetCharacter["status"]:
        if statusKey in negativeStatus:
            targetCharacter["status"][statusKey]["duration"] = max(0,targetCharacter["status"][statusKey]["duration"] - magnitude)
            #resistedStatus = targetCharacter["status"].pop(statusKey)
            print (f"{Fore.CYAN}{targetCharacter['name']}{Style.RESET_ALL} {Fore.GREEN}resisted {Style.RESET_ALL}{statusKey} effect, decreasing its duration by {magnitude} turns!({targetCharacter['status']['resistant']['duration']} turns remaining)")

#Status effect dictionaries
statusEffects = {
    "poisoned":poisoned,
    "dazed":dazed,
    "slowed":slowed,
    "focused":focused,
    "empowered":empowered,
    "sturdy":sturdy,
    "disarmed":disarmed,
    "resistant":resistant,
}

'''
 poisoned: - x health every turn -ranger
 dazed: decrease accuracy -survivalist
 slowed: decrease speed,dodge -survivalist
 focused: increased accuracy, dodge -ranger
 empowered: add attack -berserker
 sturdy: add defence -warrior
 disarmed: decrease attack for x turns -warrior
 resistant: decreased -ve status effect by x turns -surval
 stunned (if possible to implement): skip turn

'''
'''

armor break: decrease defence
'''

#Skill Functions

def poison(casterCharacter,targetCharacter, duration, magnitude):
    targetCharacter["status"]["poisoned"] = {
        "duration":duration,
        "magnitude":magnitude,
        }
    print(f"{Fore.CYAN}{casterCharacter['name']}{Style.RESET_ALL} used {Fore.GREEN}Poison{Style.RESET_ALL} of power {magnitude} on {Fore.YELLOW}{targetCharacter['name']}{Style.RESET_ALL} for {duration} turns!")

def daze(casterCharacter,targetCharacter, duration, magnitude):
    targetCharacter["status"]["dazed"] = {
        "duration":duration,
        "magnitude":magnitude,
    }
    print(f"{Fore.CYAN}{casterCharacter['name']}{Style.RESET_ALL} used {Fore.GREEN}Daze{Style.RESET_ALL} of power {magnitude} on {Fore.YELLOW}{targetCharacter['name']}{Style.RESET_ALL} for {duration} turns!")

def slow(casterCharacter,targetCharacter, duration, magnitude):
    targetCharacter["status"]["slowed"] = {
        "duration":duration,
        "magnitude":magnitude,
    }
    print(f"{Fore.CYAN}{casterCharacter['name']}{Style.RESET_ALL} used {Fore.GREEN}Slow{Style.RESET_ALL} of power {magnitude} on {Fore.YELLOW}{targetCharacter['name']}{Style.RESET_ALL} for {duration} turns!")

def focus(casterCharacter,targetCharacter, duration, magnitude):
    targetCharacter["status"]["focused"] = {
        "duration":duration,
        "magnitude":magnitude,
    }
    print(f"{Fore.CYAN}{casterCharacter['name']}{Style.RESET_ALL} used {Fore.GREEN}Inner Focus{Style.RESET_ALL} of power {magnitude} on {Fore.YELLOW}{targetCharacter['name']}{Style.RESET_ALL} for {duration} turns!")

def empower(casterCharacter,targetCharacter, duration, magnitude):
    targetCharacter["status"]['empowered'] = {
        "duration":duration,
        "magnitude":magnitude,

    }
    print(f"{Fore.CYAN}{casterCharacter['name']}{Style.RESET_ALL} used {Fore.GREEN}Empower{Style.RESET_ALL} of power {magnitude} on {Fore.YELLOW}{targetCharacter['name']}{Style.RESET_ALL} for {duration} turns!")

def guard(casterCharacter,targetCharacter, duration, magnitude):
    targetCharacter["status"]['sturdy'] = {
        "duration":duration,
        "magnitude":magnitude,
    }
    print(f"{Fore.CYAN}{casterCharacter['name']}{Style.RESET_ALL} used {Fore.GREEN}Guard{Style.RESET_ALL} of power {magnitude} on {Fore.YELLOW}{targetCharacter['name']}{Style.RESET_ALL} for {duration} turns!")

def disarm(casterCharacter,targetCharacter, duration, magnitude):
    targetCharacter["status"]['disarmed'] = {
        "duration":duration,
        "magnitude":magnitude,
    }
    print(f"{Fore.CYAN}{casterCharacter['name']}{Style.RESET_ALL} used {Fore.GREEN}Disarm{Style.RESET_ALL} of power {magnitude} on {Fore.YELLOW}{targetCharacter['name']}{Style.RESET_ALL} for {duration} turns!")

def resist(casterCharacter,targetCharacter, duration, magnitude):
    targetCharacter["status"]['resistant'] = {
        "duration":duration,
        "magnitude":magnitude,
    }
    print(f"{Fore.CYAN}{casterCharacter['name']}{Style.RESET_ALL} used {Fore.GREEN}Resist{Style.RESET_ALL} of power {magnitude} on {Fore.YELLOW}{targetCharacter['name']}{Style.RESET_ALL} for {duration} turns!")

#Skill dictionaries
skills = {
    "poison":{
        "function":poison,
        "description":"Poisons target, removing health each turn.",
    },
    "daze":{
        "function":daze,
        "description":"Dazes target, decreasing accuracy of target.",
    },
    "slow":{
        "function":slow,
        "description":"Slows target, decreasing dodge and speed of target.",
    },
    "heighten senses":{
        "function":focus,
        "description":"Heighten senses of target, increasing target accuracy and dodge.",
    },
    "empower":{
        "function":empower,
        "description":"Empowers target, increasing attack.",
    },
    "guard":{
        "function":guard,
        "description":"Guards target, increasing defence.",
    },
    "disarm":{
        "function":disarm,
        "description":"Disarms target, decreasing attack.",
    },
    "resist":{
        "function":resist,
        "description":"Grants resistance to target, decreasing duration of negative status effects.",
    },
    #"stun":stun,
}