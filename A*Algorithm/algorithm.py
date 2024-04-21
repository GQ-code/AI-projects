# Gabriel Quezada

import sys
import heapq
import numpy as np

# Function that converts degrees into radians
def degrees_to_radians(degrees):
    return degrees * np.pi / 180

# Function to compute straight line distance using Haversine formula
def straight_line_distance(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    lat1, lon1, lat2, lon2 = map(degrees_to_radians, [lat1, lon1, lat2, lon2])
    distance_lat = lat2 - lat1 
    distance_lon = lon2 - lon1 
    x = np.sin(distance_lat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(distance_lon/2)**2
    distance = 2 * 3958.8 * np.arcsin(np.sqrt(x)) 
    return distance

# Function that reads coordinates file
def read_coordinates(file_path):
    coordinates = {}
    with open(file_path, 'r') as file:
        for line in file:
            city, coords = line.strip().split(':')
            lat, lon = coords.strip('()').split(',')
            coordinates[city] = (float(lat), float(lon))
    return coordinates

# Function that reads map file
def read_map(file_path):
    map = {}
    with open(file_path, 'r') as file:
        for line in file:
            first = line.strip().split('-')
            city = first[0].strip()
            nearby_cities = {}
            for nearby in first[1].split(','):
                nearby_city_data = nearby.split('(')
                nearby_city = nearby_city_data[0].strip()
                distance = float(nearby_city_data[1].strip(')'))
                nearby_cities[nearby_city] = distance
            map[city] = nearby_cities
    return map

# Function to implement A* algorithm
def a_star(start, end, coordinates, map):
    # priority queue
    open_set = [(0, start)]
    came_from = {}
    g_cost = {city: float('inf') for city in coordinates}
    g_cost[start] = 0

    while open_set:
        # get city with lowest f value from priority queue
        _, current_city = heapq.heappop(open_set)
        if current_city == end:
            path = [current_city]
            while current_city in came_from:
                current_city = came_from[current_city]
                path.append(current_city)
            path.reverse()
            return path, g_cost[end]

        for neighbor_city, distance in map[current_city].items():
            temp_g_cost = g_cost[current_city] + distance
            # if temp g cost is better, update optimal path
            if temp_g_cost < g_cost[neighbor_city]:
                came_from[neighbor_city] = current_city
                g_cost[neighbor_city] = temp_g_cost
                f_cost = temp_g_cost + straight_line_distance(coordinates[neighbor_city], coordinates[end])
                heapq.heappush(open_set, (f_cost, neighbor_city))

# Main function
def main():
    coordinates = read_coordinates('coordinates.txt')
    map = read_map('map.txt')

    args = sys.argv[1:]
    if len(args) != 2:
        print("Usage: python a-star.py (departing city) (arriving city)")
        return

    start = args[0]
    end = args[1]

    if start not in coordinates or end not in coordinates:
        print("Invalid departing or arriving city.")
        return

    path, total_distance = a_star(start, end, coordinates, map)

    if path is not None:
        print(f"From city: {start}")
        print(f"To city: {end}")
        print("Best Route:", ' - '.join(path))
        print(f"Total distance: {total_distance:.2f} mi")
    else:
        print("No route found between the departing and arriving cities.")

if __name__ == "__main__":
    main()
