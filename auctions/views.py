from curses.ascii import HT
import re
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Listing, userWatchlist, Category, Comment, Bid


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all().filter(ended=False),
        "heading": "Active Listings"

    })

def closed_listings(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all().filter(ended=True),
        "heading": "Closed Listings"
        
    })

def categoryListing(request, categoryName):
    return render(request, "auctions/categoryListing.html", {
        "listings": Listing.objects.all().filter(ended=False).filter(category__categoryName=categoryName.capitalize()), 
        "categoryName": categoryName.capitalize()
    })

@login_required
def new_listing(request):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        initialBid= request.POST['initialBid']
        image = request.POST['image']
        if image == "":
            image = "https://static.thenounproject.com/png/2884221-200.png"
        else: 
            image = image
        cat = request.POST['category']
        cat_object = Category.objects.get(categoryName=cat)
        listing = Listing.objects.create(title=title, description=description, initialBid=initialBid, image=image, category=cat_object, creator=request.user)
        return HttpResponseRedirect(reverse('index'))

    else:
        return render(request, "auctions/newListing.html", {
            "categories": Category.objects.all()
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@login_required
def details(request, name, error = "",):
    print(request.user)
    listing = Listing.objects.get(id=name)
    try:
        watchlistObjects = userWatchlist.objects.get(user=request.user)
    except:
        return HttpResponse("Please sign in to view the listing details.")
    if watchlistObjects.watchlist.all().filter(id=name).exists():
        inWatchlist=True
    else:
        inWatchlist=False

    print(f"watchlistObject:{watchlistObjects}")
    return render(request, "auctions/detail.html", {
       "listingItem":Listing.objects.get(id=name), 
       "inWatchlist":inWatchlist,
       "Comment":Comment.objects.all().filter(listing=name),
       "error_msg":error
    })

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            watchlist = userWatchlist.objects.create(user=username)
            watchlist.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def add_to_watchlist(request, listing_id):
    user = userWatchlist.objects.get(user=request.user)
    add = user.watchlist.add(Listing.objects.get(id=listing_id))
    return HttpResponseRedirect(f"/listings/{listing_id}")

@login_required
def remove_from_watchlist(request, listing_id):
    user = userWatchlist.objects.get(user=request.user)
    add = user.watchlist.remove(Listing.objects.get(id=listing_id))
    return HttpResponseRedirect(f"/listings/{listing_id}")

@login_required
def watchlist(request):
    user = userWatchlist.objects.get(user=request.user)
    listings = user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

def categories(request):
    category = Category.objects.all()
    print(category)
    return render(request, "auctions/categories.html", {
        "category": category
    })

@login_required
def comment(request):
    if request.method == "POST":
        comment = request.POST['comment']
        username = request.user
        listingID = request.POST['listingItemID']
        print(f'listing:{listingID}')
        listing = Listing.objects.get(id=listingID)
        create = Comment.objects.create(user=username, contents=comment, listing=listing)
        return HttpResponseRedirect(f"/listings/{listingID}")
    else: 
        return HttpResponseRedirect(f"/listings/{listingID}")

@login_required
def add_bid(request):
    if request.method == "POST":
        amount = request.POST['bidAmount']
        amount = float(amount)
        listingID = request.POST['listingItemID']
        listing = Listing.objects.get(id=listingID)
        if amount > listing.initialBid:
            bid = Bid.objects.create(listing=listing, user=request.user, amount=amount)
            listing.initialBid=amount
            listing.currentWinner=request.user.username
            listing.save()
            print(listing.initialBid)
            return HttpResponseRedirect(f"/listings/{listingID}")
        else: 
            print(listing.initialBid)
            return details(request, listing.id, "invalid Bid")

    else:
        return HttpResponseRedirect(f"/listings/{listingID}")

@login_required
def end_listing(request):
    listingID = request.POST['listingItemID']
    listing=Listing.objects.get(id=listingID)
    listing.ended=True
    listing.save()
    winner = listing.currentWinner
    return details(request, listing.id)




