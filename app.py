import tkinter as tk
from tkinter import ttk, messagebox

from route_data import ALL_LOCATIONS, LABELS, NODE_POSITIONS, TIME_OPTIONS
from route_logic import compute_route, resolve_location_code
from traffic_logic import TRAFFIC_COLORS


BACKGROUND_MAP_FILES = [
    "campus_map.png",
    "campus_map.jpg",
    "campus_map.jpeg",
    "map.png",
    "map.jpg",
    "map.jpeg",
]


def get_background_map_path():
    from pathlib import Path

    base_dir = Path(__file__).resolve().parent
    for file_name in BACKGROUND_MAP_FILES:
        candidate = base_dir / file_name
        if candidate.exists():
            return str(candidate)
    return None


def draw_map_background(canvas):
    canvas.delete("map_bg")
    canvas.create_rectangle(
        0, 0, 1000, 700, fill="#eef5ef", outline="", tags="map_bg")

    for i in range(0, 1000, 120):
        canvas.create_line(i, 0, i, 700, fill="#d8dfd7",
                           width=1, tags="map_bg")
    for j in range(0, 700, 120):
        canvas.create_line(0, j, 1000, j, fill="#d8dfd7",
                           width=1, tags="map_bg")

    canvas.create_oval(50, 40, 200, 180, fill="#d9f0ff",
                       outline="#cef", width=2, tags="map_bg")
    canvas.create_oval(760, 75, 940, 220, fill="#d9f0ff",
                       outline="#cef", width=2, tags="map_bg")
    canvas.create_oval(430, 480, 620, 650, fill="#d9f0ff",
                       outline="#cef", width=2, tags="map_bg")

    roads = [
        (120, 100, 260, 100), (260, 100, 360, 200), (360,
                                                     200, 520, 120), (520, 120, 650, 220),
        (650, 220, 850, 250), (120, 100, 200, 220), (200,
                                                     220, 360, 200), (200, 220, 180, 340),
        (180, 340, 360, 360), (360, 360, 560, 340), (560,
                                                     340, 710, 360), (710, 360, 850, 250),
        (360, 360, 360, 200), (360, 200, 640, 220), (640,
                                                     220, 700, 120), (560, 340, 640, 220),
        (520, 120, 730, 120), (730, 120, 850, 250)
    ]
    for x1, y1, x2, y2 in roads:
        canvas.create_line(x1, y1, x2, y2, fill="#c0c8c7",
                           width=8, tags="map_bg")
        canvas.create_line(x1, y1, x2, y2, fill="#f7f7f7",
                           width=4, tags="map_bg")

    canvas.create_line(60, 200, 210, 410, fill="#7db0ff",
                       width=10, tags="map_bg")
    canvas.create_line(230, 420, 500, 420, fill="#7db0ff",
                       width=10, tags="map_bg")
    canvas.create_line(520, 420, 900, 430, fill="#7db0ff",
                       width=10, tags="map_bg")
    canvas.create_line(340, 90, 340, 520, fill="#7db0ff",
                       width=10, tags="map_bg")
    canvas.create_line(820, 120, 820, 610, fill="#7db0ff",
                       width=10, tags="map_bg")


def draw_route(canvas, route_nodes, route_color, glow_color):
    canvas.delete("route_highlight")
    if not route_nodes or len(route_nodes) < 2:
        return

    for idx in range(len(route_nodes) - 1):
        a = route_nodes[idx]
        b = route_nodes[idx + 1]
        ax, ay = NODE_POSITIONS[a]
        bx, by = NODE_POSITIONS[b]
        canvas.create_line(ax, ay, bx, by, fill=glow_color,
                           width=10, tags="route_highlight", capstyle=tk.ROUND)
        canvas.create_line(ax, ay, bx, by, fill=route_color,
                           width=6, tags="route_highlight", capstyle=tk.ROUND)


def draw_traffic_overlay(canvas, traffic_segments):
    if not traffic_segments:
        return

    for item in traffic_segments:
        a, b = item["a"], item["b"]
        ax, ay = NODE_POSITIONS[a]
        bx, by = NODE_POSITIONS[b]
        color = item["color"]
        canvas.create_line(ax, ay, bx, by, fill=color, width=12,
                           tags="traffic_overlay", capstyle=tk.ROUND, dash=(7, 5))
        canvas.create_line(
            ax,
            ay,
            bx,
            by,
            fill="#fff4c2" if color == TRAFFIC_COLORS[
                "yellow"] else "#ffd6d6" if color == TRAFFIC_COLORS["red"] else "#d9f9df",
            width=5,
            tags="traffic_overlay",
            capstyle=tk.ROUND,
        )


def draw_base_map(canvas, selected_route=None, alternate_route=None, traffic_segments=None):
    canvas.delete("all")
    background_path = get_background_map_path()
    if background_path:
        try:
            img = tk.PhotoImage(file=background_path)
            canvas.config(width=img.width(), height=img.height())
            canvas.create_image(0, 0, anchor="nw", image=img, tags="all")
            canvas.image = img
        except Exception:
            draw_map_background(canvas)
    else:
        draw_map_background(canvas)

    if traffic_segments:
        draw_traffic_overlay(canvas, traffic_segments)

    for node, (x, y) in NODE_POSITIONS.items():
        canvas.create_oval(x - 12, y - 12, x + 12, y + 12,
                           fill="#ffffff", outline="#3c4856", width=2, tags="all")
        canvas.create_text(x, y, text=node, fill="#0b1f2d",
                           font=("Arial", 10, "bold"), tags="all")
        canvas.create_text(
            x, y + 22, text=LABELS[node], fill="#1f2d3d", font=("Arial", 8), tags="all")

    if alternate_route and alternate_route != selected_route:
        draw_route(canvas, alternate_route, TRAFFIC_COLORS["red"], "#b22222")
    if selected_route:
        color = TRAFFIC_COLORS["green"]
        if any(seg["a"] in selected_route and seg["b"] in selected_route for seg in traffic_segments or []):
            color = TRAFFIC_COLORS["yellow"]
        draw_route(canvas, selected_route, color, "#1a7f4d")


def update_ui(location_var, destination_var, time_var, traffic_var, result_text, canvas):
    start_code = resolve_location_code(location_var.get(), ALL_LOCATIONS)
    end_code = resolve_location_code(destination_var.get(), ALL_LOCATIONS)
    selected_time = time_var.get()
    traffic_value = int(traffic_var.get())

    if start_code == end_code:
        messagebox.showinfo(
            "Notice", "Current location and destination cannot be the same.")
        return

    data = compute_route(start_code, end_code, selected_time, traffic_value)
    fastest_route = data["quickest_path"] if data["quickest_path"] else data["shortest_path"]
    shortest_route = data["shortest_path"]
    draw_base_map(canvas, fastest_route, shortest_route,
                  data.get("traffic_segments", []))

    summary = []
    summary.append("====================================")
    summary.append(f"From: {LABELS[start_code]} -> To: {LABELS[end_code]}")
    summary.append(
        f"Time: {selected_time} | Traffic intensity: {traffic_value}% | Factor: {data['multiplier']:.2f}x")
    summary.append(
        f"{data['agent1_label']}: {LABELS[start_code]} -> {' -> '.join(LABELS[n] for n in data['shortest_path'])} | Distance: {data['shortest_distance']:.1f} km"
    )
    summary.append(
        f"{data['agent2_label']}: {LABELS[start_code]} -> {' -> '.join(LABELS[n] for n in data['quickest_path'])} | Time: {data['quickest_time']:.1f} minutes"
    )
    if data["traffic_hotspots"]:
        hotspot_summary = ", ".join(
            f"{item['road']} ({item['factor']}x)" for item in data["traffic_hotspots"])
        summary.append(f"Traffic warning: {hotspot_summary}")
    summary.append("")
    summary.append("Other possible routes:")
    for idx, route in enumerate(data["all_routes"][:4], start=1):
        route_names = " -> ".join(LABELS[n] for n in route["path"])
        summary.append(
            f"{idx}. {route_names} | {route['distance']:.1f} km | {route['time']:.1f} minutes")

    result_text.config(state="normal")
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, "\n".join(summary))
    result_text.config(state="disabled")


def make_app():
    root = tk.Tk()
    root.title("University of Chittagong Route Planner")
    root.geometry("1420x820")
    root.minsize(1200, 700)
    root.configure(bg="#eaf1ea")

    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("Map.TFrame", background="#f4f7f4")
    style.configure("Sidebar.TFrame", background="#f9faf9")
    style.configure("TLabel", background="#f9faf9", foreground="#1d2833")
    style.configure("TButton", padding=(14, 8))

    outer = ttk.Frame(root, padding=10)
    outer.pack(fill=tk.BOTH, expand=True)

    map_panel = ttk.Frame(outer, style="Map.TFrame", padding=14)
    map_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    topbar = ttk.Frame(map_panel)
    topbar.pack(fill=tk.X, pady=(0, 10))

    ttk.Label(topbar, text="Route Search", font=(
        "Arial", 16, "bold")).pack(side=tk.LEFT)
    ttk.Label(topbar, text="Google Maps style planner", font=(
        "Arial", 10), foreground="#5b6470").pack(side=tk.LEFT, padx=(14, 0))

    canvas = tk.Canvas(map_panel, width=980, height=620, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    draw_base_map(canvas)

    sidebar = ttk.Frame(outer, style="Sidebar.TFrame", width=360, padding=16)
    sidebar.pack(side=tk.RIGHT, fill=tk.Y)

    ttk.Label(sidebar, text="CU Route Planner", font=(
        "Arial", 18, "bold")).pack(anchor="w", pady=(0, 16))

    ttk.Label(sidebar, text="Current Location", font=(
        "Arial", 11, "bold")).pack(anchor="w")
    location_var = tk.StringVar(value="1 No. Gate")
    location_combo = ttk.Combobox(sidebar, textvariable=location_var, values=[
                                  name for _, name in ALL_LOCATIONS], state="readonly", width=30)
    location_combo.pack(anchor="w", pady=(6, 12))

    ttk.Label(sidebar, text="Destination", font=(
        "Arial", 11, "bold")).pack(anchor="w")
    destination_var = tk.StringVar(value="2 No. Gate")
    destination_combo = ttk.Combobox(sidebar, textvariable=destination_var, values=[
                                     name for _, name in ALL_LOCATIONS], state="readonly", width=30)
    destination_combo.pack(anchor="w", pady=(6, 12))

    ttk.Label(sidebar, text="Time of Day", font=(
        "Arial", 11, "bold")).pack(anchor="w")
    time_var = tk.StringVar(value="10:00")
    time_combo = ttk.Combobox(
        sidebar, textvariable=time_var, values=TIME_OPTIONS, state="readonly", width=30)
    time_combo.pack(anchor="w", pady=(6, 12))

    traffic_frame = ttk.Frame(sidebar)
    traffic_frame.pack(fill=tk.X, pady=(4, 12))
    ttk.Label(traffic_frame, text="Traffic Intensity",
              font=("Arial", 11, "bold")).pack(anchor="w")
    traffic_var = tk.IntVar(value=60)
    slider = tk.Scale(traffic_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                      variable=traffic_var, length=260, showvalue=True, sliderrelief="flat")
    slider.pack(fill=tk.X)

    def refresh_route(event=None):
        update_ui(location_var, destination_var, time_var,
                  traffic_var, result_text, canvas)

    location_combo.bind("<<ComboboxSelected>>", refresh_route)
    destination_combo.bind("<<ComboboxSelected>>", refresh_route)
    time_combo.bind("<<ComboboxSelected>>", refresh_route)
    traffic_var.trace_add("write", lambda *_: refresh_route())

    go_btn = ttk.Button(sidebar, text="Find Best Route", command=refresh_route)
    go_btn.pack(fill=tk.X, pady=(8, 16))

    result_container = ttk.LabelFrame(
        sidebar, text="Route Details", padding=(8, 8))
    result_container.pack(fill=tk.BOTH, expand=True)

    result_text = tk.Text(result_container, height=22,
                          wrap=tk.WORD, font=("Arial", 10), bg="#f7f7f7")
    result_text.pack(fill=tk.BOTH, expand=True)
    result_text.config(state="disabled")

    update_ui(location_var, destination_var, time_var,
              traffic_var, result_text, canvas)
    root.mainloop()


if __name__ == "__main__":
    make_app()
