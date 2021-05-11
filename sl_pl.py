import pandas as pd
import streamlit as st
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
def chart_options(index):
    st.header("Chart Options")
    c2,c3,c4,c5=st.beta_columns(4)
    alpha=c2.slider("Select Transparency",0.0,1.0,.5,key=index)
    grid=c3.checkbox("Grid?",key=index)
    color=c4.selectbox("Select Color for Charts",["purple","red","blue","green","yellow","orange","black","grey"],key=index)
    spacing=c5.slider("X label spacing",0,30,1,key=index)
    if grid ==True:
        linestyle=c3.selectbox("What lines would you like for the grid",["-","--","-.",":"],key=index)
        thickness=c3.slider("Grid thickness",0.0,2.0,.5,key=index)
        color2=c3.selectbox("Select Color for grid",["purple","red","blue","green","yellow","orange","black","grey"],key=index)

    else:
        linestyle=0
        thickness=0
        color2=0
    return alpha,grid,linestyle,thickness,color,color2,spacing

def sales_rev(days):
    #alpha,grid,linestyle,thickness,color,color2,spacing=chart_options(1)

    df=pd.read_csv('Levia_Live_Sales.csv')
    df=df[df["Date"].isin(days)]
    revs=[]
    case=[]
    total_revs=[]
    tr=0
    for x in days:
        rev=84*sum(df[df["Date"]==x]["Total"])
        cases= sum(df[df["Date"]==x]["Total"])
        revs.append(rev)
        case.append(cases)
        tr+=rev
        total_revs.append(tr)
    plt.clf()
    d=[]
    c1,c2=st.beta_columns(2)
    spacing=c1.slider("X label spacing",0,30,1)
    ma_window=c2.number_input("Moving Average Window",3)

    cases_ma=[]
    for i,x in enumerate(case):
        if i<ma_window:
            cases_ma.append(0)
        else:
            ma=sum(case[i-ma_window:i+1])/ma_window
            cases_ma.append(ma)
    for day in days:
        d.append(day[:-5])
    fig, ax = plt.subplots(2,1)
    ax[0].bar(d,case)
    ax[0].set_title("Total Cases Sold by Date")
    ax[0].plot(d,cases_ma)

    ax[0].xaxis.set_major_locator(ticker.MultipleLocator(spacing))
    ax[1].bar(d,revs)
    ax[1].set_title("Revenue")
    ax[1].plot(d,total_revs)
    ax[1].xaxis.set_major_locator(ticker.MultipleLocator(spacing))
    plt.xticks(rotation='vertical')
    plt.xticks(rotation='vertical')
    fig.tight_layout(pad=3.0)
    st.pyplot(plt)
def orders_by_day(days):
    df=pd.read_csv("Levia_Live_Sales.csv")
    from bokeh.core.properties import value
    from bokeh.io import show
    from bokeh.models import ColumnDataSource, HoverTool
    from bokeh.plotting import figure
    from bokeh.io import show
    from bokeh.models import ColumnDataSource, HoverTool, CustomJSHover
    from bokeh.plotting import figure
    from bokeh.io import output_file, show
    from bokeh.palettes import Category20c
    from bokeh.plotting import figure
    from bokeh.transform import cumsum
    from bokeh.palettes import Turbo256,Turbo,inferno
    from bokeh.models import LabelSet, ColumnDataSource
    from bokeh.models import ColumnDataSource, HoverTool
    #df=pd.read_csv("LeviaExpenses.csv",index_col=0)
    output_file("stacked.html")


    dff=df[df["Date"].isin(days)]
    dfn=pd.DataFrame(index=days,columns=[act for act in pd.unique(dff["Account"])])
    print(dff)

    for i,d in enumerate(dfn.index):
        for act in dfn:
            dfff=dff[dff["Account"]==act]
            dfff=dfff[dfff["Date"]==d].reset_index()
            try:
                dfn[act][i]=dfff["Total"][0]
            except:
                dfn[act][i]=0

    st.dataframe(dfn)

    data={"Years":[x[:-5] for x in days]}

    for i,col in enumerate(dfn.columns):

        data[col]=dfn[col].to_list()

    print(data)


    #data['color'] = Category20c[len(dict)]
    colors = inferno(43)
    #st.write(colors)
    df = pd.DataFrame(data)
    df = df.set_index('Years').rename_axis(None)

    source = ColumnDataSource(data=df)
    colors = inferno(len(df.columns))
    p = figure(x_range=[x for x in df.index], plot_height=500, plot_width=750, title="Orders by Day by Dispensary",
               toolbar_location=None, tools="")
    columns=[x for x in df.columns]
    renderers = p.vbar_stack(columns, x='index', width=0.9, color=colors, source=source,
                             legend_label=columns   , name=columns)

    formatter = CustomJSHover(
        args=dict(source=source),)

    for r in renderers:
        hover = HoverTool(tooltips=[
            ("Account", "$name"),
            ("Day", "@index"),
            ('Cases', "@$name{0}")

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
def orders_by_acct(days):
    df=pd.read_csv("Levia_Live_Sales.csv")
    from bokeh.models import ColumnDataSource, HoverTool, CustomJSHover
    from bokeh.io import output_file, show
    from bokeh.plotting import figure
    from bokeh.palettes import inferno
    from bokeh.models import ColumnDataSource, HoverTool
    output_file("stacked.html")


    dff=df[df["Date"].isin(days)].sort_values(by="Total")
    dfn=pd.DataFrame(index=[act for act in pd.unique(dff["Account"])],columns=["Cel","Ach","Dre"])
    print(dff)

    for i,act in enumerate(dfn.index):
        for flv in dfn:
            dfff=dff[dff["Account"]==act]
            try:
                dfn[flv][i]=sum(dfff[flv].to_list())
            except:
                dfn[flv][i]=0

    st.dataframe(dfn)
    #dfn=dfn.sort_values(by="")
    data={"Years":[x for x in dfn.index]}

    for i,col in enumerate(dfn.columns):

        data[col]=dfn[col].to_list()

    print(data)


    #data['color'] = Category20c[len(dict)]
    colors = inferno(43)
    #st.write(colors)
    df = pd.DataFrame(data)
    df = df.set_index('Years').rename_axis(None)

    source = ColumnDataSource(data=df)
    colors = inferno(len(df.columns))
    p = figure(x_range=[x for x in df.index], plot_height=500, plot_width=750, title="Orders By Account",
               toolbar_location=None, tools="")
    columns=[x for x in df.columns]
    p.xaxis.major_label_orientation = "vertical"
    renderers = p.vbar_stack(columns, x='index', width=0.9, color=colors, source=source,
                             legend_label=columns   , name=columns)

    formatter = CustomJSHover(
        args=dict(source=source),)

    for r in renderers:
        hover = HoverTool(tooltips=[
            ("Flavor", "$name"),
            ("Account", "@index"),
            ('Cases', "@$name{0}")

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

    pass
def production_kpi(days):
        plt.clf()
        c7,c8=st.beta_columns(2)

        for penis in [0]:
            if penis==0:
                revs=pd.read_csv("Live_Revs_PS.csv")
                sales=pd.read_csv("Live_Sales_PS.csv")
                new=pd.read_csv("Live_New_PS.csv")
                sales=sales[sales["Date"].isin(days)]
                new=new[new["Date"].isin(days)]
                revs=revs[revs["Date"].isin(days)]
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
            #ax[0].xaxis.set_major_locator(ticker.MultipleLocator(5))
            #ax[0].xaxis.set_minor_locator(ticker.MultipleLocator(1))
            ax[0].set_title('Total Inventory')
            ax[1].bar(new["Date"],new["Ach"])
            ax[1].bar(new["Date"],new["Dre"])
            ax[1].bar(new["Date"],new["Cel"])
            ax[1].fmt_xdata = mdates.DateFormatter('%m/%d/%Y')
            #ax[1].xaxis.set_major_locator(ticker.MultipleLocator(5))
            #ax[1].xaxis.set_minor_locator(ticker.MultipleLocator(1))
            ax[1].set_title('Cases Packaged')
            ax[2].bar(sales["Date"],sales["Ach"])
            ax[2].bar(sales["Date"],sales["Dre"])
            ax[2].bar(sales["Date"],sales["Cel"])
            ax[2].fmt_xdata = mdates.DateFormatter('%m/%d/%Y')
            #ax[2].xaxis.set_major_locator(ticker.MultipleLocator(5))
            #ax[2].xaxis.set_minor_locator(ticker.MultipleLocator(1))
            ax[2].set_title('Cases Sold')
            ax[0].legend(["Ach","Dre","Cel"])
            if penis==0:
                fig.suptitle('Live Production Schedule', fontsize=16)
            else:
                fig.suptitle('Joints Production Schedule', fontsize=16)
            fig.autofmt_xdate()

            if penis ==0:

                st.pyplot(plt)
            else:

                c8.pyplot(plt)
def sales_by_act(days):

    df=pd.read_csv(f"SBA.csv")
    df=df[df["Date"].isin(days)]
    dfn=pd.DataFrame()
    print(df)
    for x in df["Dre"]:
        print(type(x))
    for act in df["Account"]:
        dff=df[df["Account"]==act]
        if dfn.empty:
            dfn=pd.DataFrame([act,sum(dff["Cel"]),sum(dff["Ach"]),sum(dff["Dre"])]).transpose()
            print(dfn)
        else:
            if act in dfn[0].to_list():
                continue
            else:
                dfn=pd.concat([dfn,pd.DataFrame([act,sum(dff["Cel"]),sum(dff["Ach"]),sum(dff["Dre"])]).transpose()])
    print(dfn)
    dfn.columns=["Account","Cel","Ach","Dre"]
    dfn["Total"]=dfn["Dre"]+dfn["Ach"]+dfn["Cel"]

    sort=st.selectbox("Sort by Flavor:",["Total","Cel","Ach","Dre"])
    dfn=dfn.sort_values(by=sort)
    import numpy as np
    plt.clf()
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
    plt.bar(r4, bars4, color='blue', width=barWidth/2, edgecolor='white', label='Total',alpha=.25)
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


    st.pyplot(plt)
st.title("Levia Dashboard")

d=st.sidebar.date_input("Insert Date")
di=st.sidebar.number_input("Input Lookback Window ",value=8)
dayss=[(d-datetime.timedelta(days=x)).strftime("%m/%d/%Y")for x in range(0,di,1)][::-1]
days=[]
for day in dayss:
    d=""
    for i, s in enumerate(day):
        if s=="0" and i==0:
            pass
        elif s=="0" and i ==3:
            pass
        else:
            d=d+s
    days.append(d)




sales_rev(days)
orders_by_day(days)
orders_by_acct(days)

#sales_by_act(days)
production_kpi(days)
