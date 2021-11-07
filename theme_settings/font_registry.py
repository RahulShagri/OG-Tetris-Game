# Add all fonts
import dearpygui.dearpygui as dpg

with dpg.font_registry() as main_font_registry:
    regular_font = dpg.add_font('fonts/PressStart2P-vaV7.ttf', 15)
    play_font = dpg.add_font('fonts/PressStart2P-vaV7.ttf', 18)
