#!/usr/bin/env python3
"""simple helper function"""


def index_range(page, page_size):
    """function implementation"""
    start = (page - 1) * page_size
    end = page * page_size
    return (start, end)
