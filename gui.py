import os
import dearpygui.dearpygui as dpg
import cv2
import numpy as np
from tkinter import filedialog
from video_analyzer import VideoAnalyzer

import random

#TODO Currently can't edit analysis result windows well.  Consider a system to update stored values when windows are deleted.  Perhaps new button inside window instead of close button?
#TODO Maybe implement an auto sort feature to the frame window settings to sort by chronological order

class Gui:

    def __init__(self):
        self._update_frame = False
        self._current_frame = 0
        self._analyzer = VideoAnalyzer()
        self._target_windows = []
        self._setting_ranges = []
        self._data_bindings = {}
        self._video = None
        self._slider = None

        hasSaved = True

        self._context = dpg.create_context()
        dpg.create_viewport(title='Video Bites', width=900, height=650, resizable = False)

        width, height, channels, data = dpg.load_image('./vid-preview-bg.png')

        with dpg.texture_registry(show=False):
            width, height, channels, data = dpg.load_image('./vid-preview-bg.png')
            dpg.add_raw_texture(width=width, height=height, default_value=data, id='vid-preview-bg')
            width, height, channels, data = dpg.load_image('./results-bg.png')
            dpg.add_raw_texture(width=width, height=height, default_value=data, id='results-bg')
            
        with dpg.window(id='ModalNewSetting', modal=True, width=515, height=200, no_resize=True,show=False):
            with dpg.group():
                dpg.add_text(default_value='Specify number of seconds for running average time window.')
                with dpg.group(horizontal=True):
                    dpg.add_text(default_value='Starting Frame:')
                    dpg.add_input_int(id='NewSettingStartInput', width=100, min_value=0, default_value=1)
                    dpg.add_spacer(width=6)
                    dpg.add_text(id='StartErrorText', default_value='', color=(255,0,0,255))
                with dpg.group(horizontal=True):
                    dpg.add_text(default_value='Ending Frame:')
                    dpg.add_spacer(width=6)
                    dpg.add_input_int(id='NewSettingEndInput', width=100, min_value=0, max_value=59, default_value=1)
                    dpg.add_spacer(width=6)
                    dpg.add_text(id='EndErrorText', default_value='', color=(255,0,0,255))
                dpg.add_spacer(height=10)
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=100)
                    dpg.add_text(id='NewSettingGeneralErrorText', default_value='', color=(255,0,0,255))
                dpg.add_spacer(height=10)
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=325)
                    dpg.add_button(id='NewSettingConfirmBtn', width=70, label='Confirm', callback=Gui._cb_confirm_new_setting_modal, user_data={'ctr':self})
                    dpg.add_button(width=70, label='Cancel', callback=Gui._cb_close_new_setting_modal, user_data={'ctr':self})

        with dpg.window(id='ModalNewTab', modal=True, width=515, height=200, no_resize=True, show=False):
            with dpg.group():
                dpg.add_text(default_value='Specify number of seconds for running average time window.')
                with dpg.group(horizontal=True):
                    dpg.add_input_int(id='NewTabHoursInput', width=100, min_value=0)
                    dpg.add_text(default_value=' hours')
                    dpg.add_spacer(width=6)
                    dpg.add_text(id='HoursErrorText', default_value='', color=(255,0,0,255))
                with dpg.group(horizontal=True):
                    dpg.add_input_int(id='NewTabMinutesInput', width=100, min_value=0, max_value=59)
                    dpg.add_text(default_value=' minutes')
                    dpg.add_text(id='MinutesErrorText', default_value='', color=(255,0,0,255))
                with dpg.group(horizontal=True):
                    dpg.add_input_int(id='NewTabSecondsInput', width=100, min_value=0, max_value=59)
                    dpg.add_text(default_value=' seconds')
                    dpg.add_text(id='SecondsErrorText', default_value='', color=(255,0,0,255))
                dpg.add_spacer(height=10)
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=100)
                    dpg.add_text(id='NewTabGeneralErrorText', default_value='', color=(255,0,0,255))
                dpg.add_spacer(height=10)
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=325)
                    dpg.add_button(width=70, label='Confirm', callback=Gui._cb_confirm_new_tab_modal, user_data={'ctr':self})
                    dpg.add_button(width=70, label='Cancel', callback=Gui._cb_close_new_tab_modal)

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
                            dpg.add_button(id='NewSettingBtn', callback=Gui._cb_add_setting, user_data={'ctr':self},label='+')
                        with dpg.child_window(id='SettingsContainer', width=(230), height=(320), pos=(5, 30), no_scrollbar=False):
                            pass
                                
                    with dpg.child_window(id='PreviewSection', width=(622), height=(350), no_scrollbar=False, border=False):
                        with dpg.group(horizontal=True):
                            dpg.add_button(id='SrcBtn', label='Source...', callback=Gui._cb_choose_src_vid, user_data={'analyzer':self._analyzer,'ctr':self})
                            dpg.add_text(id='TgtFilepath', default_value='mp4 file not yet chosen')
                        
                        with dpg.child_window(id='VideoPreview', width=529, height=298, border=False):
                            dpg.add_image('vid-preview-bg')
                        self._slider = dpg.add_slider_int(id='VideoPosSlider', min_value=0, max_value=0, width=580,enabled=True, callback=Gui._cb_frame_slider, user_data={'ctr':self})
                        pass

                dpg.add_spacer(height=10)

                with dpg.child_window(id='AnalysisResults', width=(880), height=(200), no_scrollbar=False):
                    
                    with dpg.tab_bar(id='ResultsTabBar', reorderable=True):
                        #dpg.add_tab(id='BaseTab', show=False)
                        dpg.add_tab_button(label='+', trailing=True, callback=Gui._cb_click_new_tab_btn)
                    #dpg.add_image('results-bg',pos=(7,30), )
                    with dpg.group(horizontal=True):
                        dpg.add_button(id='ResultsDelBtn', label='Edit', callback=Gui._cb_test)
                        dpg.add_button(id='ResultsEditBtn', label='Delete', callback=Gui._cb_del_window, user_data={'ctr':self})
                dpg.add_spacer(height=3)
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=716, show=True)
                    with dpg.group():
                        dpg.add_button(id='RunAnalysisBtn', label='Begin Analysis',callback=Gui._cb_run_analysis, user_data={'ctr':self}, enabled=False)
                    dpg.add_loading_indicator(id='LoadingIcon', style=1, radius=1.8, show=False)

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
    
    def _cb_test(sender, app_data, user_data):
        pass

    def _cb_del_window(sender, app_data, user_data):
        title = dpg.get_value('ResultsTabBar')
        print(title)
        children = dpg.get_item_children(title)[1]
        for child in children:
            dpg.delete_item(child)
        dpg.delete_item(title)
        bound_data = user_data['ctr']._data_bindings[title]
        print(f'bound data:{bound_data}')
        user_data['ctr']._target_windows.remove(bound_data)
        test = {}
        user_data['ctr']._data_bindings.pop(title)
        #value = dpg.get_value(108)
        #dpg.delete_item
        print(children)
        dpg.configure_item('RunAnalysisBtn', enabled=Gui._check_analysis_prereqs(user_data['ctr']))


    def _cb_frame_slider(sender, app_data, user_data):
        controller = user_data['ctr']
        if(controller._video != None):
            controller._current_frame = app_data
            controller._update_frame = True

    def _cb_add_setting(sender, app_data, user_data):
        edit_tgt = user_data.get('edit-tgt')
        if(edit_tgt != None):
            string = dpg.get_value(edit_tgt)
            index = string.find('-')
            start = int(string[:index])
            end = int(string[index+1:])
            dpg.set_value('NewSettingStartInput', start)
            dpg.set_value('NewSettingEndInput', end)
        dpg.configure_item('ModalNewSetting', show=True, pos=(250, 100), user_data=user_data)
        dpg.configure_item('NewSettingConfirmBtn', user_data=user_data)

    def _cb_confirm_new_setting_modal(sender, app_data, user_data):
        is_data_valid = True
        setting_ranges = user_data.get('ctr')._setting_ranges
        edit_tgt = user_data.get('edit-tgt')
        prev_range = user_data.get('range')
        start_frame = dpg.get_value('NewSettingStartInput')
        end_frame = dpg.get_value('NewSettingEndInput')

        if (start_frame < 1):
            dpg.set_value('StartErrorText','Please enter a number greater than 0.')
            is_data_valid = False
        else:
            dpg.set_value('StartErrorText','')

        if (end_frame < 1):
            dpg.set_value('EndErrorText','Please enter a number greater than 0.')
            is_data_valid = False
        else:
            dpg.set_value('EndErrorText','')

        frame_overlap = False
        relevant_range = None

        for setting_range in setting_ranges:
            if (setting_range != prev_range
            and Gui._do_ranges_overlap((start_frame, end_frame), setting_range)):
                frame_overlap = True
                relevant_range = setting_range
                break

        if (is_data_valid and end_frame <= start_frame):
            dpg.set_value('NewSettingGeneralErrorText','End value must be greater than Start value.')
            is_data_valid = False
        elif(frame_overlap):
            dpg.set_value('NewSettingGeneralErrorText',f'Range overlaps with existing range ({relevant_range[0]}-{relevant_range[1]}).')
            is_data_valid = False
        else:
            dpg.set_value('NewSettingGeneralErrorText','')

        if(is_data_valid):
            current_range = (start_frame,end_frame)
            text = f"{start_frame}-{end_frame}"
            if(edit_tgt == None):
                with dpg.group(parent='SettingsContainer', horizontal=True):
                    user_data['ctr']._setting_ranges.append((start_frame, end_frame))
                    label = dpg.add_text(default_value=text)
                    edit_btn = dpg.add_button()
                    del_btn = dpg.add_button()
                    dpg.configure_item(edit_btn, label='Edit', callback=Gui._cb_add_setting,
                        user_data={
                            'ctr':user_data['ctr'],
                            'edit-tgt':label,
                            'range':current_range,
                            'label':label,
                            'edit-btn':edit_btn,
                            'del-btn':del_btn
                        }
                    )
                    dpg.configure_item(del_btn,label='Delete', callback=Gui._cb_delete_setting_button,
                        user_data={
                            'ctr':user_data['ctr'],
                            'self':dpg.get_item_parent(label),
                            'range':current_range
                        }
                    )
            else:
                setting_ranges.remove(prev_range)
                setting_ranges.append(current_range)
                label = user_data['label']
                dpg.set_value(label, text)
                edit_btn = user_data['edit-btn']
                del_btn = user_data['del-btn']
                dpg.configure_item(edit_btn, label='Edit', callback=Gui._cb_add_setting,
                    user_data={
                        'ctr':user_data['ctr'],
                        'edit-tgt':label,
                        'range':current_range,
                        'label':label,
                        'edit-btn':edit_btn,
                        'del-btn':del_btn
                    }
                )
                dpg.configure_item(del_btn,label='Delete', callback=Gui._cb_delete_setting_button,
                    user_data={
                        'ctr':user_data['ctr'],
                        'self':dpg.get_item_parent(label),
                        'range':current_range
                    }
                )
                
            is_ready = Gui._check_analysis_prereqs(user_data['ctr'])
            dpg.configure_item('RunAnalysisBtn', enabled=is_ready)
            Gui._cb_close_new_setting_modal(sender, app_data, user_data)
        
    def _cb_close_new_setting_modal(sender, app_data, user_data):
        dpg.configure_item('ModalNewSetting', show=False, pos=(250, 100), user_data=user_data)
        dpg.configure_item('NewSettingConfirmBtn', user_data=user_data)
        dpg.set_value('NewSettingStartInput', 1)
        dpg.set_value('NewSettingEndInput', 1)
        dpg.set_value('StartErrorText','')
        dpg.set_value('EndErrorText','')
        dpg.set_value('NewSettingGeneralErrorText','')

    def _cb_delete_setting_button(sender, app_data, user_data):
        group = user_data['self']
        children = dpg.get_item_children(group)[1]
        current_range = user_data['range']
        user_data['ctr']._setting_ranges.remove(current_range)
        for child in children:
            dpg.delete_item(child)
        dpg.delete_item(group)
        dpg.configure_item('RunAnalysisBtn', enabled=Gui._check_analysis_prereqs(user_data['ctr']))

    def _cb_click_new_tab_btn(sender, app_data):
        dpg.configure_item('ModalNewTab', show=True, pos=(250, 100))

    def _cb_close_new_tab_modal(sender, app_data):
        dpg.configure_item('ModalNewTab', show=False, pos=(250, 100))
        dpg.set_value('NewTabHoursInput', 0)
        dpg.set_value('NewTabMinutesInput', 0)
        dpg.set_value('NewTabSecondsInput', 0)
        dpg.set_value('HoursErrorText', '')
        dpg.set_value('MinutesErrorText', '')
        dpg.set_value('SecondsErrorText', '')
        dpg.set_value('NewTabGeneralErrorText', '')

    def _cb_confirm_new_tab_modal(sender, app_data, user_data):
        analyzer = user_data['ctr']._analyzer
        num_hours = dpg.get_value('NewTabHoursInput')
        num_minutes = dpg.get_value('NewTabMinutesInput')
        num_seconds = dpg.get_value('NewTabSecondsInput')
        title_str = f"{num_hours:02}h{num_minutes:02}m{num_seconds:02}s"
        total_seconds = num_seconds + num_minutes * 60 + num_hours * 3600

        input_is_valid = True

        if(num_hours < 0):
            dpg.set_value('HoursErrorText','Please enter a positive number.')
            input_is_valid = False
        else:
            dpg.set_value('HoursErrorText','')
        if(num_minutes < 0 or num_minutes >= 60):
            dpg.set_value('MinutesErrorText','Please enter a number between 0 and 59.')
            input_is_valid = False
        else:
            dpg.set_value('MinutesErrorText','')
        if(num_seconds < 0 or num_seconds >= 60):
            dpg.set_value('SecondsErrorText','Please enter a number between 0 and 59.')
            input_is_valid = False
        else:
            dpg.set_value('SecondsErrorText','')

        if(num_hours == 0 and num_minutes == 0 and num_seconds == 0):
            dpg.set_value('NewTabGeneralErrorText','Please enter a time amount above 0 seconds.')
            input_is_valid = False
        else:
            dpg.set_value('NewTabGeneralErrorText','')

        if(total_seconds in user_data['ctr']._target_windows):
            dpg.set_value('NewTabGeneralErrorText','Tab already exists for this amount.')
            input_is_valid = False
        elif(input_is_valid == True):
            dpg.set_value('NewTabGeneralErrorText','')

        if(input_is_valid):
            user_data['ctr']._target_windows.append(total_seconds)
            new_tab_alias = 'tab-' + title_str
            new_tab = dpg.add_tab(parent='ResultsTabBar', label=title_str, closable=True)
            
            plot = dpg.add_simple_plot(parent=new_tab, width=700, height=130)
            user_data['ctr']._data_bindings[new_tab_alias+"-plot"] = plot
            user_data['ctr']._data_bindings[new_tab] = total_seconds
            dpg.configure_item('RunAnalysisBtn', enabled=Gui._check_analysis_prereqs(user_data['ctr']))
            Gui._cb_close_new_tab_modal(sender, app_data)

    def _cb_exit_tab(sender, app_data, user_data):
        pass

    def _cb_choose_src_vid(sender, app_data, user_data):
        accepted_filetypes = [ ('MP4 video files', '*.mp4') ]
        filepath = filedialog.askopenfilename(initialdir=os.getcwd(), filetypes=accepted_filetypes)
        
        if (filepath != None and filepath != ()):
            analyzer = user_data['analyzer']
            controller = user_data['ctr']
            if(controller._video != None):
                controller._video.release()
            
            analyzer.set_filepath(filepath)
            dpg.set_value('TgtFilepath', filepath)
            dpg.delete_item('VideoPosSlider')
            controller._video = cv2.VideoCapture(filepath)
            num_frames = int(controller._video.get(cv2.CAP_PROP_FRAME_COUNT))
            Gui._change_preview_frame(controller._video, 0)
            controller._current_frame = 0
            dpg.add_slider_int(
                id='VideoPosSlider',
                parent='PreviewSection',
                min_value=1,
                max_value=num_frames,
                default_value=1,
                width=580,
                enabled=True,
                callback=Gui._cb_frame_slider,
                user_data={'ctr':controller}
            )
        dpg.configure_item('RunAnalysisBtn', enabled=Gui._check_analysis_prereqs(user_data['ctr']))

    def _cb_run_analysis(sender, app_data, user_data):
        dpg.configure_item('LoadingIcon',show=True)
        frame_ranges = user_data['ctr']._setting_ranges
        running_average_windows = user_data['ctr']._target_windows
        results = user_data['ctr']._analyzer.run_analysis(frame_ranges, running_average_windows)
        for i, window in enumerate(running_average_windows):
            tab_plot = Gui._secs_to_tab_binding_title(window)
            dpg.set_value(user_data['ctr']._data_bindings[tab_plot], results[i])
        dpg.configure_item('LoadingIcon',show=False)  

    def _get_video_preview_frame(video_capture, frame_number):
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number - 1)
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

    def _do_ranges_overlap(left, right):
        if(right[0] < left[0] < right[1]
            or right[0] < left[1] < right[1]
            or left[0] < right[1] < left[1]):
            return True
        return False

    def _secs_to_tab_binding_title(num_total_seconds):
        num_seconds = int(num_total_seconds % 60)
        num_minutes = int(num_total_seconds / 60 % 60)
        num_hours = int(num_total_seconds / 3600)
        return f'tab-{num_hours:02}h{num_minutes:02}m{num_seconds:02}s-plot'

    def _check_analysis_prereqs(self):
        return len(self._setting_ranges) > 0 and len(self._target_windows) > 0 and self._analyzer.is_initialized()