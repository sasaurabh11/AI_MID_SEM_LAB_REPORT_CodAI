import numpy as np
import random
import math
import folium

def rajasthan_tour():
    loc = {
        'Jaipur': (26.9124, 75.7873),
        'Udaipur': (24.5718, 73.6840),
        'Jodhpur': (26.2389, 73.0243),
        'Jaisalmer': (26.9157, 70.9160),
        'Pushkar': (26.4922, 74.5552),
        'Ajmer': (26.4520, 74.6399),
        'Bikaner': (28.0182, 73.3132),
        'Kota': (25.2138, 75.8648),
        'Mount Abu': (24.5920, 72.7021),
        'Chittorgarh': (24.8798, 74.6248),
        'Ranthambore': (26.0022, 76.3624),
        'Bundi': (25.4420, 75.6355),
        'Neemrana': (27.9515, 76.4117),
        'Mandawa': (27.1485, 75.1824),
        'Sariska': (27.0864, 76.6350),
        'Alwar': (27.5544, 76.6005),
        'Barmer': (25.7508, 71.4013),
        'Tonk': (26.1945, 75.7907),
        'Shekhawati': (28.2706, 75.4550),
        'Osian': (26.2866, 72.8850),
    }

    init_temp = 10000
    cool_rate = 0.995
    iters = 1000

    curr_sol = list(loc.keys())
    random.shuffle(curr_sol)
    curr_cost = sum(math.sqrt((loc[curr_sol[i]][0] - loc[curr_sol[i + 1]][0]) ** 2 + (loc[curr_sol[i]][1] - loc[curr_sol[i + 1]][1]) ** 2) for i in range(len(curr_sol) - 1)) + \
                    math.sqrt((loc[curr_sol[-1]][0] - loc[curr_sol[0]][0]) ** 2 + (loc[curr_sol[-1]][1] - loc[curr_sol[0]][1]) ** 2)

    best_sol = curr_sol
    best_cost = curr_cost

    temp = init_temp

    for _ in range(iters):
        new_sol = curr_sol[:]
        i, j = random.sample(range(len(new_sol)), 2)
        new_sol[i], new_sol[j] = new_sol[j], new_sol[i]
        new_cost = sum(math.sqrt((loc[new_sol[k]][0] - loc[new_sol[k + 1]][0]) ** 2 + (loc[new_sol[k]][1] - loc[new_sol[k + 1]][1]) ** 2) for k in range(len(new_sol) - 1)) + \
                       math.sqrt((loc[new_sol[-1]][0] - loc[new_sol[0]][0]) ** 2 + (loc[new_sol[-1]][1] - loc[new_sol[0]][1]) ** 2)

        if new_cost < curr_cost or random.random() < math.exp((curr_cost - new_cost) / temp):
            curr_sol, curr_cost = new_sol, new_cost

        if curr_cost < best_cost:
            best_sol, best_cost = curr_sol, curr_cost

        temp *= cool_rate

    print("Best Tour:", best_sol)
    print("Total Cost:", best_cost)

    avg_loc = np.mean([loc[city] for city in best_sol], axis=0)
    tour_map = folium.Map(location=avg_loc, zoom_start=6)

    for city in best_sol:
        folium.Marker(location=loc[city], popup=city).add_to(tour_map)

    loc_coords = [loc[city] for city in best_sol]
    folium.PolyLine(locations=loc_coords + [loc[best_sol[0]]], color='blue', weight=2.5, opacity=1).add_to(tour_map)

    tour_map.save("rajasthan_tour_map.html")
    print("Map saved to 'rajasthan_tour_map.html'. Open this file to view the map.")

rajasthan_tour()
