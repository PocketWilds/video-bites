import cv2
import os
import numpy as np
from skimage.metrics import structural_similarity
from PIL import Image
import matplotlib.pyplot as plt
import threading

import queue

class FraneWorkQueue:
    def __init__(self):
        self.frames = []

class Test:
    def __init__(self, filepath):
        self.filepath = filepath
        self.raw_analysis = None


        self.mse_threshold = 7000.0
        self.ssim_threshold = 0.47

        pass

    def read_frames(video_path, frames_queue, framecount):
        video = cv2.VideoCapture(video_path)
        while video.isOpened():
            ret, frame = video.read()
            if not ret:
                break
            #print(video.get(cv2.CAP_PROP_POS_FRAMES))
            framecount[0] += 1
            #frames_queue.put(frame)
        video.release()

    def test_chat(self):
        video_path = './test_vod_extra_short.mp4'
        frames = queue.Queue()
        results = []

        # Start the frame reading thread
        framecount = [0]
        frame_reader_thread = threading.Thread(target=Test.read_frames, args=(video_path, frames, framecount))
        frame_reader_thread.start()

        # Process frames in the main thread
        while True:
            if(framecount[0] > 3900):
                break

        # Wait for the frame reading thread to finish
        frame_reader_thread.join()
        cv2.destroyAllWindows()

    def process_video(self, num_threads = 1):
        cam = cv2.VideoCapture(self.filepath)
        frames = []
        threads = []

        for i in range(num_threads):
            threads.append(threading.Thread(target=cam.read(),args=()))
        scaleFactor = 1.0
        currentFrame = 0
        while(True):
            ret, frame = cam.read()
            if (ret):
                Test.process_frame(frame)
            else:
                break
        pass

    def process_frame(frame):
        im = Image.fromarray(frame)
        crop = im.crop((1638, 70, 1852, 570))
        section = np.asarray(crop)
        shape = section.shape

        name = "./data/frame" + str(currentFrame) + '.png'
        if currentFrame > 0:
            pass
        else:
            pass

        return (0,0,0)

    def test(self):
        frame_comparisons = []
        cam = cv2.VideoCapture(self.filepath)
        try:
            if not os.path.exists('data'):
                os.makedirs('data')
        except:
            print('Error: could not create data directory')
        scaleFactor = 1.0
        currentFrame = 0
        past_frame = None
        while(True):
            ret, frame = cam.read()
            if ret:
                im = Image.fromarray(frame)
                crop = im.crop((1638, 70, 1852, 570))
                #crop.save("./tmp.png")
                frame = np.asarray(crop)
                shape = frame.shape
                scaledH = int(shape[0] * scaleFactor)
                scaledW = int(shape[1] * scaleFactor)
                frame = cv2.resize(frame, dsize=(scaledW, scaledH), interpolation=cv2.INTER_CUBIC)

                name = "./data/frame" + str(currentFrame) + '.png'
                if currentFrame > 0:
                    mse_result = Test.mse(frame, past_frame)
                    ssim_result = Test.ssim(frame, past_frame)
                    frame_comparisons.append((currentFrame, mse_result, ssim_result))
                
                #cv2.imwrite(name, scaledFrame)

                currentFrame += 1
                past_frame = frame
            else:
                break
        cam.release()
        cv2.destroyAllWindows()

        self.raw_analysis = frame_comparisons

        writeFile ="./simplified-detection.txt"
        file = open(writeFile, 'w')
        frame_comparisons_str = ""
        for tup_elem in frame_comparisons:
            frame_comparisons_str += str(tup_elem[0]) + "\t" + str(tup_elem[1]) + "\t" + str(tup_elem[2]) + "\n"
        file.write(frame_comparisons_str)
        file.close()

    def test2(self):

        interactions_mse = list(filter(lambda x:x[1] > self.mse_threshold, self.raw_analysis))
        interactions_ssim = list(filter(lambda x:x[2] < self.ssim_threshold, self.raw_analysis))
        num_interactions_mse = len(interactions_mse)
        num_interactions_ssim = len(interactions_ssim)

        print("num inter mse: " + str(num_interactions_mse))
        print("num inter ssim: " + str(num_interactions_ssim))
        print("offset: " + str(abs(num_interactions_mse - num_interactions_ssim)))

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

        

    