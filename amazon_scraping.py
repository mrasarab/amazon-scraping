import requests
from bs4 import BeautifulSoup
import smtplib
import secrets
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
load_dotenv()

URL = 'https://www.amazon.de/Puma-Unisex-Erwachsene-Sneaker-Schwarz-Black-Puma/dp/B077MLZ1KS/?_encoding=UTF8&pd_rd_w=9kY5p&content-id=amzn1.sym.0b0b934e-1f89-4d8b-9a61-672a3b20f8d0&pf_rd_p=0b0b934e-1f89-4d8b-9a61-672a3b20f8d0&pf_rd_r=J80QC5YZ30S0YZ3BB20V&pd_rd_wg=gH445&pd_rd_r=18906c67-c917-4443-acf0-1b1def1e0305&ref_=pd_gw_ci_mcx_mr_hp_atf_m&th=1&psc=1'

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}

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



