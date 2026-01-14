import dearpygui.dearpygui as dpg
import tomllib
from view.tags import Tag
from view.themes import create_theme_imgui_default, create_theme_imgui_light, create_theme_imgui_dark

class MainView:

    @staticmethod
    def create_view():
        MainView._init_font()
        MainView._init_theme()
        MainView._load_textures()
        MainView._create_help_window()
        MainView._create_loading_window()

        MainView._create_main_window()

        MainView._create_tooltips()

    @staticmethod
    def _create_main_window():
        with dpg.window(tag=Tag.MAIN_WINDOW):
            with dpg.menu_bar():
                with dpg.menu(label="Theme"):
                    dpg.add_radio_button(tag=Tag.THEME_RADIO_BUTTON ,items=["Default", "Dark", "Light"],
                                         default_value="Default", callback=MainView._change_global_theme)
                dpg.add_menu_item(tag=Tag.HELP_MENU_BUTTON, label="Help")
            with dpg.table(header_row=False, resizable=True, width=-1, height=-1):
                dpg.add_table_column(init_width_or_weight=40)
                dpg.add_table_column(init_width_or_weight=60)
                with dpg.table_row():
                    with dpg.table_cell(): # First column
                        MainView._create_first_column()
                    with dpg.table_cell(): # Second column
                        MainView._create_second_column()

    @staticmethod
    def _create_first_column():
        with dpg.group(horizontal=True):
            dpg.add_image_button(tag=Tag.LOAD_IMAGE_BUTTON, texture_tag=Tag.LOAD_IMAGE_TEXTURE)
            dpg.add_image_button(tag=Tag.DETECT_TEXT_BUTTON, texture_tag=Tag.DETECT_TEXT_TEXTURE)
        dpg.add_separator()
        with dpg.child_window(tag=Tag.IMAGE_WINDOW, width=-1, height=-1):
            pass

    @staticmethod
    def _create_second_column():
        dpg.add_image_button(tag=Tag.COPY_TEXT_BUTTON, texture_tag=Tag.COPY_TEXT_TEXTURE)
        dpg.add_separator()
        with dpg.child_window(width=-1, height=-1):
            dpg.add_input_text(tag=Tag.RESULT_TEXT, multiline=True, width=-1, height=-1)

    @staticmethod
    def _create_help_window():
        with dpg.window(tag=Tag.HELP_WINDOW, label="Help Window", show=False, width=725, height=320):
            dpg.add_text("Welcome to OCR Text Detector!")
            dpg.add_separator()
            with dpg.group(horizontal=True):
                dpg.add_image(texture_tag=Tag.LOAD_IMAGE_TEXTURE)
                dpg.add_text("Select Image - Opens a file dialog to choose an image for text detection.")
            dpg.add_separator()
            with dpg.group(horizontal=True):
                dpg.add_image(texture_tag=Tag.DETECT_TEXT_TEXTURE)
                dpg.add_text("Process Image - Analyzes the selected image and highlights detected text with green outlines.")
            dpg.add_separator()
            with dpg.group(horizontal=True):
                dpg.add_image(texture_tag=Tag.COPY_TEXT_TEXTURE)
                dpg.add_text("Copy Text - Copies all detected text to clipboard.")
            dpg.add_separator()
            dpg.add_text("Supported formats: PNG, JPG, JPEG")

    @staticmethod
    def _create_loading_window():
        with dpg.window(tag=Tag.LOADING_WINDOW, show=False, modal=True, no_close=True, no_title_bar=True, width=300):
            dpg.add_text("Please Wait...")
            dpg.add_separator()
            dpg.add_loading_indicator(indent=110)

    @staticmethod
    def _create_tooltips():
        with dpg.tooltip(parent=Tag.LOAD_IMAGE_BUTTON):
            dpg.add_text("Load new image")
        with dpg.tooltip(parent=Tag.DETECT_TEXT_BUTTON):
            dpg.add_text("Detect text in image")
        with dpg.tooltip(parent=Tag.COPY_TEXT_BUTTON):
            dpg.add_text("Copy text to clipboard")
        with dpg.tooltip(parent=Tag.HELP_MENU_BUTTON):
            dpg.add_text("Click here for more information")

    @staticmethod
    def _load_textures():
        width1, height1, _, data1 = dpg.load_image("resources/icons/load_image.png")
        width2, height2, _, data2 = dpg.load_image("resources/icons/detect_image_64.png")
        width3, height3, _, data3 = dpg.load_image("resources/icons/copy_text.png")
        with dpg.texture_registry():
            dpg.add_static_texture(width=width1, height=height1, default_value=data1, tag=Tag.LOAD_IMAGE_TEXTURE)
            dpg.add_static_texture(width=width2, height=height2, default_value=data2, tag=Tag.DETECT_TEXT_TEXTURE)
            dpg.add_static_texture(width=width3, height=height3, default_value=data3, tag=Tag.COPY_TEXT_TEXTURE)

    @staticmethod
    def _init_font():
        with dpg.font_registry():
            dpg.add_font(file="resources/fonts/FallingSky-JKwK.otf", size=20, tag=Tag.DEFAULT_FONT)

        dpg.bind_font(font=Tag.DEFAULT_FONT)

    @staticmethod
    def _init_theme():
        try:
            with open("config/config.toml", "rb") as file:
                config = tomllib.load(file)
                if config["theme"] == "default":
                    dpg.bind_theme(create_theme_imgui_default())
                elif config["theme"] == "light":
                    dpg.bind_theme(create_theme_imgui_light())
                elif config["theme"] == "dark":
                    dpg.bind_theme(create_theme_imgui_dark())
        except Exception as e:
            print(e)
            dpg.bind_theme(create_theme_imgui_default())

    @staticmethod
    def _change_global_theme(_sender, value):
        if value == "Default":
            with open("config/config.toml", "w") as f:
                f.write(f'theme = "default"\n')
            dpg.bind_theme(create_theme_imgui_default())
        elif value == "Dark":
            with open("config/config.toml", "w") as f:
                f.write(f'theme = "dark"\n')
            dpg.bind_theme(create_theme_imgui_dark())
        elif value == "Light":
            with open("config/config.toml", "w") as f:
                f.write(f'theme = "light"\n')
            dpg.bind_theme(create_theme_imgui_light())
