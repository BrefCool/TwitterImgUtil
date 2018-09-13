#!/usr/bin/env python
# encoding: utf-8
# Author - Prateek Mehta


import tweepy  # https://github.com/tweepy/tweepy
import json
import urllib
import os

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

def extract_images_url(file_name='tweet.json'):
    image_urls = []
    with open(file_name) as file:
        data = json.loads(file.read())

    for tweet in data:
        if 'extended_entities' in tweet.keys():
            extended_entities = tweet['extended_entities']['media']
            for extended_entity in extended_entities:
                if 'photo' == extended_entity['type']:
                    image_urls.append(extended_entity['media_url'])

    return image_urls

def download_images(user, urls=[]):
    save_path = './download_images/'
    count = 0
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    save_path += user
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    for url in urls:
        save_name = 'image-%05d.jpg' % count
        with open(save_path+'/'+save_name, 'wb') as file:
            file.write(urllib.request.urlopen(url).read())
        count += 1

def get_all_tweets(screen_name):
    # Twitter only allows access to a users most recent 3240 tweets with this method
    api = twitter_OAuth_login()
    if api is None:
        print("fail to authorize twitter. please check twitter_dev.ini and network condition")
        return

    alltweets = []
    alltweets_json = []

    new_tweets = api.user_timeline(screen_name=screen_name,count=10,tweet_mode='extended')
    alltweets.extend(new_tweets)

    oldest = alltweets[-1].id - 1

    while len(new_tweets) > 0:

        new_tweets = api.user_timeline(screen_name=screen_name, count=50, max_id=oldest, tweet_mode='extended')

        alltweets.extend(new_tweets)

        oldest = alltweets[-1].id - 1
        if (len(alltweets) > 500):
            break
        print("...%s tweets downloaded so far" % (len(alltweets)))

    file = open('tweet.json', 'w')
    print("Writing tweet objects to JSON please wait...")
    for status in alltweets:
        alltweets_json.append(status._json)

    json.dump(alltweets_json, file, sort_keys=True, indent=4)

    file.close()

def get_all_images(screen_name):
    print("start grabbing tweets...")
    get_all_tweets(screen_name)
    print("..................finish")
    print("start downloading images...")
    urls = extract_images_url()
    download_images(screen_name, urls)
    print("..................finish")
