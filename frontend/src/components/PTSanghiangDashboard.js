import React, { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline, CircleMarker } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import './PTSanghiangDashboard.css';

// Fix untuk icon Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

const PTSanghiangDashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedRoute, setSelectedRoute] = useState(null);
  const [panelOpen, setPanelOpen] = useState(false);
  const [trafficData, setTrafficData] = useState({});
  const [weatherData, setWeatherData] = useState({});
  const [vehiclePositions, setVehiclePositions] = useState([]);
  const [map, setMap] = useState(null);
  const mapRef = useRef(null);

  // Koordinat depot PT. Sanghiang Perkasa - Pulogadung, Jakarta Timur
  const depotCoordinates = [-6.1857, 106.9367];

  // Koordinat destinasi berdasarkan alamat lengkap
  const destinations = [
    {
      id: 'C25',
      name: 'Bogor',
      address: 'Jl. Wangun no. 216 Sindangsari Bogor Timur 16720',
      coordinates: [-6.5971, 106.8060],
      distance: 60,
      capacity: 2000,
      load: 2000,
      utilization: 100
    },
    {
      id: 'C26', 
      name: 'Tangerang',
      address: 'JL. PAJAJARAN, RT 001/003 KEL GANDASARI, KEC JATIUWUNG, TANGERANG 15137',
      coordinates: [-6.1783, 106.6319],
      distance: 55,
      capacity: 1000,
      load: 700,
      utilization: 70
    },
    {
      id: 'C27',
      name: 'Jakarta',
      address: 'Jl. Srengseng Raya No.8, RT.2/RW.8, Srengseng, Kec. Kembangan, Kota Jakarta Barat',
      coordinates: [-6.1778, 106.7378],
      distance: 17,
      capacity: 2000,
      load: 1700,
      utilization: 85
    },
    {
      id: 'C28',
      name: 'Bekasi', 
      address: 'Jl. Jakasetia no. 27 B, Kp. Poncol, Kel. Jakasetia, Bekasi Selatan 17423',
      coordinates: [-6.2346, 106.9896],
      distance: 10,
      capacity: 1000,
      load: 500,
      utilization: 50
    }
  ];

  // Fallback data untuk PT. Sanghiang Perkasa dengan 4 destinasi
  const fallbackData = {
    success: true,
    routes: [
      {
        destination: "Bogor",
        location: { lat: -6.5950, lng: 106.8167 },
        distance_km: 60.0,
        eta: 1.2,
        traffic_level: "moderate",
        traffic_color: "#ffaa00",
        vehicle_type: "Truck Sedang",
        capacity_kg: 2000,
        utilization: 100,
        current_load: 2000,
        estimated_time: 100,
        estimated_arrival: 1.2,
        utilization_percent: 100,
        weather: {
          description: "Cerah Berawan",
          temperature: 28,
          humidity: 75
        },
        road_segments: [
          { road_name: "Tol Jagorawi", length_km: 45, traffic_level: "Lancar" },
          { road_name: "Jalan Raya Bogor", length_km: 15, traffic_level: "Sedang" }
        ]
      },
      {
        destination: "Tangerang",
        location: { lat: -6.1783, lng: 106.6319 },
        distance_km: 55.0,
        eta: 1.1,
        traffic_level: "heavy",
        traffic_color: "#ff4444",
        vehicle_type: "Truck Kecil",
        capacity_kg: 1000,
        utilization: 70,
        current_load: 700,
        estimated_time: 90,
        estimated_arrival: 1.1,
        utilization_percent: 70,
        weather: {
          description: "Hujan Ringan",
          temperature: 26,
          humidity: 85
        },
        road_segments: [
          { road_name: "Tol Jakarta-Tangerang", length_km: 40, traffic_level: "Macet" },
          { road_name: "Jalan Raya Tangerang", length_km: 15, traffic_level: "Sedang" }
        ]
      },
      {
        destination: "Jakarta",
        location: { lat: -6.2088, lng: 106.8456 },
        distance_km: 17.0,
        eta: 0.8,
        traffic_level: "heavy",
        traffic_color: "#ff4444",
        vehicle_type: "Truck Sedang",
        capacity_kg: 2000,
        utilization: 85,
        current_load: 1700,
        estimated_time: 60,
        estimated_arrival: 0.8,
        utilization_percent: 85,
        weather: {
          description: "Cerah",
          temperature: 30,
          humidity: 70
        },
        road_segments: [
          { road_name: "Tol Dalam Kota", length_km: 12, traffic_level: "Macet" },
          { road_name: "Jalan Arteri Jakarta", length_km: 5, traffic_level: "Sedang" }
        ]
      },
      {
        destination: "Bekasi",
        location: { lat: -6.2349, lng: 106.9896 },
        distance_km: 10.0,
        eta: 0.5,
        traffic_level: "light",
        traffic_color: "#44ff44",
        vehicle_type: "Truck Kecil",
        capacity_kg: 1000,
        utilization: 50,
        current_load: 500,
        estimated_time: 30,
        estimated_arrival: 0.5,
        utilization_percent: 50,
        weather: {
          description: "Cerah Berawan",
          temperature: 29,
          humidity: 72
        },
        road_segments: [
          { road_name: "Tol Jakarta-Cikampek", length_km: 8, traffic_level: "Lancar" },
          { road_name: "Jalan Raya Bekasi", length_km: 2, traffic_level: "Lancar" }
        ]
      }
    ],
    statistics: {
      total_routes: 4,
      total_distance_km: 142.0,
      average_utilization: 76.25,
      active_vehicles: 4
    }
  };

  const transformRouteInfoData = (data) => {
    if (!data || !data.routes) return fallbackData;
    
    return {
      ...data,
      routes: data.routes.map(route => ({
        ...route,
        location: route.location || route.end_location,
        distance_km: route.distance_km || route.distance,
        eta: route.eta || route.estimated_arrival,
        traffic_level: route.traffic_level || 'moderate',
        traffic_color: route.traffic_color || '#ffaa00',
        vehicle_type: route.vehicle_type || 'Truck',
        capacity_kg: route.capacity_kg || route.capacity,
        utilization: route.utilization || route.utilization_percent || 0,
        current_load: route.current_load || route.load,
        estimated_time: route.estimated_time || 60,
        estimated_arrival: route.estimated_arrival || route.eta,
        utilization_percent: route.utilization_percent || route.utilization,
        weather: route.weather || {
          description: "Cerah Berawan",
          temperature: 28,
          humidity: 75
        },
        road_segments: route.road_segments || [
          { road_name: "Jalan Utama", length_km: route.distance_km || 10, traffic_level: "Sedang" }
        ]
      }))
    };
  };

  const fetchPTSanghiangData = async () => {
    try {
      setLoading(true);
      
      // Simulasi API call dengan delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Gunakan fallback data untuk demo
      const transformedData = transformRouteInfoData(fallbackData);
      setData(transformedData);
      
      // Simulasi vehicle positions
      const vehiclePositions = transformedData.routes.map((route, index) => ({
        id: `vehicle-${index + 1}`,
        position: route.location,
        route: route.destination,
        type: route.vehicle_type,
        load: route.current_load,
        capacity: route.capacity_kg
      }));
      setVehiclePositions(vehiclePositions);
      
    } catch (error) {
      console.error('Error fetching data:', error);
      setError('Gagal memuat data. Menggunakan data demo.');
      setData(transformRouteInfoData(fallbackData));
    } finally {
      setLoading(false);
    }
  };

  const fetchTrafficAndWeatherData = async () => {
    try {
      // Simulasi traffic dan weather data
      const trafficData = {
        Bogor: { level: 'moderate', color: '#ffaa00' },
        Tangerang: { level: 'heavy', color: '#ff4444' },
        Jakarta: { level: 'heavy', color: '#ff4444' },
        Bekasi: { level: 'light', color: '#44ff44' }
      };
      
      const weatherData = {
        Bogor: { condition: 'Cerah Berawan', temp: 28, humidity: 75 },
        Tangerang: { condition: 'Hujan Ringan', temp: 26, humidity: 85 },
        Jakarta: { condition: 'Cerah', temp: 30, humidity: 70 },
        Bekasi: { condition: 'Cerah Berawan', temp: 29, humidity: 72 }
      };
      
      setTrafficData(trafficData);
      setWeatherData(weatherData);
    } catch (error) {
      console.error('Error fetching traffic/weather data:', error);
    }
  };

  const getTrafficColor = (city) => {
    return trafficData[city]?.color || '#ffaa00';
  };

  const getWeatherColor = (city) => {
    const condition = weatherData[city]?.condition?.toLowerCase() || 'cerah';
    if (condition.includes('hujan')) return '#007bff';
    if (condition.includes('berawan')) return '#6c757d';
    return '#ffc107';
  };

  const getUtilizationColor = (utilization) => {
    if (utilization >= 80) return '#28a745';
    if (utilization >= 60) return '#ffc107';
    return '#dc3545';
  };

  const createVehicleIcon = (weatherColor) => {
    return L.divIcon({
      className: 'vehicle-marker',
      html: `
        <div class="vehicle-icon" style="background: linear-gradient(135deg, ${weatherColor}, #1e7e34);">
          <div class="vehicle-number">🚚</div>
          <div class="vehicle-type">TRUCK</div>
        </div>
      `,
      iconSize: [40, 40],
      iconAnchor: [20, 20]
    });
  };

  const renderRoadSegments = (roadSegments) => {
    if (!roadSegments || roadSegments.length === 0) return null;
    
    return (
      <div className="road-segments">
        <h5>Jalan yang dilewati:</h5>
        {roadSegments.map((segment, index) => (
          <div key={index} className="road-segment">
            <strong>{segment.road_name}</strong> ({segment.length_km || segment.length} km)
            <br />
            <small>Traffic: {segment.traffic_level}</small>
          </div>
        ))}
      </div>
    );
  };

  const renderTrafficIcon = (level) => {
    const iconMap = {
      'light': '🟢',
      'moderate': '🟡',
      'heavy': '🔴'
    };
    
    return iconMap[level] || '🟡';
  };

  const renderWeatherIcon = (weather) => {
    const description = weather?.description?.toLowerCase() || '';
    
    if (description.includes('hujan')) return '🌧️';
    if (description.includes('berawan')) return '☁️';
    if (description.includes('cerah')) return '☀️';
    
    return '🌤️';
  };

  const renderDepotMarker = () => {
    console.log('🔍 Rendering depot marker at:', depotCoordinates);
    
    // Create a simple custom icon
    const depotIcon = L.divIcon({
      className: 'depot-marker',
      html: `
        <div style="
          background: #dc3545;
          color: white;
          padding: 8px 12px;
          border-radius: 15px;
          box-shadow: 0 2px 8px rgba(0,0,0,0.3);
          text-align: center;
          font-weight: bold;
          border: 2px solid white;
          min-width: 70px;
          font-size: 11px;
          z-index: 1000;
        ">
          <div style="font-size: 14px;">🏢</div>
          <div style="font-size: 9px;">DEPOT</div>
        </div>
      `,
      iconSize: [70, 50],
      iconAnchor: [35, 25]
    });

    console.log('🏢 Depot icon created:', depotIcon);

    return (
      <Marker 
        position={depotCoordinates}
        icon={depotIcon}
        zIndexOffset={1000}
      >
        <Popup>
          <div className="depot-popup">
            <h4>🏢 PT. Sanghiang Perkasa</h4>
            <p><strong>📍 Lokasi:</strong> Jakarta Pusat</p>
            <p><strong>🏭 Status:</strong> Depot Utama</p>
            <p><strong>📦 Kapasitas:</strong> 10,000 kg</p>
            <p><strong>🛣️ Terhubung ke:</strong></p>
            <ul style={{ margin: '5px 0', paddingLeft: '20px' }}>
              <li>📍 Bogor (C25) - 60 km</li>
              <li>📍 Tangerang (C26) - 55 km</li>
              <li>📍 Jakarta (C27) - 17 km</li>
              <li>📍 Bekasi (C28) - 10 km</li>
            </ul>
            <p><strong>🚚 Kendaraan Aktif:</strong> 4 unit</p>
            <p><strong>📊 Total Jarak:</strong> 142 km</p>
          </div>
        </Popup>
      </Marker>
    );
  };

  // Helper function to format ETA
  const formatETA = (eta) => {
    if (eta < 1) {
      const minutes = Math.round(eta * 60);
      return `${minutes} menit`;
    } else {
      const hours = Math.floor(eta);
      const minutes = Math.round((eta - hours) * 60);
      if (minutes === 0) {
        return `${hours} jam`;
      } else {
        return `${hours} jam ${minutes} menit`;
      }
    }
  };

  const renderRouteMarkers = () => {
    if (!data || !data.routes) return null;
    
    return data.routes.map((route, index) => {
      const position = route.location || route.end_location;
      if (!position || !position.lat || !position.lng) return null;
      
      return (
        <Marker 
          key={`route-${index}`}
          position={[position.lat, position.lng]}
          icon={L.divIcon({
            className: 'route-marker',
            html: `
              <div class="marker-content">
                <div class="marker-number">${index + 1}</div>
                <div class="marker-destination">${route.destination}</div>
              </div>
            `,
            iconSize: [60, 40],
            iconAnchor: [30, 20]
          })}
          eventHandlers={{
            click: () => setSelectedRoute(route)
          }}
        >
          <Popup>
            <div className="route-popup">
              <h4>{route.destination}</h4>
              <p><strong>Jarak:</strong> {route.distance_km} km</p>
              <p><strong>ETA:</strong> {formatETA(route.estimated_arrival || route.eta)}</p>
              <p><strong>Kendaraan:</strong> {route.vehicle_type}</p>
              <p><strong>Kapasitas:</strong> {route.capacity_kg} kg</p>
              <p><strong>Utilisasi:</strong> {route.utilization_percent || route.utilization}%</p>
              <p><strong>Traffic:</strong> {route.traffic_level}</p>
              <p><strong>Cuaca:</strong> {route.weather?.description || 'Tidak tersedia'}</p>
              {renderRoadSegments(route.road_segments)}
            </div>
          </Popup>
        </Marker>
      );
    });
  };

  const renderRoutePolylines = () => {
    if (!data || !data.routes) return null;
    
    return data.routes.map((route, index) => {
      const position = route.location || route.end_location;
      if (!position || !position.lat || !position.lng) return null;
      
      const positions = [depotCoordinates, [position.lat, position.lng]];
      
      return (
        <Polyline 
          key={`polyline-${index}`}
          positions={positions}
          color={getTrafficColor(route.destination)}
          weight={4}
          opacity={0.8}
          dashArray="10, 5"
        >
          <Popup>
            <div className="polyline-popup">
              <h5>🛣️ Rute ke {route.destination}</h5>
              <p><strong>📍 Jarak:</strong> {route.distance_km} km</p>
              <p><strong>⏱️ Waktu:</strong> {formatETA(route.estimated_arrival || route.eta)}</p>
              <p><strong>🚦 Traffic:</strong> {route.traffic_level}</p>
              <p><strong>🚚 Kendaraan:</strong> {route.vehicle_type}</p>
              <p><strong>📦 Muatan:</strong> {route.current_load || route.load} / {route.capacity_kg} kg</p>
            </div>
          </Popup>
        </Polyline>
      );
    });
  };

  const renderVehicleMarkers = () => {
    return vehiclePositions.map((vehicle, index) => {
      if (!vehicle.position || !vehicle.position.lat || !vehicle.position.lng) return null;
      
      const weatherColor = getWeatherColor(vehicle.route);
      
      return (
        <Marker 
          key={vehicle.id}
          position={[vehicle.position.lat, vehicle.position.lng]}
          icon={createVehicleIcon(weatherColor)}
        >
          <Popup>
            <div className="vehicle-popup">
              <h5>Kendaraan {index + 1}</h5>
              <p><strong>Rute:</strong> {vehicle.route}</p>
              <p><strong>Tipe:</strong> {vehicle.type}</p>
              <p><strong>Muatan:</strong> {vehicle.load} / {vehicle.capacity} kg</p>
            </div>
          </Popup>
        </Marker>
      );
    });
  };

  const renderTrafficMarkers = () => {
    if (!data || !data.routes) return null;
    
    const markers = [];
    
    data.routes.forEach((route, index) => {
      const position = route.location || route.end_location;
      
      if (position && position.lat && position.lng) {
        const trafficIcon = L.divIcon({
          className: 'traffic-icon',
          html: `
            <div style="font-size: 20px; color: ${getTrafficColor(route.destination)};">
              ${renderTrafficIcon(route.traffic_level)}
            </div>
          `,
          iconSize: [20, 20]
        });

        markers.push(
          <Marker 
            key={`traffic-${index}`}
            position={[position.lat, position.lng]}
            icon={trafficIcon}
          >
            <Popup>
              <div className="traffic-popup">
                <h5>Traffic Info</h5>
                <p><strong>Kondisi:</strong> {route.traffic_level}</p>
                <p><strong>Lokasi:</strong> {route.destination}</p>
              </div>
            </Popup>
          </Marker>
        );
      }
    });

    return markers;
  };

  const renderWeatherMarkers = () => {
    if (!data || !data.routes) return null;
    
    const markers = [];
    
    data.routes.forEach((route, index) => {
      const position = route.location || route.end_location;
      
      if (position && position.lat && position.lng && route.weather) {
        const weatherIcon = (() => {
          const description = route.weather?.description?.toLowerCase() || 'sunny';
          
          if (description.includes('rain') || description.includes('hujan')) {
            return L.divIcon({
              className: 'weather-icon weather-rain',
              html: '🌧️',
              iconSize: [20, 20]
            });
          } else if (description.includes('cloud') || description.includes('berawan')) {
            return L.divIcon({
              className: 'weather-icon weather-cloudy',
              html: '☁️',
              iconSize: [20, 20]
            });
          } else {
            return L.divIcon({
              className: 'weather-icon weather-sunny',
              html: '☀️',
              iconSize: [20, 20]
            });
          }
        })();

        markers.push(
          <Marker 
            key={`weather-${index}`}
            position={[position.lat, position.lng]}
            icon={weatherIcon}
          >
            <Popup>
              <div className="weather-popup">
                <h5>Weather Info</h5>
                <p><strong>Kondisi:</strong> {route.weather.description}</p>
                <p><strong>Lokasi:</strong> {route.destination}</p>
              </div>
            </Popup>
          </Marker>
        );
      }
    });

    return markers;
  };

  useEffect(() => {
    fetchPTSanghiangData();
  }, []);

  useEffect(() => {
    fetchTrafficAndWeatherData();
  }, []);

  useEffect(() => {
    if (!data) return;
    
    const interval = setInterval(() => {
      fetchPTSanghiangData();
    }, 30000); // Update every 30 seconds
    
    return () => clearInterval(interval);
  }, [data]);

  useEffect(() => {
    if (!data) return;
    
    const interval = setInterval(() => {
      fetchTrafficAndWeatherData();
    }, 60000); // Update every minute
    
    return () => clearInterval(interval);
  }, [data]);

  // Debug effect for depot marker
  useEffect(() => {
    console.log('🗺️ Map container ready, depot coordinates:', depotCoordinates);
    console.log('🏢 Depot marker function:', renderDepotMarker);
    
    // Force map to center on depot
    if (map) {
      console.log('🗺️ Setting map center to depot:', depotCoordinates);
      map.setView(depotCoordinates, 10);
    }
  }, [map]);

  if (loading) {
    return (
      <div className="dashboard-container">
        <div className="loading-spinner">
          Memuat data PT. Sanghiang Perkasa...
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-container">
        <div className="error-message">
          {error}
          <button onClick={fetchPTSanghiangData} style={{ marginLeft: '10px', padding: '5px 10px' }}>
            Coba Lagi
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1 className="dashboard-title">🏢 PT. Sanghiang Perkasa - Vehicle Routing Dashboard</h1>
        <p className="dashboard-subtitle">Sistem Manajemen Rute Kendaraan dengan Real-time Traffic & Weather</p>
        <div style={{
          background: 'linear-gradient(135deg, #dc3545, #c82333)',
          color: 'white',
          padding: '10px 20px',
          borderRadius: '10px',
          marginTop: '10px',
          textAlign: 'center',
          boxShadow: '0 4px 10px rgba(220, 53, 69, 0.3)'
        }}>
          <strong>🏢 DEPOT PUSAT</strong> - Terhubung ke 4 Destinasi: 
          <span style={{ marginLeft: '10px', fontSize: '14px' }}>
            📍 Bogor (60km) | 📍 Tangerang (55km) | 📍 Jakarta (17km) | 📍 Bekasi (10km)
          </span>
        </div>
      </div>

      {data && data.statistics && (
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-value">{data.statistics.total_routes}</div>
            <div className="stat-label">Total Rute</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{data.statistics.total_distance_km?.toFixed(1)} km</div>
            <div className="stat-label">Total Jarak</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{data.statistics.average_utilization?.toFixed(1)}%</div>
            <div className="stat-label">Utilisasi Rata-rata</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{data.statistics.active_vehicles}</div>
            <div className="stat-label">Kendaraan Aktif</div>
          </div>
        </div>
      )}

      {/* Map Container */}
      <div className="map-container">
        <MapContainer
          center={depotCoordinates}
          zoom={10}
          style={{ height: '600px', width: '100%' }}
          ref={mapRef}
          whenCreated={setMap}
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          />

          {/* Render all map components */}
          {/* Depot Marker - Direct */}
          <Marker 
            position={depotCoordinates}
            icon={L.icon({
              iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
              shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
              iconSize: [25, 41],
              iconAnchor: [12, 41],
              popupAnchor: [1, -34],
              shadowSize: [41, 41]
            })}
            zIndexOffset={1000}
          >
            <Popup>
              <div className="depot-popup">
                <h4>🏢 PT. Sanghiang Perkasa</h4>
                <p><strong>📍 Lokasi:</strong> Pulogadung, Jakarta Timur</p>
                <p><strong>🏭 Alamat:</strong> Kw. Industri Pulogadung, Jl. Pulo Lentut No.10, RW.3, Rw. Terate, Kec. Cakung, Kota Jakarta Timur</p>
                <p><strong>📦 Kapasitas:</strong> 10,000 kg</p>
                <p><strong>🛣️ Terhubung ke:</strong></p>
                <ul style={{ margin: '5px 0', paddingLeft: '20px' }}>
                  <li>📍 Bogor (C25) - 60 km</li>
                  <li>📍 Tangerang (C26) - 55 km</li>
                  <li>📍 Jakarta (C27) - 17 km</li>
                  <li>📍 Bekasi (C28) - 10 km</li>
                </ul>
                <p><strong>🚚 Kendaraan Aktif:</strong> 4 unit</p>
                <p><strong>📊 Total Jarak:</strong> 142 km</p>
              </div>
            </Popup>
          </Marker>
          
          {/* Backup Depot Circle Marker */}
          <CircleMarker
            center={depotCoordinates}
            radius={15}
            fillColor="#dc3545"
            color="#dc3545"
            weight={3}
            opacity={1}
            fillOpacity={0.8}
          >
            <Popup>
              <div className="depot-popup">
                <h4>🏢 PT. Sanghiang Perkasa (Backup)</h4>
                <p><strong>📍 Lokasi:</strong> Pulogadung, Jakarta Timur</p>
                <p><strong>🏭 Alamat:</strong> Kw. Industri Pulogadung, Jl. Pulo Lentut No.10, RW.3, Rw. Terate, Kec. Cakung, Kota Jakarta Timur</p>
                <p><strong>📦 Kapasitas:</strong> 10,000 kg</p>
                <p><strong>🛣️ Terhubung ke:</strong></p>
                <ul style={{ margin: '5px 0', paddingLeft: '20px' }}>
                  <li>📍 Bogor (C25) - 60 km</li>
                  <li>📍 Tangerang (C26) - 55 km</li>
                  <li>📍 Jakarta (C27) - 17 km</li>
                  <li>📍 Bekasi (C28) - 10 km</li>
                </ul>
                <p><strong>🚚 Kendaraan Aktif:</strong> 4 unit</p>
                <p><strong>📊 Total Jarak:</strong> 142 km</p>
              </div>
            </Popup>
          </CircleMarker>

          {renderRouteMarkers()}
          {renderRoutePolylines()}
          {renderVehicleMarkers()}
          {renderTrafficMarkers()}
          {renderWeatherMarkers()}

          {/* Legend */}
          <div className="map-legend">
            <div className="legend-title">Keterangan</div>
            <div className="legend-item">
              <div className="legend-icon depot-icon">🏢</div>
              <span>Depot</span>
            </div>
            <div className="legend-item">
              <div className="legend-icon route-icon">📍</div>
              <span>Destinasi</span>
            </div>
            <div className="legend-item">
              <div className="legend-icon vehicle-icon">🚚</div>
              <span>Kendaraan</span>
            </div>
            <div className="legend-item">
              <div className="legend-icon traffic-icon">🚦</div>
              <span>Traffic</span>
            </div>
            <div className="legend-item">
              <div className="legend-icon weather-icon">🌤️</div>
              <span>Cuaca</span>
            </div>
            <div style={{ marginTop: '10px', fontSize: '12px' }}>
              <div style={{ display: 'flex', alignItems: 'center', margin: '3px 0', fontSize: '10px' }}>
                <span style={{ marginRight: '8px', fontSize: '14px', color: '#28a745' }}>🟢</span>
                <span>Lancar</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', margin: '3px 0', fontSize: '10px' }}>
                <span style={{ marginRight: '8px', fontSize: '14px', color: '#ffc107' }}>🟡</span>
                <span>Sedang</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', margin: '3px 0', fontSize: '10px' }}>
                <span style={{ marginRight: '8px', fontSize: '14px', color: '#dc3545' }}>🔴</span>
                <span>Macet</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', margin: '3px 0', fontSize: '10px' }}>
                <span style={{ marginRight: '8px', fontSize: '14px', color: '#6c757d' }}>☀️</span>
                <span>Cerah</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', margin: '3px 0', fontSize: '10px' }}>
                <span style={{ marginRight: '8px', fontSize: '14px', color: '#6c757d' }}>☁️</span>
                <span>Berawan</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', margin: '3px 0', fontSize: '10px' }}>
                <span style={{ marginRight: '8px', fontSize: '14px', color: '#007bff' }}>🌧️</span>
                <span>Hujan</span>
              </div>
            </div>
          </div>
        </MapContainer>
      </div>

      {/* Control Buttons */}
      <div style={{
        position: 'absolute',
        bottom: '20px',
        left: '50%',
        transform: 'translateX(-50%)',
        display: 'flex',
        gap: '10px',
        zIndex: 1000
      }}>
        <button 
          className="detail-button"
          onClick={() => setPanelOpen(true)}
          style={{
            background: '#6c757d',
            color: 'white',
            border: 'none',
            padding: '10px 20px',
            borderRadius: '5px',
            cursor: 'pointer'
          }}
        >
          📋 Detail Rute
        </button>
      </div>

      {/* Detail Panel */}
      <div className={`detail-panel ${panelOpen ? 'open' : ''}`}>
        <div className="panel-header">
          <h2 className="panel-title">Detail Rute</h2>
          <button className="close-button" onClick={() => setPanelOpen(false)}>×</button>
        </div>
        <div className="panel-content">
          {selectedRoute ? (
            <div className="route-detail">
              <h3>{selectedRoute.destination}</h3>
              <div className="detail-grid">
                <div className="detail-item">
                  <span className="detail-label">Jarak:</span>
                  <span className="detail-value">{selectedRoute.distance_km} km</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">ETA:</span>
                  <span className="detail-value">{formatETA(selectedRoute.estimated_arrival || selectedRoute.eta)}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Kendaraan:</span>
                  <span className="detail-value">{selectedRoute.vehicle_type}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Kapasitas:</span>
                  <span className="detail-value">{selectedRoute.capacity_kg} kg</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Utilisasi:</span>
                  <span className="detail-value">{selectedRoute.utilization_percent || selectedRoute.utilization}%</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Traffic:</span>
                  <span className="detail-value">{selectedRoute.traffic_level}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Cuaca:</span>
                  <span className="detail-value">{selectedRoute.weather?.description || 'Tidak tersedia'}</span>
                </div>
              </div>
              
              {selectedRoute.road_segments && (
                <div>
                  <h4>Jalan yang dilewati:</h4>
                  {selectedRoute.road_segments.map((segment, index) => (
                    <div key={index} className="road-segment">
                      <strong>{segment.road_name}</strong> ({segment.length_km || segment.length} km)
                      <br /><small>Traffic: {segment.traffic_level}</small>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ) : (
            <p>Pilih rute untuk melihat detail</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default PTSanghiangDashboard; 