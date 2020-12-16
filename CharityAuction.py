import streamlit as st
import pandas as pd
import ezsheets
from PIL import Image
def process_data():
    df=pd.read_csv("PortnoyAuctionItems.csv")
    auctions=pd.read_csv("Auctions.csv")
    for index,x in enumerate(auctions["auctionId"]):
        dff=df[df["auctionId"]==x]
        auctions["moneyRaised"][index]=sum(dff["currentBid"])
        auctions["itemsForAuction"][index]=len(dff)
    biddings=pd.read_csv("BiddingHistory.csv",index_col=0)
    return df,auctions,biddings
api="AIzaSyBD5kM1S1-yLP5GSwIT4xDIjItDr7Y4Yms"
"""SAMPLE_SPREADSHEET_ID = '1HhvS-I9wmNv2cgcQVAHVehofO_jdQZNcRnJGcp-YolI'
ss=ezsheets.Spreadsheet("Form Responses 1")
print(ss)"""
def create_auction(auctions):
    data={}
    email=st.text_input("Enter your email address:")
    cause=st.text_input("What is your charity or cause for raising money?")
    if len(email)>0:
        try:
            website=email.split("@")[1]
            com=website.split(".")[1]
            #cause=st.text_input("What is your charity or cause for raising money?")
        except:
            st.write("Type in a correct email address.")

    auctionid=auctions["auctionId"].max()+1
    if len(cause)>0 and len(email)>0:
        dict={"auctionId":auctionid,"charity":cause,"email":email,"itemsForAuction":0,"moneyRaised":0}
        dfn=pd.DataFrame(dict,index=[0])
        print(dfn.head())
        print(auctions.head())

        #print(dfn,auctions)
        auctions=pd.concat([auctions,dfn])
       # auctions=auctions.append(dfn)
        print(auctions)
        auctions.to_csv("Auctions.csv")
        """Your charity auction has been created!"""
    return auctions
def auctions():


    o=st.sidebar.radio("Main Menu",["View Auctions","Create Charity Auction","Auction an Item"])
    if o=="Create Charity Auction":
        df,auctions,biddings=process_data()
        auctions=create_auction(auctions)
    if o=="Auction an Item":
        df,auctions,biddings=process_data()
        st.sidebar.write("https://forms.gle/BEqc5YyiFJDrT2JAA")
    if o=="View Auctions":
       df,auctions,biddings=process_data()
       auction= st.sidebar.radio("Which Charity Auction would you like to see?",auctions["charity"])
       for index1,y in enumerate(auctions["charity"]):
            if auction==y:
                st.title(y)
                st.title(f"{auctions['itemsForAuction'][index1]} Items up for auction")
                st.title(f"${auctions['moneyRaised'][index1]} Dollars Raised")
                st.title(("Auction off an item: https://forms.gle/BEqc5YyiFJDrT2JAA"))
                sort=st.select_slider("Sort by bid Price",["Ascending","Descending"])
                if sort=="Ascending":
                    sort=True
                else:
                    sort=False
                print(sort)
                df=df.sort_values(by="currentBid",ascending=sort)
                print(df)
                auctionid=auctions["auctionId"][index1]
                for index,x in enumerate(df["auctionId"]):
                    if x==auctionid:
                        st.title(df["itemName"][index])
                        st.image(Image.open(df["picture"][index]))
                        cb=df["currentBid"][index]
                        st.title(f"Current Bid: ${cb}.00")
                        email=st.text_input(f"Enter email to bid ${cb+1}.00",key=f"{index}")
                        if len(email)>0:
                            try:
                                website=email.split("@")[1]
                                com=website.split(".")[1]
                                for index2,z in enumerate(biddings["itemId"]):
                                    if z==df["itemId"][index]:
                                        dfn=pd.DataFrame([z,cb,df["bidder"][index]]).transpose()
                                        biddings=pd.concat([biddings,dfn])
                                        biddings.to_csv("BiddingHistory.csv")


                                df["bidder"][index]=email
                                df["currentBid"][index]=cb+1

                                print(df)
                                df.to_csv("PortnoyAuctionItems.csv")
                                st.write("Refresh the page to see bid.")
                                break
                            except:
                                st.write("Please enter a valid email address.")

                st.title(("Auction off an item: https://forms.gle/BEqc5YyiFJDrT2JAA"))

                if len(email)>0:

                    break


auctions()
