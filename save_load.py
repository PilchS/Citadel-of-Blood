import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

SAVE_FOLDER = "saves"

def ensure_save_folder():
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)

def save_game(player, dungeon_data, monsters_in_rooms, party, party_gold, magic_enabled):
    ensure_save_folder()

    save_name = simpledialog.askstring("Save Game", "Enter save name:")
    if not save_name:
        messagebox.showerror("Save Error", "Save name cannot be empty!")
        return

    save_path = os.path.join(SAVE_FOLDER, f"{save_name}.json")

    save_data = {
        "player_position": list(player.position),
        "dungeon_data": {str(k): v for k, v in dungeon_data.items()},
        "monsters_in_rooms": {str(k): v for k, v in monsters_in_rooms.items()},
        "party_gold": party_gold,
        "party": party,
        "magic_enabled": magic_enabled
    }

    try:
        with open(save_path, "w") as file:
            json.dump(save_data, file, indent=4)
        messagebox.showinfo("Game Saved", f"Game saved as '{save_name}'")
    except Exception as e:
        messagebox.showerror("Save Error", f"An error occurred while saving: {str(e)}")



def load_game():
    ensure_save_folder()

    save_files = [f for f in os.listdir(SAVE_FOLDER) if f.endswith(".json")]

    if not save_files:
        messagebox.showerror("Load Error", "No saved games found!")
        return None

    save_name = simpledialog.askstring("Load Game", f"Available saves:\n{', '.join(save_files)}\nEnter save name:")
    if not save_name or f"{save_name}.json" not in save_files:
        messagebox.showerror("Load Error", "Invalid save name selected!")
        return None

    save_path = os.path.join(SAVE_FOLDER, f"{save_name}.json")

    try:
        with open(save_path, "r") as file:
            save_data = json.load(file)

        save_data["player_position"] = tuple(save_data["player_position"])
        save_data["dungeon_data"] = {eval(k): v for k, v in save_data["dungeon_data"].items()}
        save_data["monsters_in_rooms"] = {eval(k): v for k, v in save_data["monsters_in_rooms"].items()}

        global party, party_gold, magic_enabled
        party = save_data.get("party", [])
        party_gold = save_data.get("party_gold", 1000)
        magic_enabled = save_data.get("magic_enabled", False)

        print(f"Loaded party: {party}")
        print(f"Magic Enabled: {magic_enabled}")

        messagebox.showinfo("Game Loaded", f"Game '{save_name}' successfully loaded.")
        return save_data
    except Exception as e:
        messagebox.showerror("Load Error", f"An error occurred while loading: {str(e)}")
        return None



def add_save_button(parent_frame, player, dungeon_data, monsters_in_rooms):
    save_button = tk.Button(
        parent_frame,
        text="Save Game",
        command=lambda: save_game(player, dungeon_data, monsters_in_rooms),
        bg="#555",
        fg="white"
    )
    save_button.pack(side=tk.BOTTOM, pady=10)

def add_load_button(parent_frame):
    load_button = tk.Button(
        parent_frame,
        text="Load Game",
        command=load_game,
        bg="#555",
        fg="white"
    )
    load_button.pack(side=tk.BOTTOM, pady=10)
