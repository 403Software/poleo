"""
It is responsible for recommendation functionality, as also
providing the available filters that go along with the result

...

Methods
-------
get_documents(query_base_request, documents_deploy_request)
    Disables recommendation resource creation calls
"""
import cProfile
import pstats
import io
import os
import sys
import logging
from logging.handlers import TimedRotatingFileHandler
from time import perf_counter
from config import get_current_config

LEVEL = get_current_config().LOG_LEVEL

FORMATTER = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

def create_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def create_file_handler(file_name: str):
    log_file_name = f'{file_name}.log'
    log_file_path = os.path.join(get_current_config().LOGS_PATH, log_file_name)
    
    try:
        file = open(log_file_path, 'r+')
    except FileNotFoundError:
        if not os.path.exists(os.path.join(get_current_config().LOGS_PATH)):
            os.makedirs(os.path.join(get_current_config().LOGS_PATH))
        file = open(log_file_path, 'w+')

    file.close()
    file_handler = TimedRotatingFileHandler(
        log_file_path, when='midnight', encoding='UTF-8')
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(name='default', file_name='log'):
    log = logging.getLogger(name)
    log.setLevel(LEVEL)
    log.addHandler(create_console_handler())
    log.addHandler(create_file_handler(file_name))
    log.propagate = False
    return log


class Logger:
    def __init__(self):
        self.log = get_logger()
        self.__start = 0

    def info(self, msg):
        self.log.info(msg)

    def exception(self, error):
        self.log.exception(error)


class Chronometer:

    def __init__(self):
        self.__start = 0

    def start(self):
        self.__start = perf_counter()

    def end(self):
        result = perf_counter() - self.__start
        self.__start = 0
        return result


def profile(fnc):
    def inner(*arg, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*arg, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        log = get_logger()
        log.info(s.getvalue())
        return retval
    return inner


chrono = Chronometer()
logger = Logger()
