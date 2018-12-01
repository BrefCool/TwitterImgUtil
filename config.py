"""
This module is to config the basic information for TwitterImgCrawler,
including username, Twitter credential file and Google dev auth file.
"""

import argparse
import configparser
import os
import getpass
from settings import Settings
from database import config_mongodb, config_mysql, add_user_to_mongodb, add_user_to_mysql

ARGS = None
RES_DIR = Settings().RES_DIR
CONFIGURE = Settings().CONFIGURE

def check_args():
    config_operations = []

    if ARGS.db is not None:
        if ARGS.db != 'mysql' and ARGS.db != 'mongodb':
            print("invalid database type: %s, only accept mysql or mongodb" % ARGS.db)
            return config_operations
        else:
            config_operations.append({'op': 'config_database',
                                      'db_type': ARGS.db})

    if ARGS.user is not None:
        user_op = {'op': 'add_user',
                   'need_username': False,
                   'need_password': True,
                   'need_twitter': True,
                   'need_google': True}
        if ARGS.twitter_auth_path is not None:
            user_op['need_twitter'] = False
        if ARGS.google_auth_path is not None:
            user_op['need_google'] = False
        config_operations.append(user_op)

    return config_operations


def config_db(job):
    # check or create resources dir and configure .ini file
    try:
        if not os.path.exists(RES_DIR):
            os.mkdir(RES_DIR)
    except Exception as e:
        print("error creating res dir: %s" % e)
        return -1
    first_time_config = not os.path.exists(os.path.join(RES_DIR, CONFIGURE))
    cfg = configparser.RawConfigParser()
    need_config_db = False
    if first_time_config:
        with open(os.path.join(RES_DIR, CONFIGURE), 'w') as configure_file:
            line_str = '#####################################################\n'\
                       '#  These are settings for TwitterImgCrawler.        #\n'\
                       '#  You should use "python config.py" to generate    #\n' \
                       '#  this file.                                       #\n'\
                       '#####################################################\n'
            configure_file.write(line_str)
            cfg.add_section('DATABASE')
            cfg.set('DATABASE', 'host', '127.0.0.1')
            cfg.set('DATABASE', 'port', '3306')
            cfg.set('DATABASE', 'db_name', 'TIC_db')
            cfg.set('DATABASE', 'user', 'root')
            cfg.set('DATABASE', 'password', 'admin')
            cfg.set('DATABASE', 'db_type', job['db_type'])
            cfg.write(configure_file)
        need_config_db = True
    else:
        cfg.read(os.path.join(RES_DIR, CONFIGURE))

    # ask user whether to change saved database
    if not need_config_db:
        ans = input("Already have database info.Do you want to change database info?[y|n]: ")
        while ans not in ('y', 'n', 'yes', 'no', 'Y', 'N', 'YES', 'NO'):
            ans = input("Do you want to config database info?[y|n]: ")
        if ans in ('y', 'Y', 'YES', 'yes'):
            need_config_db = True

    # config database
    if need_config_db:
        if job['db_type'] == 'mysql':
            return config_mysql(cfg)
        else:
            return config_mongodb(cfg)

    return True, "don't need re-config database"


def sign_up(job):
    # get username & password
    username = ARGS.user
    password = getpass.getpass("Enter your password(for security, the password won't print out): ")

    # get twitter credential file path
    twitter_auth_path = ARGS.twitter_auth_path
    if job['need_twitter']:
        twitter_auth_path = input("Enter the Twitter credential file path: ")
    while not os.path.exists(twitter_auth_path):
        print("path[%s]: no such file or directory " % twitter_auth_path)
        twitter_auth_path = input("Enter the Twitter credential file path: ")

    # get google credential file path
    google_auth_path = ARGS.google_auth_path
    if job['need_google']:
        google_auth_path = input("Enter the Google credential file path: ")
    while not os.path.exists(google_auth_path):
        print("path[%s]: no such file or directory " % google_auth_path)
        google_auth_path = input("Enter the Google credential file path: ")

    try:
        cfg = configparser.RawConfigParser()
        cfg.read(os.path.join(RES_DIR, CONFIGURE))
        db_type = cfg['DATABASE']['db_type']
    except:
        print("get config information fail. please check %s" % os.path.join(RES_DIR, CONFIGURE))
        print("if not exists, you should config database first. use '--db' to config mysql or mongodb database")
        return False, "error adding new user"

    if db_type == 'mysql':
        return add_user_to_mysql({'username': username,
                                  'password': password,
                                  'twitter_auth': twitter_auth_path,
                                  'google_auth': google_auth_path})
    else:
        return add_user_to_mongodb()


OPERATIONS = {'config_database': config_db,
              'add_user': sign_up}


def config():
    # check input args
    config_jobs = check_args()
    if len(config_jobs) == 0:
        print("no configure job need to do. exit!")
        return 0

    ret_code = 0
    #print(config_jobs)
    for job in config_jobs:
        is_success, outputs = OPERATIONS[job['op']](job)
        if not is_success:
            print("Job[%s] Failed! msg: %s" % (job['op'], outputs))
            ret_code |= 1
        else:
            print("Job[%s] Success! msg: %s" % (job['op'], outputs))

    return ret_code


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--db',
        type=str,
        default=None,
        help='database type(mysql or mongodb)'
    )
    parser.add_argument(
        '--twitter_auth_path',
        type=str,
        default=None,
        help='path to twitter dev credential file'
    )
    parser.add_argument(
        '--google_auth_path',
        type=str,
        default=None,
        help='path to google dev credential file'
    )
    parser.add_argument(
        '--user',
        type=str,
        default=None,
        help='user name'
    )
    ARGS, unparsed = parser.parse_known_args()
    config()
