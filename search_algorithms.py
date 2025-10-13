import json
import os
import heapq
import time
import random

def load_graph(filename="transport_graph.json"):
    """Memuat struktur graf dari file JSON."""
    try:
        with open(filename, 'r') as f:
            graph = json.load(f)
        print(f"✅ Graf dari '{filename}' berhasil dimuat.")
        return graph
    except FileNotFoundError:
        print(f"❌ GAGAL: File '{filename}' tidak ditemukan.")
        return None

def a_star_search(graph, start_node, end_node, cost_type='distance'):
    """Menemukan rute optimal menggunakan algoritma A* (Dijkstra)."""
    if start_node not in graph or end_node not in graph: return None, float('inf'), 0
    pq = [(0, [start_node])]; visited = set(); nodes_explored = 0
    while pq:
        cost, path = heapq.heappop(pq); node = path[-1]
        if node in visited: continue
        visited.add(node); nodes_explored += 1
        if node == end_node: return path, cost, nodes_explored
        for neighbor, attrs in graph.get(node, []):
            if neighbor not in visited:
                new_cost = cost + attrs.get(cost_type, 0)
                heapq.heappush(pq, (new_cost, path + [neighbor]))
    return None, float('inf'), nodes_explored

def greedy_bfs_search(graph, start_node, end_node, cost_type='distance'):
    """Menemukan rute menggunakan algoritma Greedy BFS."""
    if start_node not in graph or end_node not in graph: return None, float('inf'), 0
    pq = [(0, [start_node])]; visited = set(); nodes_explored = 0
    while pq:
        _, path = heapq.heappop(pq); node = path[-1]
        if node in visited: continue
        visited.add(node); nodes_explored += 1
        if node == end_node:
            total_cost = calculate_path_cost(graph, path, cost_type)
            return path, total_cost, nodes_explored
        for neighbor, attrs in graph.get(node, []):
            if neighbor not in visited:
                edge_cost = attrs.get(cost_type, 0)
                heapq.heappush(pq, (edge_cost, path + [neighbor]))
    return None, float('inf'), nodes_explored

def calculate_path_cost(graph, path, cost_type):
    """Menghitung total biaya (jarak/harga) dari sebuah rute."""
    total_cost = 0
    for i in range(len(path) - 1):
        u, v = path[i], path[i+1]
        found_edge = False
        for neighbor, attrs in graph.get(u, []):
            if neighbor == v:
                total_cost += attrs.get(cost_type, 0)
                found_edge = True
                break
        if not found_edge: return float('inf')
    return total_cost

def find_initial_solution(graph, start_node, end_node):
    """Mencari satu rute valid apapun menggunakan Depth-First Search."""
    stack = [(start_node, [start_node])]
    visited = {start_node}
    while stack:
        (node, path) = stack.pop()
        if node == end_node:
            return path
        for neighbor, _ in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, path + [neighbor]))
    return None

def hill_climbing_search(graph, start_node, end_node, cost_type, max_iterations=1000):
    """Mencari rute menggunakan algoritma Hill Climbing."""
    current_path = find_initial_solution(graph, start_node, end_node)
    if not current_path:
        return None, float('inf'), 0
    
    current_cost = calculate_path_cost(graph, current_path, cost_type)
    nodes_explored = 1

    for i in range(max_iterations):
        nodes_explored +=1
        if len(current_path) <= 2: break

        node_to_change_idx = random.randint(1, len(current_path) - 2)
        node_before = current_path[node_to_change_idx - 1]
        
        possible_new_nodes = [n for n, a in graph.get(node_before, []) if n not in current_path]
        if not possible_new_nodes:
            continue
        
        new_mid_node = random.choice(possible_new_nodes)

        path_head = current_path[:node_to_change_idx]
        path_tail_start = new_mid_node
        
        new_path_tail = find_initial_solution(graph, path_tail_start, end_node)
        
        if new_path_tail:
            neighbor_path = path_head + new_path_tail
            neighbor_cost = calculate_path_cost(graph, neighbor_path, cost_type)

            if neighbor_cost < current_cost:
                current_path = neighbor_path
                current_cost = neighbor_cost
    
    return current_path, current_cost, nodes_explored

def get_user_choice(locations, prompt_message):
    """Menampilkan daftar lokasi dan meminta user memilih berdasarkan nomor."""
    os.system('cls')
    print(f"\n{prompt_message}")
    for i, location in enumerate(locations): print(f"  {i + 1}. {location}")
    while True:
        try:
            choice = int(input(">> Masukkan nomor pilihan Anda: "));
            if 1 <= choice <= len(locations): return locations[choice - 1]
            else: print("   ⚠️ Pilihan tidak valid.")
        except ValueError: print("   ⚠️ Input tidak valid.")

if __name__ == '__main__':
    graph = load_graph()
    if not graph: exit()

    all_locations = sorted(list(graph.keys()))
    start_loc = get_user_choice(all_locations, "--- PILIH LOKASI AWAL ---")
    end_loc = get_user_choice(all_locations, "--- PILIH LOKASI TUJUAN ---")
    while start_loc == end_loc:
        print("\n⚠️ Titik awal dan tujuan tidak boleh sama."); end_loc = get_user_choice(all_locations, "--- PILIH LOKASI TUJUAN ---")

    os.system('cls')
    print(f"\n🔍 Mencari Rute dari [{start_loc}] ke [{end_loc}]")
    
    # --- A* Search ---
    print("\n======================= A* Search =======================")
    for cost_type in ['distance', 'price']:
        start_time = time.time()
        path, cost, nodes = a_star_search(graph, start_loc, end_loc, cost_type)
        end_time = time.time()
        if path:
            unit = "mil" if cost_type == 'distance' else "USD"
            prefix = "" if cost_type == 'distance' else "$"
            print(f"\n--- Skenario {cost_type.title()} ---")
            print(f"  Rute: {' -> '.join(path)}")
            print(f"  Total: {prefix}{cost:.2f} {unit} | Node Dieksplorasi: {nodes} | Waktu: {(end_time - start_time) * 1000:.4f} ms")

    # --- Greedy BFS ---
    print("\n\n============ Greedy Best-First Search ============")
    for cost_type in ['distance', 'price']:
        start_time = time.time()
        path, cost, nodes = greedy_bfs_search(graph, start_loc, end_loc, cost_type)
        end_time = time.time()
        if path:
            unit = "mil" if cost_type == 'distance' else "USD"
            prefix = "" if cost_type == 'distance' else "$"
            print(f"\n--- Skenario {cost_type.title()} ---")
            print(f"  Rute: {' -> '.join(path)}")
            print(f"  Total: {prefix}{cost:.2f} {unit} | Node Dieksplorasi: {nodes} | Waktu: {(end_time - start_time) * 1000:.4f} ms")

    # --- Hill Climbing ---
    print("\n\n=============== Hill Climbing ================")
    for cost_type in ['distance', 'price']:
        start_time = time.time()
        path, cost, nodes = hill_climbing_search(graph, start_loc, end_loc, cost_type)
        end_time = time.time()
        if path:
            unit = "mil" if cost_type == 'distance' else "USD"
            prefix = "" if cost_type == 'distance' else "$"
            print(f"\n--- Skenario {cost_type.title()} ---")
            print(f"  Rute: {' -> '.join(path)}")
            print(f"  Total: {prefix}{cost:.2f} {unit} | Iterasi: {nodes} | Waktu: {(end_time - start_time) * 1000:.4f} ms")
    print("=======================================================================")
