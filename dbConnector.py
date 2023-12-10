import json
import mysql.connector
from mysql.connector import errorcode

# Load JSON data from file
with open('C:/Users/Tengis/JupyterLabProjects/apiResponse.json', 'r') as json_file:
    data = json.load(json_file)

with open('MysqlRootPwd.txt', 'r') as file:
    credentials = [line.rstrip() for line in file]

# Connect to MySQL
try:
    connection = mysql.connector.connect(
        host='localhost',
        user= credentials[0],
        password= credentials[1],
        database='reddit_db'
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

# Insert data into MySQL table
for post in data:
    query = "INSERT INTO posts (title, subreddit, full_name, id, ups, downs, upvote_ratio, score, created_utc) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (data[post]['title'], data[post]['subreddit_name_prefixed'], data[post]['name'], data[post]['id'], data[post]['ups'], data[post]['downs'], data[post]['upvote_ratio'], data[post]['score'], data[post]['created_utc'])
    cursor.execute(query, values)

# Commit changes and close connection
connection.commit()
cursor.close()
connection.close()

#for more info on mysql connector documentation, see:
#https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-select.html
