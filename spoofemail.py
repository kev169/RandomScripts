import smtplib

def message():
    messageContent = raw_input(">>>").strip()
    return messageContent

if __name__ == "__main__":
    print("Welcome")
    server = raw_input("IP:")
    client = smtplib.SMTP(server)
    client.set_debuglevel(1)
    fromemail = raw_input("From:")
    toemail = raw_input("To:")
    subject = raw_input("Subject:")
    messagecont = message()
    messagestring = string.join(("From: %s" % fromemail,
			"To: %s" % toemail,
			"Subject: %s" % subject,
			"",
			messagecont
			),"\r\n")
    client.sendmail(fromemail,[toemail], messagestring)
    client.quit()

