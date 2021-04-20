import streamlit as st
import pandas as pd
import pydeck as pdk



def dispo_map():

        mbapi="pk.eyJ1IjoibWlrZXlxdWFudCIsImEiOiJja25rbDE0ODUwYWRpMnJwYjI0a25zc2FtIn0.XRafIAKi72faYbEMjYO5aw"
        df=pd.read_csv("MassDispoCords2.csv")
        df["red"]=0
        df["green"]=0
        df["blue"]=0
        for i,x in enumerate(df["approved_license_type"]):
                print(x)
                if x=="FINAL LICENSE":
                        print(x)
                        #df["blue"][i]=225
                        df["green"][i]=225
                else:
                        df["red"][i]=225
        print((df))
        view=pdk.ViewState(latitude=df["lat"].mean(),longitude=df["lon"].mean(),pitch=20,zoom=5)
        all_dispo = pdk.Layer("ColumnLayer",data=df,get_position=["lon", "lat"],get_elevation="ClosestDispo",elevation_scale=250,radius=500,pickable=True,auto_highlight=True,get_fill_color=["red","green","blue",225])
        dff=pd.read_csv("CustomersMap.csv")
        sales_dispo = pdk.Layer("ColumnLayer",data=dff,get_position=["lon", "lat"],get_elevation=500,elevation_scale=15,radius=600,pickable=True,auto_highlight=True,get_fill_color=[255,255,255,255])

        tooltip = {"html": "<b>{business_name}</b> Town Population: {town_pop} Distance: {ClosestDispo}","style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"}}

        arc_layer_map=pdk.Deck(map_provider='carto',layers=[all_dispo,sales_dispo],initial_view_state=view,api_keys=None,tooltip=tooltip)
        st.header("All Mass Dispensaries Map")
        st.write("Columns Heights represent distance from nearest current customer")
        st.write("White Columns are current customers.\n\nRed Columns are Provisional License holders.\n\nGreen/Blue hold Final Licenses.")

        st.pydeck_chart(arc_layer_map)
        arc_layer_map.to_html("Dispensary_Map.html")
dispo_map()
