from PIL import Image
from dungeon_creator import room_counts
import os

tile_folder = "tiles"
tile_size = 53

def load_tiles():
    tiles = {}
    for tile in os.listdir("tiles"):
        if tile.endswith(".png"):
            tile_name = tile.split(".")[0]
            if tile_name == "end":
                tiles[tile_name] = Image.open(f"tiles/{tile}").convert("RGBA")
            else:
                tiles[tile_name] = Image.open(f"tiles/{tile}").convert("RGBA")
    return tiles


def rotate_tile(tile, rotation_suffix):
    angle = -90 * (int(rotation_suffix) - 1)
    return tile.rotate(angle, expand=True)

def draw_dungeon_visualization(used_positions, tiles, window_width, window_height, starting_position):
    tile_size = 53

    offset_x = window_width // 2
    offset_y = window_height // 2

    start_x, start_y = starting_position

    canvas = Image.new("RGBA", (window_width, window_height), (255, 255, 255, 0))

    for (x, y), room in used_positions.items():
        if not room:
            print(f"Skipping invalid room at position {(x, y)}")
            continue

        if room == "start" or room == "end":
            base_room = room
            rotation_suffix = None
        else:
            base_room = room[:-1]
            rotation_suffix = room[-1]

        if base_room not in tiles:
            print(f"Invalid base_room '{base_room}' at position {(x, y)}. Skipping.")
            continue

        tile = tiles[base_room]
        rotated_tile = rotate_tile(tile, rotation_suffix) if rotation_suffix else tile

        pos_x = offset_x + (y - start_y) * tile_size
        pos_y = offset_y + (x - start_x) * tile_size

        canvas.paste(rotated_tile, (pos_x, pos_y), rotated_tile)

    return canvas