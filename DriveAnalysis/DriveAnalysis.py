#!/usr/bin/env python310
# -*- coding: utf-8 -*-
import logging
import os
import pandas as pd
import pathlib
import sys
import time
import datetime
import math
import csv
from collections import OrderedDict

__author__ = "Derek Whang"
__version__ = "1.0"
__maintainer__ = "Derek Whang"
__email__ = "dezz.whang@gmail.com"

class Main:
    def __init__(self, _logger: logging.Logger):
        """
        Initializing script

        Args:
            _logger (Logging.logger): the logger that the class will use
        """
        self.logger = _logger
        self.target_dir = None
        self.filter = None
        self.ending = None

    def run(self):
        """
        Returns:
            bool: True for success, False if errors were encountered
        """
        script_path = "\\\\?\\"+os.path.realpath(__file__)
        script_name = script_path.split("\\")[-1]
        root_folder = script_path.replace(script_name,"")
        self.logger.info(f"{script_name} is now running!")

        # self.target_dir = input("Directory to search: ")
        self.target_dir = "C:\\Users\\dezzw\\OneDrive\\Documents\\_script\\tech-team"
        self.target_dir = pathlib.Path("\\\\?\\"+self.target_dir).absolute()
        if str(self.target_dir).lower() == "q" or str(self.target_dir).lower()=="quit":
            self.logger.info("Quitting script")
            return True

        self.filter = input("Filter filename: ")
        if self.filter.lower() == "q" or self.filter.lower()=="quit":
            self.logger.info("Quitting script")
            return True

        self.ending = input("Filetype: ")
        if self.ending.lower() == "q" or self.ending.lower()=="quit":
            self.logger.info("Quitting script")
            return True

        if not pathlib.Path.exists(self.target_dir):
            self.logger.error("Couldn't find directory.")
            return False

        file_list = self.get_files(self.target_dir)
        if not file_list:
            self.logger.error("Couldn't find any files in directory")
            return False

        df = pd.DataFrame(file_list)
        df.to_csv(root_folder+"output.csv",index=False,header=["file_name","file_path","file_size","file_modified","file_created"])

        return True

    def stuff(self):
        """
            This should do something

        Args:

        """
        return False

    def get_files(self,directory):
        """
        Gets list of folders from targer directory

        Returns:
            bool: True for success, False if errors were encountered
        """
        try:
            file_list = []
            for it in os.scandir(directory):
                if it.is_dir():
                    file_list.extend(self.get_files(it.path))
                if it.is_file():
                    file_mtime = datetime.datetime.fromtimestamp(it.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                    file_ctime = datetime.datetime.fromtimestamp(it.stat().st_ctime).strftime('%Y-%m-%d %H:%M:%S')
                    file_stat = it.stat()
                    file_data = [it.name,it.path,file_stat.st_size,file_mtime,file_ctime]
                    if self.filter and self.ending:
                        if self.filter.lower() in it.name.lower() and it.name.lower().endswith(self.ending.lower()):
                            file_list.append(file_data)
                    elif self.filter:
                        if self.filter.lower() in it.name.lower():
                            file_list.append(file_data)
                    elif self.ending:
                        if it.name.lower().endswith(self.ending.lower()):
                            file_list.append(file_data)
                    else:
                        file_list.append(file_data)

        except Exception:
            self.logger.exception("issue with get_files")
            return False

        return file_list

    def print_banner_text(self, text: str, full_border: bool = False, banner_char: str = '~', total_length: int = 80):
        """
        Print a banner with the provided text centered.

        Args:
            text (str) - the text to put in the middle of the banner
            full_border (bool) - whether or not to add borders above and below
                the line with the text
            banner_char (str) - the character to use for the banner borders
                (trimmed to one character)
            total_length (int) - total characters in line for the banner
        """
        if full_border:
            self.logger.info(banner_char * total_length)

        banner_char_count = total_length - len(text)
        left_chars = banner_char * (banner_char_count // 2)
        right_chars = banner_char * math.ceil(banner_char_count / 2)
        self.logger.info("{}{}{}".format(left_chars, text, right_chars))

        if full_border:
            self.logger.info(banner_char * total_length)


def get_logger(script_path) -> logging.Logger:
    """
    Setup the logger so that it is saved to a file and also is outputted to the
    console.

    Returns:
        Logging.logger: The configured Logger object
    """
    try:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        # logger.setLevel(logging.DEBUG)

        script_name = script_path.split("\\")[-1]
        root_folder = script_path.replace(script_name,"")

        if not os.path.isdir(pathlib.Path(root_folder).joinpath("Logger")):
            os.makedirs(pathlib.Path(root_folder).joinpath("Logger"))

        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)8s] : %(message)s")

        file_handler = logging.FileHandler(str(pathlib.Path(root_folder).joinpath(f"Logger/Logger_{script_name.replace('.py','')}_{datetime.datetime.now().strftime('%m-%d_%H%M')}.log")))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        return logger
    except Exception as e:
        print("Failed logging setup, how'd you manage that?")
        print(e)
        print("Exiting now!")
        sys.exit()

def exit_script(error_status: bool, logger: logging.Logger, script_name):
    """
    Exit the script, printing logging information as this is done.

    Args:
        error_status (boolean) - false indicates the script is
            exiting with errors, true indicates a clean run
        logger (Logger) - the logger to use
    """
    logger.info(f"{script_name} is exiting")
    if error_status:
        logger.info(f"{script_name} ran without errors")
    else:
        logger.error(f"{script_name} exited with errors")
    sys.exit()

if __name__ == "__main__":
    script_path = "\\\\?\\"+os.path.realpath(__file__)
    script_name = script_path.split("\\")[-1]
    logger = get_logger(script_path)

    start_time = time.time()
    logger.info(f"{script_name} is starting...")

    call_class = Main(logger)
    run_status = call_class.run()

    end_time = time.time()

    logger.info(f"Runtime: {round(end_time - start_time, 2)}s")

    exit_script(run_status, logger, script_name)
