CLIENT_ID = 'QDp6IOY52ye8CpzPk20PUQ'
SECRET_KEY = 'OM7mOfe-YjbJA-bb7ljo97sbyicMXg'

import requests
import json
import subprocess

client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

with open('reddit_pw.txt', 'r') as file:
    credentials = [line.rstrip() for line in file]


data = {
    'grant_type': 'password',
    'username': credentials[0],
    'password': credentials[1]
}

headers = {'User-Agent': 'GnomeBot/0.0.1'}


#request access token for OAuth2 protocol
response = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=client_auth, data=data, headers=headers)


TOKEN = response.json()['access_token']
#print(TOKEN)


headers['Authorization'] = f'bearer {TOKEN}'


subreddit = 'Palestine' 
print(f"Grabbing Posts from: r/{subreddit}.........")


#limit param goes from 1-100
response = requests.get(f'https://oauth.reddit.com/r/{subreddit}/hot',
                    headers=headers, params={'limit':'100'})

if response.status_code != 200:
    print("Error collecting; please double check request syntax")
    print(f"HTTP Response: {response.status_code}")



#extract desired fields from API response; write to json file to be inserted in db
to_extract = ['title','subreddit_name_prefixed','name','id','ups','downs','upvote_ratio','score','created_utc']

out_dict = {}
count=0

for post in response.json()['data']['children']:
    #if count == 0: #skip 1st post: weekly discussion board
    #    count+=1
    #    continue
    out_dict[f'post_{count}'] = {}
    for field in to_extract:
        #print(f"{field}: {post['data'][field]}")
        out_dict[f'post_{count}'][field] = post['data'][field]

        #add words in title to find keywords
        #if field == 'title':
            #with open("titles.txt","a", encoding="utf-8") as outfile:
                #outfile.write(post['data']['title']+"\n")
    count+=1

json_obj = json.dumps(out_dict, indent=4)
with open("apiResponse.json","w") as outfile:
    outfile.write(json_obj)

#print(out_dict)
print("output saved to: apiResponse.json")




'''
#find 10 most common words in post titles (keywords) and write to file
def call_most_common_words_script(input_file_path, output_file_path, n):
    script_path = "C:/Users/Tengis/VSCodeProjects/RedditAPI/MostCommonWordTrie.py"  # Replace with the actual path to your script
    command = ["python", script_path, input_file_path, output_file_path]

    try:
        # Run the script with input file, output file, and n as arguments
        subprocess.run(command + [str(n)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        # Handle the error as needed

input_path = "C:/Users/Tengis/VSCodeProjects/RedditAPI/titles.txt"
output_path = "C:/Users/Tengis/VSCodeProjects/RedditAPI/keywords.txt"
call_most_common_words_script(input_path, output_path, 10)



#arbitrary post ID
postID = "17vtdi3"
response_comments = requests.get('https://oauth.reddit.com/r/politics/comments/'+postID,
                    headers=headers, params={'limit':'5'})
# NOTE: FIRST 1-2 comments are autoMod's commenting rules (will need to skip)




for comment in response_comments.json()[1]['data']['children']:
    print(comment['data'],end='------------\n')

# NOTE: FIRST 1-2 comments are autoMod's commenting rules (will need to skip)
# last dict in ['children'] array is parent id's -> can be ignored
#only loop thru (1 to n-1) comments
'''




