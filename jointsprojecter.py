from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.colors import named
from bokeh.palettes import Turbo256,Turbo,inferno
from math import pi
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import pandas as pd
import pydeck as pdk
from bokeh.io import output_file, show
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum

from bokeh.models import LabelSet, ColumnDataSource
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
st.set_page_config(layout="wide")
mbapi="sk.eyJ1IjoibWlrZXlxdWFudCIsImEiOiJja2lqN2pvMGgwZHdyMnZxcmF2cHF4ZGR0In0.pBJ7Tv-oTyWSAd_V1SOpQw"
def sales_by_acct_chart():
    dfn=pd.read_csv("SBA.csv",index_col=0)
    # set width of bar
    barWidth = 0.25

    # set height of bar
    bars1 = dfn["Cel"].to_list()
    bars2 = dfn["Ach"].to_list()
    bars3 = dfn["Dre"].to_list()
    bars4=dfn["Total"].to_list()
    # Set position of bar on X axis
    r1 = np.arange(len(bars1))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
    r4= [x + barWidth for x in r3]
    # Make the plot
    plt.bar(r1, bars1, color='green', width=barWidth, edgecolor='white', label='Celebrate')
    plt.bar(r2, bars2, color='yellow', width=barWidth, edgecolor='white', label='Achieve')
    plt.bar(r3, bars3, color='red', width=barWidth, edgecolor='white', label='Dream')
    plt.bar(r4, bars4, color='blue', width=barWidth, edgecolor='white', label='Total')
    # Add xticks on the middle of the group bars
    plt.xlabel('Dispensary', fontweight='bold')
    plt.xticks([r + barWidth for r in range(len(bars1))],dfn["Account"].to_list() )
    plt.xticks(rotation='vertical')
    # Create legend & Show graphic
    plt.title("Delivered Orders by Dispensary")
    plt.tight_layout()
    plt.xlabel("Dispensary")
    plt.ylabel("Cases Sold")
    plt.legend()
    c3,c4=st.beta_columns(2)


    c3.pyplot(plt)
    c4.dataframe(dfn)
def bs_pie():
    col1,col2=st.beta_columns(2)
    def bodek_pie(a):
            output_file("pie.html")
            dict={}
            for x,v in zip(a.index,a["Value"]):
                dict[x]=v

            data = pd.Series(dict).reset_index(name='value').rename(columns={'index':'item'})
            print(data)
            #data['angle'] = data['value']/data['value'].sum() * 2*pi
            data['color'] = Category20c[len(dict)]
            data['angle'] = data['value']/data['value'].sum() * 2*pi
            source = ColumnDataSource(data)
            p = figure(plot_height=350, toolbar_location=None,
                       tools="hover", tooltips="@item: @value{int}", x_range=(-0.5, 1.0))

            p.wedge(x=0, y=1, radius=0.4,start_angle=cumsum('angle', include_zero=True),end_angle=cumsum('angle'),
                    line_color="white", fill_color='color', legend_field='item', source=data)
            labels = LabelSet(x=0, y=1, text='value',angle=cumsum('angle', include_zero=False), source=source, render_mode='canvas')

            p.add_layout(labels)
            p.axis.axis_label=None
            p.axis.visible=False
            p.grid.grid_line_color = None
            #st.bokeh_chart(p)
            return p
    st.header("Balance Sheet Breakdown")

    a=pd.read_csv("Apie.csv",index_col=0)
    l=pd.read_csv("Lpie.csv",index_col=0)
    col2.header("Liability Breakdown")
    col2.bokeh_chart(bodek_pie(l))
    col1.header("Asset Breakdown")

    col1.bokeh_chart(bodek_pie(a))




def production_kpi():
        c7,c8=st.beta_columns(2)

        for penis in [0,1]:
            if penis==0:
                revs=pd.read_csv("Live_Revs_PS.csv")
                sales=pd.read_csv("Live_Sales_PS.csv")
                new=pd.read_csv("Live_New_PS.csv")
            else:
                revs=pd.read_csv("Joints_Revs_PS.csv")
                sales=pd.read_csv("Joints_Sales_PS.csv")
                new=pd.read_csv("Joints_New_PS.csv")
            fig, ax = plt.subplots(3,1)#,constrained_layout=True)

            #ax[0].plot(revs["Date"],revs["Total"])
            ax[0].plot(revs["Date"],revs["Ach"])
            ax[0].plot(revs["Date"],revs["Dre"])
            ax[0].plot(revs["Date"],revs["Cel"])


            ax[0].fmt_xdata = mdates.DateFormatter('%m/%d/%Y')
            ax[0].xaxis.set_major_locator(ticker.MultipleLocator(5))
            ax[0].xaxis.set_minor_locator(ticker.MultipleLocator(1))
            ax[0].set_title('Total Inventory')
            ax[1].bar(new["Date"],new["Ach"])
            ax[1].bar(new["Date"],new["Dre"])
            ax[1].bar(new["Date"],new["Cel"])
            ax[1].fmt_xdata = mdates.DateFormatter('%m/%d/%Y')
            ax[1].xaxis.set_major_locator(ticker.MultipleLocator(5))
            ax[1].xaxis.set_minor_locator(ticker.MultipleLocator(1))
            ax[1].set_title('Cases Packaged')
            ax[2].bar(sales["Date"],sales["Ach"])
            ax[2].bar(sales["Date"],sales["Dre"])
            ax[2].bar(sales["Date"],sales["Cel"])
            ax[2].fmt_xdata = mdates.DateFormatter('%m/%d/%Y')
            ax[2].xaxis.set_major_locator(ticker.MultipleLocator(5))
            ax[2].xaxis.set_minor_locator(ticker.MultipleLocator(1))
            ax[2].set_title('Cases Sold')
            ax[0].legend(["Ach","Dre","Cel"])
            if penis==0:
                fig.suptitle('Live Production Schedule', fontsize=16)
            else:
                fig.suptitle('Joints Production Schedule', fontsize=16)
            fig.autofmt_xdate()

            if penis ==0:

                c7.pyplot(plt)
            else:

                c8.pyplot(plt)
            #st.pyplot(plt)

def expense_graph():
    from bokeh.core.properties import value
    from bokeh.io import show
    from bokeh.models import ColumnDataSource, HoverTool
    from bokeh.plotting import figure

    from bokeh.io import show
    from bokeh.models import ColumnDataSource, HoverTool, CustomJSHover
    from bokeh.plotting import figure

    from bokeh.models import ColumnDataSource, HoverTool
    df=pd.read_csv("LeviaExpenses.csv",index_col=0)
    output_file("stacked.html")

    data={"Years":[x for x in df.index]}

    for i,col in enumerate(df.columns):

        data[col]=df[col].to_list()

    print(data)


    #data['color'] = Category20c[len(dict)]
    colors = inferno(43)
    #st.write(colors)
    df = pd.DataFrame(data)
    df = df.set_index('Years').rename_axis(None)

    source = ColumnDataSource(data=df)

    p = figure(x_range=[x for x in df.index], plot_height=750, plot_width=1900, title="Fruit Counts by Year",
               toolbar_location=None, tools="")
    columns=[x for x in df.columns]
    renderers = p.vbar_stack(columns, x='index', width=0.9, color=colors, source=source,
                             legend_label=columns   , name=columns)

    formatter = CustomJSHover(
        args=dict(source=source),)

    for r in renderers:
        hover = HoverTool(tooltips=[
            ("Expense Class", "$name"),
            ("Period", "@index"),
            ('$', "@$name{0.00}")

        ],
        formatters={'@%s'%r.name: formatter},
        renderers=[r])
        p.add_tools(hover)

    # this doesn't trigger the formatter


    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"

    st.bokeh_chart(p)
def sales_map():
        df=pd.read_csv("Leviasalessheetx.csv")
        view=pdk.ViewState(latitude=df["lat"].mean(),longitude=df["lon"].mean(),pitch=20,zoom=9)
        column_layer = pdk.Layer("ColumnLayer",data=df,get_position=["lon", "lat"],get_elevation="Revenue",elevation_scale=5,radius=250,pickable=True,auto_highlight=True,)

        tooltip = {"html": "<b>{Dispensary}</b>  Rev: <b>{Revenue}</b> Cases:{Cases} ","style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"}}

        arc_layer_map=pdk.Deck(map_style='mapbox://styles/mapbox/light-v10',layers=[column_layer],initial_view_state=view,mapbox_key=mbapi,tooltip=tooltip)
        st.header("Sales Map")
        c1,c2=st.beta_columns(2)


        c1.pydeck_chart(arc_layer_map)
        c2.dataframe(df)
def generate_cords(df):
            import googlemaps
            api="AIzaSyA9lJOx8mjlgRdgc-OOzXasd58Pa4B6neo"
            gmaps = googlemaps.Client(key=api)
            df['lon'] = ""
            df['lat'] = ""
            for x in range(len(df)):
                try:
                     #to add delay in case of large DFs
                    geocode_result = gmaps.geocode(df['Address'][x])

                    print( geocode_result[0]['geometry']['location'] ['lat'],type( geocode_result[0]['geometry']['location'] ['lat']))
                    df['lat'][x] =float( geocode_result[0]['geometry']['location'] ['lat'])
                    df['lon'][x] = float(geocode_result[0]['geometry']['location']['lng'])
                except IndexError:
                    print("Address was wrong...")
                except Exception as e:
                    print("Unexpected error occurred.", e )
            return df
def dispo_map():

        df=pd.read_csv("MassDispoCords.csv").dropna(axis='columns')
        ref=pd.read_csv("masstowns.csv")
        df["town_pop"]=0
        for i,town in enumerate(df["business_city"]):
            for i2,t in enumerate(ref["Name"]):
                if type(t)==type(1.1):
                    pass



                else:
                    print(t,town)
                    if t.upper()==town.upper():
                        df["town_pop"][i]=int(ref["Population"][i2].replace(",",""))
                        print(type(ref["Population"][i]))
                        print(town)
                        break
        api="AIzaSyA9lJOx8mjlgRdgc-OOzXasd58Pa4B6neo"

        # importing googlemaps module
        import googlemaps
        gmaps = googlemaps.Client(key=api)
        dm=[]
        durm=[]
        ad1=[]
        ad2=[]
        y="68+Tenney+Street+Georgetown+MA"
        df["Distance"]=0
        for i,x in enumerate(df["Address"]):

              df["Distance"][i]=( gmaps.distance_matrix(x,y)["rows"][0]["elements"][0]["distance"]["text"])
              print(df["Distance"][i],x)
        for index, x in enumerate(df["Distance"]):
            df["Distance"][index]=float(x.split(" ")[0].replace(",",""))
            print(type(df["Distance"][index]))
        df.to_csv("MassDispoCords.csv")
        view=pdk.ViewState(latitude=df["lat"].mean(),longitude=df["lon"].mean(),pitch=20,zoom=5)
        column_layer = pdk.Layer("ColumnLayer",data=df,get_position=["lon", "lat"],get_elevation="town_pop",elevation_scale=1,radius=250,pickable=True,auto_highlight=True,get_fill_color=[1,1,1,1])

        tooltip = {"html": "<b>{business_name}</b> Town Population: {town_pop}","style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"}}

        arc_layer_map=pdk.Deck(map_style='mapbox://styles/mapbox/light-v10',layers=[column_layer],initial_view_state=view,mapbox_key=mbapi,tooltip=tooltip)
        st.header("Sales Map")
        c1,c2=st.beta_columns(2)
        c1.pydeck_chart(arc_layer_map)
        c2.dataframe(df)
def kpi():

    expense_graph()
    sales_by_acct_chart()
    sales_map()
    bs_pie()

    production_kpi()
dispo_map()
