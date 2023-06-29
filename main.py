from gui import Gui
from test import Test

import cv2
import os
import numpy as np
from skimage.metrics import structural_similarity
from PIL import Image
import time

from skimage import measure
from skimage.io import imread


from video_analyzer import VideoAnalyzer


if __name__ == "__main__":
    start_time = time.perf_counter()

    gui = Gui()
    end_time = time.perf_counter()
    sr= end_time - start_time
    sr_s = str((sr) % 60)
    sr_m = str(int(sr / 60) % 60)
    sr_h = str(int(sr / 3600))
    #print("Length of video: " + rt_h + " hr "+rt_m+" min "+rt_s+" sec")
    print("Software Runtime: " + sr_h + " hr " + sr_m + " min " + sr_s + " sec")
    #print("Perf speed: " + str(runtime_s / sr))
