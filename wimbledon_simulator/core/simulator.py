import os
import json
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
import yaml
from dotenv import load_dotenv

from wimbledon_simulator.agents.player_agent import PlayerAgent
from wimbledon_simulator.core.match_engine import MatchEngine
from wimbledon_simulator.core.bracket_manager import BracketManager
from wimbledon_simulator.ui.cli import CLIDisplay

class WimbledonSimulator:
    def __init__(self, config_path: str = "config.yaml"):
        # Load configuration
        load_dotenv(".env.local")
        # If config_path is the default, resolve it relative to this file's parent directory
        if config_path == "config.yaml":
            config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Initialize components
        self.players = self._load_players()
        self.match_engine = MatchEngine()
        self.bracket_manager = BracketManager(self.players)
        self.cli = CLIDisplay()
        
    def _load_players(self) -> List[PlayerAgent]:
        """Load players from CSV and create PlayerAgent instances."""
        df = pd.read_csv(self.config['simulation']['players_csv'])
        return [PlayerAgent(**row) for _, row in df.iterrows()]
    
    def run_tournament(self, live_display: bool = True) -> Dict[str, Any]:
        """Run the full tournament simulation."""
        results = []
        
        while not self.bracket_manager.is_finished():
            if live_display:
                self.cli.display_bracket(self.bracket_manager)
            
            round_results = self.bracket_manager.run_current_round()
            results.extend(round_results)
            
            if live_display:
                self.cli.display_round_results(round_results)
        
        champion = self.bracket_manager.get_champion()
        
        # Print all results at the end
        print("\nFull Tournament Results:")
        for r in results:
            print(f"Round: {r['round']}, {r['player1'].name} vs {r['player2'].name}, Winner: {r['winner'].name}, Score: {r['score']}")
        
        return {
            'champion': champion.name,
            'results': results
        }
    
    def _save_results(self, results: List[Dict[str, Any]]):
        """Save tournament results to JSON and CSV."""
        pass  # No longer needed

def main():
    simulator = WimbledonSimulator()
    results = simulator.run_tournament()
    print(f"\nTournament Champion: {results['champion']}")

if __name__ == "__main__":
    main() 