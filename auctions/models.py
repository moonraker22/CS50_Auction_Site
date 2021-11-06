from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# one for auction listings, one for bids, and one for comments made on auction listings.
#  They should be able to specify a title for the listing, a text-based description, and
# what the starting bid should be.Users should also optionally be able to provide a URL
# for an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home,
# etc.).


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    # Watchlist


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    class Meta:
        verbose_name_plural = "Catagories"
        ordering = ("name",)

    def get_absolute_url(self):
        return reverse("catagory_detail", args=[self.slug])

    def __str__(self):
        return self.name


# class ListingManager(models.Manager):
#     def active(self):
#         return super().get_queryset().filter(is_active=True)

#     def expired(self):
#         return super().get_queryset().filter(is_active=False)


class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=50)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=6, decimal_places=2)
    history = models.ManyToManyField(User, through="Bid", related_name="bids")
    image_url = models.URLField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(max_length=50)
    # objects = models.Manager()
    # ListingManager = ListingManager()

    class Meta:
        verbose_name_plural = "Listings"
        ordering = ("-starting_bid",)

    def get_absolute_url(self):
        return reverse("listing_detail", args=[self.slug])

    def __str__(self):
        return self.title


class Bid(models.Model):
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid_time = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=50)

    class Meta:
        verbose_name_plural = "Bids"
        ordering = (
            "-listing",
            "-amount",
        )

    def place_bid(self, bid_amount):
        if bid_amount > self.listing.current_bid:
            self.amount = bid_amount
            self.save()
            self.listing.current_bid = bid_amount
            self.listing.save()
            return True
        else:
            return False

    def get_absolute_url(self):
        return reverse("bid_detail", args=[self.slug])

    def __str__(self):
        return f"{self.user} bid {self.amount} on {self.listing}"


class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.CharField(max_length=50)

    class Meta:

        verbose_name_plural = "Comments"
        ordering = ("-created",)

    def get_absolute_url(self):
        return reverse("comment_detail", args=[self.slug])

    def __str__(self):
        return f"{self.user} commented on {self.listing}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=50)

    class Meta:
        ordering = ("-created",)

    def get_absolute_url(self):
        return reverse("watchlist_detail", args=[self.slug])

    def __str__(self):
        return f"{self.user} added {self.listing} to watchlist"