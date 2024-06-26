from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django import forms

from .models import User, Auction, Watchlist

# Forms

class CreateListingForm(forms.ModelForm):
    title = forms.CharField(label="Title", max_length=20, required=True)
    description = forms.CharField(label="Description", required=True, widget=forms.Textarea)
    bid = forms.CharField(label="Starting bid", max_length=20, required=False)
    image = forms.CharField(label="Image URL:", required=False)
    category = forms.CharField(label="Category:", required=False)

    class Meta:
        model = Auction
        fields = ["title", "description", "bid", "image", "category"]

# Views


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Auction.objects.all()
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
    
def create(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            bid = form.cleaned_data['bid']
            image = form.cleaned_data['image']
            category = form.cleaned_data['category']

            auction = Auction(
                title=title, 
                description=description,
                bid=bid,
                image=image,
                category=category)
            
            auction.save()
        else:
            return render(request, "auctions/create.html", {
                "form": form
            })
    
    return render(request, "auctions/create.html", {
        "form": CreateListingForm()
    })

def listing(request, auction_id):
    
    auction = get_object_or_404(Auction, id=auction_id)

    if request.user.is_authenticated: 
        is_in_watchlist = Watchlist.objects.filter(user=request.user, listing=auction).exists()
        
        if request.method == "POST":
            watchlist_item = Watchlist.objects.filter(user=request.user, listing=auction)
            if is_in_watchlist:
                watchlist_item.delete()
                is_in_watchlist = Watchlist.objects.filter(user=request.user, listing=auction).exists()
            else:
                Watchlist.objects.get_or_create(user=request.user, listing=auction)
                is_in_watchlist = Watchlist.objects.filter(user=request.user, listing=auction).exists()
           
    return render(request, "auctions/listing.html", {
        "listing": auction,
        "is_in_watchlist": is_in_watchlist
    })

@login_required(login_url="login")
def watch(request):

    watchlist_items = Watchlist.objects.filter(user=request.user)

    return render(request, "auctions/watch.html", {
        "watchlist_items": watchlist_items
    })
