## 506 PS 9 draft

# import statements
import unittest
import requests
import json
from pprint import pprint

### The following code makes lists of positive words and negative words, saving them in the variables pos_ws and neg_ws. DO NOT CHANGE THIS CODE. You'll need it later!
pos_ws = []
f = open('positive-words.txt', 'r')

for l in f.readlines()[35:]:
    pos_ws.append(unicode(l.strip()))
f.close()

neg_ws = []
f = open('negative-words.txt', 'r')
for l in f.readlines()[35:]:
    neg_ws.append(unicode(l.strip()))

### END PROVIDED CODE

# [PROBLEM 1]
print "\n\n***** Problem 1 *****"

## Fill in the missing parts of class Post per the instructions in the textbook. 

class Post():
    """object representing status update"""
    def __init__(self, post_dict={}):
        if 'message' in post_dict:
            self.message = post_dict['message']
        else:
            self.message = ""
        
    def positive(self):
        return None
                   
    def negative(self):
        return None

    def emo_score(self):
        return None
        

## [PROBLEM 2]
print "\n\n***** Problem 2 *****"
## This code is provided so you can use it in the problem set. Do not change it!
## You should answer the question about it on the textbook assignment, too.
sample = open('samplepost.txt').read()
sample_post_dict = json.loads(sample)
p = Post(sample_post_dict)
## End provided code

## Now, if you want, uncomment and run the next lines of code if you're having trouble getting the tests for the above problem to pass. The output from this code may help you understand what a post_dict contains, and what your code has actually extracted from it and assigned to the comments and likes instance variables.
#print "sample_post_dict\n", pprint(sample_post_dict)
#print "the comments in one Post instance\n", pprint(p.comments)
#print "the likes in one Post instance\n", pprint(p.likes)



## [PROBLEM 3]
print "\n\n***** Problem 3 *****"

## Fill in your access token (in quotes, because it's a string) in the code if you don't want to have to paste it every time you run the program (but you'll have to replace it every couple hours).

access_token = None 

####The following code allows us to grade your code with graders' tokens. (It also helps you run the code if your access token has expired.) Please do not change it! 
r = requests.get("https://graph.facebook.com/v2.3/me/feed",params={"limit":2, "access_token":access_token})
# print r.status_code
if r.status_code != 200:
    access_token = raw_input("Get a Facebook access token v2.3 from https://developers.facebook.com/tools/explorer and enter it here if the one saved in the file doesn't work anymore.  :\n")

## This global variable holds the group id for our class Facebook group.
GROUP_ID = "323187111349524"  

#### End provided code

## Baseurl for the Facebook API
## Remember to replace "me" with the GROUP ID value if you want data from the class FB group 
baseurl = "https://graph.facebook.com/v2.3/me/feed"  

# Building the Facebook parameters dictionary
url_params = {}
url_params["access_token"] = access_token
url_params["fields"] = "comments{comments{like_count,from,message,created_time},like_count,from,message,created_time},likes,message,created_time,from" # Parameter key-value so you can get post message, comments, likes, etc. as described in assignment instructions.

# Write code to make a request to the Facebook API using paging and save data in fb_data here.


## [PROBLEM 4]
print "\n\n***** Problem 4 *****"
    
# Write your list comprehension here:






## [PROBLEM 5]
print "\n\n***** Problem 5 *****"

# Write code to collect top commenters and top likers here.

 


## [PROBLEM 6]
print "\n\n***** Problem 6 *****"

# Define your function here.


  
## [PROBLEM 7]
print "\n\n***** Problem 7 *****"
# Write code to create your emo_scores.csv file here!





##### TESTS BELOW, DO NOT CHANGE #########
class Problem1(unittest.TestCase):
    def test_instvar_1(self):
        self.assertEqual(type(p.comments), type([]), "testing type of p.comments")
    def test_instvar_2(self):
        self.assertEqual(len(p.comments), 4, "testing length of p.comments")
    def test_instvar_3(self):
        self.assertEqual(type(p.comments[0]), type({}), "testing type of p.comments[0]")
    def test_instvar_4(self):
        self.assertEqual(type(p.likes), type([]), "testing type of p.likes") 
    def test_instvar_5(self):       
        self.assertEqual(len(p.likes), 4, "testing length of p.likes")
    def test_instvar_6(self):
        self.assertEqual(type(p.likes[0]), type({}), "testing type of p.likes[0]")
    def test_method_1(self):
        p.message = "adaptive acumen abuses acerbic aches for everyone"
        self.assertEqual(p.positive(), 2, "testing return value of .positive()")
    def test_method_2(self):
        p.message = "adaptive acumen abuses acerbic aches for everyone"
        self.assertEqual(p.negative(), 3, "testing return value of .negative()")
    def test_method_3(self):
        p.message = "adaptive acumen abuses acerbic aches for everyone"
        self.assertEqual(p.emo_score(), -1, "testing return value of .emo_score()")

class Problem3(unittest.TestCase):
    def test_1(self):
        self.assertEqual(type(fb_data),type({}),"testing type of fb_data")
    def test_1(self):
        self.assertEqual(type(fb_data["data"]),type([]), "testing type of the data key in fb_data, and that fb_data has a key data")

class Problem4(unittest.TestCase):
    def test_1(self):
        self.assertEqual(type(post_insts), type([]), "testing that post_insts is a list")
    def test_2(self):
        self.assertTrue(len(post_insts) > 0)
    def test_3(self):
        self.assertIsInstance(post_insts[1], Post, "Testing that elements of post_insts are  Post instances")

class Problem5(unittest.TestCase):
    def test_1(self):
        self.assertEqual(len(top_commenters),3,"Testing that there are 3 elements in top_commenters")
    def test_2(self):
        self.assertEqual(type(top_commenters[1]),type(u""), "Testing that elements of top_commenters are Unicode strings (should be strings of the commenters' names -- note that you'll have to judge whether they're the correct names)")
    def test_3(self):
        self.assertEqual(len(top_likers),3,"Testing that there are 3 elements in top_likers")
    def test_2(self):
        self.assertEqual(type(top_likers[1]),type(u""), "Testing that elements of top_likers are Unicode strings (should be strings of the likers' names -- note that you'll have to judge whether they're the correct names)")

class Problem6(unittest.TestCase):
    def test_1(self):
        pi = [p] # list of one post
        self.assertEqual(unique_facebookers(pi),"likers", "Testing that the unique_facebookers function returns 'likers' in an appropriate scenario")

unittest.main(verbosity=2)