from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import DirectoryReadTool, FileReadTool, SerperDevTool
from customeroutreach.tools.sentimentanalysis import SentimentAnalysisTool
import logging
import os
import time
from rich.console import Console
from rich.panel import Panel
from datetime import datetime

# Configure logging for better visibility
logging.basicConfig(
	level=logging.INFO,
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	handlers=[
		logging.FileHandler("crew_execution.log"),
		logging.StreamHandler()
	]
)
logger = logging.getLogger("CustomerOutreach")

# Rich console for prettier output
console = Console()

# Global flag to control educational output
# This will be set from the demo.py file
show_educational_output = False

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

# Tools setup
directory_read_tool = DirectoryReadTool(directory='./instructions')
file_read_tool = FileReadTool()
search_tool = SerperDevTool()
sentiment_analysis_tool = SentimentAnalysisTool()

# Callback functions to track agent activity
def on_agent_start(agent, task):
	"""Callback when an agent starts working on a task"""
	console.print(Panel(
		f"[bold green]STARTING NEW AGENT:[/bold green] {agent.name}\n\n"
		f"[yellow]Task:[/yellow] {task.description[:100]}...\n"
		f"[dim]This agent will use its specialized knowledge and tools to complete this task.[/dim]", 
		border_style="green", 
		title=f"🤖 Agent: {agent.name}"
	))
	logger.info(f"Agent {agent.name} started working on task: {task.description[:100]}...")

def on_agent_end(agent, task, output):
	"""Callback when an agent finishes a task"""
	console.print(Panel(
		f"[bold blue]AGENT COMPLETED TASK:[/bold blue] {agent.name}\n\n"
		f"[yellow]Task completed:[/yellow] {task.description[:100]}...\n\n"
		f"[dim]The output from this task will be used by the next agent in the workflow.[/dim]",
		border_style="blue",
		title=f"✅ Task Complete"
	))
	logger.info(f"Agent {agent.name} completed task: {task.description[:100]}")

def on_chain_start(agent, task):
	"""Callback when an agent's chain (reasoning process) starts"""
	if not show_educational_output:
		console.print(f"[dim]Agent {agent.name} is thinking about how to approach the task...[/dim]")
	logger.info(f"Agent {agent.name} chain started for task: {task.description[:100]}")

def on_tool_use(agent, tool_input, tool_name, task):
	"""Callback when an agent uses a tool"""
	# Only display tool usage if educational mode is NOT enabled
	if not show_educational_output:
		if "SerperDev" in tool_name:
			# For search, show a brief message of what's being searched
			query = str(tool_input)[:50] + "..." if len(str(tool_input)) > 50 else str(tool_input)
			console.print(f"[magenta]🔍 {agent.name} is searching for information: \"{query}\"[/magenta]")
		elif "Sentiment" in tool_name:
			# For sentiment analysis, show a brief note
			console.print(f"[magenta]📊 {agent.name} is analyzing sentiment[/magenta]")
		else:
			# For other tools, just show a simple usage notification
			console.print(f"[magenta]🛠️ {agent.name} is using {tool_name}[/magenta]")
	
	logger.info(f"Agent {agent.name} using tool {tool_name} with input: {tool_input}")

def on_tool_output(agent, tool_output, tool_name, task):
	"""Callback when a tool returns output to the agent"""
	# Only display tool output if educational mode is NOT enabled
	if not show_educational_output:
		formatted_output = format_tool_output(tool_name, tool_output)
		
		# Only show detailed output for certain tools in a panel
		if "SerperDev" in tool_name:
			console.print(Panel(
				formatted_output,
				title=f"[bold]Search Results Summary[/bold]",
				border_style="blue",
				width=100
			))
		elif "Sentiment" in tool_name:
			console.print(Panel(
				formatted_output,
				title=f"[bold]Sentiment Analysis[/bold]",
				border_style="green",
				width=80
			))
		else:
			# For other tools, just show a simple notification
			console.print(f"[dim]Tool {tool_name} provided data to {agent.name}[/dim]")
	
	logger.info(f"Tool {tool_name} returned output to {agent.name}")

def on_subtask_creation(agent, subtask, parent_task):
	"""Callback when a subtask is created"""
	console.print(Panel(
		f"[bold yellow]NEW SUBTASK CREATED:[/bold yellow]\n\n"
		f"[cyan]Parent task:[/cyan] {parent_task.description[:50]}...\n"
		f"[cyan]Subtask:[/cyan] {subtask.description[:50]}...\n"
		f"[cyan]Assigned to:[/cyan] {subtask.agent.name}\n\n"
		f"[dim]This demonstrates task decomposition in multi-agent systems.[/dim]",
		border_style="yellow",
		title="🔄 Task Delegation"
	))
	logger.info(f"Subtask created: {subtask.description[:100]} for parent task: {parent_task.description[:100]}")

def on_delegation(delegator, task, delegatee, reason=None):
	"""Callback when an agent delegates a task to another agent"""
	console.print(Panel(
		f"[bold yellow]TASK DELEGATION:[/bold yellow]\n\n"
		f"[cyan]From:[/cyan] {delegator.name}\n"
		f"[cyan]To:[/cyan] {delegatee.name}\n"
		f"[cyan]Task:[/cyan] {task.description[:100]}...\n"
		f"[cyan]Reason:[/cyan] {reason or 'Specialized expertise required'}\n\n"
		f"[dim]Agents delegate tasks to others with more appropriate expertise.[/dim]",
		border_style="yellow",
		title="⤴️ Agent Delegation"
	))
	logger.info(f"Agent {delegator.name} delegated task to {delegatee.name}: {task.description[:100]}")

def format_tool_output(tool_name, output):
	"""Format tool output for better readability"""
	if not output:
		return "[dim]No output[/dim]"
	
	# Convert to string if it's not already
	output_str = str(output)
	
	# For search results, make it more readable
	if "SerperDev" in tool_name:
		try:
			# Hide the raw search results and just show a clean summary
			if isinstance(output, dict) and "organic" in output:
				results = output.get("organic", [])
				
				# Create a clean, formatted panel for search results
				formatted = [f"[bold yellow]Found {len(results)} results for search query:[/bold yellow]"]
				
				# Extract search query if available
				if "searchParameters" in output and "q" in output["searchParameters"]:
					query = output["searchParameters"]["q"]
					formatted.append(f"[cyan]\"{query}\"[/cyan]\n")
				
				formatted.append("[bold green]Top Results:[/bold green]")
				
				# Only show top 3 results with cleaner formatting
				for i, result in enumerate(results[:3]):
					title = result.get("title", "No title")
					link = result.get("link", "No link")
					snippet = result.get("snippet", "No snippet")
					
					formatted.append(f"[bold cyan]{i+1}. {title}[/bold cyan]")
					formatted.append(f"[blue]{link}[/blue]")
					formatted.append(f"{snippet}")
					formatted.append("") # Add blank line between results
				
				if len(results) > 3:
					formatted.append(f"[dim]...and {len(results)-3} more results (not shown for clarity)[/dim]")
					
				return "\n".join(formatted)
			
			# Fallback to a generic message for search results
			return "[dim]Search complete - results processed by agent[/dim]"
		except:
			# Hide any errors in processing and show a clean message
			return "[dim]Search complete - results processed by agent[/dim]"
	
	# For sentiment analysis, highlight the sentiment
	if "Sentiment" in tool_name:
		if "positive" in output_str.lower():
			return f"[green]POSITIVE[/green]: {output_str}"
		elif "negative" in output_str.lower():
			return f"[red]NEGATIVE[/red]: {output_str}"
		elif "neutral" in output_str.lower():
			return f"[yellow]NEUTRAL[/yellow]: {output_str}"
	
	# For longer outputs, just show a summary instead of the raw text
	if len(output_str) > 300:
		return f"[dim]Tool returned data ({len(output_str)} characters) - processed by agent[/dim]"
	
	return output_str

# Function to set the educational output flag
def set_educational_mode(enabled):
	"""Set the global flag for showing educational output"""
	global show_educational_output
	show_educational_output = enabled

@CrewBase
class CustomerOutreach():
	"""Customeroutreach crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	#Agents
	@agent
	def intelligence_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['intelligence_analyst'],
			allow_delegation=False,
			verbose=not show_educational_output,
			callbacks={
				"on_start": on_agent_start,
				"on_end": on_agent_end,
				"on_chain_start": on_chain_start,
				"on_tool_use": on_tool_use,
				"on_tool_output": on_tool_output
			}
		)

	@agent
	def lead_sales_rep_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['lead_sales_rep_agent'],
			allow_delegation=False,
			verbose=not show_educational_output,
			callbacks={
				"on_start": on_agent_start,
				"on_end": on_agent_end,
				"on_chain_start": on_chain_start,
				"on_tool_use": on_tool_use,
				"on_tool_output": on_tool_output
			}
		)
	
	@agent
	def outreach_quality_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['outreach_quality_agent'],
			allow_delegation=True,
			verbose=not show_educational_output,
			callbacks={
				"on_start": on_agent_start,
				"on_end": on_agent_end,
				"on_delegation": on_delegation,
				"on_chain_start": on_chain_start,
				"on_tool_use": on_tool_use,
				"on_tool_output": on_tool_output
			}
		)

	#Tasks
	@task
	def lead_profiling_task(self) -> Task:
		return Task(
			config=self.tasks_config['lead_profiling_task'],
			agent=self.intelligence_analyst(),
			tools=[directory_read_tool, file_read_tool, search_tool],
			output_file='lead_profile.md'
		)

	@task
	def personalized_outreach_task(self) -> Task:
		return Task(
			config=self.tasks_config['personalized_outreach_task'],
			agent=self.lead_sales_rep_agent(),
			tools=[sentiment_analysis_tool, search_tool],
			output_file='initial_outreach.md'
		)

	@task
	def outreach_quality_task(self) -> Task:
		return Task(
			config=self.tasks_config['outreach_quality_task'],
			agent=self.outreach_quality_agent(),
			tools=[sentiment_analysis_tool, search_tool],
			output_file='qa_report.md'
		)

	@task
	def finalize_outreach_task(self) -> Task:
		return Task(
			config=self.tasks_config['finalize_outreach_task'],
			agent=self.lead_sales_rep_agent(),
			tools=[sentiment_analysis_tool, search_tool],
			output_file='final_outreach.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Customeroutreach crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		console.print(Panel(f"[bold]Customer Outreach Crew Initialization[/bold]\nSequential Process\nAgents: Intelligence Analyst, Lead Sales Rep, Outreach Quality Agent", 
					 border_style="green"))
		
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential, #process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
			verbose=not show_educational_output,
			callbacks={
				"on_subtask_creation": on_subtask_creation,
			}
		)
	
	def run(self, inputs):
		"""Run the crew and return results with enhanced output"""
		console.print(Panel.fit("[bold cyan]INITIALIZING MULTI-AGENT SYSTEM[/bold cyan]", border_style="cyan"))
		
		# Display input parameters
		console.print(Panel.fit(
			"\n".join([f"[bold]{k}:[/bold] {v}" for k, v in inputs.items()]), 
			title="[bold]Input Parameters[/bold]", 
			border_style="blue"
		))
		
		# Create output directory for all files
		timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
		output_dir = f"outputs_{timestamp}"
		os.makedirs(output_dir, exist_ok=True)
		
		# Record start time
		start_time = time.time()
		
		# Initialize the crew object first (this will print the initialization message)
		crew_instance = self.crew()
		
		# Educational descriptions for each phase - only show AFTER crew initialization
		if show_educational_output:
			educational_panels = [
				Panel.fit(
					"[bold green]Intelligence Analyst Agent[/bold green] is researching the target company.\n\n"
					"[dim]This agent uses internet search tools and knowledge bases to gather detailed information about "
					"the company, its challenges, recent news, and potential needs that our solution could address.[/dim]",
					title="🔍 Research Phase", 
					border_style="green"
				),
				Panel.fit(
					"[bold blue]Lead Sales Rep Agent[/bold blue] is creating a personalized outreach message.\n\n"
					"[dim]This agent uses the research from the Intelligence Analyst to craft a compelling, personalized message "
					"tailored to the decision maker's position and company needs.[/dim]",
					title="✍️ Content Creation Phase", 
					border_style="blue"
				),
				Panel.fit(
					"[bold magenta]Quality Control Agent[/bold magenta] is evaluating the outreach message.\n\n"
					"[dim]This agent reviews the message for effectiveness, persuasiveness, tone, and alignment with "
					"business objectives. It provides feedback for improvement.[/dim]",
					title="🔍 Quality Assessment Phase", 
					border_style="magenta"
				),
				Panel.fit(
					"[bold cyan]Lead Sales Rep Agent[/bold cyan] is refining the final message.\n\n"
					"[dim]This agent incorporates the feedback from the Quality Control Agent to produce a highly "
					"effective final outreach message ready for sending.[/dim]",
					title="✨ Final Refinement Phase", 
					border_style="cyan"
				)
			]
			
			# Display the first educational panel
			console.print(educational_panels[0])
		
		# Now kick off the crew with the inputs
		result = crew_instance.kickoff(inputs=inputs)
		
		# Calculate duration
		duration = time.time() - start_time
		
		# Display output files if in educational mode
		if show_educational_output:
			output_files = [
				'lead_profile.md',
				'initial_outreach.md', 
				'qa_report.md',
				'final_outreach.md'
			]
			
			for i, file_name in enumerate(output_files):
				if os.path.exists(file_name):
					with open(file_name, 'r') as f:
						content = f.read()
						# Format the content for display
						preview = content[:500] + ("..." if len(content) > 500 else "")
						
						# Get agent name from the task config
						agent_names = {
							0: "Intelligence Analyst",
							1: "Lead Sales Rep",
							2: "Quality Control Agent",
							3: "Lead Sales Rep"
						}
						agent_name = agent_names.get(i, "Agent")
						
						console.print(Panel(
							f"[bold cyan]Task Completed:[/bold cyan] {agent_name}\n\n"
							f"[yellow]Output Summary:[/yellow]\n{preview}",
							title=f"[bold]Phase {i+1} Output[/bold]",
							border_style="cyan",
							width=100
						))
		
		# Copy output files to timestamped directory
		import glob
		import shutil
		
		for file in glob.glob("*.md"):
			shutil.copy(file, f"{output_dir}/{file}")
		
		# Return information about the run
		return {
			"result": result,
			"output_directory": output_dir,
			"execution_time": duration
		}