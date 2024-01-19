from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid

def listing(request, id):
    listing_data = Listing.objects.get(pk=id)
    in_watchlist = request.user in listing_data.watchlist.all()
    comments = Comment.objects.filter(listing=listing_data)
    is_owner = request.user.username == listing_data.owner.username
    return render(request, "auctions/listing.html", {
        "listing": listing_data,
        "in_watchlist": in_watchlist,
        "comments": comments,
        "is_owner": is_owner
    })

def close_auction(request, id):
    listing_data = Listing.objects.get(pk=id)
    in_watchlist = request.user in listing_data.watchlist.all()
    comments = Comment.objects.filter(listing=listing_data)
    is_owner = request.user.username == listing_data.owner.username
    listing_data.isActive = False
    listing_data.save()
    return render(request, "auctions/listing.html", {
            "listing": listing_data,
            "message": "Your auction has been closed.",
            "update": True,
            "in_watchlist": in_watchlist,
            "comments": comments,
            "is_owner": is_owner,
        })

def add_bid(request, id):
    new_bid = request.POST['new_bid']
    listing_data = Listing.objects.get(pk=id)
    in_watchlist = request.user in listing_data.watchlist.all()
    comments = Comment.objects.filter(listing=listing_data)
    is_owner = request.user.username == listing_data.owner.username
    current_user = request.user
    listing_data.watchlist.add(current_user)
    if int(new_bid) > listing_data.price.bid:
        update_bid = Bid(user=request.user, bid=int(new_bid))
        update_bid.save()
        listing_data.price = update_bid
        listing_data.save()
        return render(request, "auctions/listing.html", {
            "listing": listing_data,
            "message": "Bid was placed successfully",
            "update": True,
            "in_watchlist": in_watchlist,
            "comments": comments,
            "is_owner": is_owner,
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing_data,
            "message": "Bid failed",
            "update": False,
            "in_watchlist": in_watchlist,
            "comments": comments,
            "is_owner": is_owner,
        })

def add_comment(request, id):
    current_user = request.user
    listing_data = Listing.objects.get(pk=id)
    message = request.POST['new_comment']
    
    new_comment = Comment(
        author = current_user,
        listing = listing_data,
        message = message
    )

    new_comment.save()

    return HttpResponseRedirect(reverse("listing", args=(id, )))

def watchlist(request):
    current_user = request.user
    listings = current_user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings,
    })

def add_watchlist(request, id):
    listing_data = Listing.objects.get(pk=id)
    current_user = request.user
    listing_data.watchlist.add(current_user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def remove_watchlist(request, id):
    listing_data = Listing.objects.get(pk=id)
    current_user = request.user
    listing_data.watchlist.remove(current_user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def index(request):
    active_listings = Listing.objects.filter(isActive=True)
    all_categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": active_listings,
        "categories": all_categories
    })

def categories(request):
    active_listings = Listing.objects.filter(isActive=True)
    all_categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": active_listings,
        "categories": all_categories
    })

def display_category(request):
    if request.method == "POST":
        choice = request.POST['category']
        category = Category.objects.get(categoryName = choice)
        active_listings = Listing.objects.filter(isActive=True, category=category)
        all_categories = Category.objects.all()
        return render(request, "auctions/index.html", {
            "listings": active_listings,
            "categories": all_categories
        })
   
def create_listing(request):
    if request.method == "GET":
        all_categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": all_categories
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        imageurl = request.POST["imageurl"]
        price = request.POST["price"]
        category = request.POST["category"]

        current_user = request.user

        category_data = Category.objects.get(categoryName = category)

        bid = Bid(bid=int(price), user=current_user)
        bid.save()

        new_listing = Listing(
            title=title,
            description=description,
            imageurl=imageurl,
            price=bid,
            category=category_data,
            owner=current_user,
        )

        new_listing.save()
        return HttpResponseRedirect(reverse(index))


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
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
