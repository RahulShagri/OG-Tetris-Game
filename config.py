# Sets up all important config variables
import dearpygui.dearpygui as dpg

# Set up all IDs required by items in Dear PyGui
item_id = {
    "windows": {
        "main_window": dpg.generate_uuid(),
        "score_window": dpg.generate_uuid(),
        "tetris_board": dpg.generate_uuid(),
        "next_block_board": dpg.generate_uuid(),
        "statistics_window": dpg.generate_uuid(),
    },
    "displays": {
        "enter_level": dpg.generate_uuid(),
        "level_text": dpg.generate_uuid(),
        "full_line_text": dpg.generate_uuid(),
        "score_text": dpg.generate_uuid(),
        "I_block_stat": dpg.generate_uuid(),
        "J_block_stat": dpg.generate_uuid(),
        "L_block_stat": dpg.generate_uuid(),
        "O_block_stat": dpg.generate_uuid(),
        "S_block_stat": dpg.generate_uuid(),
        "T_block_stat": dpg.generate_uuid(),
        "Z_block_stat": dpg.generate_uuid(),
        "Total_block_stat": dpg.generate_uuid(),
    },
    "registries": {
        "texture_registry": dpg.generate_uuid(),
        "key_release_handler": dpg.generate_uuid(),
        "mouse_release_handler": dpg.generate_uuid(),
    },
    "buttons": {
        "play_button": dpg.generate_uuid(),
    },
    "block_texture": {
        "I_block": dpg.generate_uuid(),
        "J_block": dpg.generate_uuid(),
        "L_block": dpg.generate_uuid(),
        "O_block": dpg.generate_uuid(),
        "S_block": dpg.generate_uuid(),
        "T_block": dpg.generate_uuid(),
        "Z_block": dpg.generate_uuid(),
    },
    "blocks": {
    },
}

# Names of all blocks
block_names = ["I", "J", "L", "O", "S", "T", "Z"]

# Set up lists to track walls and cells occupied
cell_boundary1 = [[n, -1] for n in range(10)]  # Bottom Wall
cell_boundary2 = [[10, n] for n in range(20)]  # Right Wall
cell_boundary3 = [[n, 20] for n in range(10)]  # Top Wall
cell_boundary4 = [[-1, n] for n in range(20)]  # Left Wall

cell_boundary = cell_boundary1 + cell_boundary2 + cell_boundary3 + cell_boundary4  # All points in all walls combined
cells_occupied = []  # List of all cells occupied by tetris blocks

# List of all block numbers active on the tetris board
block_numbers = []

# Count of blocks created
block_count = 0

# Flag to check if the last block is moving or not. 0=Stationary, 1-7=Corresponding type of block in motion
block_moving_flag = 0

# Keep track of level and corresponding speed
level = 0
speed = 0

# Keep track of full lines completed
full_lines = 0

# Keep track of score
score = 0
