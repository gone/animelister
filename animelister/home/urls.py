from django.urls import path
from django.views.generic.base import TemplateView

from .views import (
    error,
    dashboard,
    HomeView,
    AnimeDetailView,
    UserRatingView,
    FixedHomeView,
)

urlpatterns = [
    path(r"error/", error, name="error"),
    path("dashboard/", dashboard, name="dashboard"),
    path("<slug:slug>/", AnimeDetailView.as_view(), name="anime-detail"),
    path("<slug:slug>/rating", UserRatingView.as_view(), name="rate-anime"),
    path("fix", FixedHomeView.as_view(), name="fixedindex"),
    path("", HomeView.as_view(), name="index"),
]
