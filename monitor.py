import time
import requests
import smtplib
import bs4

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
        server = smtplib.SMTP("mail.alexanderlao.com", 26) #establishes connection to server
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
        url = "https://www.mrporter.com/en-us/mens/adidas_originals/gazelle-suede-sneakers/721301" #url to be examined
        refresh_time = 5

        user = "exampleuser" #Username of sender
        pwd = "examplepw" #Password of sender

        recipient = "lao.alex97@gmail.com" #Recipient of email when update is made
        subject = "SITE HAS CHANGED!"
        body = "Change At " + str(url)

        page1=c.get(url) #retrieves information of the page for the first time
        #Comment out next two lines if you wish to compare the whole page. Otherwise it's compare a section.
        soup1 = bs4.BeautifulSoup(page1.content)
        divs1 = soup1.findAll("div", {"class":"product-size-selection select-option-style__container threeSelectionItems  js-size-select" }) #change parameters to specific section/element you want to focus in on

        time.sleep(refresh_time)

        page2=c.get(url) #after a wait, it retrieves information of a page again
        #See comment about regarding this section
        soup2 = bs4.BeautifulSoup(page2.content)
        divs2 = soup2.findAll("div", {"class":"product-size-selection select-option-style__container threeSelectionItems  js-size-select" })
        #if uncomment below line and comment out "dives1==divs2" line if you want to check overall page
        #if page1.content == page2.content:
        if divs1 == divs2:
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