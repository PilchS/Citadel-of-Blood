import random

# dodac wszystkie pokoje, grafika, przeciwnicy i pulapki

connections = {
    "x": {"top": "small", "bottom": "small", "left": "small", "right": "small"},
    "a": {"right": "small", "bottom": "small"},
    "b": {"right": "small", "top": "small"},
    "c": {"left": "small", "bottom": "small"},
    "d": {"left": "small", "top": "small"},
    "e": {"left": "small", "right": "small"},
    "f": {"top": "small", "bottom": "small"},
}


shared_a_count = 5
shared_e_count = 5 

map_grid = [[" "] * 10 for _ in range(10)]
start_x, start_y = 5, 5

map_grid[start_x][start_y] = "X"
used_positions = {(start_x, start_y): "x"}

def get_adjacent_position(x, y, direction):
    if direction == "top":
        return x - 1, y
    elif direction == "bottom":
        return x + 1, y
    elif direction == "left":
        return x, y - 1
    elif direction == "right":
        return x, y + 1

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
    global shared_a_count, shared_e_count
    rotation_order = ["a", "c", "b", "d"]
    is_line_room = base_room in ["e", "f"]

    if is_line_room:
        chosen_room = "e" if direction in ["left", "right"] else "f"
        nx, ny = get_adjacent_position(current_position[0], current_position[1], direction)

        if (0 <= nx < len(map_grid)) and (0 <= ny < len(map_grid[0])) and (nx, ny) not in used_positions:
            if compatible_connection(current_room, chosen_room, direction):
                map_grid[nx][ny] = chosen_room
                used_positions[(nx, ny)] = chosen_room
                shared_e_count -= 1
                print(f"Connecting room {current_room} to room {chosen_room} from the {direction}.")
                return (nx, ny, chosen_room, True)

    else:
        for rotated_room in rotation_order:
            nx, ny = get_adjacent_position(current_position[0], current_position[1], direction)
            if (0 <= nx < len(map_grid)) and (0 <= ny < len(map_grid[0])) and (nx, ny) not in used_positions:
                if compatible_connection(current_room, rotated_room, direction):
                    map_grid[nx][ny] = rotated_room
                    used_positions[(nx, ny)] = rotated_room
                    shared_a_count -= 1
                    print(f"Connecting room {current_room} to room {rotated_room} from the {direction}.")
                    return (nx, ny, rotated_room, True)

    return (None, None, None, False)

def create_dungeon(max_rooms):
    path = []
    current_room = "x"
    current_position = (start_x, start_y)
    room_count = 1

    while room_count < max_rooms:
        possible_rooms = []

        if shared_a_count > 0:
            possible_rooms.append("a")
        if shared_e_count > 0:
            possible_rooms.append("e")

        if not possible_rooms:
            print("No available rooms left to draw.")
            break

        random.shuffle(possible_rooms)
        placed = False

        for next_room in possible_rooms:
            for direction in connections[current_room]:
                nx, ny, placed_room, placed = try_place_room(current_room, next_room, current_position, direction)

                if placed:
                    path.append((current_position, current_room))
                    current_position = (nx, ny)
                    current_room = placed_room
                    room_count += 1
                    break

            if placed:
                break

        if not placed:
            if path:
                last_position, last_room = path.pop()
                current_position = last_position
                current_room = last_room
                print(f"Backtracking to room {current_room} at position {current_position}")
            else:
                print("Bad dungeon: could not connect to any available room.")
                return

create_dungeon(20)

for row in map_grid:
    print(" ".join(row))
