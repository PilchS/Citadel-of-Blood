import random
import time

connections = {
    "start": {"top": "any", "bottom": "any", "left": "any", "right": "any"},

    "end": {"top": "any", "bottom": "any", "left": "any", "right": "any"},

    "a1": {"right": "small"},
    "a2": {"bottom": "small"},
    "a3": {"left": "small"},
    "a4": {"top": "small"},

    "b1": {"right": "small", "bottom": "small"},
    "b2": {"left": "small", "bottom": "small"},
    "b3": {"left": "small", "top": "small"},
    "b4": {"right": "small", "top": "small"},

    "c1": {"left": "big", "top": "big", "bottom": "small"},
    "c2": {"left": "small", "right": "big", "top": "big"},
    "c3": {"right": "big", "top": "small", "bottom": "big"},
    "c4": {"left": "big", "right": "small", "bottom": "big"},

    "d1": {"left": "big", "right": "big", "bottom": "small"},
    "d2": {"left": "small", "top": "big", "bottom": "big"},
    "d3": {"left": "big", "right": "big", "top": "small"},
    "d4": {"right": "small", "top": "big", "bottom": "big"},

    "e1": {"left": "big", "right": "big", "top": "small", "bottom": "small"},
    "e2": {"left": "small", "right": "small", "top": "big", "bottom": "big"},

    "f1": {"top": "small", "bottom": "small"},
    "f2": {"left": "small", "right": "small"},

    "g1": {"left": "small", "right": "big", "bottom": "big"},
    "g2": {"left": "big", "top": "small", "bottom": "big"},
    "g3": {"left": "big", "right": "small", "top": "big"},
    "g4": {"right": "big", "top": "big", "bottom": "small"},

    "h1": {"left": "big", "bottom": "big"},
    "h2": {"left": "big", "top": "big"},
    "h3": {"right": "big", "top": "big"},
    "h4": {"right": "big", "bottom": "big"},

    "i1": {"left": "big", "right": "small", "top": "small", "bottom": "big"},
    "i2": {"left": "big", "right": "small", "top": "big", "bottom": "small"},
    "i3": {"left": "small", "right": "big", "top": "big", "bottom": "small"},
    "i4": {"left": "small", "right": "big", "top": "small", "bottom": "big"},

    "j1": {"left": "big", "right": "big"},
    "j2": {"top": "big", "bottom": "big"},   

    "k1": {"left": "small", "right": "small", "top": "small", "bottom": "small"},
    "m1": {"left": "small", "right": "small", "top": "small", "bottom": "small"},
    "p1": {"left": "small", "right": "small", "top": "small", "bottom": "small"},
    "s1": {"left": "small", "right": "small", "top": "small", "bottom": "small"},
    "t1": {"left": "small", "right": "small", "top": "small", "bottom": "small"},
    "w1": {"left": "small", "right": "small", "top": "small", "bottom": "small"},
    "x1": {"left": "small", "right": "small", "top": "small", "bottom": "small"},
    "z1": {"left": "small", "right": "small", "top": "small", "bottom": "small"}
}

room_types = {
    "start": {"type": "start"},
    "end": {"type": "end"},
    "a1": {"type": "corridor"},
    "a2": {"type": "corridor"},
    "a3": {"type": "corridor"},
    "a4": {"type": "corridor"},
    "b1": {"type": "corridor"},
    "b2": {"type": "corridor"},
    "b3": {"type": "corridor"},
    "b4": {"type": "corridor"},
    "c1": {"type": "corridor"},
    "c2": {"type": "corridor"},
    "c3": {"type": "corridor"},
    "c4": {"type": "corridor"},
    "d1": {"type": "corridor"},
    "d2": {"type": "corridor"},
    "d3": {"type": "corridor"},
    "d4": {"type": "corridor"},
    "e1": {"type": "corridor"},
    "e2": {"type": "corridor"},
    "f1": {"type": "corridor"},
    "f2": {"type": "corridor"},
    "g1": {"type": "corridor"},
    "g2": {"type": "corridor"},
    "g3": {"type": "corridor"},
    "g4": {"type": "corridor"},
    "h1": {"type": "corridor"},
    "h2": {"type": "corridor"},
    "h3": {"type": "corridor"},
    "h4": {"type": "corridor"},
    "i1": {"type": "corridor"},
    "i2": {"type": "corridor"},
    "i3": {"type": "corridor"},
    "i4": {"type": "corridor"},
    "j1": {"type": "corridor"},
    "j2": {"type": "corridor"},
    "k1": {"type": "room"},
    "m1": {"type": "room"},
    "p1": {"type": "room"},
    "s1": {"type": "room"},
    "t1": {"type": "room"},
    "w1": {"type": "room"},
    "x1": {"type": "room"},
    "z1": {"type": "room"}
}

room_counts = {
    "start": 0, "end":0, "a": 11, "b": 4, "c": 12, "d": 16, "e": 14, "f": 7, "g": 6, "h": 18, "i": 11, "j": 14, "k": 5, "m": 10, "p": 4, "s": 10, "t": 5, "w": 5, "x": 4, "z": 5
    #"start": 0, "a": 0, "b": 0, "c": 0, "d": 0, "e": 0, "f": 0, "g": 0, "h": 0, "i": 0, "j": 50, "k": 0, "m": 0, "p": 0, "s": 0, "t": 0, "w": 0, "x": 0, "z": 0
}

rotation_map = {room: base for base in room_counts for room in connections if room.startswith(base)}

map_grid = [[" "] * 9 for _ in range(9)]
start_x, start_y = 4, 4
map_grid[start_x][start_y] = "X"
used_positions = {(start_x, start_y): "x"}

def draw_starting_room():
    global start_x, start_y
    predefined_start_room = "start"
    map_grid[start_x][start_y] = predefined_start_room
    used_positions[(start_x, start_y)] = {
        "room": predefined_start_room,
        "type": "start",
    }
    room_counts[predefined_start_room] = 0
    print(f"Starting room drawn: {predefined_start_room}")
    return predefined_start_room

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

    if current_room == "start":
        if direction in connections["start"]:
            return connections["start"][direction] == "any" and opposite_dir in connections[next_room]
        return False

    if next_room == "start":
        if opposite_dir in connections["start"]:
            return connections["start"][opposite_dir] == "any" and direction in connections[current_room]
        return False

    if direction in connections[current_room] and opposite_dir in connections[next_room]:
        current_conn = connections[current_room][direction]
        next_conn = connections[next_room][opposite_dir]

        return current_conn == "any" or next_conn == "any" or current_conn == next_conn

    return False

def check_all_connections(current_position, new_room):
    directions = ["top", "bottom", "left", "right"]

    for direction in directions:
        nx, ny = get_adjacent_position(current_position[0], current_position[1], direction)

        if not (0 <= nx < len(map_grid) and 0 <= ny < len(map_grid[0])):
            continue
        if (nx, ny) not in used_positions:
            continue

        neighbor_data = used_positions[(nx, ny)]

        if isinstance(neighbor_data, str):
            neighbor_room = neighbor_data
        else:
            neighbor_room = neighbor_data["room"]

        if not compatible_connection(new_room, neighbor_room, direction):
            print(f"Conflict detected: {new_room} at {current_position} is not compatible with {neighbor_room} at {(nx, ny)}.")
            return False

    return True

def try_place_room(current_room, base_room, current_position, direction):
    global room_counts
    rotations = [r for r in connections if r.startswith(base_room)]
    directions = ["top", "right", "bottom", "left"]

    for _ in range(len(directions)):
        nx, ny = get_adjacent_position(current_position[0], current_position[1], direction)
        if (0 <= nx < len(map_grid)) and (0 <= ny < len(map_grid[0])) and (nx, ny) not in used_positions:
            for rotated_room in rotations:
                if rotated_room == "start":
                    continue
                if compatible_connection(current_room, rotated_room, direction):
                    if check_all_connections((nx, ny), rotated_room):
                        map_grid[nx][ny] = rotated_room
                        used_positions[(nx, ny)] = {
                            "room": rotated_room,
                            "type": room_types.get(rotated_room, {}).get("type", "unknown"),
                        }

                        room_counts[base_room] -= 1
                        print(f"Placed room {rotated_room}, type: {used_positions[(nx, ny)]['type']} at {(nx, ny)} in direction {direction}")
                        return (nx, ny, rotated_room, True)

        direction = directions[(directions.index(direction) + 1) % len(directions)]

    print(f"Failed to place room {base_room} from {current_position} in any direction.")
    return (None, None, None, False)

def rotate_direction(direction):
    order = ["top", "right", "bottom", "left"]
    idx = order.index(direction)
    return order[(idx + 1) % len(order)]

def create_dungeon(max_rooms):
    global start_x, start_y
    start_time = time.time()

    current_position = (start_x, start_y)
    current_room = draw_starting_room()

    if not current_room:
        return None

    room_counts["start"] = 0
    room_counts["end"] = 1
    end_room_placed = False

    path = []
    room_count = 1

    while room_count < max_rooms:
        possible_rooms = [r for r, count in room_counts.items() if count > 0 and r not in ["start", "end"]]
        if not possible_rooms:
            print("No available rooms left to draw.")
            break

        placed = False
        attempted_directions = set()

        while not placed and len(attempted_directions) < 4:
            base_room = random.choice(possible_rooms)
            direction = random.choice(["top", "right", "bottom", "left"])

            if direction in attempted_directions:
                continue

            attempted_directions.add(direction)
            nx, ny = get_adjacent_position(current_position[0], current_position[1], direction)

            if (0 <= nx < len(map_grid)) and (0 <= ny < len(map_grid[0])) and (nx, ny) not in used_positions:
                rotations = [r for r in connections if r.startswith(base_room)]

                for rotated_room in rotations:
                    if rotated_room == "start" or rotated_room == "end":
                        continue

                    if compatible_connection(current_room, rotated_room, direction):
                        if check_all_connections((nx, ny), rotated_room):
                            map_grid[nx][ny] = rotated_room
                            used_positions[(nx, ny)] = {
                                "room": rotated_room,
                                "type": room_types.get(rotated_room, {}).get("type", "unknown"),
                            }
                            room_counts[base_room] -= 1

                            print(f"Placed room {rotated_room}, type: {used_positions[(nx, ny)]['type']} at {(nx, ny)} in direction {direction}")

                            path.append((current_position, current_room))
                            current_position = (nx, ny)
                            current_room = rotated_room
                            room_count += 1
                            placed = True
                            break

        if not placed:
            print("Backtracking...")
            if not path:
                print("No rooms to backtrack to. Exiting...")
                break

            last_position, last_room = path.pop()
            current_position = last_position
            current_room = last_room

    if not end_room_placed:
        draw_end_room()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Room placing completed in {elapsed_time:.6f} seconds.")

    return used_positions

def draw_end_room():
    global end_room_placed

    for (x, y), room_data in list(used_positions.items())[::-1]:
        for direction in ["top", "right", "bottom", "left"]:
            nx, ny = get_adjacent_position(x, y, direction)
            if (0 <= nx < len(map_grid)) and (0 <= ny < len(map_grid[0])) and (nx, ny) not in used_positions:
                if check_all_connections((nx, ny), "end"):
                    map_grid[nx][ny] = "end"
                    used_positions[(nx, ny)] = {
                        "room": "end",
                        "type": "end",
                    }
                    end_room_placed = True
                    print(f"End room placed at {(nx, ny)} in direction {direction}.")
                    return True

    print("Failed to place an end room.")
    return False
