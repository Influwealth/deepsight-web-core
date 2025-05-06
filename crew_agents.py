import os
from crewai import Agent, Task, Crew
from litellm import completion

# Load environment variables
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
if not HUGGINGFACE_API_KEY:
    raise ValueError("Hugging Face API key not found. Set it in your .env file or environment variables.")

# Query Model Function
def query_model(prompt):
    try:
        # Specify the provider and model explicitly
        response = completion(
            model="huggingface/mistralai/Mixtral-8x7B-Instruct-v0.1",  # Correctly specify the provider and model
            messages=[{"role": "user", "content": prompt}],
            api_key=HUGGINGFACE_API_KEY  # Use your Hugging Face API key
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error querying model: {str(e)}")

# Define Agents
nova = Agent(
    role="Risk Analyst",
    goal="Review risks and ensure compliance",
    backstory="An expert in identifying potential risks in operations.",
    verbose=True,
    llm=lambda prompt: query_model(prompt)  # Use the corrected query_model function
)

mindmax = Agent(
    role="Autonomous Decision-Maker",
    goal="Make decisions without human intervention",
    backstory="A fully autonomous agent capable of executing tasks independently.",
    verbose=True,
    llm=lambda prompt: query_model(prompt)
)

# Define Tasks
risk_analysis_task = Task(
    description="Evaluate operational risks associated with Kaspa mining operations.",
    agent=nova
)

decision_task = Task(
    description="Decide whether to proceed with mining based on risk analysis.",
    agent=mindmax
)

# Create Crew
crew = Crew(
    agents=[nova, mindmax],
    tasks=[risk_analysis_task, decision_task],
    verbose=True
)

# Run the Crew
if __name__ == "__main__":
    print("ðŸš€ Initializing DeepSight Core AI Mining Team...")
    result = crew.kickoff()
    print("Final Output:")
    print(result)
