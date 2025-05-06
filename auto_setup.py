#!/usr/bin/env python3
"""
DeepSight + WealthBridge Setup Script
This script sets up the initial project structure and files needed for the
DeepSight + WealthBridge project and initiates the first GitHub deployment.
"""

import os
import sys
import logging
import subprocess
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Project directory structure
PROJECT_DIRS = [
    "agents",
    "templates",
    "static",
    "config",
    "logs"
]

# === Environment Variables Configuration ===
ENV_CONTENT = """# DeepSight + WealthBridge Environment Variables
# API Keys - Replace with your actual keys
HUGGINGFACE_API_KEY=hf_your_api_key_here
GITHUB_TOKEN=your_github_token_here

# Configuration Settings
LOG_LEVEL=INFO
DEPLOYMENT_BRANCH=main
REPO_NAME=deepsight-web-core

# Agent Configuration
AGENT_TEMPERATURE=0.7
MAX_TOKENS=4000
"""

# === Project Dependencies ===
REQ_CONTENT = """# DeepSight + WealthBridge Dependencies
# Core libraries
crewai==0.29.2
litellm==1.67.1
python-dotenv==1.0.1
PyGithub==2.2.0

# Additional utilities
requests==2.31.0
pyyaml==6.0.1
rich==13.5.2
jinja2==3.1.2

# Development dependencies
pytest==7.4.0
black==23.7.0
isort==5.12.0
"""

# === HTML Template ===
HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="DeepSight and WealthBridge AI Agent Network Dashboard">
    <title>DeepSight + WealthBridge</title>
    <style>
        :root {
            --primary-color: #007BFF;
            --primary-dark: #0056b3;
            --background-color: #f4f6f8;
            --text-color: #333;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--background-color);
            color: var(--text-color);
            padding: 2rem;
            text-align: center;
            margin: 0;
            line-height: 1.6;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            color: var(--primary-color);
        }
        
        p {
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 1.5rem;
        }
        
        .timestamp {
            font-size: 0.9rem;
            color: #666;
            margin-top: 2rem;
        }
        
        .status {
            display: inline-block;
            background-color: #e8f4ff;
            border-left: 4px solid var(--primary-color);
            padding: 1rem;
            text-align: left;
            margin: 1rem 0;
            width: 100%;
            box-sizing: border-box;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>DeepSight + WealthBridge Agent Network</h1>
        <p>This site is deployed automatically by your AI agent system via GitHub + Netlify.</p>
        
        <div class="status">
            <p><strong>Status:</strong> Initial setup complete</p>
            <p><strong>Next steps:</strong> The agent system will begin monitoring and generating insights automatically.</p>
        </div>
        
        <p class="timestamp">Generated on: {timestamp}</p>
    </div>
</body>
</html>""".format(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# === GitHub Push Script ===
PUSH_SCRIPT_CONTENT = """#!/usr/bin/env python3
\"\"\"
GitHub Deployment Script
This script handles the automatic deployment of HTML content to GitHub,
which then triggers a Netlify build.
\"\"\"

import os
import sys
import logging
from dotenv import load_dotenv
from github import Github
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/github_deployment.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def main():
    # Load environment variables
    load_dotenv()
    
    # Get GitHub token from environment
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token or github_token == "your_github_token_here":
        error_msg = "GitHub token not found in .env or using default value"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    # Get repository name (default to deepsight-web-core if not specified)
    repo_name = os.getenv("REPO_NAME", "deepsight-web-core")
    branch_name = os.getenv("DEPLOYMENT_BRANCH", "main")
    
    try:
        # Connect to GitHub
        gh = Github(github_token)
        user = gh.get_user()
        logger.info(f"Authenticated as GitHub user: {user.login}")
        
        # Get repository
        repo = user.get_repo(repo_name)
        logger.info(f"Connected to repository: {repo.full_name}")
        
        # Read HTML content
        try:
            with open("index.html", "r") as file:
                content = file.read()
            logger.info("Successfully read index.html content")
        except Exception as e:
            error_msg = f"Failed to read index.html: {str(e)}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Create unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"index-{timestamp}.html"
        
        # Create commit message
        commit_message = f"DeepSight deployment at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Check if branch exists and create if necessary
        try:
            repo.get_branch(branch_name)
            logger.info(f"Using existing branch: {branch_name}")
        except Exception:
            logger.warning(f"Branch '{branch_name}' not found, creating it")
            # Get default branch as source
            default_branch = repo.default_branch
            default_branch_ref = repo.get_git_ref(f"heads/{default_branch}")
            # Create new branch
            repo.create_git_ref(f"refs/heads/{branch_name}", default_branch_ref.object.sha)
            logger.info(f"Created new branch: {branch_name}")
        
        # Push file to GitHub
        result = repo.create_file(
            path=filename,
            message=commit_message,
            content=content,
            branch=branch_name
        )
        
        logger.info(f"âœ… Successfully pushed '{filename}' to GitHub")
        logger.info(f"Commit SHA: {result['commit'].sha}")
        
        # Also update the main index.html if it exists in the repo
        try:
            main_index = repo.get_contents("index.html", ref=branch_name)
            logger.info("Updating main index.html file")
            repo.update_file(
                path="index.html",
                message=f"Update main index.html at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                content=content,
                sha=main_index.sha,
                branch=branch_name
            )
            logger.info("âœ… Successfully updated main index.html")
        except Exception as e:
            logger.info(f"Creating new main index.html file")
            repo.create_file(
                path="index.html",
                message=f"Create main index.html at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                content=content,
                branch=branch_name
            )
            logger.info("âœ… Successfully created main index.html")
        
        print(f"âœ… Deployment successful! File: {filename}")
        print(f"   View at: https://github.com/{repo.full_name}/blob/{branch_name}/{filename}")
        
    except Exception as e:
        logger.error(f"âŒ Failed to push to GitHub: {str(e)}")
        print(f"âŒ Error: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Run the main function
    success = main()
    sys.exit(0 if success else 1)
"""

def create_file(path, content, description="file"):
    """Create a file with the given content if it doesn't exist"""
    if not os.path.exists(path):
        try:
            with open(path, "w") as f:
                f.write(content)
            logger.info(f"âœ… Created {description} at {path}")
            return True
        except Exception as e:
            logger.error(f"âŒ Failed to create {description} at {path}: {str(e)}")
            return False
    else:
        logger.info(f"â„¹ï¸ {description} already exists at {path}. Skipping creation.")
        return False

def create_directory(path):
    """Create a directory if it doesn't exist"""
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            logger.info(f"âœ… Created directory {path}")
            return True
        except Exception as e:
            logger.error(f"âŒ Failed to create directory {path}: {str(e)}")
            return False
    else:
        logger.info(f"â„¹ï¸ Directory {path} already exists. Skipping creation.")
        return False

def run_command(command, description="command"):
    """Run a shell command and log the output"""
    logger.info(f"Running {description}: {command}")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            capture_output=True
        )
        logger.info(f"âœ… {description} completed successfully")
        logger.debug(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"âŒ {description} failed with code {e.returncode}")
        logger.error(f"Error output: {e.stderr}")
        return False

def main():
    """Main execution function"""
    logger.info("ðŸš€ Starting DeepSight + WealthBridge project setup...")
    
    # Step 1: Create project directories
    logger.info("Setting up project directory structure...")
    for directory in PROJECT_DIRS:
        create_directory(directory)
    
    # Step 2: Create environment file
    create_file(".env", ENV_CONTENT, "environment file")
    
    # Step 3: Create requirements file
    create_file("requirements.txt", REQ_CONTENT, "requirements file")
    
    # Step 4: Create HTML template
    create_file("index.html", HTML_CONTENT, "HTML template")
    
    # Step 5: Create GitHub push script
    push_script_created = create_file("push_to_github.py", PUSH_SCRIPT_CONTENT, "GitHub push script")
    
    # Step 6: Create a simple README file
    readme_content = f"""# DeepSight + WealthBridge

AI-Powered Compliance, Strategy, and Content Automation

## Setup Instructions

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Configure your .env file with your API keys
3. Run the GitHub push script:
   ```
   python push_to_github.py
   ```

## Project Structure

- `agents/`: Agent configuration and logic
- `templates/`: HTML templates
- `static/`: Static assets
- `config/`: Configuration files
- `logs/`: Log files

Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    create_file("README.md", readme_content, "README file")
    
    # Step 7: Create .gitignore file
    gitignore_content = """# Environment variables
.env

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Logs
logs/
*.log

# Virtual Environment
venv/
env/
ENV/

# IDE files
.idea/
.vscode/
*.swp
*.swo
"""
    create_file(".gitignore", gitignore_content, ".gitignore file")
    
    # Make push script executable
    if push_script_created and os.name != 'nt':  # Not on Windows
        try:
            os.chmod("push_to_github.py", 0o755)
            logger.info("âœ… Made push_to_github.py executable")
        except Exception as e:
            logger.warning(f"âš ï¸ Could not make push_to_github.py executable: {str(e)}")
    
    # Step 8: Attempt to run the push script if environment is properly configured
    logger.info("\nðŸ” Checking if GitHub token is configured...")
    try:
        with open(".env", "r") as f:
            env_content = f.read()
        
        if "your_github_token_here" in env_content:
            logger.warning("âš ï¸ GitHub token not configured. Please update the .env file with your GitHub token.")
            print("\nâš ï¸ Setup completed but GitHub deployment was skipped.")
            print("   Please edit the .env file to add your GitHub token, then run:")
            print("   python push_to_github.py")
        else:
            logger.info("GitHub token appears to be configured. Running initial push...")
            print("\nðŸŽ‰ All files have been created or updated. Now running the initial push to GitHub...")
            
            # Create logs directory for the push script
            create_directory("logs")
            
            # Run the push script
            if run_command("python push_to_github.py", "initial GitHub push"):
                print("\nâœ… Initial GitHub push completed successfully!")
            else:
                print("\nâŒ Initial GitHub push failed. Please check the logs and try again.")
    except Exception as e:
        logger.error(f"âŒ Error checking GitHub token: {str(e)}")
        print("\nâš ï¸ Setup completed but GitHub deployment check failed.")
    
    print("\nðŸ“‹ Setup Summary:")
    print("   - Project structure created")
    print("   - Configuration files initialized")
    print("   - Deployment script created")
    print("\nðŸ“ Next Steps:")
    print("   1. Edit .env file with your actual API keys")
    print("   2. Install dependencies: pip install -r requirements.txt")
    print("   3. Run the push script: python push_to_github.py")

if __name__ == "__main__":
    main()
