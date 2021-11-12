from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
    DetailView,
)
from django.views.generic.detail import SingleObjectMixin
from .models import Listing, Bid, Comment, Category, User
from .models import User


def catagories(request):
    return {"categories": Category.objects.all()}


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


class Index(ListView):
    model = Listing
    template_name = "auctions/index.html"
    context_object_name = "listings"
    paginate_by = 5

    def get_queryset(self):
        return Listing.objects.all().filter(is_active=True)
        # return Listing.objects.active()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["bids"] = Bid.objects.all()
        return context


class ListingDetail(DetailView, SingleObjectMixin):
    model = Listing
    template_name = "auctions/listing_detail.html"
    context_object_name = "listing"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bids"] = Bid.objects.filter(listing=self.object)
        context["comments"] = Comment.objects.filter(listing=self.object)
        return context


class CreateListing(CreateView):
    model = Listing
    fields = ["title", "description", "starting_bid", "image_url", "category"]
    template_name = "auctions/create_listing.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("listing_detail", kwargs={"slug": self.object.slug})
