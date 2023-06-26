
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
    
    def run_analysis(self, scale_factor=1.0):
        frames_queue = queue.Queue()
        frame_comparisons = []

        video = cv2.VideoCapture(self.filepath)
        next_available_trigger = 0
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

        video.release()
        cv2.destroyAllWindows()

        writeFile ="./simplified-detection.txt"
        file = open(writeFile, 'w')
        frame_comparisons_str = ""
        for tup_elem in frame_comparisons:
            frame_comparisons_str += str(tup_elem[0]) + "\t" + str(tup_elem[1]) + "\t" + str(tup_elem[2]) + "\t" + str(tup_elem[3]) + "\n"
        file.write(frame_comparisons_str)
        file.close()

       
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