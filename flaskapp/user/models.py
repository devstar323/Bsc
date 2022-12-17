from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from flaskapp import db
import uuid
import pandas as pd
import tweepy
import json
import csv

class User:

  def start_session(self, user):
    del user['password']
    session['logged_in'] = True
    session['user'] = user
    return jsonify(user), 200

  def signup(self):
    print(request.form)

    # Create the user object
    user = {
      "_id": uuid.uuid4().hex,
      "name": request.form.get('name'),
      "email": request.form.get('email'),
      "password": request.form.get('password')
    }
    

    # Encrypt the password
    user['password'] = pbkdf2_sha256.encrypt(user['password'])

    # Check for existing email address
    if db.users.find_one({ "email": user['email'] }):
      return jsonify({ "error": "Email address already in use" }), 400

    if db.users.insert_one(user):
      return self.start_session(user)

    return jsonify({ "error": "Signup failed" }), 400
  
  def signout(self):
    session.clear()
    return redirect('/')
  
  def login(self):

    user = db.users.find_one({
      "email": request.form.get('email')
    })

    if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
      return self.start_session(user)
    
    return jsonify({ "error": "Invalid login credentials" }), 401

def twitter_scrapping(self):
    def printtweetdata(n, ith_tweet):
            print()
            print(f"Tweet {n}:")
            print(f"Username:{ith_tweet[0]}")
            print(f"Description:{ith_tweet[1]}")
            print(f"Location:{ith_tweet[2]}")
            print(f"Following Count:{ith_tweet[3]}")
            print(f"Follower Count:{ith_tweet[4]}")
            print(f"Total Tweets:{ith_tweet[5]}")
            print(f"Retweet Count:{ith_tweet[6]}")
            print(f"Tweet Text:{ith_tweet[7]}")
            print(f"Hashtags Used:{ith_tweet[8]}")


    # function to perform data extraction
    def scrape(words, date_since, numtweet):

            # Creating DataFrame using pandas
            db = pd.DataFrame(columns=['username',
                                    'description',
                                    'location',
                                    'following',
                                    'followers',
                                    'totaltweets',
                                    'retweetcount',
                                    'text',
                                    'hashtags'])

            # We are using .Cursor() to search
            # through twitter for the required tweets.
            # The number of tweets can be
            # restricted using .items(number of tweets)
            tweets = tweepy.Cursor(api.search_tweets,
                                words, lang="en",
                                since_id=date_since,
                                tweet_mode='extended').items(numtweet)


            # .Cursor() returns an iterable object. Each item in
            # the iterator has various attributes
            # that you can access to
            # get information about each tweet
            list_tweets = [tweet for tweet in tweets]

            # Counter to maintain Tweet Count
            i = 1

            # we will iterate over each tweet in the
            # list for extracting information about each tweet
            for tweet in list_tweets:
                    username = tweet.user.screen_name
                    description = tweet.user.description
                    location = tweet.user.location
                    following = tweet.user.friends_count
                    followers = tweet.user.followers_count
                    totaltweets = tweet.user.statuses_count
                    retweetcount = tweet.retweet_count
                    hashtags = tweet.entities['hashtags']

                    # Retweets can be distinguished by
                    # a retweeted_status attribute,
                    # in case it is an invalid reference,
                    # except block will be executed
                    try:
                            text = tweet.retweeted_status.full_text
                    except AttributeError:
                            text = tweet.full_text
                    hashtext = list()
                    for j in range(0, len(hashtags)):
                            hashtext.append(hashtags[j]['text'])

                    # Here we are appending all the
                    # extracted information in the DataFrame
                    ith_tweet = [username, description,
                                location, following,
                                followers, totaltweets,
                                retweetcount, text, hashtext]
                    db.loc[len(db)] = ith_tweet

                    # Function call to print tweet data on screen
                    printtweetdata(i, ith_tweet)
                    i = i+1
            filename = 'scraped_tweets.csv'

            # we will save our database as a CSV file.
            db.to_csv(filename)

    if __name__ == '__main__':

            # Enter your own credentials obtained
            # from your developer account
            consumer_key = "k9yAXXOh2oUoaJ8GWLq6QYzK7"
            consumer_secret = "7ThFqTMo5trPGGqsnJxz9MPvDtlchzoJmwGD84J6lrA2dHNl3A"
            access_key = "468641184-JBkHmVXvdsMe18BkiOPd9RQlRcYwLIqHvNceCQVx"
            access_secret = "6GQHBti29cFPFNywD7RzIVEhDQbFEpgWDaPVeZKwefLkJ"




            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_key, access_secret)
            api = tweepy.API(auth)

            # Enter Hashtag and initial date
            print("Enter Twitter HashTag to search for")
            words = input()
            print("Enter Date since The Tweets are required in yyyy-mm--dd")
            date_since = input()

            # number of tweets you want to extract in one run
            numtweet = 50
            scrape(words, date_since, numtweet)
            print('Scraping has completed!')






            public_tweets = api.home_timeline()
            tweets = api.user_timeline(screen_name="ahmednasserr__") # law 3ayez ageb tweets beta3t el user da bas
            print(public_tweets)
    columns = ['Time', 'User', 'Tweet']

    # Initialize a list
    data = []

    # Initialize a counter for the serial number
    i= 1
    for tweet in public_tweets:
        data.append([tweet.created_at, tweet.user.screen_name, tweet.text])
        print(f"{i}. User: {tweet.user.screen_name}\n Tweet: {tweet.text}")
        i +=1

    df = pd.DataFrame(data, columns=columns)
    #print(df)

    df.to_csv('public_tweets.csv')












     
      


