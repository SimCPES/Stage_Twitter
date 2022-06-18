#!/bin/bash



DATE=$(date --date='1 day ago' +%d-%m-%Y);
HOUR=$(date +%T);



truncate -s -2 ./tweets/tweets_$DATE.json
echo ] >> ./tweets/tweets_$DATE.json
gzip -v ./tweets/tweets_$DATE.json





