# SETUP
import gurobipy as gp
from gurobipy import GRB
from itertools import combinations
import math
import folium
from folium.map import Popup
from IPython.display import display



f1_venues =  [
    {"city": "Yas Marina", "country": "Abu Dhabi", "latitude": 24.4672, "longitude": 54.6037},
    {"city": "Melbourne", "country": "Australia", "latitude": -37.8136, "longitude": 144.9631},
    {"city": "Shanghai", "country": "China", "latitude": 31.2304, "longitude": 121.4737},
    {"city": "Sakhir", "country": "Bahrain", "latitude": 26.0325, "longitude": 50.5106},
    {"city": "Jeddah", "country": "Saudi Arabia", "latitude": 21.4858, "longitude": 39.1925},
    {"city": "Miami", "country": "USA", "latitude": 25.7617, "longitude": -80.1918},
    {"city": "Imola", "country": "Italy", "latitude": 44.3559, "longitude": 11.7161},
    {"city": "Monaco", "country": "Monaco", "latitude": 43.7384, "longitude": 7.4246},
    {"city": "São Paulo", "country": "Brazil", "latitude": -23.5505, "longitude": -46.6333},
    {"city": "Barcelona", "country": "Spain", "latitude": 41.3851, "longitude": 2.1734},
    {"city": "Montreal", "country": "Canada", "latitude": 45.5017, "longitude": -73.5673},
    {"city": "Spielberg", "country": "Austria", "latitude": 47.2195, "longitude": 14.7799},
    {"city": "Silverstone", "country": "UK", "latitude": 52.0742, "longitude": -1.0141},
    {"city": "Spa", "country": "Belgium", "latitude": 50.4921, "longitude": 5.8641},
    {"city": "Budapest", "country": "Hungary", "latitude": 47.4979, "longitude": 19.0402},
    {"city": "Zandvoort", "country": "Netherlands", "latitude": 52.3840, "longitude": 4.5294},
    {"city": "Suzuka", "country": "Japan", "latitude": 34.8823, "longitude": 136.5847},
    {"city": "Monza", "country": "Italy", "latitude": 45.5845, "longitude": 9.2744},
    {"city": "Singapore", "country": "Singapore", "latitude": 1.3521, "longitude": 103.8198},
    {"city": "Baku", "country": "Azerbaijan", "latitude": 40.4093, "longitude": 49.8671},
    {"city": "Austin", "country": "USA", "latitude": 30.2672, "longitude": -97.7431},
    {"city": "Mexico City", "country": "Mexico", "latitude": 19.4326, "longitude": -99.1332},
    {"city": "Las Vegas", "country": "USA", "latitude": 36.1699, "longitude": -115.1398},
    {"city": "Lusail", "country": "Qatar", "latitude": 25.4670, "longitude": 51.3960}
]

us_capitals = [
    {"city": "Montgomery", "state": "Alabama", "latitude": 32.377716, "longitude": -86.300568},
    {"city": "Phoenix", "state": "Arizona", "latitude": 33.448143, "longitude": -112.096962},
    {"city": "Little Rock", "state": "Arkansas", "latitude": 34.746613, "longitude": -92.288986},
    {"city": "Sacramento", "state": "California", "latitude": 38.576668, "longitude": -121.493629},
    {"city": "Denver", "state": "Colorado", "latitude": 39.739227, "longitude": -104.99025},
    {"city": "Hartford", "state": "Connecticut", "latitude": 41.764046, "longitude": -72.682198},
    {"city": "Dover", "state": "Delaware", "latitude": 39.157307, "longitude": -75.519722},
    {"city": "Tallahassee", "state": "Florida", "latitude": 30.438118, "longitude": -84.281296},
    {"city": "Atlanta", "state": "Georgia", "latitude": 33.749027, "longitude": -84.388229},
    {"city": "Boise", "state": "Idaho", "latitude": 43.617775, "longitude": -116.199722},
    {"city": "Springfield", "state": "Illinois", "latitude": 39.798363, "longitude": -89.654961},
    {"city": "Indianapolis", "state": "Indiana", "latitude": 39.768623, "longitude": -86.162643},
    {"city": "Des Moines", "state": "Iowa", "latitude": 41.590939, "longitude": -93.620866},
    {"city": "Topeka", "state": "Kansas", "latitude": 39.048191, "longitude": -95.677956},
    {"city": "Frankfort", "state": "Kentucky", "latitude": 38.186722, "longitude": -84.875374},
    {"city": "Baton Rouge", "state": "Louisiana", "latitude": 30.457069, "longitude": -91.187393},
    {"city": "Augusta", "state": "Maine", "latitude": 44.307167, "longitude": -69.781693},
    {"city": "Annapolis", "state": "Maryland", "latitude": 38.978445, "longitude": -76.492183},
    {"city": "Boston", "state": "Massachusetts", "latitude": 42.358162, "longitude": -71.063698},
    {"city": "Lansing", "state": "Michigan", "latitude": 42.733635, "longitude": -84.555328},
    {"city": "Saint Paul", "state": "Minnesota", "latitude": 44.955097, "longitude": -93.102211},
    {"city": "Jackson", "state": "Mississippi", "latitude": 32.298756, "longitude": -90.18481},
    {"city": "Jefferson City", "state": "Missouri", "latitude": 38.579201, "longitude": -92.172935},
    {"city": "Helena", "state": "Montana", "latitude": 46.585709, "longitude": -112.018417},
    {"city": "Lincoln", "state": "Nebraska", "latitude": 40.808075, "longitude": -96.699654},
    {"city": "Carson City", "state": "Nevada", "latitude": 39.163914, "longitude": -119.766121},
    {"city": "Concord", "state": "New Hampshire", "latitude": 43.206898, "longitude": -71.537994},
    {"city": "Trenton", "state": "New Jersey", "latitude": 40.220596, "longitude": -74.769913},
    {"city": "Santa Fe", "state": "New Mexico", "latitude": 35.686975, "longitude": -105.937799},
    {"city": "Albany", "state": "New York", "latitude": 42.652843, "longitude": -73.748184},
    {"city": "Raleigh", "state": "North Carolina", "latitude": 35.78043, "longitude": -78.639099},
    {"city": "Bismarck", "state": "North Dakota", "latitude": 46.82085, "longitude": -100.783318},
    {"city": "Columbus", "state": "Ohio", "latitude": 39.961346, "longitude": -82.999069},
    {"city": "Oklahoma City", "state": "Oklahoma", "latitude": 35.492207, "longitude": -97.503342},
    {"city": "Salem", "state": "Oregon", "latitude": 44.938461, "longitude": -123.030403},
    {"city": "Harrisburg", "state": "Pennsylvania", "latitude": 40.264378, "longitude": -76.883598},
    {"city": "Providence", "state": "Rhode Island", "latitude": 41.830914, "longitude": -71.414963},
    {"city": "Columbia", "state": "South Carolina", "latitude": 34.000343, "longitude": -81.033211},
    {"city": "Pierre", "state": "South Dakota", "latitude": 44.367031, "longitude": -100.346405},
    {"city": "Nashville", "state": "Tennessee", "latitude": 36.16581, "longitude": -86.784241},
    {"city": "Austin", "state": "Texas", "latitude": 30.274665, "longitude": -97.74035},
    {"city": "Salt Lake City", "state": "Utah", "latitude": 40.777477, "longitude": -111.888237},
    {"city": "Montpelier", "state": "Vermont", "latitude": 44.262436, "longitude": -72.580536},
    {"city": "Richmond", "state": "Virginia", "latitude": 37.538857, "longitude": -77.43364},
    {"city": "Olympia", "state": "Washington", "latitude": 47.035805, "longitude": -122.905014},
    {"city": "Charleston", "state": "West Virginia", "latitude": 38.336246, "longitude": -81.612328},
    {"city": "Madison", "state": "Wisconsin", "latitude": 43.074684, "longitude": -89.384445},
    {"city": "Cheyenne", "state": "Wyoming", "latitude": 41.140259, "longitude": -104.820236}
]




# CREATE MAP FOR GIVEN ROUTE, START/END CITIES, TOUR TYPE, CONTEXT
def create_map(route, coordinates, context, start_city="", end_city="", tour="path"):
    if context == "US":
        map = folium.Map(location=[39, -98], zoom_start=4, min_zoom=4, max_bounds=True, tiles="CartoDB positron")
    else:
        map = folium.Map(location=[0, 0], zoom_start=2, min_zoom=2, max_bounds=True, tiles="CartoDB positron")
    points = []

    tooltip_style = """
        font-family: Verdana, Geneva, Tahoma, sans-serif;
        font-size: 14px;
        color: black;
        """

    for city in route:
        points.append(coordinates[city])
        if city == start_city:
            folium.Marker(
                location=coordinates[city],
                tooltip= folium.Tooltip(city, tooltip_style),
                icon=folium.Icon(icon='star',color='green')
            ).add_to(map)
        elif city == end_city:
            folium.Marker(
                location=coordinates[city],
                tooltip= folium.Tooltip(city, tooltip_style),
                icon=folium.Icon(icon='star',color='red')
            ).add_to(map)
        else:
            folium.CircleMarker(
                location=coordinates[city],
                radius=5,
                color='red',
                fill=True,
                fill_color='white',
                tooltip= folium.Tooltip(city, tooltip_style)
            ).add_to(map)
    if tour == "cycle":
        points.append(points[0])
    folium.PolyLine(points, color='black').add_to(map)
    map_html = map._repr_html_()
    return map_html
    


# GET DATA FOR SELECTED CITIES
def get_data(selected_cities, context):
    cities = []
    coordinates = {}
    if context == "F1":
        for venue in f1_venues:
            if venue['city'] in selected_cities:
                city = venue['city']
                cities.append(city)
                coordinates[city] = (float(venue['latitude']), float(venue['longitude']))
    elif context == "US":
        for capital in us_capitals:
            if capital['city'] in selected_cities:
                city = capital['city']
                cities.append(city)
                coordinates[city] = (float(capital['latitude']), float(capital['longitude']))
    
    def distance(city1, city2):
        c1 = coordinates[city1]
        c2 = coordinates[city2]
        lat1 = math.radians(c1[0])
        lon1 = math.radians(c1[1])
        lat2 = math.radians(c2[0])
        lon2 = math.radians(c2[1])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        R = 6371.0
        distance = R * c
        return distance
    
    dist = {(c1, c2): distance(c1, c2) for c1, c2 in combinations(cities, 2)}
    return cities, coordinates, dist



# REGULAR TSP MODEL
def reg_tsp(selected_cities):
    cities, coordinates, dist = get_data(selected_cities)

    def subtour(edges):
        unvisited = cities[:]
        cycle = cities[:]
        while unvisited:
            thiscycle = []
            neighbors = unvisited
            while neighbors:
                current = neighbors[0]
                thiscycle.append(current)
                unvisited.remove(current)
                neighbors = [j for i, j in edges.select(current, '*') if j in unvisited]
            if len(thiscycle) <= len(cycle):
                cycle = thiscycle
        return cycle
    
    def subtourelim(model, where):
        if where == GRB.Callback.MIPSOL:
            vals = model.cbGetSolution(model._vars)
            selected = gp.tuplelist((i, j) for i, j in model._vars.keys() if vals[i, j] > 0.5)
            tour = subtour(selected)
            if len(tour) < len(cities):
                model.cbLazy(gp.quicksum(model._vars[i, j] for i, j in combinations(tour, 2)) <= len(tour)-1)

    m = gp.Model()
    vars = m.addVars(dist.keys(), obj=dist, vtype=GRB.BINARY, name='x')
    vars.update({(j,i):vars[i,j] for i,j in vars.keys()})
    cons = m.addConstrs(vars.sum(c, '*') == 2 for c in cities)
    m.setParam('OutputFlag', 0)
    m._vars = vars
    m.Params.lazyConstraints = 1
    m.optimize(subtourelim)

    solved_vars = m.getAttr('x', vars)
    solved_obj = m.ObjVal
    selected = gp.tuplelist((i, j) for i, j in solved_vars.keys() if solved_vars[i, j] > 0.5)
    tour = subtour(selected)
    assert len(tour) == len(cities)


    tour_text = "<p>" + "<br>".join(tour) + "<p>"
    map_render = create_map(tour, coordinates, tour="cycle")

    return tour_text, round(solved_obj), map_render



# FREELY-OPEN-LOOP TSP MODEL
def fol_tsp(selected_cities, start_city, end_city, context):
    cities, coordinates, dist = get_data(selected_cities, context)

    def subtour(edges):
        unvisited = cities[:]
        cycle = cities[:]
        path = []
        while unvisited:
            thistour = []
            neighbors = unvisited
            while neighbors:
                cycle_found = 0
                current = neighbors[0]
                thistour.append(current)
                unvisited.remove(current)
                neighbors = [j for i,j in edges.select(current, '*') if j in unvisited]
                if not neighbors:
                    if thistour[0] in [j for i,j in edges.select(current, '*')] and len(thistour) > 2:
                        cycle_found = 1
                        if len(thistour) <= len(cycle):
                            cycle = thistour
                        break
                    thistour.reverse()
                    current = thistour[-1]
                    neighbors = [i for i,j in edges.select('*', current) if i in unvisited]
            if not cycle_found:
                path = thistour
        if len(path) == len(cities):
            return path
        return cycle

    def subtourelim(model, where):
        if where == GRB.Callback.MIPSOL:
            vals = model.cbGetSolution(model._vars)
            selected = gp.tuplelist((i, j) for i, j in model._vars.keys() if round(vals[i, j]) != 0)
            tour = subtour(selected)
            if len(tour) < len(cities):
                model.cbLazy(gp.quicksum(model._vars[i, j] for i, j in combinations(tour, 2)) <= len(tour)-1)

    m = gp.Model()
    vars = m.addVars(dist.keys(), obj=dist, vtype=GRB.BINARY, name='x')
    vars.update({(j,i):vars[i,j] for i,j in vars.keys()})
    if start_city:
        m.addConstr(vars.sum(start_city, '*') == 1)
    if end_city:
        m.addConstr(vars.sum(end_city, '*') == 1)
    m.addConstrs(vars.sum(c, '*') <= 2 for c in cities)
    m.addConstrs(vars.sum(c, '*') >= 1 for c in cities)
    m.addConstr((gp.quicksum(vars[(i,j)] for i,j in dist.keys()) == len(cities)-1))
    m.setParam('OutputFlag', 0)
    m._vars = vars
    m.Params.lazyConstraints = 1
    m.optimize(subtourelim)

    solved_vars = m.getAttr('x', vars)
    solved_obj = m.ObjVal
    selected = gp.tuplelist((i, j) for i, j in solved_vars.keys() if round(solved_vars[i, j]) != 0)
    tour = subtour(selected)
    assert len(tour) == len(cities)
    if start_city:
        if tour[0] != start_city:
            tour = tour[::-1]
    if end_city:
        if tour[-1] != end_city:
            tour = tour[::-1]

    tour_text = "<p>" + "<br>".join(tour) + "<p>"
    map_render = create_map(tour, coordinates, context, start_city, end_city)

    return tour_text, round(solved_obj), map_render



# NEAREST NEIGHBOR METHOD
def nn(selected_cities, start_city, context):
    cities, coordinates, dist = get_data(selected_cities, context)

    def nearest_neighbor(current_city, unvisited_cities):
        min_distance = float('inf')
        nearest_neighbor = None
        for city in unvisited_cities:
            try:
                d = dist[current_city, city]
            except:
                d = dist[city, current_city]
            if d < min_distance:
                min_distance = d
                nearest_neighbor = city
        return nearest_neighbor, min_distance

    def nearest_neighbor_algorithm(start_city):
        total_distance = 0
        unvisited = cities[:]
        current_city = start_city
        path = [current_city]
        unvisited.remove(current_city)
        while unvisited:
            next_city, dist = nearest_neighbor(current_city, unvisited)
            path.append(next_city)
            total_distance += dist
            unvisited.remove(next_city)
            current_city = next_city
        return path, total_distance
    
    if start_city:
        tour, total_distance = nearest_neighbor_algorithm(start_city)
    else:
        paths = []
        for city in cities:
            paths.append(nearest_neighbor_algorithm(city))
        paths.sort(key = lambda x: x[1])
        tour, total_distance = paths[0]
    
    tour_text = "<p>" + "<br>".join(tour) + "<p>"
    map_render = create_map(tour, coordinates, context)

    return tour_text, round(total_distance), map_render



# NEAREST INSERTION METHOD
def ni(selected_cities, start_city, context):
    cities, coordinates, dist = get_data(selected_cities, context)

    def nearest_neighbor(current_city, unvisited_cities):
        min_distance = float('inf')
        nearest_neighbor = None
        for city in unvisited_cities:
            try:
                d = dist[current_city, city]
            except:
                d = dist[city, current_city]
            if d < min_distance:
                min_distance = d
                nearest_neighbor = city
        return nearest_neighbor, min_distance

    def nearest_insertion_algorithm(start_city):
        total_distance = 0
        unvisited = cities[:]
        path = [start_city]
        unvisited.remove(start_city)
        while unvisited:
            city_1 = path[0]
            city_2 = path[-1]
            next_city_1, dist_1 = nearest_neighbor(city_1, unvisited)
            next_city_2, dist_2 = nearest_neighbor(city_2, unvisited)
            if dist_1 <= dist_2:
                path = [next_city_1] + path
                total_distance += dist_1
                unvisited.remove(next_city_1)
            else:
                path = path + [next_city_2]
                total_distance += dist_2
                unvisited.remove(next_city_2)
        return path, total_distance
    
    if start_city:
        tour, total_distance = nearest_insertion_algorithm(start_city)
    else:
        paths = []
        for city in cities:
            paths.append(nearest_insertion_algorithm(city))
        paths.sort(key = lambda x: x[1])
        tour, total_distance = paths[0]

    tour_text = "<p>" + "<br>".join(tour) + "<p>"
    map_render = create_map(tour, coordinates, context)

    return tour_text, round(total_distance), map_render



# DELETED TSP MODEL
def del_tsp(selected_cities, context):
    cities, coordinates, dist = get_data(selected_cities, context)

    def subtour_fol_tsp(edges):
        unvisited = cities[:]
        cycle = cities[:]
        path = []
        while unvisited:
            thistour = []
            neighbors = unvisited
            while neighbors:
                cycle_found = 0
                current = neighbors[0]
                thistour.append(current)
                unvisited.remove(current)
                neighbors = [j for i,j in edges.select(current, '*') if j in unvisited]
                if not neighbors:
                    if thistour[0] in [j for i,j in edges.select(current, '*')] and len(thistour) > 2:
                        cycle_found = 1
                        if len(thistour) <= len(cycle):
                            cycle = thistour
                        break
                    thistour.reverse()
                    current = thistour[-1]
                    neighbors = [i for i,j in edges.select('*', current) if i in unvisited]
            if not cycle_found:
                path = thistour
        if len(path) == len(cities):
            return path
        return cycle

    def subtour_reg_tsp(edges):
        unvisited = cities[:]
        cycle = cities[:]
        while unvisited:
            thiscycle = []
            neighbors = unvisited
            while neighbors:
                current = neighbors[0]
                thiscycle.append(current)
                unvisited.remove(current)
                neighbors = [j for i, j in edges.select(current, '*') if j in unvisited]
            if len(thiscycle) <= len(cycle):
                cycle = thiscycle
        return cycle
    
    def subtourelim(model, where):
        if where == GRB.Callback.MIPSOL:
            vals = model.cbGetSolution(model._vars)
            selected = gp.tuplelist((i, j) for i, j in model._vars.keys() if vals[i, j] > 0.5)
            tour = subtour_reg_tsp(selected)
            if len(tour) < len(cities):
                model.cbLazy(gp.quicksum(model._vars[i, j] for i, j in combinations(tour, 2)) <= len(tour)-1)

    m = gp.Model()
    vars = m.addVars(dist.keys(), obj=dist, vtype=GRB.BINARY, name='x')
    vars.update({(j,i):vars[i,j] for i,j in vars.keys()})
    cons = m.addConstrs(vars.sum(c, '*') == 2 for c in cities)
    m.setParam('OutputFlag', 0)
    m._vars = vars
    m.Params.lazyConstraints = 1
    m.optimize(subtourelim)

    solved_vars = m.getAttr('x', vars)
    solved_obj = m.ObjVal
    selected = gp.tuplelist((i, j) for i, j in solved_vars.keys() if solved_vars[i, j] > 0.5)
    
    pair_distances = []
    for pair in selected:
        try:
            d = dist[pair]
        except:
            d = dist[pair[::-1]]
        pair_distances.append((pair, d))
    pair_distances.sort(key=lambda x: x[1])
    longest_distance = pair_distances[-1][1]
    pair_distances.pop()
    pair_distances.pop()
    selected = gp.tuplelist(pair for pair, dist in pair_distances)

    tour = subtour_fol_tsp(selected)
    assert len(tour) == len(cities)
    solved_obj = solved_obj - longest_distance

    tour_text = "<p>" + "<br>".join(tour) + "<p>"
    map_render = create_map(tour, coordinates, context)

    return tour_text, round(solved_obj), map_render