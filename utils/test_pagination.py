from unittest import TestCase

from utils.pagination import make_pagination_range


class PaginationTest(TestCase):
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):  # noqa E501
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=2,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=3,
        )['pagination']
        self.assertEqual([2, 3, 4, 5], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=4,
        )['pagination']
        self.assertEqual([3, 4, 5, 6], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=5,
        )['pagination']
        self.assertEqual([4, 5, 6, 7], pagination)

    def test_make_sure_middle_ranges_are_correct(self):

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=3,
        )['pagination']
        self.assertEqual([2, 3, 4, 5], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=10,
        )['pagination']
        self.assertEqual([9, 10, 11, 12], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 100)),
            qty_pages=4,
            current_page=31,
        )['pagination']
        self.assertEqual([30, 31, 32, 33], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 100)),
            qty_pages=4,
            current_page=32,
        )['pagination']
        self.assertEqual([31, 32, 33, 34], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=17,
        )['pagination']
        self.assertEqual([16, 17, 18, 19], pagination)

    def test_is_static_range_if_last_page_is_in_the_range(self):

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=18,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=19,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=20,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 51)),
            qty_pages=4,
            current_page=48,
        )['pagination']
        self.assertEqual([47, 48, 49, 50], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 51)),
            qty_pages=4,
            current_page=49,
        )['pagination']
        self.assertEqual([47, 48, 49, 50], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 51)),
            qty_pages=4,
            current_page=50,
        )['pagination']
        self.assertEqual([47, 48, 49, 50], pagination)
