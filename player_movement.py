class Player:
    def __init__(self):
        self.position = (7, 7)
        self.connected_tiles = {}

    def set_dungeon_connections(self, dungeon_data):
        self.connected_tiles = {
            position: room.get("connections", []) for position, room in dungeon_data.items()
        }

    def move(self, direction):
        x, y = self.position
        if direction == "up":
            new_position = (x, y - 1)
        elif direction == "down":
            new_position = (x, y + 1)
        elif direction == "left":
            new_position = (x - 1, y)
        elif direction == "right":
            new_position = (x + 1, y)
        else:
            return False

        if new_position in self.connected_tiles.get(self.position, []):
            self.position = new_position
            return True
        return False
