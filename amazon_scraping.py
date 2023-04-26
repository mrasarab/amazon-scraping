import requests
from bs4 import BeautifulSoup
import smtplib
import secrets
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
load_dotenv()

URL = os.getenv('my_shoes')

headers = {
    'user-agent': os.getenv('user-agent')}

page = requests.get(URL,headers = headers)
soup = BeautifulSoup(page.content,'html.parser')

product_price = soup.find(class_='a-price-whole').get_text()
product_title = soup.find(id='productTitle').get_text()
product_price1 = (product_price)[0:2]


def price_check():
    if int(product_price1)>34 :
        email_sender = os.getenv('email_sender')
        msg = MIMEMultipart()
        msg["subject"] = "schuhe"
        msg["from"] = email_sender
        msg["to"] = email_sender
        msg.attach(MIMEText("the price of shoe is below 34 euro"))
        server = smtplib.SMTP(os.getenv('Smtp_server'), 25)
        server.starttls()
        server.login(os.getenv('Smtp_Username'),os.getenv('Smtp_Password'))
        text = msg.as_string()
        server.sendmail(email_sender,email_sender, text)
        server.quit()
    
if __name__ =="__main__":
    price_check()



