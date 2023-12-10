#!/usr/bin/env python
# coding: utf-8

# In[1]:


CLIENT_ID = 'QDp6IOY52ye8CpzPk20PUQ'
SECRET_KEY = 'OM7mOfe-YjbJA-bb7ljo97sbyicMXg'


# In[2]:


import requests
import json


# In[3]:


client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)


# In[4]:


with open('pw.txt', 'r') as file:
    credentials = [line.rstrip() for line in file]


# In[5]:


data = {
    'grant_type': 'password',
    'username': credentials[0],
    'password': credentials[1]
}


# In[6]:


headers = {'User-Agent': 'GnomeBot/0.0.1'}


# In[7]:


#request access token for OAuth2 protocol
response = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=client_auth, data=data, headers=headers)


# In[8]:


TOKEN = response.json()['access_token']
#print(TOKEN)


# In[9]:


headers['Authorization'] = f'bearer {TOKEN}'


# In[10]:


headers


# In[14]:


#limit param goes from 1-100
response = requests.get('https://oauth.reddit.com/r/politics/hot',
                    headers=headers, params={'limit':'100'})
#response.json()


# In[15]:


#take response dict & convert into json obj; then write to file
#see: https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/#
#https://www.geeksforgeeks.org/json-dumps-in-python/

#json_obj = json.dumps(response.json(), indent=4)
#with open("apiResponse.json","w") as outfile:
#    outfile.write(json_obj)

#will most likely need to trim unnecessary fields in here.
#need to skip first [element 0] in child arr post in API response as that is weekly discussion thread


# In[16]:


to_extract = ['title',
'subreddit_name_prefixed',
'name',
'id',
'ups',
'downs',
'upvote_ratio',
'score',
'created_utc']

out_dict = {}
count=0

for post in response.json()['data']['children']:
    if count == 0: #skip 1st post: weekly discussion board
        count+=1
        continue
    out_dict[f'post_{count}'] = {}
    for field in to_extract:
        #print(f"{field}: {post['data'][field]}")
        out_dict[f'post_{count}'][field] = post['data'][field]
    count+=1

json_obj = json.dumps(out_dict, indent=4)
with open("apiResponse.json","w") as outfile:
    outfile.write(json_obj)

out_dict


# ## API response structure
# to get to fields in post:
# repsonse.json() >> ['data']['children'] -> array dict's of all posts in response [{'kind' : "t3", 'data': {>useful fields here<} }, {}, ...]
# 
# all fields from dict of FIRST post in children array:
#     "print(response.json()['data']['children'][0]['data'].keys())"
# ## fields interested in:
# 
# ['title',
# 'subeddit_name_prefixed',
# 'name',
# 'id',
# 'ups',
# 'downs',
# 'upvote_ratio',
# 'score',
# 'created_utc']
# 
# for  'created_utc' field to Date/Time format: see https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_convert-tz

# ## Selecting speficic fields from response Json example
# 
# refer to documentation (outdated): https://github.com/reddit-archive/reddit/wiki/json
# 
# to_extract = ['title','url','score','num_comments','view_count','ups','downs','selftext']
# 
# for e in to_extract:
#     print(f"{e}: {r['data']['children'][0]['data'][e]}")

# ## Getting Comments from API example:
# https://www.reddit.com/r/redditdev/comments/v7sw57/will_i_get_all_the_comments_of_a_post_through/?rdt=53787

# In[34]:


postID = "17vtdi3"
response_comments = requests.get('https://oauth.reddit.com/r/politics/comments/'+postID,
                    headers=headers, params={'limit':'5'})
# NOTE: FIRST 1-2 comments are autoMod's commenting rules (will need to skip)


# In[47]:


for comment in response_comments.json()[1]['data']['children']:
    print(comment['data'],end='------------\n')

# NOTE: FIRST 1-2 comments are autoMod's commenting rules (will need to skip)
# last dict in ['children'] array is parent id's -> can be ignored
#only loop thru (1 to n-1) comments





