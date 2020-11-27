# Add new monsters/encounters here
nonPlayableCharacters = {
    "G": {
        "name": "Goblin",
        "health": {
            "max":25,
            "current":25
        },
        "attack": [2,6],
        "defence": 0,
        "speed": {
            "current":7,
            "max":7,
        },
        "accuracy": {
            "current":75,
            "max":75
        },
        "dodge": {
            "current":9,
            "max":9
        },
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
        "gold": [5,20],
        "intent": "hostile",
        "behaviour": "simple"
    },

    "S": {
        "name": "Slime",
        "health": {
            "max":33,
            "current":33
        },
        "attack": [1,4],
        "defence": 0,
        "speed": {
            "current":4,
            "max":4,
        },
        "accuracy": {
            "current":65,
            "max":65
        },
        "dodge": {
            "current":0,
            "max":0
        },
        "status": [],
        "possible loot": {
            "small torch fuel":50,
            "torch fuel":10,
            "large torch fuel":5,
            "small food ration":5,
            "small health potion":5
        },
        "gold": [3,15],
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
        "speed": {
            "current":12,
            "max":12,
        },
        "accuracy": {
            "current":85,
            "max":85
        },
        "dodge": {
            "current":16,
            "max":16
        },
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
        "speed": {
            "current":10,
            "max":10,
        },
        "accuracy": {
            "current":75,
            "max":75
        },
        "dodge": {
            "current":10,
            "max":10
        },
        "status": [],
        "possible loot": {
            "small food ration":95,
            "food ration":25,
            "small health potion":45,
            "health potion":25,
            "dagger":75,
            "leather armor":55,
            "chainmail":8,
            "gladius":10,
            "short sword":15,
            "spear":5,
        },
        "gold": [15,40],
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
        "speed": {
            "current":8,
            "max":8,
        },
        "accuracy": {
            "current":75,
            "max":75
        },
        "dodge": {
            "current":11,
            "max":11
        },
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
        "gold": [75,150],
        "intent": "hostile",
        "behaviour": "simple"
    }
    
}