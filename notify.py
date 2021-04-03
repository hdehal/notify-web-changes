# See also:
# https://stackoverflow.com/q/61036457
# https://stackoverflow.com/a/24077717
# https://www.crummy.com/software/BeautifulSoup

import requests
from bs4 import BeautifulSoup
import re
import time
import smtplib
from email.mime.text import MIMEText

# URL of webpage you want to check
url = 'https://example.com'

headers = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

while True:
    # Download the webpage (first request)
    response = requests.get(url, headers=headers)

    # Parse and grab all text
    soup = BeautifulSoup(response.text, "lxml")

    # Find specific string to monitor for changes (e.g. "full")
    vaccine_sites = soup.findAll(string=re.compile("full"))
    print("Found string: " + str(vaccine_sites))

    # Wait 5 minutes
    time.sleep(300)

    # Download the webpage again (subsequent requests)
    soup = BeautifulSoup(requests.get(url, headers=headers).text, "lxml")

    # Compare requests for diff/changes
    if soup.findAll(string=re.compile("full")) == vaccine_sites:
        print('Vaccine appointments still full, retrying...')
        continue

    else:
        # Send email if diff/changes found
        msg_content = "{url}".format(url=url)
        message = MIMEText(msg_content, 'html')
        message['Subject'] = 'Vaccine appointments available!'
        msg_full = message.as_string()
        server = smtplib.SMTP('smtp.example.com:587')
        server.starttls()
        server.login('from@example.com', 'password')
        # Tip: Use your mobile provider's email-to-sms service to message yourself instantly without an SMS/API gateway
        # from, to
        server.sendmail('from@example.com', 'to@example.com', msg_full)
        server.quit()