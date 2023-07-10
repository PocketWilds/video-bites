from gui import Gui
from log_manager import LogManager

if __name__ == '__main__':
    try:
        gui = Gui()
    except Exception as e:
        LogManager.write_error_log(e)
    except SystemError as e:
        LogManager.write_error_log(e)