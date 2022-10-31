from django.db import models

# Create your models here.

class scrapped_tweet(models.Model):
    tweet_id = models.IntegerField(default= None, null=True)

class trending_tweet(models.Model):
    tweet_id = models.IntegerField()
    tweet_time = models.DateTimeField()