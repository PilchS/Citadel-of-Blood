from heroes import HEROES, create_character_record, load_character_image
from monsters import MONSTER_CHARACTERISTICS, ROOM_MONSTER_TABLE, WANDERING_MONSTER_TABLE, roll_monster
from tables import TREASURE_TABLE, COMBAT_RESULTS_TABLE, BRIBERY_TABLE
from helper_functions import shuffle_and_pick, roll_dice
import random
import tkinter as tk
from PIL import ImageTk, Image
import os
import dungeon_gui
from tkinter import messagebox

IS_GUI_MODE = True

dungeon_data = None
tiles = None
tile_iterator = None


def roll_dice_expression(expression):
    try:
        if ":" in expression:
            prefix, dice_expr = expression.split(":")
            prefix = int(prefix)
            dice_result = roll_dice_expression(dice_expr)
            return prefix * dice_result

        if "x" in expression:
            multiplier_expr, dice_expr = expression.split("x")
            multiplier = roll_dice_expression(multiplier_expr) if "D" in multiplier_expr else int(multiplier_expr)
            dice_result = roll_dice_expression(dice_expr)
            return multiplier * dice_result

        parts = expression.split("D")
        if len(parts) == 2:
            dice_count = int(parts[0])
            sides = int(parts[1].split("+")[0]) if "+" in parts[1] else int(parts[1])
            modifier = int(parts[1].split("+")[1]) if "+" in parts[1] else 0

            rolls = [random.randint(1, sides) for _ in range(dice_count)]
            return sum(rolls) + modifier

        return int(expression)
    except Exception as e:
        raise ValueError(f"Invalid dice expression: {expression}") from e


def setup_initiates(gui_initiates=None):
    if gui_initiates:
        print("Setting up initiates from GUI...")
        return gui_initiates


def combat_sequence(party, monsters, combat_log=None):
    print("\nCombat Begins!")

    party = [character for character in party if character["WP"] > 0]

    def calculate_damage(attacker, weapon):
        roll = sum(roll_dice(6, 1)) + attacker.get("CB", 0)
        damage_table = COMBAT_RESULTS_TABLE.get(weapon, COMBAT_RESULTS_TABLE["Monster"])
        damage = damage_table[min(roll, len(damage_table)) - 1]
        return damage

    def attack(attacker, defender):
        max_wp = defender.get("Max WP", defender["WP"])
        weapon = attacker.get("Weapons", "Monster").split(", ")[0] if "Weapons" in attacker else "Monster"
        damage = calculate_damage(attacker, weapon)
        defender["WP"] -= damage
        combat_message = (
            f"{attacker['Name']} attacks {defender['Name']} with {weapon}. "
            f"Damage: {damage}, Remaining WP: {defender['WP']}/{max_wp}"
        )
        if combat_log:
            append_to_combat_log(combat_log, combat_message)
        print(combat_message)
        return defender["WP"] <= 0

    while party and monsters:
        if combat_log:
            append_to_combat_log(combat_log, "--- Party Turn ---")
        for character in party[:3]:
            if monsters:
                target = monsters[0]
                if attack(character, target):
                    if combat_log:
                        append_to_combat_log(combat_log, f"{target['Name']} is killed!")
                    monsters.pop(0)

        if combat_log:
            append_to_combat_log(combat_log, "--- Monster Turn ---")
        for monster in monsters[:3]:
            if party:
                target = party[0]
                if attack(monster, target):
                    if combat_log:
                        append_to_combat_log(combat_log, f"{target['Name']} is killed!")
                    party.pop(0)

        if not party:
            if combat_log:
                append_to_combat_log(combat_log, "The party has been defeated!")
            return False
        if not monsters:
            if combat_log:
                append_to_combat_log(combat_log, "All monsters have been defeated!")
            return True

    return True if party else False


def append_to_combat_log(combat_log, message):
    combat_log.config(state="normal")
    combat_log.insert(tk.END, message + "\n")
    combat_log.config(state="disabled")
    combat_log.see(tk.END)


def calculate_treasure(monsters, encounter_type="Room"):
    treasure_summary = {}
    for monster in monsters:
        treasure_type = monster.get("Treasure")
        if treasure_type:
            if "/" in treasure_type:
                treasure_type = treasure_type.split("/")[0] if encounter_type == "Room" else treasure_type.split("/")[1]

            if treasure_type in TREASURE_TABLE:
                treasure = TREASURE_TABLE[treasure_type]
                for item, value in treasure.items():
                    if value != "0:0":
                        rolled_value = roll_dice_expression(value)
                        treasure_summary[item] = treasure_summary.get(item, 0) + rolled_value
    return treasure_summary

def reorganize_party(party):
    print("\nReorganizing Party:")
    for i, character in enumerate(party):
        print(f"{i + 1}. {character['Name']} ({character['Race']}) {character['WP']}/{character['Max WP']}")
    print("Enter new positions by number (comma-separated for rows, e.g., 1,2,3|4,5,6):")
    try:
        positions = input("Reorganize: ").split("|")
        new_order = [party[int(p.strip()) - 1] for row in positions for p in row.split(",")]
        return new_order
    except (ValueError, IndexError):
        print("Invalid input, keeping current order.")
        return party

def reorganize_monsters(monsters):
    print("\nReorganizing Monsters:")
    for i, monster in enumerate(monsters):
        print(f"{i + 1}. {monster['Name']} {monster['WP']}/{monster.get('Max WP', monster['WP'])}")
    front_row = monsters[:3]
    back_row = monsters[3:]
    if back_row:
        front_row.append(back_row.pop(0))
    return front_row + back_row

def encounter_monster(room_visited, room_type):
    print("\nChecking for monsters...")
    roll = random.randint(1, 6)

    if room_visited:
        if roll == 1:
            print("Wandering Monster detected!")
            monsters = roll_monster(WANDERING_MONSTER_TABLE)
            resolve_encounter(monsters, encounter_type="Wandering")
    else:
        if room_type == "corridor" and roll == 1:
            print("Corridor Monster detected!")
            monsters = roll_monster(ROOM_MONSTER_TABLE)
            resolve_encounter(monsters, encounter_type="Room")
        elif room_type == "room" and roll in [1, 2, 3]:
            print("Room Monster detected!")
            monsters = roll_monster(ROOM_MONSTER_TABLE)
            resolve_encounter(monsters, encounter_type="Room")

def resolve_encounter(monsters, encounter_type):
    print(f"Encountered {len(monsters)} {monsters[0]['Name']} with {monsters[0]['WP']} WP each.")

    action = input("Choose action: Negotiate (n), Bribe (b), Fight (f): ").lower()

    if action == "n":
        negotiation_result = negotiate(monsters[0])
        if negotiation_result == "Agreement":
            print("The monster agrees to let the party pass.")
            return
        elif negotiation_result == "Intimidate":
            print("The monster is intimidated and leaves some treasure!")
            return
        else:
            print("Negotiation failed.")

    if action == "b":
        bribe_success = attempt_bribe(monsters)
        if bribe_success:
            print("The monster accepts the bribe and leaves the party.")
            return
        else:
            print("Bribe failed.")

    print("The party must fight the monster!")
    if combat_sequence(party, monsters):
        treasure = calculate_treasure(monsters, encounter_type)
        if treasure:
            print("\nTreasure collected:")
            for item, amount in treasure.items():
                print(f"{item}: {amount}")
        else:
            print("\nNo treasure found.")

def negotiate(monster):
    roll = sum(roll_dice(6, 2)) - monster["NV"]
    print(f"Negotiation roll: {roll}")

    if roll >= 10:
        return "Intimidate"
    elif roll >= 7:
        return "Agreement"
    else:
        return "Failure"

def attempt_bribe(monsters):
    offer = int(input("Enter Gold Marks offered: "))
    monster_strength = monsters[0]["WP"] + monsters[0]["NV"]

    for row in BRIBERY_TABLE:
        if offer >= row["Gold Marks"] and monster_strength in row["Range"]:
            roll = roll_dice(6)[0]
            return roll <= row["Roll"]

    return False

def main():
    if IS_GUI_MODE:
        print("Launching GUI mode...")
        dungeon_gui.root.mainloop()
        return

    print("Welcome to the Citadel Adventure Setup!")

    heroes = shuffle_and_pick(HEROES, 3)
    print("\nSelected Heroes:")
    for hero in heroes:
        print(f"- {hero['Name']} ({hero['Race']})")

    hero_records = [
        {
            "Name": hero["Name"],
            "Race": hero["Race"],
            "Weapons": hero["Weapons"],
            "Magical Potential": hero["MP"],
            "WP": hero["WP"],
            "Max WP": hero["WP"],
            "RV": hero["RV"],
            "CB": hero["CB"],
            "Skills": hero["Skill"],
            "Spells": [],
            "Magic Items": [],
            "Gold Marks": 0,
            "Jewels": 0,
            "Experience Points": 0,
        }
        for hero in heroes
    ]

    initiates = setup_initiates()

    global party
    party = hero_records + initiates

    print("\nOrganize your party before starting the adventure:")
    party = reorganize_party(party)


if __name__ == "__main__":
    main()

