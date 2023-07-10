import cv2
import numpy as np
from PIL import Image

from log_manager import LogManager

#TODO: introduce possible error handling to manage uninitiated filepath
class VideoAnalyzer:
    def __init__(self, filepath=None):
        self.filepath = filepath
        if(filepath == None):
            self._video = None
        else:
            self.set_filepath(self.filepath)

    def __del__(self):
        if(self._video != None):
            self._video.release()
            cv2.destroyAllWindows()
    
    def set_filepath(self, filepath):
        self.filepath = filepath
        self._video = cv2.VideoCapture(self.filepath)

    def run_analysis(self, frame_ranges):
        if(self._video != None and self.filepath != None):
            self._video = cv2.VideoCapture(self.filepath)
        
        raw_results, frame_count, fps = self._get_raw_video_analysis(frame_ranges)
        return raw_results, frame_count, fps

    def _get_raw_video_analysis(self, frame_ranges, scale_factor=1.0, monitored_section=(1638, 70, 1852, 570)):
        frame_comparisons = []
        next_available_trigger = 0
        for frame_range in frame_ranges:
            self._video.set(cv2.CAP_PROP_POS_FRAMES, frame_range[0])
            past_frame = None
            range_floor = frame_range[0]
            for i in range(frame_range[0] - 1, frame_range[1]):
                read_result, frame = self._video.read()
                if read_result:
                    src_img = Image.fromarray(frame)
                    crop = src_img.crop(monitored_section)
                    frame = np.asarray(crop)
                    shape = frame.shape
                    scaled_h = int(shape[0] * scale_factor)
                    scaled_w = int(shape[1] * scale_factor)
                    frame = cv2.resize(frame, dsize=(scaled_w, scaled_h), interpolation=cv2.INTER_CUBIC)
                    
                    if i > range_floor:
                        isnt_locked = i > next_available_trigger
                        mse_result = VideoAnalyzer.mse(frame, past_frame)
                        has_new_msg = mse_result > 11000.0 and isnt_locked
                        if(has_new_msg):
                            next_available_trigger = i + 19
                        frame_comparisons.append((i, mse_result, has_new_msg))
                    #cv2.imwrite(name, scaledFrame)
                    past_frame = frame
                else:
                    break
        
        log_output = ""
        for tup_elem in frame_comparisons:
            log_output += f'{tup_elem[0]}\t{tup_elem[1]}\t{tup_elem[2]}\n'
        LogManager.write_log(log_output)

        return frame_comparisons, self._video.get(cv2.CAP_PROP_FRAME_COUNT), self._video.get(cv2.CAP_PROP_FPS)
    
    def mse(imageA, imageB):
        err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
        err /= float(imageA.shape[0] * imageA.shape[1])
        return err

    def is_initialized(self):
        return self._video != None and self.filepath != None
