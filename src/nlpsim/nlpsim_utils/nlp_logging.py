#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
 *************************************************************************
 *
 * AUDIO FIRST COMMERCE PRIVATE LIMITED Confidential
 * Copyright (c) 2020 AUDIO FIRST COMMERCE PRIVATE LIMITED.
 * All Rights Reserved.
 *
 * NOTICE:  All information contained herein is, and remains the property of
 * AUDIO FIRST COMMERCE PRIVATE LIMITED and its suppliers, if any. The intellectual
 * and technical concepts contained herein are proprietary to AUDIO FIRST COMMERCE
 * PRIVATE LIMITED and its suppliers and may be covered by Indian and Foreign Patents,
 * patents in process, and are protected by trade secret or copyright law. Dissemination
 * of this information or reproduction of this material is strictly forbidden unless
 * prior written permission is obtained from AUDIO FIRST COMMERCE PRIVATE LIMITED.
 *
 *************************************************************************
"""

import os, sys
from pathlib import Path


class LogAppStd:
    def __init__(self, log_file_dir):
        import logging
        from logging.handlers import RotatingFileHandler
        _rest_api_call_path = log_file_dir
        if log_file_dir is None:
            _rest_api_call_path = './../apps/nlp/'
        _basepath = _rest_api_call_path #os.path.basename(_rest_api_call_path)
        print(_basepath)
        _LOGFILE_PATH = _basepath / Path("nlp_logs/nlp_app.log")
        print(_LOGFILE_PATH, _LOGFILE_PATH.parent)

        _STDOUT_LEVEL = logging.ERROR
        _LOGFILE_MBSZ = 30*1024*1024  # filesize in MB, x2 files
        _LOGFILE_LEVL = logging.DEBUG

        os.makedirs(_LOGFILE_PATH.parent, mode=0o700,exist_ok=True)

        formatter = logging.Formatter('%(asctime)-15s - %(name)s - %(levelname)s - %(message)s')

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(_STDOUT_LEVEL)
        stdout_handler.setFormatter(formatter)

        file_handler = RotatingFileHandler(_LOGFILE_PATH,
                                           maxBytes=_LOGFILE_MBSZ,
                                           backupCount=10)
        file_handler.setLevel(_LOGFILE_LEVL)
        file_handler.setFormatter(formatter)

        logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
        root = logging.getLogger()
        root.addHandler(stdout_handler)
        root.addHandler(file_handler)
        self.logging = root
        pass

    def log_error(self, s):
        self.logging.error(s)

    def log_debug(self, s):
        self.logging.debug(s)

    def log_info(self, s):
        self.logging.info(s)

