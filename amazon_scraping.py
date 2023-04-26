import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

# Get the URL of the product to monitor from the environment variables
URL = os.getenv('my_shoes')

# Set the user-agent header to avoid being blocked by the website
headers = {
    'user-agent': os.getenv('user-agent')
}

# Send a GET request to the product page and parse the HTML content
page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')

# Extract the title and price of the product
product_price = soup.find(class_='a-price-whole').get_text()
product_title = soup.find(id='productTitle').get_text()

# Extract the first two digits of the price to check against the threshold
product_price1 = (product_price)[0:2]

# Function to check the product price and send an email if it is below a certain threshold
def price_check():
    # Check if the product price is below 34 euros
    if int(product_price1) > 34:
        # Set up the email message with the necessary details
        email_sender = os.getenv('email_sender')
        msg = MIMEMultipart()
        msg["subject"] = "schuhe"
        msg["from"] = email_sender
        msg["to"] = email_sender
        msg.attach(MIMEText("the price of shoe is below 34 euro"))
        
        # Set up the SMTP server and send the email
        server = smtplib.SMTP(os.getenv('Smtp_server'), 25)
        server.starttls()
        server.login(os.getenv('Smtp_Username'), os.getenv('Smtp_Password'))
        text = msg.as_string()
        server.sendmail(email_sender, email_sender, text)
        server.quit()

# Check the product price and send an email if it is below the threshold
if __name__ == "__main__":
    price_check()
