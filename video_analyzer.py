
import cv2
import threading
import queue
import numpy as np
from skimage.metrics import structural_similarity
from PIL import Image

class FrameQueue:
    def __init__(self):
        self.frames = []
        self.frame_counter
        
    def get_next_pair(self):
        valid_pair = None

        return valid_pair

    def find_next_hole(self):

        return
    
    def enqueue(self, to_enqueue):
        pass

    def dequeue(self, to_dequeue):
        pass


class VideoAnalyzer:
    def __init__(self, filepath):
        self.filepath = filepath
    
    def run_analysis(self, num_threads=1, scale_factor=1.0):
        frames_queue = queue.Queue()
        raw_results = []
        read_threads = []
        proc_threads = []

        video = cv2.VideoCapture(self.filepath)
        thread_one = threading.Thread(target=VideoAnalyzer._read_in_frame, args=(video,frames_queue, scale_factor))
        thread_two = threading.Thread(target=VideoAnalyzer._read_in_frame, args=(video,frames_queue, scale_factor))
        thread_one.start()
        thread_two.start()
        thread_one.join()
        thread_two.join()
        
        """for i in range(num_threads):
            new_thread = threading.Thread(target=VideoAnalyzer._read_in_frame, args=(video,frames_queue, scale_factor))
            read_threads.append(new_thread)
            new_thread.start()"""

        for i in range(num_threads):
            new_thread = threading.Thread(target=VideoAnalyzer._process_frame, args=(frames_queue, read_threads))
            proc_threads.append(new_thread)
            new_thread.start()

        for thread in read_threads:
            thread.join()
        for thread in proc_threads:
            thread.join()

    def _read_in_frame(video, frames_queue, scale_factor):
        while (True):
            read_result, frame = video.read()
            if read_result:
                current_frame = video.get(cv2.CAP_PROP_POS_FRAMES)
                src_img = Image.fromarray(frame)
                crop = src_img.crop((1638, 70, 1852, 570))
                frame = np.asarray(crop)
                shape = frame.shape
                scaled_h = int(shape[0] * scale_factor)
                scaled_w = int(shape[1] * scale_factor)
                frame = cv2.resize(frame, dsize=(scaled_w, scaled_h), interpolation=cv2.INTER_CUBIC)
                    
                #name = "./data/frame" + str(current_frame) + '.png'
                #cv2.imwrite(name, scaledFrame)

                frames_queue.put(frame)
                print("adding frame #" + str(current_frame))
                pass
            else:
                break
        return
        
    def _process_frame(frames_queue, read_threads):
        while (True):
            still_reading = any(t.is_alive() for t in read_threads)
            if(still_reading):
            #if(frames_queue.qsize() > 0 or still_reading):
                """if current_frame > 0:
                    mse_result = Test.mse(frame, past_frame)
                    ssim_result = Test.ssim(frame, past_frame)
                    frame_comparisons.append((current_frame, mse_result, ssim_result))"""
                pass
            else:
                break

        return