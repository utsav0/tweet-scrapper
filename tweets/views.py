from django.shortcuts import render
from .jobs import get_trending_tweets, time_diff_in_secs
import os
def get_tweets_to_show():
    tweet_list = []
    for each_tweet in get_trending_tweets():
        time_diff = time_diff_in_secs(each_tweet[1])/3600
        time_diff_of_hours = int(time_diff)
        time_diff_of_minutes = int(((time_diff % 1)/10)*60)
        time_diff_final = f"{time_diff_of_hours} hours and {time_diff_of_minutes} minutes older"
        tweet_list.append([each_tweet[0], time_diff_final])
    return tweet_list

def home(request):
    params = {"tweets": get_tweets_to_show()}
    return render(request, "index.html", params)

