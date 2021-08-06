import time

import config
from theme_settings import *
from config import *
import tetrominos_handler
import threading

dpg.setup_viewport()
dpg.set_viewport_title("Tetris Game")
dpg.configure_viewport(0, x_pos=0, y_pos=0, width=1000, height=735)
dpg.set_viewport_max_height(735)
dpg.set_viewport_max_width(1000)
dpg.set_viewport_min_height(735)
dpg.set_viewport_min_width(100)


def set_main_window():
    # Play audio for selection made
    tetrominos_handler.audio_effectsDispatcher("selection.wav")

    config.level = dpg.get_value(item=item_id["displays"]["enter_level"])

    with dpg.window(pos=[0, 0], autosize=True, no_collapse=True, no_resize=True, no_close=True, no_move=True,
                    no_title_bar=True, id=item_id["windows"]["main_window"]):

        with dpg.group(horizontal=True):
            with dpg.child(width=320, id=item_id["windows"]["score_window"]):
                dpg.add_dummy(height=10)

                dpg.add_text(default_value=" Your level : ")
                dpg.add_same_line()
                dpg.add_text(default_value=config.level, id=item_id["displays"]["level_text"])

                dpg.add_dummy()
                dpg.add_text(default_value=" Full lines : ")
                dpg.add_same_line()
                dpg.add_text(default_value="0", id=item_id["displays"]["full_line_text"])

                dpg.add_dummy(height=10)
                dpg.add_text(default_value=" SCORE : ")
                dpg.add_same_line()
                dpg.add_text(default_value="0", color=(161, 94, 33), id=item_id["displays"]["score_text"])

                dpg.add_dummy(height=50)
                help_text = dpg.add_button(label="H E L P", width=-1)
                dpg.set_item_theme(item=help_text, theme=dummy_button_theme)

                dpg.add_dummy(height=20)
                dpg.add_text(default_value=" LEFT KEY  : Left")
                dpg.add_text(default_value=" RIGHT KEY : Right")
                dpg.add_text(default_value=" UP KEY    : Rotate")
                dpg.add_text(default_value=" DOWN KEY  : Speed up")
                dpg.add_text(default_value=" SPACE     : Drop")

                dpg.add_dummy(height=50)
                next_text = dpg.add_button(label="Next :", width=-1)
                dpg.set_item_theme(item=next_text, theme=dummy_button_theme)

                with dpg.plot(no_menus=False, no_title=True, no_box_select=True, no_mouse_pos=True, width=315,
                              height=160, equal_aspects=True, id=item_id["windows"]["next_block_board"]):

                    dpg.set_item_theme(item=item_id["windows"]["next_block_board"], theme=no_border_board_theme)

                    x = dpg.add_plot_axis(axis=0, no_gridlines=True, no_tick_marks=True, no_tick_labels=True,
                                          lock_min=True)
                    y = dpg.add_plot_axis(axis=1, no_gridlines=True, no_tick_marks=True, no_tick_labels=True,
                                          lock_min=True)

                    dpg.set_axis_limits(axis=x, ymin=0, ymax=8)
                    dpg.set_axis_limits(axis=y, ymin=0, ymax=4)

            with dpg.group():
                with dpg.plot(no_menus=False, no_title=True, no_box_select=True, no_mouse_pos=True, width=325,
                              height=650, equal_aspects=True, id=item_id["windows"]["tetris_board"]):
                    default_x = dpg.add_plot_axis(axis=0, no_gridlines=False, no_tick_marks=True, no_tick_labels=True,
                                                  lock_min=True)
                    default_y = dpg.add_plot_axis(axis=1, no_gridlines=False, no_tick_marks=True, no_tick_labels=True,
                                                  lock_min=True)

                    dpg.set_axis_limits(axis=default_x, ymin=0, ymax=10)
                    dpg.set_axis_limits(axis=default_y, ymin=0, ymax=20)

                    dpg.add_vline_series(x=[n for n in range(10)], parent=default_x)
                    dpg.add_hline_series(x=[n for n in range(120)], parent=default_y)

                dpg.add_button(label="Play TETRIS !", width=325, callback=tetrominos_handler.create_blocksDispatcher,
                               id=item_id["buttons"]["play_button"])
                dpg.set_item_font(item=item_id["buttons"]["play_button"], font=play_font)
                dpg.set_item_theme(item=item_id["buttons"]["play_button"], theme=play_button_theme)

            with dpg.child(autosize_x=True):
                dpg.add_dummy(height=10)

                statistics_text = dpg.add_button(label="STATISTICS", width=-1)
                dpg.set_item_theme(item=statistics_text, theme=dummy_button_theme)

                with dpg.plot(no_menus=False, no_title=True, no_box_select=True, no_mouse_pos=True, width=315,
                              height=560, equal_aspects=True, id=item_id["windows"]["statistics_window"]):

                    dpg.set_item_theme(item=item_id["windows"]["statistics_window"], theme=no_border_board_theme)

                    x = dpg.add_plot_axis(axis=0, no_gridlines=True, no_tick_marks=True, no_tick_labels=True,
                                          lock_min=True)
                    y = dpg.add_plot_axis(axis=1, no_gridlines=True, no_tick_marks=True, no_tick_labels=True,
                                          lock_min=True)

                    dpg.set_axis_limits(axis=x, ymin=0, ymax=10)
                    dpg.set_axis_limits(axis=y, ymin=0, ymax=19)

                    tetrominos_handler.draw_statistics_LBlock()
                    tetrominos_handler.draw_statistics_IBlock()
                    tetrominos_handler.draw_statistics_TBlock()
                    tetrominos_handler.draw_statistics_ZBlock()
                    tetrominos_handler.draw_statistics_SBlock()
                    tetrominos_handler.draw_statistics_OBlock()
                    tetrominos_handler.draw_statistics_JBlock()

                dashed_line_text = dpg.add_button(label="-------------------", width=-1)
                dpg.add_text(default_value=" Total")
                dpg.add_same_line(spacing=170)
                dpg.add_text(default_value=0, id=item_id["displays"]["Total_block_stat"])
                dpg.set_item_theme(item=dashed_line_text, theme=dummy_button_theme)

    dpg.delete_item(item=enter_level_screen)
    dpg.set_primary_window(window=item_id["windows"]["main_window"], value=True)


def press_any_key_to_start():
    # Play audio effect to indicate selection
    tetrominos_handler.audio_effectsDispatcher("selection.wav")

    # Continue with setting up enter level screen
    #dpg.delete_item(item=item_id["registries"]["key_release_handler"])
    dpg.delete_item(item=item_id["registries"]["mouse_release_handler"])
    dpg.delete_item(item=welcome_screen)
    dpg.configure_item(item=enter_level_screen, show=True, modal=True)
    dpg.set_primary_window(window=enter_level_screen, value=True)


with dpg.window(modal=True, autosize=True, no_collapse=True, no_resize=True, no_close=True, no_move=True,
                no_title_bar=True) as welcome_screen:
    width, height, channels, data = dpg.load_image("textures/welcome_screen.jpg")

    welcome_screen_image = dpg.add_static_texture(width, height, data, parent=item_id["registries"]["texture_registry"])
    dpg.add_image(texture_id=welcome_screen_image, width=984, height=688)

    #dpg.add_key_release_handler(callback=press_any_key_to_start, id=item_id["registries"]["key_release_handler"])
    dpg.add_mouse_release_handler(callback=press_any_key_to_start, id=item_id["registries"]["mouse_release_handler"])

with dpg.window(autosize=True, no_collapse=True, no_resize=True, no_close=True, no_move=True,
                no_title_bar=True,show=False) as enter_level_screen:
    dpg.add_dummy(height=300)

    with dpg.group(horizontal=True):
        dpg.add_child(width=250)

        with dpg.group():
            dpg.add_text(default_value="Enter your level (0-9) > ")
            dpg.add_same_line()
            dpg.add_input_int(label="", step=0, min_value=0, max_value=9, width=30, on_enter=True,
                              callback=set_main_window, id=item_id["displays"]["enter_level"])

            # If continue button is required, use this
            # continue_button = dpg.add_button(label="Continue", callback=set_main_window)
            # dpg.set_item_theme(item=continue_button, theme=play_button_theme)


def background_theme():
    play_theme_thread = threading.Thread(name="play theme", target=theme_audio, args=(), daemon=True)
    play_theme_thread.start()


def theme_audio():
    time.sleep(3)
    while True:
        tetrominos_handler.audio_effectsDispatcher("theme.mp3")
        time.sleep(85)

background_theme()

dpg.set_primary_window(window=welcome_screen, value=True)
dpg.start_dearpygui()
