from flask import Flask, render_template, request
from tsp_methods import *
from waitress import serve

f1_2025_cities = [
    "Melbourne",        # Australian Grand Prix
    "Shanghai",         # Chinese Grand Prix
    "Suzuka",           # Japanese Grand Prix
    "Sakhir",           # Bahrain Grand Prix
    "Jeddah",           # Saudi Arabian Grand Prix
    "Miami",            # Miami Grand Prix
    "Imola",            # Emilia Romagna Grand Prix
    "Monaco",           # Monaco Grand Prix
    "Barcelona",        # Spanish Grand Prix
    "Montreal",         # Canadian Grand Prix
    "Spielberg",        # Austrian Grand Prix
    "Silverstone",      # British Grand Prix
    "Spa",              # Belgian Grand Prix
    "Budapest",         # Hungarian Grand Prix
    "Zandvoort",        # Dutch Grand Prix
    "Monza",            # Italian Grand Prix
    "Baku",             # Azerbaijan Grand Prix
    "Singapore",        # Singapore Grand Prix
    "Austin",           # United States Grand Prix
    "Mexico City",      # Mexico City Grand Prix
    "São Paulo",        # São Paulo Grand Prix
    "Las Vegas",        # Las Vegas Grand Prix
    "Lusail",           # Qatar Grand Prix
    "Yas Marina"        # Abu Dhabi Grand Prix
]

f1_venues = [
    'Austin', 'Baku', 'Barcelona', 'Budapest', 'Imola', 
    'Jeddah', 'Las Vegas', 'Lusail', 'Melbourne', 'Mexico City', 
    'Miami', 'Monaco', 'Montreal', 'Monza', 'Sakhir', 
    'Shanghai', 'Silverstone', 'Singapore', 'Spa', 'Spielberg', 
    'Suzuka', 'São Paulo', 'Yas Marina', 'Zandvoort']

f1_venues_coords =  {
    'Austin': (30.2672, -97.7431),
    'Baku': (40.4093, 49.8671),
    'Barcelona': (41.3851, 2.1734),
    'Budapest': (47.4979, 19.0402),
    'Imola': (44.3559, 11.7161),
    'Jeddah': (21.4858, 39.1925),
    'Las Vegas': (36.1699, -115.1398),
    'Lusail': (25.467, 51.396),
    'Melbourne': (-37.8136, 144.9631),
    'Mexico City': (19.4326, -99.1332),
    'Miami': (25.7617, -80.1918),
    'Monaco': (43.7384, 7.4246),
    'Montreal': (45.5017, -73.5673),
    'Monza': (45.5845, 9.2744),
    'Sakhir': (26.0325, 50.5106),
    'Shanghai': (31.2304, 121.4737),
    'Silverstone': (52.0742, -1.0141),
    'Singapore': (1.3521, 103.8198),
    'Spa': (50.4921, 5.8641),
    'Spielberg': (47.2195, 14.7799),
    'Suzuka': (34.8823, 136.5847),
    'São Paulo': (-23.5505, -46.6333),
    'Yas Marina': (24.4672, 54.6037),
    'Zandvoort': (52.384, 4.5294)
}

us_capitals = [
    'Albany', 'Annapolis', 'Atlanta', 'Augusta', 'Austin', 
    'Baton Rouge', 'Bismarck',  'Boise', 'Boston', 'Carson City', 
    'Charleston', 'Cheyenne', 'Columbia', 'Columbus',  'Concord', 
    'Denver', 'Des Moines', 'Dover', 'Frankfort', 'Harrisburg', 
    'Hartford',  'Helena', 'Indianapolis', 'Jackson', 'Jefferson City', 
    'Lansing', 'Lincoln',  'Little Rock', 'Madison', 'Montgomery', 
    'Montpelier', 'Nashville', 'Oklahoma City',  'Olympia', 'Phoenix', 
    'Pierre', 'Providence', 'Raleigh', 'Richmond', 'Sacramento',  
    'Saint Paul', 'Salem', 'Salt Lake City', 'Santa Fe', 'Springfield', 
    'Tallahassee',  'Topeka', 'Trenton']


app = Flask(__name__)

# Starting screen
@app.route('/')
@app.route('/index')
def index():
    map_html = create_map(f1_2025_cities, f1_venues_coords, context="F1", start_city="Melbourne", end_city="Yas Marina", tour="path")
    return render_template('index.html', map_html = map_html)

# FOL TSP initial screen
@app.route('/testmodelinit')
def test_model_init():
    return render_template('test_model_init.html', cities=f1_venues)

# FOL TSP results screen
@app.route('/testmodelresults')
def test_model_results():
    # Retrieving selected cities, start city, and end city
    chosen_cities = request.args.getlist('cities')
    start_city = request.args.get('startcity')
    end_city = request.args.get('endcity')

    # If no cities are chosen, then defaults to all cities
    if not chosen_cities:
        chosen_cities = f1_venues

    # Solving model
    tour, solved_obj, map_html = fol_tsp(chosen_cities, start_city, end_city, context="F1")

    if not start_city:
        start_city = "N/A"
    if not end_city:
        end_city = "N/A"
    
    return render_template(
        "test_model_results.html", 
        cities = f1_venues,
        path = tour,
        distance = solved_obj,
        map_html = map_html,
        selected_start_city = start_city,
        selected_end_city = end_city
    )

# Comparing models initial screen
@app.route('/comparemodelsinit')
def compare_models_init():
    return render_template('compare_models_init.html', cities=us_capitals)

# Comparing models results screen
@app.route('/comparemodelsresults')
def compare_models_result():
    # Retrieving selected cities, start city, and end city
    solve_method = request.args.get('solve')
    chosen_cities = request.args.getlist('cities')
    start_city = request.args.get('startcity')
    end_city = request.args.get('endcity')

    # If no cities are chosen, then defaults to all cities
    if not chosen_cities:
        chosen_cities = us_capitals
    
    # If no solve type is chosen, then default to FOL TSP
    if not solve_method:
        solve_method = "FOL TSP"

    # Running algorithm based on chosen solve method
    if solve_method == "FOL TSP":
        tour, solved_obj, map_html = fol_tsp(chosen_cities, start_city, end_city, context="US")
        solve_method = "Freely-Open-Loop TSP"
    elif solve_method == "NN":
        tour, solved_obj, map_html = nn(chosen_cities, start_city, context="US")
        solve_method = "Nearest Neighbor"
    elif solve_method == "NI":
        tour, solved_obj, map_html = ni(chosen_cities, start_city, context="US")
        solve_method = "Nearest Insertion"
    elif solve_method == "DEL TSP":
        tour, solved_obj, map_html = del_tsp(chosen_cities, context="US")
        solve_method = "Deleted TSP"

    if not start_city:
        start_city = "N/A"
    if not end_city:
        end_city = "N/A"

    return render_template(
        "compare_models_results.html", 
        cities = us_capitals,
        path = tour,
        distance = solved_obj,
        map_html = map_html,
        selected_solve_type = solve_method,
        selected_start_city = start_city,
        selected_end_city = end_city
    )

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)