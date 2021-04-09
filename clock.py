from bs4 import BeautifulSoup
import requests
from datetime import date
import pyrebase
import apscheduler
from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()



config = {
    "apiKey": "AIzaSyAJDxFPg_oQHvQnUsAF_t9ytSqjU1YuhBU",
    "authDomain": "analysis-598e0.firebaseapp.com",
    "databaseURL": "https://analysis-598e0-default-rtdb.firebaseio.com",
    "projectId": "analysis-598e0",
    "storageBucket": "analysis-598e0.appspot.com",
    "messagingSenderId": "216359052416",
    "appId": "1:216359052416:web:f4705f3df8da261a91b265",
    "measurementId": "G-KL4VK6P7C1"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

def getdata(url):
    r = requests.get(url)
    return r.text

def data(petrolurl):
    htmldata = getdata(petrolurl)
    soup = BeautifulSoup(htmldata, 'html.parser')
    result = soup.find_all("div", class_="gold_silver_table")
    mydatastr = ''
    result = []

    for table in soup.find_all('tr'):
        mydatastr += table.get_text()
    
    mydatastr = mydatastr[1:]
    itemlist = mydatastr.split("\n\n")
    
    for item in itemlist[:-5]:
        result.append(item.split("\n"))
    reqnew=[]
    req = result[1:15]
    for each in req:
        reqnew.append(each[:2])
    return reqnew
petrolurl = "https://www.goodreturns.in/petrol-price.html"
dieselurl = "https://www.goodreturns.in/diesel-price.html"

def insert(today):
    petroldata = data(petrolurl)
    dieseldata = data(dieselurl)
    for each in petroldata:
        db.child(today).child(each[0]).update({"petrol":each[1]})
    for each in dieseldata:
        db.child(today).child(each[0]).update({"diesel":each[1]})
    return True

@sched.scheduled_job('interval', hours = 10)
def initiate():
    today = date.today()
    var = insert(today)
    if var:
        print('success')
sched.start()
