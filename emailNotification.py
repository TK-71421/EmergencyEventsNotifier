import pprint
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime
import spacy
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#query db to get data to build email

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

#read query from file
fd = open("C:/Users/Tengis/VSCodeProjects/EmailNotificationGenerator/sqlQuery.sql","r")
query = fd.read()
fd.close()

cursor.execute(query)

#identify things needed for email via Named Entity Recognition in query results
#need to handle potential puplicate posts?
nlp = spacy.load('en_core_web_sm')

emailData = {}

for i,(twitter_title, tp_post_date, reddit_title, reddit_post_date) in enumerate(cursor):
    emailData[f"notif_{i}"] = {}
    emailData[f"notif_{i}"]["postTitle"] = twitter_title
    emailData[f"notif_{i}"]["time_posted"] = tp_post_date
    emailData[f"notif_{i}"]["keywords"] = {}
   
    doc = nlp(twitter_title) 
    for entity in doc.ents:
        emailData[f"notif_{i}"]["keywords"][f"{entity.text}"] = entity.label_

#close db connection
cursor.close()
connection.close()

'''
see below for info on all SpaCy entity labels:
https://stackoverflow.com/questions/70835924/how-to-get-a-description-for-each-spacy-ner-entity
'''


with open("C:/Users/Tengis/VSCodeProjects/EmailNotificationGenerator/emailpw.txt") as file:
        pw = file.read()

def send_email_notif(fromaddr, toaddr, pw, post_data):
    '''
    fromaddr: sender email address
    toaddr: recipient email address
    pw: password of sender email actt
    post_data: body contents (nested dict) of email 
    '''
    #convert time_posted field to datetime & other preprocessing
    posted_dt = datetime.strptime(post_data['time_posted'], "%b %d, %Y · %I:%M %p UTC")
    time_elapsed = datetime.now() - posted_dt
    hours, remainder = divmod(time_elapsed.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    tags = ', '.join(post_data['keywords'].keys())

    #build email body from post_data
    body = (f"RECENT SOCIAL MEDIA ACTIVITY SPIKING AROUND EVENT:\n\n"
            f"TAGS INCLUDE: [{tags}]\n\n"
            f"TIME OF EVENT: {post_data['time_posted']}\n\n"
            f"TIME ELAPSED SINCE EVENT: {time_elapsed.days} days, {hours} hours, {minutes} minutes, {seconds} seconds\n\n"
            f"RECENT HEADLINE:\n\"{post_data['postTitle']}\""
    )


    # Set up MIMEText and MIMEMultipart objects
    msg = MIMEMultipart()
    msg.attach(MIMEText(body, 'plain'))

    # Configure the email headers
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "EMERGENCY ALERT NOTIFICATION"

    # Connect to the SMTP server (in this example, using Gmail)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    
    # Create a connection to the SMTP server & login
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Use TLS for security
    server.login(fromaddr, pw)

    # Send the email
    server.sendmail(fromaddr, toaddr, msg.as_string())

    # Close the connection to the SMTP server
    server.quit()


#prompt for recipient email & send alerts
email = input("Enter an email to recieve Alerts from Emergency Notification System:\n")
for notif in emailData:
    try:
        print(f"sending notification alert email to: {email}...")
        send_email_notif("hjohnson24816@gmail.com", email, pw, emailData[notif])
    except smtplib.SMTPException as err:
        print(f"Error sending Alert(s):\n{err}")
        exit(1)
