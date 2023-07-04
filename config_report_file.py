class SaveFile:
    def __init__(self, tgt_file, frame_windows, target_windows, analysis_results):
        self.tgt_file = tgt_file
        self.frame_windows = frame_windows
        self.target_windows = target_windows
        self.analysis_results = analysis_results

    def dump(self):
        dictified_obj = { "tgt_file": self.tgt_file, 
            "frame_windows":self.frame_windows,
            "target_windows":self.target_windows,
            "analysis_results":self.analysis_results
        }
        return dictified_obj
