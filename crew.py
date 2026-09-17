from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

load_dotenv()

llm = LLM(model="ollama/llama3.1", base_url="http://localhost:11434")
search_tool = SerperDevTool()

researcher = Agent(
    role="Stock Market Researcher",
    goal="Find recent news, price info, and analyst sentiment for {company}",
    backstory="You are a sharp financial researcher who tracks market news daily.",
    tools=[search_tool],
    llm=llm,
    verbose=True,
)

analyst = Agent(
    role="Investment Analyst",
    goal="Turn research into a clear investment recommendation for {company}",
    backstory="You are a seasoned analyst who writes concise, actionable stock reports.",
    llm=llm,
    verbose=True,
)

research_task = Task(
    description="Search for the latest news, stock price movement, and analyst opinions about {company}. Summarize key findings.",
    expected_output="A bullet-point summary of recent news, price action, and sentiment for {company}.",
    agent=researcher,
)

analysis_task = Task(
    description="Using the research provided, write a short investment recommendation for {company} (buy/hold/sell) with reasoning.",
    expected_output="A short report with a clear recommendation and 3-5 supporting reasons.",
    agent=analyst,
    context=[research_task],
)

crew = Crew(
    agents=[researcher, analyst],
    tasks=[research_task, analysis_task],
    process=Process.sequential,
    verbose=True,
)