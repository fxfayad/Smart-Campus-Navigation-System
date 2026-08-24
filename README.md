# AI Route Planning Prototype

This project is a Python Tkinter-based campus route planner. It simulates a university map, lets a user choose a starting point and destination, and then calculates the best route based on distance and traffic conditions.

## Project idea

The app models the campus as a road network:

- each place is a node
- each road between two places is an edge
- every edge has a distance and travel time
- the system uses algorithms to choose the best route

This is a simple example of graph-based route planning, similar to how real navigation apps work.

## Features

- English-language interface
- Select current location and destination
- Choose time of day
- Adjust traffic intensity level
- AI Agent 1: shortest-distance route
- AI Agent 2: fastest route under traffic conditions
- Highlight routes and traffic hotspots on the map
- Show route summary in a text panel

## How the app works

When the user opens the app:

1. The window is created in the main UI file.
2. The campus map is displayed on a canvas.
3. The user selects a start point and destination.
4. The selected time and traffic value are read.
5. The route logic computes the best route.
6. The map is redrawn with the selected route and traffic highlights.
7. The result panel shows details such as distance, time, and route names.

## File-by-file explanation

### 1. main.py

This file is the program launcher.

It contains:

- the main entry point
- the import of the app builder from app.py
- a small script that starts the application

It does not contain most of the logic. It simply runs the UI.

### 2. app.py

This is the main application file.

It handles:

- the Tkinter window
- the map canvas
- the route selection controls
- traffic display
- route drawing on the map
- the summary text area

Important functions:

- draw_map_background(): draws the campus road grid and map background
- draw_route(): draws a route line between two nodes
- draw_traffic_overlay(): colors active roads based on congestion level
- draw_base_map(): redraws the map with nodes, labels, route, and traffic
- update_ui(): runs when route data is requested and updates the interface
- make_app(): creates the full app window and widgets

This file connects the user interface and the route logic together.

### 3. route_data.py

This file contains all static data used by the system.

It stores:

- node positions, like A, B, C, ...
- human-readable place names, such as 1 No. Gate and Library
- road list with distance and time values
- list of all campus locations
- time options like 06:00, 08:00, 10:00, etc.

Example:

- A = 1 No. Gate
- D = Library
- L = 2 No. Gate

These are used to build the network of campus routes.

### 4. route_logic.py

This is the heart of the route calculation system.

It contains:

- build_graph(): converts road data into a graph
- traffic_multiplier(): changes travel time according to time of day
- slider_multiplier(): changes travel time according to user traffic slider
- dijkstra(): computes the shortest path using Dijkstra's algorithm
- find_all_routes(): finds several possible routes
- agent1_best_route(): computes the shortest-distance route
- agent2_traffic_aware_route(): computes the fastest route under congestion
- compute_route(): combines everything into one final result
- resolve_location_code(): converts place names to internal node codes

### 5. traffic_logic.py

This file creates the traffic simulation.

It has:

- traffic colors: green, yellow, red
- traffic_level_for_factor(): decides the road level by factor
- generate_traffic_segments(): creates road traffic conditions for the selected time and traffic settings

This file is responsible for making the map look realistic and showing which roads are highly congested.

## Route planning logic

The program uses a graph structure.

A graph is a collection of nodes and connections:

- nodes are campus locations
- links are roads connecting them
- each road has a distance and time cost

For example:

- A to C = distance 3.6 km, time 6 minutes
- C to E = distance 4.5 km, time 8 minutes

### Dijkstra algorithm

Dijkstra's algorithm is used to compute the shortest route from a start node to a destination node.

It works by:

1. starting from the source node
2. exploring neighbors
3. calculating the travel cost for each path
4. selecting the lowest-cost path first
5. repeating until the destination is reached

This is a standard algorithm for shortest path problems in maps and navigation systems.

## AI Agent 1

AI Agent 1 finds the shortest-distance route.

It calculates the best route based only on total distance.

This means:

- fewer kilometers
- not necessarily the fastest in traffic
- good for distance-focused travel

## AI Agent 2

AI Agent 2 finds the route that is fastest when traffic is considered.

It uses:

- time-of-day traffic multiplier
- user-selected traffic intensity
- random traffic adjustment for each road
- route cost based on travel time instead of only distance

This is why the route may change from the shortest-distance path to a different path if traffic is heavy.

## Traffic simulation

The app does not use a real traffic system from the internet. Instead, it simulates traffic by adjusting the time cost of each road.

The logic uses:

- morning peak hours: higher traffic multiplier
- evening peak hours: higher traffic multiplier
- low-traffic hours: lower multiplier
- user traffic slider: raises or lowers road difficulty

This affects the route chosen by AI Agent 2.

## Map display

The map canvas draws:

- a base road grid
- campus nodes and labels
- road lines
- route highlight for the selected route
- alternate route as a second color
- traffic overlays in yellow and red for congested roads

The selected route is shown in green, while the alternate route appears in red. Traffic-heavy roads are highlighted with red or yellow lines.

## Result summary

After route calculation, the app prints a summary like:

- start location
- destination
- time of day
- traffic intensity
- distance and route names
- route details for other possible paths

This allows the user to compare multiple potential routes.

## Program flow in simple steps

1. User opens the app
2. User chooses current location and destination
3. User picks time and traffic level
4. app.py calls update_ui()
5. update_ui() resolves names into codes
6. compute_route() is called with the selected values
7. route_logic.py finds shortest and quickest routes
8. traffic_logic.py calculates road congestion levels
9. draw_base_map() redraws the map with highlights
10. Text summary is displayed to the user

## How to run

Open the project folder and run:

python main.py

If the app uses Tkinter and Python is installed correctly, the window should appear.

## Notes

This project is a prototype and not a production-grade navigation system. It is useful for learning:

- graph theory
- shortest path algorithms
- route optimization
- traffic simulation
- Tkinter GUI design

It is a good beginner project for understanding how navigation apps think internally.

## Summary

This application is a small AI-based route planner for a campus map. It uses graph data, shortest-path algorithms, and traffic-aware logic to choose routes and visually highlight them on a map. The main concept is that the app treats roads as connections between places and calculates the best route based on distance and congestion.
