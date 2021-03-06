"""
F04 Group 2: Bryan Tan, Ryan Kaw Zheng Da, Colin Teoh, Xu Muzi, Joseph Lai
"""
from colorama import Fore, Style, Back
maps = {
    "normal" : [
["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
["0", f"{Fore.GREEN}P{Style.RESET_ALL}", " ", "G", "0", "G", "C", "0", "E", "0"],
["0", " ", " ", " ", "0", " ", "0", " ", "R", "0"],
["0", " ", "S", " ", "G", " ", "S", "S", " ", "0"],
["0", "G", "0", "G", "C", "0", " ", " ", "H", "0"],
["0", "C", "0", " ", "M", "0", " ", "D", " ", "0"],
["0", " ", " ", "G", "S", " ", "G", " ", "0", "0"],
["0", " ", "0", "0", "K", "D", " ", "H", "H", "0"],
["0", "H", "C", "S", " ", "C", "0", "C", "C", "0"],
["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
],

    "hard" : [
["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
["0", f"{Fore.GREEN}P{Style.RESET_ALL}", " ", "0", "D", "S", "0", "C", "M", "0", "K", "0"],
["0", " ", " ", " ", " ", " ", " ", "G", " ", "D", " ", "0"],
["0", " ", " ", "S", "0", "0", "0", " ", " ", "0", "G", "0"],
["0", " ", "G", " ", "G", "0", " ", " ", "S", "0", " ", "0"],
["0", "S", " ", " ", " ", "C", " ", "0", " ", "S", " ", "0"],
["0", " ", "0", "0", " ", " ", " ", " ", " ", "C", " ", "0"],
["0", "C", "0", "C", "D", "0", "G", " ", "S", "0", "H", "0"],
["0", "M", "0", "0", "0", "0", "0", "0", " ", "D", " ", "0"],
["0", "C", "D", " ", " ", " ", "0", "C", "S", "C", "S", "0"],
["0", "G", "0", "0", "0", " ", "G", "H", " ", " ", " ", "0"],
["0", "C", "H", " ", "S", "S", "C", "S", "G", "M", " ", "0"],
["0", "0", "0", " ", "C", " ", " ", " ", " ", "0", " ", "0"],
["0", "E", "R", "D", "0", " ", "0", "H", " ", "0", "D", "0"],
["0", "0", "H", " ", "0", "C", "0", "C", " ", "0", "C", "0"],
["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
],


}

testMap = [
["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
["0", f"{Fore.GREEN}P{Style.RESET_ALL}", " ", "G", "0", " ", " ", " ", " ", "0"],
["0", " ", "K", " ", "0", " ", "0", " ", " ", "0"],
["0", "C", "S", " ", " ", " ", " ", " ", " ", "0"],
["0", "C", "0", "G", " ", "0", " ", " ", " ", "0"],
["0", "C", "0", " ", " ", "0", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", "0", "0", " ", " ", " ", " ", " ", "0"],
["0", "H", " ", "S", " ", " ", "0", " ", "G", "E"],
["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
]

testMap2 = [
["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
["0", "{Fore.GREEN}P{Style.RESET_ALL}", " ", "0", "D", "S", "0", "C", "0", "0", "K", "0"],
["0", " ", " ", " ", " ", " ", " ", "G", " ", "D", " ", "0"],
["0", " ", " ", "S", "0", "0", "0", " ", " ", "0", "G", "0"],
["0", " ", "G", " ", "G", "0", " ", " ", "S", "0", " ", "0"],
["0", "S", " ", " ", " ", "C", " ", "0", " ", "S", " ", "0"],
["0", " ", "0", "0", " ", " ", " ", " ", " ", "C", " ", "0"],
["0", "C", "0", "C", "D", "0", "G", " ", "S", "0", "H", "0"],
["0", "0", "0", "0", "0", "0", "0", "0", " ", "D", " ", "0"],
["0", "C", "D", " ", " ", " ", "0", "C", "S", "C", "S", "0"],
["0", "G", "0", "0", "0", " ", "G", "H", " ", " ", " ", "0"],
["0", "C", "H", " ", "S", "S", "C", "S", "G", "0", " ", "0"],
["0", "0", "0", " ", "C", " ", " ", " ", " ", "0", " ", "0"],
["0", "E", "R", "D", "0", " ", "0", "H", " ", "0", "D", "0"],
["0", "0", "H", " ", "0", "C", "0", "C", " ", "0", "C", "0"],
["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
]
hard = [
["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
["0", f"{Fore.GREEN}P{Style.RESET_ALL}", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
],

testMap3 = [
["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
["0", "{Fore.GREEN}P{Style.RESET_ALL}", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "0"],
["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
]

[
["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
["0", "{Fore.GREEN}P{Style.RESET_ALL}", " ", "G", "0", "G", "C", "0", "E", "0"],
["0", " ", " ", " ", "0", " ", "0", " ", "R", "0"],
["0", " ", "S", " ", "G", " ", "S", "S", " ", "0"],
["0", "G", "0", "G", "C", "0", " ", " ", "H", "0"],
["0", "C", "0", " ", "M", "0", " ", "D", " ", "0"],
["0", " ", " ", "G", "S", " ", "G", " ", "0", "0"],
["0", " ", "0", "0", "K", "D", " ", "H", "H", "0"],
["0", "H", "C", "S", " ", "C", "0", "C", "C", "0"],
["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
]