#!/usr/bin/env python3
"""simple pagination"""
import csv
import math
from typing import List


def index_range(page, page_size):
    """function implementation"""
    start = (page - 1) * page_size
    end = page * page_size
    return (start, end)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """get page"""
        assert isinstance(page, int)
        assert isinstance(page_size, int)
        assert page > 0
        assert page_size > 0
        page_infos = index_range(page, page_size)
        try:
            self.__dataset = self.dataset()
            indexed = []
            for i in range(page_infos[0], page_infos[1]):
                indexed.append(self.__dataset[i])
            return indexed
        except Exception as e:
            return []
