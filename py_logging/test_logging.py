#!/usr/bin/env python
# encoding: utf-8

import logging
import os
import time
from unittest import TestCase


class TestLogging(TestCase):
    def setUp(self):
        dir_path = os.path.dirname(__file__)
        self.logfile = os.path.join(dir_path, "tmp.log")
        self.logger = logging.getLogger(
            "test_logger_%s" % int(time.time() * 1000))

    def tearDown(self):
        if os.path.exists(self.logfile):
            os.remove(self.logfile)

    def log_lines(self):
        with open(self.logfile, "rt") as fp:
            return [l.strip() for l in fp]

    def test_logger(self):
        self.assertEqual(self.logger.level, logging.NOTSET)

    def test_filehandler(self):
        filehdr = logging.FileHandler(self.logfile)
        self.logger.addHandler(filehdr)
        self.logger.setLevel(logging.INFO)

        self.logger.debug("debug")
        self.logger.info("info")
        self.logger.warning("warning")
        self.logger.error("error")
        self.logger.critical("critical")

        self.assertListEqual(self.log_lines(), [
            "info", "warning", "error", "critical"])

    def test_format(self):
        filehdr = logging.FileHandler(self.logfile)
        logfmt = logging.Formatter("test: %(name)s %(levelname)-8s %(message)s")
        filehdr.setFormatter(logfmt)
        self.logger.addHandler(filehdr)
        self.logger.setLevel(logging.INFO)

        self.logger.info("info")

        self.assertListEqual(self.log_lines(), [
            "test: %s INFO     info" % (self.logger.name,)])
