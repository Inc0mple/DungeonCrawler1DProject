"""
F04 Group 2: Bryan Tan, Ryan Kaw Zheng Da, Colin Teoh, Xu Muzi, Joseph Lai
"""
classes = {
    "warrior": {
        "name": "Aragon",
        "class":"warrior",
        "health": {
            "max":50,
            "current":50
        },
        "attack": {
            "max":[4,6],
            "modifier":[0,0],
            "current":[4,6]
        },
        "defence": {
            "max":1,
            "modifier":0,
            "current":1
        },
        "speed": {
            "max":7,
            "modifier":0,
            "current":7
        },
        "accuracy": {
            "max":85,
            "modifier":0,
            "current":85
        },
        "dodge": {
            "max":10,
            "modifier":0,
            "current":10
        },
        "equipments": {
            "armor":"empty",
            "weapon":"empty",
            "trinket":"empty"
        },
        "status": {},
        "skills":{
            "guard": {
                "duration":4,
                "magnitude":1,
                "cooldown":7,
                "turnsTillReady":0,
            },
            "disarm": {
                "duration":4,
                "magnitude":1,
                "cooldown":7,
                "turnsTillReady":0,
            }
        },
        "inventory": [],
        "gold": 175,
        "torch":{
            "max":20,
            "current":15
        },
        "food": {
            "max":30,
            "current":30
        }
    },

    "ranger": {
        "name": "PlaceholderName",
        "class":"ranger",
        "health": {
            "max":40,
            "current":40
        },
        "attack": {
            "max":[3,6],
            "modifier":[0,0],
            "current":[3,6]
        },
        "defence": {
            "max":0,
            "modifier":0,
            "current":0
        },
        "speed": {
            "max":11,
            "modifier":0,
            "current":11
        },
        "accuracy": {
            "max":90,
            "modifier":0,
            "current":90
        },
        "dodge": {
            "max":20,
            "modifier":0,
            "current":20
        },
        "equipments": {
            "armor":"empty",
            "weapon":"empty",
            "trinket":"empty"
        },
        "status": {},
        "skills":{
            "poison": {
                "duration":5,
                "magnitude":2,
                "cooldown":6,
                "turnsTillReady":0,
            },
            "heighten senses": {
                "duration":4,
                "magnitude":2,
                "cooldown":4,
                "turnsTillReady":0,
            }
        },
        "inventory": [],
        "gold": 175,
        "torch":{
            "max":25,
            "current":20
        },
        "food": {
            "max":27,
            "current":27
        }
    },

    "beserker": {
        "name": "PlaceholderName",
        "class":"beserker",
        "health": {
            "max":45,
            "current":45
        },
        "attack": {
            "max":[3,9],
            "modifier":[0,0],
            "current":[3,9]
        },
        "defence": {
            "max":0,
            "modifier":0,
            "current":0
        },
        "speed": {
            "max":7,
            "modifier":0,
            "current":7
            
        },
        "accuracy": {
            "max":80,
            "modifier":0,
            "current":80
            
        },
        "dodge": {
            "max":10,
            "modifier":0,
            "current":10
            
        },
        "equipments": {
            "armor":"empty",
            "weapon":"empty",
            "trinket":"empty"
        },
        "status": {},
        "skills":{
            "empower": {
                "duration":5,
                "magnitude":1,
                "cooldown":5,
                "turnsTillReady":0,
            },
        },
        "inventory": [],
        "gold": 175,
        "torch":{
            "max":15,
            "current":15
        },
        "food": {
            "max":25,
            "current":25
        }
    },

    "survivalist": {
        "name": "PlaceholderName",
        "class":"survivalist",
        "health": {
            "max":55,
            "current":55
        },
        "attack": {
            "max":[3,5],
            "modifier":[0,0],
            "current":[3,5]
        },
        "defence": {
            "max":1,
            "modifier":0,
            "current":1
        } ,
        "speed": {
            "max":10,
            "modifier":0,
            "current":10
        },
        "accuracy": {
            "max":80,
            "modifier":0,
            "current":80
        },
        "dodge": {
            "max":13,
            "modifier":0,
            "current":13
        },
        "equipments": {
            "armor":"empty",
            "weapon":"empty",
            "trinket":"empty"
        },
        "status": {},
        "skills":{
            "daze": {
                "duration":4,
                "magnitude":4,
                "cooldown":3,
                "turnsTillReady":0,
            },
            "slow": {
                "duration":6,
                "magnitude":4,
                "cooldown":5,
                "turnsTillReady":0,
            }
        },
        "inventory": [],
        "gold": 175,
        "torch":{
            "max":30,
            "current":25
        },
        "food": {
            "max":35,
            "current":35
        }
    }

}

