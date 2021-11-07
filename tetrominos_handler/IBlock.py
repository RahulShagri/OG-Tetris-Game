import time
import threading
import config
from config import *


class IBlock:
    def __init__(self):
        self.cells = 4  # Number of cells occupied by the block
        config.block_count += 1
        config.item_id["blocks"][f"{config.block_count}"] = {}  # Add a new key to dictionary to add block IDs

        for n in range(self.cells):
            # Loop draws the complete block on the top of the board

            # Generate an ID for each cell occupied by the block
            config.item_id["blocks"][f"{config.block_count}"][f"{n}"] = dpg.generate_uuid()

            # Make a list of the initial cells occupied by the blocks
            config.cells_occupied.append([3 + n, 19])

            # Draw the cell
            dpg.draw_image(texture_tag=item_id["block_texture"]["I_block"], pmin=[3 + n, 20], pmax=[4 + n, 19],
                           parent=item_id["windows"]["tetris_board"],
                           id=config.item_id["blocks"][f"{config.block_count}"][f"{n}"])

        # Update statistics
        # Take the value shown, add 1 and set value
        dpg.configure_item(item=item_id["displays"]["I_block_stat"],
                           text=int(
                               dpg.get_item_configuration(item=item_id["displays"]["I_block_stat"])["text"]) + 1)

        dpg.set_value(item=item_id["displays"]["Total_block_stat"],
                      value=int(dpg.get_value(item=item_id["displays"]["Total_block_stat"])) + 1)

    def move_blockDispatcher(self):
        # Function creates a new thread that controls the continuous movement of the new blocks
        move_block_thread = threading.Thread(name="move block", target=self.move_block, args=(), daemon=True)
        move_block_thread.start()

    def move_block(self):
        # Function controls the continuous downward movement of the blocks
        config.block_moving_flag = 1  # Set to 1=IBlock. Block is moving

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


def draw_next_IBlock():
    for n in range(4):
        # Loop draws the complete block on the "next" board

        # Draw the cell
        dpg.draw_image(texture_tag=item_id["block_texture"]["I_block"], pmin=[2 + n, 4], pmax=[3 + n, 3],
                       parent=item_id["windows"]["next_block_board"])


def draw_statistics_IBlock():
    for n in range(4):
        # Loop draws the complete block on the "next" board

        # Draw the cell
        dpg.draw_image(texture_tag=item_id["block_texture"]["I_block"], pmin=[2 + n, 16], pmax=[3 + n, 15],
                       parent=item_id["windows"]["statistics_window"])

    dpg.draw_line(p1=[6.5, 15.5], p2=[7.5, 15.5], thickness=0.1, color=[168, 168, 168],
                  parent=item_id["windows"]["statistics_window"])

    dpg.draw_text(pos=[8.5, 15.8], text="0", size=0.5, color=[168, 168, 168],
                  id=item_id["displays"]["I_block_stat"])