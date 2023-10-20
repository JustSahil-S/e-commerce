from email.policy import default
from pyexpat import model
from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Category(models.Model):
    categoryName = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.categoryName}"
def get_default_category():
    cat = Category.objects.get_or_create(categoryName="Uncategorized")
    print(cat)
    return cat[0]
    

class Listing(models.Model):
    creator = models.CharField(max_length=64)
    currentWinner = models.CharField(max_length=64, default="No Winner")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    initialBid = models.FloatField(max_length=25)
    image = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete= models.CASCADE, related_name="categoryListing", default=get_default_category)
    ended = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.id}: {self.title}"

class userWatchlist(models.Model):
    user = models.CharField(max_length=64)
    watchlist = models.ManyToManyField(Listing, blank=True, related_name="watchlist")
    def __str__(self):
        return f"{self.user}"

class Comment(models.Model):
    user = models.CharField(max_length=64)
    contents = models.CharField(max_length=500)
    listing = models.ForeignKey(Listing, on_delete= models.CASCADE, related_name="commentListing")
    def __str__(self):
        return f"Comment by {self.user} on {self.listing.title}"

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete= models.CASCADE, related_name="bidListing")
    user = models.CharField(max_length=64)
    amount = models.FloatField(max_length=25)
    def __str__(self):
        return f"${self.amount} bid by {self.user} on {self.listing.title}"

