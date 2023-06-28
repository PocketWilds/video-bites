import os
import dearpygui.dearpygui as dpg
import cv2
import numpy as np
from tkinter import filedialog
from video_analyzer import VideoAnalyzer


class Gui:

    def __init__(self):
        #target_video_filepath = ("../video-bites-data/test_vod_extra_short.mp4")
        #target_video_filepath = ("../video-bites-data/test_vod_short.mp4")
        #target_video_filepath = ("../video-bites-data/test_vod_med.mp4")
        #$target_video_filepath = ("../video-bites-data/test_vod_long.mp4")

        self._update_frame = False
        self._current_frame = 0
        self._analyzer = VideoAnalyzer()
        self._video = None
        self._slider = None

        hasSaved = True

        self._context = dpg.create_context()
        dpg.create_viewport(title='Video Bites', width=950, height=800, resizable = False)

        width, height, channels, data = dpg.load_image('./vid-preview-bg.png')

        with dpg.texture_registry(show=False):
            dpg.add_raw_texture(width=width, height=height, default_value=data, id='vid-preview-bg')

        with dpg.window(id='ModalNewTab', modal=True, width=425, height=200, no_resize=True,show=True):
            with dpg.group():
                dpg.add_text(default_value="Specify number of seconds for running average time window.")
                with dpg.group(horizontal=True):
                    dpg.add_input_int(id="NewTabHoursInput", width=150, min_value=0)
                    dpg.add_text(default_value=" hours")
                with dpg.group(horizontal=True):
                    dpg.add_input_int(id="NewTabMinutesInput", width=150, min_value=0, max_value=59)
                    dpg.add_text(default_value=" minutes")
                with dpg.group(horizontal=True):
                    dpg.add_input_int(id="NewTabSecondsInput", width=150, min_value=0, max_value=59)
                    dpg.add_text(default_value=" seconds")
                dpg.add_spacer(height=10)
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=75)
                    dpg.add_text(default_value="")
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=225)
                    dpg.add_button(width=70, label="Cancel", callback=Gui._cb_close_new_tab_modal)
                    dpg.add_button(width=70, label="Confirm", callback=Gui._cb_confirm_new_tab_modal)


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
                                
                    with dpg.child_window(id='PreviewSection', width=(622), height=(350), no_scrollbar=False, border=False):
                        with dpg.group(horizontal=True):
                            dpg.add_button(id='SrcBtn', label='Source...', callback=Gui._cb_choose_src_vid, user_data={'analyzer':self._analyzer,"ctr":self})
                            dpg.add_text(id='TgtFilepath', default_value='mp4 file not yet chosen')
                        
                        with dpg.child_window(id='VideoPreview', width=529, height=298, border=False):
                            dpg.add_image('vid-preview-bg')
                        self._slider = dpg.add_slider_int(id='VideoPosSlider', min_value=0, max_value=0, width=580,enabled=True, callback=Gui._cb_frame_slider, user_data={"ctr":self})
                        pass

                dpg.add_spacer(height=10)

                with dpg.child_window(id='AnalysisResults', width=(880), height=(200), no_scrollbar=False):
                    with dpg.tab_bar(id='ResultsTabBar', reorderable=True):
                        dpg.add_tab_button(label='+', trailing=True, callback=Gui._cb_click_new_tab_btn)
                    with dpg.child_window(id='ResultDisplayWindow', width=(860), height=(155), pos=(10, 35), horizontal_scrollbar=True, no_scrollbar=False, border=False):
                        dpg.add_simple_plot(default_value=(0.3,0.9,2.5,8.9),height=125, width = 700)
                        pass

                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=766)
                    dpg.add_button(label='Begin Analysis',callback=Gui._cb_run_analysis)

        dpg.set_primary_window('MainWindow', True)

        dpg.setup_dearpygui()
        dpg.show_viewport()

        while dpg.is_dearpygui_running():
            tmp = dpg.get_value('VideoPosSlider')
            if(self._update_frame == True):
                self._refresh_preview_frame()
            dpg.render_dearpygui_frame()


        dpg.destroy_context()
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
    
    def _cb_frame_slider(sender, app_data, user_data):
        controller = user_data['ctr']
        if(controller._video != None):
            controller._current_frame = app_data
            controller._update_frame = True

    def _cb_add_setting(sender, app_data):
        pass

    def _cb_click_new_tab_btn(sender, app_data):
        dpg.configure_item('ModalNewTab', show=True, pos=(250,100))

    def _cb_close_new_tab_modal(sender, app_data):
        dpg.configure_item('ModalNewTab', show=False, pos=(250,100))
        dpg.set_value('NewTabHoursInput', 0)
        dpg.set_value('NewTabMinutesInput', 0)
        dpg.set_value('NewTabSecondsInput', 0)

    def _cb_confirm_new_tab_modal(sender, app_data):

        if(False):
            pass #mess with the error label
        else:
            pass #process the input data, create the new tab
            Gui._cb_close_new_tab_modal(sender, app_data)

    def _cb_choose_src_vid(sender, app_data, user_data):
        accepted_filetypes = [ ('MP4 video files', '*.mp4') ]
        filepath = filedialog.askopenfilename(initialdir=os.getcwd(), filetypes=accepted_filetypes)
        if (filepath != None and filepath != ''):
            analyzer = user_data['analyzer']
            controller = user_data['ctr']
            if(controller._video != None):
                controller._video.release()
            
            analyzer.tgt_filepath = filepath
            dpg.set_value('TgtFilepath',filepath)
            dpg.delete_item('VideoPosSlider')
            controller._video = cv2.VideoCapture(filepath)
            num_frames = int(controller._video.get(cv2.CAP_PROP_FRAME_COUNT))
            Gui._change_preview_frame(controller._video, 0)
            controller._current_frame = 0
            dpg.add_slider_int(id='VideoPosSlider', parent='PreviewSection', min_value=0, max_value=num_frames - 1, width=580,enabled=True, callback=Gui._cb_frame_slider, user_data={"ctr":controller})

    def _cb_run_analysis(sender, app_data, user_data):
        pass

    def _get_video_preview_frame(video_capture, frame_number):
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        frame = video_capture.read()[1]
        shape = frame.shape
        scaled_h = int(shape[0] * 0.275)
        scaled_w = int(shape[1] * 0.275)
        preview_frame = cv2.resize(frame, dsize=(scaled_w, scaled_h), interpolation=cv2.INTER_CUBIC)
        return preview_frame

    def _refresh_preview_frame(self):
        self._update_frame = False
        Gui._change_preview_frame(self._video, self._current_frame)

    def _change_preview_frame(video, frame_number):
        frame = Gui._get_video_preview_frame(video, frame_number)
        texture_data = Gui._cv2_frame_to_dpg_texture_array(frame)
        
        tmp = dpg.does_item_exist('FramePreviewImage')

        if(dpg.does_item_exist('FramePreviewImage') == False):
            with dpg.texture_registry(show=False):
                width = frame.shape[1]
                height = frame.shape[0]
                dpg.add_raw_texture(width=width, height=height, default_value=texture_data, format=dpg.mvFormat_Float_rgb, id='current-frame-preview')
            dpg.add_image('current-frame-preview', id='FramePreviewImage', parent='VideoPreview', pos=(0,0))
        else:
            dpg.set_value('current-frame-preview', texture_data)


    def _cv2_frame_to_dpg_texture_array(frame):
        unrolled_array = []
        height = frame.shape[0]
        width = frame.shape[1]

        texture = np.flip(frame, 2)
        texture = texture.ravel()
        texture = np.asfarray(texture, dtype='f')
        texture = np.true_divide(texture, 255.0)

        return texture