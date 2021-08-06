# All settings required for tetris blocks (aka tetrominos)
import time
import threading
import math
import random
from playsound2 import playsound
import pandas as pd
import os
import config
from theme_settings import *
from config import *
import tetrominos_handler

dpg.setup_registries()  # Registries for mouse and keyboard press events

# Load and add all block textures
with dpg.texture_registry(id=item_id["registries"]["texture_registry"]):
    # Start a texture registry. Textures will be added later
    pass

for block in block_names:
    # Extract data from images and add static textures for each cell of a block
    width, height, channels, data = dpg.load_image(f"textures/{block}-block.jpg")

    dpg.add_static_texture(width, height, data, id=item_id["block_texture"][f"{block}_block"],
                           parent=item_id["registries"]["texture_registry"])


def get_distance_between_points(point1: list, point2: list):
    # Calculates the distance between two points
    return math.sqrt(math.pow((point2[0] - point1[0]), 2) + math.pow((point2[1] - point1[1]), 2))


# Set up the class for each tetris blocks
def rotate_block(cells: int, rotation_point: int):
    # Function rotates the block 90 degrees clockwise when called
    rotation_point = config.cells_occupied[-rotation_point]
    temp_point = []
    new_point = []

    for n in range(cells):
        radius = get_distance_between_points(config.cells_occupied[-1 - n], rotation_point)

        # Shift the origin to the rotation point and calculate the angle of points
        if config.cells_occupied[-1 - n][1] - rotation_point[1] >= 0:  # If point is above the rotation point
            x = rotation_point[0] - config.cells_occupied[-1 - n][0]
            y = config.cells_occupied[-1 - n][1] - rotation_point[1]
            temp_point.append([x, y])
            angle_of_rotation = math.degrees(math.atan2(temp_point[-1][1], temp_point[-1][0]))
            temp_point[-1][0] = -1*temp_point[-1][0]

        else:  # If the point is below the rotation point
            x = config.cells_occupied[-1 - n][0] - rotation_point[0]
            y = config.cells_occupied[-1 - n][1] - rotation_point[1]
            temp_point.append([x, y])
            angle_of_rotation = - math.degrees(math.atan2(temp_point[-1][1], temp_point[-1][0])) + 180

        x = round(radius*math.sin(math.radians(angle_of_rotation)))
        y = round(radius*math.cos(math.radians(angle_of_rotation)))
        new_point.append([x, y])
        config.cells_occupied[-1 - n][0] += (new_point[-1][0] - temp_point[-1][0])
        config.cells_occupied[-1 - n][1] += (new_point[-1][1] - temp_point[-1][1])

    if any(item in config.cells_occupied[-cells:] for item in config.cell_boundary) or \
            any(item in config.cells_occupied[-cells:] for item in config.cells_occupied[:-cells]):
        # If any of the cells updated above, are found to be clashing with the walls or other blocks, reset the
        # cells occupied list and return. Do NOT move the block further
        for n in range(cells):
            config.cells_occupied[-1 - n][0] -= (new_point[n][0] - temp_point[n][0])
            config.cells_occupied[-1 - n][1] -= (new_point[n][1] - temp_point[n][1])
        return

    for n in range(cells):
        dpg.configure_item(item=config.item_id["blocks"][f"{config.block_count}"][f"{n}"],
                           pmin=[config.cells_occupied[-1 - n][0], config.cells_occupied[-1 - n][1] + 1],
                           pmax=[config.cells_occupied[-1 - n][0] + 1, config.cells_occupied[-1 - n][1]])


def audio_effectsDispatcher(file_name):
    # Function creates a new thread that runs the audio file so that the main code does not lag or interfere
    play_audio_thread = threading.Thread(name="play audio", target=play_audio_effect, args=(file_name,), daemon=True)
    play_audio_thread.start()


def play_audio_effect(file_name):
    playsound(os.path.abspath(os.path.abspath("tetris_game.py")[:-14]) + "\\sounds\\" + file_name)


def create_blocksDispatcher():
    # Function creates a new thread that controls the continuous movement of the new blocks
    dpg.add_key_press_handler(callback=tetrominos_handler.key_release_handler)
    dpg.configure_item(item=item_id["buttons"]["play_button"], enabled=False)
    dpg.set_item_disabled_theme(item=item_id["buttons"]["play_button"], theme=play_button_theme)

    create_blocks_thread = threading.Thread(name="create blocks", target=create_blocks, args=(), daemon=True)
    create_blocks_thread.start()


def create_blocks():
    # Play audio effect to indicate selection
    tetrominos_handler.audio_effectsDispatcher("selection.wav")

    # Set up the speed for level chosen by the user
    block_speeds_data = pd.read_csv("block_speeds_data.csv")
    config.speed = (block_speeds_data.values[config.level][1]) / 20

    random_blocks = [random.randint(0, 6), random.randint(0, 6)]
    temp_block = eval(f"tetrominos_handler.{block_names[random_blocks[0]]}Block()")

    dpg.delete_item(item=item_id["windows"]["next_block_board"], children_only=True)
    eval(f"tetrominos_handler.draw_next_{block_names[random_blocks[1]]}Block()")

    time.sleep(config.speed)
    temp_block.move_blockDispatcher()

    # If any of the blocks occupy these cells, then the game ends
    top_cells = [[3, 19], [4, 19], [5, 19], [6, 19], [3, 18], [4, 18], [5, 18], [6, 18]]

    while True:  # Check if top cells are occupied
        if config.block_moving_flag == 0:

            if any(item in config.cells_occupied for item in top_cells):
                break

            random_blocks.pop(0)
            random_blocks.append(random.randint(0, 6))
            check_complete_line()
            temp_block = eval(f"tetrominos_handler.{block_names[random_blocks[0]]}Block()")

            dpg.delete_item(item=item_id["windows"]["next_block_board"], children_only=True)
            eval(f"tetrominos_handler.draw_next_{block_names[random_blocks[1]]}Block()")

            time.sleep(config.speed)
            temp_block.move_blockDispatcher()

    time.sleep(0.5)

    # Fade the board by placing a semi-transparent rectangle
    dpg.draw_rectangle(pmin=[0,0], pmax=[10, 20], color=[0, 0, 0, 150], thickness=0,
                       fill=[0, 0, 0, 150], parent=item_id["windows"]["tetris_board"])

    # Show GAME OVER text on the board
    dpg.draw_text(pos=[0.5, 11], text="GAME OVER", size=1, parent=item_id["windows"]["tetris_board"])

    time.sleep(0.5)
    # Play the game over tune
    audio_effectsDispatcher("gameover.wav")


def check_complete_line():
    # Function checks every horizontal line to see if a complete row has been filled. If so, the line disappears

    row = 0
    lines_completed = 0  # Total lines completed together (max 4 using I block)

    while row < 20:
        cell_count = 0  # Count the number of cells occupied in the given row. If equals 10, then line is complete
        for point in config.cells_occupied:
            if point[1] == row:
                cell_count += 1

        if cell_count == 10:
            # Increase complete lines in one-go
            lines_completed += 1
            # Increase full lines text display
            config.full_lines += 1
            dpg.set_value(item=item_id["displays"]["full_line_text"], value=config.full_lines)

            # Check if level up is needed using the number of full lines completed
            if min((config.level*10 + 10), (max(100, (config.level*10 - 50)))) == config.full_lines:
                config.level += 1
                dpg.set_value(item=item_id["displays"]["level_text"], value=config.level)

                # Speed up to match the speed for the corresponding level
                block_speeds_data = pd.read_csv("block_speeds_data.csv")
                config.speed = (block_speeds_data.values[config.level][1]) / 20

            block_cells = []

            for block in config.item_id["blocks"].keys():
                for cell in config.item_id["blocks"][block].keys():
                    cell_id = config.item_id["blocks"][block][cell]
                    cell_number = dpg.get_item_configuration(item=cell_id)["pmax"]

                    if cell_number[1] == row:
                        dpg.delete_item(item=cell_id)
                        block_cells.append([block, cell])
                        config.cells_occupied.remove([cell_number[0] - 1, cell_number[1]])

            audio_effectsDispatcher("line.wav")

            for pair in block_cells:
                del config.item_id["blocks"][pair[0]][pair[1]]

            time.sleep(0.1)

            for block in config.item_id["blocks"].keys():
                for cell in config.item_id["blocks"][block].keys():
                    cell_id = config.item_id["blocks"][block][cell]
                    cell_number = dpg.get_item_configuration(item=cell_id)["pmax"]
                    cell_number[0] -= 1

                    if cell_number[1] > row:
                        cells_occupied_index = config.cells_occupied.index([cell_number[0], cell_number[1]])
                        config.cells_occupied[cells_occupied_index][1] -= 1
                        cell_number[1] -= 1

                        dpg.configure_item(item=cell_id,
                                           pmin=[cell_number[0], cell_number[1] + 1],
                                           pmax=[cell_number[0] + 1, cell_number[1]])
            time.sleep(0.1)

        else:
            row += 1

    if lines_completed == 1:
        config.score += 40*(config.level + 1)

    elif lines_completed == 2:
        config.score += 100*(config.level + 1)

    elif lines_completed == 3:
        config.score += 300*(config.level + 1)

    elif lines_completed == 4:
        config.score += 1200*(config.level + 1)

    dpg.set_value(item=item_id["displays"]["score_text"], value=config.score)


def key_release_handler(sender, app_data):
    if config.block_moving_flag != 0:
        cells = 0  # Number of cells occupied by the moving block
        rotation_cell = 0  # Cell about which the block will rotate

        if config.block_moving_flag == 1:
            cells = 4  # I Block occupies 4 cells
            rotation_cell = 2  # Second from the right in the list of points

        if config.block_moving_flag == 2:
            cells = 4  # J Block occupies 4 cells
            rotation_cell = 3  # Third from the right in the list of points

        if config.block_moving_flag == 3:
            cells = 4  # J Block occupies 4 cells
            rotation_cell = 3  # Third from the right in the list of points

        if config.block_moving_flag == 4:
            cells = 4  # O Block occupies 4 cells
            rotation_cell = 0  # Set to 0 because no rotation

        if config.block_moving_flag == 5:
            cells = 4  # S Block occupies 4 cells
            rotation_cell = 3

        if config.block_moving_flag == 6:
            cells = 4  # T Block occupies 4 cells
            rotation_cell = 3

        if config.block_moving_flag == 7:
            cells = 4  # Z Block occupies 4 cells
            rotation_cell = 2

        if app_data == 38:
            if config.block_moving_flag == 4:  # Do NOT rotate O-Block
                return
            rotate_block(cells, rotation_cell)
            return

        if app_data == 32:
            # Hard drop block
            cells_dropped = 0  # Count of number of cells the block dropped. Used to calculate the score

            while True:
                # Loop and move Y coordinate down until we hit another block or the bottom wall
                for n in range(cells):
                    config.cells_occupied[-1 - n][1] -= 1  # Shift the Y Coordinate down by 1 unit

                if any(item in config.cells_occupied[-cells:] for item in config.cell_boundary) or \
                        any(item in config.cells_occupied[-cells:] for item in config.cells_occupied[:-cells]):
                    # If any of the cells updated above, are found to be clashing with the walls or other blocks,
                    # reset the cells occupied list and return. Do NOT move the block further
                    for n in range(cells):
                        config.cells_occupied[-1 - n][1] += 1
                    break

                cells_dropped += 1

            for n in range(cells):
                # Finally when the block hits another block or bottom, draw and show the block
                dpg.configure_item(item=config.item_id["blocks"][f"{config.block_count}"][f"{n}"],
                                   pmin=[config.cells_occupied[-1 - n][0], config.cells_occupied[-1 - n][1] + 1],
                                   pmax=[config.cells_occupied[-1 - n][0] + 1, config.cells_occupied[-1 - n][1]])

            # Update the score accordingly
            config.score += cells_dropped*2
            dpg.set_value(item=item_id["displays"]["score_text"], value=config.score)

            audio_effectsDispatcher("fall.wav")

        for n in range(cells):
            if app_data == 37:  # Move left
                config.cells_occupied[-1 - n][0] -= 1  # Shift the X Coordinate left by 1 unit

            elif app_data == 39:  # Move right
                config.cells_occupied[-1 - n][0] += 1  # Shift the X Coordinate right by 1 unit

            elif app_data == 40:  # Soft drop (Accelerate down)
                config.cells_occupied[-1 - n][1] -= 1  # Shift the Y Coordinate down by 1 unit

        if any(item in config.cells_occupied[-cells:] for item in config.cell_boundary) or \
                any(item in config.cells_occupied[-cells:] for item in config.cells_occupied[:-cells]):
            # If any of the cells updated above, are found to be clashing with the walls or other blocks, reset the
            # cells occupied list and return. Do NOT move the block further
            for n in range(cells):
                if app_data == 37:
                    config.cells_occupied[-1 - n][0] += 1
                elif app_data == 39:
                    config.cells_occupied[-1 - n][0] -= 1
                elif app_data == 40:
                    config.cells_occupied[-1 - n][1] += 1
            return

        for n in range(cells):
            dpg.configure_item(item=config.item_id["blocks"][f"{config.block_count}"][f"{n}"],
                               pmin=[config.cells_occupied[-1 - n][0], config.cells_occupied[-1 - n][1] + 1],
                               pmax=[config.cells_occupied[-1 - n][0] + 1, config.cells_occupied[-1 - n][1]])

        # Check if soft drop was successfully completed and add to scoring points and play audio effect
        if app_data == 40:
            config.score += 1
            dpg.set_value(item=item_id["displays"]["score_text"], value=config.score)
            audio_effectsDispatcher("fall.wav")
