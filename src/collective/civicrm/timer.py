# -*- coding: utf-8 -*-
"""Python Timer Class - Context Manager for Timing Code Blocks
Corey Goldberg - 2012
https://gist.github.com/cgoldberg/2942781
"""
from timeit import default_timer


class Timer(object):
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.timer = default_timer

    def __enter__(self):
        self.start = self.timer()
        return self

    def __exit__(self, *args):
        end = self.timer()
        self.elapsed_secs = end - self.start
        self.elapsed = self.elapsed_secs * 1000  # millisecs
        if self.verbose:
            print 'elapsed time: %f ms' % self.elapsed
