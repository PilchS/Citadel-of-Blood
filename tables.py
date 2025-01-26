TREASURE_TABLE = {
    "A": {"Gold Marks": "0:0", "Jewels": "0:0", "Magic Items": "0:0"},
    "B": {"Gold Marks": "6:1D6", "Jewels": "0:0", "Magic Items": "0:0"},
    "C": {"Gold Marks": "6:3D6", "Jewels": "0:0", "Magic Items": "1:1"},
    "D": {"Gold Marks": "1:3D6", "Jewels": "1:1D3", "Magic Items": "0:0"},
    "E": {"Gold Marks": "2:1D6x10", "Jewels": "2:1D6", "Magic Items": "2:1"},
    "F": {"Gold Marks": "3:1D6x5", "Jewels": "3:1D6", "Magic Items": "1:1"},
    "G": {"Gold Marks": "6:3D6x5", "Jewels": "3:1D6", "Magic Items": "2:1"},
    "H": {"Gold Marks": "6:2D6", "Jewels": "1:1D3", "Magic Items": "1:1"},
    "I": {"Gold Marks": "6:1D6x5", "Jewels": "2:1D6", "Magic Items": "2:1"},
    "J": {"Gold Marks": "6:1D6x20", "Jewels": "2:1D6", "Magic Items": "3:1D3"},
    "K": {"Gold Marks": "6:2D6x20", "Jewels": "3:1D6", "Magic Items": "3:1D3"},
    "L": {"Gold Marks": "6:3D6x20", "Jewels": "4:1D6", "Magic Items": "4:1D3"},
}

COMBAT_RESULTS_TABLE = {
    "Dagger": [0, 0, 0, 1, 1, 2, 2, 3, 3, 4],
    "Throw Dagger": [0, 0, 0, 1, 1, 1, 2, 2, 3, 4],
    "Bow": [0, 0, 0, 1, 1, 2, 2, 3, 3, 4],
    "Sword": [0, 0, 1, 1, 2, 2, 3, 4, 5],
    "Hammer": [0, 0, 1, 1, 2, 2, 3, 4, 5],
    "Ax": [0, 0, 1, 1, 2, 2, 3, 4, 5],
    "Monster": [0, 0, 1, 1, 1, 2, 3, 4, 5]
}

BRIBERY_TABLE = [
    {"Gold Marks": 20, "Range": range(1, 6), "Roll": 4},
    {"Gold Marks": 20, "Range": range(6, 10), "Roll": 2},
    {"Gold Marks": 20, "Range": range(10, 13), "Roll": 1},
    {"Gold Marks": 20, "Range": range(13, 17), "Roll": 1},
    {"Gold Marks": 20, "Range": range(17, 21), "Roll": 0},
    {"Gold Marks": 20, "Range": range(21, 100), "Roll": 0},

    {"Gold Marks": 40, "Range": range(1, 6), "Roll": 4},
    {"Gold Marks": 40, "Range": range(6, 10), "Roll": 3},
    {"Gold Marks": 40, "Range": range(10, 13), "Roll": 2},
    {"Gold Marks": 40, "Range": range(13, 17), "Roll": 1},
    {"Gold Marks": 40, "Range": range(17, 21), "Roll": 1},
    {"Gold Marks": 40, "Range": range(21, 100), "Roll": 0},

    {"Gold Marks": 60, "Range": range(1, 6), "Roll": 5},
    {"Gold Marks": 60, "Range": range(6, 10), "Roll": 4},
    {"Gold Marks": 60, "Range": range(10, 13), "Roll": 2},
    {"Gold Marks": 60, "Range": range(13, 17), "Roll": 2},
    {"Gold Marks": 60, "Range": range(17, 21), "Roll": 1},
    {"Gold Marks": 60, "Range": range(21, 100), "Roll": 1},

    {"Gold Marks": 80, "Range": range(1, 6), "Roll": 6},
    {"Gold Marks": 80, "Range": range(6, 10), "Roll": 5},
    {"Gold Marks": 80, "Range": range(10, 13), "Roll": 4},
    {"Gold Marks": 80, "Range": range(13, 17), "Roll": 2},
    {"Gold Marks": 80, "Range": range(17, 21), "Roll": 2},
    {"Gold Marks": 80, "Range": range(21, 100), "Roll": 1},

    {"Gold Marks": 100, "Range": range(1, 6), "Roll": 6},
    {"Gold Marks": 100, "Range": range(6, 10), "Roll": 6},
    {"Gold Marks": 100, "Range": range(10, 13), "Roll": 4},
    {"Gold Marks": 100, "Range": range(13, 17), "Roll": 3},
    {"Gold Marks": 100, "Range": range(17, 21), "Roll": 2},
    {"Gold Marks": 100, "Range": range(21, 100), "Roll": 1},

    {"Gold Marks": 150, "Range": range(1, 6), "Roll": 6},
    {"Gold Marks": 150, "Range": range(6, 10), "Roll": 6},
    {"Gold Marks": 150, "Range": range(10, 13), "Roll": 5},
    {"Gold Marks": 150, "Range": range(13, 17), "Roll": 4},
    {"Gold Marks": 150, "Range": range(17, 21), "Roll": 3},
    {"Gold Marks": 150, "Range": range(21, 100), "Roll": 2},

    {"Gold Marks": 200, "Range": range(1, 6), "Roll": 6},
    {"Gold Marks": 200, "Range": range(6, 10), "Roll": 6},
    {"Gold Marks": 200, "Range": range(10, 13), "Roll": 6},
    {"Gold Marks": 200, "Range": range(13, 17), "Roll": 4},
    {"Gold Marks": 200, "Range": range(17, 21), "Roll": 4},
    {"Gold Marks": 200, "Range": range(21, 100), "Roll": 2},

    {"Gold Marks": 300, "Range": range(1, 6), "Roll": 6},
    {"Gold Marks": 300, "Range": range(6, 10), "Roll": 6},
    {"Gold Marks": 300, "Range": range(10, 13), "Roll": 6},
    {"Gold Marks": 300, "Range": range(13, 17), "Roll": 5},
    {"Gold Marks": 300, "Range": range(17, 21), "Roll": 4},
    {"Gold Marks": 300, "Range": range(21, 100), "Roll": 3},

    {"Gold Marks": 400, "Range": range(1, 6), "Roll": 6},
    {"Gold Marks": 400, "Range": range(6, 10), "Roll": 6},
    {"Gold Marks": 400, "Range": range(10, 13), "Roll": 6},
    {"Gold Marks": 400, "Range": range(13, 17), "Roll": 5},
    {"Gold Marks": 400, "Range": range(17, 21), "Roll": 5},
    {"Gold Marks": 400, "Range": range(21, 100), "Roll": 4},
]
