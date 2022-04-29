from rest_framework.pagination import PageNumberPagination


class PostPageNumberPagination(PageNumberPagination):
    page_size = 18
    page_size_query_param = 'page_size'
    max_page_size = 25
