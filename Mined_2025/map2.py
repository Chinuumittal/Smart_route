import pandas as pd
import folium
import osmnx as ox
import networkx as nx

# Warehouse location (latitude, longitude)
warehouse_location = (19.075887, 72.877911)

# Load optimized trips data
optimized_trips_file = "Optimized_Trips_With_Metrics.xlsx"
optimized_trips = pd.read_excel(optimized_trips_file)

# Define the road network for the region (20km radius from warehouse)
print("Downloading road network...")
G = ox.graph_from_point(warehouse_location, dist=20000, network_type="drive")

# Function to get the nearest road node for a given coordinate
def get_nearest_node(lat, lon):
    try:
        node = ox.distance.nearest_nodes(G, X=lon, Y=lat)
        return node
    except Exception as e:
        print(f"Error finding nearest node for ({lat}, {lon}): {e}")
        return None  # Return None if no valid node found

# Function to calculate the distance between two nodes
def calculate_distance(node1, node2):
    try:
        return nx.shortest_path_length(G, source=node1, target=node2, weight="length")
    except nx.NetworkXNoPath:
        return float('inf')  # If no path exists, return an infinite distance

# Nearest Neighbor Heuristic: Create a route starting from the warehouse
def nearest_neighbor_heuristic(points):
    remaining_points = points[1:]  # Exclude warehouse
    current_point = points[0]  # Warehouse as starting point
    route = [current_point]
    
    while remaining_points:
        nearest_point = min(remaining_points, key=lambda point: calculate_distance(
            get_nearest_node(current_point[0], current_point[1]), 
            get_nearest_node(point[0], point[1])
        ))
        route.append(nearest_point)
        remaining_points.remove(nearest_point)
        current_point = nearest_point
    
    # Return to warehouse at the end
    route.append(points[0])
    return route

# Function to generate a route following real roads
def get_road_route(points):
    try:
        # Get nearest road nodes for each point
        nodes = [get_nearest_node(lat, lon) for lat, lon in points]
        nodes = [node for node in nodes if node is not None]  # Remove invalid nodes
        
        if len(nodes) < 2:
            print("Not enough valid nodes to create a route")
            return points  # Fallback: return original points

        route_nodes = []
        for i in range(len(nodes) - 1):
            try:
                # Get the shortest path on the road network
                path = nx.shortest_path(G, nodes[i], nodes[i + 1], weight="length")
                route_nodes.extend(path if i == 0 else path[1:])  # Avoid duplicate nodes
            except nx.NetworkXNoPath:
                print(f"No path found between {nodes[i]} and {nodes[i + 1]}")
        
        # Convert road network nodes to latitude/longitude for mapping
        route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route_nodes]
        return route_coords
    except Exception as e:
        print(f"Error calculating road-following route: {e}")
        return points  # Fallback: return direct points if routing fails

# Get user input for trip visualization
trip_id = input("Enter the Trip ID to visualize: ")
selected_trip = optimized_trips[optimized_trips['TRIP_ID'] == int(trip_id)]

if not selected_trip.empty:
    print(f"Generating map for Trip ID {trip_id}...")

    # Add the warehouse location as the starting and ending point
    trip_points = [(warehouse_location[0], warehouse_location[1])]  # Start from warehouse
    trip_points += list(zip(selected_trip['Latitude'], selected_trip['Longitude']))  # Add shipment locations

    # Use nearest neighbor heuristic to order the stops
    ordered_trip_points = nearest_neighbor_heuristic(trip_points)

    # Get road-based route
    route_coords = get_road_route(ordered_trip_points)

    # Create the map centered on the warehouse
    map_trip = folium.Map(location=warehouse_location, zoom_start=12)

    # Plot the optimized route
    folium.PolyLine(route_coords, color="blue", weight=5).add_to(map_trip)

    # Add markers for each stop
    for idx, (lat, lon) in enumerate(ordered_trip_points, start=1):
        folium.Marker(
            location=[lat, lon],
            popup=f"Stop {idx}",
            icon=folium.Icon(color="blue", icon="info-sign"),
        ).add_to(map_trip)

    # Highlight the warehouse with a green icon
    folium.Marker(
        location=warehouse_location,
        popup="Warehouse (Start/End)",
        icon=folium.Icon(color="green", icon="home"),
    ).add_to(map_trip)

    # Save the map
    map_trip.save(f"Optimized_Trip_{trip_id}.html")
    print(f"Map for Trip ID {trip_id} saved as 'Optimized_Trip_{trip_id}.html'.")
else:
    print("Invalid Trip ID or no data available.")
