import os
import sys
import getpass
import configparser
from settings import Settings
from database import log_in, get_username, create_task, update_task
from TwitterImgUtil import twitter, GVision, selfFFMPEG

RES_DIR = Settings().RES_DIR
CONFIGURE = Settings().CONFIGURE
CFG = configparser.RawConfigParser()
CFG.read(os.path.join(RES_DIR, CONFIGURE))


def login():
    username = input("Enter the username: ")
    password = getpass.getpass("Enter your password(for security, the password won't print out): ")
    is_success, outputs = log_in(username, password)
    if not is_success:
        print(outputs)
        return False, "login failed"
    return True, outputs


def start_task(userid):
    target = input("Please enter the twitter account id you want to crawl: ")
    nums = input("Please enter how many tweets you want to crawl: ")
    is_success, outputs = create_task(userid, target)
    if not is_success:
        print(outputs)
        return
    taskid = outputs
    print(taskid)
    start_crawl(userid, target, nums, taskid)


def start_crawl(userid, target, nums, taskid):
    is_success, outputs = get_username(userid)
    if not is_success:
        print("get userinfo failed. exit!")
        return False, "crawl failed"
    twitter_auth_file = os.path.join(RES_DIR, str(userid), outputs[3])
    google_auth_file = os.path.join(RES_DIR, str(userid), outputs[4])

    print("authorize Twitter...")
    api = twitter.twitter_OAuth_login(twitter_auth_file)
    print("start grabbing tweets...")
    # Twitter can only return maximum 3000+ tweets
    twitter.download_tweets(api, target, int(nums))
    print("start downloading images...")
    urls = twitter.extract_images_url(file_name=target + '_tweets.json')
    image_count = len(urls)
    twitter.download_images(target, urls)

    images_src = os.path.join('./download_images', target)
    images_dst = os.path.join(images_src, 'add_labels')
    os.mkdir(images_dst)
    image_client = GVision.get_image_client(google_auth_file)
    GVision.draw_labels_on_images(image_client, images_src, images_dst)

    selfFFMPEG.convert_images_to_video(images_dst, images_src)
    image_location = images_src
    video_location = images_src

    # update task info
    is_success, outputs = update_task({'id': taskid,
                                       'image': image_location,
                                       'video': video_location,
                                       'image_count': image_count})
    if not is_success:
        print(outputs)
        return False, "crawl failed"

    return True, "crawl success"


def main(userid):
    welcome = "###################################################################\n"\
              "# This is a simple crawler to get images from twitter account and #\n"\
              "# convert them to several videos with recognized label on it.     #\n"\
              "# author: Yuxuan Su(syx525@bu.edu)                                #\n"\
              "###################################################################\n"
    print(welcome)
    is_success, outputs = get_username(userid)
    if not is_success:
        print("get username failed. exit!")
        sys.exit(-1)
    print("Welcome! %s" % outputs[1])
    while True:
        op = input("Press [C] to start a task, Press [I] to view collective statistics, Press [Q] to quit:")
        if op in ("C", "c"):
            start_task(userid)
        elif op in ("Q", "q"):
            sys.exit(0)
        elif op in ("I", "i"):
            pass


if __name__ == '__main__':
    is_success, outputs = login()
    if not is_success:
        print(outputs)
        sys.exit(-1)
    main(outputs)
