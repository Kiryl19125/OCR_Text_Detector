import dearpygui.dearpygui as dpg
from controller.controller import Controller
from model.model import Model
from view.main_view import MainView
from view.tags import Tag

model: Model = Model()
view: MainView = MainView()
controller: Controller = Controller(model, view)

def main():
    dpg.create_context()

    controller.init_view()
    controller.init_controller()

    dpg.create_viewport(title="OCR Text Detector", resizable=True)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.maximize_viewport()
    dpg.set_primary_window(Tag.MAIN_WINDOW, True)

    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()

    dpg.destroy_context()


if __name__ == '__main__':
    main()