#!/usr/bin/env python
# coding: utf-8

# In[1]:


from ntscraper import Nitter
from datetime import datetime
import json


# In[ ]:


scraper = Nitter(log_level=1, skip_instance_check=False)


# In[ ]:


today = datetime.today().strftime('%Y-%m-%d')
liveTweets = scraper.get_tweets("gaza injured", mode="term", exclude= ["nativeretweets"], number = 30, since=today)


# In[ ]:


#liveTweets


# In[ ]:


#for tweet in liveTweets['tweets']:
#    print(tweet['text'])
#    print(tweet['date'])
#    print(tweet['stats'])
#    print(tweet['user']['profile_id'])
#    print('---------------------------------------')


# In[ ]:


to_extract = ['text','date', 'stats','user']
out_dict = {}
count = 0

for tweet in liveTweets['tweets']:
    out_dict[f'tweet_{count}'] = {}
    for field in to_extract:
        #print(f"{field}: {tweet[field]}")
        out_dict[f'tweet_{count}'][field] = tweet[field]
    count+=1

json_obj = json.dumps(out_dict, indent=4)
with open("liveTweets.json","w") as outfile:
    outfile.write(json_obj)


# In[ ]:


#out_dict


# In[ ]:




