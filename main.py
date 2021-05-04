# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# save this as app.py
from flask import Flask, render_template, request
import tweepy
import re
from textblob import TextBlob

app = Flask(__name__, template_folder='templates')

def Auth():
    api_key = "lrRxfrV5n4AudieQDnl7BsX50"
    api_secret_key = "dPF86YYwFFTunkWL8TrQu3rRo3p13eRIevX3RKkOHkw2XCafCZ"
    access_token = "1389444564054810632-PXJiEIbHJv6eHK22LdL4zHd2A9TtO5"
    access_token_secret = "SGHgDBKQxQv0fxe80RE4GfMb6IrrcW22FeFoBY4NCNCAl"

    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

@app.route('/', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        api = Auth()

        username = request.form['username']
        tweetUser = api.user_timeline(id=username, count=20)

        hasilAnalysis = []
        for tweet in tweetUser:
            tweet_properties = {}
            tweet_properties["tanggal_tweet"] = tweet.created_at
            tweet_properties["pengguna"] = tweet.user.screen_name
            tweet_properties["isi_tweet"] = tweet.text
            clean_tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.text).split())

            analysis = TextBlob(clean_tweet)

            try:
                analysis = analysis.translate(to="en")
            except Exception as e:
                print(e)

            if analysis.sentiment.polarity > 0.0:
                tweet_properties["sentimen"] = "positif"
            elif analysis.sentiment.polarity == 0.0:
                tweet_properties["sentimen"] = "netral"
            else:
                tweet_properties["sentimen"] = "negatif"

            hasilAnalysis.append(tweet_properties)

        tweet_positif = [t for t in hasilAnalysis if t["sentimen"] == "positif"]
        tweet_negatif = [t for t in hasilAnalysis if t["sentimen"] == "negatif"]
        tweet_netral = [t for t in hasilAnalysis if t["sentimen"] == "netral"]

        positif = len(tweet_positif), "{}%".format(100 * len(tweet_positif) / len(hasilAnalysis))
        netral = len(tweet_netral), "{}%".format(100 * len(tweet_netral) / len(hasilAnalysis))
        negatif = len(tweet_negatif), "{}%".format(100 * len(tweet_negatif) / len(hasilAnalysis))
        total_tweet = len(hasilAnalysis)

        return render_template('index.html', username=username, tweet_positif=tweet_positif, tweet_negatif=tweet_negatif,
                               tweet_netral=tweet_netral, positif=positif, netral=netral, negatif=negatif, total_tweet=total_tweet)
    return render_template('form.html')

if __name__ == "__main__":
    app.run()