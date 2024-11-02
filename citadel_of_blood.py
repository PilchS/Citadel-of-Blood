import random

connections = {
    "x": ["top", "bottom", "left", "right"],
    "a": ["right", "bottom"],
    "b": ["right", "top"],
    "c": ["left", "bottom"],
    "d": ["left", "top"],
    "e": ["left", "right"],
    "f": ["top", "bottom"]
}

room_limits = {
    "x": 2,
    "a": 1,
    "b": 1,
    "c": 1,
    "d": 1,
    "e": 1,
    "f": 1
}

room_counts = {room: 0 for room in room_limits}

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

def create_dungeon(max_rooms):
    path = []
    current_room = "x"
    current_position = (start_x, start_y)
    room_count = 1

    while room_count < max_rooms:
        possible_rooms = [room for room in connections.keys() if room_counts[room] < room_limits[room]]
        
        if not possible_rooms:
            print("No more available rooms to place.")
            return
        
        random.shuffle(possible_rooms)
        placed = False

        for next_room in possible_rooms:
            for direction in connections[current_room]:
                nx, ny = get_adjacent_position(current_position[0], current_position[1], direction)

                if (0 <= nx < len(map_grid)) and (0 <= ny < len(map_grid[0])):
                    if (nx, ny) not in used_positions:
                        if opposite_direction(direction) in connections[next_room]:
                            map_grid[nx][ny] = next_room
                            used_positions[(nx, ny)] = next_room
                            room_counts[next_room] += 1
                            print(f"Connecting room {next_room} to room {current_room} from the {direction}")
                            path.append((current_position, current_room))
                            current_position = (nx, ny)
                            current_room = next_room
                            room_count += 1
                            placed = True
                            break
                    elif used_positions[(nx, ny)] == next_room:
                        if opposite_direction(direction) in connections[next_room]:
                            print(f"Reconnecting room {next_room} to room {current_room} from the {direction}")
                            path.append((current_position, current_room))
                            current_position = (nx, ny)
                            current_room = next_room
                            placed = True
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
                print(f"Bad dungeon: could not connect room {current_room} to any available room.")
                return

create_dungeon(10)

for row in map_grid:
    print(" ".join(row))
