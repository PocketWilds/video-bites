import bisect
import cv2
import threading
import queue
import numpy as np
from skimage.metrics import structural_similarity
from PIL import Image

class FrameSettings:
    class Setting:
        def __init__(self, range, origin, height, width):
            self.start = range[0]
            self.end = range[1]
            self.origin = origin
            self.height = height
            self.width = width

        @property
        def tgt_crop(self):
            return (self.origin[0], self.origin[1], self.origin[0] + self.width, self.origin[1] + height)

    def __init__(self, limit):
        self.limit = limit
        self._keys = []
        self._ranges = []
        self._settings = {}

    def add_setting(self, new_setting):
        index = bisect.bisect_right(self._keys, new_setting.start)
        self._keys.insert(index, new_setting.start)
        self._ranges.insert(index, (new_setting.start, new_setting.end))        

    def get_setting(self, frame_num):
        index = bisect.bisect_right(self._keys, frame_num) - 1
        if (index >= 0 and frame_num <= self._ranges[index][1]):
            return self._ranges[index]
        return None

class TriggerScores:
    def __init__(self, frame_window, last_frame_num):
        self.frame_window = frame_window
        self.limit = last_frame_num
        self.scores = {}
    
    def _clamp(value, min, max):
        return max(min(value, max), min)

    def add(self, frame_num):
        
        left_limit = int(max(frame_num - int(self.frame_window / 2), 0))

        right_limit = int(min(frame_num + int(self.frame_window / 2), self.limit))
        for i in range(left_limit,right_limit):
            attempt = self.scores.get(i)
            if (attempt == None):
                self.scores[i] = 1
            else:
                self.scores[i] = attempt + 1

    def get(self, frame_num):
        if (frame_num > self.limit or frame_num < 0):
            raise IndexError(f"\"{frame_num}\" is outside the range of this map")
        attempt = self.scores.get(int(frame_num))
        return attempt if attempt != None else 0

#TODO: consider cutting out the inclusion of non-trigger frames with the implication of 0
#TODO: introduce possible error handling to manage uninitiated filepath
class VideoAnalyzer:
    def __init__(self, filepath=None):
        self.filepath = filepath
        self._video = None

    def __del__(self):
        if(self._video != None):
            self._video.release()
            cv2.destroyAllWindows()
    
    def set_filepath(self, filepath):
        self.filepath = filepath
        self._video = cv2.VideoCapture(self.filepath)

    def run_analysis(self):
        if(self._video == None and self.filepath != None):
            self._video = cv2.VideoCapture(self.filepath)
        raw_results, frame_count, fps = self._get_raw_video_analysis()
        meta_results = self._get_meta_analysis(raw_results, frame_count, fps)

    def _get_raw_video_analysis(self, scale_factor=1.0):
        frames_queue = queue.Queue()
        frame_comparisons = []
        
        next_available_trigger = 0
        while (True):
            read_result, frame = self._video.read()
            if read_result:
                current_frame = self._video.get(cv2.CAP_PROP_POS_FRAMES)
                src_img = Image.fromarray(frame)
                crop = src_img.crop((1638, 70, 1852, 570))
                frame = np.asarray(crop)
                shape = frame.shape
                scaled_h = int(shape[0] * scale_factor)
                scaled_w = int(shape[1] * scale_factor)
                frame = cv2.resize(frame, dsize=(scaled_w, scaled_h), interpolation=cv2.INTER_CUBIC)
                
                if current_frame > 1.0:
                    isnt_locked = current_frame > next_available_trigger
                    mse_result = VideoAnalyzer.mse(frame, past_frame)
                    ssim_result = VideoAnalyzer.ssim(frame, past_frame)
                    has_new_msg = mse_result > 11000.0 and ssim_result < 0.55 and isnt_locked
                    if(has_new_msg):
                        next_available_trigger = current_frame + 19.0
                    frame_comparisons.append((current_frame, mse_result, ssim_result, has_new_msg))
                #name = "..video-bites-data/data/" + str(current_frame) + '.png'
                #cv2.imwrite(name, scaledFrame)
                past_frame = frame

                print("adding frame #" + str(current_frame))
                pass
            else:
                break

        writeFile ="./simplified-detection.txt"
        file = open(writeFile, 'w')
        frame_comparisons_str = ""
        for tup_elem in frame_comparisons:
            file.write(str(tup_elem[0]) + "\t" + str(tup_elem[1]) + "\t" + str(tup_elem[2]) + "\t" + str(tup_elem[3]) + "\n")
        file.close()

        return frame_comparisons, self._video.get(cv2.CAP_PROP_FRAME_COUNT), self._video.get(cv2.CAP_PROP_FPS)

    def _get_meta_analysis(self, raw_results, frame_count, fps):
        trigger_points = list(filter(lambda x:x[3] == True, raw_results))
        total_triggers = len(trigger_points)
        vid_len_sec = frame_count / fps
        trigger_per_sec = total_triggers / vid_len_sec

        print(total_triggers)
        pass       

    def mse(imageA, imageB):
        err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
        err /= float(imageA.shape[0] * imageA.shape[1])
        return err

    def ssim(imageA, imageB):
        ra, ga, ba = cv2.split(imageA)
        rb, gb, bb = cv2.split(imageB)

        ssim_score_r = structural_similarity(ra, rb)
        ssim_score_g = structural_similarity(ga, gb)
        ssim_score_b = structural_similarity(ba, bb)

        return (ssim_score_r + ssim_score_g + ssim_score_b) / 3