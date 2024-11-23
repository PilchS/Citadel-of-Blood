from dungeon_creator import create_dungeon
from dungeon_visualizer import initialize_window, draw_dungeon

def main():
    used_positions = create_dungeon(20)
    
    if used_positions:
        window, clock = initialize_window()
        draw_dungeon(window, clock, used_positions)
    else:
        print("Dungeon generation failed.")

if __name__ == "__main__":
    main()
