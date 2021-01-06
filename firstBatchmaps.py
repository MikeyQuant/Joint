import pandas as pd
import streamlit as st
import pydeck as pdk
mbapi="sk.eyJ1IjoibWlrZXlxdWFudCIsImEiOiJja2lqN2pvMGgwZHdyMnZxcmF2cHF4ZGR0In0.pBJ7Tv-oTyWSAd_V1SOpQw"

def sl():
    df=pd.read_csv('LeviaDeliveriesFB.csv')
    view=pdk.ViewState(latitude=df["lat"].mean(),longitude=df["lon"].mean(),pitch=20,zoom=9)
    column_layer = pdk.Layer("ColumnLayer",data=df,get_position=["lon", "lat"],get_elevation="Cases",elevation_scale=50,radius=500,pickable=True,auto_highlight=True,)

    tooltip = {"html": "<b>{Dispensary}</b>  Rev: <b>{Revenue}</b> Cases:{Cases} Flavors: Celebrate-{Celebrate} Dream-{Dream} Achieve:{Achieve}","style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"}}

    arc_layer_map=pdk.Deck(map_style='mapbox://styles/mapbox/light-v10',layers=[column_layer],initial_view_state=view,mapbox_key=mbapi,tooltip=tooltip)
    
    data=df.to_dict()
    print(data)
    st.pydeck_chart(arc_layer_map)
sl()
