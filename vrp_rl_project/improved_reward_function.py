def improved_calculate_reward(self, distance: float, travel_time: float, service_time: float) -> float:
    """
    Improved reward function for DQN VRP.
    
    Args:
        distance: Distance traveled
        travel_time: Time taken to travel
        service_time: Time spent at customer location
        
    Returns:
        Calculated reward
    """
    # Distance penalty (more aggressive)
    distance_penalty = -distance * 0.2  # Increased penalty
    
    # Time efficiency bonus (more emphasis)
    time_efficiency = 2.0 / (travel_time + service_time + 1e-6)  # Added epsilon
    
    # Capacity utilization bonus (more granular)
    utilization_ratio = (self.max_capacity - self.remaining_capacity) / self.max_capacity
    utilization_bonus = utilization_ratio * 10  # Increased bonus
    
    # Completion bonus (larger reward)
    completion_bonus = 200 if len(self.visited_customers) == self.n_customers else 0
    
    # Efficiency bonus (new component)
    efficiency_bonus = 50 if len(self.visited_customers) > 0 and self.total_distance < 200 else 0
    
    # Time window bonus (new component)
    time_window_bonus = 20 if self.current_time <= 24 else -10  # Penalty for overtime
    
    total_reward = (distance_penalty + 
                   time_efficiency + 
                   utilization_bonus + 
                   completion_bonus + 
                   efficiency_bonus + 
                   time_window_bonus)
    
    return total_reward 