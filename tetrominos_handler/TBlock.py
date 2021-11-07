import time
import threading
import config
from config import *


class TBlock:
    def __init__(self):
        self.cells = 4  # Number of cells occupied by the block
        config.block_count += 1
        config.item_id["blocks"][f"{config.block_count}"] = {}  # Add a new key to dictionary to add block IDs

        for n in range(self.cells - 1):
            # Loop draws the bottom cells of the block on the top of the board

            # Generate an ID for each cell occupied by the block
            config.item_id["blocks"][f"{config.block_count}"][f"{n}"] = dpg.generate_uuid()

            # Make a list of the initial cells occupied by the blocks
            config.cells_occupied.append([3 + n, 18])

            # Draw the cell
            dpg.draw_image(texture_tag=item_id["block_texture"]["T_block"], pmin=[3 + n, 19], pmax=[4 + n, 18],
                           parent=item_id["windows"]["tetris_board"],
                           id=config.item_id["blocks"][f"{config.block_count}"][f"{n}"])

        # Draw the final cell on the top
        # Generate an ID for the top cell occupied by the block
        config.item_id["blocks"][f"{config.block_count}"]["3"] = dpg.generate_uuid()
        # Add point to cells_occupied list
        config.cells_occupied.append([4, 19])
        # Draw the cell
        dpg.draw_image(texture_tag=item_id["block_texture"]["T_block"], pmin=[4, 20], pmax=[5, 19],
                       parent=item_id["windows"]["tetris_board"],
                       id=config.item_id["blocks"][f"{config.block_count}"]["3"])

        # Update statistics
        # Take the value shown, add 1 and set value
        dpg.configure_item(item=item_id["displays"]["T_block_stat"],
                           text=int(dpg.get_item_configuration(item=item_id["displays"]["T_block_stat"])["text"]) + 1)

        dpg.set_value(item=item_id["displays"]["Total_block_stat"],
                      value=int(dpg.get_value(item=item_id["displays"]["Total_block_stat"])) + 1)


    def move_blockDispatcher(self):
        # Function creates a new thread that controls the continuous movement of the new blocks
        move_block_thread = threading.Thread(name="move block", target=self.move_block, args=(), daemon=True)
        move_block_thread.start()

    def move_block(self):
        # Function controls the continuous downward movement of the blocks
        config.block_moving_flag = 6  # Set to 6=TBlock. Block is moving

        while True:
            for n in range(self.cells):
                config.cells_occupied[-1 - n][1] -= 1  # Shift the Y Coordinate down by 1 unit

            if any(item in config.cells_occupied[-self.cells:] for item in config.cell_boundary) or \
                    any(item in config.cells_occupied[-self.cells:] for item in config.cells_occupied[:-self.cells]):
                # Check if any cells have touched the wall or other blocks. If so, stop the movement
                for n in range(self.cells):
                    config.cells_occupied[-1 - n][1] += 1  # Reset the Y coordinate
                    config.block_moving_flag = 0  # Block has stopped moving
                return

            for n in range(self.cells):
                # Draw after all cells are updated
                dpg.configure_item(item=config.item_id["blocks"][f"{config.block_count}"][f"{n}"],
                                   pmin=[config.cells_occupied[-1 - n][0], config.cells_occupied[-1 - n][1] + 1],
                                   pmax=[config.cells_occupied[-1 - n][0] + 1, config.cells_occupied[-1 - n][1]])

            time.sleep(config.speed)  # Wait at each cell


def draw_next_TBlock():
    for n in range(3):
        # Loop draws the complete block on the "next" board
        dpg.draw_image(texture_tag=item_id["block_texture"]["T_block"], pmin=[3 + n, 3], pmax=[4 + n, 2],
                       parent=item_id["windows"]["next_block_board"])

    # Draw the final cell on the top
    # Draw the cell
    dpg.draw_image(texture_tag=item_id["block_texture"]["T_block"], pmin=[4, 4], pmax=[5, 3],
                   parent=item_id["windows"]["next_block_board"])


def draw_statistics_TBlock():
    for n in range(3):
        # Loop draws the bottom of the complete block on the board
        dpg.draw_image(texture_tag=item_id["block_texture"]["T_block"], pmin=[1 + n, 13], pmax=[2 + n, 12],
                       parent=item_id["windows"]["statistics_window"])

    # Draw the final cell on the top
    # Draw the cell
    dpg.draw_image(texture_tag=item_id["block_texture"]["T_block"], pmin=[2, 14], pmax=[3, 13],
                   parent=item_id["windows"]["statistics_window"])

    dpg.draw_line(p1=[6.5, 13], p2=[7.5, 13], thickness=0.1, color=[168, 168, 168],
                  parent=item_id["windows"]["statistics_window"])

    dpg.draw_text(pos=[8.5, 13.3], text="0", size=0.5, color=[168, 168, 168],
                  id=item_id["displays"]["T_block_stat"])
