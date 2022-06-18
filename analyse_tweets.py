import json_stream
import json
import time
import naya
import gzip
from unidecode import unidecode

x = time.time()
tweets = []
dates = ["10-03-2022", "15-03-2022", "18-03-2022", "20-03-2022", "22-03-2022", "25-03-2022", "27-03-2022", "29-03-2022", "09-04-2022", "20-04-2022"]

for date in dates:

    i = 0

    with gzip.open(f"./tweets/tweets_{date}.json.gz", mode="rt") as f:
        data = naya.stream_array(naya.tokenize(f))

        for status in data:
            if i == 20000:
                break
            if "retweeted_status" in status:
                try:
                    tweets.append(status["retweeted_status"]["extended_tweet"]["full_text"])
                except KeyError:
                    tweets.append(status["retweeted_status"]["text"])

            else:
                try:
                    tweets.append(status["extended_tweet"]["full_text"])
                except:
                    tweets.append(status["text"])
            i += 1        

i = 0        

with open("other_tweets.json") as f:
 
    data = naya.stream_array(naya.tokenize(f))
    
    for status in data:
        if i == 250000:
            break
        if i%2.5 == 0:
            if "retweeted_status" in status:
                try:
                    tweets.append(status["retweeted_status"]["extended_tweet"]["full_text"])
                except KeyError:
                    tweets.append(status["retweeted_status"]["text"])

            else:
                try:
                    tweets.append(status["extended_tweet"]["full_text"])
                except:
                    tweets.append(status["text"])
        i += 1

print(len(tweets))
print(time.time() - x)

seen = []
for tweet in tweets:
    if tweet not in seen:
        seen.append(tweet)

with open("text_tweets_200000_t4.json", "x") as g:
    g.write(json.dumps(seen))
