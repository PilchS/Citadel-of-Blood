import random

connections = {
    # a = 11
    "a1": {"right": "small"},
    "a2": {"bottom": "small"},
    "a3": {"left": "small"},
    "a4": {"top": "small"},

    # b = 4
    "b1": {"right": "small", "bottom": "small"},
    "b2": {"left": "small", "bottom": "small"},
    "b3": {"left": "small", "top": "small"},
    "b4": {"right": "small", "top": "small"},

    # c = 12
    "c1": {"left": "big", "top": "big", "bottom": "small"},
    "c2": {"left": "small", "right": "big", "top": "big"},
    "c3": {"right": "big", "top": "small", "bottom": "big"},
    "c4": {"left": "big", "right": "small", "bottom": "big"},

    # d = 16
    "d1": {"left": "big", "right": "big", "bottom": "small"},
    "d2": {"left": "small", "top": "big", "bottom": "big"},
    "d3": {"left": "big", "right": "big", "top": "small"},
    "d4": {"right": "small", "top": "big", "bottom": "big"},

    # e = 14
    "e1": {"left": "big", "right": "big", "top": "small", "bottom": "small"},
    "e2": {"left": "small", "right": "small", "top": "big", "bottom": "big"},

    # f = 7
    "f1": {"left": "small", "right": "small"},
    "f2": {"top": "small", "bottom": "small"},

    # g = 6
    "g1": {"left": "small", "right": "big", "bottom": "small"},
    "g2": {"left": "big", "top": "small", "bottom": "big"},
    "g3": {"left": "big", "right": "small", "top": "big"},
    "g4": {"right": "big", "top": "big", "bottom": "small"},

    # h = 18
    "h1": {"left": "big", "bottom": "big"},
    "h2": {"left": "big", "top": "big"},
    "h3": {"right": "big", "top": "big"},
    "h4": {"right": "big", "bottom": "big"},

    # i = 11
    "i1": {"left": "big", "right": "small", "top": "small", "bottom": "big"},
    "i2": {"left": "big", "right": "small", "top": "big", "bottom": "small"},
    "i3": {"left": "small", "right": "big", "top": "big", "bottom": "small"},
    "i4": {"left": "small", "right": "big", "top": "small", "bottom": "big"},

    # j = 14
    "j1": {"left": "big", "right": "big"},
    "j2": {"top": "big", "bottom": "big"}
}

room_counts = {
    "a": 11, "b": 4, "c": 12, "d": 16, "e": 14, "f": 7, "g": 6, "h": 18, "i": 11, "j": 14
}

rotation_map = {room: base for base in room_counts for room in connections if room.startswith(base)}

map_grid = [[" "] * 10 for _ in range(10)]
start_x, start_y = 5, 5
map_grid[start_x][start_y] = "X"
used_positions = {(start_x, start_y): "x"}


def draw_starting_room():
    global start_x, start_y
    available_rooms = [room for room, count in room_counts.items() if count > 0]
    if not available_rooms:
        print("No available starting rooms.")
        return None

    base_room = random.choice(available_rooms)
    rotations = [r for r in connections if r.startswith(base_room)]
    starting_room = random.choice(rotations)

    map_grid[start_x][start_y] = starting_room
    used_positions[(start_x, start_y)] = starting_room
    room_counts[base_room] -= 1
    print(f"Starting room drawn: {starting_room}")
    return starting_room


def get_adjacent_position(x, y, direction):
    return {
        "top": (x - 1, y),
        "bottom": (x + 1, y),
        "left": (x, y - 1),
        "right": (x, y + 1)
    }[direction]


def opposite_direction(direction):
    return {
        "top": "bottom",
        "bottom": "top",
        "left": "right",
        "right": "left"
    }[direction]


def compatible_connection(current_room, next_room, direction):
    opposite_dir = opposite_direction(direction)
    return (direction in connections[current_room] and
            opposite_dir in connections[next_room] and
            connections[current_room][direction] == connections[next_room][opposite_dir])


def try_place_room(current_room, base_room, current_position, direction):
    global room_counts
    rotations = [r for r in connections if r.startswith(base_room)]

    for rotated_room in rotations:
        nx, ny = get_adjacent_position(current_position[0], current_position[1], direction)
        if (0 <= nx < len(map_grid)) and (0 <= ny < len(map_grid[0])) and (nx, ny) not in used_positions:
            if compatible_connection(current_room, rotated_room, direction):
                map_grid[nx][ny] = rotated_room
                used_positions[(nx, ny)] = rotated_room
                room_counts[base_room] -= 1
                print(f"Connecting room {current_room} to room {rotated_room} from the {direction}. Drawn room: {rotated_room}")
                return (nx, ny, rotated_room, True)

    return (None, None, None, False)


def create_dungeon(max_rooms):
    global start_x, start_y
    current_position = (start_x, start_y)
    current_room = draw_starting_room()

    if not current_room:
        print("Dungeon creation failed: No starting room available.")
        return None

    path = []
    room_count = 1

    while room_count < max_rooms:
        possible_rooms = [r for r, count in room_counts.items() if count > 0]
        if not possible_rooms:
            print("No available rooms left to draw.")
            break

        base_room = random.choice(possible_rooms)
        placed = False

        for direction in connections[current_room]:
            nx, ny, placed_room, placed = try_place_room(current_room, base_room, current_position, direction)

            if placed:
                path.append((current_position, current_room))
                current_position = (nx, ny)
                current_room = placed_room
                room_count += 1
                break

        if not placed:
            if path:
                last_position, last_room = path.pop()
                current_position = last_position
                current_room = last_room
                print(f"Backtracking to room {current_room} at position {current_position}")
            else:
                print("Bad dungeon: could not connect to any available room.")
                return used_positions

    return used_positions


if __name__ == "__main__":
    create_dungeon(20)
    for row in map_grid:
        print(" ".join(row))
