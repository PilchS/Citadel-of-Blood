import pygame
import os

TILE_SIZE = 54
GRID_WIDTH = 10
GRID_HEIGHT = 10
WINDOW_WIDTH = TILE_SIZE * GRID_WIDTH
WINDOW_HEIGHT = TILE_SIZE * GRID_HEIGHT
TILE_FOLDER = "tiles"

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Dungeon Map")
clock = pygame.time.Clock()

tile_images = {}
for file_name in os.listdir(TILE_FOLDER):
    if file_name.endswith(".png"):
        tile_name = file_name.split(".")[0]
        tile_images[tile_name] = pygame.image.load(os.path.join(TILE_FOLDER, file_name))

def draw_dungeon(map_grid):
    window.fill((0, 0, 0))
    for row_idx, row in enumerate(map_grid):
        for col_idx, tile_name in enumerate(row):
            if tile_name != " ":
                tile_image = tile_images.get(tile_name)
                if tile_image:
                    x = col_idx * TILE_SIZE
                    y = row_idx * TILE_SIZE
                    window.blit(tile_image, (x, y))
    pygame.display.flip()

dungeon_map = [
    [" ", " ", " ", "a1", "c1", " "],
    [" ", " ", " ", " ", "b1", "c2"],
    [" ", " ", " ", "X", "f1", " "],
    [" ", " ", " ", " ", "f2", " "],
    [" ", " ", " ", " ", "b2", " "],
]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    draw_dungeon(dungeon_map)
    clock.tick(30)

pygame.quit()
