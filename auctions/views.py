from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django import forms

from .models import User, Auction

# Forms

class CreateListingForm(forms.ModelForm):
    title = forms.CharField(label="Title", max_length=20, required=True)
    description = forms.CharField(label="Description", required=True, widget=forms.Textarea)
    bid = forms.CharField(label="Starting bid:", max_length=20, required=False)
    image = forms.CharField(label="Image URL:")
    category = forms.CharField(label="Category:")

    class Meta:
        model = Auction
        fields = ["title", "description", "bid", "image", "category"]

# Views


def index(request):
    return render(request, "auctions/index.html")


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
