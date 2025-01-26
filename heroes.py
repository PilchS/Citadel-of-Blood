import random
from PIL import ImageTk, Image
import os

HEROES = [
    {"Name": "Almuric", "Race": "Human", "WP": 8, "MP": "1/1/2", "RV": 2, "CB": 3, "Weapons": "Sword, Dagger", "Weapon Skill": "+2 Sword", "Skill": "1 Hellgate"},
    {"Name": "Alric", "Race": "Human", "WP": 6, "MP": "2/3/4", "RV": 2, "CB": 0, "Weapons": "Sword, Throw Dagger", "Weapon Skill": "None", "Skill": "1 Hellgate"},
    {"Name": "Curvenol", "Race": "Human", "WP": 5, "MP": "5/5/5", "RV": 1, "CB": 0, "Weapons": "Sword, Throw Dagger", "Weapon Skill": "None", "Skill": "2 Hellgate"},
    {"Name": "Dalmilandril", "Race": "Elf", "WP": 5, "MP": "3/4/5", "RV": 3, "CB": 2, "Weapons": "Bow, Dagger", "Weapon Skill": "+2 Bow", "Skill": "+2 Negotiation"},
    {"Name": "Dierdra", "Race": "Human", "WP": 7, "MP": "0/0/0", "RV": 1, "CB": 4, "Weapons": "Hammer, Sword", "Weapon Skill": "+1 Hammer", "Skill": "1 Hellgate"},
    {"Name": "Eodred", "Race": "Human", "WP": 6, "MP": "3/4/5", "RV": 2, "CB": 0, "Weapons": "Bow, Throw Dagger", "Weapon Skill": "+2 Bow", "Skill": "2 Hellgate"},
    {"Name": "Gerudirr", "Race": "Dwarf", "WP": 6, "MP": "0/0/0", "RV": 2, "CB": 6, "Weapons": "Ax, Dagger", "Weapon Skill": "+3 Ax", "Skill": "1 Detrap"},
    {"Name": "Gilith", "Race": "Elf", "WP": 8, "MP": "0/0/0", "RV": 3, "CB": 4, "Weapons": "Bow, Dagger", "Weapon Skill": "+2 Bow", "Skill": "+2 Negotiation"},
    {"Name": "Gislan", "Race": "Dwarf", "WP": 10, "MP": "4/4/4", "RV": 3, "CB": 4, "Weapons": "Ax, Dagger", "Weapon Skill": "+2 Ax", "Skill": "3 Detrap"},
    {"Name": "Gwaigilion Elengal", "Race": "Elf", "WP": 7, "MP": "4/3/2", "RV": 3, "CB": 4, "Weapons": "Bow, Dagger", "Weapon Skill": "+2 Bow", "Skill": "+1 Negotiation"},
    {"Name": "Larraka", "Race": "Human", "WP": 5, "MP": "6/5/4", "RV": 3, "CB": 0, "Weapons": "Bow, Dagger", "Weapon Skill": "None", "Skill": "1 Hellgate"},
    {"Name": "Linfalas", "Race": "Elf", "WP": 9, "MP": "0/0/0", "RV": 2, "CB": 5, "Weapons": "Bow, Sword", "Weapon Skill": "+2 Bow", "Skill": "+3 Negotiation"},
    {"Name": "Lord Dil", "Race": "Human", "WP": 10, "MP": "0/0/0", "RV": 3, "CB": 5, "Weapons": "Sword, Dagger", "Weapon Skill": "+2 Sword", "Skill": "2 Hellgate"},
    {"Name": "Maytwist", "Race": "Elf", "WP": 7, "MP": "3/3/3", "RV": 2, "CB": 0, "Weapons": "Throw Dagger, Bow", "Weapon Skill": "+2 Bow", "Skill": "+3 Negotiation"},
    {"Name": "Paladin Glade", "Race": "Human", "WP": 10, "MP": "0/0/0", "RV": 2, "CB": 4, "Weapons": "Sword, Throw Dagger", "Weapon Skill": "+2 Sword", "Skill": "2 Hellgate"},
    {"Name": "Raman Cronkevitch", "Race": "Demi-Cronk", "WP": 9, "MP": "0/0/0", "RV": 3, "CB": 4, "Weapons": "Sword, Dagger", "Weapon Skill": "+1 Sword", "Skill": "1 Detrap"},
    {"Name": "Sliggoth", "Race": "Swamp Creature", "WP": 8, "MP": "1/2/3", "RV": 2, "CB": 4, "Weapons": "Ax, Bow", "Weapon Skill": "+1 Ax", "Skill": "1 Detrap"},
    {"Name": "Stephen Paladin", "Race": "Human", "WP": 10, "MP": "0/0/0", "RV": 2, "CB": 5, "Weapons": "Sword, Dagger", "Weapon Skill": "+2 Sword", "Skill": "2 Hellgate"},
    {"Name": "Theregond", "Race": "Human", "WP": 8, "MP": "4/3/2", "RV": 2, "CB": 1, "Weapons": "Sword, Throw Dagger", "Weapon Skill": "+3 Sword", "Skill": "3 Hellgate"},
    {"Name": "Weldron", "Race": "Human", "WP": 9, "MP": "0/0/0", "RV": 2, "CB": 5, "Weapons": "Sword, Bow", "Weapon Skill": "+2 Sword", "Skill": "3 Hellgate"},
    {"Name": "Wendolyn", "Race": "Human", "WP": 7, "MP": "4/3/2", "RV": 2, "CB": 1, "Weapons": "Sword, Dagger", "Weapon Skill": "+2 Dagger", "Skill": "4 Hellgate"},
    {"Name": "Zareth", "Race": "Human", "WP": 9, "MP": "0/0/0", "RV": 4, "CB": 4, "Weapons": "Sword, Throw Dagger", "Weapon Skill": "+1 Sword", "Skill": "3 Hellgate"},
    {"Name": "Zurik", "Race": "Dwarf", "WP": 8, "MP": "3/4/5", "RV": 2, "CB": 3, "Weapons": "Ax, Dagger", "Weapon Skill": "+2 Ax", "Skill": "3 Detrap"},
]

def create_character_record(character):
    return {
        "Name": character["Name"],
        "Race": character.get("Race", ""),
        "Wound Points": character["WP"],
        "Magical Potential": character.get("MP", "0/0/0"),
        "Resistance Value": character["RV"],
        "Combat Bonus": character["CB"],
        "Weapons": character["Weapons"],
        "Weapon Skill": character.get("Weapon Skill", "None"),
        "Skills": character.get("Skill", "None"),
        "Spells": [],
        "Magic Items": [],
        "Gold Marks": 0,
        "Jewels": 0,
        "Experience Points": 0
    }

def load_character_image(name, folder, variant=None):
    try:
        if variant:
            filename = f"{name}{variant}.jpg"
        else:
            filename = f"{name}.jpg"

        filepath = os.path.join(folder, filename)

        image = Image.open(filepath)
        return ImageTk.PhotoImage(image)
    except FileNotFoundError:
        print(f"Image not found for {name}. Using placeholder.")
        placeholder = Image.new("RGB", (100, 100), color="gray")
        return ImageTk.PhotoImage(placeholder)