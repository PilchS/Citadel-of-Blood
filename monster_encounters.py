import tkinter as tk
from PIL import ImageTk, Image

def start_battle(hero_party, monsters, canvas, dungeon_canvas):
    """Transition to battle canvas and set up combat."""
    dungeon_canvas.pack_forget()  # Hide dungeon canvas
    canvas.pack()  # Show battle canvas
    setup_battle(canvas, hero_party, monsters)

def setup_battle(canvas, hero_party, monsters):
    """Draw battle canvas with heroes and monsters."""
    canvas.delete("all")  # Clear the canvas

    # Draw Heroes
    for i, hero in enumerate(hero_party):
        x, y = 100, 100 + i * 50
        canvas.create_oval(x, y, x+20, y+20, fill="green")
        canvas.create_text(x + 30, y + 10, text=f"{hero['Name']} {hero['WP']}/{hero['Max WP']}")

    # Draw Monsters
    for i, monster in enumerate(monsters):
        x, y = 500, 100 + i * 50
        canvas.create_oval(x, y, x+20, y+20, fill="red")
        canvas.create_text(x - 30, y + 10, text=f"{monster['Name']} {monster['WP']}")

    setup_battle_buttons(canvas)

def setup_battle_buttons(canvas):
    """Create buttons for combat actions."""
    fight_button = tk.Button(canvas, text="Fight", command=lambda: print("Fight logic"))
    bribe_button = tk.Button(canvas, text="Bribe", command=lambda: print("Bribe logic"))
    negotiate_button = tk.Button(canvas, text="Negotiate", command=lambda: print("Negotiate logic"))
    next_turn_button = tk.Button(canvas, text="Next Turn", command=lambda: print("Next Turn logic"))
    reorganize_button = tk.Button(canvas, text="Reorganize", command=lambda: print("Reorganize logic"))

    fight_button.pack(side=tk.LEFT)
    bribe_button.pack(side=tk.LEFT)
    negotiate_button.pack(side=tk.LEFT)
    next_turn_button.pack(side=tk.LEFT)
    reorganize_button.pack(side=tk.LEFT)
