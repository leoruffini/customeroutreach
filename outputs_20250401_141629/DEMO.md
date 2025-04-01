# Multi-Agent System Demonstration

This demo showcases a multi-agent system working together on customer outreach tasks, with clear console output showing agent activities, interactions, and outputs.

## Features

- Colorful, visually-distinct console output showing agent activities
- Detailed logging of agent thoughts, tool usage, and delegations
- Visual progress indicators
- Output file organization
- Clear indication of agent collaboration

## Running the Demo

To run the demo:

```bash
python -m src.customeroutreach.demo
```

### Command Line Options

- `--company` - Target company name (default: "Manpower Group Poland")
- `--industry` - Company industry (default: "HR and Recruitment") 
- `--decision-maker` - Key decision maker (default: "Tomasz Walenczak")
- `--position` - Decision maker position (default: "Country Manager")
- `--verbose` - Display more verbose output

Example with custom inputs:

```bash
python -m src.customeroutreach.demo \
  --company "Netflix Poland" \
  --industry "Entertainment" \
  --decision-maker "Susan Smith" \
  --position "Country Director" \
  --verbose
```

## Understanding the Console Output

The demo displays the multi-agent system execution with several types of visual indicators:

1. **Agent Starting**: 🟢 Green panels show when agents start working on tasks
2. **Agent Thinking**: ⚙️ Cyan messages indicate when agents are reasoning
3. **Tool Usage**: 🔧 Magenta messages show when agents use tools
4. **Tool Output**: 🔍 Magenta panels display formatted results from tool usage
5. **Delegation**: 📢 Orange panels appear when tasks are delegated
6. **Task Completion**: ✅ Blue panels indicate when tasks are completed

The demo includes interactive pauses after each agent completes a task, allowing you to examine the output before proceeding to the next step. Simply press Enter to continue.

### Tool Output Formatting

Tool outputs are formatted for better readability:

- **Search Results**: Shows top 5 results with title, link, and snippet
- **Sentiment Analysis**: Color-coded by sentiment (positive, negative, neutral)
- **Long Outputs**: Truncated with indicators to improve readability

## Output Files

The demo generates several types of output files:

1. **Task Outputs**: Stored in the `outputs_TIMESTAMP/` directory
   - `lead_profile.md` - Company research by the Sales Rep
   - `initial_outreach.md` - Initial email draft by Lead Sales Rep
   - `qa_report.md` - Quality assessment by Quality Agent
   - `final_outreach.md` - Final polished email

2. **Agent Outputs**: Detailed agent outputs in `agent_outputs/`
   - Raw output from each agent for each task

## Exploring the Multi-Agent System

To better understand how the agents work together:

1. Watch the console output to see the sequential flow of agents working
2. Notice how information flows from one agent to the next
3. Observe the different tools each agent uses
4. See how the quality agent evaluates and critiques the work
5. Study the final output that integrates all agents' contributions

## Customizing the Demo

You can customize aspects of the demo in the following files:

- `src/customeroutreach/config/agents.yaml`: Agent roles and personalities
- `src/customeroutreach/config/tasks.yaml`: Task definitions and expected outputs
- `src/customeroutreach/crew.py`: Agent and task assignments, process flow

## System Architecture

The demo showcases a multi-agent system with:

- **Agents**: Sales Rep, Lead Sales Rep, Quality Control
- **Tasks**: Lead profiling, outreach creation, quality assessment, finalization
- **Tools**: Directory reading, file reading, search, sentiment analysis
- **Process**: Sequential workflow with possible hierarchical subtask delegation
- **Output**: Rich console output, logging, task outputs

This architecture demonstrates how multiple specialized agents can collaborate to solve complex tasks by passing information and building on each other's work.
