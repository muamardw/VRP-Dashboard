import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

# Daftar koordinat (lat, lon) cabang
locations = [
    ("Cikampek", -6.4194, 107.4515),
    ("Jakarta", -6.2088, 106.8456),
    ("Bandung", -6.9175, 107.6191),
    ("Semarang", -6.9667, 110.4167),
    ("Surabaya", -7.2575, 112.7521),
    ("Yogyakarta", -7.7956, 110.3695),
    ("Cirebon", -6.7320, 108.5523),
    ("Tegal", -6.8694, 109.1403),
    ("Solo", -7.5666, 110.8166),
    ("Malang", -7.9819, 112.6265),
]

# Ambil peta jalan Pulau Jawa (atau area yang cukup besar)
G = ox.graph_from_place('Java, Indonesia', network_type='drive')

# Ambil node terdekat di graph untuk setiap lokasi
nodes = []
for name, lat, lon in locations:
    node = ox.nearest_nodes(G, lon, lat)
    nodes.append(node)

# Contoh: Visualisasi rute Cikampek ke Surabaya
start, end = nodes[0], nodes[4]
route = nx.shortest_path(G, start, end, weight='length')

# Plot peta dan rute
fig, ax = ox.plot_graph_route(G, route, node_size=0, bgcolor='white', route_color='red', route_linewidth=3)