# Set up themes
import dearpygui.dearpygui as dpg

with dpg.theme() as global_theme:  # Sets up the default theme
    with dpg.theme_component(dpg.mvAll):
        # Styles
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 4, 4, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 8, 8, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 4, 4, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 4, 4, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4, 4, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0, category=dpg.mvThemeCat_Core)

        # Colors
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (0, 0, 0), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (0, 0, 0), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (0, 0, 0), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (0, 0, 0), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (48, 48, 48), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Text, (168, 168, 168), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 0, 0), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (33, 33, 33), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (33, 33, 33), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvPlotCol_PlotBg, (0, 0, 0), category=dpg.mvThemeCat_Plots)
        dpg.add_theme_color(dpg.mvPlotCol_XAxisGrid, (30, 30, 255), category=dpg.mvThemeCat_Plots)
        dpg.add_theme_color(dpg.mvPlotCol_YAxisGrid, (30, 30, 255), category=dpg.mvThemeCat_Plots)
        dpg.add_theme_color(dpg.mvPlotCol_Line, (0, 0, 255), category=dpg.mvThemeCat_Plots)
        dpg.add_theme_color(dpg.mvPlotCol_FrameBg, (0, 0, 0), category=dpg.mvThemeCat_Plots)
        dpg.add_theme_color(dpg.mvPlotCol_PlotBorder, (30, 30, 255), category=dpg.mvThemeCat_Plots)

with dpg.theme() as dummy_button_theme:
    with dpg.theme_component(dpg.mvAll):
        # Styles
        # Colors
        dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 0, 0), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (0, 0, 0), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (0, 0, 0), category=dpg.mvThemeCat_Core)

with dpg.theme() as play_button_theme:
    with dpg.theme_component(dpg.mvAll):
        # Styles
        # Colors
        dpg.add_theme_color(dpg.mvThemeCol_Text, (161, 94, 33), category=dpg.mvThemeCat_Core)

with dpg.theme() as no_border_board_theme:
    with dpg.theme_component(dpg.mvAll):
        # Styles
        # Colors
        dpg.add_theme_color(dpg.mvPlotCol_PlotBorder, (0, 0, 0), category=dpg.mvThemeCat_Plots)
