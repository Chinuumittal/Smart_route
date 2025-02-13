import pandas as pd
from geopy.distance import geodesic
from sklearn.cluster import KMeans

# Load data
file_path = "SmartRoute Optimizer.xlsx"
shipments_df = pd.read_excel(file_path, sheet_name="Shipments_Data")
vehicles_df = pd.read_excel(file_path, sheet_name="Vehicle_Information")

# Warehouse location
warehouse_location = (19.075887, 72.877911)

print("Please wait while we generate data...")

def calculate_geodesic_distance(lat, lon):
    return geodesic(warehouse_location, (lat, lon)).km

# Step 1: Group shipments by time slot
grouped_shipments = shipments_df.groupby("Delivery Timeslot")

# Step 2: Cluster shipments based on distance from warehouse
def cluster_shipments(shipments, num_clusters=5):
    if shipments.empty:
        print("No shipments found for this time slot.")
        return shipments

    locations = shipments[["Latitude", "Longitude"]].values

    n_clusters = min(num_clusters, len(shipments)) if len(shipments) > 1 else 1
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    shipments["Cluster"] = kmeans.fit_predict(locations)
    return shipments

# Step 3: Assign vehicles and calculate metrics
def assign_vehicles_with_metrics(clustered_shipments, vehicles_df, time_slot_duration):
    trips = []
    trip_id = 1
    unassigned_shipments = clustered_shipments.copy()
    
    for _, vehicle in vehicles_df.iterrows():
        vehicle_type = vehicle["Vehicle Type"]
        capacity = int(vehicle["Shipments_Capacity"])
        max_radius = float(vehicle["Max Trip Radius (in KM)"]) if vehicle["Max Trip Radius (in KM)"] != "Any" else float('inf')
        
        while not unassigned_shipments.empty:
            trip_shipments = []
            total_distance = 0
            used_capacity = 0
            trip_time = 0
            current_time_slot = None
            
            for idx, row in unassigned_shipments.iterrows():
                distance = calculate_geodesic_distance(row.Latitude, row.Longitude)
                estimated_time = distance * 15  # Adjusted travel and delivery times
                
                if used_capacity < capacity and total_distance + distance <= max_radius:
                    if current_time_slot is None or row["Delivery Timeslot"] == current_time_slot or trip_time + estimated_time <= time_slot_duration:
                        trip_shipments.append(row)
                        total_distance += distance
                        used_capacity += 1
                        trip_time += estimated_time
                        current_time_slot = row["Delivery Timeslot"]
            
            if trip_shipments:
                last_shipment = trip_shipments[-1]
                return_to_store_distance = calculate_geodesic_distance(last_shipment.Latitude, last_shipment.Longitude)
                mst_dist = total_distance + return_to_store_distance
                capacity_utilization = len(trip_shipments) / capacity
                time_utilization = trip_time / time_slot_duration
                distance_utilization = mst_dist / (max_radius * 2) if max_radius != 0 else 0
                
                trips.append({
                    "TRIP_ID": f"T{trip_id}",
                    "Shipments": trip_shipments,
                    "MST_DIST": round(mst_dist, 2),
                    "TRIP_TIME": round(trip_time, 2),
                    "Vehicle_Type": vehicle_type,
                    "CAPACITY_UTI": round(capacity_utilization, 2),
                    "TIME_UTI": round(time_utilization, 2),
                    "COV_UTI": round(distance_utilization, 2)
                })
                trip_id += 1
                
                unassigned_shipments = unassigned_shipments.drop([s.name for s in trip_shipments])
            else:
                break
    
    if not unassigned_shipments.empty:
        print("Warning: Some shipments were not assigned to any trip:")
        print(unassigned_shipments)
    
    return trips

# Process shipments
output_data = []
time_slot_duration = 120  # Assume 2 hours per time slot

for time_slot, shipments in grouped_shipments:
    clustered_shipments = cluster_shipments(shipments)
    trips = assign_vehicles_with_metrics(clustered_shipments, vehicles_df, time_slot_duration)
    
    for trip in trips:
        for shipment in trip["Shipments"]:
            output_data.append([
                trip["TRIP_ID"],
                shipment["Shipment ID"],
                shipment["Latitude"],
                shipment["Longitude"],
                time_slot,
                len(trip["Shipments"]),
                trip["MST_DIST"],
                trip["TRIP_TIME"],
                trip["Vehicle_Type"],
                trip["CAPACITY_UTI"],
                trip["TIME_UTI"],
                trip["COV_UTI"]
            ])

# Save to Excel
columns = ["TRIP_ID", "Shipment ID", "Latitude", "Longitude", "TIME SLOT", "Shipments", "MST_DIST", "TRIP_TIME", "Vehicle_Type", "CAPACITY_UTI", "TIME_UTI", "COV_UTI"]
output_df = pd.DataFrame(output_data, columns=columns)
output_df.to_excel("Optimized_Trips_With_Metrics.xlsx", index=False)
print("Optimized trips with metrics saved to Excel.")