from django.contrib import admin

from .models import Listing, Category, userWatchlist, Comment, Bid, User
# Register your models here.

admin.site.register(Listing)
admin.site.register(Category)
admin.site.register(userWatchlist)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(User)
