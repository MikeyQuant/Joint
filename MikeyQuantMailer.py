import pandas as pd
from datetime import datetime
from datetime import timedelta
from yahoo_earnings_calendar import YahooEarningsCalendar
from yahoo_fin.stock_info import *
import dateutil.parser
import os
import pandas_datareader.data as web
import ezgmail
import streamlit as st
def email():
    ezgmail.init()
    DAYS_AHEAD=1
    start_date = datetime.now().date() + timedelta(days=DAYS_AHEAD)
    end_date = (datetime.now().date() + timedelta(days=DAYS_AHEAD))

    # downloading the earnings calendar
    yec = YahooEarningsCalendar()
    earnings_list = yec.earnings_between(start_date, end_date)
    print(earnings_list)
    # saving the data in a pandas DataFrame
    earnings_df = pd.DataFrame(earnings_list)
    print(earnings_df["startdatetime"])
    earnings_df["startdatetime"]= earnings_df['startdatetime'].astype(str).str[:-14]
    earnings_df["Link"]="https://finance.yahoo.com/quote/{}".format(earnings_df["ticker"])
    for index, x in enumerate(earnings_df["ticker"]):
        earnings_df["Link"][index]="https://finance.yahoo.com/quote/{}".format(x)
    print(earnings_df["startdatetime"])
    print(earnings_df)
    earnings_df.to_csv( r"C:\Users\MIKEB\Desktop\Python\Fuhnance\Earnings_For_{}.csv".format(start_date))
    e,g,l=generate_dfs(10)
    msg="Top Gainers Today:\n\n"
    for index,x in enumerate(g["Symbol"]):
        try:
            line=f"{x} | {g['Name'][index]} | {g['% Change'][index]}% | https://finance.yahoo.com/quote/{x}\n\n"
            msg=msg+line
        except:
            pass
        print(msg)
    msg=msg+"\n\nTop Losers Today:\n\n"
    for index,x in enumerate(l["Symbol"]):
        try:
            line=f"{x} | {l['Name'][index]} | {l['% Change'][index]}% | https://finance.yahoo.com/quote/{x}\n\n"
            msg=msg+line
        except:
            pass
    msg=msg+"\n\nEarnings Action Today:\n\n"
    for index,x in enumerate(e["ticker"]):
        line=f"{x} | {e['companyshortname'][index]} | {e['startdatetimetype'][index]} | {round(e['% Change'][index],2)}% | https://finance.yahoo.com/quote/{x}\n\n"
        msg=msg+line
    print(msg)
    #for x in ["Thompso_evan@bentley.edu","decrescenzomatt@gmail.com","Arthur.zhou@woosternet.org","pitardr4@gmail.com","mikebell180@gmail.com"]:
    for x in ["jake@jakeoconnell.com","willy_hodgson@yahoo.com","bscammett@gmail.com","devito_jake@bentley.edu","Pdntpdnt@gmail.com","Robnraymond@gmail.com","kjwalker2798@gmail.com","dvstrongin@gmail.com","sepich_matt@bentley.edu","mrsepich@gmail.com","Thompso_evan@bentley.edu","decrescenzomatt@gmail.com","Arthur.zhou@woosternet.org","pitardr4@gmail.com","mikebell180@gmail.com"]:
        ezgmail.send(x,"Gainers, Losers, and Earnings {}".format(start_date),msg,r"C:\Users\MIKEB\Desktop\Python\Fuhnance\Earnings_For_{}.csv".format(start_date))




def generate_dfs(num_gl):

    start_date = datetime.now().date()
    end_date = datetime.now().date()
    gainers=get_day_gainers()
    topg=gainers.nlargest(num_gl,"% Change")
    topg=topg.drop(columns=["Price (Intraday)","Change","Volume","Avg Vol (3 month)"])

    losers=get_day_losers()
    topl=losers.nsmallest(num_gl,"% Change")
    topl=topl.drop(columns=["Price (Intraday)","Change","Volume","Avg Vol (3 month)"])
    #try:
    yec = YahooEarningsCalendar()
    earnings_list = yec.earnings_between(start_date, end_date)
    earnings_df = pd.DataFrame(earnings_list)
    earnings_df["% Change"]=""
    earnings_df["Current Price"]=""
    earnings_df["Previous Close"]=""
    earnings_df=earnings_df.drop(columns=["epsestimate","epsactual","epssurprisepct","startdatetime","timeZoneShortName","gmtOffsetMilliSeconds","quoteType"])
    for index, x in enumerate(earnings_df["ticker"]):
        try:
            earnings_df["Previous Close"][index]=get_quote_table(x , dict_result = True)["Previous Close"]
            earnings_df["Current Price"][index]=get_live_price(x)
            earnings_df["% Change"][index]=100*((earnings_df["Current Price"][index]-earnings_df["Previous Close"][index])/earnings_df["Previous Close"][index])
        except:
            pass
    earnings_df=earnings_df.dropna().sort_values(by="% Change",ascending=False)
    #except:
     #   earnings_df=pd.DataFrame
    return earnings_df , topg,topl
#email()
st.title("Stock Dashboard")

e,g,l=generate_dfs(100)

try:
    st.title("Declaring Earnings Today: ")
    st.dataframe(e)

except:
    pass
st.title("Day Gainers")
st.dataframe(g)

st.title("Day Losers")
st.dataframe(l)
