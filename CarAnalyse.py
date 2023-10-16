import pandas as pd
import numpy as np
import mysql.connector
import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
class Analyse:
    def __init__(self):
        connection=mysql.connector.connect(host="localhost",user="root",password="vm3cbm0m",database="ikincieloto")
        self.df=pd.read_sql_query("SELECT * FROM ikincieloto.arabamcom1",connection)
        for i in range(len(self.df["Fiyat"])): 
           self.df["Fiyat"][i]=self.df["Fiyat"][i].replace(".","")
        self.df["Fiyat"]=self.df["Fiyat"].astype("int")
        self.df["İlanGünü"]=self.df.VeriTarihi
        self.df["Month"]=pd.DatetimeIndex(self.df["VeriTarihi"]).month
        print(self.df["Month"])
        self.df["Marka/Seri"]=self.df["Marka"]
        for i in range(len(self.df["İlanGünü"])):   
         self.df["İlanGünü"][i]=(self.df.VeriTarihi[i].day-self.df.İlanTarihi[i].day)+(self.df.VeriTarihi[i].month-self.df.İlanTarihi[i].month)*30+(self.df.VeriTarihi[i].year-self.df.İlanTarihi[i].year)*365
         self.df["Marka/Seri"][i]=self.df["Marka"][i]+" "+self.df["Seri"][i]
    def addlabel(self,x,y):
      a=x.values.tolist()
      l=0
      for i in a:
       self.axes.text(l,i,str("{0:.2f}".format(i)))
       l=l+1  
    def ilananalyse(self):
        ilannumber=self.df[self.df["VeriTarihi"]>datetime.date(2023,9,1)].groupby(["Marka","Seri"])["Fiyat"].count().sort_values(ascending=False).head(10)
        labels=ilannumber.index.tolist()
        plt.subplot(221)
        ilannumber.plot(kind="pie",title="Car Model Based Frequency",autopct='%.1f%%',wedgeprops={'linewidth': 3.0, 'edgecolor': 'white'},textprops={'fontsize':9})
        plt.gca().set_ylabel(" ")
        #pie=plt.pie(ilannumber,labels=labels,autopct='%.1f%%',textprops={'fontsize':9})
        #plt.tight_layout()
        #plt.subplot2grid((2,2),(0,0))
        #plt.tight_layout()
        #############
        price_change=self.df.groupby(["Month"])["Fiyat"].agg(np.mean)
        #print(price_change)
        plt.subplot(222)
        #hist=plt.bar(price_change)
        price_change.plot(kind="bar",title="Average Price by Months")
        current_values=plt.gca().get_yticks()
        plt.gca().set_yticklabels(["{:,.0f}".format(x) for x in current_values])
        ax=price_change.plot.bar()
        ax.bar_label(ax.containers[0],labels=["{:,.0f}".format(x) for x in ax.containers[0].datavalues])
        #ax.set_ylabel(" ")
        #plt.subplot2grid((2,2),(0,1))
        #plt.tight_layout()
        #plt.legend()
        ############
        advertday=self.df.groupby(["Marka/Seri"])["İlanGünü"].agg(np.mean).sort_values(ascending=False).head(10)
        plt.subplot(223)
        advertday.plot(kind="bar",title="Longest Advert Day Analyse",color="y")
        current_values=plt.gca().get_yticks()
        plt.gca().set_yticklabels(["{:.0f}".format(x) for x in current_values])
        self.axes=advertday.plot.bar()
        self.axes.tick_params(axis="x",direction="in",labelsize="x-small",rotation=55)
        # current_valuesx=plt.gca().get_xticks()
        # plt.gca().set_xticklabels()
        self.addlabel(advertday,1)
        ############
        pricemodelchange=self.df[(self.df["Marka"]=="Renault") & (self.df["Seri"]=="Clio")].groupby(["Month"])["Fiyat"].agg(np.mean)
        plt.subplot(224)
        pricemodelchange.plot(kind="line")
        plt.title("Renault Clio Price Changes By Month",y=1,pad=-14)
        axx=pricemodelchange.plot.line()
        axx.xaxis.set_major_locator(MultipleLocator(1))

        # current_values=plt.gca().get_yticks()
        # plt.gca().set_yticklabels(["{:,.0f}".format(x) for x in current_values])
        # x=pricemodelchange.index.tolist()
        # y=0
        # for i in x:
        #    x[y]=int(i)
        #    y=y+1
        # default_x_ticks=range(len(x))
        # print(x)
        # plt.xticks(default_x_ticks,x)
        manager = plt.get_current_fig_manager()
        manager.full_screen_toggle()
        plt.show()
        #print(ilannumber)
        
    def analyse(self,Marka,Seri):
        advertbymodel=self.df[self.df["Marka"]==Marka].groupby(["Marka","Seri"])["Fiyat"].count().sort_values(ascending=False).reset_index().values[0]
        pricemodel=self.df[(self.df["Marka"]==Marka)&(self.df["Seri"]==Seri)].groupby(["Marka","Seri","Renk"])[("Fiyat","İlanGünü")].agg([np.mean]).reset_index().round(2)
        pricevariation=self.df[(self.df["Marka"]==Marka)&(self.df["Seri"]==Seri)].groupby(["ilanID","VeriTarihi"]).agg([np.max]).reset_index()
        np.set_printoptions(suppress=True)
        gün=self.df[(self.df["Marka"]==Marka)&(self.df["Seri"]==Seri)].groupby(["ilanID","Marka","Seri","Renk","KM","Yıl"])["İlanGünü"].agg(np.max).sort_values(ascending=False)
        ilangunu=self.df[(self.df["Marka"]==Marka)&(self.df["Seri"]==Seri)].sort_values(by=["İlanGünü"],ascending=False)
        #print(advertbymodel)
        #print(gün)
        #print(pricemodel)
        # print(pricevariation)
        #print(ilangunu)
a=Analyse()
# a.analyse("Ford","Focus")
a.ilananalyse()