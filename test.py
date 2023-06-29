import cv2

class Test:
    def __init__(self):
        pass
       
    def test(self):
        target_video_filepath = ("../video-bites-data/test_vod_extra_short.mp4")
        video = cv2.VideoCapture(target_video_filepath)
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        frame = video.read()[1]
        shape = frame.shape
        scaled_h = int(shape[0] * 0.275)
        scaled_w = int(shape[1] * 0.275)
        frame = cv2.resize(frame, dsize=(scaled_w, scaled_h), interpolation=cv2.INTER_CUBIC)
        cv2.imshow('test',frame)


        pass