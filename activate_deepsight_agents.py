import os
from crewai import Agent, Task, Crew
from langchain.llms import HuggingFaceHub

# === LOAD KEYS ===
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
if not HUGGINGFACE_API_KEY:
    raise ValueError("Hugging Face API key not found. Set it in your .env file.")

# === CONFIGURE LLM ===
llm = HuggingFaceHub(
    repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
    huggingfacehub_api_token=HUGGINGFACE_API_KEY
)

# === DEEPSIGHT CORE AGENTS ===
nova = Agent(
    role="Risk & Compliance Analyst",
    goal="Ensure operational, ethical, and legal compliance across AI systems",
    backstory="Specialist in ESG, financial regulations, and AI safety.",
    verbose=True,
    llm=llm
)

mindmax = Agent(
    role="Autonomous Decision-Maker",
    goal="Execute high-level decisions with no human intervention.",
    backstory="Strategic agent empowered with autonomous logic trees.",
    verbose=True,
    llm=llm
)

deepsynth = Agent(
    role="Research Synthesizer",
    goal="Rapidly gather and synthesize domain intelligence.",
    backstory="Built to merge quantum data models with real-time intelligence.",
    verbose=True,
    llm=llm
)

stratops = Agent(
    role="Strategic Orchestrator",
    goal="Coordinate agents and macro-strategy deployments.",
    backstory="Commander-level AI agent directing DeepSight modules.",
    verbose=True,
    llm=llm
)

# === WEALTHBRIDGE / GGM AGENTS ===
asset_planner = Agent(
    role="Asset Planner",
    goal="Build scalable and resilient wealth strategies.",
    backstory="Expert in hybrid asset classes and sustainable yield.",
    verbose=True,
    llm=llm
)

risk_profiler = Agent(
    role="Risk Profiler",
    goal="Quantify threats and produce risk-to-reward matrices.",
    backstory="Deep evaluator of portfolio and operational risks.",
    verbose=True,
    llm=llm
)

market_analyst = Agent(
    role="Market Analyst",
    goal="Forecast and analyze global and regional financial trends.",
    backstory="Quantum-enhanced analyst for predictive modeling.",
    verbose=True,
    llm=llm
)

policy_advisor = Agent(
    role="Policy Advisor",
    goal="Validate compliance with ESG, legal, and ethical governance.",
    backstory="Expert in fintech regulation and social impact policy.",
    verbose=True,
    llm=llm
)

# === TASKS ===

# 🔐 Compliance Audit
compliance_audit = Task(
    description=(
        "Perform a full compliance audit for Kaspa mining operations, "
        "including regulatory, environmental, and financial risks. Output a detailed compliance status report, "
        "flagging high-risk areas and proposed mitigation strategies."
    ),
    expected_output="Complete compliance report with ESG score, risk factors, and legal readiness.",
    agent=nova
)

# ⚖️ Wealth Strategy Design
wealth_design = Task(
    description=(
        "Develop a sustainable and quantum-resilient wealth strategy for emerging markets, "
        "aligned with ESG and decentralized finance principles."
    ),
    expected_output="A multi-phase wealth blueprint integrating asset strategy, risk forecast, and ESG compliance.",
    agent=asset_planner
)

# 🧠 Strategic Call
strategic_call = Task(
    description="Based on risk and compliance reports, decide whether to proceed with Kaspa mining deployment.",
    expected_output="Final go/no-go decision and alternative scenarios.",
    agent=mindmax
)

# 📊 Market Forecast
market_forecast = Task(
    description="Analyze current financial and regulatory trends relevant to wealth systems in Sub-Saharan Africa.",
    expected_output="Market forecast with risk vectors and emerging opportunity maps.",
    agent=market_analyst
)

# 🧩 Policy Validation
policy_check = Task(
    description="Validate the new wealth strategy against ESG policies and emerging regulatory frameworks.",
    expected_output="Policy report with compliance gaps and suggested governance improvements.",
    agent=policy_advisor
)

# 🧠 Research Synthesis
intel_scan = Task(
    description="Compile emerging technologies, AI agents, and quantum-secure methods for financial innovation.",
    expected_output="Technical brief integrating cutting-edge tools for GGM system design.",
    agent=deepsynth
)

# 🧠 Strategic Coordination
global_strategy = Task(
    description="Integrate all agent outputs and present a unified go-forward strategy for WealthBridge's rollout.",
    expected_output="Unified deployment plan covering compliance, finance, tech, and policy integration.",
    agent=stratops
)

# === FULL CREW ORCHESTRATION ===
crew = Crew(
    agents=[
        nova, mindmax, deepsynth, stratops,
        asset_planner, risk_profiler, market_analyst, policy_advisor
    ],
    tasks=[
        compliance_audit, wealth_design, strategic_call,
        market_forecast, policy_check, intel_scan, global_strategy
    ],
    verbose=True
)

# === RUN CREW ===
if __name__ == "__main__":
    print("🧠 Activating DeepSight + WealthBridge Agent Network...")
    result = crew.kickoff()
    print("\n✅ FINAL SYNTHESIS RESULT:")
    print(result)