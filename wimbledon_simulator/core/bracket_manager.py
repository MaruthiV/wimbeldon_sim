from typing import List, Dict, Any, Tuple, Optional
from wimbledon_simulator.agents.player_agent import PlayerAgent
from wimbledon_simulator.core.match_engine import MatchEngine

class BracketManager:
    def __init__(self, players: List[PlayerAgent]):
        self.players = sorted(players, key=lambda p: p.seed)
        self.match_engine = MatchEngine()
        self.current_round = 1
        self.active_players = self.players.copy()
        self.results = []
    
    def get_pairs(self) -> List[Tuple[PlayerAgent, PlayerAgent]]:
        """Get current round pairings based on seeding."""
        if len(self.active_players) < 2:
            return []
        
        # Sort by seed for proper bracket placement
        sorted_players = sorted(self.active_players, key=lambda p: p.seed)
        pairs = []
        
        # Create pairs based on seeding (1v16, 2v15, etc.)
        for i in range(len(sorted_players) // 2):
            pairs.append((sorted_players[i], sorted_players[-(i+1)]))
        
        return pairs
    
    def run_current_round(self) -> List[Dict[str, Any]]:
        """Run all matches in the current round."""
        if not self.active_players:
            return []
        
        round_results = []
        pairs = self.get_pairs()
        
        for p1, p2 in pairs:
            # Simulate match
            winner, scores = self.match_engine.simulate_match(p1, p2)
            
            # Update player states
            loser = p2 if winner == p1 else p1
            match_length = sum(sum(score) for score in scores)
            
            winner.apply_fatigue(match_length)
            loser.apply_fatigue(match_length)
            
            winner.update_rivalry(loser, True)
            loser.update_rivalry(winner, False)
            
            # Record result
            result = {
                'round': self.current_round,
                'player1': p1,
                'player2': p2,
                'winner': winner,
                'score': scores,
                'strategy_p1': p1.decide_strategy(p2),
                'strategy_p2': p2.decide_strategy(p1)
            }
            round_results.append(result)
            
            # Update memories
            winner.update_memory(
                f"Won against {loser.name} in round {self.current_round} "
                f"with score {scores}"
            )
            loser.update_memory(
                f"Lost to {winner.name} in round {self.current_round} "
                f"with score {scores}"
            )
        
        # Update tournament state
        self.active_players = [r['winner'] for r in round_results]
        self.results.extend(round_results)
        self.current_round += 1
        
        return round_results
    
    def is_finished(self) -> bool:
        """Check if tournament is finished."""
        return len(self.active_players) <= 1
    
    def get_champion(self) -> Optional[PlayerAgent]:
        """Get the tournament champion."""
        return self.active_players[0] if self.active_players else None
    
    def get_bracket_state(self) -> Dict[str, Any]:
        """Get current state of the tournament bracket."""
        return {
            'current_round': self.current_round,
            'active_players': [p.name for p in self.active_players],
            'results': self.results
        } 