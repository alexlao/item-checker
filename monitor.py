import time
import requests
import smtplib

from timeit import default_timer as timer

start = timer()

#Function to send the email to a recipient when a change on a site is made.
#When using this script, the user must update the server being used with the new emails respective information.
def alert_email(user, pwd, recipient, subject, body):
    sender = user
    senderpwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Makes the message object
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    #Tries to send an email to a recipient. If any error is thrown when attempting, it is caught.
    try:
        server = smtplib.SMTP("mail.example.com", 26) #establishes connection to server
        server.ehlo()
        server.starttls()
        server.login(sender, senderpwd)  # login to gmail server
        server.sendmail(FROM, TO, message)  # actually perform sending of mail
        server.close()  # end server
        print 'successfully sent the mail'  # alert user mail was sent
    except Exception as e:  # else tell user it failed and why (exception e)
        print "failed to send mail, " + str(e)

#Main method runs indefinitely, until the user ends the script.
#Checks if page has been updated
def main():
    with requests.Session() as c:
        url = "http://www.ExampleAddress.com/" #url to be examined
        refresh_time = 5

        user = "sender@example.com" #Username of sender
        pwd = "examplePWD!" #Password of sender

        recipient = "example@example.com" #Recipient of email when update is made
        subject = "Site change"
        body = "Change At " + str(url)

        page1=c.get(url) #retrieves information of the page for the first time

        time.sleep(refresh_time)

        page2=c.get(url) #after a wait, it retrieves information of a page again

        #if pages are the same, nothing happens
        if page1.content == page2.content:
            end = timer()
            if((end-start))>=60:
                timeMinutes = (end-start)/60
                print "No change detected @ " + str(url) + " Elapsed time: " + str(timeMinutes) +" minutes"
            else:
                print "No change detected @ " + str(url) + " Elapsed time: " + str((end-start)) + " seconds"

        #if pages are different, then an email is sent to the recipient
        else:
            end = timer()
            if int((end-start))>=60:
                timeMinutes = (end-start)/60
                print "Change Detected @ " + str(url) + " Elapsed time " + str(timeMinutes)
            else:
                print "Change Detected @ " + str(url) + " Elapsed Time " + str((end-start))

            alert_email(user, pwd, recipient, subject, body)

        page2 = None
        main()

if __name__ == "__main__":
    main()