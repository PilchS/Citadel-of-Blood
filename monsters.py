
import random
from helper_functions import roll_dice

MONSTER_CHARACTERISTICS = {
    "Chimaera": {"RV": 2, "NV": 7, "Treasure": "I", "Special": "Firebreath", "WP": 12, "CB": 2},
    "Cronks": {"RV": 1, "NV": 9, "Treasure": "E/B", "Special": "Stench", "WP": 8, "CB": 1},
    "Dire Wolves": {"RV": 1, "NV": 9, "Treasure": "A", "Special": None, "WP": 6, "CB": 1},
    "Evil Hero": {"RV": 2, "NV": 5, "Treasure": "J/C", "Special": None, "WP": 10, "CB": 3},
    "Evil Mage": {"RV": 3, "NV": 3, "Treasure": "J/C", "Special": None, "WP": 8, "CB": 2},
    "Gargoyle": {"RV": 3, "NV": 4, "Treasure": "G", "Special": None, "WP": 9, "CB": 2},
    "Harpies": {"RV": 1, "NV": 5, "Treasure": "A", "Special": None, "WP": 5, "CB": 1},
    "Medusa": {"RV": 2, "NV": 5, "Treasure": "G", "Special": "Flesh/Stone", "WP": 12, "CB": 3},
    "Minotaur": {"RV": 3, "NV": 7, "Treasure": "J/C", "Special": None, "WP": 15, "CB": 4},
    "Ogre": {"RV": 2, "NV": 2, "Treasure": "J/E", "Special": None, "WP": 14, "CB": 3},
    "Orcs": {"RV": 1, "NV": 0, "Treasure": "H/B", "Special": None, "WP": 6, "CB": 1},
    "Skeletons": {"RV": 1, "NV": 9, "Treasure": "F/A", "Special": None, "WP": 4, "CB": 1},
    "Troll": {"RV": 3, "NV": 4, "Treasure": "J", "Special": "Regenerate", "WP": 16, "CB": 4},
    "Vampire": {"RV": 4, "NV": 6, "Treasure": "J", "Special": "Charm", "WP": 12, "CB": 3},
    "Wargs": {"RV": 1, "NV": 6, "Treasure": "A", "Special": None, "WP": 7, "CB": 2},
    "Wight": {"RV": 2, "NV": 4, "Treasure": "H", "Special": None, "WP": 10, "CB": 2},
    "Wraiths": {"RV": 1, "NV": 2, "Treasure": "I/D", "Special": None, "WP": 8, "CB": 1}
}

ROOM_MONSTER_TABLE = [
    ["Evil Mage: 1", "Evil Hero: 1", "Cronks: 1D6", "Gargoyle: 1", "Chimaera: 1", "Medusa: 1"],
    ["Orcs: 1D3", "Troll: 1", "Vampire: 1", "Harpies: 1D3+2", "Ogre: 1", "Minotaur: 1"],
    ["Dire Wolves: 1D6", "Wight: 1", "Wargs: 1D3", "Evil Mage: 1", "Evil Hero: 1", "Cronks: 1D6+1"],
    ["Gargoyle: 2", "Chimaera: 2", "Medusa: 1", "Orcs: 1D6+1", "Harpies: 1D6", "Vampire: 1"],
    ["Harpies: 1D6+2", "Ogre: 2", "Minotaur: 1", "Dire Wolves: 1D6", "Wight: 2", "Wargs: 1D6"],
    ["Skeletons: 1D3", "Wraiths: 1D3", "Skeletons: 1D6", "Wraiths: 1D3+2", "Troll: 1", "Medusa: 1"]
]


WANDERING_MONSTER_TABLE = [
    ["Evil Hero: 1", "Evil Mage: 1", "Chimaera: 1"],
    ["Gargoyle: 1", "Medusa: 1", "Orcs: 1D3"],
    ["Troll: 1", "Vampire: 1", "Harpies: 1D3+2"],
    ["Ogre: 1", "Minotaur: 1", "Dire Wolves: 1D6"],
    ["Wight: 1", "Wargs: 1D3", "Wraiths: 1D3"],
    ["Vampire: 1", "Skeletons: 1D3", "Cronks: 1D6"]
]

def roll_monster(table):
    first_roll, second_roll = roll_dice(6, 2)

    first_roll = min(max(first_roll, 1), len(table))
    second_roll = min(max(second_roll, 1), len(table[first_roll - 1]))

    # Get monster information
    monster_info = table[first_roll - 1][second_roll - 1]
    name, count = parse_monster_count(monster_info)
    
    # Create the monster dictionary
    monster = {"Name": name, "Count": count, "WP": MONSTER_CHARACTERISTICS[name]["WP"] * count}
    monster.update(MONSTER_CHARACTERISTICS[name])

    # Assign default Treasure attribute if it doesn't exist
    monster["Treasure"] = MONSTER_CHARACTERISTICS[name].get("Treasure", "T1")  # Default to "T1"

    # Debug the generated monster
    print(f"DEBUG: Generated monster: {monster['Name']}, Count: {monster['Count']}, WP: {monster['WP']}, Treasure: {monster['Treasure']}")

    return monster




def parse_monster_count(monster_info):
    name, count = monster_info.split(": ")
    if "D" in count:
        dice, modifier = count.split("+") if "+" in count else (count, 0)
        rolls, sides = map(int, dice.split("D"))
        number = sum(roll_dice(sides, rolls)) + int(modifier)
    else:
        number = int(count)
    return name, number