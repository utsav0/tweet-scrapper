from django.shortcuts import render
from .jobs import get_tweets_to_show, delete_older_tweets, scrape
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


def home(request):
    tweets = get_tweets_to_show()
    print("the length of the tweets: ",len(tweets))

    if len(tweets) > 0:
        tweets_not_available_msg = ""
    else:
        tweets_not_available_msg = "Oops! No tweets available, please check back later."
    params = {"tweets": tweets, "tweets_not_available_msg": tweets_not_available_msg}
    return render(request, "index.html", params)


