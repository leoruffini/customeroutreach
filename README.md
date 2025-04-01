# Customer Outreach Multi-Agent System

A demonstration of a multi-agent system for creating personalized customer outreach messages. The system uses a crew of specialized AI agents that work together to research companies, create personalized messaging, and optimize outreach quality.

## Overview

This project showcases the power of multi-agent systems in handling complex business tasks through task decomposition and specialization. The agents in this system include:

1. **Intelligence Analyst** - Researches and profiles potential customers
2. **Lead Sales Representative** - Creates personalized outreach messages
3. **Quality Control Specialist** - Evaluates and provides feedback on outreach quality

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/customeroutreach.git
cd customeroutreach

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

The demo can be run with various options to customize the experience:

```bash
# Run the basic demo
python -m src.customeroutreach.demo

# Run with custom parameters
python -m src.customeroutreach.demo --company "Acme Inc" --industry "Technology" --decision-maker "John Smith" --position "CTO"

# Run with educational mode (recommended for learning)
python -m src.customeroutreach.demo --educational

# Run with verbose output
python -m src.customeroutreach.demo --verbose
```

### Available Options

- `--company`: Target company name
- `--industry`: Company industry
- `--decision-maker`: Key decision maker's name
- `--position`: Decision maker's position
- `--educational`: Enable educational mode with detailed explanations
- `--verbose`: Show more detailed agent outputs

## Educational Mode

The `--educational` flag enables a special mode designed for learning about multi-agent systems. When enabled, you'll see:

- Visual representation of the agent architecture
- Detailed explanations of each agent's role and expertise
- Information about how agents communicate and coordinate
- Key learning points about multi-agent system design
- Explanations of each phase in the workflow

This mode is ideal for:
- Students learning about AI agent systems
- Developers wanting to understand multi-agent architectures
- Workshops and demonstrations

## Output Files

After running the demo, you'll find the following output files in a timestamped directory:

- `lead_profile.md`: Detailed research about the target company
- `initial_outreach.md`: First draft of the outreach message
- `qa_report.md`: Quality assessment and improvement suggestions
- `final_outreach.md`: The refined, final outreach message

## Project Structure

```
customeroutreach/
├── src/
│   └── customeroutreach/
│       ├── crew.py           # Main agent crew implementation
│       ├── demo.py           # Demo script with educational features
│       ├── main.py           # CLI entry point
│       └── tools/            # Specialized tools for agents
├── config/
│   ├── agents.yaml           # Agent configurations
│   └── tasks.yaml            # Task definitions
└── README.md                 # This file
```

## Extensions and Customization

You can extend this system by:

1. Adding more specialized agents
2. Creating new tools for agents to use
3. Modifying the task workflows
4. Changing the agent architectures

## License

[MIT License](LICENSE)
