import dearpygui.dearpygui as dpg
from view.main_view import MainView
from model.model import Model
from view.tags import Tag

class Controller:

    def __init__(self, model: Model, view: MainView):
        self._model = model
        self._view = view

    def init_view(self):
        self._view.create_view()

    def init_controller(self):
        dpg.set_item_callback(item=Tag.HELP_MENU_BUTTON, callback=Controller.help_callback)

    @staticmethod
    def help_callback():
        Controller._center_window(Tag.HELP_WINDOW)
        dpg.show_item(Tag.HELP_WINDOW)

    @staticmethod
    def _center_window(tag):
        viewport_width = dpg.get_viewport_client_width()
        viewport_height = dpg.get_viewport_client_height()

        window_width = dpg.get_item_width(tag)
        window_height = dpg.get_item_height(tag)

        pos_x = (viewport_width // 2) - (window_width // 2)
        pos_y = (viewport_height // 2) - (window_height // 2)

        dpg.set_item_pos(tag, [pos_x, pos_y])