from rest_framework.pagination import PageNumberPagination


class FeedPageNumberPagination(PageNumberPagination):
    page_size = 27
    page_size_query_param = 'page_size'
    max_page_size = 50
    # pagination_class = searchPageNumberPagination