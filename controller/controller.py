import dearpygui.dearpygui as dpg
import xdialog
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
        dpg.set_item_callback(item=Tag.LOAD_IMAGE_BUTTON, callback=Controller.load_image_callback)

    @staticmethod
    def help_callback():
        Controller._center_window(Tag.HELP_WINDOW)
        dpg.show_item(Tag.HELP_WINDOW)

    @staticmethod
    def load_image_callback():
        path = xdialog.open_file(title="Select Image",  filetypes=[("Images", "*.png *.jpg *.jpeg")], multiple=False)

        if path:
            dpg.delete_item(item=Tag.CURRENT_IMAGE_TEXTURE, children_only=False)
            dpg.delete_item(item=Tag.CURRENT_IMAGE, children_only=False)

        width, height, _, data = dpg.load_image(path)
        with dpg.texture_registry():
            dpg.add_static_texture(width=width, height=height, default_value=data, tag=Tag.CURRENT_IMAGE_TEXTURE)

        dpg.add_image(tag=Tag.CURRENT_IMAGE, texture_tag=Tag.CURRENT_IMAGE_TEXTURE, parent=Tag.IMAGE_WINDOW,
                      width=600, height=Controller._calculate_height(
                new_width=600, current_width=width, current_height=height
            ))

    @staticmethod
    def _center_window(tag):
        viewport_width = dpg.get_viewport_client_width()
        viewport_height = dpg.get_viewport_client_height()

        window_width = dpg.get_item_width(tag)
        window_height = dpg.get_item_height(tag)

        pos_x = (viewport_width // 2) - (window_width // 2)
        pos_y = (viewport_height // 2) - (window_height // 2)

        dpg.set_item_pos(tag, [pos_x, pos_y])


    @staticmethod
    def _calculate_height(new_width: int, current_width, current_height: int) -> int:
        # Calculate the scale factor
        aspect_ratio = current_height / current_width
        new_height = int(new_width * aspect_ratio)
        return new_height