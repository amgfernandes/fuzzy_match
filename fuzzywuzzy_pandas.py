# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

'''Based on:
https://github.com/kelmouloudi/MediumArticle-FuzzyWuzzy
'''
# %%
from IPython import get_ipython

# %%
import pandas as pd
from fuzzywuzzy import process, fuzz
import matplotlib.pyplot as plt

# %%
hr = pd.read_csv('data/hr.csv', encoding='unicode_escape')
it = pd.read_csv('data/it.csv', encoding='unicode_escape')

display( hr.head() )
display( it.head() )

# %%

'''Dumb strategy string matching'''
hr['gen_email'] = hr['full_name'].str[0] + '.' + hr['full_name'].str.split().str[1] + '@giantbabybibs.org'
hr['gen_email'] = hr['gen_email'].str.lower()
hr.head(3)

# %%
# Now let's check if the gen_email values exist in the actual email list
hr['exists'] = hr.apply(lambda x: x.gen_email in list(it.email), axis=1)
hr.head(5)

# %% 
# How many emails did we get right using this method?
%matplotlib inline
ax= hr.exists.value_counts().sort_values().plot(kind='barh', color=['tomato', 'c'], figsize=(12,1), width=0.3)
plt.xlim(0,201), plt.xticks(fontsize=8), ax.set_frame_on(False), plt.grid(color='white', alpha=.4, axis='x') ;


# %%

'''The not so boring FuzzyWuzzy application :
In our case, we want to compare each full name in the hr.full_name column with all the actual emails in the it.email column, so we'll be using process.extract.

However, we only need the first part of the emails for this comparison, because the domain name part @giantbabybibs.org could interfere with ratio calculation. Let's generate a new column within the it dataframe called username :
'''

it['username'] = it['email'].str.replace('@giantbabybibs.org', '')
it.head(3)

# %% [markdown]
# Now let's use **process.extract** to compare `hr.full_name` to `it.username` (note that we added the domaine name `@giantbabybibs.org` AFTER calculating the ratios): <br>
# <sub id='codex'>[code explanation 6](#codex6)</sub>
# <a id='code6'></a>

# %%

'''Now let's use process.extract to compare hr.full_name to it.username (note that we added the domaine name @giantbabybibs.org AFTER calculating the ratios):'''
actual_email = []
similarity = []

for i in hr.full_name:
        ratio = process.extract( i, it.username, limit=1)
        actual_email.append(ratio[0][0])
        similarity.append(ratio[0][1])

hr['actual_email'] = pd.Series(actual_email)
hr['actual_email'] = hr['actual_email'] + '@giantbabybibs.org'
hr['similarity'] = pd.Series(similarity)

hr.head()

# %%
final_result = hr[['full_name', 'actual_email', 'similarity']]
final_result.head()

# %%
final_result.sort_values(by='similarity', ascending=False).head(10)

# %%
# Random sampling

sample = final_result.sample( n=8, random_state=9 )
sample

# %%
'''
As we can see here, the random sample above shows that one particular mistake was made for employee N°60: Rocio E. Thatch. Could that be because of the abbreviated middle name? 
Let's check if we have any other employees like this one :'''
final_result[final_result['full_name'].str.contains('.', regex=False)]

'''The process got all of the 4 employees wrong. Even though that's only 4 wrongs out of 200, which means a success rate of 98%'''


# %% [markdown]
# Now would you look at that! The process got all of the 4 employees wrong. Even though that's only **4 wrongs** out of **200**, which means a **success rate of 98%**, imagine if you have 173.000 employees in the dataframe (for a company like General Motors for example), that would mean **3460 wrong emails**.
# 
# To understand why this mistake was made, we have to inspect which `FuzzyWuzzy` **scorer** the process used. A scorer is a method that generates a ratio by comparing two strings. And yes, as we have seen before, `FuzzyWuzzy` has many different scorers you can choose from depending on the kind of data you're working with. Here is a list of said scorers :
# * fuzz.ratio
# * fuzz.partial_ratio
# * fuzz.token_set_ratio
# * fuzz.token_sort_ratio
# * fuzz.partial_token_set_ratio
# * fuzz.partial_token_sort_ratio
# * **fuzz.WRatio**
# * fuzz.QRatio
# * fuzz.UWRatio
# * fuzz.UQRatio
# 
# The one used by default for the process is `fuzz.WRatio`. If you want to use `process` with one of these scorers, just pass it as an argument like this:
# 
# `ratio = process.extract( column_A, column_B, limit=1, scorer=fuzz.ratio)`
# 
# Next, we'll test some of these scorers to see which one works perfectly in our case. Let the hunt for a success rate of 100% begin!
# %% [markdown]

# # The quest for the perfect FuzzyWuzzy scorer :
# Let's see all the `FuzzyWuzzy` scorers we can use. We'll assign an abbreviation to each of them to use it later as a key in a dictionary (the scorer methods are case sensitive. fuzz.wratio for example will not work) :
# * fuzz.ratio (R)
# * fuzz.partial_ratio (PR)
# * fuzz.token_set_ratio (TSeR)
# * fuzz.token_sort_ratio (TSoR)
# * fuzz.partial_token_set_ratio (PTSeR)
# * fuzz.partial_token_sort_ratio (PTsoR)
# * fuzz.WRatio (WR)
# * fuzz.QRatio (QR)
# * fuzz.UWRatio (UWR)
# * fuzz.UQRatio (UQR)



# %%

# And here's our fancy `scorer_dict` dictionary :
scorer_dict = { 'R':fuzz.ratio, 'PR': fuzz.partial_ratio, 'TSeR': fuzz.token_set_ratio, 'TSoR': fuzz.token_sort_ratio,
                'PTSeR': fuzz.partial_token_set_ratio, 'PTSoR': fuzz.partial_token_sort_ratio, 'WR': fuzz.WRatio, 
                'QR': fuzz.QRatio, 'UWR': fuzz.UWRatio, 'UQR': fuzz.UQRatio }

# %% [markdown]
# Remember the `hr` dataframe? We'll use its column `full_name` for this test. We'll call it `scorer_test` :

# %%
scorer_test = hr[['full_name']].copy()
scorer_test.head()

# %% [markdown]
# And now for the big show! We'll define a **function** called `scorer_tester_function` that takes a **parameter x** from the `scorer_dict` (which is simply the name of the scorer) and matches the `scorer_test.full_name` column with the `it.email` column : <br>


# %%
def scorer_tester_function(x) :
    actual_email = []
    similarity = []
    
    for i in scorer_test['full_name']:
        ratio = process.extract( i, it.username, limit=1, scorer=scorer_dict[x])
        actual_email.append( ratio[0][0] )
        similarity.append( ratio[0][1] )

        scorer_test['actual_email'] = pd.Series(actual_email)
        scorer_test['actual_email'] = scorer_test['actual_email'] + '@giantbabybibs.org'
        scorer_test['similarity'] = pd.Series(similarity)
        
    return scorer_test

# %% [markdown]
# And then, we'll apply the function with different scorers from the `scorer_dict` dictionary. Let's start with the 4 employees **fuzz.WRatio (WR)** got wrong : <br><br>


# %%
scorer_tester_function('WR')
scorer_test[scorer_test.full_name.str.contains('.', regex=False)]

# %% [markdown]
# As we can see, **fuzz.WRatio (WR)** performs badly with full names having an abbreviated middle name. Let's see if other scorers will correct this, **fuzz.ratio (R)** for example :

# %%
scorer_tester_function('R')
display(scorer_test[scorer_test.full_name.str.contains('.', regex=False)])
display(scorer_test[81:82])

# %% [markdown]
# It did! **fuzz.ratio (R)** got **199 out of 200 correct** (99.5% success rate). The only mistake it made was for employee N°81: **Sterling Malory Archer**. (we're in the danger zone!). However, all employees with abbreviated middle names were properly handled with this scorer.
# 
# Can we do better? Let's try another scorer, **fuzz.partial_ratio (PR)** this time, and see if it's going to work on all problematic employee names :

# %%
scorer_tester_function('PR')
display(scorer_test[scorer_test.full_name.str.contains('.', regex=False)])
display(scorer_test[81:82])

# %% [markdown]
# Finally! After manually checking all other records, I hereby announce **fuzz.partial_ratio (PR)** the champion with **100% success rate**. The quest is over guys!

# 
# In real world applications, you may be working with huge amounts of data, in which case manually inspecting the results is not an option. That's why you need to understand what each `FuzzyWuzzy` scorer does in order to choose the one that works best for the kind of data you're handling.
# 
# To explore the differences between the scorers `FuzzyWuzzy` has to offer, we're going to work with a test string. We want to match the **address of a friend** with **multiple addresses from a phonebook** (yes, phonebooks are still a thing!):

# %%
friend_address = '56 West Princess Rd. Cedar Rapids, IA 52402'

phonebook = [ '9102 South St. Lake Worth, FL 33460',
              '20425 Prince Edward Road, West philadelphia, PA 56560',
              'Wst Princess Road, Appt. 56 N°8 3rd floor, C.Rapids, 52402 Iowa ',
              '400 Van Dyke St.Hartford, IA 26106',
              '56 Golden Star Rd, Stone Rapids, GA 52483' ]

# %% [markdown]
# And now let's put all the scorers to the test. We'll use the `fuzz` module instead of `process` in this case.


# %%
print("Friend's address : ", friend_address, '\n', 62*'-', '\n')

for address in phonebook:
    ratio = fuzz.ratio(friend_address, address)
    print(address,'\nRATIO: ',ratio, '\n')

# %% [markdown]
# **fuzz.ratio (R)** simply calculates the **Levenshtein distance**. It only returns 100% if the two strings are exactly similar, uppercase and lowercase included, which makes it useful if we're looking for an exact match.
# %% [markdown]
# * ## fuzz.partial_ratio (PR) :

# %%
print("Friend's address : ", friend_address, '\n', 62*'-', '\n')

for address in phonebook:
    ratio = fuzz.partial_ratio(friend_address, address)
    print(address,'\nRATIO: ',ratio, '\n')

# %% [markdown]
# **fuzz.partial_ratio (PR)** takes into account subsets of the strings it compares, and then returns a ratio according to their similarities. For example, it will return a ratio of 100% if it compares **Dwayne The Rock Johnson** with **Dwayne** :

# %%
fuzz.partial_ratio('Dwayne The Rock Johnson', 'Dwayne')

# %% [markdown]
# In our case however, it got fooled because the 5<sup>th</sup> address has common words with the friend's address like `56`, `Rd.` and `Rapids`. So, perhaps this is not the best scorer to use for this particular task.


# %%
print("Friend's address : ", friend_address, '\n', 62*'-', '\n')

for address in phonebook:
    ratio = fuzz.token_sort_ratio(friend_address, address)
    print(address,'\nRATIO: ',ratio, '\n')

# %% [markdown]
# The Token methods have the advantage of ignoring case and punctuation (all characters get turned to lowercase characters). In the case of **fuzz.token_sort_ratio (TSoR)**, the 'Tokenized' strings (each word is turned into a token) get sorted in alphanumeric order before applying the basic **fuzz.ratio (R)** on them, so the order of the words in both strings compared doesn't matter (unlike the previous non-token methods). In this case, this scorer performed very well.
# %% [markdown]
# * ## fuzz.token_set_ratio (TSeR) :

# %%
print("Friend's address : ", friend_address, '\n', 62*'-', '\n')

for address in phonebook:
    ratio = fuzz.token_set_ratio(friend_address, address)
    print(address,'\nRATIO: ',ratio, '\n')

# %% [markdown]
# This is by far the best ratio for the given task. **fuzz.token_set_ratio (TSeR)** is similar to **fuzz.token_sort_ratio (TSoR)**, except it ignores duplicated words (hence the name, because a `set` in Math and also in Python is a collection/data structure that holds no duplicate values). It also conducts a pair to pair comparison on tokens that are common to both strings compared.
# 
# Example of a set :

# %%
song = ['badger', 'badger', 'badger', 'mushroom', 'mushroom', 'snake', 'badger']
set(song)

# %% [markdown]
# * ## fuzz.partial_token_sort_ratio (PTSoR) :

# %%
print("Friend's address : ", friend_address, '\n', 62*'-', '\n')

for address in phonebook:
    ratio = fuzz.partial_token_sort_ratio(friend_address, address)
    print(address,'\nRATIO: ',ratio, '\n')

# %% [markdown]
# **fuzz.partial_token_sort_ratio (PTSoR)** has the same working as **fuzz.token_sort_ratio (TSR)**, but it uses the **fuzz.partial_ratio (PR)** method after tokenization and sorting rather than the normal **fuzz.ratio (R)** method.
# %% [markdown]
# * ## fuzz.partial_token_set_ratio (PTSeR) :

# %%
print("Friend's address : ", friend_address, '\n', 62*'-', '\n')

for address in phonebook:
    ratio = fuzz.partial_token_set_ratio(friend_address, address)
    print(address,'\nRATIO: ',ratio, '\n')

# %% [markdown]
# Same as **fuzz.token_set_ratio (TSR)**, but instead of using **fuzz.ratio (R)** after tokenization and setting (eliminating duplicates), it uses **fuzz.partial_ratio (PR)**. Here we see it is way too forgiving to be useful in this case.
# %% [markdown]
# * ## fuzz.WRatio (WR) :

# %%
print("Friend's address : ", friend_address, '\n', 62*'-', '\n')

for address in phonebook:
    ratio = fuzz.WRatio(friend_address, address)
    print(address,'\nRATIO: ',ratio, '\n')

# %% [markdown]
# This is the default scorer that gets used with **process.extract()**. This scorer, **fuzz.WRation (WR)** (which stands for Weighted Ratio), is an attempt to get a better ratio than the standard **fuzz.ratio (R)** one. Here is how it works according to the source code:
# 1. Take the ratio of the two processed strings (fuzz.ratio)
# 2. Run checks to compare the length of the strings
#     * If one of the strings is more than 1.5 times as long as the other
#       use partial_ratio comparisons - scale partial results by 0.9
#       (this makes sure only full results can return 100)
#     * If one of the strings is over 8 times as long as the other
#       instead scale by 0.6
# 3. Run the other ratio functions
#     * if using partial ratio functions call partial_ratio,
#       partial_token_sort_ratio and partial_token_set_ratio
#       scale all of these by the ratio based on length
#     * otherwise call token_sort_ratio and token_set_ratio
#     * all token based comparisons are scaled by 0.95
#       (on top of any partial scalars)
# 4. Take the highest value from these results, round it and return it as an integer.
# %% [markdown]
# It's magic I tell you!
# %% [markdown]
# * ## fuzz.UWRatio (UWR) :

# %%
print("Friend's address : ", friend_address, '\n', 62*'-', '\n')

for address in phonebook:
    ratio = fuzz.UWRatio(friend_address, address)
    print(address,'\nRATIO: ',ratio, '\n')

# %% [markdown]
# Same as **WR**, but it takes Unicode into consideration (hence the U). In this case, the 3rd address got a score of 72 instead of 73 that we got with **WR** because of the **° character** that forces the use of Unicode encoding (it not being present in the friend's address made the score slightly lower).
# %% [markdown]
# * ## fuzz.QRatio (QR) :

# %%
print("Friend's address : ", friend_address, '\n', 62*'-', '\n')

for address in phonebook:
    ratio = fuzz.QRatio(friend_address, address)
    print(address,'\nRATIO: ',ratio, '\n')

# %% [markdown]
# According to the source code, **QR** stands for Quick Ratio because it short circuits the comparison process if either of the strings is empty after processing.
# %% [markdown]
# * ## fuzz.UQRatio (UQR) :

# %%
print("Friend's address : ", friend_address, '\n', 62*'-', '\n')

for address in phonebook:
    ratio = fuzz.UQRatio(friend_address, address)
    print(address,'\nRATIO: ',ratio, '\n')

# %% [markdown]
# Same as **QR** but it stands for Unicode Quick Ratio (just like there is a Unicode version of **WR**)
# %% [markdown]
# <a id='theverdict'></a>
# 
# ---
# [Go back to table of contents ^](#table)
# # The verdict :
# %% [markdown]
# As we can see, the best performing scorer changes from an application to an other. In the case of comparing full names to emails, **fuzz.partial_ratio (PR)** is the way to go. For addresses, **fuzz.token_set_ratio (TSeR)** is the scorer that performed best, not only because it gave the highest ratio to the correct address, but because the difference between the ratios of the correct address and the closest wrong address is the highest (12 points).
# 
# In any case, using `FuzzyWuzzy` needs some experimenting before settling for the best method to match strings.

# %%
