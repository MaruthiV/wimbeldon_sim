from typing import Dict, Any, Optional
import numpy as np
from wimbledon_simulator.memory.vector_store import VectorStore

class PlayerAgent:
    def __init__(self, name: str, seed: int, style: str, 
                 serve_pct: float, return_pct: float):
        # Static attributes
        self.name = name
        self.seed = seed
        self.style = style
        self.baseline_stats = {
            'serve_pct': serve_pct,
            'return_pct': return_pct
        }
        
        # Dynamic attributes
        self.fitness_level = 1.0  # 1.0 = 100% fit
        self.mental_toughness = 0.7  # Base mental toughness
        self.rivalries: Dict[str, float] = {}  # Head-to-head records
        self.memory_store = VectorStore()
        
    def decide_strategy(self, opponent: 'PlayerAgent') -> str:
        """Decide match strategy based on opponent and current state."""
        # Get relevant memories
        memories = self.memory_store.query(self.name, k=3)
        
        # Create strategy prompt
        prompt = f"""
        Player: {self.name}
        Style: {self.style}
        Current Fitness: {self.fitness_level:.2f}
        Mental Toughness: {self.mental_toughness:.2f}
        
        Opponent: {opponent.name}
        Opponent Style: {opponent.style}
        
        Recent Memories:
        {chr(10).join(memories)}
        
        Based on this information, what strategy should {self.name} employ?
        Consider:
        1. Playing style matchups
        2. Current physical condition
        3. Mental state
        4. Historical performance
        """
        
        # TODO: Call LLM with prompt
        # For now, return a simple strategy
        return f"Play to {self.style} strengths while adapting to {opponent.style}"
    
    def update_memory(self, event: str):
        """Add a new memory to the vector store."""
        self.memory_store.add_memory(self.name, event)
    
    def apply_fatigue(self, match_length: int):
        """Update fitness level based on match length."""
        # More fatigue for longer matches
        fatigue_factor = 0.1 * (match_length / 3)  # Normalize to 3 sets
        self.fitness_level = max(0.5, self.fitness_level - fatigue_factor)
    
    def update_rivalry(self, opponent: 'PlayerAgent', won: bool):
        """Update head-to-head record with opponent."""
        if opponent.name not in self.rivalries:
            self.rivalries[opponent.name] = 0.5  # Neutral starting point
        
        # Update rivalry score (0-1 scale)
        adjustment = 0.1 if won else -0.1
        self.rivalries[opponent.name] = max(0, min(1, 
            self.rivalries[opponent.name] + adjustment))
    
    def get_features(self) -> Dict[str, float]:
        """Get current feature vector for ML model."""
        return {
            'serve_pct': self.baseline_stats['serve_pct'] * self.fitness_level,
            'return_pct': self.baseline_stats['return_pct'] * self.fitness_level,
            'fitness_level': self.fitness_level,
            'mental_toughness': self.mental_toughness
        } 