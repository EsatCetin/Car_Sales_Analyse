from bs4 import BeautifulSoup
import json
import os
import pandas as pd
import requests
import mysql.connector
from datetime import datetime
from selenium import webdriver
import urllib.request
import html5lib
from datetime import datetime
class Arabamcom:
    def __init__(self):
      self.connection=mysql.connector.connect(host="localhost",user="root",password="vm3cbm0m",database="ikincieloto")
      #As main structure , Open the database automatically
      self.cursor=self.connection.cursor() 
      self.dict={"Ocak":"1","Şubat":"2","Mart":"3","Nisan":"4"
                 ,"Mayıs":"05","Haziran":"6","Temmuz":"7","Ağustos":"8","Eylül":"9","Ekim":"10","Kasım":"11","Aralık":"12"}
      #to identify calendar by the name of months , we have created a dictionary of calenders
    def collectdata(self):
         user_agent={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.3"}
         #For webscrapping , I use User_agent method.
         page=51
         #Number of pages in the website
         now=datetime.now()#Data's date to keep track of the changes on prices
         ozelik=[]
         self.urunlist=[]
         for i in range(1,page):#To take every pages data , i used for loop .Max page number is 50 
          self.response=urllib.request.Request("https://www.arabam.com/ikinci-el/otomobil?take=50&view=List&page="+str(i),headers=user_agent)
          self.url=urllib.request.urlopen(self.response)
          self.soup=BeautifulSoup(self.url,'html.parser')
          self.soup.prettify()

          liste=self.soup.find("table",{"id":"main-listing"}).find_all("tr")
          # from html page , we find necessary rows for web scraping
          for i in liste:
           #in the list of datas , with a loop we take data and clean them 
           a=i.get("id")
           
           if a==None:
              continue
           else:
              ozelik=[a.replace("listing","")]
              try:
               marka=i.find_all("td")
               y=0
               for x in marka:
                try:
                 if x.get("class")==["listing-text"]:
                   place=x.find("div",{"class":"fade-out-content-wrapper"}).text.strip().replace("\n"," ").replace("TL","").split()
                   #print(place)
                   if y==2:
                    ozelik.append("".join(place))
                   else:
                    ozelik+=place
                   y=y+1
                 elif x.get("class")==["listing-modelname","pr"]:
                   marka=x.text.strip().split()
                   if marka[1]=="-":
                    marka[1]=marka[2]
                    marka[2]=""
                   model=marka[0]
                   Seri=marka[1]
                   ozelik.append(model)
                   ozelik.append(Seri)
                   ozelik.append(" ".join(marka[2:]))
                 elif x.text.strip()=="":
                  
                   continue
                 else:
                    #print(x.get("class"))
                    if x.get("class")==["listing-text","tac"]:
                     
                     date=x.find("div",{"class":"fade-out-content-wrapper"}).text.strip().replace("\n"," ").replace("TL","").split()
                     #print(date)
                     date[1]=self.dict[date[1]]
                     #print(date[1])
                     #print(date)
                     x="-".join(date[::-1])
                     #print(x)
                     ozelik.append(x)
                    else:
                       y=x.text.strip().replace("\n"," ").replace("TL","").split()
                       ozelik.append(y[0])
                #at the end of the algorithm we create a list of necessary datas .
                except:
                  continue
              except:
               continue
           tar=datetime.now()
           ozelik.append(f"{tar.year}-{tar.month}-{tar.day}")
           #print(ozelik)
           if len(ozelik)==13:
            self.urunlist.append(ozelik)
           else:
             continue    
    def savetodatabase(self):
      #Datas that we collect should be saved in a database so we insert these datas in a precreated MySQL database
      self.collectdata()
      insert="INSERT into arabamcom1(İlanID,Marka,Seri,Model,Açıklama,Yıl,KM,Renk,Fiyat,İlanTarihi,İL,İLÇE,VeriTarihi) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
      self.cursor.executemany(insert,self.urunlist)
      try:
         self.connection.commit()
      except mysql.connector.Error as err:
            print("Hata:",err)
      self.connection.close()

a=Arabamcom()
a.savetodatabase()

