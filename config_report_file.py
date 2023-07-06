class SaveFile:
    def __init__(self, src_file, frame_windows, target_windows, analysis_results):
        self.src_file = src_file
        self.frame_windows = frame_windows
        self.target_windows = target_windows
        self.analysis_results = analysis_results

    def dump(self):
        dictified_obj = { "src_file": self.src_file, 
            "frame_windows":self.frame_windows,
            "target_windows":self.target_windows,
            "analysis_results":self.analysis_results
        }
        return dictified_obj
