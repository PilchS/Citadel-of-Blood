import tkinter as tk
from PIL import ImageTk, Image

def start_battle(hero_party, monsters, canvas, dungeon_canvas):
    dungeon_canvas.pack_forget()
    canvas.pack()
    setup_battle(canvas, hero_party, monsters)

def setup_battle(canvas, hero_party, monsters):
    canvas.delete("all")

    for i, hero in enumerate(hero_party):
        x, y = 100, 100 + i * 50
        canvas.create_oval(x, y, x+20, y+20, fill="green")
        canvas.create_text(x + 30, y + 10, text=f"{hero['Name']} {hero['WP']}/{hero['Max WP']}")

    for i, monster in enumerate(monsters):
        x, y = 500, 100 + i * 50
        canvas.create_oval(x, y, x+20, y+20, fill="red")
        canvas.create_text(x - 30, y + 10, text=f"{monster['Name']} {monster['WP']}")

    setup_battle_buttons(canvas)

def setup_battle_buttons(canvas):
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
