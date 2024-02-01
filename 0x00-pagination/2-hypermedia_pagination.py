#!/usr/bin/env python3
"""Simple Pagination Module
"""

from typing import Dict, Tuple, List
import csv
import math


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
        """paginate the dataset correctly and
        return the appropriate page of the dataset
        """
        if type(page) is not int or type(page_size) is not int:
            assert ()
        if page <= 0 or page_size <= 0:
            assert ()
        page_range = index_range(page, page_size)

        try:
            return self.dataset()[page_range[0]:page_range[1]]
        except Exception:
            pass

        return []

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """paginate the dataset correctly and
        return the appropriate page of the dataset
        """
        if type(page) is not int or type(page_size) is not int:
            assert ()
        if page <= 0 or page_size <= 0:
            assert ()
        total_pages = math.ceil(len(self.dataset())/page_size)
        data = self.get_page(page, page_size)
        next_page = page+1 if page < total_pages else None
        prev_page = page-1 if page > 1 else None

        return {
            "page_size": len(data),
            "page": page, "data": data, "next_page": next_page,
            "prev_page": prev_page, "total_pages": total_pages}


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    return a tuple of size two containing a start index and an end index
    corresponding to the range of indexes to return in a list for
    those particular pagination parameters
    """
    start_index = (page-1)*page_size
    end_index = start_index+page_size

    return (start_index, end_index)
