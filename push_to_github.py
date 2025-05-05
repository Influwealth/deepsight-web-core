from dotenv import load_dotenv
import os
import logging
from github import Github
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# === GITHUB AUTHENTICATION ===
def authenticate_github():
    """Authenticate with GitHub using token from environment variables"""
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("GitHub token not found. Set it in your .env file.")
    
    try:
        # Connect to GitHub
        gh = Github(github_token)
        # Test connection
        user = gh.get_user()
        logger.info(f"Successfully authenticated as {user.login}")
        return gh
    except Exception as e:
        logger.error(f"Failed to authenticate with GitHub: {str(e)}")
        raise

# === GET REPOSITORY ===
def get_repository(gh, repo_name="deepsight-web-core"):
    """Get the specified repository object"""
    try:
        repo = gh.get_user().get_repo(repo_name)
        logger.info(f"Connected to repository: {repo.full_name}")
        return repo
    except Exception as e:
        logger.error(f"Failed to access repository {repo_name}: {str(e)}")
        raise

# === GENERATE HTML CONTENT ===
def generate_html_content():
    """Generate HTML content with current timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DeepSight Agent Output</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            color: #333;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
        }}
        .timestamp {{
            color: #7f8c8d;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Auto-Generated Content from DeepSynth</h1>
        <p>This page was created by your AI agent system and is deployed automatically via GitHub + Netlify.</p>
        <p class="timestamp">Generated on: {timestamp}</p>
    </div>
</body>
</html>"""

# === PUSH TO GITHUB ===
def push_to_github(repo, content, branch="main"):
    """Push content to GitHub repository"""
    try:
        # Create a more descriptive commit message
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_message = f"Agent deployment: DeepSight web update at {timestamp}"
        
        # Create a new file each time with organized naming
        filename = f"index-{datetime.now().strftime('%Y%m%d%H%M%S')}.html"
        
        # Check if branch exists
        try:
            repo.get_branch(branch)
            logger.info(f"Branch '{branch}' exists, proceeding with commit")
        except Exception:
            logger.warning(f"Branch '{branch}' not found, creating it")
            # Get default branch as source
            default_branch = repo.default_branch
            default_branch_ref = repo.get_git_ref(f"heads/{default_branch}")
            default_branch_sha = default_branch_ref.object.sha
            # Create new branch
            repo.create_git_ref(f"refs/heads/{branch}", default_branch_sha)
            
        # Push the content to GitHub
        result = repo.create_file(
            path=filename,
            message=commit_message,
            content=content,
            branch=branch
        )
        
        logger.info(f"✅ Successfully pushed '{filename}' to GitHub.")
        logger.info(f"Commit SHA: {result['commit'].sha}")
        
        return {"success": True, "filename": filename, "commit_sha": result['commit'].sha}
    except Exception as e:
        logger.error(f"❌ Failed to push to GitHub: {str(e)}")
        return {"success": False, "error": str(e)}

# === MAIN EXECUTION ===
def main():
    """Main execution function"""
    try:
        # Authenticate and get repository
        gh = authenticate_github()
        repo = get_repository(gh)
        
        # Generate content
        html_content = generate_html_content()
        
        # Push to GitHub
        result = push_to_github(repo, html_content)
        
        if result["success"]:
            print(f"✅ Deployment successful! File: {result['filename']}")
            print(f"   Commit SHA: {result['commit_sha']}")
        else:
            print(f"❌ Deployment failed: {result['error']}")
            
    except Exception as e:
        logger.critical(f"Script execution failed: {str(e)}")
        print(f"❌ Critical error: {str(e)}")

# Execute the script if run directly
if __name__ == "__main__":
    main()