import random

connections = {
    "x": {"top": "small", "bottom": "small", "left": "small", "right": "small"},
    "a": {"right": "small", "bottom": "small"},
    "b": {"right": "small", "top": "small"},
    "c": {"left": "small", "bottom": "small"},
    "d": {"left": "small", "top": "small"},
    "e": {"left": "small", "right": "small"},
    "f": {"top": "small", "bottom": "small"},
    "g": {"bottom": "big", "right": "small"},
    "h": {"top": "big", "left": "small"}
}


# a -> 90deg = c, 180deg = b, 270deg = d, potrzebuje tylko room limitu na a, jak nie pasuje i jest rotacja, wtedy przypisuje literke z otpowiednia rotacja
# nie powinno obracac przy startowym pokoju
room_limits = {
    "x": 1,
    "a": 2,
    "b": 2,
    "c": 2,
    "d": 2,
    "e": 1,
    "f": 1,
    "g": 2,
    "h": 2
}

room_counts = {room: 0 for room in room_limits}
room_rotations = {room: 0 for room in connections}

map_grid = [[" "] * 10 for _ in range(10)]
start_x, start_y = 5, 5

map_grid[start_x][start_y] = "X"
used_positions = {(start_x, start_y): "x"}
room_counts["x"] = 1  

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

def rotate_room(room):
    rotated = {}
    for direction, connection_type in connections[room].items():
        if direction == "top":
            rotated["right"] = connection_type
        elif direction == "right":
            rotated["bottom"] = connection_type
        elif direction == "bottom":
            rotated["left"] = connection_type
        elif direction == "left":
            rotated["top"] = connection_type
    connections[room] = rotated
    room_rotations[room] = (room_rotations[room] + 1) % 4

def try_place_room_with_rotations(current_room, next_room, current_position, direction):
    for rotation_count in range(4):
        nx, ny = get_adjacent_position(current_position[0], current_position[1], direction)
        
        if (0 <= nx < len(map_grid)) and (0 <= ny < len(map_grid[0])) and (nx, ny) not in used_positions:
            if compatible_connection(current_room, next_room, direction):
                map_grid[nx][ny] = next_room
                used_positions[(nx, ny)] = next_room
                room_counts[next_room] += 1
                print(f"Connecting room {current_room} to room {next_room} from the {direction} after rotating {rotation_count * 90} degrees.")
                
                print(f"Current entrances of room {next_room}: {connections[next_room]}\n")
                return (nx, ny, True)
        
        rotate_room(next_room)

    return (None, None, False)

def create_dungeon(max_rooms):
    path = []
    current_room = "x"
    current_position = (start_x, start_y)
    room_count = 1
    consecutive_backtracks = 0

    while room_count < max_rooms:
        possible_rooms = [room for room in connections.keys() if room_counts[room] < room_limits[room]]
        
        if not possible_rooms:
            print("No more available rooms to place.")
            return
        
        max_consecutive_backtracks = len(used_positions)
        random.shuffle(possible_rooms)
        placed = False

        for next_room in possible_rooms:
            for direction in connections[current_room]:
                nx, ny, placed = try_place_room_with_rotations(current_room, next_room, current_position, direction)
                
                if placed:
                    path.append((current_position, current_room))
                    current_position = (nx, ny)
                    current_room = next_room
                    room_count += 1
                    consecutive_backtracks = 0
                    break

            if placed:
                break

        if not placed:
            if path:
                last_position, last_room = path.pop()
                current_position = last_position
                current_room = last_room
                consecutive_backtracks += 1
                print(f"Backtracking to room {current_room} at position {current_position}")
                if consecutive_backtracks >= max_consecutive_backtracks:
                    print("Too many consecutive backtracks, ending dungeon generation.")
                    return
            else:
                print(f"Bad dungeon: could not connect room {current_room} to any available room.")
                return

create_dungeon(10)

for row in map_grid:
    print(" ".join(row))
