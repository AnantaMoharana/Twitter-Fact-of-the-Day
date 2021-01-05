
import tweepy
import requests
from bs4 import BeautifulSoup
from datetime import date
import time
import schedule
from datetime import datetime, timedelta, timezone
from urllib.request import Request, urlopen

#keys that will be used in authentication, they are balnk here in thus publication in compliance to twitter policy
CONSUMER_KEY=''
CONSUMER_SECRET=''
ACCESS_KEY=''
ACCESS_SECRET=''


class Fact_of_the_day:
    def __init__(self):

        #Authenticate to Twitter
        auth=tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)

        self.api = tweepy.API(auth)
        self.str_to_time = lambda x: datetime.strptime(x, '%a %b %d %H:%M:%S %z %Y')
        self.selection_function = lambda x: int(x['favorite_count']) + int(x['retweet_count'])
        self.last_tweet_time = datetime.now(timezone.utc) - timedelta(minutes=1440)

        #run this bot once and then run it one every 1440 minutes/24 hours/ every day
        self.run_bot()
        schedule.every(1440).minutes.do(self.run_bot)

    def run_bot(self):

        try: 
            #get the site url
            site= "https://www.beagreatteacher.com/daily-fun-fact/"
            hdr = {'User-Agent': 'Mozilla/5.0'}
            #extract the html script from the site
            req = Request(site,headers=hdr)
            page = urlopen(req)
            soup = BeautifulSoup(page)
            #get all tags containing h2 and p
            categories=soup.find_all('h2')
            substances=soup.find_all("p")
            #remove the text from the tags. The tages and thier content in stored in a list so after examining it the desire test was found in categories[2] and substances[3]
            Random=categories[2].get_text()
            Fact=substances[3].get_text()


            #join the compenents together to create out tweet
            fact_of_day=Random+"\n"+Fact 

            #tweet the fact to our twitter account
            self.api.update_status(fact_of_day)
        except Exception as e:
            #incease of error print the error
            print(e)



if __name__ == "__main__":

    bot=Fact_of_the_day()

    while True:
        schedule.run_pending()



















































