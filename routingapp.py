import streamlit as st
import pandas as pd
import pydeck as pdk
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
mbapi="sk.eyJ1IjoibWlrZXlxdWFudCIsImEiOiJja2lqN2pvMGgwZHdyMnZxcmF2cHF4ZGR0In0.pBJ7Tv-oTyWSAd_V1SOpQw"
df=pd.read_csv("LeviaDeliveriesFB.csv")
def main_menu(df):

    data={}
    index=0
    for name,cases,add in zip(df["Dispensary"],df["Cases"],df["Address"]):
        data[f"Order{index}"]=st.checkbox(f"{name}, {cases} cases, {add}")
        index+=1
    if st.button("Create Route"):
        route=[]
        for x in data.keys():
            order=x
            i=int(x.split("Order")[1])
            print(data[x])
            if data[x]==True:
                route.append([df["lat"][i],df["lon"][i],df["Dispensary"][i],df["Cases"][i],df["Address"][i]])

        dfn=pd.DataFrame(route)
        ads=["68+Tenney+St+Georgetown+MA"]
        qtys=[0]
        for ad,qty in zip(dfn[4],dfn[3]):
            ads.append(ad)
            qtys.append(qty)
        dfm=pd.read_csv("FBmatrix.csv")
        for index,x in enumerate(dfm["Distance"]):

            dfm["Duration"][index]=dfm["Duration"][index].replace("hours","hour").replace("min","mins")
            try:
                dfm["Duration"][index]=(int(dfm["Duration"][index].split(" hour ")[0])*60)+int(dfm["Duration"][index].split(" hour ")[1].split(" mins")[0])
            except:
                dfm["Duration"][index]=int(dfm["Duration"][index].split(" mins")[0])
        dism=[]
        durm=[]
        for ad in ads:
            dfmn=dfm[dfm["Ad1"]==ad ]
            dism.append(dfmn["Distance"])
            durm.append(dfmn["Duration"])
        max_load=sum(dfn[3])
        if max_load>500:
            st.write("Warning: Selected route exceeds 500 case limit")
        d={}
        d["distance_matrix"]=dism
        d["duration_matrix"]=durm
        d["num_vehicles"]=1
        d["location"]=ads
        d["demands"]=qtys
        d["vehicle_capacities"]=[max_load]
        d["depot"]=0
        def print_solution(data, manager, routing, solution,dfn,ads):
            #Prints solution on console.
            total_distance = 0
            total_load = 0
            output=[]
            for vehicle_id in range(d['num_vehicles']):
                index = routing.Start(vehicle_id)
                plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
                route_distance = 0
                route_load = 0
                while not routing.IsEnd(index):
                    node_index = manager.IndexToNode(index)
                    route_load += d['demands'][node_index]
                    #ad=[ad for i,ad in enumerate(ads) if i==node_index][0]
                    #n=[n for n,a in zip(dfn[0],dfn[4]) if a==ad][0]
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
        manager = pywrapcp.RoutingIndexManager(len(d['distance_matrix']),
                                                       d['num_vehicles'], d['depot'])
        routing = pywrapcp.RoutingModel(manager)
        def distance_callback(from_index, to_index):
                    """Returns the distance between the two nodes."""
                    # Convert from routing variable Index to distance matrix NodeIndex.
                    from_node = manager.IndexToNode(from_index)
                    to_node = manager.IndexToNode(to_index)
                    return d['distance_matrix'][from_node][to_node]
        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        def demand_callback(from_index):
                            """Returns the demand of the node."""
                            # Convert from routing variable Index to demands NodeIndex.
                            from_node = manager.IndexToNode(from_index)
                            return d['demands'][from_node]

        demand_callback_index = routing.RegisterUnaryTransitCallback(
            demand_callback)
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,  # null capacity slack
            d['vehicle_capacities'],  # vehicle maximum capacities
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
        if solution:
                    output=print_solution(data, manager, routing, solution,dfn,ads)
                    dis=[]
                    routes=[]
                    for x in output[1]:
                        route=x.split(":")[1].split("\nDistance of the route")[0]
                        route_distance=int(x.split(": ")[2].split("m")[0])
                        routes.append(route)
                        dis.append(route_distance/60)


        print(([output,dis,routes]))

        import googlemaps
        api="AIzaSyA9lJOx8mjlgRdgc-OOzXasd58Pa4B6neo"
        gmaps = googlemaps.Client(key=api)
        max_load=500
        d=[output,dis,routes]
        totald=d[0][0]
        ref=dfn
        datum=d[0][1]

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
                    y=y.replace(i,ref[4][int(i)-1])
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
        import googlemaps
        print(len(routes))
        api="AIzaSyA9lJOx8mjlgRdgc-OOzXasd58Pa4B6neo"
        gmaps = googlemaps.Client(key=api)


        from_lon=[]
        from_lat=[]
        to_lon=[]
        to_lat=[]

        maps=[]

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
            view=pdk.ViewState(latitude=dfn["from_lat"].mean(),longitude=dfn["from_lon"].mean(),pitch=20,zoom=9)
            arc_layer=pdk.Layer("ArcLayer",data=dfn,get_source_position=["from_lon","from_lat"],get_target_position=["to_lon","to_lat"],get_width=5,get_tilt=15,get_source_color=[255,165,0,80],get_target_color=[128,0,128,80])
            TOOLTIP_TEXT = {"html": "{From Address}"}

            arc_layer_map=pdk.Deck(map_style='mapbox://styles/mapbox/light-v10',layers=[arc_layer],initial_view_state=view,mapbox_key=mbapi,tooltip=TOOLTIP_TEXT)
            #maps.append(arc_layer_map)
            st.write("Trip #{}".format(index))
            st.write(f"Total Cost: ${round(sum(costs[index]),0):.2f}")
            st.write("Total Time: {} hours".format(round(sum(times[index])/60,2)))
            st.write(f"Route: {routes[index]}")
            st.pydeck_chart(arc_layer_map)
main_menu(df)
