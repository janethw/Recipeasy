import logging, sys, os
from logging.handlers import RotatingFileHandler

logger_message = '{module_name}.{function_name}: {message}'

# example:  _logger.debug(logger_message.format(module_name=__name__, function_name='_process_edamam_data', message='entry'))
# string interpolation replace module with __name__, etc.
# logging a debug message in what is interpolated goes to file and console


# sets what logging level you want in this case only logs info, warning, error and critical
logging_level = logging.INFO


def init_logger(logger_name='app', file_logging=True, terminal_logging=True):
    # configure the log format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')  # format of logging line in console and file

    # example :2024-05-27 11:58:55,187 - DEBUG - recipe_files_directory.edamam_class.process_edamam_recipe_data: Recipe class created, adding ingredients

    # set the logging level
    logging.basicConfig(level=logging_level)
    logger = logging.getLogger(logger_name)  # logging handler

    # file logging
    if file_logging and RotatingFileHandler not in [type(handler) for handler in logger.handlers]:
        # fetches the directory of the current file, negates the need for logs directory at each level
        root_dir = os.path.dirname(os.path.abspath(__file__))
        # create a rotating file handler with a max size of 10MB and a backup count of 5
        handler = RotatingFileHandler(os.path.join(root_dir, f'logs/{logger_name}.log'), maxBytes=1024 * 1024 * 10, backupCount=5)
        handler.setFormatter(formatter)
        # add the handler to the logger
        logger.addHandler(handler)

    # terminal logging
    if terminal_logging and logging.StreamHandler not in [type(handler) for handler in logger.handlers]:
        # Create handler to output to the terminal
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
