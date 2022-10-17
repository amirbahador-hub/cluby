from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    page_size_query_param = 'limit'
    max_page_size = 30

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'nextIndex': self.page.next_page_number() if self.page.has_next() else None,
            'previousIndex': self.page.previous_page_number() if self.page.has_previous() else None,
            'results': data,
        })


