#!/usr/bin/env python3
"""simple pagination"""
import csv
import math
from typing import Dict
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

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """get hyper"""
        data = self.get_page(page, page_size)
        page_data = {'page_size': page_size, 'page': page}
        page_data['data'] = data
        if len(data) == 0:
            page_data['page_size'] = 0
            page_data['next_page'] = None
        else:
            if index_range(page, page_size)[1] == len(self.__dataset) - 1:
                page_data['next_page'] = None
            else:
                page_data['next_page'] = page + 1
        if page == 1:
            page_data['prev_page'] = None
        else:
            page_data['prev_page'] = page - 1
        size = len(self.__dataset) / page_size
        if size % 2 == 0:
            page_data['total_pages'] = len(self.__dataset) // page_size
        else:
            page_data['total_pages'] = 1 + (len(self.__dataset) // page_size)

        return page_data
