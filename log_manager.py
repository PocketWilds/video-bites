import os
from datetime import datetime

class LogManager:
    
    log_dir = './logs'
    if (not os.path.exists(log_dir)):
        os.makedirs(log_dir)

    error_log_dir = './logs/errors/'
    if (not os.path.exists(error_log_dir)):
        os.makedirs(error_log_dir)

    def write_log(target_filename):
        current_timestamp = datetime.now()
        log_file_title = f'./logs/{current_timestamp.year:04d}-{current_timestamp.month:02d}-{(current_timestamp.day):02d}_{current_timestamp.hour:02d}-{current_timestamp.minute:02d}-{current_timestamp.second:02d}_output_log.txt'

    def write_error_log(error_message):
        current_timestamp = datetime.now()
        log_file_title = f'./logs/errors/{current_timestamp.year:04d}-{current_timestamp.month:02d}-{(current_timestamp.day):02d}_{current_timestamp.hour:02d}-{current_timestamp.minute:02d}-{current_timestamp.second:02d}_error_log.txt'
        log_file = open(log_file_title, 'w')
        log_file.write(str(error_message))
