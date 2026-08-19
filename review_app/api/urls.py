from django.urls import path
from review_app.api.views import ReviewsView

urlpatterns = [
    path("reviews/", ReviewsView.as_view(), name="review-list-create"),
]
