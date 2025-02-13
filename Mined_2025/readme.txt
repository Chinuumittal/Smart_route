SmartRoute Optimizer

Overview

SmartRoute Optimizer is an AIML-based delivery planning application designed to optimize shipment allocation. It minimizes the number of trips, maximizes vehicle capacity utilization, and ensures efficient delivery within designated time slots. The system prioritizes electric vehicles (EVs) and supports real-time traffic-aware routing.

Features

Optimized Vehicle Routing Uses K-Means clustering and heuristic approaches to optimize delivery routes.

Road Network Integration Utilizes OpenStreetMap (OSM) data and NetworkX for road-aware shortest path calculations.

Capacity Utilization Ensures vehicle capacity is maximized while maintaining efficiency.

Time-Slot Optimization Assigns deliveries to appropriate time slots while balancing load and trip duration.

Priority Vehicle Assignment Prefers electric vehicles (3W, 4W-EV) before standard vehicles.

Multi-Slot Trips Supports multiple deliveries per trip while adhering to constraints.

Dependencies

Ensure you have the following Python libraries installed

pip install pandas folium osmnx networkx scikit-learn openpyxl numpy matplotlib geopy

Files

app2.py Main optimization script that clusters shipments, assigns vehicles, and generates an optimized delivery plan.

map2.py Generates a visual representation of optimized routes using Folium and OSM data.

SmartRoute Optimizer.xlsx Input data file containing shipment and vehicle information.

Optimized_Trips_With_Metrics.xlsx Output file storing optimized trip details.

How to Use

Ensure the input file SmartRoute Optimizer.xlsx contains valid shipment and vehicle data.

Run the optimization script

python app2.py

This will generate Optimized_Trips_With_Metrics.xlsx with optimized routes and trip details.

To visualize a trip, run

python map2.py

Enter the required Trip ID when prompted. This will generate an HTML map file for the selected trip.

Output

Optimized_Trips_With_Metrics.xlsx Contains the optimized delivery plan with metrics such as distance, capacity utilization, and trip time.

Optimized_Trip_Trip_ID.html Interactive map showing the delivery route for a specific trip.

Future Enhancements

Real-time traffic integration for dynamic rerouting.

Enhanced clustering methods for improved efficiency.

Web-based dashboard for better visualization and user interaction.

Author

Developed as part of a hackathon project focusing on AIML-based logistics optimization.

