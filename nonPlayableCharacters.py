# Add new monsters/encounters here
nonPlayableCharacters = {
    "G": {
        "name": "Goblin",
        "health": {
            "max":25,
            "current":25
        },
        "attack":{
            "max":[2,6],
            "modifier":0,
            "current":[2,6],
        } ,
        "defence": {
            "max":0,
            "modifier":0,
            "current":0,
        },
        "speed": {
            "max":7,
            "modifier":0,
            "current":7,
        },
        "accuracy": {
            "max":75,
            "modifier":0,
            "current":75,
        },
        "dodge": {
            "max":9,
            "modifier":0,
            "current":9,
        },
        "status": {},
        "skills":{},
        "possible loot": {
            # Structured by loot and loot chance
            "small food ration":45,
            "small torch fuel":20,
            "food ration":10,
            "small health potion":20,
            "health potion":5,
            "dagger":50,
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
        "attack":{
            "max":[1,4],
            "modifier":0,
            "current":[1,4],
        } ,
        "defence": {
            "max":0,
            "modifier":0,
            "current":0,
        },
        "speed": {
            "max":4,
            "modifier":0,
            "current":4,
        },
        "accuracy": {
            "max":65,
            "modifier":0,
            "current":65,
        },
        "dodge": {
            "max":0,
            "modifier":0,
            "current":0,
        },
        "status": {},
        "skills":{},
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
        "attack":{
            "max":[4,7],
            "modifier":0,
            "current":[4,7],
        } ,
        "defence": {
            "max":0,
            "modifier":0,
            "current":0,
        },
        "speed": {
            "max":12,
            "current":12,
            "modifier":0,
        },
        "accuracy": {
            "max":85,
            "current":85,
            "modifier":0,
        },
        "dodge": {
            "max":16,
            "current":16,
            "modifier":0,
        },
        "status": {},
        "skills":{},
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
        "attack":{
            "max":[4,8],
            "modifier":0,
            "current":[4,8],
        } ,
        "defence": {
            "max":1,
            "modifier":0,
            "current":1,
        },
        "speed": {
            "max":10,
            "modifier":0,
            "current":10,
        },
        "accuracy": {
            "max":75,
            "modifier":0,
            "current":75,
            
        },
        "dodge": {
            "max":10,
            "modifier":0,
            "current":10, 
        },
        "status": {},
        "skills":{},
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
        "attack":{
            "max":[5,10],
            "modifier":0,
            "current":[5,10],
        } ,
        "defence": {
            "max":2,
            "modifier":0,
            "current":2,
        },
        "speed": {
            "max":8,
            "modifier":0,
            "current":8,
        },
        "accuracy": {
            "max":75,
            "modifier":0,
            "current":75,
        },
        "dodge": {
            "max":11,
            "modifier":0,
            "current":11,
        },
        "status": {},
        "skills":{},
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