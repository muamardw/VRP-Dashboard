import pandas as pd
from env.vrp_env import VRPDynamicEnv

# Data cabang di Pulau Jawa (depot di Cikampek)
data = [
    {"nama": "Cikampek", "latitude": -6.4194, "longitude": 107.4515, "demand": 0, "service_time": 0, "time_window_start": 0, "time_window_end": 24},
    {"nama": "Jakarta", "latitude": -6.2088, "longitude": 106.8456, "demand": 1, "service_time": 0.2, "time_window_start": 0, "time_window_end": 24},
    {"nama": "Bandung", "latitude": -6.9175, "longitude": 107.6191, "demand": 1, "service_time": 0.2, "time_window_start": 0, "time_window_end": 24},
    {"nama": "Semarang", "latitude": -6.9667, "longitude": 110.4167, "demand": 1, "service_time": 0.2, "time_window_start": 0, "time_window_end": 24},
    {"nama": "Surabaya", "latitude": -7.2575, "longitude": 112.7521, "demand": 1, "service_time": 0.2, "time_window_start": 0, "time_window_end": 24},
    {"nama": "Yogyakarta", "latitude": -7.7956, "longitude": 110.3695, "demand": 1, "service_time": 0.2, "time_window_start": 0, "time_window_end": 24},
    {"nama": "Cirebon", "latitude": -6.7320, "longitude": 108.5523, "demand": 1, "service_time": 0.2, "time_window_start": 0, "time_window_end": 24},
    {"nama": "Tegal", "latitude": -6.8694, "longitude": 109.1403, "demand": 1, "service_time": 0.2, "time_window_start": 0, "time_window_end": 24},
    {"nama": "Solo", "latitude": -7.5666, "longitude": 110.8166, "demand": 1, "service_time": 0.2, "time_window_start": 0, "time_window_end": 24},
    {"nama": "Malang", "latitude": -7.9819, "longitude": 112.6265, "demand": 1, "service_time": 0.2, "time_window_start": 0, "time_window_end": 24},
]

customers_df = pd.DataFrame(data)

# Inisialisasi environment
# Setiap perjalanan: depot -> satu cabang
for tujuan in range(1, len(customers_df)):
    print(f"Perjalanan dari Cikampek ke {customers_df.iloc[tujuan]['nama']}")
    env = VRPDynamicEnv(customers_df, n_vehicles=1)
    env.reset()
    # Langsung menuju cabang tujuan
    state, reward, done, info = env.step(tujuan)
    env.render() 