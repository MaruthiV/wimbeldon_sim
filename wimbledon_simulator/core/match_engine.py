import numpy as np
from typing import Tuple, List, Dict, Any
from wimbledon_simulator.agents.player_agent import PlayerAgent

class MatchEngine:
    def __init__(self):
        # TODO: Load trained ML model
        self.model = None
    
    def compute_win_probability(self, p1: PlayerAgent, p2: PlayerAgent) -> float:
        """Compute probability of p1 winning a point against p2."""
        # TODO: Use ML model for prediction
        # For now, use simple heuristic based on serve/return percentages
        p1_features = p1.get_features()
        p2_features = p2.get_features()
        
        # Basic probability calculation
        p1_serve_win = p1_features['serve_pct']
        p2_serve_win = p2_features['serve_pct']
        p1_return_win = 1 - p2_serve_win
        p2_return_win = 1 - p1_serve_win
        
        # Average win probability
        p1_win_prob = (p1_serve_win + p1_return_win) / 2
        p2_win_prob = (p2_serve_win + p2_return_win) / 2
        
        # Normalize to get p1's win probability
        return p1_win_prob / (p1_win_prob + p2_win_prob)
    
    def simulate_point(self, server: PlayerAgent, receiver: PlayerAgent) -> bool:
        """Simulate a single point. Returns True if server wins."""
        win_prob = self.compute_win_probability(server, receiver)
        return np.random.random() < win_prob
    
    def simulate_game(self, server: PlayerAgent, receiver: PlayerAgent) -> bool:
        """Simulate a single game. Returns True if server wins."""
        server_points = 0
        receiver_points = 0
        
        while True:
            if self.simulate_point(server, receiver):
                server_points += 1
            else:
                receiver_points += 1
            
            # Check for game win
            if server_points >= 4 and server_points - receiver_points >= 2:
                return True
            if receiver_points >= 4 and receiver_points - server_points >= 2:
                return False
    
    def simulate_set(self, p1: PlayerAgent, p2: PlayerAgent) -> Tuple[int, int]:
        """Simulate a single set. Returns (games_p1, games_p2)."""
        p1_games = 0
        p2_games = 0
        
        while True:
            # Alternate serves
            if (p1_games + p2_games) % 2 == 0:
                if self.simulate_game(p1, p2):
                    p1_games += 1
                else:
                    p2_games += 1
            else:
                if self.simulate_game(p2, p1):
                    p2_games += 1
                else:
                    p1_games += 1
            
            # Check for set win
            if p1_games >= 6 and p1_games - p2_games >= 2:
                return p1_games, p2_games
            if p2_games >= 6 and p2_games - p1_games >= 2:
                return p1_games, p2_games
    
    def simulate_match(self, p1: PlayerAgent, p2: PlayerAgent, 
                      best_of: int = 5) -> Tuple[PlayerAgent, List[Tuple[int, int]]]:
        """Simulate a full match. Returns (winner, list of set scores)."""
        p1_sets = 0
        p2_sets = 0
        set_scores = []
        
        while True:
            p1_games, p2_games = self.simulate_set(p1, p2)
            set_scores.append((p1_games, p2_games))
            
            if p1_games > p2_games:
                p1_sets += 1
            else:
                p2_sets += 1
            
            # Check for match win
            if p1_sets > best_of // 2:
                return p1, set_scores
            if p2_sets > best_of // 2:
                return p2, set_scores 