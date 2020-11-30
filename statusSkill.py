


def poisoned(targetCharacter,magnitude):
    targetCharacter["health"]["current"] -=  magnitude
    print(f"{targetCharacter['name']} is poisoned for {magnitude} health!({targetCharacter['status']['poisoned']['duration']} turns left)")

def dazed(targetCharacter,magnitude):
    targetCharacter["accuracy"]["modifier"] -= magnitude * 5
    print(f"{targetCharacter['name']} is dazed! Accuracy reduced by {magnitude}!({targetCharacter['status']['dazed']['duration']} turns left)")

def slowed(targetCharacter,magnitude):
    targetCharacter["dodge"]["modifier"] -= magnitude * 5 
    targetCharacter["speed"]["modifier"] -= magnitude
    print(f"{targetCharacter['name']} is slowed! Dodge reduced by {magnitude * 5} and speed reduced by {magnitude}!({targetCharacter['status']['slowed']['duration']} turns left)")

def focused(targetCharacter,magnitude):
    targetCharacter["accuracy"]["modifier"] += magnitude * 5
    targetCharacter["dodge"]["modifier"] += magnitude * 5
    print(f"{targetCharacter['name']} is focused! Accuracy increased by {magnitude * 5}  and dodge increased by {magnitude}!({targetCharacter['status']['focused']['duration']} turns left)")

def empowered(targetCharacter,magnitude):
    targetCharacter["attack"]["modifier"] += magnitude
    print(f"{targetCharacter['name']} is empowered! Attack increased by ({magnitude},{magnitude})!({targetCharacter['status']['empowered']['duration']} turns left)")

def sturdy(targetCharacter,magnitude):
    targetCharacter["defence"]["modifier"] += magnitude
    print(f"{targetCharacter['name']} is sturdy! Defence increased by {magnitude}!({targetCharacter['status']['sturdy']['duration']} turns left)")

def disarmed(targetCharacter,magnitude):
    targetCharacter["attack"]["modifier"] -= magnitude
    print(f"{targetCharacter['name']} is disarmed! Attack decreased by ({magnitude},{magnitude})!({targetCharacter['status']['disarmed']['duration']} turns left)")

def resistant(targetCharacter,magnitude):
    negativeStatus = ['poisoned','dazed','slowed','disarmed','stunned']
    for statusKey in targetCharacter["status"]:
        if statusKey in negativeStatus:
            targetCharacter["status"][statusKey]["duration"] = max(0,targetCharacter["status"][statusKey]["duration"] - magnitude)
            #resistedStatus = targetCharacter["status"].pop(statusKey)
            print (f"{targetCharacter['name']} resisted {statusKey} effect, decreasing its duration by {magnitude} turns!({targetCharacter['status']['resistant']['duration']} turns left)")

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
 poisoned: - x health every turn
 dazed: decrease accuracy
 slowed: decrease speed,dodge
 focused: increased accuracy, dodge
 empowered: add attack
 sturdy: add defence
 disarmed: decrease attack for x turns
 resistant: decreased -ve status effect by x turns
 stunned (if possible to implement): skip turn

'''
'''

armor break: decrease defence
'''


def poison(casterCharacter,targetCharacter, duration, magnitude):
    targetCharacter["status"]["poisoned"] = {
        "duration":duration,
        "magnitude":magnitude,
        }
    print(f"{casterCharacter['name']} used poison with power {magnitude} on {targetCharacter['name']} for {duration} turns!")

def daze(casterCharacter,targetCharacter, duration, magnitude):
    targetCharacter["status"]["dazed"] = {
        "duration":duration,
        "magnitude":magnitude,
    }
    print(f"{casterCharacter['name']} used daze of power {magnitude} on {targetCharacter['name']} for {duration} turns!")

def slow(casterCharacter,targetCharacter, duration, magnitude):
    targetCharacter["status"]["slowed"] = {
        "duration":duration,
        "magnitude":magnitude,
    }
    print(f"{casterCharacter['name']} used slow of power {magnitude} on {targetCharacter['name']} for {duration} turns!")

def focus(casterCharacter,targetCharacter, duration, magnitude):
    targetCharacter["status"]["focused"] = {
        "duration":duration,
        "magnitude":magnitude,
    }
    print(f"{casterCharacter['name']} used inner focus of power {magnitude} on {targetCharacter['name']} for {duration} turns!")

def empower(casterCharacter,targetCharacter, duration, magnitude):
    targetCharacter["status"]['empowered'] = {
        "duration":duration,
        "magnitude":magnitude,

    }
    print(f"{casterCharacter['name']} used empower of power {magnitude} on {targetCharacter['name']} for {duration} turns!")

def guard(casterCharacter,targetCharacter, duration, magnitude):
    targetCharacter["status"]['sturdy'] = {
        "duration":duration,
        "magnitude":magnitude,
    }
    print(f"{casterCharacter['name']} used guard of power {magnitude} on {targetCharacter['name']} for {duration} turns!")

def disarm(casterCharacter,targetCharacter, duration, magnitude):
    targetCharacter["status"]['disarmed'] = {
        "duration":duration,
        "magnitude":magnitude,
    }
    print(f"{casterCharacter['name']} used disarm of power {magnitude} on {targetCharacter['name']} for {duration} turns!")

def resist(casterCharacter,targetCharacter, duration, magnitude):
    targetCharacter["status"]['resistant'] = {
        "duration":duration,
        "magnitude":magnitude,
    }
    print(f"{casterCharacter['name']} used resist of power {magnitude} on {targetCharacter['name']} for {duration} turns!")

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