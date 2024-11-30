from PIL import Image
from dungeon_creator import room_counts


tile_folder = "tiles"
tile_size = 53

def load_tiles():
    tiles = {}
    for base_room in room_counts.keys():
        tile_path = f"{tile_folder}/{base_room}.png"
        tiles[base_room] = Image.open(tile_path).convert("RGBA")
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
        base_room = room[:-1]
        rotation_suffix = room[-1]
        tile = tiles[base_room]
        rotated_tile = rotate_tile(tile, rotation_suffix)

        pos_x = offset_x + (y - start_y) * tile_size
        pos_y = offset_y + (x - start_x) * tile_size

        canvas.paste(rotated_tile, (pos_x, pos_y), rotated_tile)

    return canvas