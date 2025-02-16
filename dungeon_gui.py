import tkinter as tk
from tkinter import Toplevel, Label, Button, Entry, messagebox
from PIL import Image, ImageTk
import random
from dungeon_creator import create_dungeon
from dungeon_visualizer import load_tiles, draw_dungeon_visualization
from heroes import HEROES
from monsters import MONSTER_CHARACTERISTICS, ROOM_MONSTER_TABLE, roll_monster
from player_movement import Player
from main import setup_initiates, combat_sequence, append_to_combat_log
import os
from helper_functions import roll_dice
from tables import BRIBERY_TABLE, COMBAT_RESULTS_TABLE, TREASURE_TABLE
from save_load import save_game, load_game

party = []
dungeon_data = {}
tiles = {}
player = Player()
revealed_tiles = set()
monsters_in_rooms = {}
movement_buttons = {}
party_gold = 1000
gold_label = None
spawned_monsters = {}

MONSTER_GOLD_REWARDS = {
    "Chimaera": {
        "visited": {"threshold": -1, "max_roll": 0, "multiplier": 0},
        "nonvisited": {"threshold": -1, "max_roll": 0, "multiplier": 0},
    },
    "Cronks": {
        "visited": {"threshold": 2, "max_roll": 6, "multiplier": 10},
        "nonvisited": {"threshold": 6, "max_roll": 6, "multiplier": 1},
    },
    "Dire Wolves": {
        "visited": {"threshold": -1, "max_roll": 0, "multiplier": 0},
        "nonvisited": {"threshold": -1, "max_roll": 0, "multiplier": 0},
    },
    "Evil Hero": {
        "visited": {"threshold": 6, "max_roll": 6, "multiplier": 20},
        "nonvisited": {"threshold": 6, "max_roll": 6, "multiplier": 20},
    },
    "Evil Mage": {
        "visited": {"threshold": 6, "max_roll": 6, "multiplier": 20},
        "nonvisited": {"threshold": 6, "max_roll": 6, "multiplier": 20},
    },
    "Gargoyle": {
        "visited": {"threshold": 6, "max_roll": 18, "multiplier": 5},
        "nonvisited": {"threshold": 6, "max_roll": 18, "multiplier": 5},
    },
    "Harpies": {
        "visited": {"threshold": -1, "max_roll": 0, "multiplier": 0},
        "nonvisited": {"threshold": -1, "max_roll": 0, "multiplier": 0},
    },
    "Medusa": {
        "visited": {"threshold": 6, "max_roll": 18, "multiplier": 5},
        "nonvisited": {"threshold": 6, "max_roll": 18, "multiplier": 5},
    },
    "Minotaur": {
        "visited": {"threshold": 6, "max_roll": 6, "multiplier": 20},
        "nonvisited": {"threshold": 6, "max_roll": 6, "multiplier": 20},
    },
    "Ogre": {
        "visited": {"threshold": 6, "max_roll": 6, "multiplier": 20},
        "nonvisited": {"threshold": 2, "max_roll": 6, "multiplier": 10},
    },
    "Orcs": {
        "visited": {"threshold": 1, "max_roll": 3, "multiplier": 1},
        "nonvisited": {"threshold": 6, "max_roll": 6, "multiplier": 1},
    },
    "Skeletons": {
        "visited": {"threshold": 1, "max_roll": 3, "multiplier": 1},
        "nonvisited": {"threshold": 3, "max_roll": 6, "multiplier": 1},
    },
    "Troll": {
        "visited": {"threshold": 6, "max_roll": 6, "multiplier": 20},
        "nonvisited": {"threshold": 6, "max_roll": 6, "multiplier": 20},
    },
    "Vampire": {
        "visited": {"threshold": 6, "max_roll": 6, "multiplier": 20},
        "nonvisited": {"threshold": 6, "max_roll": 6, "multiplier": 20},
    },
    "Wargs": {
        "visited": {"threshold": -1, "max_roll": 0, "multiplier": 0},
        "nonvisited": {"threshold": -1, "max_roll": 0, "multiplier": 0},
    },
    "Wight": {
        "visited": {"threshold": 1, "max_roll": 3, "multiplier": 1},
        "nonvisited": {"threshold": 1, "max_roll": 3, "multiplier": 1},
    },
    "Wraiths": {
        "visited": {"threshold": 6, "max_roll": 6, "multiplier": 5},
        "nonvisited": {"threshold": 1, "max_roll": 18, "multiplier": 1},
    }
}

MONSTER_JEWELS_TABLE = {
    "Chimaera": {
        "visited": {"threshold": 2, "max_roll": 6},
        "nonvisited": {"threshold": 2, "max_roll": 6},
    },
    "Cronks": {
        "visited": {"threshold": 2, "max_roll": 6},
        "nonvisited": {"threshold": -1, "max_roll": 0},
    },
    "Dire Wolves": {
        "visited": {"threshold": -1, "max_roll": 0},
        "nonvisited": {"threshold": -1, "max_roll": 0},
    },
    "Evil Hero": {
        "visited": {"threshold": 2, "max_roll": 6},
        "nonvisited": {"threshold": -1, "max_roll": 0},
    },
    "Evil Mage": {
        "visited": {"threshold": 2, "max_roll": 6},
        "nonvisited": {"threshold": -1, "max_roll": 0},
    },
    "Gargoyle": {
        "visited": {"threshold": 3, "max_roll": 6},
        "nonvisited": {"threshold": 3, "max_roll": 6},
    },
    "Harpies": {
        "visited": {"threshold": -1, "max_roll": 0},
        "nonvisited": {"threshold": -1, "max_roll": 0},
    },
    "Medusa": {
        "visited": {"threshold": 3, "max_roll": 6},
        "nonvisited": {"threshold": 3, "max_roll": 6},
    },
    "Minotaur": {
        "visited": {"threshold": 2, "max_roll": 6},
        "nonvisited": {"threshold": -1, "max_roll": 0},
    },
    "Ogre": {
        "visited": {"threshold": 2, "max_roll": 6},
        "nonvisited": {"threshold": 2, "max_roll": 6},
    },
    "Orcs": {
        "visited": {"threshold": 1, "max_roll": 3},
        "nonvisited": {"threshold": -1, "max_roll": 0},
    },
    "Skeletons": {
        "visited": {"threshold": 3, "max_roll": 6},
        "nonvisited": {"threshold": -1, "max_roll": 0},
    },
    "Troll": {
        "visited": {"threshold": 2, "max_roll": 6},
        "nonvisited": {"threshold": 2, "max_roll": 6},
    },
    "Vampire": {
        "visited": {"threshold": 2, "max_roll": 6},
        "nonvisited": {"threshold": 2, "max_roll": 6},
    },
    "Wargs": {
        "visited": {"threshold": -1, "max_roll": 0},
        "nonvisited": {"threshold": -1, "max_roll": 0},
    },
    "Wight": {
        "visited": {"threshold": 1, "max_roll": 3},
        "nonvisited": {"threshold": 1, "max_roll": 3},
    },
    "Wraiths": {
        "visited": {"threshold": 2, "max_roll": 6},
        "nonvisited": {"threshold": 1, "max_roll": 3},
    },
}

JEWELS_TABLE = {
    "2": "1",
    "3": "5",
    "4": "10",
    "5": "15",
    "6": "20",
    "7": "25",
    "8": "35",
    "9": "50",
    "10": "75",
    "11": "100",
    "12": "150",
}
class EnhancedPlayer(Player):
    def get_neighbors(self):
        return self.connected_tiles.get(self.position, [])

player = EnhancedPlayer()

def start_game():
    global gold_label
    main_menu.pack_forget()
    setup_party()

    gold_label_frame = tk.Frame(root, bg="#333")
    gold_label_frame.pack(side=tk.TOP, fill=tk.X)

    gold_label = tk.Label(
        gold_label_frame,
        text=f"Total Gold: {party_gold} Gold Marks",
        font=("Arial", 16),
        fg="white",
        bg="#333",
        anchor="w",
    )
    gold_label.pack(pady=5, padx=10)
    add_save_button(gold_label_frame)

def add_character_card_button(root, party, dungeon_canvas):
    button_frame = tk.Frame(dungeon_canvas, bg="#333")
    button_frame.pack(side=tk.BOTTOM, pady=10)
    
    Button(button_frame, text="Character Cards", command=lambda: show_character_selection_window(party),
           bg="#555", fg="white", width=20).pack(pady=10)
def show_character_selection_window(party):
    selection_window = Toplevel()
    selection_window.title("Character Selection")
    selection_window.geometry("300x400")
    selection_window.configure(bg="#333")
    
    Label(selection_window, text="Select a Character", font=("Arial", 14), fg="white", bg="#333").pack(pady=10)
    
    for hero in party:
        Button(selection_window, text=hero['Name'], command=lambda h=hero: show_character_card(h),
               bg="#555", fg="white", width=20).pack(pady=5)
    
    Button(selection_window, text="Close", command=selection_window.destroy, bg="#555", fg="white").pack(pady=20)

def show_character_card(hero):
    def save_changes():
        try:
            hero['WP'] = int(wp_entry.get())
            hero['Magical Potential'] = int(mp_entry.get())
            hero['RV'] = int(rv_entry.get())
            hero['CB'] = int(cb_entry.get())
            hero['Weapons'] = weapons_entry.get()
            hero['Weapon Skill'] = weapon_skill_entry.get()
            hero['Skill'] = skill_entry.get()
            card_window.destroy()
        except ValueError:
            Label(card_window, text="Invalid input! Ensure numbers are used where required.", fg="red", bg="#333").pack()

    card_window = Toplevel()
    card_window.title(f"{hero['Name']}'s Character Card")
    card_window.geometry("400x500")
    card_window.configure(bg="#333")

    Label(card_window, text=f"Name: {hero['Name']}", font=("Arial", 14), fg="white", bg="#333").pack(pady=5)
    Label(card_window, text=f"Race: {hero['Race']}", font=("Arial", 14), fg="white", bg="#333").pack(pady=5)
    
    Label(card_window, text="WP:", fg="white", bg="#333").pack()
    wp_entry = Entry(card_window, bg="#555", fg="white")
    wp_entry.insert(0, hero['WP'])
    wp_entry.pack()
    
    Label(card_window, text="Magical Potential:", fg="white", bg="#333").pack()
    mp_entry = Entry(card_window, bg="#555", fg="white")
    mp_entry.insert(0, hero.get('Magical Potential', 0))
    mp_entry.pack()
    
    Label(card_window, text="Resistance Value:", fg="white", bg="#333").pack()
    rv_entry = Entry(card_window, bg="#555", fg="white")
    rv_entry.insert(0, hero['RV'])
    rv_entry.pack()
    
    Label(card_window, text="Combat Bonus:", fg="white", bg="#333").pack()
    cb_entry = Entry(card_window, bg="#555", fg="white")
    cb_entry.insert(0, hero['CB'])
    cb_entry.pack()
    
    Label(card_window, text="Weapons:", fg="white", bg="#333").pack()
    weapons_entry = Entry(card_window, bg="#555", fg="white")
    weapons_entry.insert(0, hero['Weapons'])
    weapons_entry.pack()
    
    Label(card_window, text="Weapon Skill:", fg="white", bg="#333").pack()
    weapon_skill_entry = Entry(card_window, bg="#555", fg="white")
    weapon_skill_entry.insert(0, hero.get('Weapon Skill', 'N/A'))
    weapon_skill_entry.pack()
    
    Label(card_window, text="Skill:", fg="white", bg="#333").pack()
    skill_entry = Entry(card_window, bg="#555", fg="white")
    skill_entry.insert(0, hero.get('Skill', 'N/A'))
    skill_entry.pack()
    
    Button(card_window, text="Save Changes", command=save_changes, bg="#555", fg="white").pack(pady=10)
    Button(card_window, text="Close", command=card_window.destroy, bg="#555", fg="white").pack(pady=10)

def setup_party():
    setup_frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(setup_frame, text="Your Party", font=("Arial", 16), fg="white", bg="#333").pack()

    selected_heroes = random.sample(HEROES, 3)
    for hero in selected_heroes:
        party.append(hero)
        tk.Label(setup_frame, text=f"{hero['Name']} ({hero['Race']}) - WP: {hero['WP']}", fg="white", bg="#333").pack()

    if gold_label:
        gold_label.pack_forget()

    create_initiates_button = tk.Button(
        setup_frame,
        text="Create Initiates",
        command=create_initiates,
        bg="#555",
        fg="white",
        font=("Arial", 14),
    )
    create_initiates_button.pack(side=tk.BOTTOM, pady=10, padx=10)
    create_initiates_button.place(relx=0.5, rely=1.0, anchor="s")

    add_character_card_button(root, party, dungeon_canvas)


def create_initiates():
    setup_frame.pack_forget()
    initiate_frame.pack(fill=tk.BOTH, expand=True)

    def save_initiates():
        for i in range(3):
            name = name_entries[i].get()
            race = race_vars[i].get()
            primary_weapon = primary_weapon_vars[i].get()
            secondary_weapon = secondary_weapon_vars[i].get()
            magic_potential = magic_potential_vars[i].get()

            if race not in ["Elf", "Dwarf", "Human"]:
                messagebox.showerror("Error", "Invalid race selected.")
                return

            initiate = {
                "Name": name,
                "Race": race,
                "WP": 5,
                "Max WP": 5,
                "Weapons": f"{primary_weapon}, {secondary_weapon}",
                "RV": 2,
                "CB": 0,
                "Magical Potential": magic_potential
            }
            party.append(initiate)

        setup_initiates(party)
        initiate_frame.pack_forget()
        reorganize_party()

    tk.Label(initiate_frame, text="Create Initiates", font=("Arial", 16), fg="white", bg="#333").pack()

    name_entries = []
    race_vars = []
    primary_weapon_vars = []
    secondary_weapon_vars = []
    magic_potential_vars = []

    weapons = ["Sword", "Dagger", "Bow", "Ax", "Throw Dagger"]
    magic_potentials = ["0", "1", "2"]

    columns = [tk.Frame(initiate_frame, bg="#333") for _ in range(3)]
    for col in columns:
        col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    for i in range(3):
        tk.Label(columns[i], text=f"Initiate {i + 1}", font=("Arial", 14), fg="white", bg="#333").pack(anchor="w")

        name_label = tk.Label(columns[i], text="Name:", fg="white", bg="#333")
        name_label.pack(anchor="w")
        name_entry = tk.Entry(columns[i], bg="#555", fg="white")
        name_entry.pack(anchor="w")
        name_entries.append(name_entry)

        race_label = tk.Label(columns[i], text="Race:", fg="white", bg="#333")
        race_label.pack(anchor="w")
        race_var = tk.StringVar(value="Human")
        tk.OptionMenu(columns[i], race_var, "Elf", "Dwarf", "Human").pack(anchor="w")
        race_vars.append(race_var)

        primary_weapon_label = tk.Label(columns[i], text="Primary Weapon:", fg="white", bg="#333")
        primary_weapon_label.pack(anchor="w")
        primary_weapon_var = tk.StringVar(value=weapons[0])
        tk.OptionMenu(columns[i], primary_weapon_var, *weapons).pack(anchor="w")
        primary_weapon_vars.append(primary_weapon_var)

        secondary_weapon_label = tk.Label(columns[i], text="Secondary Weapon:", fg="white", bg="#333")
        secondary_weapon_label.pack(anchor="w")
        secondary_weapon_var = tk.StringVar(value=weapons[1])
        tk.OptionMenu(columns[i], secondary_weapon_var, *weapons).pack(anchor="w")
        secondary_weapon_vars.append(primary_weapon_var)

        magic_potential_label = tk.Label(columns[i], text="Magic Potential:", fg="white", bg="#333")
        magic_potential_label.pack(anchor="w")
        magic_potential_var = tk.StringVar(value=magic_potentials[0])
        tk.OptionMenu(columns[i], magic_potential_var, *magic_potentials).pack(anchor="w")
        magic_potential_vars.append(magic_potential_var)

    save_button = tk.Button(initiate_frame, text="Save Initiates", command=save_initiates, bg="#555", fg="white", font=("Arial", 14))
    save_button.pack(side=tk.BOTTOM, pady=10, padx=10)
    save_button.place(relx=0.5, rely=1.0, anchor="s")

def reorganize_party():
    reorganize_frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(reorganize_frame, text="Reorganize Your Party", font=("Arial", 16), fg="white", bg="#333").pack()

    party_canvas = tk.Canvas(reorganize_frame, bg="#222", highlightthickness=0)
    party_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    selected_index = tk.IntVar(value=-1)

    def update_canvas():
        party_canvas.delete("all")
        row_length = 3
        member_width = 200
        member_height = 50
        padding = 10

        for i, member in enumerate(party):
            member["Max WP"] = member.get("Max WP", member["WP"])
            member_str = f"{member['Name']} ({member['Race']}) - WP: {member['WP']}/{member['Max WP']}"

            row = i // row_length
            col = i % row_length
            x0 = col * (member_width + padding)
            y0 = row * (member_height + padding)
            x1 = x0 + member_width
            y1 = y0 + member_height

            if i == selected_index.get():
                party_canvas.create_rectangle(x0, y0, x1, y1, fill="#555", outline="white", width=2)
            else:
                party_canvas.create_rectangle(x0, y0, x1, y1, fill="#333", outline="white", width=2)

            party_canvas.create_text(
                (x0 + x1) / 2, (y0 + y1) / 2,
                text=member_str,
                fill="white",
                font=("Arial", 12),
                anchor="center"
            )

    def on_canvas_click(event):
        row_length = 3
        member_width = 200
        member_height = 50
        padding = 10

        col = event.x // (member_width + padding)
        row = event.y // (member_height + padding)
        member_index = row * row_length + col

        if member_index < len(party):
            selected_index.set(member_index)
            update_canvas()

    party_canvas.bind("<Button-1>", on_canvas_click)

    party_canvas.config(cursor="hand2")

    update_canvas()

    def move_up():
        idx = selected_index.get()
        if idx > 0:
            party[idx - 1], party[idx] = party[idx], party[idx - 1]
            update_canvas()
            selected_index.set(idx - 1)

    def move_down():
        idx = selected_index.get()
        if idx < len(party) - 1:
            party[idx + 1], party[idx] = party[idx], party[idx + 1]
            update_canvas()
            selected_index.set(idx + 1)

    button_frame = tk.Frame(reorganize_frame, bg="#333")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Move Up", command=move_up, bg="#555", fg="white").grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="Move Down", command=move_down, bg="#555", fg="white").grid(row=0, column=1, padx=5)

    def finalize_party():
        reorganize_frame.pack_forget()
        start_dungeon()

    tk.Button(reorganize_frame, text="Finalize", command=finalize_party, bg="#555", fg="white").pack(pady=10)

def check_and_spawn_monster(player_position):
    global monsters_in_rooms, spawned_monsters
    adjacent_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dx, dy in adjacent_directions:
        adjacent_tile = (player_position[0] + dx, player_position[1] + dy)

        if adjacent_tile in dungeon_data and adjacent_tile in revealed_tiles:
            tile_data = dungeon_data[adjacent_tile]
            tile_type = tile_data["type"]
            visited = adjacent_tile in monsters_in_rooms

            if tile_type == "room" and not visited:
                probability = 0.5
            elif tile_type == "room" and visited:
                probability = 1 / 6
            elif tile_type == "corridor":
                probability = 1 / 6
            else:
                probability = 0

            if random.random() < probability:
                monster = roll_monster(ROOM_MONSTER_TABLE)
                monsters_in_rooms[adjacent_tile] = monster
                print(f"A {monster['Name']} spawned at {adjacent_tile}, type: {tile_type}.")

                spawned_monsters[adjacent_tile] = {
                    "monsters": [{"Name": monster["Name"], "WP": monster["WP"], "Max WP": monster["WP"], "NV": monster.get("NV", 0)} for _ in range(monster["Count"])]
                }

def start_dungeon():
    global dungeon_data, tiles, revealed_tiles, monsters_in_rooms, movement_buttons, starting_room_position

    tiles = load_tiles()
    if not dungeon_data: 
        dungeon_data = create_dungeon(10)

    if not dungeon_data:
        print("Dungeon creation failed.")
        return

    for position, data in dungeon_data.items():
        print(f"Room at {position}: Type = {data['type']}")


    revealed_rooms = []
    room_positions = list(dungeon_data.items())
    starting_room_position = room_positions.pop(0)[0]
    first_connected_room = room_positions.pop(0)
    revealed_rooms.append((starting_room_position, dungeon_data[starting_room_position]))
    revealed_rooms.append(first_connected_room)

    verify_hero_images(party)

    revealed_tiles.add(starting_room_position)
    revealed_tiles.add(first_connected_room[0])

    player_position = starting_room_position

    canvas_width = 800
    canvas_height = 600
    canvas_center_x = canvas_width // 2
    canvas_center_y = canvas_height // 2

    def draw_dungeon():
        dungeon_image = draw_dungeon_visualization(
            dict(revealed_rooms), tiles, canvas_width, canvas_height, starting_room_position
        )
        dungeon_image_tk = ImageTk.PhotoImage(dungeon_image)

        dungeon_canvas.create_image(
            canvas_center_x, canvas_center_y, anchor="center", image=dungeon_image_tk
        )
        dungeon_canvas.image = dungeon_image_tk

        for monster_tag in dungeon_canvas.find_withtag("monster"):
            dungeon_canvas.delete(monster_tag)

        for position, monster in monsters_in_rooms.items():
            tag = f"monster_{position}"
            x, y = position
            canvas_x = canvas_center_x + (y - starting_room_position[1]) * 50
            canvas_y = canvas_center_y + (x - starting_room_position[0]) * 50

            dungeon_canvas.create_oval(
                canvas_x - 5, canvas_y - 5, canvas_x + 5, canvas_y + 5,
                fill="red", tag=("monster", tag)
            )
            print(f"Monster drawn at {position} with tag: {tag}")


    def draw_player(position):
        x, y = position
        canvas_x = canvas_center_x + (y - starting_room_position[1]) * 50
        canvas_y = canvas_center_y + (x - starting_room_position[0]) * 50

        radius = 10
        dungeon_canvas.create_oval(
            canvas_x - radius, canvas_y - radius,
            canvas_x + radius, canvas_y + radius,
            fill="green", outline="", tag="player"
        )


    def spawn_end_room_monsters(position):
        if dungeon_data[position]["type"] == "end":
            monsters_in_rooms[position] = [
            {"Name": "Evil Hero", "WP": MONSTER_CHARACTERISTICS["Evil Hero"]["WP"], "Max WP": MONSTER_CHARACTERISTICS["Evil Hero"]["WP"]},
            {"Name": "Troll", "WP": MONSTER_CHARACTERISTICS["Troll"]["WP"], "Max WP": MONSTER_CHARACTERISTICS["Troll"]["WP"]},
            {"Name": "Evil Mage", "WP": MONSTER_CHARACTERISTICS["Evil Mage"]["WP"], "Max WP": MONSTER_CHARACTERISTICS["Evil Mage"]["WP"]},
            ]
            print(f"Spawned predetermined monsters in the end room at {position}: Evil Hero, Troll, Evil Mage")

    update_leave_button = add_leave_button(dungeon_canvas, starting_room_position)

    def is_adjacent(current, target):
        cx, cy = current
        tx, ty = target
        return abs(cx - tx) + abs(cy - ty) == 1

    def move_player(direction):
        nonlocal player_position
        print(f"Attempting to move {direction}...")

        direction_map = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1)
        }

        if direction in direction_map:
            dx, dy = direction_map[direction]
            next_position = (player_position[0] + dx, player_position[1] + dy)

            if any(pos == next_position for pos, _ in revealed_rooms) and is_adjacent(player_position, next_position):
                current_tag = f"monster_{player_position}"
                if dungeon_canvas.find_withtag(current_tag):
                    dungeon_canvas.delete(current_tag)
                    print(f"Removed monster at {player_position} with tag: {current_tag}")

                if player_position in monsters_in_rooms:
                    del monsters_in_rooms[player_position]

                player_position = next_position
                print(f"Player moved to {player_position}.")

                if dungeon_data[player_position]["type"] == "end":
                    spawn_end_room_monsters(player_position)

                if player_position == revealed_rooms[-1][0] and room_positions:
                    while room_positions:
                        new_room = room_positions.pop(0)
                        if new_room[1] != "end" or not any(room[1] == "end" for room in revealed_rooms):
                            revealed_rooms.append(new_room)
                            revealed_tiles.add(new_room[0])
                            print(f"Revealed new room at {new_room[0]}.")
                            spawn_end_room_monsters(new_room[0])
                            break

                if player_position in monsters_in_rooms:
                    open_encounter_window(ROOM_MONSTER_TABLE, player_position)
                else:
                    print(f"Monsters in this room: 0")

                check_and_spawn_monster(player_position)

                draw_dungeon()
                draw_player(player_position)
                update_leave_button(player_position)
            else:
                print("Invalid move. Either room is not revealed or too far.")

    dungeon_canvas.pack(fill=tk.BOTH, expand=True)

    draw_dungeon()
    draw_player(player_position)

    button_frame = tk.Frame(dungeon_canvas, bg="#555", bd=2, relief=tk.SUNKEN)
    button_frame.pack(side=tk.RIGHT, padx=10, pady=10, anchor="se")

    movement_buttons = {
        "up": tk.Button(button_frame, text="Move Up", command=lambda: move_player("up"), bg="#555", fg="white"),
        "down": tk.Button(button_frame, text="Move Down", command=lambda: move_player("down"), bg="#555", fg="white"),
        "left": tk.Button(button_frame, text="Move Left", command=lambda: move_player("left"), bg="#555", fg="white"),
        "right": tk.Button(button_frame, text="Move Right", command=lambda: move_player("right"), bg="#555", fg="white"),
    }

    movement_buttons["up"].grid(row=0, column=1, pady=5)
    movement_buttons["left"].grid(row=1, column=0, padx=5)
    movement_buttons["right"].grid(row=1, column=2, padx=5)
    movement_buttons["down"].grid(row=2, column=1, pady=5)

def verify_hero_images(party):
    missing_images = []
    print("\nVerifying hero and initiate images...\n")

    for idx, hero in enumerate(party[:3]):
        hero_image_path = f"Heroes/{hero['Name']}.png"
        if os.path.isfile(hero_image_path):
            print(f"Hero image found: {hero_image_path}")
        else:
            print(f"Hero image missing: {hero_image_path}")
            missing_images.append(hero_image_path)

    for i, initiate in enumerate(party[3:6]):
        race = initiate["Race"]
        initiate_image_path = f"Heroes/{race}_{i + 1}.png"
        if os.path.isfile(initiate_image_path):
            print(f"Initiate image found: {initiate_image_path}")
        else:
            print(f"Initiate image missing: {initiate_image_path}")
            missing_images.append(initiate_image_path)

    if not missing_images:
        print("\nAll hero and initiate images are correctly available!")
    else:
        print("\nThe following images are missing:")
        for image in missing_images:
            print(f"- {image}")

def load_and_place_images():
    encounter_canvas.image_refs = []  

    image_size = (44, 44)

    for idx, member in enumerate(party[:6]):
        row = idx // 3
        col = idx % 3

        x = 200 + col * 80
        y = 400 + row * 80

        if idx < 3:
            image_path = f"Heroes/{member['Name']}.png"
        else:
            race = member["Race"]
            initiate_number = idx - 2
            image_path = f"Heroes/{race}_{initiate_number}.png"

        try:
            member_image = Image.open(image_path).resize(image_size, Image.Resampling.LANCZOS)
            member_photo = ImageTk.PhotoImage(member_image)
            encounter_canvas.create_image(x, y, image=member_photo, anchor="center", tags=f"member_{idx}")
            encounter_canvas.image_refs.append(member_photo) 
        except FileNotFoundError:
            print(f"Image not found: {image_path}")

def add_encounter_buttons(parent_frame, canvas, monster, party, monsters, combat_log, enable_close_button, encounter_window, is_end_room):
    button_frame = tk.Frame(parent_frame, bg="#333")
    button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=20, pady=20)

    fight_button = tk.Button(
        button_frame,
        text="Fight",
        command=lambda: handle_fight(canvas, party, monsters, combat_log, fight_button, negotiate_button, bribe_button, enable_close_button),
        bg="#555",
        fg="white",
        width=15,
        height=2
    )
    fight_button.pack(pady=10)

    negotiate_button = tk.Button(
        button_frame,
        text="Negotiate",
        command=lambda: handle_negotiation(monster, canvas, button_frame, negotiate_button, combat_log, enable_close_button),
        bg="#555",
        fg="white",
        width=15,
        height=2,
        state=tk.DISABLED if is_end_room else tk.NORMAL
    )
    negotiate_button.pack(pady=10)

    bribe_frame = tk.Frame(button_frame, bg="#333")
    bribe_frame.pack(pady=10)

    tk.Label(bribe_frame, text="Enter Gold Marks:", bg="#333", fg="white").pack()
    gold_entry = tk.Entry(bribe_frame, bg="#555", fg="white", justify="center")
    gold_entry.pack()

    bribe_button = tk.Button(
        button_frame,
        text="Bribe",
        command=lambda: handle_bribe(monster, canvas, button_frame, gold_entry, bribe_button, combat_log, enable_close_button),
        bg="#555",
        fg="white",
        width=15,
        height=2,
        state=tk.DISABLED if is_end_room else tk.NORMAL
    )
    bribe_button.pack(pady=10)

    close_button = tk.Button(
        button_frame,
        text="Close",
        state=tk.DISABLED,
        command=lambda: on_close(encounter_window),
        bg="#555",
        fg="white",
        width=15,
        height=2
    )
    close_button.pack(pady=20)

    return close_button


def add_leave_button(dungeon_canvas, starting_tile):
    def leave_dungeon():
        global party, movement_buttons

        if party_gold >= 1000:
            messagebox.showinfo(
                "Victory!",
                "Congratulations! You have amassed 1000 Gold Marks and won the game!"
            )
            for button in movement_buttons.values():
                button.config(state=tk.DISABLED)

            leave_button.config(state=tk.DISABLED)

            return

        for member in party:
            if member["WP"] > 0:
                member["WP"] = member["Max WP"]
        messagebox.showinfo(
            "Party Status",
            "The party members have been healed and are ready for the next adventure!"
        )


    leave_button = tk.Button(
        dungeon_canvas,
        text="Leave",
        command=leave_dungeon,
        bg="#555",
        fg="white",
        width=10,
        height=2,
    )

    leave_button_window = dungeon_canvas.create_window(
        25, 500, anchor="nw", window=leave_button, tags="leave_button"
    )

    def update_leave_button_visibility(player_position):
        if player_position == starting_tile:
            dungeon_canvas.itemconfigure(leave_button_window, state="normal")
        else:
            dungeon_canvas.itemconfigure(leave_button_window, state="hidden")

    return update_leave_button_visibility

def load_and_place_monsters(canvas, monster_name, monster_count):
    canvas.delete("monsters")
    image_refs = []

    cell_width = 150
    cell_height = 150
    start_x = 250
    start_y = 100

    positions = {
        1: [(1, 1)],
        2: [(1, 0), (1, 2)],
        3: [(1, 0), (1, 1), (1, 2)],
        4: [(0, 1), (1, 0), (1, 1), (1, 2)],
        5: [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)],
        6: [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)],
    }

    displayed_monster_count = min(monster_count, 6)
    monster_positions = positions[displayed_monster_count]

    for idx, (row, col) in enumerate(monster_positions):
        x = start_x + col * cell_width
        y = start_y + row * cell_height

        image_path = f"Monsters/{monster_name}.png"
        try:
            monster_image = Image.open(image_path).resize((100, 100), Image.Resampling.LANCZOS)
            monster_photo = ImageTk.PhotoImage(monster_image)
            image_refs.append(monster_photo)

            canvas.create_image(x, y, image=monster_photo, anchor="center", tags="monsters")

        except FileNotFoundError:
            print(f"Monster image not found: {image_path}")

    canvas.monster_image_refs = image_refs

def handle_negotiation(monster, canvas, button_frame, negotiate_button, combat_log, enable_close_button):
    if "NV" not in monster:
        message = "Negotiation is not possible with these monsters!"
        append_to_combat_log(combat_log, message)
        print(message)
        negotiate_button.config(state=tk.DISABLED)
        return

    roll = sum(roll_dice(6, 2))
    result = roll - monster["NV"]
    
    roll_result_text = f"Negotiation Roll: {roll} (Monster NV: {monster['NV']})"
    append_to_combat_log(combat_log, roll_result_text)
    print(roll_result_text)

    roll_result_display = canvas.create_text(
        canvas.winfo_width() // 2,
        canvas.winfo_height() // 2 - 50,
        text=roll_result_text,
        fill="white",
        font=("Arial", 14),
        tags="roll_result"
    )

    def determine_negotiation_outcome():
        def apply_choice(choice):
            if choice == "intimidation":
                negotiation_message = f"The monster is intimidated and leaves some treasure! Result: {result}"
                determine_treasure(monster)
                update_gold_label()
                for widget in button_frame.winfo_children():
                    if isinstance(widget, tk.Button):
                        widget.config(state=tk.DISABLED)
                enable_close_button()
            elif choice == "success":
                negotiation_message = f"The monster agrees to let the party pass! Result: {result}"
                for widget in button_frame.winfo_children():
                    if isinstance(widget, tk.Button):
                        widget.config(state=tk.DISABLED)
                enable_close_button()
            else:
                negotiation_message = f"Negotiation failed. Result: {result}"
                negotiate_button.config(state=tk.DISABLED)

            append_to_combat_log(combat_log, f"Negotiation: {negotiation_message}")
            print(negotiation_message)

            canvas.delete(roll_result_display)
            
            canvas.create_text(
                canvas.winfo_width() // 2,
                canvas.winfo_height() // 2 + 50,
                text=negotiation_message,
                fill="white",
                font=("Arial", 14),
                tags="negotiation_result"
            )
        
        if magic_enabled:
            choice_window = tk.Toplevel()
            choice_window.title("Choose Negotiation Outcome")
            tk.Label(choice_window, text="Choose how the negotiation ends:").pack()
            
            tk.Button(choice_window, text="Fail", command=lambda: [apply_choice("fail"), choice_window.destroy()]).pack()
            tk.Button(choice_window, text="Success", command=lambda: [apply_choice("success"), choice_window.destroy()]).pack()
            tk.Button(choice_window, text="Intimidation", command=lambda: [apply_choice("intimidation"), choice_window.destroy()]).pack()
        else:
            if result > 10:
                apply_choice("intimidation")
            elif result >= 7:
                apply_choice("success")
            else:
                apply_choice("fail")
    
    if magic_enabled:
        use_magic_window = tk.Toplevel()
        use_magic_window.title("Use Magic in Negotiation?")
        tk.Label(use_magic_window, text="Do you want to use magic?").pack()
        
        tk.Button(use_magic_window, text="Yes", command=lambda: [determine_negotiation_outcome(), use_magic_window.destroy()]).pack()
        tk.Button(use_magic_window, text="No", command=lambda: [use_magic_window.destroy(), determine_negotiation_outcome()]).pack()
    else:
        canvas.after(200, determine_negotiation_outcome)


def handle_bribe(monster, canvas, button_frame, gold_entry, bribe_button, combat_log, enable_close_button):
    global party_gold

    try:
        offer = int(gold_entry.get())

        if offer > party_gold:
            message = "You don't have enough gold to offer this bribe!"
            append_to_combat_log(combat_log, message)
            print(message)
            return

        monster_strength = monster["WP"] + monster["NV"]

        matching_row = None
        for row in BRIBERY_TABLE:
            if offer in row["Gold Marks"] and monster_strength in row["Range"]:
                matching_row = row
                break

        if not matching_row:
            message = f"The monster rejects your bribe of {offer} Gold Marks! (No valid range found)"
            append_to_combat_log(combat_log, message)
            print(message)
            bribe_button.config(state=tk.DISABLED)
            return

        roll = roll_dice(6)[0]
        bribe_roll = f"Bribe Roll: {roll}, Required Roll: {matching_row['Roll']}"
        append_to_combat_log(combat_log, bribe_roll)

        if roll <= matching_row["Roll"]:
            party_gold -= offer
            update_gold_label()
            message = f"The monster accepts your bribe of {offer} Gold Marks and leaves peacefully!"
            append_to_combat_log(combat_log, message)
            print(message)

            for widget in button_frame.winfo_children():
                if isinstance(widget, tk.Button):
                    widget.config(state=tk.DISABLED)

            for button in movement_buttons.values():
                button.config(state=tk.DISABLED)

            bribe_button.config(state=tk.DISABLED)

            enable_close_button()

            if player.position in spawned_monsters:
                monsters_in_rooms[player.position] = spawned_monsters[player.position]["monsters"]

        else:
            message = f"The monster rejects your bribe of {offer} Gold Marks!"
            append_to_combat_log(combat_log, message)
            print(message)
            bribe_button.config(state=tk.DISABLED)

    except ValueError:
        message = "Invalid input. Please enter a valid number."
        append_to_combat_log(combat_log, message)
        print(message)

PARTY_ATTACK_OPTIONS = {
    1: ["a"],
    2: ["b"],
    3: ["c"],
}

MONSTER_ATTACK_OPTIONS = {
    "a": [1],
    "b": [2],
    "c": [3],
}

def check_game_end_conditions():
    global party

    if not any(member["WP"] > 0 for member in party):
        messagebox.showinfo("Game Over", "All your party members have died. You lost the game!")
        root.destroy()
        return

    if player.position == starting_room_position and "end_cleared" in dungeon_data and dungeon_data["end_cleared"]:
        messagebox.showinfo("Victory!", "You have defeated the monsters in the end room and returned to safety. You won the game!")
        root.destroy()

def handle_fight(canvas, party, monsters, combat_log, fight_button, negotiate_button, bribe_button, enable_close_button):
    global movement_buttons

    for button in movement_buttons.values():
        button.config(state=tk.DISABLED)

    negotiate_button.config(state=tk.DISABLED)
    bribe_button.config(state=tk.DISABLED)

    canvas.delete("wp_display")

    append_to_combat_log(combat_log, "The fight begins!")
    update_combat_display(canvas, party, monsters)

    current_turn = [0]

    def process_turn():
        nonlocal monsters

        if not any(hero["WP"] > 0 for hero in party):
            append_to_combat_log(combat_log, "The party has been defeated!")
            disable_fight_button(fight_button)
            disable_all_buttons()
            check_game_end_conditions()
            return

        if not any(monster["WP"] > 0 for monster in monsters):
            append_to_combat_log(combat_log, "The monsters have been defeated!")
            total_gold = sum(calculate_monster_treasure(monster) for monster in monsters)
            if total_gold > 0:
                global party_gold
                party_gold += total_gold
                update_gold_label()
                append_to_combat_log(combat_log, f"Treasure collected: {total_gold} Gold Marks!")
            else:
                append_to_combat_log(combat_log, "No treasure collected.")

            if player.position in dungeon_data and dungeon_data[player.position]["type"] == "end":
                dungeon_data["end_cleared"] = True
                append_to_combat_log(combat_log, "You have cleared the monsters in the end room!")
            
            disable_fight_button(fight_button)
            disable_all_buttons()
            enable_close_button()
            check_game_end_conditions()
            return

        if current_turn[0] % 2 == 0:
            append_to_combat_log(combat_log, "--- Party Turn ---")
            for hero in party:
                if hero["WP"] > 0:
                    target = next((m for m in monsters if m["WP"] > 0), None)
                    if target:
                        damage = roll_attack_damage(hero, target)
                        target["WP"] -= damage
                        append_to_combat_log(combat_log, f"{hero['Name']} attacks {target['Name']} for {damage} damage!")
                        if target["WP"] <= 0:
                            append_to_combat_log(combat_log, f"{target['Name']} is defeated!")
        else:
            append_to_combat_log(combat_log, "--- Monster Turn ---")
            for monster in monsters:
                if monster["WP"] > 0:
                    target = next((h for h in party if h["WP"] > 0), None)
                    if target:
                        damage = roll_attack_damage(monster, target)
                        target["WP"] -= damage
                        append_to_combat_log(combat_log, f"{monster['Name']} attacks {target['Name']} for {damage} damage!")
                        if target["WP"] <= 0:
                            append_to_combat_log(combat_log, f"{target['Name']} is defeated!")

        update_combat_display(canvas, party, monsters)

        current_turn[0] += 1

        if any(hero["WP"] > 0 for hero in party) and any(monster["WP"] > 0 for monster in monsters):
            canvas.after(1000, process_turn)

    process_turn()

def disable_fight_button(fight_button):
    fight_button.config(state=tk.DISABLED)

def process_combat_turn(canvas, combat_log, party, monsters, party_positions, monster_positions, current_turn):
    if not any(member["WP"] > 0 for member in party):
        append_to_combat_log(combat_log, "The party has been defeated!")
        disable_all_buttons()
        canvas.create_text(
            canvas.winfo_width() // 2,
            canvas.winfo_height() // 2,
            text="The party has been defeated!",
            fill="red",
            font=("Arial", 16),
            tags="combat_result"
        )
        return

    if not any(monster["WP"] > 0 for monster in monsters):
        append_to_combat_log(combat_log, "The monsters have been defeated!")
        disable_all_buttons()
        canvas.create_text(
            canvas.winfo_width() // 2,
            canvas.winfo_height() // 2,
            text="The monsters have been defeated!",
            fill="green",
            font=("Arial", 16),
            tags="combat_result"
        )
        return

    party_to_monster = {member: [] for member in party_positions}
    monster_to_party = {monster: [] for monster in monster_positions}

    for party_member, party_pos in party_positions.items():
        for monster_id, monster_pos in monster_positions.items():
            if abs(party_pos[0] - monster_pos[0]) <= 1 and abs(party_pos[1] - monster_pos[1]) <= 1:
                party_to_monster[party_member].append(monster_id)
                monster_to_party[monster_id].append(party_member)

    if current_turn[0] % 2 == 0:
        append_to_combat_log(combat_log, "--- Party Turn ---")
        for member_id, targets in party_to_monster.items():
            if not targets:
                continue
            target_id = targets[0]
            if target_id in monster_positions:
                monster_index = list(monster_positions.keys()).index(target_id)
                monster = monsters[monster_index]
                damage = roll_attack_damage(party[member_id - 1], monster)
                monster["WP"] -= damage
                append_to_combat_log(combat_log, f"{party[member_id - 1]['Name']} attacks {monster['Name']} for {damage} damage!")
                if monster["WP"] <= 0:
                    append_to_combat_log(combat_log, f"{monster['Name']} is defeated!")
                    monsters.pop(monster_index)
                    del monster_positions[target_id]

    else:
        append_to_combat_log(combat_log, "--- Monster Turn ---")
        for monster_id, targets in monster_to_party.items():
            if not targets:
                append_to_combat_log(combat_log, f"Monster {monster_id} has no valid targets.")
                continue
            target_id = targets[0]
            if target_id in party_positions:
                hero = party[target_id - 1]
                damage = roll_attack_damage(monsters[list(monster_positions.keys()).index(monster_id)], hero)
                hero["WP"] -= damage
                append_to_combat_log(combat_log, f"{monsters[list(monster_positions.keys()).index(monster_id)]['Name']} attacks {hero['Name']} for {damage} damage!")
                if hero["WP"] <= 0:
                    append_to_combat_log(combat_log, f"{hero['Name']} is defeated!")
                    del party_positions[target_id]

    update_combat_display(canvas, party, monsters)

    current_turn[0] += 1

def disable_all_buttons():
    global movement_buttons

    for button in movement_buttons.values():
        button.config(state=tk.DISABLED)

    for widget in root.winfo_children():
        if isinstance(widget, tk.Button):
            widget.config(state=tk.DISABLED)

def roll_attack_damage(attacker, defender):
    weapon = attacker.get("Weapons", "Monster").split(", ")[0] if "Weapons" in attacker else "Monster"
    roll = sum(roll_dice(6, 1)) + attacker.get("CB", 0)
    damage_table = COMBAT_RESULTS_TABLE.get(weapon, COMBAT_RESULTS_TABLE["Monster"])
    damage = damage_table[min(roll, len(damage_table)) - 1]
    return damage

def process_combat_turn(canvas, combat_log, party, monsters, party_positions, monster_positions, current_turn):

    if not any(member["WP"] > 0 for member in party):
        append_to_combat_log(combat_log, "The party has been defeated!")
        disable_all_buttons()
        return
    if not any(monster["WP"] > 0 for monster in monsters):
        append_to_combat_log(combat_log, "The monsters have been defeated!")
        disable_all_buttons()
        return

    party_to_monster = {member: [] for member in party_positions}
    monster_to_party = {monster: [] for monster in monster_positions}

    for party_member, party_pos in party_positions.items():
        for monster_id, monster_pos in monster_positions.items():
            if abs(party_pos[0] - monster_pos[0]) <= 1 and abs(party_pos[1] - monster_pos[1]) <= 1:
                party_to_monster[party_member].append(monster_id)
                monster_to_party[monster_id].append(party_member)

    if current_turn[0] % 2 == 0:
        append_to_combat_log(combat_log, "--- Party Turn ---")
        for member_id, targets in party_to_monster.items():
            if not targets:
                continue
            target_id = targets[0]
            if target_id in monster_positions:
                monster_index = list(monster_positions.keys()).index(target_id)
                monster = monsters[monster_index]
                damage = roll_attack_damage(party[member_id - 1], monster)
                monster["WP"] -= damage
                append_to_combat_log(combat_log, f"{party[member_id - 1]['Name']} attacks {monster['Name']} for {damage} damage!")
                if monster["WP"] <= 0:
                    append_to_combat_log(combat_log, f"{monster['Name']} is defeated!")
                    monsters.pop(monster_index)
                    del monster_positions[target_id]

    else:
        append_to_combat_log(combat_log, "--- Monster Turn ---")
        for monster_id, targets in monster_to_party.items():
            if not targets:
                append_to_combat_log(combat_log, f"Monster {monster_id} has no valid targets.")
                continue
            target_id = targets[0]
            if target_id in party_positions:
                hero = party[target_id - 1]
                damage = roll_attack_damage(monsters[list(monster_positions.keys()).index(monster_id)], hero)
                hero["WP"] -= damage
                append_to_combat_log(combat_log, f"{monsters[list(monster_positions.keys()).index(monster_id)]['Name']} attacks {hero['Name']} for {damage} damage!")
                if hero["WP"] <= 0:
                    append_to_combat_log(combat_log, f"{hero['Name']} is defeated!")
                    del party_positions[target_id]

    update_combat_display(canvas, party, monsters)

    current_turn[0] += 1

def next_turn(canvas, next_turn_button, party, monsters, combat_log):
    combat_ongoing = combat_sequence(party, monsters, combat_log)

    update_combat_display(canvas, party, monsters)

    if not combat_ongoing:
        next_turn_button.destroy()

        if not any(hero["WP"] > 0 for hero in party):
            result_text = "The party has been defeated!"
        else:
            result_text = "The monsters have been defeated!"

        append_to_combat_log(combat_log, result_text)

        canvas.create_text(
            canvas.winfo_width() // 2,
            canvas.winfo_height() // 2,
            text=result_text,
            fill="white",
            font=("Arial", 16),
            tags="result_text",
        )

        for button in movement_buttons.values():
            button.config(state=tk.NORMAL)

def update_combat_display(canvas, party, monsters):
    for idx, hero in enumerate(party[:6]):
        tag = f"wp_display_hero_{idx}"
        if hero["WP"] > 0:
            row = idx // 3
            col = idx % 3
            x = 250 + col * 150
            y = 500 + row * 150

            if canvas.find_withtag(tag):
                canvas.itemconfig(tag, text=f"{hero['Name']} (WP: {hero['WP']}/{hero['Max WP']})")
            else:
                canvas.create_text(
                    x, y + 50,
                    text=f"{hero['Name']} (WP: {hero['WP']}/{hero['Max WP']})",
                    fill="white",
                    font=("Arial", 10),
                    tags=tag,
                )
        else:
            canvas.delete(tag)

    for idx, monster in enumerate(monsters):
        tag = f"wp_display_monster_{idx}"
        if monster["WP"] > 0:
            row = idx // 3
            col = idx % 3
            x = 250 + col * 150
            y = 100 + row * 150

            if canvas.find_withtag(tag):
                canvas.itemconfig(tag, text=f"{monster['Name']} (WP: {monster['WP']}/{monster['Max WP']})")
            else:
                canvas.create_text(
                    x, y + 50,
                    text=f"{monster['Name']} (WP: {monster['WP']}/{monster['Max WP']})",
                    fill="red",
                    font=("Arial", 10),
                    tags=tag,
                )
        else:
            canvas.delete(tag)

def open_encounter_window(monster_table, player_position):
    global movement_buttons, encounter_canvas, gold_label, encounter_window

    for button in movement_buttons.values():
        button.config(state=tk.DISABLED)

    encounter_window = tk.Toplevel(root)
    encounter_window.title("Monster Encounter")
    encounter_window.geometry("1200x800")
    encounter_window.configure(bg="#333")
    encounter_window.resizable(False, False)

    def prevent_close():
        messagebox.showinfo("Warning!", "Exit by clicking Close button")
    encounter_window.protocol("WM_DELETE_WINDOW", prevent_close)

    main_frame = tk.Frame(encounter_window, bg="#333")
    main_frame.pack(fill=tk.BOTH, expand=True)

    encounter_canvas = tk.Canvas(main_frame, width=900, height=800, bg="#333", highlightthickness=0)
    encounter_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    encounter_gold_label = tk.Label(
        main_frame,
        text=f"Total Gold: {party_gold} Gold Marks",
        font=("Arial", 16),
        fg="white",
        bg="#333",
        anchor="w",
    )
    encounter_gold_label.pack(side=tk.TOP, padx=10, pady=10)

    update_gold_label()

    is_end_room = dungeon_data[player_position]["type"] == "end"

    if is_end_room:
        monsters = [
            {"Name": "Evil Hero", "WP": 8, "Max WP": 8, "NV": 10},
            {"Name": "Troll", "WP": 10, "Max WP": 10, "NV": 12},
            {"Name": "Evil Mage", "WP": 6, "Max WP": 6, "NV": 8},
        ]
        append_to_combat_log(None, f"Predetermined monsters: {', '.join(m['Name'] for m in monsters)}")
    else:
        monster = roll_monster(monster_table)
        monsters = [{"Name": monster["Name"], "WP": monster["WP"], "Max WP": monster["WP"], "NV": monster.get("NV", 0)} for _ in range(monster["Count"])]

    combat_log = tk.Text(
        main_frame,
        width=50,
        height=10,
        bg="#222",
        fg="white",
        state="normal",
        wrap="word"
    )
    combat_log.pack(side=tk.BOTTOM, padx=10, pady=10)

    if is_end_room:
        append_to_combat_log(combat_log, "You encountered the strongest monsters in the end room!")
    else:
        append_to_combat_log(combat_log, f"You encountered {len(monsters)} {monsters[0]['Name']}!")

    close_button = add_encounter_buttons(
        main_frame,
        encounter_canvas,
        monsters[0],
        party,
        monsters,
        combat_log,
        lambda: close_button.config(state=tk.NORMAL),
        encounter_window,
        is_end_room=is_end_room
    )
    load_and_place_party(encounter_canvas)
    for monster in monsters:
        load_and_place_monsters(encounter_canvas, monster["Name"], len(monsters))

    encounter_window.protocol("WM_DELETE_WINDOW", prevent_close)

def update_gold_label():
    global gold_label, encounter_window

    if gold_label:
        gold_label.config(text=f"Total Gold: {party_gold} Gold Marks")

    if 'encounter_window' in globals():
        encounter_gold_label = next(
            (widget for widget in encounter_window.winfo_children() 
             if isinstance(widget, tk.Label) and "Gold" in widget.cget("text")), 
            None
        )
        if encounter_gold_label:
            encounter_gold_label.config(text=f"Total Gold: {party_gold} Gold Marks")

def on_close(encounter_window):
    global spawned_monsters

    if player.position in spawned_monsters:
        monsters_in_rooms[player.position] = spawned_monsters[player.position]["monsters"]

    for button in movement_buttons.values():
        button.config(state=tk.NORMAL)
    encounter_window.destroy()

def determine_treasure(monster):
    global party_gold

    if monster["Name"] in ["Evil Hero", "Evil Hero", "Evil Hero"]:
        print(f"{monster['Name']} does not drop any treasure.")
        display_treasure_results(0, 0)
        return

    if "Treasure" not in monster:
        print(f"Monster {monster['Name']} has no treasure.")
        display_treasure_results(0, 0)
        return

    monster_name = monster["Name"]
    print(f"Determining treasure for {monster_name}...")

    treasure_data_gold = MONSTER_GOLD_REWARDS.get(monster_name, {}).get("visited", {})
    treasure_data_jewels = MONSTER_JEWELS_TABLE.get(monster_name, {}).get("visited", {})

    total_gold = 0
    total_jewel_value = 0

    if treasure_data_gold:
        threshold = treasure_data_gold["threshold"]
        max_roll = treasure_data_gold["max_roll"]
        multiplier = treasure_data_gold["multiplier"]

        if threshold != -1 and max_roll > 0 and multiplier > 0:
            roll = random.randint(1, max_roll)
            if roll <= threshold:
                gold_amount = roll * multiplier
                total_gold += gold_amount
                print(f"Gold found from {monster_name}: {gold_amount} Gold Marks (Roll: {roll}, Multiplier: {multiplier}).")
            else:
                print(f"No gold found from {monster_name} (Roll: {roll} exceeded threshold {threshold}).")

    if treasure_data_jewels:
        threshold = treasure_data_jewels["threshold"]
        max_roll = treasure_data_jewels["max_roll"]

        if threshold != -1 and max_roll > 0:
            roll = random.randint(1, max_roll)
            if roll <= threshold:
                jewel_count = roll
                print(f"Jewels found from {monster_name}: {jewel_count} jewels (Roll: {roll}).")

                for i in range(jewel_count):
                    jewel_roll = sum(roll_dice(6, 2))
                    jewel_value = int(JEWELS_TABLE.get(str(jewel_roll), "0"))
                    total_jewel_value += jewel_value
                    print(f"Jewel {i + 1}: Rolled {jewel_roll}, worth {jewel_value} Gold Marks.")
            else:
                print(f"No jewels found from {monster_name} (Roll: {roll} exceeded threshold {threshold}).")

    total_treasure_value = total_gold + total_jewel_value
    if total_treasure_value > 0:
        party_gold += total_treasure_value
        update_gold_label()
        display_treasure_results(total_gold, total_jewel_value)
    else:
        print("You found no treasure!")
        display_treasure_results(0, 0)

def display_treasure_results(gold, jewels):
    total_value = gold + jewels

    treasure_window = tk.Toplevel(root)
    treasure_window.title("Treasure Found")
    treasure_window.geometry("400x250")
    treasure_window.configure(bg="#333")

    tk.Label(
        treasure_window,
        text=f"Gold Marks Found: {gold}",
        font=("Arial", 16),
        fg="white",
        bg="#333",
    ).pack(pady=10)

    tk.Label(
        treasure_window,
        text=f"Jewel Value Found: {jewels}",
        font=("Arial", 16),
        fg="white",
        bg="#333",
    ).pack(pady=10)

    tk.Label(
        treasure_window,
        text=f"Total Party Gold: {party_gold} Gold Marks",
        font=("Arial", 14),
        fg="white",
        bg="#333",
    ).pack(pady=10)

    tk.Button(
        treasure_window,
        text="Close",
        command=treasure_window.destroy,
        bg="#555",
        fg="white",
    ).pack(pady=10)

def update_gold_label():
    global gold_label, encounter_window

    if gold_label:
        gold_label.config(text=f"Total Gold: {party_gold} Gold Marks")

    if 'encounter_window' in globals():
        for widget in encounter_window.winfo_children():
            if isinstance(widget, tk.Label) and "Gold" in widget.cget("text"):
                widget.config(text=f"Total Gold: {party_gold} Gold Marks")

def calculate_monster_treasure(monster, tile_visited=False):

    monster_name = monster.get("Name")
    if not monster_name or monster_name not in MONSTER_GOLD_REWARDS:
        print(f"No treasure data available for {monster_name}.")
        return 0

    reward_type = "visited" if tile_visited else "nonvisited"
    reward_data = MONSTER_GOLD_REWARDS[monster_name][reward_type]

    threshold = reward_data["threshold"]
    max_roll = reward_data["max_roll"]
    multiplier = reward_data["multiplier"]

    if threshold == -1 or max_roll == 0 or multiplier == 0:
        return 0

    roll = random.randint(1, max_roll)
    if roll <= threshold:
        treasure = roll * multiplier
        print(f"Treasure found from {monster_name}: {treasure} Gold Marks (Roll: {roll}, Multiplier: {multiplier})")
        return treasure

    print(f"No treasure from {monster_name} (Roll: {roll} exceeded threshold {threshold}).")
    return 0

def load_and_place_party(canvas):

    canvas.delete("party")
    image_refs = []

    cell_width = 150
    cell_height = 150
    start_x = 250
    start_y = 500

    for idx, member in enumerate(party[:6]):
        if member["WP"] <= 0:
            continue

        row = idx // 3
        col = idx % 3

        x = start_x + col * cell_width
        y = start_y + row * cell_height

        image_path = (
            f"Heroes/{member['Name']}.png"
            if idx < 3
            else f"Heroes/{member['Race']}_{idx - 2}.png"
        )
        try:
            hero_image = Image.open(image_path).resize((100, 100), Image.Resampling.LANCZOS)
            hero_photo = ImageTk.PhotoImage(hero_image)
            image_refs.append(hero_photo)

            canvas.create_image(x, y, image=hero_photo, anchor="center", tags="party")

        except FileNotFoundError:
            print(f"Image not found: {image_path}")

    canvas.party_image_refs = image_refs

def add_save_button(parent_frame):
    save_button = tk.Button(
        parent_frame,
        text="Save Game",
        command=lambda: save_game(player, dungeon_data, monsters_in_rooms, party, party_gold, magic_enabled),
        bg="#555",
        fg="white"
    )
    save_button.pack(side=tk.RIGHT, padx=10)


def load_saved_game():
    global player, dungeon_data, monsters_in_rooms, party, party_gold, magic_enabled, gold_label

    save_data = load_game()
    if save_data:
        player.position = tuple(save_data["player_position"])
        dungeon_data = save_data["dungeon_data"]
        monsters_in_rooms = save_data["monsters_in_rooms"]
        party = save_data.get("party", [])
        party_gold = save_data.get("party_gold", 1000)
        magic_enabled = save_data.get("magic_enabled", False)

        print(f"Magic Enabled (Loaded): {magic_enabled}")

        main_menu.pack_forget()
        
        if gold_label:
            gold_label.pack_forget()

        gold_label_frame = tk.Frame(root, bg="#333")
        gold_label_frame.pack(side=tk.TOP, fill=tk.X)

        gold_label = tk.Label(
            gold_label_frame,
            text=f"Total Gold: {party_gold} Gold Marks",
            font=("Arial", 16),
            fg="white",
            bg="#333",
            anchor="w",
        )
        gold_label.pack(pady=5, padx=10)

        add_save_button(gold_label_frame)

        update_gold_label()
        start_dungeon()


def update_character_card_buttons():
    global party
    for widget in dungeon_canvas.winfo_children():
        if isinstance(widget, tk.Button) and widget.cget("text") == "Character Cards":
            widget.destroy()

    add_character_card_button(root, party, dungeon_canvas)

def toggle_magic():
    global magic_enabled
    magic_enabled = not magic_enabled
    magic_status_label.config(text="ON" if magic_enabled else "OFF")
    print("Magic ON" if magic_enabled else "Magic OFF")

root = tk.Tk()
root.title("Citadel of Blood")
root.geometry("800x600")
root.configure(bg="#333")
root.resizable(False, False)

magic_enabled = False

main_menu = tk.Frame(root, bg="#333")
setup_frame = tk.Frame(root, bg="#333")
initiate_frame = tk.Frame(root, bg="#333")
reorganize_frame = tk.Frame(root, bg="#333")
dungeon_canvas = tk.Canvas(root, bg="#222")
combat_frame = tk.Frame(root, bg="#333")

main_menu.pack(fill=tk.BOTH, expand=True)
tk.Label(main_menu, text="Citadel of Blood", font=("Arial", 24), fg="white", bg="#333").pack()

magic_frame = tk.Frame(main_menu, bg="#333")
magic_frame.pack(pady=10)

magic_checkbox = tk.Checkbutton(
    magic_frame, text="Magic", font=("Arial", 16), fg="white", bg="#333",
    selectcolor="#333", command=toggle_magic
)
magic_checkbox.pack(side=tk.LEFT)

magic_status_label = tk.Label(magic_frame, text="OFF", font=("Arial", 16), fg="white", bg="#333")
magic_status_label.pack(side=tk.RIGHT, padx=10)

start_button = tk.Button(
    main_menu,
    text="Start Game",
    command=start_game,
    bg="#555",
    fg="white",
    font=("Arial", 18),
    width=20,
    height=3
)
start_button.pack(expand=True)

button_frame = tk.Frame(main_menu, bg="#333")
button_frame.pack()
load_button = tk.Button(
    button_frame,
    text="Load Game",
    command=lambda: load_saved_game(),
    bg="#555",
    fg="white",
    font=("Arial", 18),
    width=20,
    height=3
)
load_button.pack(side=tk.RIGHT, padx=5)

root.mainloop()