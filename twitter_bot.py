import tweepy
import time
from crypto_scraping import *
from accesskeys import *

client = tweepy.Client(bearer_token=BEARER_TOKEN, consumer_key=API_KEY,
                       consumer_secret=API_KEY_SECRET,
                       access_token=ACCESS_TOKEN,
                       access_token_secret=ACCESS_TOKEN_SECRET)

file_name = 'mentionid.txt'

# Stores the mention id that has already been replied to within a file
def store_mention(mention):
    f_write = open(file_name, 'a')
    f_write.write(str(mention) + '\n')
    f_write.close()
    return

#Checks file to ensure that the mention tweet has not been replied to already
def check_file(mention):
    if str(mention) in open(file_name).read():
        return True
    else:
        return False

#checks if mention tweet has already been replied to, if not, then it replies to tweet
#and stores it in file
def reply_to_tweet():
    mentions = client.get_users_mentions(id=USER_ID)
    for mention in mentions.data:
        if check_file(str(mention.id)) is False:
            print(mention.text)
            store_mention(str(mention.id))
            conversion_text = convert_crypto(mention.text)
            response = client.create_tweet(text=conversion_text, in_reply_to_tweet_id=mention.id)

while True:
    reply_to_tweet()
    time.sleep(10)