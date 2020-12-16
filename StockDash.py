from datetime import datetime
from datetime import timedelta
from yahoo_earnings_calendar import YahooEarningsCalendar
from yahoo_fin.stock_info import *
import streamlit as st
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
