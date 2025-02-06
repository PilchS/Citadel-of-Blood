from PIL import Image, ImageDraw
from dungeon_creator import room_counts, room_types
import os

tile_folder = "tiles"
tile_size = 53
border_size = 3

def load_tiles():
    tiles = {}
    for tile in os.listdir("tiles"):
        if tile.endswith(".png"):
            tile_name = tile.split(".")[0]
            tiles[tile_name] = Image.open(f"{tile_folder}/{tile}").convert("RGBA")
    return tiles

def rotate_tile(tile, rotation_suffix):
    if rotation_suffix is None:
        return tile
    angle = -90 * (int(rotation_suffix) - 1)
    return tile.rotate(angle, expand=True)

def draw_dungeon_visualization(used_positions, tiles, window_width, window_height, starting_position):
    tile_size = 53
    offset_x = window_width // 2 - tile_size // 2
    offset_y = window_height // 2 - tile_size // 2
    start_x, start_y = starting_position

    canvas = Image.new("RGBA", (window_width, window_height), (255, 255, 255, 0))

    draw = ImageDraw.Draw(canvas)
    border_color = (0, 0, 0, 255)

    draw.rectangle([0, 0, window_width, border_size], fill=border_color)
    draw.rectangle([0, window_height - border_size, window_width, window_height], fill=border_color)

    draw.rectangle([0, 0, border_size, window_height], fill=border_color)
    draw.rectangle([window_width - border_size, 0, window_width, window_height], fill=border_color)

    for (x, y), data in used_positions.items():
        if isinstance(data, str):
            data = {"room": data, "type": room_types.get(data, {}).get("type", "unknown")}

        room = data["room"]
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
        rotated_tile = rotate_tile(tile, rotation_suffix)

        pos_x = offset_x + (y - start_y) * tile_size
        pos_y = offset_y + (x - start_x) * tile_size

        if (pos_x + tile_size > border_size and pos_x < window_width - border_size and
            pos_y + tile_size > border_size and pos_y < window_height - border_size):
            canvas.paste(rotated_tile, (pos_x, pos_y), rotated_tile)

    return canvas
