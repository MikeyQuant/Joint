import pandas as pd
import streamlit as st
import pydeck as pdk
mbapi="sk.eyJ1IjoibWlrZXlxdWFudCIsImEiOiJja2lqN2pvMGgwZHdyMnZxcmF2cHF4ZGR0In0.pBJ7Tv-oTyWSAd_V1SOpQw"

def sl():
    df=pd.read_csv('LeviaDeliveriesFB.csv')
    view=pdk.ViewState(latitude=df["lat"].mean(),longitude=df["lon"].mean(),pitch=20,zoom=9)
    column_layer = pdk.Layer("ColumnLayer",data=df,get_position=["lon", "lat"],get_elevation="Cases",elevation_scale=25,radius=500,pickable=True,auto_highlight=True,)

    tooltip = {"html": "<b>{Dispensary}</b>  Rev: <b>{Revenue}</b> Cases:{Cases} Flavors: Celebrate-{Celebrate} Dream-{Dream} Achieve:{Achieve}","style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"}}

    arc_layer_map=pdk.Deck(map_style='mapbox://styles/mapbox/light-v10',layers=[column_layer],initial_view_state=view,mapbox_key=mbapi,tooltip=tooltip)

    data=df.to_dict()
    print(data)
    st.header("Column Map (Height determined by # of cases)")
    st.pydeck_chart(arc_layer_map)
def next_closest():
    df=pd.read_csv("LeviaDeliveriesFB.csv")
    df=pd.read_csv("FBmatrix.csv")

    for index,x in enumerate(df["Distance"]):

        df["Duration"][index]=df["Duration"][index].replace("hours","hour").replace("min","mins")
        try:
            df["Duration"][index]=(int(df["Duration"][index].split(" hour ")[0])*60)+int(df["Duration"][index].split(" hour ")[1].split(" mins")[0])
        except:
            df["Duration"][index]=int(df["Duration"][index].split(" mins")[0])
    dis=df
    df=pd.read_csv("LeviaDeliveriesFB.csv")
    df["Next Closest"]=""
    df["Second Closest"]=""

    index=0
    for name,add in zip(df["Dispensary"], df["Address"]):
        print(name,add)
        dis1=dis[dis["Ad1"]==add].reindex()
        dis1["I"]=[i for i in range(0,len(dis1),1)]



        max=99999999999
        maxd=[]
        for index2,d,ad2 in zip(dis1["I"],dis1["Duration"],dis1["Ad2"]):
            print(d)
            if add==ad2 or d==1:
                print(add,ad2)
                pass
            else:
                if int(d)<max:


                    name2= [n for n,a in zip(df["Dispensary"],df["Address"])if a==ad2]
                    maxd.append(name2)
                    print(ad2)
                    max=d
        try:
            df["Next Closest"][index]=name2[0]


        except:
            pass
        index+=1
    print(df)
    st.title("First Batch Orders")
    st.write("The last column contains the next closest dispensary")
    st.dataframe(df)
def matrix():
    st.title("Distance Matrix")
    df=pd.read_csv("FBmatrix.csv")
    st.dataframe(df)
next_closest()



sl()
matrix()
