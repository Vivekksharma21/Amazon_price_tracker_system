import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

def send_email(product_name, product_url):
    sender_email = "vivekrsashok@gmail.com"
    receiver_email = "vivekrsashok2002@gmail.com"
    password = "Vivek5@1234"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Price Drop Alert for {}".format(product_name)

    body = "The price of {} has dropped!\nCheck it out here: {}".format(product_name, product_url)
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)

def track_price(url, target_price):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    page = requests.get(url, headers=headers)
    
    if page.status_code != 200:
        print(f"Failed to retrieve page, status code: {page.status_code}")
        return

    soup = BeautifulSoup(page.content, "html.parser")

    product_title_elem = soup.find("span", {"id": "productTitle"})
    if product_title_elem:
        product_name = product_title_elem.get_text().strip()
    else:
        print("Product title element not found. Check the HTML structure or URL.")
        return

    product_price_elem = soup.find("span", {"class": "a-price-whole"})
    if product_price_elem:
        product_price = product_price_elem.get_text().strip()
        converted_price = float(product_price.replace(",", ""))
    else:
        print("Product price element not found. Check the HTML structure or URL.")
        return

    if converted_price <= target_price:
        send_email(product_name, url)
        print("Email sent for price drop!")

if __name__ == "__main__":
    product_url = "https://www.amazon.in/Xiaomi-inches-Ultra-Google-L43M8-A2IN/dp/B0CH33945T/ref=sr_1_1_sspa?dib=eyJ2IjoiMSJ9.ztqBt6CZHbxgxMgMdbLN9Gefh8UEfaWnoGnoEJfTf9cNqQ69_J02plYG0Wwk0kzq5CQbn2OkKIdr6JPC--7dOObtigScR_vpWTi5G9Zc_WCI_6bnKpxanrkHlk5kiLyrlIAYji5aD0TR5exygz6SA_tD8G5IgzKd-uVOmAJeMWJo-WHDOFjywt0FHf_NY-Sn7uhee_pG6CXw-pQsO5_Qb43X_wG1xaHug9U6LcHGOsLDZve4fo9y17IiQsUSjoN3ASEy2QdGOUlVccjk78JwwObtdUCrMHtd1fX8XhyQYWw.MmSw4r58Tuf2n9XSb54CtuLLdjM920kwsFav8BNb6v8&dib_tag=se&keywords=tv&qid=1718954797&s=electronics&sr=1-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1"
    target_price = 26200.0

    while True:
        track_price(product_url, target_price)
        time.sleep(86400)
