import pandas as pd
import json

def create_graph_from_csv(file_path='cab_rides.csv'):
    """
    Memuat data perjalanan dari file CSV, membersihkannya, dan membangun
    representasi graf dalam bentuk adjacency list, lalu menyimpannya ke file JSON.
    """
    # Langkah 1: Memuat dataset
    try:
        df = pd.read_csv(file_path)
        print(f"✅ Dataset '{file_path}' berhasil dimuat.")
    except FileNotFoundError:
        print(f"❌ GAGAL: File '{file_path}' tidak ditemukan. Mohon periksa nama dan lokasi file.")
        return

    # Langkah 2: Membersihkan data dari nilai yang kosong
    initial_rows = len(df)
    df.dropna(subset=['source', 'destination', 'distance', 'price'], inplace=True)
    cleaned_rows = len(df)
    print(f"🧹 Data dibersihkan. Sisa baris: {cleaned_rows} dari {initial_rows} baris awal.")

    # Langkah 3: Membangun representasi graf (Adjacency List)
    graph = {}
    print("\n⏳ Membangun graf dari data perjalanan...")

    for _, row in df.iterrows():
        source = row['source']
        dest = row['destination']
        distance = row['distance']
        price = float(row['price'])  # Memastikan harga bertipe float

        if source not in graph:
            graph[source] = []
        
        graph[source].append((dest, {'distance': distance, 'price': price}))

    # Memastikan semua lokasi unik ada sebagai 'key' di graf
    all_locations = set(df['source']).union(set(df['destination']))
    for location in all_locations:
        if location not in graph:
            graph[location] = []

    num_nodes = len(graph)
    print(f"🎉 Graf berhasil dibuat! Terdiri dari {num_nodes} lokasi unik (nodes).")

    # Langkah 4: Menyimpan graf ke dalam file JSON
    graph_filename = 'transport_graph.json'
    try:
        with open(graph_filename, 'w') as f:
            json.dump(graph, f, indent=2)
        print(f"💾 Representasi graf telah disimpan ke file: '{graph_filename}'")
    except Exception as e:
        print(f"❌ GAGAL menyimpan file JSON. Error: {e}")

# Panggil fungsi untuk menjalankan proses
if __name__ == '__main__':
    create_graph_from_csv()
