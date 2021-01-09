
import pandas as pd
import streamlit as st
import pydeck as pdk
mbapi="sk.eyJ1IjoibWlrZXlxdWFudCIsImEiOiJja2lqN2pvMGgwZHdyMnZxcmF2cHF4ZGR0In0.pBJ7Tv-oTyWSAd_V1SOpQw"
import os
def second_batch():
    '''df=pd.read_csv("SecondBatch.csv")
    ref=pd.read_csv("LeviaCustomers.csv")
    print(ref)
    df["Address"]=""
    for i,x in enumerate(df["Dispensary"]):
        for i2 ,y in enumerate(ref["Dispensary"]):
            if x in y:
                df["Address"][i]=ref["Addy"][i2]
    df.to_csv("SecondBatch2.csv")
    os.startfile("SecondBatch2.csv"'''



    def compile_delivery_schedule():
        api="AIzaSyA9lJOx8mjlgRdgc-OOzXasd58Pa4B6neo"

        # importing googlemaps module
\        def create_data_model(number_of_trucks):
            #df=compile_delivery_file()
            '''df=pd.read_csv("FirstBatch2.csv")
            max_load=600
            df2=pd.DataFrame()
            drops=[]
            for index,x in enumerate(df["Cases"]):
                if x>max_load:
                    drops.append(index)
                    flavors=[df["Achieve"][index],df["Celebrate"][index],df["Dream"][index]]
                    print(type(flavors))
                    for index2,y in enumerate(flavors):
                        data=df.iloc[[index]]
                        print(data)
                        data["Cases"]=y
                        df2=pd.concat([df2,data])
                        print(df2)
            for x in drops:
                df=df[df.index!=x]
            df=pd.concat([df,df2])
            df=df.reset_index()
            df.to_csv("FirstBatch3.csv")'''
            df=pd.read_csv("FBfinal3.csv")
            plant= "68+Tenney+St+Georgetown+MA"

            ads=[plant]
            qtys=[0]


            for index,x in enumerate(df["Address"]):
                    qty=(df["Cases"][index])
                    qtys.append(qty)
                    ads.append(df["Address"][index])



            #Requires API key
            #gmaps = googlemaps.Client(key=api)
            #dm=[]
            #durm=[]
            #ad1=[]
            #ad2=[]
            #for x in ads:
               #for y in ads:
                  #dm.append( gmaps.distance_matrix(x,y)["rows"][0]["elements"][0]["distance"]["text"])
                  #durm.append( gmaps.distance_matrix(x,y)["rows"][0]["elements"][0]["duration"]["text"])
                  #ad1.append(x)
                  #ad2.append(y)
            #df1=pd.DataFrame(dm,columns=["Distance"])
            #df2=pd.DataFrame(durm,columns=["Duration"])
            #df3=pd.DataFrame(ad1,columns=["Ad1"])
            #df4=pd.DataFrame(ad2,columns=["Ad2"])
            #df=df1.join(df2).join(df3).join(df4)
            #df.to_csv("SBmatrix.csv")
            #input("Done")
            df=pd.read_csv("FBmatrix2.csv",index_col=0)
            for index, x in enumerate(df["Distance"]):
                df["Distance"][index]=float(df["Distance"][index].split(" ")[0])
                df["Duration"][index]=df["Duration"][index].replace("hours","hour").replace("min","mins")
                try:
                    df["Duration"][index]=(int(df["Duration"][index].split(" hour ")[0])*60)+int(df["Duration"][index].split(" hour ")[1].split(" mins")[0])
                except:
                    df["Duration"][index]=int(df["Duration"][index].split(" mins")[0])
                if df["Duration"][index]==1:
                    df["Duration"][index]=0
                if df["Distance"][index]==1:
                    df["Distance"][index]=0
                #df["Ad1"][index]=df["Ad1"][index].replace("+"," ")
                #df["Ad2"][index]=df["Ad2"][index].replace("+"," ")
            dmm=[]
            durmm=[]
            for index1,x in enumerate(ads):
                if index1==99999:
                    pass
                else:
                    dm=[]
                    durm=[]
                    for index,y in enumerate(df["Ad2"]):
                        if index==99999:
                            pass
                        elif df["Ad1"][index]==x:
                            dm.append(df["Distance"][index])
                            durm.append(df["Duration"][index])
                    dmm.append(dm)
                    durmm.append(durm)
            data={}
            data["distance_matrix"]=durmm
            data["duration_matrix"]=durmm
            data["num_vehicles"]=number_of_trucks
            data["location"]=ads
            data["demands"]=qtys
            max_cap=600
            truck_cap=[]
            for x in range(number_of_trucks):
                truck_cap.append(max_cap)

            data["vehicle_capacities"]=truck_cap
            data["depot"]=0
            print(len(data["distance_matrix"][1]))
            print(len(data["demands"]))
            return data
        def print_solution(data, manager, routing, solution):
            #Prints solution on console.
            total_distance = 0
            total_load = 0
            output=[]
            for vehicle_id in range(data['num_vehicles']):
                index = routing.Start(vehicle_id)
                plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
                route_distance = 0
                route_load = 0
                while not routing.IsEnd(index):
                    node_index = manager.IndexToNode(index)
                    route_load += data['demands'][node_index]
                    plan_output += ' {0} Load({1}) -> '.format(node_index, route_load)
                    previous_index = index
                    index = solution.Value(routing.NextVar(index))
                    route_distance += routing.GetArcCostForVehicle(
                        previous_index, index, vehicle_id)
                plan_output += ' {0} Load({1})\n'.format(manager.IndexToNode(index),
                                                         route_load)
                plan_output += 'Distance of the route: {}m\n'.format(route_distance)
                plan_output += 'Load of the route: {}\n'.format(route_load)
                print(plan_output)
                output.append(plan_output)
                total_distance += route_distance
                total_load += route_load
            print('Total distance of all routes: {}m'.format(total_distance))
            print('Total load of all routes: {}'.format(total_load))
            return [total_distance,output]
        def main():
            """Solve the CVRP problem."""
            for x in range (1,10,1):

            # Instantiate the data problem.
                data = create_data_model(x)

                # Create the routing index manager.
                manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                                       data['num_vehicles'], data['depot'])

                # Create Routing Model.
                routing = pywrapcp.RoutingModel(manager)


                # Create and register a transit callback.
                def distance_callback(from_index, to_index):
                    """Returns the distance between the two nodes."""
                    # Convert from routing variable Index to distance matrix NodeIndex.
                    from_node = manager.IndexToNode(from_index)
                    to_node = manager.IndexToNode(to_index)
                    return data['distance_matrix'][from_node][to_node]

                transit_callback_index = routing.RegisterTransitCallback(distance_callback)

                # Define cost of each arc.
                routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)


                # Add Capacity constraint.
                def demand_callback(from_index):
                    """Returns the demand of the node."""
                    # Convert from routing variable Index to demands NodeIndex.
                    from_node = manager.IndexToNode(from_index)
                    return data['demands'][from_node]

                demand_callback_index = routing.RegisterUnaryTransitCallback(
                    demand_callback)
                routing.AddDimensionWithVehicleCapacity(
                    demand_callback_index,
                    0,  # null capacity slack
                    data['vehicle_capacities'],  # vehicle maximum capacities
                    True,  # start cumul to zero
                    'Capacity')

                # Setting first solution heuristic.
                search_parameters = pywrapcp.DefaultRoutingSearchParameters()
                search_parameters.first_solution_strategy = (
                    routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
                search_parameters.local_search_metaheuristic = (
                    routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
                search_parameters.time_limit.FromSeconds(1)

                # Solve the problem.
                solution = routing.SolveWithParameters(search_parameters)
                #solution = routing.Solve()
                # Print solution on console.
                if solution:
                    output=print_solution(data, manager, routing, solution)
                    break


                else:
                    print("No Solution")

            dis=[]
            routes=[]
            for x in output[1]:
                route=x.split(":")[1].split("\nDistance of the route")[0]
                route_distance=int(x.split(": ")[2].split("m")[0])
                routes.append(route)
                dis.append(route_distance/60)


            return [output,dis,routes]
        output=main()
        return output

    def compile_delivery_costs():
        import googlemaps
        api="AIzaSyA9lJOx8mjlgRdgc-OOzXasd58Pa4B6neo"
        gmaps = googlemaps.Client(key=api)
        max_load=500
        data=compile_delivery_schedule()
        totald=data[0][0]
        ref=pd.read_csv("FBfinal3.csv",index_col=0)
        datum=data[0][1]

        routes=[]
        for x in datum:
            p=x.split("\n")[1].split(" -> ")

            route=[]
            for index,y in enumerate(p):
                i=y.split(" ")[1]
                l=y.split("(")[1].split(")")[0]
                y=y.replace(l,"xx")
                if i=="0":
                    pass
                else:
                    y=y.replace(i,ref["Address"][int(i)-1])
                y=y.replace("xx",l)
                route.append(y)
            dis=int(x.split("\nDistance of the route: ")[1].split("m")[0])*.621371
            cost=dis/8*2.75
            #route.append(cost)
            route=route[::-1]
            routes.append(route)
        times=[]
        total_time=[]
        total_cost=[]
        costs=[]
        max_load=500
        gas=3
        mpgmin=8
        mpgv=4
        dropofftime=20
        wage=17
        for index,x in enumerate(routes):
            print(x)
            time=[]
            cost=[]
            for index2,y in enumerate(x):
                print(y)
                if y==" 0 Load(0)":
                    pass


                else:
                    if y[:3]==" 0 ":
                        ady1= "68+Tenney+St+Georgetown+MA"
                        deliverytime=0
                    else:
                        deliverytime=dropofftime

                        ady1=x[index2].split("Load (")[0]
                    if len(x[index2+1].split("(0)"))==2:
                        ady2="68+Tenney+St+Georgetown+MA"
                        deliverytime=0
                    else:

                        deliverytime=dropofftime
                        ady2=x[index2+1].split("Load (")[0].replace("'","").replace(" [","").replace("]","")
                        if ady1==ady2:
                            deliverytime=0
                    print(ady1,ady2)

                    load=int(x[index2+1].replace("Load(","*").replace(")"," ").split("*")[1])/max_load


                    dis= float(gmaps.distance_matrix(ady1,ady2)["rows"][0]["elements"][0]["distance"]["text"].split(" ")[0])
                    dur=(gmaps.distance_matrix(ady1,ady2)["rows"][0]["elements"][0]["duration"]["text"])
                    if "hour" in dur or "hours" in dur:
                        hours=int(dur[0])
                        mins=(hours*60)+int(dur.split(" ")[2])
                    else:
                        mins=int(dur.split(" ")[0])
                    mins=mins+deliverytime
                    print(dur)

                    c=((dis/1.609)/(((1-load)*mpgv)+mpgmin)*gas)+((mins/60)*wage)
                    time.append(mins)
                    cost.append(c)
            total_time.append(sum(time))
            times.append(time)
            total_cost.append(sum(cost))
            costs.append(cost)
        print(costs)
        index=0
        string=""
        string=string+f"Total Delivery Costs: ${round(sum(total_cost))}\n"
        string=string+f"Total Delivery Hours: {round(sum(total_time)/60,2)} hours\n\n"
        for x ,y,z in zip(costs,routes,times):
            index2=1
            print(f"Trip #{index}")
            string=string+f"Trip #{index}\n"
            for x2,y2,z2 in zip(x,y,z):
                print(f"Departing location {index2}: {y2}\nCost: ${x2:.2f} \nTime: {z2} min")
                string=string+f"Departing location {index2}: {y2}\nCost: ${x2:.2f} \nTime: {z2} min\n"
                index2+=1
            print(f"Total Cost: ${round(total_cost[index])}")
            string=string+f"Total Cost: ${round(total_cost[index])}\n"
            if index!=0:
                print(f"Shipping Cost per Customer: ${round(total_cost[index]/len(x))}")
                string=string+f"Shipping Cost per Customer: ${round(total_cost[index]/len(x))}\n"
            print(f"Total Time: {round(total_time[index]/60)} hours\n")
            string=string+f"Total Time: {round(total_time[index]/60)} hours\n\n"
            index+=1

        print(f"Total Delivery Costs: ${round(sum(total_cost))}")

        print(f"Total Delivery Hours: {round(sum(total_time)/60,2)} hours\n\n")
        return routes,costs,times
    def generate_cords_map(routes,costs,times):
        import googlemaps
        print(len(routes))
        api="AIzaSyA9lJOx8mjlgRdgc-OOzXasd58Pa4B6neo"
        gmaps = googlemaps.Client(key=api)


        from_lon=[]
        from_lat=[]
        to_lon=[]
        to_lat=[]

        maps=[]
        df=pd.DataFrame()
        for index,x in enumerate(routes):
            from_lon=[]
            from_lat=[]
            to_lon=[]
            to_lat=[]
            addy1=[]
            addy2=[]
            print(x)
            for index2,y in enumerate(x):
                print(y)
                if y==" 0 Load(0)":
                    pass


                else:
                    if y[:3]==" 0 ":
                        addy= "68+Tenney+St+Georgetown+MA"

                    else:


                        addy=x[index2].split("Load (")[0]
                    if len(x[index2+1].split("(0)"))==2:
                        addy_to="68+Tenney+St+Georgetown+MA"

                    else:


                        addy_to=x[index2+1].split("Load (")[0]

                try:
                     #to add delay in case of large DFs
                    geocode_result1 = gmaps.geocode(addy)
                    geocode_result2 = gmaps.geocode(addy_to)

                    from_lat.append(float( geocode_result1[0]['geometry']['location'] ['lat']))
                    from_lon.append(float(geocode_result1[0]['geometry']['location']['lng']))
                    to_lat.append(float( geocode_result2[0]['geometry']['location'] ['lat']))
                    to_lon.append(float(geocode_result2[0]['geometry']['location']['lng']))
                    addy1.append(addy)
                    addy2.append(addy_to)
                except IndexError:
                    print("Address was wrong...")
                except Exception as e:
                   print("Unexpected error occurred.", e )
            master=[from_lat,from_lon,to_lat,to_lon,addy1,addy2]


            dfn=pd.DataFrame(master).transpose()
            print(dfn)
            df=pd.concat([df,dfn])
            dfn.columns=(["from_lat","from_lon","to_lat","to_lon","From Address","To Address"])
            dfn.to_csv(f"FBdelivMap-{index}.csv")
            view=pdk.ViewState(latitude=dfn["from_lat"].mean(),longitude=dfn["from_lon"].mean(),pitch=20,zoom=9)
            arc_layer=pdk.Layer("ArcLayer",data=dfn,get_source_position=["from_lon","from_lat"],get_target_position=["to_lon","to_lat"],get_width=5,get_tilt=15,get_source_color=[randrange(0,255,1),randrange(0,255,1),randrange(0,255,1),80],get_target_color=[randrange(0,255,1),randrange(0,255,1),randrange(0,255,1),80])
            TOOLTIP_TEXT = {"html": "{From Address}"}

            arc_layer_map=pdk.Deck(map_style='mapbox://styles/mapbox/light-v10',layers=[arc_layer],initial_view_state=view,mapbox_key=mbapi,tooltip=TOOLTIP_TEXT)
            #maps.append(arc_layer_map)
            data=[index,round(sum(costs[index]),0),round(sum(times[index])/60,2),routes[index]]
            dfn=pd.DataFrame(data)
            dfn.to_csv("FBdetails-{}.csv".format(index))
            st.write("Trip #{}".format(index))
            st.write(f"Total Cost: ${round(sum(costs[index]),0):.2f}")
            st.write("Total Time: {} hours".format(round(sum(times[index])/60,2)))
            st.write(f"Route: {routes[index]}")
            st.pydeck_chart(arc_layer_map)

            maps.append(arc_layer_map)
        df.columns=(["from_lat","from_lon","to_lat","to_lon","From Address","To Address"])
        df.to_csv("LeviaDeliveriesArchMap.csv")

        return df,maps
    def generate_delivery_map():
        routes,costs,times=compile_delivery_costs()
        df,maps=generate_cords_map(routes,costs,times)

        df=pd.read_csv("LeviaDeliveriesArchMap.csv")
        '''print(df)
        ref=pd.read_csv("FirstBatch2.csv")
        df["Cases"]=""
        df["Ach"]=""
        df["Dre"]=""
        df["Cel"]=""
        df["Name"]=""
        df["Rev"]=""

        for index,x in enumerate(df["From Address"]):
            if x=="68+Tenney+St+Georgetown+MA":
                df["Cases"][index]=sum(ref["Cases"])
                df["Ach"][index]=sum(ref["Achieve"])
                df["Name"][index]="HQ"
                df["Dre"][index]=sum(ref["Dream"])
                df["Cel"][index]=sum(ref["Celebrate"])
                df["Rev"][index]=sum([int(rev.replace("$","").replace(",","")) for rev in ref["Revenue"]])
                continue
            for index2,y in enumerate(ref["Address"]):
                try:
                    x=x.split(" Load(")[0].replace(" ","")
                    print(x,1)
                    print(y,2)

                    if y == x:
                        df["Cases"][index]=ref["Cases"][index2]
                        df["Ach"][index]=ref["Achieve"][index2]
                        df["Name"][index]=ref["Dispensary"][index2]
                        df["Dre"][index]=ref["Dream"][index2]
                        df["Cel"][index]=ref["Celebrate"][index2]
                        df["Rev"][index]=ref["Revenue"][index2].replace("$","").replace(",","")
                except:
                    pass
                    print(x,y)

                #except:
                    #pass
        print(df)
        df.to_csv("LeviaDeliveriesFB.csv")'''
        view=pdk.ViewState(latitude=df["from_lat"].mean(),longitude=df["from_lon"].mean(),pitch=20,zoom=9)

        arc_layer=pdk.Layer("ArcLayer",data=df,get_source_position=["from_lon","from_lat"],get_target_position=["to_lon","to_lat"],get_width=5,get_tilt=15,get_source_color=[randrange(0,255,1),randrange(0,255,1),randrange(0,255,1),80],get_target_color=[randrange(0,255,1),randrange(0,255,1),randrange(0,255,1),80])
        column_layer = pdk.Layer("ColumnLayer",data=df,get_position=["from_lon", "from_lat"],get_elevation="Cases",elevation_scale=2,radius=250,pickable=True,auto_highlight=True,)

        tooltip = {"html": "<b>{Name}</b>  Rev: <b>${Rev}</b> Cases:{Cases} Flavors: Celebrate-{Cel} Dream-{Dre} Achieve:{Ach}","style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"}}

        arc_layer_map=pdk.Deck(map_style='mapbox://styles/mapbox/light-v10',layers=[arc_layer,column_layer],initial_view_state=view,mapbox_key=mbapi,tooltip=tooltip)
        arc_layer_map.to_html("First_Batch_Sales_Map.html")
        data=df.to_dict()
        print(data)
        st.pydeck_chart(arc_layer_map)
    generate_delivery_map()
    df=pd.read_csv("LeviaDeliveriesFB2.csv")

    view=pdk.ViewState(latitude=df["lat"].mean(),longitude=df["lon"].mean(),pitch=20,zoom=9)
    column_layer = pdk.Layer("ColumnLayer",data=df,get_position=["lon", "lat"],get_elevation="Cases",elevation_scale=25,radius=500,pickable=True,auto_highlight=True,)

    tooltip = {"html": "<b>{Dispensary}</b>  Rev: <b>{Cases}</b> Cases:{Cases} ","style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"}}

    arc_layer_map=pdk.Deck(map_style='mapbox://styles/mapbox/light-v10',layers=[column_layer],initial_view_state=view,mapbox_key=mbapi,tooltip=tooltip)
    return df
def sl():
    for i,b in enumerate(["F"]):
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
#second_batch()
sl()
