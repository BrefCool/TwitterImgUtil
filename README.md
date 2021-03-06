# TwitterImgCrawler (mini-project03: database)
This is a python program which can be used to crawl images from twitter account and convert those images to videos with recognized labels.
To use this program, you should install MySQL or mongoDB on your computer.  
Also, the package pymysql and pymongo is required.  
```
pip install pymysql
pip install pymongo
```
To use this program, you should config the database info and create a user first.
1. Use config.py to config database
```
python config.py --db mysql
```
or
```
python config.py --db mongodb
```
follow the instruction to config mysql or mongodb  
2. Use config.py to sign up a new user
```
python config.py --user bref --twitter_auth twitter_dev.ini --google_auth TwitterImgUtil_credential.json
```
you should prepare the twitter and google credential files.  
the parameter behind --user is the username.  
the parameter behind --twitter_auth is the twitter account's credential file  
the parameter behind --google_auth is the google credential file  
It will ask you to create a new password for your new user.  


After Configuration, you can run crawler:  
```
python crawler.py
```
use the username and password you created before to login.
![Alt text](images_for_readme/crawler.PNG?raw=true "Title")  
you can press c to create a crawling task:  
![Alt text](images_for_readme/task.PNG?raw=true "Title")
It will download iamges and convert them to videos.   

# TwitterImgUtil
It's a package that combined Twitter API, FFMPEG and Google Vision API. It provides some function like downloading images\tweets from twitter users, converting those images to several videos and recognising objects on the images.
## How do I install it?
I have published it to the [pypi.org](https://pypi.org/project/TwitterImgUtil/#description). So user can simply use pip to install the package. Python 3 environment is recommanded.
```
pip install TwitterImgUtil
```
Or, you can just use git clone and run pip install . on the local path.
In order to get used of the selfFFMPEG module of the package, you should make sure that your computer have installed FFMPEG and add the ffmpeg.exe to your environment path.
You can download the FFMPEG from this website: https://www.ffmpeg.org/
## The Twitter Module
The Twitter Module provides functions to download tweets from users. You have to prepare a file(like twitter_dev.ini) that includes your consumer_key, consumer_secret, access_key and access_secret. The format is
```
consumer_key=oacishviodsahvoaijvioadsaiosnv
consumer_secret=vhiaohvdsaiovhasiobvnas
access_key=nhvaiovhnaiovnaso
access_secret=vbnaovnaiovnasovahnviodabnioveh
```
Then, if you want to download all the images(Twitter only returns maximum 3250 tweets) from one user: @muse：
```
from TwitterImgUtil import twitter
twitter.get_images_from_feed('@muse', 'twitter_dev.ini')
```
All the images will be saved to './download_images/@muse' file dir.
Also, the Twitter Module also provides function to download tweets:
```
from TwitterImgUtil import twitter
api = twitter.twitter_OAuth_login('twitter_dev.ini')
twitter.download_tweets(api, '@muse', 200)
```
It will download 200 tweets from user @muse
## The FFMPEG Module
The FFMPEG Module provides functions convert images to videos. It takes maximum 100 images to 1 videos. So if there are more than 100 images, the FFMPEG Module will generate more than 1 videos.
the first parameter of the convert_images_to_video function is the dir where images are saved. The second parameter represents where the generated video should be saved.
```
from TwitterImgUtil import selfFFMPEG
selfFFMPEG.convert_images_to_video('./download_images/@muse', './download_images/@muse')
```
## The Google Vision Module
The Google Vision Module provides functions to explain objects on the image. Also, it helps us print the labels on the images.
You should have a Google cloud service account and the related credential json file.
```
from TwitterImgUtil import GVision
image_client = GVision.get_image_client('TwitterImgUtil_credential.json')
GVision.draw_labels_on_images(image_client, './download_images/@muse', './download_images/@muse/add_labels')
```
the draw_labels_on_images function will save all the images with labels to the ./download_imags/@muse/add_labels
