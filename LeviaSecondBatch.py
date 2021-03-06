
import pandas as pd
import streamlit as st
import pydeck as pdk
mbapi="sk.eyJ1IjoibWlrZXlxdWFudCIsImEiOiJja2lqN2pvMGgwZHdyMnZxcmF2cHF4ZGR0In0.pBJ7Tv-oTyWSAd_V1SOpQw"
import os

def sl():
    for i,b in enumerate(["G"]):
        if i==0:

            st.title("First Batch")
        #if i==1:
            #st.title("Second Batch")
        try:
            for x in range(0,10,1):
                dfd1=pd.read_csv("{}Bdetails-{}.csv".format(b,x))

                dfm1=pd.read_csv(f"{b}BdelivMap-{x}.csv")
                #dfm2=pd.read_csv(f"SBdelivMap-{x}.csv")
                #print(dfd1,dfd2,dfm1,dfm2)
                print(dfd1)
                for index,a in dfd1.iterrows():
                    for index2,y in enumerate(a):
                        if index2==1:
                            print(y,index2)
                            if index==0:
                                st.write(f"Route #{a[index2]}")
                            if index==1:
                                st.write(f"Total cost: ${a[index2]}")
                            if index==2:
                                st.write("Total hours: {}".format(a[index2]))
                            if index==3:
                                st.write("Route: {}".format(a[index2]))

                df=dfm1
                view=pdk.ViewState(latitude=df["from_lat"].mean(),longitude=df["from_lon"].mean(),pitch=20,zoom=9)

                arc_layer=pdk.Layer("ArcLayer",data=df,get_source_position=["from_lon","from_lat"],get_target_position=["to_lon","to_lat"],get_width=5,get_tilt=15,get_source_color=[255,165,0,80],get_target_color=[128,0,128,80])
                #dfc=generate_sales_map_df()
                dfc=pd.read_csv("LeviaDeliveriesFB2.csv")
                column_layer = pdk.Layer("ColumnLayer",data=dfc,get_position=["lon", "lat"],get_elevation="Cases",elevation_scale=50,radius=250,pickable=True,auto_highlight=True,)

                tooltip = {"html": "<b>{Dispensary}</b>  Rev: <b>${Revenue}</b> Cases:{Cases} ","style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"}}

                arc_layer_map=pdk.Deck(map_style='mapbox://styles/mapbox/light-v10',layers=[arc_layer,column_layer],initial_view_state=view,mapbox_key=mbapi,tooltip=tooltip)
                arc_layer_map.to_html("First_Batch_Sales_Map.html")
                data=df.to_dict()
                print(data)
                st.pydeck_chart(arc_layer_map)
        except:
            pass
sl()
