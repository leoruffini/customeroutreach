from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import DirectoryReadTool, FileReadTool, SerperDevTool
from customeroutreach.tools.sentimentanalysis import SentimentAnalysisTool

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

# Tools setup
directory_read_tool = DirectoryReadTool(directory='./instructions')
file_read_tool = FileReadTool()
search_tool = SerperDevTool()
sentiment_analysis_tool = SentimentAnalysisTool()

@CrewBase
class CustomerOutreach():
	"""Customeroutreach crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	#Agents
	@agent
	def sales_rep_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['sales_rep_agent'],
			allow_delegation=False,
			verbose=True
		)

	@agent
	def lead_sales_rep_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['lead_sales_rep_agent'],
			allow_delegation=False,
			verbose=True
		)
	
	@agent
	def outreach_quality_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['outreach_quality_agent'],
			allow_delegation=True,
			verbose=True
		)

	#Tasks
	@task
	def lead_profiling_task(self) -> Task:
		return Task(
			config=self.tasks_config['lead_profiling_task'],
			agent=self.sales_rep_agent(),
			tools=[directory_read_tool, file_read_tool, search_tool]
		)

	@task
	def personalized_outreach_task(self) -> Task:
		return Task(
			config=self.tasks_config['personalized_outreach_task'],
			agent=self.lead_sales_rep_agent(),
			tools=[sentiment_analysis_tool, search_tool],
			#output_file='emails.md'
		)

	@task
	def outreach_quality_task(self) -> Task:
		return Task(
			config=self.tasks_config['outreach_quality_task'],
			agent=self.outreach_quality_agent(),
			tools=[sentiment_analysis_tool, search_tool],
			#output_file='qa_report.md'
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

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential, #process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
			verbose=True, 
		)