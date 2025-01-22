import tkinter as tk
from dungeon_creator import create_dungeon, room_types
from dungeon_visualizer import load_tiles, draw_dungeon_visualization
from PIL import ImageTk
from collections import deque
import random

def bfs_shortest_path(start, target, used_positions):
    queue = deque([(start, [])])
    visited = set()

    while queue:
        current, path = queue.popleft()

        if current == target:
            return path + [current]

        if current in visited:
            continue

        visited.add(current)

        neighbors = []
        x, y = current
        directions = {
            "top": (x - 1, y),
            "bottom": (x + 1, y),
            "left": (x, y - 1),
            "right": (x, y + 1),
        }

        for direction, neighbor in directions.items():
            if neighbor in used_positions and neighbor not in visited:
                neighbors.append(neighbor)

        for neighbor in neighbors:
            queue.append((neighbor, path + [current]))

    return []

def main():
    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 600
    BUTTON_HEIGHT = 40
    CANVAS_MARGIN = 10

    tile_size = 53
    root = tk.Tk()
    root.title("Dungeon Visualizer")
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.resizable(False, False)
    root.config(bg="#2E2E2E")


    player_stats = {
        "Name": "string",
        "Race": "string",
        "Ability": "integer",
        "Strength": "integer",
        "Spells": "string",
        "Magical Potential": "integer",
        "Magical Items": "string",
        "Resistance": "integer",
        "Gold": "integer",
        "Agility": "integer",
        "Weapon": "string",
        "Experience Points": "integer",
        "Proficiency": "string",
        "Valuables": "string",
    }

    stats_frame = tk.Frame(root, bg="#1E1E1E")
    stats_frame.pack(fill=tk.BOTH, expand=True)

    stats_entries = {}
    error_label = tk.Label(stats_frame, text="", bg="#1E1E1E", fg="red")
    error_label.grid(row=len(player_stats) + 1, column=0, columnspan=2, pady=10)

    def start_game():
        nonlocal player_stats

        errors = []
        for stat, (expected_type, entry) in stats_entries.items():
            value = entry.get()
            if expected_type == "integer":
                if not value.isdigit():
                    errors.append(f"{stat} must be an integer.")
                    continue
                player_stats[stat] = int(value)
            else:
                player_stats[stat] = value if value else ""

        player_stats["Gold"] = player_stats.get("Gold", 0) or 0
        player_stats["Experience Points"] = player_stats.get("Experience Points", 0) or 0

        if errors:
            error_label.config(text="\n".join(errors))
            return

        error_label.config(text="")
        stats_frame.pack_forget()
        game_frame.pack(fill=tk.BOTH, expand=True)

    for idx, (stat, expected_type) in enumerate(player_stats.items()):
        label = tk.Label(stats_frame, text=f"{stat} ({expected_type}):", bg="#1E1E1E", fg="white")
        label.grid(row=idx, column=0, sticky="w", padx=10, pady=5)

        entry = tk.Entry(stats_frame, bg="#3A3A3A", fg="white", relief="flat")
        entry.grid(row=idx, column=1, padx=10, pady=5)
        stats_entries[stat] = (expected_type, entry)

    start_button = tk.Button(
        stats_frame,
        text="Start Game",
        bg="#3A3A3A",
        fg="white",
        relief="flat",
        command=start_game,
    )
    start_button.grid(row=len(player_stats), column=0, columnspan=2, pady=10)

    game_frame = tk.Frame(root, bg="#1E1E1E")

    canvas_width = WINDOW_WIDTH - 2 * CANVAS_MARGIN
    canvas_height = WINDOW_HEIGHT - BUTTON_HEIGHT - 2 * CANVAS_MARGIN

    canvas = tk.Canvas(game_frame, bg="#1E1E1E", width=canvas_width, height=canvas_height)
    canvas.pack(side=tk.TOP, pady=CANVAS_MARGIN)

    button_frame = tk.Frame(game_frame, bg="#2E2E2E")
    button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=0)

    button_container = tk.Frame(button_frame, bg="#2E2E2E")
    button_container.pack(side=tk.BOTTOM, pady=5)

    reveal_button = tk.Button(
        button_container,
        text="Reveal Next Room",
        bg="#3A3A3A",
        fg="white",
        relief="flat",
        height=2,
    )
    reveal_button.pack(side=tk.LEFT, padx=10)

    lost_button = tk.Button(
        button_container,
        text="I lost to the enemy",
        bg="#FF4C4C",
        fg="white",
        relief="flat",
        height=2,
        state=tk.DISABLED,
    )
    lost_button.pack(side=tk.LEFT, padx=10)

    tiles = load_tiles()
    used_positions = create_dungeon(10)
    if not used_positions:
        print("Dungeon creation failed.")
        reveal_button.config(state=tk.DISABLED)
        return

    revealed_rooms = []
    room_positions = list(used_positions.items())
    starting_room_position = room_positions[0][0]
    player_position = starting_room_position
    target_position = starting_room_position
    path_to_target = []
    active_enemy_position = None

    canvas_center_x = canvas_width // 2
    canvas_center_y = canvas_height // 2

    dungeon_image = None

    def draw_player(position):
        x, y = position
        canvas_x = canvas_center_x + (y - starting_room_position[1]) * tile_size
        canvas_y = canvas_center_y + (x - starting_room_position[0]) * tile_size

        radius = 10
        tile_center_x = canvas_x + tile_size // 2
        tile_center_y = canvas_y + tile_size // 2

        canvas.create_oval(
            tile_center_x - radius,
            tile_center_y - radius,
            tile_center_x + radius,
            tile_center_y + radius,
            fill="green",
            outline="",
            tag="player",
        )

    def spawn_enemy(position):
        nonlocal active_enemy_position
        room_type = room_types[used_positions[position]]['type']

        if room_type == 'corridor' and random.randint(1, 6) == 1:
            active_enemy_position = position
        elif room_type != 'corridor' and random.randint(1, 2) == 1:
            active_enemy_position = position
        else:
            active_enemy_position = None

    def draw_enemy():
        if active_enemy_position:
            x, y = active_enemy_position
            canvas_x = canvas_center_x + (y - starting_room_position[1]) * tile_size
            canvas_y = canvas_center_y + (x - starting_room_position[0]) * tile_size

            radius = 10
            enemy_center_x = canvas_x + tile_size // 2
            enemy_center_y = canvas_y + tile_size // 2

            canvas.create_oval(
                enemy_center_x - radius,
                enemy_center_y - radius,
                enemy_center_x + radius,
                enemy_center_y + radius,
                fill="red",
                outline="",
                tag="enemy",
            )

    def check_proximity_to_enemy():
        if active_enemy_position:
            px, py = player_position
            ex, ey = active_enemy_position
            distance = abs(px - ex) + abs(py - ey)
            if distance == 1:
                lost_button.config(state=tk.NORMAL)
            else:
                lost_button.config(state=tk.DISABLED)
        else:
            lost_button.config(state=tk.DISABLED)

    def handle_loss():
        lost_button.config(state=tk.DISABLED)
        reveal_button.config(state=tk.DISABLED)
        print("Player lost to the enemy!")
        print("Player Statistics:")
        for stat, value in player_stats.items():
            print(f"{stat}: {value}")

    lost_button.config(command=handle_loss)

    def move_player():
        nonlocal player_position, active_enemy_position
        if path_to_target:
            next_step = path_to_target.pop(0)
            player_position = next_step

            if player_position == active_enemy_position:
                pass

            if used_positions.get(player_position) == "end":
                print("Player has reached the 'end' tile.")
                print("Player Statistics:")
                for stat, value in player_stats.items():
                    print(f"{stat}: {value}")
                canvas.create_text(
                    canvas_center_x,
                    canvas_center_y,
                    text="You escaped!",
                    fill="white",
                    font=("Arial", 24),
                )
                reveal_button.config(state=tk.DISABLED)

            canvas.delete("all")
            draw_dungeon()
            draw_player(player_position)
            draw_enemy()
            canvas.update()

            check_proximity_to_enemy()
            return True
        return False

    def draw_dungeon():
        nonlocal dungeon_image
        dungeon_image = draw_dungeon_visualization(
            dict(revealed_rooms), tiles, canvas_width, canvas_height, starting_room_position
        )

        dungeon_image_tk = ImageTk.PhotoImage(dungeon_image)
        canvas.create_image(
            canvas_center_x, canvas_center_y, anchor="center", image=dungeon_image_tk
        )
        canvas.image = dungeon_image_tk

        draw_enemy()

    def reveal_next_room():
        nonlocal dungeon_image, path_to_target, target_position

        if player_position != target_position:
            if not move_player():
                print("Error: Player failed to move.")
            return

        if room_positions:
            previous_position = player_position
            position, room = room_positions.pop(0)
            revealed_rooms.append((position, room))

            if room == "end":
                print("Final room placed: the 'end' tile has been set.")
            else:
                spawn_enemy(position)

            target_position = position
            path_to_target = bfs_shortest_path(previous_position, target_position, dict(revealed_rooms))

            draw_dungeon()
            draw_player(player_position)

            check_proximity_to_enemy()
        else:
            print("All rooms revealed.")
            reveal_button.config(state=tk.DISABLED)

    reveal_button.config(command=reveal_next_room)

    draw_dungeon()
    draw_player(player_position)

    root.mainloop()

if __name__ == "__main__":
    main()
