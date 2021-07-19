from selenium import webdriver
from bs4 import BeautifulSoup
import smtplib
import schedule, time

url = 'https://www.amazon.com/Apple-EarPods-3-5mm-Headphone-Plug/dp/B06X16Z7DZ/ref=sr_1_2_sspa?dchild=1&keywords=earpods&qid=1626660973&sr=8-2-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUE5UURISlJVRThHUDAmZW5jcnlwdGVkSWQ9QTA0OTcyOTgxRVRIWExVMU4wSVFVJmVuY3J5cHRlZEFkSWQ9QTA1Nzk4NDkxNzZVMUdUWFU5VEY1JndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ=='
ini_price = 14.49
title = ''

def send_mail(username, pw):
    # Ensure valid inputs get processed as strings
    username_str = str(username)
    pw_str = str(pw)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(username_str, pw_str)

    subject = 'Price for "' + title + '" has dropped!'
    body = 'Check the Amazon link: ' + url
    msg = f'Subject: {subject}\n\n{body}'
    
    server.sendmail(
        username_str, # from
        username_str, # to
        msg
    )

    print('Email has been sent!')
    server.quit()

def check_price():
    global title
    # these options are to stop the invalid errors from chromedriver from clogging logs
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    html = driver.page_source
    driver.close()

    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find('span', {'id': 'productTitle'}).text.strip()
    price = soup.find('span', {'id': 'priceblock_ourprice'}).text
    converted_price = float(price[1:])

    if converted_price == ini_price:
        send_mail('austinaimhigh@gmail.com', 'Blaze884r*procsetor')

def job():
    print("I'm working...")
    check_price()

schedule.every().day.at("12:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60 * 60) # hour
