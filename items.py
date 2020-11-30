weapon = {
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
    "empty": {
        "accuracy":0,
        "dodge":0,
        "speed":0
    },
    "bracelet of accuracy": {
        "accuracy":5,
        "dodge":0,
        "speed":0
    },
    "ring of speed": {
        "accuracy":0,
        "dodge":0,
        "speed":2
    },
    "focus shard": {
        "accuracy":25,
        "dodge":-5,
        "speed":-1
    },
    "gloves of haste": {
        "accuracy":-10,
        "dodge":5,
        "speed":5
    },
    "talisman of evasion": {
        "accuracy":0,
        "dodge":10,
        "speed":1
    },
    "cloak of darkness": {
        "accuracy":-15,
        "dodge":25,
        "speed":-1
    },
    "obfuscating shroud": {
        "accuracy":-55,
        "dodge":40,
        "speed":-3
    },
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
        "food": 9,
        "health": 2
    },
    "food ration": {
        "food": 18,
        "health": 3
    },
    "large food ration": {
        "food": 25,
        "health": 5
    },
}

priceSheet = {
    "weapon": {
        "dagger":50,
        "gladius":95,
        "short sword":105,
        "sword":140,
        "spear":190,
        "longsword":275,
        "halberd":275
    },
    "armor": {
        "leather armor":70,
        "chainmail":145,
        "scale armor":220,
        "plate armor":300,
        "dragonscale armor":400

    },
    "consumables": {
        "small torch fuel":30,
        "small food ration":45,
        "small health potion":50,
        "torch fuel":55,
        "food ration":85,
        "health potion":90,
        "large torch fuel":90,
        "large food ration":110,
        "large health potion":125
    },
    "trinket": {
        "bracelet of accuracy":55,
        "ring of speed":95,
        "focus shard":85,
        "gloves of haste":100,
        "cloak of darkness":120,
        "obfuscating shroud":185,
        "talisman of evasion":125,
    }

}