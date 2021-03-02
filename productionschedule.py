import collections
from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
from intuitlib.exceptions import AuthClientError
import requests
import json
import pandas as pd
import streamlit as st
import os
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from time import sleep
import streamlit as st
from datetime import datetime
# Import Python wrapper for or-tools CP-SAT solver.
from ortools.sat.python import cp_model
from random import randrange
def generate_production_schedule():
    flv=["CEL","ACH","DRE"]
    import ezsheets
    ss=ezsheets.Spreadsheet("1-Q8b5sb2Q6Tnk4VkBAcGyQFkbxXOOXnfHuGBImyIrKw")
    sheet=ss[-1]
    alp="abcdefghijklmnopqrstuvwxyz"
    alph=[]
    for letter in alp:
        alph.append(letter)
    for letter in alp:
        for letter2 in alp:
            alph.append(letter+letter2)
    count=0
    approval_window=10
    mschedule=[]
    '''for l in range(5,240,4):
            for y in range(9,14,1):
                sheet[f"{alph[l+1]}{y}"]=0
                sleep(1.01)'''
    prev_y=0
    for l in range(5,400,4):
        def int_convert(v):
            if len(v)>0:
                v=int(v)
            else:
                v=0
            return v
        dschedule=[]
        can_brew=True
        can_bottle=True
        for y in range(9,15,1):
            #print(y,alph[l])
            tank=sheet[f"A{y}"]
            in_tank=int_convert(sheet[f"{alph[l+1]}{y}"])
            out_tank=int_convert(sheet[f"{alph[l+2]}{y}"])
            eod=int_convert(sheet[f"{alph[l+3]}{y}"])
            peod=int_convert(sheet[f"{alph[l-1]}{y}"])

            if in_tank>0:
                can_brew=False
            if (in_tank)==0 and can_brew==True and prev_y!=y:

                if peod>=50 :
                    #print(eod)
                    pass
                else:
                    #print(int(sheet[f"{alph[l-1]}{y}"]))
                    sheet[f"{alph[l+1]}{y}"]=50
                    prev_y=y
                    sleep(1)
                    can_brew=False
                    ss=ezsheets.Spreadsheet("1-Q8b5sb2Q6Tnk4VkBAcGyQFkbxXOOXnfHuGBImyIrKw")
                    sheet=ss[-1]
                    sleep(1.01)
            elif (in_tank)==0 and can_brew==False:
                pass


            if peod>0:
                #print(tank,l,y)
                try:

                    v10=int(sheet[f"{alph[l-(approval_window*4)+1]}{y}"])
                    print(v10,eod,f"{alph[l-(approval_window*4)+1]}{y}")
                    if v10==eod:
                        days_left=0
                        if can_bottle==True:
                            sheet[f"{alph[l+2]}{y}"]=peod
                            flvs=[int(sheet[f"{alph[l]}{x}"]) for x in range(20,23,1)]
                            print(flvs)

                            lowest=max(flvs)
                            index=0
                            for i,x in enumerate(flvs):
                                if x <= lowest:
                                    index=i
                                    lowest=x

                            sheet[f"{alph[l]}{y}"]=flv[index]
                            #sleep(2)
                            can_bottle=False
                            ss=ezsheets.Spreadsheet("1-Q8b5sb2Q6Tnk4VkBAcGyQFkbxXOOXnfHuGBImyIrKw")
                            sheet=ss[-1]
                            sleep(1.01)

                        print(days_left,(alph[l],y))
                    else:
                        days_left=10

                except:
                    days_left=1
            else:
                continue
