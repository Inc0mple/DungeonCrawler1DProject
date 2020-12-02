# **Dungeon Crawler Game**
**Cohort 4 Groupt 2 Members**: Bryan, Ryan, Colin, Muzi, Joseph
## **Setup**

### **From [Github](https://github.com/Inc0mple/DungeonCrawler1DProject)**

Download file and unzip. Run DungeonCrawler.py to start the game.

### **From [Repl.it](https://repl.it/@BryanTan3/DungeonCrawler1DProject)**

Click Run at the top of the page to start the game.

## **Game Description**

### **Background of Genre**

Inspired by the popular fantasy roleplaying table top game of Dungeons and Dragons, Dungeon Crawlers
simulates the navigation of a dungeon in which the protagonist slays monsters and aquires loots in
an attempt to fulfil a certain objective (killing the main antagonist or escaping). The randomised
nature of each run via procedually generated map layouts, enemies and loot results in emergent
gameplay where the circumstance of each playthrough is fresh and unique. The potential for replayability
and relative simplicity of implementation (generally no need for fancy graphics or computations)
makes Dungeon Crawlers popular even among older systems.

### **Objectives**

The objective of this game is to find the dungeon key and escape from the dungeon in the least amount of
turns without dying from starvation or combat while carrying as much gold as possible. Players that escape
will be given a score that can be compared with others to determine whoever had the best playthroughs.

### **Controls**

Available actions are shown at all time during the game in the form \[key\:action\]. Type one of the keys and press enter to perform/select the corresponding action/choice. Inputs are always case insensitive. Press enter to continue whenever prompted.  

In general, the controls are as follows:

**General controls:**  

- **`1-9`** (or more) to choose from a list of available items/choices (Browsing shop, casting skills, using items etc.).  
- **`X`** to leave/go back from a menu if possible.  

**Map Controls:**  

- **`WASD`** to move up, right, down and left respectively.  
- **`M`** to view map  
- **`I`** to access inventory  
- **`E`** to check equipment  
- **`C`** to check player profile/stats  
- **`Q`** to quit.  

**Combat Controls:**  

- **`A`** to attack  
- **`W`** to wait  
- **`S`** to cast a skill  
- **`D`** to describe the enemy  
- **`I`** to access the inventory for using an item  
- **`E`** to check equipement to unequip  
- **`R`** to attempt to run away.

### **Attributes**

- **`Name`**: Character name  
- **`Class`**: Character class  
- **`Health`**: Player loses when current health reaches 0  
- **`Attack`**: Current attack determines raw damage dealt to enemies  
- **`Defence`**: Current defence negates incoming attack by a given amount  
- **`Speed`**: Affects dodge, determines turn order and chance to run away  
- **`Accuracy`**: Affects chance to hit enemies with attack. Hit chance is calculated as ((Your Speed-Enemy Speed) + ((Your Accuracy-Enemy Dodge)/Your Accuracy))%, with a minimum of 5%
- **`Dodge`**: Affects chance to completely negate damage from enemy attacks  
- **`Equipments`**: Shows currently equipped items in your various slots  
- **`Status`**: Shows status effects that are currently affecting the character  
- **`Skills`**: Shows skills that can be used in combat  
- **`Inventory`**:  Shows items currently in the inventory  
- **`Gold`**: Can be spent on equipments and consumables when trading with merchants. Also determines final score  
- **`Torch`**: Determines how far you can reveal the tiles around you as you traverse the Dungeon. Reaching 0 prevents the revealing of adjacent tile  
- **`Food`**: High food levels allow for regeneration of health when moving across the map. Reaching 0 food results in starvation which causes health to degenerate instead  

### **Map Tiles**

- `P`: The player.
- `0`: Impassable Wall.
- '&nbsp;' : Empty Space.
- `C`: Chest. Generates a random loot box for the player upon walking on it, after which it disappears.
- `M`: Merchant.Impassable. Buy and sell everything here.
- `E`: Exit. Move here with the key to win the game (or go to next level maybe? If that's ever implemented).
- `K`: Key. Required to exit the Dungeon.
- `S`: Slime: Weak but durable. Only drops torch fuel. 33 Health, 1-4 Attack. Easiest.
- `G`: Goblin: Typical enemy, variety of useful drops. 25 Health, 2-6 Attack. Easy.
- `D`: Dire Wolf: Glass cannon, low Health but high attack. Usually drops meat in form of food ration. 20 Health, 4-7 Attack, high dodge and accuracy. Medium.
- `H`: Hobgoblin: Strong version of goblin, fairly dangerous with good attack and defence. 40 Health, 4-8 Attack. Hard.
- `R`: Revenant: Strongest enemy,Dungeon Boss found blocking the exit. 50 Health 5-10 Attack. Very Hard.

### **Items**

#### **Weapons**

- `empty`: +0-0 Attack
- `dagger`: +1-1 Attack
- `gladius`: +2-1 Attack
- `short sword`: +1-3 Attack
- `sword`: +2-3 Attack
- `spear`: +1-5 Attack
- `halberd`: +2-6 Attack
- `longsword`: +3-5 Attack

#### **Armor**

- `empty`: +0 Defence
- `leather armor`: +1 Defence
- `chainmail`: +2 Defence
- `scale armor`: +3 Defence
- `plate armor`: +4 Defence
- `dragonscale armor`: +5 Defence

#### **Trinket**

- `empty`: No effect
- `bracelet of accuracy`: +5 Accuracy
- `ring of speed`: +2 Speed
- `focus shard`: +25 Accuracy, -5 Dodge, -1 Speed
- `gloves of haste`: +5 Dodge, +5 Speed, -10 Accuracy
- `talisman of evasion`: +10 Dodge, +1 Speed
- `cloak of darkness`: +25 Dodge, -15 Accuracy, -1 Speed
- `obfuscating shroud`: +40 Dodge, -25 Accuracy, -3 Speed

#### **Consumables**

Amount restored depends on size of consumable (Small/Normal/Large)  

- `Health Potion`: Restores 15/25/35 health
- `Torch Fuel`: Restores 5/10/20 torch
- `Food Ration`: Restores 9/18/25 food and 2/3/5 health

#### **Special**

The `Dungeon Key` is a unique item that cannot be used on the map or during combat. Having it in your inventory is a requirement for exiting the Dungeon to win the game.

### **Map Loot (Chest)**

Walking over the `C` tile on the map will cause the player to receive one of the following loot set (with equal chances for each set):

- `Treasure Chest`: High amount of gold, with the potential to provide a large variety of items  
- `Box of Supplies`: Usually contains consumables like health potions, food and torch fuel.  
- `Caverneer's Stash`: Almost always contains torch fuel, with a small chance of containing trinkets  
- `Box of equipment`: Often contains at least one low-level equipment, with a small chance of containing equipments in greater qualities/quantities
- `Potion Pouch`: High chance of containing health potions  

### **Classes**  

- `Warrior`: Good all-rounder. Can use Guard and Disarm.
- `Ranger`: Dextrous at the sacrifice of power and durability. Casts Poison and Inner Focus.
- `Beserker`: Powerful in combat but neglects defences and supplies. Can use Empower.
- `Survivalist`: Durable and starts with more supplies. Can Daze and Slow.

### **Skills**  

Can be used in combat, with different classes having different skills.

- `Poison`: Poisons target, removing health each turn.
- `Daze`: Dazes target, decreasing accuracy of target.
- `Slow`: Slows target, decreasing dodge and speed of target.
- `Heighten Senses`: Heighten senses of target, increasing target accuracy and dodge.
- `Empower`: Empowers target, increasing attack
- `Guard`: Guards target, increasing defence.
- `Disarm`: Disarms target, decreasing attack.

### **References**

Hit chance formula modified from: <https://www.gamedev.net/forums/topic/685930-the-simplest-but-most-effective-and-intuitive-way-to-implement-accuracy-and-dodge-chance-in-an-rpg>  
Basic map movement and updating learnt from: <https://www.youtube.com/watch?v=G17XPI6t6kg>

## **Documentation**

### **Imports**

#### **Python modules:**

    import math
    from colorama import Fore, Style, Back
    from random import randint, choice
    from copy import deepcopy, copy
    from time import sleep

**Rationale:**  

- `math`, `randint` and `choice` are used whenever to calculate chance of events, from attack damage to loot received.
- `Fore` and `Style` from `colorama` are used to enhance visual experience, increase readiblity and provide a sense of reward/danger during positive/negative events. This is important especially in the absence of any other visual libraries.

#### **Custom modules:**  

    from mapLoot import mapLoot
    from classes import classes
    from maps import maps
    from nonPlayableCharacters import nonPlayableCharacters
    from items import weapon,armor,trinket,consumables,priceSheet
    from statusSkill import *

**Rationale:** We created and imported variables and functions from other files in the game folder to allow for seperation of concerns and to prevent clutter in the main game file due to their heavy nesting/occuying a large space. It also allows for easy editing and referencing of variables.

### **Functions**

`printMap`

## **Video Demonstration (TODO)**

## **Notes**

1D Project Brief:
<https://docs.google.com/document/d/14Yq8YuP0RxB080rZlBmDTTOS-8_ds3UmV0gc3L_Sv4s/edit>

Dungeon Crawler Game Tutorial:


Deliverables:

  1) Game description
  2) Code Documentation
  3) Code itself
  4) 3 minute video

### **Map generator**

1. Make a function, generateMap(x,y), that takes in 2 arguements which will determine the size of the map (Maybe reject if area is below certain number). Maybe try 20x20 first?
2. Function returns a list of list. eg:  
[  
["0", "0", "0", "0", "0"],  
["0", "P", "0", "E", "0"],  
["0", " ", "K", "R", "0"],  
["0", "0", "0", "0", "0"],  
]  

3. The generated map would probably have the following features:

- Initial Room (Must spawn a room with a 'P', the player).
- One room with a Dungeon key 'K' that is blocked by medium-hard monster.
- One room with exit blocked by 'R' (the dungeon boss).
- At least one room with a merchant.
- A couple of 'loot rooms' with a chest/chests that is often, but not always, blocked by a monster.
- Corridors joining rooms that very occasionally has weak enemies blocking it.

### Future ideas

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
torch radius system

player stats ideas:
attack, defence,speed,vision,dodge,accuracy

item ideas:
torch fuel -> refuel torch when used
health potion -> restore 20 health
glow ring trinket -> increase light radius, if not acts as permanent torch (Idk how to implement scaling light radius yet tho)
some powerup that permanently increases a stat when used? (also a version that increases stat temporarily...idk how to implement yet )
