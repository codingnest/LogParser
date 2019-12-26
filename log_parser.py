import argparse, logging, re, smtplib, configparser
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def level_count(read_FH, write_FH):
    '''
    Method will Extract all the Messages with Logging Level as 'Critical' and 'Error'
    and generate extract_log.txt file
    It will return dictionary with all the logging levels and it's count
    return: Dictionary
    '''
    loglevel_count = {}
    for line in read_FH:
        if re.search('DEBUG',line):
            if 'DEBUG' in loglevel_count:
                loglevel_count['DEBUG'] += 1
            else:
                loglevel_count['DEBUG'] = 1

        if re.search('INFO', line):
            if 'INFO' in loglevel_count:
                loglevel_count['INFO'] += 1
            else:
                loglevel_count['INFO'] = 1

        if re.search('WARNING', line):
            if 'WARNING' in loglevel_count:
                loglevel_count['WARNING'] += 1
            else:
                loglevel_count['WARNING'] = 1

        if re.search('ERROR', line):
            write_FH.write(line)
            if 'ERROR' in loglevel_count:
                loglevel_count['ERROR'] +=1
            else:
                loglevel_count['ERROR'] = 1

        if re.search('CRITICAL', line):
            write_FH.write(line)
            if 'CRITICAL' in loglevel_count:
                loglevel_count['CRITICAL'] += 1
            else:
                loglevel_count['CRITICAL'] = 1

    return loglevel_count

def config_reader(filepath = None):
    '''
    Method parses config file, return dictionary of all the sections
    return: dictionary
    '''
    dict_option = {}
    config = configparser.ConfigParser()
    config.read(filepath)
    sections = config.sections()
    options = config.options(sections[0])
    for option in options:
        try:
            dict_option[option] = config.get(sections[0], option)
            if dict_option[option] == -1:
                logger.error("Please check Threshold Configuration File")
        except:
            dict_option[option] = None
    return dict_option

def send_mail(user, password, to_list, subject, body, files = []):
    '''
    Method sends mail to List of users using GMAIL credentials
    '''
    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = ",".join(to_list)
    msg['Subject'] = subject

    msg_body = MIMEText(body, 'html')
    msg.attach(msg_body)

    for f in files:
        with open(f, "rb") as infile:
            part = MIMEApplication(
                infile.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename={}'.format(basename(f))
        msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(user, password)
        server.sendmail(user, ",".join(to_list), msg.as_string())
        server.quit()
        logger.info("Email Sent!!")
    except Exception as e:
        logger.error("Error: {}".format(e))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    requiredNamed = parser.add_argument_group('Required Named arguments')
    requiredNamed.add_argument('-e', '--email', dest='email_id', required=True,
                               type=str, nargs='+')
    args = parser.parse_args()

    # Logger Configuration
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    fileHandler = logging.FileHandler(filename='app.log')  # Relative Path
    fileHandler.setFormatter(formatter)
    logger.setLevel(level=logging.DEBUG)  # Logging Level

    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)

    # read Gmail UserName and Password from config File
    dict_config = config_reader('config.ini')  # Relative Path

    loglevel_count = {}
    try:
        with open('error_log.txt') as infile: #Relative Path
            with open('extract_log.txt','w') as outfile: #Relative Path
                loglevel_count = level_count(infile,outfile)
    except Exception as e:
        logger.error("File Exception {}".format(e))

    logger.debug("Log Level Count: {}".format(loglevel_count))
    msg_body = '''\
        <html>
            <head></head>
            <body>
                <p>Hey {},<br>
                <br>
                Following is the Log Message Count:<br>\
                '''.format(",".join(args.email_id))
    for key in loglevel_count:
        msg_body += "<b>"+key+" -> "+str(loglevel_count[key])+"<br></b>"

    msg_body += '''\
            </p>
            </body>
            </html>
            '''
    logger.debug("Message Body {}".format(msg_body))
    send_mail(dict_config['gmail_user'], dict_config['gmail_password'], args.email_id,
              'Log Parser Results', msg_body, files=['extract_log.txt'])