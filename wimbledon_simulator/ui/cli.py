from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from typing import List, Dict, Any
from wimbledon_simulator.core.bracket_manager import BracketManager

class CLIDisplay:
    def __init__(self):
        self.console = Console()
    
    def display_bracket(self, bracket_manager: BracketManager):
        """Display current tournament bracket state."""
        state = bracket_manager.get_bracket_state()
        
        # Create bracket table
        table = Table(title=f"Wimbledon Tournament - Round {state['current_round']}")
        table.add_column("Match", style="cyan")
        table.add_column("Player 1", style="green")
        table.add_column("Player 2", style="yellow")
        table.add_column("Status", style="magenta")
        
        # Add matches
        for i, (p1, p2) in enumerate(bracket_manager.get_pairs(), 1):
            status = "Pending"
            if state['results']:
                # Find most recent result for this pair
                for result in reversed(state['results']):
                    if (result['player1'] == p1 and result['player2'] == p2) or \
                       (result['player1'] == p2 and result['player2'] == p1):
                        winner = result['winner']
                        status = f"Winner: {winner.name}"
                        break
            
            table.add_row(
                f"Match {i}",
                f"{p1.name} ({p1.seed})",
                f"{p2.name} ({p2.seed})",
                status
            )
        
        self.console.print(table)
    
    def display_round_results(self, results: List[Dict[str, Any]]):
        """Display results of the current round."""
        if not results:
            return
        
        # Create results table
        table = Table(title=f"Round {results[0]['round']} Results")
        table.add_column("Match", style="cyan")
        table.add_column("Score", style="green")
        table.add_column("Winner", style="yellow")
        table.add_column("Strategy", style="magenta")
        
        for i, result in enumerate(results, 1):
            # Format score
            score_str = " ".join(f"{p1}-{p2}" for p1, p2 in result['score'])
            
            # Format strategy
            strategy = f"{result['winner'].name}: {result[f'strategy_p{1 if result['winner'] == result['player1'] else 2}']}"
            
            table.add_row(
                f"Match {i}",
                score_str,
                result['winner'].name,
                strategy
            )
        
        self.console.print(table)
    
    def display_champion(self, champion: Any):
        """Display tournament champion."""
        if not champion:
            return
        
        text = Text()
        text.append("🏆 Tournament Champion 🏆\n\n", style="bold gold")
        text.append(f"{champion.name}\n", style="bold green")
        text.append(f"Seed: {champion.seed}\n", style="cyan")
        text.append(f"Style: {champion.style}\n", style="yellow")
        
        panel = Panel(text, title="Wimbledon Champion", border_style="green")
        self.console.print(panel) 