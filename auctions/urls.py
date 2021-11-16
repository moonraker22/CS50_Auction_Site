from django.urls import path

from . import views
from .views import Index, ListingDetail, CreateListing, WatchlistView

urlpatterns = [
    # path("", views.index, name="index"),
    path("", Index.as_view(), name="index"),
    path("listing_detail/<slug:slug>/", ListingDetail.as_view(), name="listing_detail"),
    path("create_listing/", CreateListing.as_view(), name="create_listing"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("add_to_watchlist/", views.add_to_watchlist, name="add_to_watchlist"),
    path("watchlist/", WatchlistView.as_view(), name="watchlist"),
]
