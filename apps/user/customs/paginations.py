from collections import OrderedDict

from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response


class CustomPagination(LimitOffsetPagination):
    def paginate(self, limit=10, page=1, request=None, queryset=None, view=None):
        self.limit = int(limit) * int(page)
        if self.limit is None:
            return None

        self.count = self.get_count(queryset)
        self.offset = self.limit - int(limit)
        self.request = request
        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True

        if self.count == 0 or self.offset > self.count:
            return []
        return list(queryset[self.offset : self.limit])


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "limit"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("total", self.page.paginator.count),
                    ("count", len(data)),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                    ("status", status.HTTP_200_OK),
                ]
            ),
            status=status.HTTP_200_OK,
        )
