!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: base_error.py
Author: wormhole1026(wormhole1026@gmail.com)
Date: 2015/12/19 16:47:25
"""

import sys
import traceback

class BaseError(Exception):
    """Base Exception for pmclient
    Attributes:
        ret: error code
        msg: error message
        exc: exception in chain
    """
    def __init__(self, ret, msg, exc=None):
        """ init """
        Exception.__init__(self)
        self.errno = ret
        self.message = msg
        self.exc_list = []
        if exc is not None and exc.exc_chain:
            self.exc_list = exc.exc_chain
        exc_info = sys.exc_info()
        if exc_info[0]:
            self.exc_list.append(sys.exc_info())

    def __str__(self):
        """ format string """
        return self.message

    @property
    def ret(self):
        """ get errno """
        return self.errno

    @property
    def msg(self):
        """ get error message """
        return self.message

    @property
    def exc_chain(self):
        """ exception chain """
        return self.exc_list

    def format_exc_chain(self):
        """ format exception chain """
        ret_str = ''
        if not self.exc_list:
            ret_str = "exception chain is empty."
        for exc in self.exc_list:
            ret_str += 'Caused by %s, %s\n' % (exc[0].__name__, exc[1])
            for trbk in traceback.format_tb(exc[2]):
                ret_str += trbk
        return ret_str

    def print_exc_chain(self):
        """ print format_exc_chain """
        try:
            import colorama
            print colorama.Fore.YELLOW + self.format_exc_chain() + colorama.Style.RESET_ALL
        except ImportError:
            print self.format_exc_chain()
            
