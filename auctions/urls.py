from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings/closed", views.closed_listings, name="closedListings"),
    path("listings/category/<str:categoryName>", views.categoryListing, name="categoryListing"),
    path("listings/add", views.new_listing, name="addListing"),
    path("listings/<str:name>", views.details, name="details"),
    path("watchlist/add/<str:listing_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("watchlist/remove/<str:listing_id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("comment", views.comment, name="addComment"),
    path("bid/add", views.add_bid, name="addBid"),
    path("bid/end", views.end_listing, name="endListing"),



]
