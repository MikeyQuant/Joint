import streamlit as st
import pandas as pd
import pydeck as pdk



def dispo_map():

        mbapi="pk.eyJ1IjoibWlrZXlxdWFudCIsImEiOiJja25rbDE0ODUwYWRpMnJwYjI0a25zc2FtIn0.XRafIAKi72faYbEMjYO5aw"
        df=pd.read_csv("MassDispoCords2.csv")
        print(len(df))
        view=pdk.ViewState(latitude=df["lat"].mean(),longitude=df["lon"].mean(),pitch=20,zoom=5)
        all_dispo = pdk.Layer("ColumnLayer",data=df,get_position=["lon", "lat"],get_elevation="ClosestDispo",elevation_scale=250,radius=500,pickable=True,auto_highlight=True,get_fill_color=["Distance", "town_pop", "255 - Distance", 255])
        dff=pd.read_csv("CustomersMap.csv")
        sales_dispo = pdk.Layer("ColumnLayer",data=dff,get_position=["lon", "lat"],get_elevation=500,elevation_scale=15,radius=600,pickable=True,auto_highlight=True,get_fill_color=[255,255,255,255])

        tooltip = {"html": "<b>{business_name}</b> Town Population: {town_pop} Distance: {ClosestDispo}","style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"}}

        arc_layer_map=pdk.Deck(map_provider='carto',layers=[all_dispo,sales_dispo],initial_view_state=view,api_keys=None,tooltip=tooltip)
        st.header("All Mass Dispensaries Map")
        st.write("Columns are weighted by Square Footage of Facility")
        st.write("Black Columns are current customers, some may overlap with potential customers")

        st.pydeck_chart(arc_layer_map)
        arc_layer_map.to_html("Dispensary_Map.html")
dispo_map()
