import pandas as pd
import numpy as np
from env.vrp_env import VRPDynamicEnv

# Membuat data customer dummy (depot + 9 customer)
def create_dummy_customers(n_customers=10, seed=42):
    np.random.seed(seed)
    # Depot di tengah koordinat (lat, lon)
    depot = {
        'latitude': 0.0,
        'longitude': 0.0,
        'demand': 0,
        'service_time': 0,
        'time_window_start': 0,
        'time_window_end': 24
    }
    customers = []
    for i in range(1, n_customers):
        customers.append({
            'latitude': np.random.uniform(-1, 1),
            'longitude': np.random.uniform(-1, 1),
            'demand': np.random.randint(1, 5),
            'service_time': np.random.uniform(0.1, 0.5),
            'time_window_start': np.random.uniform(0, 12),
            'time_window_end': np.random.uniform(12, 24)
        })
    data = [depot] + customers
    return pd.DataFrame(data)

# Membuat DataFrame dummy
customers_df = create_dummy_customers(n_customers=10)

# Inisialisasi environment
env = VRPDynamicEnv(customers_df, n_vehicles=1)

# Reset environment
state = env.reset()

# Lakukan beberapa langkah acak dan render
actions = [i for i in range(1, customers_df.shape[0])]
np.random.shuffle(actions)

for action in actions[:5]:
    state, reward, done, info = env.step(action)
    env.render()
    if done:
        break

# Render terakhir (jika ingin lihat state akhir)
env.render() 