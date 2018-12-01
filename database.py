import pymysql
import os
import configparser
import uuid
from settings import Settings
from shutil import copyfile
from pymongo import MongoClient

RES_DIR = Settings().RES_DIR
CONFIGURE = Settings().CONFIGURE


def config_mysql(cfg):
    # get host
    msg = "Enter the mysql host ip(default: %s): " % str(cfg['DATABASE']['host'])
    host = input(msg) or str(cfg['DATABASE']['host'])
    cfg.set('DATABASE', 'host', host)

    # get port
    msg = "Enter the mysql port(default: %s): " % str(cfg['DATABASE']['port'])
    port = input(msg) or str(cfg['DATABASE']['port'])
    cfg.set('DATABASE', 'port', port)

    # get db name
    msg = "Enter the mysql db's name(default: %s): " % str(cfg['DATABASE']['db_name'])
    db_name = input(msg) or str(cfg['DATABASE']['db_name'])
    cfg.set('DATABASE', 'db_name', db_name)

    # get db user
    msg = "Enter the mysql db's username(default: %s): " % str(cfg['DATABASE']['user'])
    user = input(msg) or str(cfg['DATABASE']['user'])
    cfg.set('DATABASE', 'user', user)

    # get db pwd
    msg = "Enter the mysql db's password(default: %s): " % str(cfg['DATABASE']['password'])
    pwd = input(msg) or str(cfg['DATABASE']['password'])
    cfg.set('DATABASE', 'password', pwd)

    with open(os.path.join(RES_DIR, CONFIGURE), 'w') as configure_file:
        cfg.write(configure_file)

    # try connection
    print("try connection....")
    try:
        pymysql.connect(host=host,
                        user=user,
                        password=pwd,
                        db=db_name)
    except Exception as e:
        print("connect failed. Please check if your configure info is correct: %s" % e)
        return False, "config mysql failed"

    print("connect success")
    return True, "config mysql success"


def config_mongodb(cfg):
    print("start config mongodb")
    # get host
    msg = "Enter the mongodb host ip(default: %s): " % str(cfg['DATABASE']['host'])
    host = input(msg) or str(cfg['DATABASE']['host'])
    cfg.set('DATABASE', 'host', host)

    # get port
    msg = "Enter the mongodb port(default: %s): " % str(cfg['DATABASE']['port'])
    port = input(msg) or str(cfg['DATABASE']['port'])
    cfg.set('DATABASE', 'port', port)

    # get db name
    msg = "Enter the mongodb db's name(default: %s): " % str(cfg['DATABASE']['db_name'])
    db_name = input(msg) or str(cfg['DATABASE']['db_name'])
    cfg.set('DATABASE', 'db_name', db_name)

    # # get db user
    # msg = "Enter the mysql db's username(default: %s): " % str(cfg['DATABASE']['user'])
    # user = input(msg) or str(cfg['DATABASE']['user'])
    # cfg.set('DATABASE', 'user', user)
    #
    # # get db pwd
    # msg = "Enter the mysql db's password(default: %s): " % str(cfg['DATABASE']['password'])
    # pwd = input(msg) or str(cfg['DATABASE']['password'])
    # cfg.set('DATABASE', 'password', pwd)

    with open(os.path.join(RES_DIR, CONFIGURE), 'w') as configure_file:
        cfg.write(configure_file)

    return True, "config mongodb success"


def add_user_to_mysql(data):
    cfg = configparser.RawConfigParser()
    cfg.read(os.path.join(RES_DIR, CONFIGURE))

    host = cfg['DATABASE']['host']
    port = cfg['DATABASE']['port']
    db_name = cfg['DATABASE']['db_name']
    user = cfg['DATABASE']['user']
    pwd = cfg['DATABASE']['password']

    username = data['username']
    password = data['password']
    twitter_auth = data['twitter_auth']
    google_auth = data['google_auth']

    try:
        connect = pymysql.connect(host=host,
                                  port=int(port),
                                  user=user,
                                  password=pwd,
                                  db=db_name)
    except Exception as e:
        print("connect failed. Please check if your configure info is correct: %s" % e)
        return False, "add user failed"

    try:
        with connect.cursor() as cursor:
            sql = "insert into `users` (`username`, `password`, `twitter_auth`, `google_auth`) "\
                  "values (%s, %s, %s, %s)"
            cursor.execute(sql, (username, password, twitter_auth, google_auth))

        connect.commit()

        with connect.cursor() as cursor:
            sql = "select `id` from `users` where `username`=%s"
            cursor.execute(sql, (username,))
            result = cursor.fetchone()
            userid = result[0]

            if not os.path.exists(os.path.join(RES_DIR, str(userid))):
                os.mkdir(os.path.join(RES_DIR, str(userid)))
                copyfile(twitter_auth, os.path.join(RES_DIR, str(userid), twitter_auth))
                copyfile(google_auth, os.path.join(RES_DIR, str(userid), google_auth))
    except Exception as e:
        print("add user failed. err msg: %s" % e)
        connect.close()
        return False, "add user failed"

    connect.close()
    return True, "add user Success"


def add_user_to_mongodb(data):
    cfg = configparser.RawConfigParser()
    cfg.read(os.path.join(RES_DIR, CONFIGURE))

    host = cfg['DATABASE']['host']
    port = cfg['DATABASE']['port']
    db_name = cfg['DATABASE']['db_name']

    username = data['username']
    password = data['password']
    twitter_auth = data['twitter_auth']
    google_auth = data['google_auth']

    user = {'username': username,
            'password': password,
            'twitter_auth': twitter_auth,
            'google_auth': google_auth}

    client = MongoClient(host, int(port))
    db = client[db_name]

    try:
        userid = db.users.insert_one(user).inserted_id
        if not os.path.exists(os.path.join(RES_DIR, str(userid))):
            os.mkdir(os.path.join(RES_DIR, str(userid)))
            copyfile(twitter_auth, os.path.join(RES_DIR, str(userid), twitter_auth))
            copyfile(google_auth, os.path.join(RES_DIR, str(userid), google_auth))
    except Exception as e:
        print("add user failed. Please check if your configure info is correct: %s" % e)
        return False, "add user failed"

    return True, "add user Success"


def log_in(username, password):
    cfg = configparser.RawConfigParser()
    cfg.read(os.path.join(RES_DIR, CONFIGURE))
    if cfg['DATABASE']['db_type'] == 'mysql':
        return login_mysql(username, password)
    else:
        return login_mongodb(username, password)


def login_mongodb(username, password):
    cfg = configparser.RawConfigParser()
    cfg.read(os.path.join(RES_DIR, CONFIGURE))

    host = cfg['DATABASE']['host']
    port = cfg['DATABASE']['port']
    db_name = cfg['DATABASE']['db_name']

    client = MongoClient(host, int(port))
    db = client[db_name]
    result = db.users.find_one({'username': username, 'password': password})

    if result is None:
        return False, "username or password wrong"

    return True, result['_id']


def login_mysql(username, password):
    cfg = configparser.RawConfigParser()
    cfg.read(os.path.join(RES_DIR, CONFIGURE))

    host = cfg['DATABASE']['host']
    port = cfg['DATABASE']['port']
    db_name = cfg['DATABASE']['db_name']
    user = cfg['DATABASE']['user']
    pwd = cfg['DATABASE']['password']

    try:
        connect = pymysql.connect(host=host,
                                  port=int(port),
                                  user=user,
                                  password=pwd,
                                  db=db_name)
    except Exception as e:
        print("connect failed. Please check if your configure info is correct: %s" % e)
        return False, "add user failed"

    try:
        with connect.cursor() as cursor:
            sql = "select `id` from users where `username`=%s and `password`=%s"
            cursor.execute(sql, (username, password))
            result = cursor.fetchone()
            if result is None:
                return False, "username or password wrong"
            userid = result[0]
    except Exception as e:
        print("login failed. err msg: %s" % e)
        connect.close()
        return False, "login failed"

    connect.close()
    return True, userid

def get_username(userid):
    cfg = configparser.RawConfigParser()
    cfg.read(os.path.join(RES_DIR, CONFIGURE))
    if cfg['DATABASE']['db_type'] == 'mysql':
        return get_username_mysql(userid)
    else:
        return get_username_mongodb(userid)


def get_username_mysql(userid):
    cfg = configparser.RawConfigParser()
    cfg.read(os.path.join(RES_DIR, CONFIGURE))

    host = cfg['DATABASE']['host']
    port = cfg['DATABASE']['port']
    db_name = cfg['DATABASE']['db_name']
    user = cfg['DATABASE']['user']
    pwd = cfg['DATABASE']['password']

    try:
        connect = pymysql.connect(host=host,
                                  port=int(port),
                                  user=user,
                                  password=pwd,
                                  db=db_name)
    except Exception as e:
        print("connect failed. Please check if your configure info is correct: %s" % e)
        return False, "get username failed"

    try:
        with connect.cursor() as cursor:
            sql = "select * from users where `id`=%s"
            cursor.execute(sql, (userid,))
            result = cursor.fetchone()
            if result is None:
                return False, "invalid id"
    except Exception as e:
        print("login failed. err msg: %s" % e)
        connect.close()
        return False, "login failed"

    connect.close()
    return True, result


def get_username_mongodb(userid):
    cfg = configparser.RawConfigParser()
    cfg.read(os.path.join(RES_DIR, CONFIGURE))

    host = cfg['DATABASE']['host']
    port = cfg['DATABASE']['port']
    db_name = cfg['DATABASE']['db_name']

    client = MongoClient(host, int(port))
    db = client[db_name]
    result = db.users.find_one({'_id': userid})

    if result is None:
        return False, "get username failed"

    return True, (result['_id'], result['username'], result['password'], result['twitter_auth'], result['google_auth'])


def create_task(userid, target):
    cfg = configparser.RawConfigParser()
    cfg.read(os.path.join(RES_DIR, CONFIGURE))
    if cfg['DATABASE']['db_type'] == 'mysql':
        return create_task_mysql(userid, target)
    else:
        return create_task_mongodb(userid, target)


def create_task_mysql(userid, target):
    cfg = configparser.RawConfigParser()
    cfg.read(os.path.join(RES_DIR, CONFIGURE))

    host = cfg['DATABASE']['host']
    port = cfg['DATABASE']['port']
    db_name = cfg['DATABASE']['db_name']
    user = cfg['DATABASE']['user']
    pwd = cfg['DATABASE']['password']
    taskid = str(uuid.uuid1())

    try:
        connect = pymysql.connect(host=host,
                                  port=int(port),
                                  user=user,
                                  password=pwd,
                                  db=db_name)
    except Exception as e:
        print("connect failed. Please check if your configure info is correct: %s" % e)
        return False, "add task failed"

    try:
        with connect.cursor() as cursor:
            sql = "insert into `tasks` (`id`, `owener`, `twitter_id`, `state`) "\
                  "values (%s, %s, %s, %s)"
            cursor.execute(sql, (taskid, userid, target, 'initialize'))

        connect.commit()

    except Exception as e:
        print("add task failed. err msg: %s" % e)
        connect.close()
        return False, "add task failed"

    connect.close()
    return True, taskid


def create_task_mongodb(userid, target):
    cfg = configparser.RawConfigParser()
    cfg.read(os.path.join(RES_DIR, CONFIGURE))

    host = cfg['DATABASE']['host']
    port = cfg['DATABASE']['port']
    db_name = cfg['DATABASE']['db_name']

    client = MongoClient(host, int(port))
    db = client[db_name]

    task = {'image_count': 0,
            'owener': userid,
            'image_location': '',
            'state': 'initialize',
            'video_location': '',
            'twitter_id': target}

    try:
        taskid = db.tasks.insert_one(task).inserted_id
    except Exception as e:
        print("create task failed. %s" % e)
        return False, "create task failed"

    return True, taskid


def update_task(data):
    cfg = configparser.RawConfigParser()
    cfg.read(os.path.join(RES_DIR, CONFIGURE))
    if cfg['DATABASE']['db_type'] == 'mysql':
        return update_task_mysql(data)
    else:
        return update_task_mongodb(data)


def update_task_mysql(data):
    cfg = configparser.RawConfigParser()
    cfg.read(os.path.join(RES_DIR, CONFIGURE))

    host = cfg['DATABASE']['host']
    port = cfg['DATABASE']['port']
    db_name = cfg['DATABASE']['db_name']
    user = cfg['DATABASE']['user']
    pwd = cfg['DATABASE']['password']

    taskid = data['id']
    image_location = data['image']
    video_location = data['video']
    image_count = data['image_count']

    try:
        connect = pymysql.connect(host=host,
                                  port=int(port),
                                  user=user,
                                  password=pwd,
                                  db=db_name)
    except Exception as e:
        print("connect failed. Please check if your configure info is correct: %s" % e)
        return False, "update task failed"

    try:
        with connect.cursor() as cursor:
            sql = "update `tasks` set `image_location`=%s, `video_location`=%s, `image_count`=%s, `state`=%s "\
                  "where `id`=%s"
            cursor.execute(sql, (image_location, video_location, str(image_count), 'finish', taskid))

        connect.commit()

    except Exception as e:
        print("update task failed. err msg: %s" % e)
        connect.close()
        return False, "update task failed"

    connect.close()
    return True, taskid


def update_task_mongodb(data):
    cfg = configparser.RawConfigParser()
    cfg.read(os.path.join(RES_DIR, CONFIGURE))

    host = cfg['DATABASE']['host']
    port = cfg['DATABASE']['port']
    db_name = cfg['DATABASE']['db_name']

    taskid = data['id']
    image_location = data['image']
    video_location = data['video']
    image_count = data['image_count']

    client = MongoClient(host, int(port))
    db = client[db_name]

    result = db.tasks.find_one({'_id': taskid})
    if result is None:
        print('invalid task ')
        return False, "update task failed"
    try:
        db.tasks.update_one({'_id': result['_id']}, {'$set': {'image_location': image_location,
                                                              'video_location': video_location,
                                                              'image_count': image_count}})
    except Exception as e:
        print("update task failed. %s" % e)
        return False, "update task failed"

    return True, taskid