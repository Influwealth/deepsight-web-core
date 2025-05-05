from crewai import Agent, Task, Crew
from crewai.tools import BaseTool

# Define the custom tool for human confirmation
class ConfirmByHumanTool(BaseTool):
    name: str = "confirm_by_human"  # Add type annotation
    description: str = "Waits for human confirmation before launching the miner."  # Add type annotation

    def _run(self, *args, **kwargs):
        print(">>> Awaiting human confirmation to begin mining...")
        input("Press [ENTER] to proceed with launching BzMiner...")

        import subprocess
        try:
            subprocess.Popen([
                "cmd.exe", "/c",
                "C:\\Users\\VICTOR MORALES\\Downloads\\bzminer_v23.0.2_windows\\start_kaspa.bat"
            ])
            return "✅ Mining started!"
        except Exception as e:
            return f"❌ Error launching miner: {e}"

    def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async execution is not supported for this tool.")

# Define agent
miner = Agent(
    role='Quantum Mining Ops Analyst',
    goal='Launch mining only with human clearance and report success/failure.',
    backstory='Optimizes and monitors mining operations with user in the loop.',
    verbose=True
)

# Create an instance of the custom tool
confirm_tool = ConfirmByHumanTool()

# Define task
mining_task = Task(
    description='Wait for human approval, then launch BzMiner for Kaspa mining.',
    expected_output='Mining process initiated with human clearance.',
    agent=miner,
    tools=[confirm_tool]
)

# Assemble and run
crew = Crew(agents=[miner], tasks=[mining_task], verbose=True)

if __name__ == "__main__":
    print(">>> Initializing supervised mining agent crew...")
    result = crew.kickoff()
    print(result)