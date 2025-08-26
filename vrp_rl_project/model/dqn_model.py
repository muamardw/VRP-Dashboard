import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from collections import deque
import random
from typing import List, Tuple, Dict

class DQNAgent:
    def __init__(self, state_size: int, action_size: int, config: Dict):
        """
        Initialize DQN Agent.
        
        Args:
            state_size: Size of state space
            action_size: Size of action space
            config: Configuration dictionary
        """
        self.state_size = state_size
        self.action_size = action_size
        self.config = config
        
        # Hyperparameters
        self.learning_rate = config['model']['learning_rate']
        self.gamma = config['model']['gamma']
        self.epsilon = config['model']['epsilon_start']
        self.epsilon_min = config['model']['epsilon_end']
        self.epsilon_decay = config['model']['epsilon_decay']
        self.memory_size = config['model']['memory_size']
        self.batch_size = config['model']['batch_size']
        self.target_update = config['model']['target_update']
        
        # Initialize memory
        self.memory = deque(maxlen=self.memory_size)
        
        # Create main and target networks
        self.model = self._build_model()
        self.target_model = self._build_model()
        self.update_target_model()

    def _build_model(self) -> models.Model:
        """
        Build neural network model.
        
        Returns:
            Compiled Keras model
        """
        model = models.Sequential()
        
        # Input layer
        model.add(layers.Dense(self.config['model']['hidden_layers'][0], 
                             input_dim=self.state_size, 
                             activation='relu'))
        
        # Hidden layers
        for units in self.config['model']['hidden_layers'][1:]:
            model.add(layers.Dense(units, activation='relu'))
        
        # Output layer
        model.add(layers.Dense(self.action_size, activation='linear'))
        
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate),
                     loss='mse')
        
        return model

    def update_target_model(self):
        """Update target network weights with main network weights."""
        self.target_model.set_weights(self.model.get_weights())

    def remember(self, state: np.ndarray, action: int, reward: float, 
                next_state: np.ndarray, done: bool):
        """
        Store experience in memory.
        
        Args:
            state: Current state
            action: Action taken
            reward: Reward received
            next_state: Next state
            done: Whether episode is done
        """
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state: np.ndarray, valid_actions: List[int] = None) -> int:
        """
        Choose action using epsilon-greedy policy.
        
        Args:
            state: Current state
            valid_actions: List of valid actions (optional)
            
        Returns:
            Selected action
        """
        if np.random.rand() <= self.epsilon:
            if valid_actions:
                return random.choice(valid_actions)
            return random.randrange(self.action_size)
        
        act_values = self.model.predict(state.reshape(1, -1), verbose=0)
        
        if valid_actions:
            # Mask invalid actions with large negative values
            mask = np.ones(self.action_size) * -np.inf
            mask[valid_actions] = 0
            act_values = act_values + mask
            
        return np.argmax(act_values[0])

    def replay(self) -> float:
        """
        Train on batch of experiences from memory.
        
        Returns:
            Loss value
        """
        if len(self.memory) < self.batch_size:
            return 0.0
            
        minibatch = random.sample(self.memory, self.batch_size)
        
        states = np.array([i[0] for i in minibatch])
        actions = np.array([i[1] for i in minibatch])
        rewards = np.array([i[2] for i in minibatch])
        next_states = np.array([i[3] for i in minibatch])
        dones = np.array([i[4] for i in minibatch])
        
        # Predict Q-values for current states
        target = self.model.predict(states, verbose=0)
        
        # Predict Q-values for next states using target network
        target_next = self.target_model.predict(next_states, verbose=0)
        
        # Update Q-values for taken actions
        for i in range(self.batch_size):
            if dones[i]:
                target[i][actions[i]] = rewards[i]
            else:
                target[i][actions[i]] = rewards[i] + self.gamma * np.max(target_next[i])
        
        # Train the model
        history = self.model.fit(states, target, epochs=1, verbose=0)
        
        # Decay epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
            
        return history.history['loss'][0]

    def load(self, name: str):
        """Load model weights from file."""
        self.model.load_weights(name)

    def save(self, name: str):
        """Save model weights to file."""
        self.model.save_weights(name) 