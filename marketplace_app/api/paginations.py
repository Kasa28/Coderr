from rest_framework.pagination import PageNumberPagination


class OffersResultPagination(PageNumberPagination):
    page_size = 6
