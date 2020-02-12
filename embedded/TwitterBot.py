import tweepy
import twitter_credentials
import random

class TwitterBot(): 
    def __init__(self): 
        auth = tweepy.OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRETS)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        try: 
            self.api = tweepy.API(auth)
        except: 
            print("Cannot connect to Twitter Developper account")

    def send_tweet(self, text, user=None): 
        """ Send tweet on DataBreach account in a formatted way
            Input: Text to be tweeted and username (optional)
            Output: No output but tweet sent to @kubitz19 with random hashtags and a format defined by format_tweet()
        """
        tweet = self.format_tweet(text, user)

        try: 
            self.api.update_status(tweet)
        except: 
            print("Tweet could not be sent")

    def format_tweet(self, text, user = None): 
        """ Formats tweet with a header and three random hashtags
            Input: User (optional) and text to be formated
            Output: formatted tweet
        """
        hashtags = self.get_hastags()
        if user is None: 
            tweet = "DATA BREACH! an IoTea user said: \n {}\n {}".format(text, hashtags)
        else: 
            tweet = "DATA BREACH! {} said: \n {}\n {}".format(user, text, hashtags)

        return tweet

    def get_hastags(self, number=3): 
        """ Returns a number of random hashtags in a string
            Input: number of random hashtags to be returned (optional)
            Output: String with random hashtags
        """
        
        list_of_hashtags = [
            "#DataBreach", "#Privacy", "#WhyDoYouCare","#IoTofShits", "#HeSaidIt", "#IoT", "#DataProtection", 
            "#encryption", "#PrivacyPlease", "#cybersecurity", "#PrivacyForDemocracy", "#SecurityFlaw", 
            "#datasecurity", "#goals"
        ]
        random_indexes = random.sample(range(0,len(list_of_hashtags)), number)
        hashtags = ""

        for idx in range(number):
            hashtags =hashtags + list_of_hashtags[random_indexes[idx]] + " "

        return hashtags




if __name__ == "__main__":
    twitter_bot = TwitterBot()
    print(twitter_bot.send_tweet("Ghaj is a chicken hater", user="Ghaj"))