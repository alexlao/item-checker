import time
import requests
import smtplib
from timeit import default_timer as timer

start = timer()

def alert_email(user, pwd, recipient, subject, body):
    gmail_sender=user
    gmail_senderpwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)  # start smtp server on port 587
        server.ehlo()
        server.starttls()
        server.login(gmail_sender, gmail_senderpwd)  # login to gmail server
        server.sendmail(FROM, TO, message)  # actually perform sending of mail
        server.close()  # end server
        print 'successfully sent the mail'  # alert user mail was sent
    except Exception as e:  # else tell user it failed and why (exception e)
        print "failed to send mail, " + str(e)


def main():

    with requests.Session() as c
        url = "https://www.mrporter.com/en-us/mens/adidas_originals/gazelle-suede-sneakers/721301?ppv=2"
        refresh_time = 120
        user = "alexlaodevtests@gmail.com"
        pwd = "mxoi mpdo vmst engj"
        recipient = "lao.alex97@gmail.com"
        subject = "Site change"
        body = "Change At" + str(url)