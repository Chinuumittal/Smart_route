# **SmartRoute Optimizer**

An AI-ML-based delivery planning application designed to optimize shipment allocation. Built using **Python**, this project minimizes trips, maximizes vehicle capacity utilization, and ensures efficient deliveries within designated time slots. The system prioritizes **electric vehicles (EVs)** and supports **real-time traffic-aware routing**.

---

## **Description**

SmartRoute Optimizer provides an intelligent and efficient logistics solution by leveraging AI and ML techniques. It integrates **K-Means clustering**, **heuristic approaches**, and **network-based shortest path algorithms** to optimize delivery routes. The system ensures optimal vehicle utilization while prioritizing EVs and considering real-time traffic conditions.

---

## **Table of Contents**

1. [Features](#features)
2. [Benefits](#benefits)
3. [Release History](#release-history)
4. [Illustrations](#illustrations)
5. [Scope of Functionalities](#scope-of-functionalities)
6. [Examples of Use](#examples-of-use)

---

## **Features**

- **Optimized Vehicle Routing**: Uses K-Means clustering and heuristic approaches to determine the most efficient routes.
- **Road Network Integration**: Incorporates OpenStreetMap (OSM) data and NetworkX for accurate shortest path calculations.
- **Capacity Utilization**: Ensures vehicles are efficiently loaded to minimize trips while maximizing payload.
- **Time-Slot Optimization**: Allocates deliveries to optimized time slots while balancing trip duration.
- **Priority Vehicle Assignment**: Prefers electric vehicles (3W, 4W-EV) before standard vehicles.
- **Multi-Slot Trips**: Supports multiple deliveries per trip while maintaining constraints.

---

## **Benefits**

- **Cost Efficiency**: Reduces operational costs by minimizing fuel consumption and optimizing vehicle allocation.
- **Sustainability**: Prioritizes **EV usage** to promote eco-friendly logistics.
- **Traffic-Aware Routing**: Uses road network data to optimize delivery times and avoid congestion.
- **Improved Capacity Management**: Ensures maximum vehicle utilization to reduce unnecessary trips.
- **Real-Time Visualizations**: Generates interactive route maps for better planning and decision-making.

---

## **Release History**

- **v1.0.0**: Initial release with route optimization and vehicle allocation.
- **v1.1.0**: Integrated OpenStreetMap (OSM) and NetworkX for improved shortest path calculations.
- **v1.2.0**: Added priority-based EV assignment and interactive map visualization.

---

## **Illustrations**

### Optimized Delivery Route Visualization:
![Route Example](https://via.placeholder.com/800x400)

*An interactive map showcasing optimized delivery routes based on shipment data.*

---

## **Scope of Functionalities**

This project includes:
- AI-driven route optimization using **K-Means clustering**.
- Shortest path calculation using **OSM and NetworkX**.
- Real-time **graph-based visualizations** of optimized routes.
- **EV-first allocation strategy** to prioritize sustainable logistics.
- **CSV-based input and output processing** for shipment data.

Planned Enhancements:
- Integration with **real-time traffic data** for dynamic rerouting.
- Development of a **web-based dashboard** for route monitoring.
- Implementation of **advanced clustering techniques** for improved efficiency.

---

## **Examples of Use**

Here’s how a logistics team might use SmartRoute Optimizer:

1. Prepare the input file (`SmartRoute Optimizer.xlsx`) with shipment and vehicle details.
2. Run the optimization script:
   ```sh
   python app.py
   ```
3. View the generated `Optimized_Trips_With_Metrics.xlsx`, which contains optimized trip details.
4. Visualize a specific trip by running:
   ```sh
   python map2.py
   ```
   - Enter the **Trip ID** when prompted to generate an **HTML map** for the selected trip.
5. Analyze the output files:
   - `Optimized_Trips_With_Metrics.xlsx`: Contains optimized routes with metrics such as distance, capacity utilization, and trip time.
   - `Optimized_Trip_Trip_ID.html`: Interactive route visualization for specific trips.

---
