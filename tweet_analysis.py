import json
import gzip
import string 
import operator
from datetime import datetime


# Initialize matrices to hold tweet timestamps and tweet contents:
tweet_list = []
# Initialize variables to keep track of counts:
count_start_brace = 0
count_end_brace = 0
count_newline = 0 

try:
    tweet_list = open('twitter_data.txt').read().splitlines()
    
except IOError: # if file does not exist, then create it
    filename = "twitterData.json.txt.gz"
    for line in gzip.open(filename , 'rt', encoding='utf-8'):
        if line[0] != '{': # If missing curly brace at beginning of object
            line = '{' + line
            count_start_brace += 1
        if line[-1] != '\n': # If missing newline at end of object
            line = line + '\n'
            count_newline += 1
        if line[-2] != '}': # If missing curly brace at end of object
            line = line[:-1] + '}' + line[-1:]
            count_end_brace += 1
        tweet = json.loads(line.strip())
        tweet_list.append(tweet["created_at"] + ' ~ ' + tweet["text"]) # append tweet timestamp and text to list
    with open("twitter_data.txt", "w") as fobj:
        for x in tweet_list:
            fobj.write(str(x.encode('utf8')))
            fobj.write('\n')
   
# Initialize corpora:
O_corpus = []
R_corpus = []

# Place tweets in appropriate corpora:
for tweet in tweet_list:
    if ('obama' or 'barack') in str.lower(tweet): # render tweet all lowercase
        O_corpus.append(tweet)
    if ('mitt' or 'romney') in str.lower(tweet):
        R_corpus.append(tweet)

# Initialize lists for date - H (chop off the minutes and seconds characters 
# from the "created_at" string before you parse it into a date)
O_date_h = []
R_date_h = []
datetime_format = '%a, %d %b %Y %H'

# Loop through tweets to get date:
for tweet in O_corpus:
    O_date_h.append(datetime.strptime(tweet[:19], datetime_format))
for tweet in R_corpus:
    R_date_h.append(datetime.strptime(tweet[:19], datetime_format))

earliest_tweet = min(min(R_date_h), min(O_date_h))
min(R_date_h) == min(O_date_h) # True

# Initialize lists to hold only hours:
O_h = []
R_h = []

for date_h in O_date_h:
    time_since = (date_h - earliest_tweet)
    hours_since = int(time_since.total_seconds()//3600)
    O_h.append(hours_since)
for date_h in R_date_h:
    time_since = (date_h - earliest_tweet)
    hours_since = int(time_since.total_seconds()//3600)
    R_h.append(hours_since)

latest_hour = max(max(R_h), max(O_h))
max(R_h) == max(O_h) # True

f = open('input_p2.txt','w+') # Create file to write to
for i in range(latest_hour + 1): # Establish range of hours to look for and get counts
    f.write(str(i) + ' ' + str(O_h.count(i)) + ' ' + str(R_h.count(i)) + '\n')
f.close()

# Initialize lists to hold words
O_words = []
R_words = []
for tweet in O_corpus:
    words = (str.lower(tweet[28:])).split() # Remove the "created at" data from string and split it into words
    O_words += words
    
for tweet in R_corpus:
    words = (str.lower(tweet[28:])).split() # Remove the "created at" data from string and split it into words
    R_words += words

O_words_clean = []
R_words_clean = []

# Remove hashtag #words and @UserName and any misc 1 letter words other than 'a' or 'I':
for word in O_words:
    if (word[0] == '@') or (word[0] == '#') or ((len(word) == 1) and ((word != 'a') or (word != 'i'))): 
       continue
    else:
       O_words_clean.append(word)
for word in R_words:
    if (word[0] == '@') or (word[0] =='#') or ((len(word) == 1) and ((word != 'a') or (word != 'i'))):
       continue
    else:
       R_words_clean.append(word)


# Strip punctuation from words:
O_words_no_punc = []
R_words_no_punc = []
O_words_no_punc = [''.join(c for c in text if c not in string.punctuation) for text in O_words_clean]
R_words_no_punc = [''.join(c for c in text if c not in string.punctuation) for text in R_words_clean]

words_both = list(set(O_words_no_punc) & set(R_words_no_punc)) # Find words common to both
del words_both[0] # remove ""
words_both = [item for item in words_both if item.isalpha()] #  remove items that contain non-alphabetic characters

word_freq_O = []
word_freq_R = []

for word in words_both:
    word_freq_O.append(O_words_no_punc.count(word))
    word_freq_R.append(R_words_no_punc.count(word))

c_values = []

for i in range(len(words_both)):
    c = (word_freq_O[i] - word_freq_R[i])/(word_freq_O[i] + word_freq_R[i])
    c_values.append(c)

word_c_dict = dict(zip(words_both, c_values))
O_slanted = dict(sorted(word_c_dict.items(), key=operator.itemgetter(1), reverse=True)[:100])
R_slanted = dict(sorted(word_c_dict.items(), key=operator.itemgetter(1), reverse=False)[:100])

l_just_width = max(max(len(x) for x in O_slanted), max(len(x) for x in R_slanted)) # width for left justification of words

f = open('yule_coefficients.txt','w+') # Create file to write to
for (key_col_1, val_col_1), (key_col_2, val_col_2) in zip(O_slanted.items(), R_slanted.items()):
    f.write(key_col_1.ljust(l_just_width,' ') + ' ' + ('{0:.5f}'.format(val_col_1)).rjust(7,' ') + ' ' + 
    key_col_2.ljust(l_just_width, ' ') + ' ' + ('{0:.5f}'.format(val_col_2)).rjust(8,' ') + '\n')

f.close()
