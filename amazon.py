import requests
import re
import smtplib
import time
from bs4 import BeautifulSoup

url=input("Enter the url of the Product:")
if(url==''):
   url="https://www.amazon.in/Hacking-Art-Exploitation-Jon-Erickson/dp/1593271441/ref=pd_sim_14_4/261-8826932-3814658?_encoding=UTF8&pd_rd_i=1593271441&pd_rd_r=714fd0b1-8935-41c5-9eb2-e7826d75460d&pd_rd_w=1sDBH&pd_rd_wg=DKepn&pf_rd_p=3ba80840-2950-4d64-ba61-c68a14bd0939&pf_rd_r=3E5ZB6VHNE1HGJ3226EG&psc=1&refRID=3E5ZB6VHNE1HGJ3226EG"

headers ={"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}

t_price=int(input("Enter the target price:"))
t=float(input("Enter the time interval in min:"))
def check_price(t_price):
        page = requests.get(url,headers=headers)

        soup=BeautifulSoup(page.content,'html.parser')
        #priceblock_ourprice
        title=soup.find(id="productTitle").get_text()
        try:
           price=soup.find(id="soldByThirdParty").get_text()
        except AttributeError:
           price=soup.find(id="priceblock_ourprice").get_text()
        
        i=price.index('.')
        cov_p=price[2:i+3]
        cov_pr=float((re.sub(",","",cov_p)))
        if(cov_pr<=t_price):
            sendemail(str(cov_pr),url)
        else:    
            print("Current price of the product is:",cov_pr)
        print("Book:",title.strip())

def sendemail(cov_pr,url):
         server=smtplib.SMTP("smtp.gmail.com",587)
         server.ehlo()
         server.starttls()
         server.ehlo()
         email=input("Enter email address:")
         passwd=input("Enter the password:")
         temail=input("Enter the email to send it to:")
         server.login(email,passwd)
         subject="Product Price's reduced to "+cov_pr
         body="check the link "+url
         msg=f"Subject:{subject}\n\n{body}"
         server.sendmail(email,temail,msg)
         print("Mail has been sent to the given email")
         server.quit()
while(True):
     check_price(t_price)
     time.sleep(t*60)
