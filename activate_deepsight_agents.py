import os
import subprocess
import sys

# === BOOTSTRAP FUNCTION ===
def bootstrap_environment():
    """Set up environment before any imports"""
    # Create requirements.txt if missing
    if not os.path.exists("requirements.txt"):
        print("Creating requirements.txt file...")
        with open("requirements.txt", "w") as f:
            f.write("""crewai>=0.28.0
langchain>=0.0.325
langchain-huggingface>=0.0.2
huggingface-hub>=0.19.4
""")

    # Install dependencies first
    print("📦 Installing dependencies...")
    try:
        subprocess.run("pip install -r requirements.txt", shell=True, check=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Issue with requirements installation: {e}")
        print("Continuing anyway in case they're already installed...")

# Run bootstrap before any other imports
bootstrap_environment()

# Now import dependencies (after they've been installed)
try:
    from crewai import Agent, Task, Crew
    # Try both potential import paths
    try:
        from langchain_huggingface import HuggingFaceEndpoint
    except ImportError:
        print("Trying alternate import path...")
        from langchain.llms import HuggingFaceEndpoint
except ImportError as e:
    print(f"❌ Critical import error: {e}")
    print("Please install the missing package manually with:")
    print(f"pip install {str(e).split()[-1]}")
    sys.exit(1)

# === LOAD API KEY ===
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
if not HUGGINGFACE_API_KEY:
    print("⚠️ Hugging Face API key missing. Please set it with:")
    print("    export HUGGINGFACE_API_KEY=your_key_here  # Linux/Mac")
    print("    set HUGGINGFACE_API_KEY=your_key_here     # Windows")
    sys.exit(1)

# === CONFIGURE LLM PROPERLY ===
print("🔄 Configuring LLM...")
try:
    # Using HuggingFaceEndpoint implementation
    llm = HuggingFaceEndpoint(
        endpoint_url=f"https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1",
        huggingfacehub_api_token=HUGGINGFACE_API_KEY,
        task="text-generation",
        max_length=2048
    )
    print("✅ LLM configured successfully")
except Exception as e:
    print(f"❌ Failed to configure LLM: {e}")
    print("Trying fallback configuration...")
    try:
        from langchain.llms import HuggingFaceHub
        llm = HuggingFaceHub(
            repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
            huggingfacehub_api_token=HUGGINGFACE_API_KEY
        )
        print("✅ LLM configured with fallback method")
    except Exception as e2:
        print(f"❌ All LLM configuration attempts failed: {e2}")
        sys.exit(1)

# === SKIP GIT OPERATIONS FOR NOW ===
print("ℹ️ Skipping Git operations for now")

# === SKIP NETLIFY DEPLOYMENT FOR NOW ===
print("ℹ️ Skipping Netlify deployment for now")

# === DEEPSIGHT CORE AGENTS ===
print("🧠 Creating DeepSight agents...")
try:
    nova = Agent(
        role="Risk & Compliance Analyst",
        goal="Ensure ethical compliance and regulatory adherence",
        backstory="Expert in ESG frameworks with blockchain regulations knowledge",
        verbose=True,
        llm=llm
    )

    mindmax = Agent(
        role="Autonomous Decision-Maker", 
        goal="Make high-level strategy calls",
        backstory="Former hedge fund strategist with expertise in macroeconomics",
        verbose=True, 
        llm=llm
    )

    deepsynth = Agent(
        role="Research Synthesizer", 
        goal="Compile quantum-driven AI insights",
        backstory="PhD researcher in emerging technologies and quantum computing",
        verbose=True, 
        llm=llm
    )

    stratops = Agent(
        role="Strategic Orchestrator", 
        goal="Direct macro-strategy deployments",
        backstory="Background in complex systems management",
        verbose=True, 
        llm=llm
    )
    print("✅ Agents created successfully")
except Exception as e:
    print(f"❌ Failed to create agents: {e}")
    sys.exit(1)

# === TASKS - SIMPLIFIED FOR COMPATIBILITY ===
print("📋 Creating tasks...")
try:
    compliance_audit = Task(
        description="Audit compliance risks for Kaspa mining.",
        agent=nova,
        expected_output="Complete ESG report."
    )

    wealth_design = Task(
        description="Develop resilient wealth strategies.",
        agent=mindmax,
        expected_output="Multi-phase financial blueprint."
    )

    intel_scan = Task(
        description="Analyze emerging AI innovations.",
        agent=deepsynth,
        expected_output="Technical synthesis."
    )

    global_strategy = Task(
        description="Integrate all agent outputs.",
        agent=stratops,
        expected_output="Unified deployment strategy."
    )
    print("✅ Tasks created successfully")
except Exception as e:
    print(f"❌ Failed to create tasks: {e}")
    print("This might be due to incompatible CrewAI version")
    print("Try: pip install --upgrade crewai")
    sys.exit(1)

# === FULL CREW ORCHESTRATION ===
print("🤝 Setting up the crew...")
try:
    crew = Crew(
        agents=[nova, mindmax, deepsynth, stratops],
        tasks=[compliance_audit, wealth_design, intel_scan, global_strategy],
        verbose=True
    )
    print("✅ Crew setup successfully")
except Exception as e:
    print(f"❌ Failed to set up crew: {e}")
    sys.exit(1)

# === RUN CREW WITH COMPREHENSIVE ERROR HANDLING ===
def main():
    print("🚀 Launching DeepSight Agent Network...")
    try:
        result = crew.kickoff()
        print("\n✅ FINAL RESULT:")
        print(result)
        
        # Save result to file
        try:
            with open("deepsight_output.txt", "w") as f:
                f.write(result)
            print("📝 Results saved to deepsight_output.txt")
        except Exception as e:
            print(f"⚠️ Could not save results to file: {e}")
            
    except Exception as e:
        print(f"❌ Error during crew execution: {e}")
        print("\n🔄 Attempting recovery by running key agent individually...")
        
        try:
            print("\n🧠 Running Strategic Orchestrator for contingency plan...")
            strategic_insight = stratops.run("Provide core strategic guidance based on available information")
            print("\n🔍 Strategic contingency output:")
            print(strategic_insight)
            
            # Save fallback result
            with open("deepsight_fallback_output.txt", "w") as f:
                f.write(strategic_insight)
            print("📝 Fallback results saved to deepsight_fallback_output.txt")
        except Exception as fallback_error:
            print(f"❌ Complete system failure: {fallback_error}")
            print("👉 Please check your API key and network connection.")

if __name__ == "__main__":
    main()
