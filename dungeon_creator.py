import random

connections = {
    # start = 1
    "start": {"top": "any", "bottom": "any", "left": "any", "right": "any"},

    "end": {"top": "any", "bottom": "any", "left": "any", "right": "any"},

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
    "g1": {"left": "small", "right": "big", "bottom": "big"},
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
    "j2": {"top": "big", "bottom": "big"},

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
    "j2": {"type": "corridor"}
}

room_counts = {
    "start": 0, "end":0, "a": 11, "b": 4, "c": 12, "d": 16, "e": 14, "f": 7, "g": 6, "h": 18, "i": 11, "j": 14
}

rotation_map = {room: base for base in room_counts for room in connections if room.startswith(base)}


map_grid = [[" "] * 14 for _ in range(14)]
start_x, start_y = 7, 7
map_grid[start_x][start_y] = "X"
used_positions = {(start_x, start_y): "x"}


def draw_starting_room():
    global start_x, start_y
    predefined_start_room = "start"
    map_grid[start_x][start_y] = predefined_start_room
    used_positions[(start_x, start_y)] = predefined_start_room
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
    if current_room == "start" or next_room == "start":
        return True

    opposite_dir = opposite_direction(direction)

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

        neighbor_room = used_positions[(nx, ny)]
        if not compatible_connection(new_room, neighbor_room, direction):
            print(f"Conflict detected: {new_room} at {current_position} is not compatible with {neighbor_room} at {(nx, ny)}.")
            return False

    return True


def try_place_room(current_room, base_room, current_position, direction):
    global room_counts
    rotations = [r for r in connections if r.startswith(base_room)]

    for rotated_room in rotations:
        if rotated_room == "start" or rotated_room == "end":
            continue

        nx, ny = get_adjacent_position(current_position[0], current_position[1], direction)
        if (0 <= nx < len(map_grid)) and (0 <= ny < len(map_grid[0])) and (nx, ny) not in used_positions:
            if compatible_connection(current_room, rotated_room, direction):
                if check_all_connections((nx, ny), rotated_room):
                    map_grid[nx][ny] = rotated_room
                    used_positions[(nx, ny)] = rotated_room
                    room_counts[base_room] -= 1
                    print(f"Connecting room {current_room} to room {rotated_room} from the {direction}")
                    return (nx, ny, rotated_room, True)

    return (None, None, None, False)

def create_dungeon(max_rooms):
    global start_x, start_y
    current_position = (start_x, start_y)
    current_room = draw_starting_room()

    if not current_room:
        return None

    room_counts["start"] = 0  # Ensure the start room is considered used
    path = [(current_position, current_room)]  # Include the start room in the path
    explored_directions = {current_position: set()}  # Track explored directions
    room_count = 1
    backtrack_limit = 50

    while room_count < max_rooms:
        possible_rooms = [r for r, count in room_counts.items() if count > 0]
        if not possible_rooms:
            print("No available rooms left to draw.")
            break

        base_room = random.choice(possible_rooms)
        placed = False

        # Attempt to place a room from the current position
        for direction in connections[current_room]:
            if direction in explored_directions.get(current_position, set()):
                continue

            # Allow connection regardless of passage size if involving the start room
            nx, ny, placed_room, placed = try_place_room(
                current_room, base_room, current_position, direction, allow_any_passage=(current_room == "start")
            )

            if placed:
                path.append((current_position, current_room))
                explored_directions.setdefault(current_position, set()).add(direction)
                current_position = (nx, ny)
                current_room = placed_room
                room_count += 1
                break

        # If placement fails, backtrack
        if not placed:
            backtrack_count = 0
            while not placed and path and backtrack_count < backtrack_limit:
                print("Backtracking...")

                # Always prioritize the start room if it has unexplored directions
                if backtrack_count == 0 and start_x == path[0][0][0] and start_y == path[0][0][1]:
                    last_position, last_room = path[0]
                else:
                    last_position, last_room = random.choice(path)

                current_position = last_position
                base_room = rotation_map[last_room]
                backtrack_count += 1

                for direction in connections[last_room]:
                    if direction in explored_directions.get(last_position, set()):
                        continue

                    nx, ny, rotated_room, success = try_place_room(
                        last_room, base_room, current_position, direction, allow_any_passage=(last_room == "start")
                    )
                    if success:
                        explored_directions.setdefault(last_position, set()).add(direction)
                        current_position = (nx, ny)
                        current_room = rotated_room
                        room_count += 1
                        placed = True
                        break

            if backtrack_count >= backtrack_limit:
                print("Backtracking limit reached. Exiting...")
                return used_positions

            if not placed:
                print("Failed to place any room after backtracking.")
                return used_positions

    # Mark the last room as the "end" tile
    if used_positions:
        last_room_position = list(used_positions.keys())[-1]
        used_positions[last_room_position] = "end"
        print(f"The 'end' tile has been placed at position {last_room_position}.")

    return used_positions


