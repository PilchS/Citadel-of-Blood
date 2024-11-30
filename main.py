import tkinter as tk
from dungeon_creator import create_dungeon
from dungeon_visualizer import load_tiles, draw_dungeon_visualization
from PIL import ImageTk


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

    canvas_center_x = canvas_width // 2
    canvas_center_y = canvas_height // 2

    dungeon_image = None

    def reveal_next_room():
        nonlocal dungeon_image
        if room_positions:
            position, room = room_positions.pop(0)
            revealed_rooms.append((position, room))

            dungeon_image = draw_dungeon_visualization(
                dict(revealed_rooms), tiles, canvas_width, canvas_height, starting_room_position
            )

            dungeon_image_tk = ImageTk.PhotoImage(dungeon_image)

            dungeon_width, dungeon_height = dungeon_image.size
            canvas.config(scrollregion=(0, 0, dungeon_width, dungeon_height))
            canvas.create_image(
                canvas_center_x, canvas_center_y, anchor="center", image=dungeon_image_tk
            )

            canvas.image = dungeon_image_tk
        else:
            print("All rooms revealed.")
            reveal_button.config(state=tk.DISABLED)

    reveal_button.config(command=reveal_next_room)

    root.mainloop()


if __name__ == "__main__":
    main()
