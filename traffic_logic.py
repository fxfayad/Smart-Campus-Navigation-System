import random

TRAFFIC_COLORS = {
    "green": "#2ecc71",
    "yellow": "#f1c40f",
    "red": "#ff4d4d",
}


def traffic_level_for_factor(factor):
    if factor < 1.05:
        return "green"
    if factor < 1.7:
        return "yellow"
    return "red"


def generate_traffic_segments(graph, start_code, end_code, time_label, traffic_value):
    hour = int(time_label.split(":")[0])
    seed = sum(ord(ch)
               for ch in f"{start_code}{end_code}{time_label}{traffic_value}")
    rng = random.Random(seed)
    seen = set()
    segments = []

    for node, edges in graph.items():
        for edge in edges:
            neighbor = edge["to"]
            pair = tuple(sorted((node, neighbor)))
            if pair in seen:
                continue
            seen.add(pair)

            base = 0.85 + rng.random() * 2.1
            if 7 <= hour < 10 or 17 <= hour < 19:
                base *= 1.5
            if 10 <= hour < 12:
                base *= 1.2
            if traffic_value >= 75:
                base *= 1.35
            elif traffic_value <= 25:
                base *= 0.9
            if node in {start_code, end_code} or neighbor in {start_code, end_code}:
                base *= 1.1

            factor = round(base, 2)
            level = traffic_level_for_factor(factor)
            segments.append({
                "a": node,
                "b": neighbor,
                "name": edge["name"],
                "factor": factor,
                "level": level,
                "color": TRAFFIC_COLORS[level],
            })

    return sorted(segments, key=lambda item: (item["factor"], item["name"]))
