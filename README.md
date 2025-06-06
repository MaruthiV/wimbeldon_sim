# AgentSwarm Wimbledon Simulator

A sophisticated tennis tournament simulator that uses multi-agent architecture combined with ML and LLM-driven decision-making to simulate a full Wimbledon tournament.

## Features

- Live CLI bracket display
- ML-powered point prediction
- LLM-driven player strategies
- Dynamic player state and memory
- Detailed match and tournament statistics

## Project Structure

```
wimbledon_simulator/
├── core/               # Core simulation logic
├── agents/            # Player agent implementations
├── memory/            # Vector store and memory management
├── ui/                # CLI interface
├── data/              # Player data and configurations
├── prompts/           # LLM prompt templates
├── requirements.txt   # Project dependencies
└── config.yaml        # Configuration file
```

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env.local` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

Run the simulator:
```bash
python -m core.simulator
```

## Output

The simulator generates:
- Live CLI bracket display
- `results.json`: Detailed match data
- `summary.csv`: Tournament summary

## Development

Run tests:
```bash
pytest
```

## License

MIT License # wimbeldon_sim
