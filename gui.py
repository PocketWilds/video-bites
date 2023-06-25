import dearpygui.dearpygui as dpg


class Gui:
    def __init__(self):
        hasSaved = True
        pass

    def test(self):
        dpg.create_context()
        dpg.create_viewport(title='Video Bites', width=950, height=800, resizable = False)

        with dpg.viewport_menu_bar(label="MainMenuBar"):
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="Open", callback=self.open)
                dpg.add_menu_item(label="Save", callback=self.save)
                dpg.add_menu_item(label="Save As...", callback=self.save)
                dpg.add_menu_item(label="Exit", callback=self.exit)

        with dpg.window(label="Example Window"):            
            dpg.add_text("Hello, World")
            dpg.add_button(label="Save")
            dpg.add_input_text(label="string", default_value="Quick brown fox")
            dpg.add_slider_float(label="float", default_value=0.273, max_value=1)
        
        with dpg.window(label="MainWindow",width=950,height=750,no_resize=True, no_title_bar=True, no_move = True, pos=(0,19)):
            with dpg.child_window(label="SectionSettings",width=(250),height=(350),pos=(10, 30), no_scrollbar = False):
                
                pass
            
            with dpg.child_window(label="VideoPreview",width=(600),height=(350), pos=(270, 30), no_scrollbar=False):
                pass

            with dpg.child_window(label="AnalysisResults",width=(800),height=(200), pos=(10, 410), no_scrollbar=False):
                pass
            

        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

    def save(self):
        print("save")
        pass

    def open(self):
        print("open")
        pass

    def exit(self):
        print("exit")
        pass