## To run this scirpt: /home/linxy29/code/Others/.conda/bin/python /home/linxy29/code/Others/csf_signup.py

from urllib.request import urlopen 
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import schedule
import time

def check_slots():
    # Get the webpage content
    html = urlopen("https://fcbooking.cse.hku.hk/")
    html_text = bytes.decode(html.read())
    soup = BeautifulSoup(html_text, 'html.parser')
    b_active_section = soup.find('div', {'id': 'c10002Content'})
    slots = b_active_section.find_all('div', class_='border-top border-light font-size-list')
    
    available_slots = []
    for slot in slots:
        time_div = slot.find('div', class_='col text-center')
        availability_div = time_div.find_next_sibling('div')
        if "FULL" not in availability_div.get_text():
            available_slots.append(time_div.get_text())

    if available_slots:
        # Prepare the email
        sender_email = "forsdemail@163.com"
        recipient_email = "xl2836@outlook.com"
        subject = "Available Slots in HKU B-Active"
        body = f"Available slots: {', '.join(available_slots)}"

        msg = MIMEText(body)
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Send the email
        with smtplib.SMTP_SSL('smtp.163.com', 465) as server:
            server.login(sender_email, "GEQRHYVMTTIGIYKU")
            server.sendmail(sender_email, recipient_email, msg.as_string())

# Schedule the function to run every 30 minutes from 6am to 11:59pm
schedule.every(30).minutes.do(check_slots).tag('slot_checking')

# Start the schedule
while True:
    current_hour = int(time.strftime('%H'))
    if 6 <= current_hour <= 23:  # Check if current time is between 6am to 11:59pm
        schedule.run_pending()
    time.sleep(60)  # Sleep for 60 seconds before checking the schedule again
