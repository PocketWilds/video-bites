import os
import dearpygui.dearpygui as dpg
import cv2
import numpy as np
from tkinter import filedialog
from video_analyzer import VideoAnalyzer


class Gui:

    def __init__(self):
        target_video_filepath = ("../video-bites-data/test_vod_extra_short.mp4")
        #target_video_filepath = ("../video-bites-data/test_vod_short.mp4")
        #target_video_filepath = ("../video-bites-data/test_vod_med.mp4")
        #$target_video_filepath = ("../video-bites-data/test_vod_long.mp4")

        self.model = VideoAnalyzer(target_video_filepath)

        hasSaved = True
        

        dpg.create_context()
        dpg.create_viewport(title='Video Bites', width=950, height=800, resizable = False)

        self.texture_registry = dpg.texture_registry(show=False)

        width, height, channels, data = dpg.load_image('./vid-preview-bg.png')
        with self.texture_registry:
            dpg.add_raw_texture(width=width, height=height, default_value=data, id='vid-preview-bg')

        with dpg.window(id='MainWindow', width=950, height=750, no_title_bar=True, no_resize=True, no_move=True, pos=(0,19)):
            with dpg.menu_bar(label='MainMenuBar'):
                with dpg.menu(label='File'):
                    dpg.add_menu_item(label='Open', callback=self.open)
                    dpg.add_menu_item(label='Save', callback=self.save)
                    dpg.add_menu_item(label='Save As...', callback=self.save)
                    dpg.add_menu_item(label='Exit', callback=self.exit)
            with dpg.group():
                with dpg.group(horizontal=True):
                    with dpg.child_window(label='AnalysisSettings', width=(250), height=(350), border=False):
                        with dpg.group(horizontal=True):
                            dpg.add_spacer(width=5)
                            dpg.add_text(id='AnalysisSettingsLabel', default_value='Analysis Settings')
                            dpg.add_button(id='NewSettingBtn', callback=Gui. _cb_add_setting, label='+')
                        with dpg.child_window(label='SettingsContainer', width=(230), height=(320), pos=(5, 30), no_scrollbar=False):
                            pass
                        
                        pass
                                
                    with dpg.child_window(id='PreviewSection', width=(622), height=(350), no_scrollbar=False, border=False):
                        with dpg.group(horizontal=True):
                            dpg.add_button(id='SrcBtn', label='Source...', callback=Gui._cb_choose_src_vid, user_data={'model':self.model})
                            dpg.add_text(id='TgtFilepath', default_value='mp4 file not yet chosen')
                        
                        video_preview_window = dpg.child_window(id='VideoPreview', width=528, height=297, border=False)
                        with video_preview_window:
                            dpg.add_image('vid-preview-bg')
                        dpg.add_slider_int(id='VideoPosSlider', min_value=0, max_value=0, width=580,enabled=True, callback=Gui._cb_frame_slider)
                        pass

                dpg.add_spacer(height=10)

                with dpg.child_window(id='AnalysisResults', width=(880), height=(200), no_scrollbar=False):
                    with dpg.tab_bar(id='ResultsTabBar', callback=Gui._cb_click_tab):
                        dpg.add_tab(label='+')
                    with dpg.child_window(id='ResultDisplayWindow', width=(860), height=(155), pos=(10, 35), horizontal_scrollbar=True, no_scrollbar=False, border=False):
                        dpg.add_simple_plot(default_value=(0.3,0.9,2.5,8.9),height=125, width = 700)
                        pass

                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=766)
                    dpg.add_button(label='Begin Analysis',callback=Gui._cb_run_analysis)

        dpg.set_primary_window('MainWindow', True)

        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()
        pass

    def test(self):
        pass

    def save(self):
        print('save')
        pass

    def open(self):
        print('open')
        pass

    def exit(self):
        print('exit')
        pass
    
    def _cb_frame_slider(sender, app_data):
        processed_data = app_data % 2
        print("number post proc: " + str(processed_data))
        pass

    def _cb_add_setting(sender, app_data):
        pass

    def _cb_click_tab(sender, app_data):
        pass

    def _cb_choose_src_vid(sender, app_data, user_data):
        accepted_filetypes = [ ('MP4 video files', '*.mp4') ]
        filepath = filedialog.askopenfilename(initialdir=os.getcwd(), filetypes=accepted_filetypes)
        if (filepath != None and filepath != ''):
            model = user_data['model']
            model.tgt_filepath = filepath
            dpg.set_value('TgtFilepath',filepath)
            dpg.delete_item('VideoPosSlider')
            dpg.add_slider_int(id='VideoPosSlider',parent='PreviewSection', min_value=0, max_value=51, width=580,enabled=True, callback=Gui._cb_frame_slider)

    def _cb_run_analysis(sender, app_data, user_data):
        pass