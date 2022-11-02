from django.shortcuts import render
from .jobs import get_trending_tweets, time_diff_in_secs, delete_older_tweets, scrape

import threading
import time
from schedule import Scheduler

# Initiates the whole scrapping process
def awake_scrapper():
    delete_older_tweets()
    scrape()

def run_continuously(self, interval=7200):

    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):

        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                self.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.setDaemon(True)
    continuous_thread.start()
    return cease_continuous_run

Scheduler.run_continuously = run_continuously

def start_scheduler():
    scheduler = Scheduler()
    scheduler.every().second.do(awake_scrapper)
    scheduler.run_continuously()
start_scheduler()

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

