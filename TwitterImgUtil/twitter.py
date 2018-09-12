#!/usr/bin/env python
# encoding: utf-8
# Author - Prateek Mehta


import tweepy  # https://github.com/tweepy/tweepy
import json

# Twitter API credentials

def twitter_OAuth_login():
    # need consumer_key, consumer_secret, access_key, access_secret from files
    secret_dict = {'consumer_key': '',
                   'consumer_secret': '',
                   'access_key': '',
                   'access_secret': ''}
    # try open config file
    try:
        file = open('twitter_dev.ini', 'r')
    except:
        print("open config file fail!")
        return None
    # record key & secret mentioned above
    for line in file:
        if line[-1] == '\n':
            line = line[:-1]
        elements = line.split('=')
        if elements[0] in secret_dict.keys():
            secret_dict[elements[0]] = elements[1]
    file.close()
    # try access to twitter by OAuth
    try:
        auth = tweepy.OAuthHandler(secret_dict['consumer_key'], secret_dict['consumer_secret'])
        auth.set_access_token(secret_dict['access_key'], secret_dict['access_secret'])
        api = tweepy.API(auth)
    except tweepy.TweepError:
        print("fail to access to twitter by OAuth")
        print(secret_dict)
        return None

    return api



def get_all_tweets(screen_name):
    # Twitter only allows access to a users most recent 3240 tweets with this method
    api = twitter_OAuth_login()
    if api is None:
        print("fail to authorize twitter. please check twitter_dev.ini and network condition")
        return

    alltweets = []
    curr_page = 1

    new_tweets = api.user_timeline(screen_name=screen_name,count=200,tweet_mode='extended')
    alltweets.extend(new_tweets)

    oldest = alltweets[-1].id - 1

    while len(new_tweets) > 0:

        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest, tweet_mode='extended')

        alltweets.extend(new_tweets)

        oldest = alltweets[-1].id - 1
        if (len(alltweets) > 3000):
            break
        print("...%s tweets downloaded so far" % (len(alltweets)))

    file = open('tweet.json', 'w')
    print("Writing tweet objects to JSON please wait...")
    for status in alltweets:
        json.dump(status._json, file, sort_keys=True, indent=4)

    file.close()


if __name__ == '__main__':
    # pass in the username of the account you want to download
    get_all_tweets("@foofighters")