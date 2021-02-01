import pandas as pd
import streamlit as st
df=pd.read_csv("Delivery.csv")
print(df)
st.title("Revenue Projections")
gg=st.slider("Enter average weeks till reorder / 10")
st.write(f"Re order every {gg/10} weeks")

df["cases_per_week"]=df["Cases"]/gg
for x in df:
    print(x)
df["Revenue"]=df["Cases"]*84
df["Yearly Cases"]=52*df["cases_per_week"]
df["Annual Revenue"]=df["Yearly Cases"]*84
df["Monthly Revenue"]=df["Annual Revenue"]/12
gr=st.slider("Enter Monthly Growth Rate / 100")
st.write(f"{gr}% per month growth rate")
alp="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alph=[]
for letter in alp:
    alph.append(letter)
for letter in alp:
    for letter2 in alp:
        alph.append(letter+letter2)
revs=[]
for month in range(1,25):
    try:
        df[f"month{month}"]=df["Monthly Revenue"] *1+([gr*x for x in range(month)][-1])
    except:
        df[f"month{month}"]=df["Monthly Revenue"] *1+([gr*x for x in range(month)][-1])

    s=sum(df[f"month{month}"])
    print(s)
    revs.append(s)

st.line_chart(pd.DataFrame(revs))
