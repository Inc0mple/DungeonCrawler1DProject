# Dungeon Crawler Game

## Setup

### From Github

Download file and unzip. Run DungeonCrawler.py to start the game.

### From Repl.it

Click Run at the top of the page to start the game.

## Game Description (TODO)

### To do

Character save system using Firebase  
Status effects
Skills system  
smart enemy behvaiours  

### Objectives

### Controls

Controls: WASD. Press M to view map, I to access inventory and C to check player profile/stats.

### Features

### Tiles

- 'P': The player.
- '0': Impassable Wall.
- '&nbsp; ': Empty Space.
- 'C': Chest. Generates a random loot box for character upon walking on it after which it disappears.
- 'M': Merchant.Impassable. Buy and sell everything here.
- 'E': Exit. Move here with the key to win the game (or go to next level maybe? If that's ever implemented).
- 'K': Key. Required to exit the Dungeon.
- 'S': Slime: Weak but durable. Only drops torch fuel. 33 HP, 1-4 Atk. Easiest.
- 'G': Goblin: Typical enemy, variety of useful drops. 25 HP, 2-6 Atk. Easy.
- 'D': Dire Wolf: Glass cannon, low HP but high attack. Usually drops meat in form of food ration. 20 HP, 4-7 Atk, high dodge and accuracy. Medium.
- 'H': Hobgoblin: Strong version of goblin, fairly dangerous with good attack and defence. 40 HP, 4-8 Atk. Hard.
- 'R': Revenant: Strongest enemy,Dungeon Boss found blocking the exit. 50 HP 5-10 Attk. Very Hard.

### References

## Documentation (TODO)

### Imports

### Functions

## Video Demonstration (TODO)

## Notes

1D Project Brief:
<https://docs.google.com/document/d/14Yq8YuP0RxB080rZlBmDTTOS-8_ds3UmV0gc3L_Sv4s/edit>

Dungeon Crawler Game Tutorial:
<https://www.youtube.com/watch?v=G17XPI6t6kg>

Deliverables:

  1) Game description
  2) Code Documentation
  3) Code itself
  4) 3 minute video

### Map generator

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
