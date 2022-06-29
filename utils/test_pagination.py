from unittest import TestCase

from utils.pagination import make_pagination_range


class PaginationTest(TestCase):

    def test_make_pagination_range_is_correct_in_beginning(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1
        )['pagination']
        self.assertEqual(pagination, [1, 2, 3, 4])

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=2
        )['pagination']
        self.assertEqual(pagination, [1, 2, 3, 4])

    def test_make_pagination_range_is_correct_in_middle(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=4
        )['pagination']
        self.assertEqual(pagination, [3, 4, 5, 6])

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=6
        )['pagination']
        self.assertEqual(pagination, [5, 6, 7, 8])

    def test_make_pagination_range_is_correct_in_end(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=18
        )['pagination']
        self.assertEqual(pagination, [17, 18, 19, 20])

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=19
        )['pagination']
        self.assertEqual(pagination, [17, 18, 19, 20])

    def test_make_pagination_range_works_with_few_pages(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 3)),
            qty_pages=4,
            current_page=2
        )['pagination']
        self.assertEqual(pagination, [1, 2])
