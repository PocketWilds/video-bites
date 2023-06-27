from gui import Gui
from test import Test



import cv2
import os
import numpy as np
from skimage.metrics import structural_similarity
import matplotlib.pyplot as plt
structural_similarity
from PIL import Image
import time

from skimage import measure
from skimage.io import imread


from video_analyzer import VideoAnalyzer


if __name__ == "__main__":
    start_time = time.perf_counter()
    #target_video_filepath = ("../video-bites-data/test_vod_extra_short.mp4")
    #target_video_filepath = ("../video-bites-data/test_vod_short.mp4")
    #target_video_filepath = ("../video-bites-data/test_vod_med.mp4")
    #$target_video_filepath = ("../video-bites-data/test_vod_long.mp4")

    #analyzer = VideoAnalyzer(filepath=target_video_filepath)
    #analyzer.run_analysis()
    
    #test = Test(target_video_filepath)
    #test.test_chat()
    #test.process_video()
    #test.test()
    #test.test2()
    gui = Gui()
    end_time = time.perf_counter()

    #video = cv2.VideoCapture("./test_vod_extra_short.mp4")
    #video = cv2.VideoCapture(target_video_filepath)
    
    #frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
    #fps = video.get(cv2.CAP_PROP_FPS)
    #print("frames: " + str(frames))
    #print("fps: " + str(fps))

    #runtime_s = frames / fps
    #rt_s = str(runtime_s % 60)
    #rt_m = str(int(runtime_s / 60))
    #rt_h = str(int(runtime_s / 3600))

    sr= end_time - start_time
    sr_s = str((sr) % 60)
    sr_m = str(int(sr / 60) % 60)
    sr_h = str(int(sr / 3600))
    #print("Length of video: " + rt_h + " hr "+rt_m+" min "+rt_s+" sec")
    print("Software Runtime: " + sr_h + " hr "+sr_m+" min "+sr_s+" sec")
    #print("Perf speed: " + str(runtime_s / sr))
    #gui.test()
