import random
from collections import defaultdict

from route_data import NODE_POSITIONS, ROADS
from traffic_logic import generate_traffic_segments


def build_graph():
    graph = defaultdict(list)
    for u, v, dist, travel_time, road_name in ROADS:
        graph[u].append({"to": v, "distance": dist,
                        "time": travel_time, "name": road_name})
        graph[v].append({"to": u, "distance": dist,
                        "time": travel_time, "name": road_name})
    return graph


def traffic_multiplier(time_label):
    hour = int(time_label.split(":")[0])
    if 7 <= hour < 10:
        return 1.9
    if 10 <= hour < 12:
        return 1.3
    if 17 <= hour < 19:
        return 2.2
    if 20 <= hour <= 23:
        return 1.1
    return 0.95


def slider_multiplier(value):
    value = max(0, min(100, value))
    if value < 25:
        return 0.9
    if value < 50:
        return 1.1
    if value < 75:
        return 1.5
    return 2.0


def dijkstra(graph, start, goal, mode="distance"):
    distances = {node: float("inf") for node in NODE_POSITIONS}
    previous = {node: None for node in NODE_POSITIONS}
    distances[start] = 0.0
    unvisited = set(NODE_POSITIONS.keys())

    while unvisited:
        current = min(unvisited, key=lambda n: distances[n])
        if current == goal:
            break
        if distances[current] == float("inf"):
            break
        unvisited.remove(current)

        for edge in graph[current]:
            nxt = edge["to"]
            if nxt not in unvisited:
                continue
            base_cost = edge["distance"] if mode == "distance" else edge["time"]
            alt = distances[current] + base_cost
            if alt < distances[nxt]:
                distances[nxt] = alt
                previous[nxt] = (current, edge["name"],
                                 edge["distance"], edge["time"])

    if distances[goal] == float("inf"):
        return None, None

    path = []
    node = goal
    while node is not None:
        path.append(node)
        prev = previous[node]
        node = prev[0] if prev else None
    path.reverse()
    return path, distances[goal]


def find_all_routes(graph, start, goal, max_depth=8):
    results = []

    def dfs(node, destination, visited, path, cost_distance, cost_time):
        if node == destination:
            results.append({
                "path": path.copy(),
                "distance": round(cost_distance, 2),
                "time": round(cost_time, 2),
            })
            return
        if len(path) >= max_depth:
            return
        for edge in graph[node]:
            nxt = edge["to"]
            if nxt in visited:
                continue
            visited.add(nxt)
            dfs(
                nxt,
                destination,
                visited,
                path + [nxt],
                cost_distance + edge["distance"],
                cost_time + edge["time"],
            )
            visited.remove(nxt)

    dfs(start, goal, {start}, [start], 0, 0)
    results.sort(key=lambda item: (item["distance"], item["time"]))
    return results[:5]


def agent1_best_route(graph, start_code, end_code):
    shortest_path, shortest_distance = dijkstra(
        graph, start_code, end_code, mode="distance")
    return {
        "best_path": shortest_path,
        "distance": shortest_distance,
        "label": "AI Agent 1: Shortest Distance Route",
    }


def agent2_traffic_aware_route(graph, start_code, end_code, time_label, traffic_value):
    base_multiplier = traffic_multiplier(time_label)
    slider_factor = slider_multiplier(traffic_value)
    combined_multiplier = base_multiplier * slider_factor
    random.seed((hash(start_code + end_code + time_label) %
                1000000) + traffic_value)

    traffic_hotspots = []
    traffic_aware_graph = defaultdict(list)

    for node, edges in graph.items():
        for edge in edges:
            random_factor = random.uniform(0.8, 2.7)
            if 0 <= traffic_value < 30:
                random_factor *= 0.9
            elif traffic_value >= 70:
                random_factor *= 1.35
            adjusted_time = edge["time"] * combined_multiplier * random_factor
            if random_factor > 1.55:
                traffic_hotspots.append({
                    "road": edge["name"],
                    "factor": round(random_factor, 2),
                    "nodes": (node, edge["to"]),
                })
            traffic_aware_graph[node].append({
                "to": edge["to"],
                "distance": edge["distance"],
                "time": adjusted_time,
                "name": edge["name"],
            })

    quickest_path, quickest_time = dijkstra(
        traffic_aware_graph, start_code, end_code, mode="time")
    return {
        "best_path": quickest_path,
        "time": quickest_time,
        "multiplier": combined_multiplier,
        "traffic_hotspots": traffic_hotspots[:6],
        "label": "AI Agent 2: Traffic-Aware Fastest Route",
    }


def compute_route(start_code, end_code, time_label, traffic_value=60):
    graph = build_graph()
    agent1 = agent1_best_route(graph, start_code, end_code)
    agent2 = agent2_traffic_aware_route(
        graph, start_code, end_code, time_label, traffic_value)
    all_routes = find_all_routes(graph, start_code, end_code)
    traffic_segments = generate_traffic_segments(
        graph, start_code, end_code, time_label, traffic_value)

    return {
        "shortest_path": agent1["best_path"],
        "shortest_distance": agent1["distance"],
        "quickest_path": agent2["best_path"],
        "quickest_time": agent2["time"],
        "all_routes": all_routes,
        "multiplier": agent2["multiplier"],
        "traffic_hotspots": agent2["traffic_hotspots"],
        "traffic_segments": traffic_segments,
        "agent1_label": agent1["label"],
        "agent2_label": agent2["label"],
    }


def resolve_location_code(value, all_locations):
    for code, name in all_locations:
        if name == value:
            return code
    return all_locations[0][0]
