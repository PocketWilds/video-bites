import time

from gui import Gui
from log_manager import LogManager

if __name__ == '__main__':
    start_time = time.perf_counter()
    try:
        gui = Gui()
    except Exception as e:
        LogManager.write_error_log(e)
