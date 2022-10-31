from django.contrib import admin

# Register your models here.

from .models import scrapped_tweet, trending_tweet

admin.site.register(scrapped_tweet)
admin.site.register(trending_tweet)