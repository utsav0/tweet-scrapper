import tweepy
import datetime
import os
from .models import scrapped_tweet, trending_tweet as trending_tweet_ids

secret_key = os.environ.get('secret_key')

secret_key_api = os.environ.get('secret_key_api')

access_token = os.environ.get('access_token')

access_token_api = os.environ.get('access_token_api')

secret_key = "0DGIfbKapOjP2BvCSpp3UBMOL"

secret_key_api = "TllXoqSqGOGuLoIOc1s0qlPmbVphFNT00Pyl4nhGQuZ3dubYV4"

access_token = "1584841697783328773-txFqi7OKlmKf1oZpAnd52JFtqpoobt"

access_token_api = "DFZZCZHOkWqnc1Kkyz2pwH3iQboKzk73NLxbL8ETcIgQM"

auth = tweepy.OAuthHandler(secret_key, secret_key_api)

auth.set_access_token(access_token, access_token_api)

api = tweepy.API(auth)


# Returns the ids of all the tweets scrapped last time
def get_last_search():
    return list((scrapped_tweet.objects.values_list("tweet_id")))

# Update the latest scrapped tweets

def update_timeline(ids_list):
    scrapped_tweet.objects.all().delete()
    for each_id in ids_list:
        new_id = scrapped_tweet(tweet_id=each_id)
        new_id.save()

# Gets the number of replies on a particular tweet
# Currently, not in use
def get_replies_count(id, user_name):
    reply_count = 0
    yesterdays_date = datetime.date.today()-datetime.timedelta(days = 1)
    replies = api.search_tweets(q=f"(to:{user_name}) since:{yesterdays_date} filter:replies", count=100)
    for this_tweet in replies:
        if this_tweet.in_reply_to_status_id == id:
            reply_count += 1
    return reply_count
# Check if a tweet is trending or not

def trending_tweet(tweet):
    current_time = datetime.datetime.now(datetime.timezone.utc)
    time_diff_in_secs = (current_time - tweet.created_at).total_seconds()
    time_diff_in_hrs = time_diff_in_secs / 3600
    required_likes_count = time_diff_in_hrs*15
    required_retweet_count = time_diff_in_hrs*1
    # When time pased after posting is less than 28800 seconds(8 hours).
    # Likes getting are more or equal to 50 per hour.
    # Retweets getting are more or equal to 6 per hour.
    if (time_diff_in_secs < 36000) and (tweet.favorite_count >= required_likes_count) and (tweet.retweet_count >= required_retweet_count):
        return True
    else:
        return False


# Gets the latest tweets by seaching and then check if they're trending

def scrape():
    tweet_id_list = []
    current_date = str(datetime.date.today())
    searched_tweets = api.search_tweets(
        q=f"(programming OR devs OR coding OR HTML OR CSS OR programmer OR developers OR developer) min_replies:20 min_faves:19 min_retweets:3 lang:en since:{current_date} -filter:links -filter:replies", count=100)
    for this_tweet in searched_tweets:
        this_tweet_id = this_tweet.id
        tweet_id_list.append(this_tweet_id)
        if (this_tweet_id,) in get_last_search():
            pass
        else:
            if trending_tweet(this_tweet):
                new_trending_tweet = trending_tweet_ids(
                    tweet_id=this_tweet_id, tweet_time=this_tweet.created_at)
                new_trending_tweet.save()
            else:
                pass
    update_timeline(tweet_id_list)
# Update the old trending list to the given new list

def update_treding_list(updated_tweet_list):
    trending_tweet_ids.objects.all().delete()
    for each_trending_tweet in updated_tweet_list:
        new_trending_tweet = trending_tweet_ids(
            tweet_id=each_trending_tweet[0], tweet_time=each_trending_tweet[1])
        new_trending_tweet.save()

# Gets the existing trending tweets list


def get_trending_tweets():
    trending_tweets_list = trending_tweet_ids.objects.values_list(
        "tweet_id", "tweet_time")
    return (trending_tweets_list)


def time_diff_in_secs(tweet_time):
    current_time_without_tz = datetime.datetime.utcnow()
    current_time = current_time_without_tz.replace(
        tzinfo=datetime.timezone.utc)
    return (current_time - tweet_time).total_seconds()

# Deletes the trending tweets that are older than 18 hours


def delete_older_tweets():
    trending_tweet_list = get_trending_tweets()
    updated_trending_tweets = []
    for this_tweet in trending_tweet_list:
        if time_diff_in_secs(this_tweet[1]) > 72000:
            # When the tweet is older than 20 hours
            pass
        else:
            updated_trending_tweets.append(this_tweet)
    update_treding_list(updated_trending_tweets)


def get_tweets_to_show():
    tweet_list = []
    for each_tweet in get_trending_tweets():
        time_diff = time_diff_in_secs(each_tweet[1])/3600
        time_diff_of_hours = int(time_diff)
        time_diff_of_minutes = int(((time_diff % 1)/10)*60)
        time_diff_final = f"{time_diff_of_hours} hours and {time_diff_of_minutes} minutes older"
        tweet_list.append([each_tweet[0], time_diff_final])
    return tweet_list