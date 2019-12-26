Problem Statement:

Extract all the Messages with logging Level as CRITICAL and ERROR from error_log.txt log file.
Use SMTP Module to send the information to the user as an attachment and Get the Count of all the Logging level Messages and display that information in the body of the message.


Steps:

1. Take email address from the user for sending the mail using ArgParse Module.
2. Create Logging Configuration object for saving the Log Events.
3. Parse the Configuration file for fetching gmail_user and gmail_password
4. Use regular Expression, to find all the messages with Logging Level as 'CRITICAL' and 'EEROR' and save the result in extract_log.txt file.
5. Use regular expression, to find the count of all the logging levels and save the result in a dictionary.
6. Created a Function for sending the mail using SMTPLIB Module and attach extract_log.txt file as an attachment.


Help File:

(venv) C:\Users\admin\PycharmProjects\LogParser>python log_parser.py -h
usage: log_parser.py [-h] -e EMAIL_ID [EMAIL_ID ...]

optional arguments:
  -h, --help            show this help message and exit

Required Named arguments:
  -e EMAIL_ID [EMAIL_ID ...], --email EMAIL_ID [EMAIL_ID ...]
  


Execution:

(venv) C:\Users\admin\PycharmProjects\LogParser>python log_parser.py -e ***
26-Dec-19 11:26:02 - Log Level Count: {'DEBUG': 10, 'INFO': 10, 'WARNING': 10, 'ERROR': 10, 'CRITICAL': 10}
26-Dec-19 11:26:02 - Message Body         <html>
            <head></head>
            <body>
                <p>Hey ***,<br>
                <br>
                Following is the Log Message Count:<br>                <b>DEBUG -> 10<br></b><b>INFO -> 10<br></b><b>WARNING -> 10<b
r></b><b>ERROR -> 10<br></b><b>CRITICAL -> 10<br></b>            </p>
            </body>
            </html>

26-Dec-19 11:26:11 - Email Sent!!
