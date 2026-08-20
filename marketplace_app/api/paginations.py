from rest_framework.pagination import PageNumberPagination


class OffersResultPagination(PageNumberPagination):
    """Return offer lists in pages containing six results."""

    page_size = 6
