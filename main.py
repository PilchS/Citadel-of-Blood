import tkinter as tk
from dungeon_creator import create_dungeon
from dungeon_visualizer import load_tiles, draw_dungeon_visualization
from PIL import ImageTk
from collections import deque


def bfs_shortest_path(start, target, used_positions):
    """Find the shortest path between start and target using BFS."""
    queue = deque([(start, [])])
    visited = set()

    while queue:
        current, path = queue.popleft()

        if current == target:
            return path

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
            queue.append((neighbor, path + [neighbor]))

    return []


def main():
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 800
    BUTTON_HEIGHT = 40
    CANVAS_MARGIN = 10

    root = tk.Tk()
    root.title("Dungeon Visualizer")
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.resizable(False, False)

    root.config(bg="#2E2E2E")

    frame = tk.Frame(root, bg="#000000")
    frame.pack(fill=tk.BOTH, expand=True)

    canvas_width = WINDOW_WIDTH - 2 * CANVAS_MARGIN
    canvas_height = WINDOW_HEIGHT - BUTTON_HEIGHT - 2 * CANVAS_MARGIN

    canvas = tk.Canvas(frame, bg="#1E1E1E", width=canvas_width, height=canvas_height)
    canvas.pack(side=tk.TOP, pady=CANVAS_MARGIN)

    button_frame = tk.Frame(root, bg="#000000")
    button_frame.pack(side=tk.BOTTOM, fill=tk.X)

    reveal_button = tk.Button(
        button_frame,
        text="Reveal Next Room",
        command=None,
        bg="#3A3A3A",
        fg="white",
        relief="flat",
        height=2
    )
    reveal_button.pack(pady=5)

    tiles = load_tiles()
    used_positions = create_dungeon(50)
    if not used_positions:
        print("Dungeon creation failed.")
        reveal_button.config(state=tk.DISABLED)
        return

    revealed_rooms = []
    room_positions = list(used_positions.items())
    starting_room_position = room_positions[0][0]
    player_position = starting_room_position

    canvas_center_x = canvas_width // 2
    canvas_center_y = canvas_height // 2

    dungeon_image = None

    def draw_player(position):
        x, y = position
        canvas_x = canvas_center_x + (y - starting_room_position[1]) * 53
        canvas_y = canvas_center_y + (x - starting_room_position[0]) * 53

        radius = 10
        tile_center_x = canvas_x + 53 // 2
        tile_center_y = canvas_y + 53 // 2

        canvas.create_oval(
            tile_center_x - radius, tile_center_y - radius,
            tile_center_x + radius, tile_center_y + radius,
            fill="green", outline=""
        )


    def move_player_to(target_position):
        nonlocal player_position
        path = bfs_shortest_path(player_position, target_position, dict(revealed_rooms))

        for step in path:
            player_position = step
            canvas.delete("all")
            draw_dungeon()
            draw_player(player_position)
            canvas.update()
            canvas.after(200)

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

    def reveal_next_room():
        nonlocal dungeon_image
        if room_positions:
            position, room = room_positions.pop(0)
            revealed_rooms.append((position, room))

            draw_dungeon()
            move_player_to(position)
        else:
            print("All rooms revealed.")
            reveal_button.config(state=tk.DISABLED)

    reveal_button.config(command=reveal_next_room)

    draw_dungeon()
    draw_player(player_position)

    root.mainloop()


if __name__ == "__main__":
    main()
