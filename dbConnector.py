import json
import mysql.connector
from mysql.connector import errorcode

# Load JSON data from file
choice = input("Select social media sata to insert into database:\n1)Reddit\n2)Twitter\n")

if(choice == '1'):
    print("Loading Reddit post data...")
    with open('C:/Users/Tengis/VSCodeProjects/RedditAPI/apiResponse.json', 'r') as json_file:
        data = json.load(json_file)
elif (choice == '2'):
    print("Loading Twitter post data...")
    with open('C:/Users/Tengis/JupyterLabProjects/liveTweets.json', 'r') as json_file:
        data = json.load(json_file)
else:
    print("Input Error issue\nexiting...")
    exit()


#get Mysql credentials
with open('C:/Users/Tengis/VSCodeProjects/Mysql_PyConnector/MysqlRootPwd.txt', 'r') as file:
    credentials = [line.rstrip() for line in file]

# Connect to MySQL
try:
    connection = mysql.connector.connect(
        host='localhost',
        user= credentials[0],
        password= credentials[1],
        database='social_media_data'
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Invalid username/password combination")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database specified does not exist")
    else:
        print(err)


# Create a cursor
cursor = connection.cursor()

#test connection
if connection.is_connected():
    print("DB Connection Succesful...")

# Insert data into MySQL table; this method protects against sql inject
#TODO: implement exception handling per iteration incase of duplicate insert
if(choice == '1'):
    #insert Reddit Data
    for post in data:
        query = "INSERT INTO reddit_posts (title, subreddit, full_name, id, ups, downs, upvote_ratio, score, created_utc) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (data[post]['title'], data[post]['subreddit_name_prefixed'], data[post]['name'], data[post]['id'], data[post]['ups'], data[post]['downs'], data[post]['upvote_ratio'], data[post]['score'], data[post]['created_utc'])
        cursor.execute(query, values)
elif(choice == '2'):
    #Insert Twitter data
    for post in data:
        query = "INSERT INTO twitter_posts (title, date_posted, comments, retweets, quotes, likes, profile_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (data[post]['text'], data[post]['date'], data[post]['stats']['comments'], data[post]['stats']['retweets'], data[post]['stats']['quotes'], data[post]['stats']['likes'], data[post]['user']['profile_id'])
        cursor.execute(query, values)
else:
    #Insert Facebook data
    pass

print(cursor)
# Commit changes and close connection
connection.commit()
print("Database changes commited!")
cursor.close()
connection.close()

#for more info on mysql connector documentation, see:
#https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-select.html
