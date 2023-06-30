import bisect
import cv2
import threading
import queue
import numpy as np
from skimage.metrics import structural_similarity
from PIL import Image

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

    def run_analysis(self, frame_ranges, average_windows):
        if(self._video != None and self.filepath != None):
            self._video = cv2.VideoCapture(self.filepath)
        
        raw_results, frame_count, fps = self._get_raw_video_analysis(frame_ranges)
        meta_results = self._get_meta_analysis(average_windows, raw_results, int(frame_count), fps)
        return meta_results

    def _get_raw_video_analysis(self, frame_ranges, scale_factor=1.0, monitored_section=(1638, 70, 1852, 570)):
        frame_comparisons = []
        next_available_trigger = 0
        for frame_range in frame_ranges:
            self._video.set(cv2.CAP_PROP_POS_FRAMES, frame_range[0])
            past_frame = None
            range_floor = frame_range[0] + 1
            for i in range(frame_range[0], frame_range[1]):
                read_result, frame = self._video.read()
                if read_result:
                    current_frame = self._video.get(cv2.CAP_PROP_POS_FRAMES)
                    src_img = Image.fromarray(frame)
                    crop = src_img.crop(monitored_section)
                    frame = np.asarray(crop)
                    shape = frame.shape
                    scaled_h = int(shape[0] * scale_factor)
                    scaled_w = int(shape[1] * scale_factor)
                    frame = cv2.resize(frame, dsize=(scaled_w, scaled_h), interpolation=cv2.INTER_CUBIC)
                    
                    if current_frame > range_floor:
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

                    #print("adding frame #" + str(current_frame))
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
    
    def _get_meta_analysis(self, average_windows, raw_results, frame_count, fps):
        meta_results = []
        for window in average_windows:
            meta_results.append({})

        triggers = list(filter(lambda x:x[3] == True, raw_results))
        total_triggers = len(triggers)

        for trigger in triggers:
            for i, window in enumerate(average_windows):
                range_diff = int(fps * window / 2)
                min_frame_range = max(int(trigger[0]) - range_diff, 1)
                max_frame_range = min(int(trigger[0]) + range_diff, frame_count)
                for j in range(min_frame_range, max_frame_range):
                    if (meta_results[i].get(j) == None):
                        meta_results[i][j] = 1.0
                    else:
                        meta_results[i][j] += 1.0

        vid_len_sec = frame_count / fps
        trigger_per_sec = total_triggers / vid_len_sec
        prepared_results = []
        for results in meta_results:
            new_result_set = []
            for i in range(1, frame_count):
                if (results.get(i) != None):
                    new_result_set.append(results[i])
                else:
                    new_result_set.append(0.0)    
            prepared_results.append(new_result_set)
        
        return prepared_results

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

    def is_initialized(self):
        return self._video != None and self.filepath != None
