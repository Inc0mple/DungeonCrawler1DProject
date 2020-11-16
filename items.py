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