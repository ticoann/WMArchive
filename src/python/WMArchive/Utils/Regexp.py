#!/usr/bin/env python
#-*- coding: utf-8 -*-
#pylint: disable=
"""
File       : Regexp.py
Author     : Valentin Kuznetsov <vkuznet AT gmail dot com>
Description: Module for common regular expressions
"""
# futures
from __future__ import print_function, division

# system modules
import re

# global regexp
PAT_QUERY = re.compile(r"^[a-zA-Z]+")
PAT_INFO = re.compile(r"^[0-9]$")
PAT_UID = re.compile(r"^[a-z0-9]{32,32}$")
