import requests_oauthlib
import webbrowser
import json

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)
    
# Get these from the Twitter website, by going to
# https://apps.twitter.com/ and creating an "app"
# Don't fill in a callback_url and put in a placeholder for the website
# Visit the Keys and Access Tokens tab for your app and grab the following two values

client_key = "" # what Twitter calls Consumer Key
client_secret = "" # What Twitter calls Consumer Secret

if not client_secret or not client_key:
    print "You need to fill in client_key and client_secret. See comments in the code around line 8-14"
    exit()



def get_tokens():
    ## Step 1. Obtain a request token which will identify you (the client) in the next step. 
    # At this stage you will only need your client key and secret

    # OAuth1Session is a class defined in the requests_oauthlib module
    # Two values are passed to the __init__ method of OAuth1Session
    # -- the key is passed as the value of the first parameter (whose name we don't know)
    # -- the secret is passed as the value of the parameter that is also called client_secret
    # after this line executes, oauth will now be an instance of the class OAuth1Session
    oauth = requests_oauthlib.OAuth1Session(client_key, client_secret=client_secret)

    request_token_url = 'https://api.twitter.com/oauth/request_token'

    # invoke the fetch_request_token method of the class OAuth1Session on our instance
    # it returns a dictionary that might look like this:
    # {
    #     "oauth_token": "Z6eEdO8MOmk394WozF5oKyuAv855l4Mlqo7hhlSLik",
    #     "oauth_token_secret": "Kd75W4OQfb2oJTV0vzGzeXftVAwgMnEK9MumzYcM"
    # }
    # It also saves the oauth_token as an instance variable of the object
    # oauth is bound to, so it can be used in later steps
    fetch_response = oauth.fetch_request_token(request_token_url)

    # pull the two values out of the dictionary and store them in a variable for later use
    # note that d.get('somekey') is another way of writing d['somekey']
    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')

    ## Step 2. Obtain authorization from the user (resource owner) to access their protected resources (images, tweets, etc.). This is commonly done by redirecting the user to a specific url to which you add the request token as a query parameter. Note that not all services will give you a verifier even if they should. Also the oauth_token given here will be the same as the one in the previous step.

    base_authorization_url = 'https://api.twitter.com/oauth/authorize'
    # append the query parameters need to make it a full url.
    # they will include the resource_owner_key from the previus step,
    # which was stored in the oauth object above as an instance variable
    # when fetch_request_token was invoked
    authorization_url = oauth.authorization_url(base_authorization_url)

    webbrowser.open(authorization_url) # opens a window in your web browser
    # Once you log in, and give permissions, you should see a string of characters that you need to copy.

    # After the user authenticates at Twitter, it would normally "redirect"
    # the browser back to our website. But we aren't running a website.
    # Some services, like Twitter, will let you configure the app to 
    # display a verifier, or the entire redirect url, rather than actually
    # redirecting to it.
    # User will have to cut and paste the verifier or the whole redirect url

    # version where the website provides a verifier
    verifier = raw_input('Please input the verifier>>> ') 

    # version where the website provides the entire redirect url
    # redirect_response = raw_input('Paste the full redirect URL here: ')
    # oauth_response = oauth.parse_authorization_response(redirect_response)
    # get back something like this
    #{
    #    "oauth_token": "Z6eEdO8MOmk394WozF5oKyuAv855l4Mlqo7hhlSLik",
    #    "oauth_verifier": "sdflk3450FASDLJasd2349dfs"
    #}
    # verifier = oauth_response.get('oauth_verifier')

    ## Step 3. Obtain an access token from the OAuth provider. Save this token so it can be re-used later. 
    # In this step we re-use most of the credentials obtained up to this point.

    # make a new instance of the OAuth1Session class, with several more parameters filled in
    oauth = requests_oauthlib.OAuth1Session(client_key,
                              client_secret=client_secret,
                              resource_owner_key=resource_owner_key,
                              resource_owner_secret=resource_owner_secret,
                              verifier=verifier)
                              
    access_token_url = 'https://api.twitter.com/oauth/access_token'
    oauth_tokens = oauth.fetch_access_token(access_token_url)
    # You get back something like this
    #{
    #    "oauth_token": "6253282-eWudHldSbIaelX7swmsiHImEL4KinwaGloHANdrY",
    #    "oauth_token_secret": "2EEfA6BG3ly3sR3RjE0IBSnlQu4ZrUzPiYKmrkVU"
    #}
    resource_owner_key = oauth_tokens.get('oauth_token')
    resource_owner_secret = oauth_tokens.get('oauth_token_secret')
    
    return (client_key, client_secret, resource_owner_key, resource_owner_secret, verifier)

try:
    # This code tries to see if you can read the credentials from the file
    # (If you have credentials for the wrong user, or expired credentials
    # just delete the file creds.txt and run this code again)
    f = open("creds.txt", 'r')
    (client_key, client_secret, resource_owner_key, resource_owner_secret, verifier) = json.loads(f.read())
    f.close()
except:
    # If not, you'll have to get them!
    # and then, save them in a file called creds.txt
    tokens = get_tokens()
    f = open("creds.txt", 'w')
    f.write(json.dumps(tokens))
    f.close()
    (client_key, client_secret, resource_owner_key, resource_owner_secret, verifier) = tokens
  
## Step 4. Access protected resources. 

# For Twitter API endpoints that might be interesting to try, see docs at
# https://dev.twitter.com/rest/tools/console and
# https://dev.twitter.com/rest/public

# Create an instance of OAuth1Session in a variable that you can use to make a request
oauth = requests_oauthlib.OAuth1Session(client_key,
                        client_secret=client_secret,
                        resource_owner_key=resource_owner_key,
                        resource_owner_secret=resource_owner_secret)

# Call the get method. The work of encoding the client_secret 
# and "signing" the request is taken care of behind the scenes.
# The results are also processed for you, including calling .read() and 
# encoding as json.

# The above you need to keep around to use. The rest is up to you -- what requests you want to make, what you do with the data you get back, etc!


## Commented out this request, you can uncomment to see the results of this request
# protected_url = 'https://api.twitter.com/1.1/account/settings.json' # path that points to authenticated user's account settings data
# r = oauth.get(protected_url)
# r is now an instance of the Response class in the requests module
# documentation at 
# http://docs.python-requests.org/en/latest/user/quickstart/#response-content

## Of particular interest to us is the json() method of the Response class
## Same as getting .text attribute, then json.loads() on the value of the .text attribute, as you've seen before!

#print pretty(r.json())

# Make a request to the Tweet search endpoint, searching for the phrase 'University of Michigan', looking to get 3 Tweets back
r = oauth.get("https://api.twitter.com/1.1/search/tweets.json", params = {'q': 'University of Michigan', 'count' : 3})



# investigate the data
print type(r.json())
# print json.dumps(r.json(), indent=2) # another way to print it pretty
res = r.json() # get a Python object in a variable, you now know it's a dictionary
print res.keys() # print the dictionary's keys
print pretty(res) # print the pretty version for people to look at

# cache the data we got back from the request
f = open('nested.txt', 'w')
f.write(json.dumps(res))
f.close()

# do some investigation with the cached data
fileref = open("nested.txt","r")
file_str = fileref.read()
twitter_data = json.loads(file_str)
print type(twitter_data) # dictionary!

# remember the pattern for investigating nested data
print twitter_data.keys() # [u'search_metadata', u'statuses']
# one of those looks interesting
print type(twitter_data["statuses"]) # print the type of that key's value
print twitter_data["statuses"][0] # it's a list, so print the first element
print type(twitter_data["statuses"][0]) # print the type of the first element
print twitter_data["statuses"][0].keys() # that's a dictionary, so print its keys
# --> [u'contributors', u'truncated', u'text', u'is_quote_status', u'in_reply_to_status_id', u'id', u'favorite_count', u'source', u'retweeted', u'coordinates', u'entities', u'in_reply_to_screen_name', u'id_str', u'retweet_count', u'in_reply_to_user_id', u'favorited', u'retweeted_status', u'user', u'geo', u'in_reply_to_user_id_str', u'possibly_sensitive', u'lang', u'created_at', u'in_reply_to_status_id_str', u'place', u'metadata']

# hmm, let's look at the values associated with some of those keys in each dictionary
# maybe each dictionary in that list twitter_data["statuses"] represents one tweet!
print twitter_data["statuses"][0]["text"] # looks like the text of one tweet!
# so we were probably right! hooray!
print twitter_data["statuses"][0]["retweet_count"] # looks like a number of RTs for this tweet!
# etc.



####PAGING
# Getting multiple pages of results can be tricky. See Twitter's explanation at
# https://dev.twitter.com/rest/public/timelines
# (Other sites handle paging slightly differently; you'll have to read the documentation.)

# Let's get my (or your) last 25 tweets, 5 at a time.
# Twitter actually lets you get more than 25 at a time, but not more than 200, so this is practice for when you want to get more than 200. You could get the last 1000, 200 at a time, using the same pattern.

# To pass parameters using the requests_oauthlib module, we use the same 
# get() method used in the requests module.
# see documentation at 
# http://docs.python-requests.org/en/latest/user/quickstart/#passing-parameters-in-urls


collected_tweets = [] # where I'll collect all the tweet data I get as I page through my results, 5 at a time
ids = []
max_id = None
my_params = {'count' : 5} # query parameters for 1st request

for i in range(5):
    if len(ids) > 0: # if we have already started the paging process 
        my_params['max_id'] = min(ids) - 1
        # Twitter suggests that you take the minimum of the ids you got before, then subtract one from it, to make sure you get only ones you haven't received before. We can use the built-in min function here (could also accumulate by hand).
    # Regardless, now we need to make a request to the logged in user's timeline with the query parameters
    r = oauth.get("https://api.twitter.com/1.1/statuses/user_timeline.json",params = my_params)  # passes {'count': 5, 'max_id': whatever} ...
    # Now, append this data to a list so we can collect all the paged results
    collected_tweets.append(r.json())
    next_five_ids = [tweet['id'] for tweet in r.json()]  # get the ids from the tweets we just got         
    ids = ids + next_five_ids # add them to the list, and start the for loop process over again

print ids
# print pretty(collected_tweets)

# cache the data we got back and collected
fr = open("paging_nested.txt","w")
fr.write(json.dumps(collected_tweets))
fr.close()

# Now, can investigate using this data that got cached.
# If you're testing with the data in the file only, you may want to comment out all the code above this for a while so you don't inadvertently make a lot of requests to Twitter and then run out of request privileges for the day!


## To start work on a complex program using Twitter data:
twitter_data_file1 = "paging_nested.txt"
try:
    fp = open(twitter_data_file1,"r") # I know that paging_nested.txt is where I am saving cached data for this program / the file where my twitter data is b/c it's saved in a global var in my program
    collected_tweets = json.loads(fp.read()) # try to read the file and load it into json and save it in the twitter_stuff variable
except Exception, e: # If I run into an error opening it or loading it into JSON, I probably don't have it/it's not good data/I messed it up, so let's do the except block stuff
    # print e # in case I want to print out info about the exception -- see the try/except chapter
    ## Run code!
    collected_tweets = [] # where I'll collect all the tweet data I get as I page through my results, 5 at a time
    ids = []
    max_id = None
    my_params = {'count' : 5} # query parameters for 1st request

    for i in range(5):
        if len(ids) > 0: # if we have already started the paging process 
            my_params['max_id'] = min(ids) - 1
            # Twitter suggests that you take the minimum of the ids you got before, then subtract one from it, to make sure you get only ones you haven't received before. We can use the built-in min function here (could also accumulate by hand).
        # Regardless, now we need to make a request to the logged in user's timeline with the query parameters
        r = oauth.get("https://api.twitter.com/1.1/statuses/user_timeline.json",params = my_params)  # passes {'count': 5, 'max_id': whatever} ...
        # Now, append this data to a list so we can collect all the paged results
        collected_tweets.append(r.json())
        next_five_ids = [tweet['id'] for tweet in r.json()]  # get the ids from the tweets we just got         
        ids = ids + next_five_ids # add them to the list, and start the for loop process over again

print "\n***Regardless -- here's collected tweets! ***\n"
print collected_tweets
# so here, using cached data, if you supplied it (or live data if you didn't), you could do investigation/your project: create class instances, sort stuff, etc.
