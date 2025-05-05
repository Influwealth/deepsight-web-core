#!/usr/bin/env python3
"""
Environment Variable Validation Script
This script validates that required environment variables are properly loaded and configured.
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define required environment variables and their descriptions
REQUIRED_VARIABLES = {
    "GITHUB_TOKEN": "GitHub Personal Access Token for repository operations",
    "HUGGINGFACE_API_KEY": "HuggingFace API Key for AI model access"
}

# Optional environment variables
OPTIONAL_VARIABLES = {
    "LOG_LEVEL": "Logging level (default: INFO)",
    "DEPLOYMENT_BRANCH": "GitHub branch for deployment (default: main)",
    "REPO_NAME": "GitHub repository name (default: deepsight-web-core)"
}

def find_env_file() -> Optional[Path]:
    """Find the .env file in the current or parent directories"""
    current_dir = Path.cwd()
    
    # Check current directory
    env_path = current_dir / ".env"
    if env_path.exists():
        return env_path
    
    # Check parent directory (up to 2 levels)
    for i in range(2):
        current_dir = current_dir.parent
        env_path = current_dir / ".env"
        if env_path.exists():
            return env_path
    
    return None

def load_environment_variables() -> bool:
    """Load environment variables from .env file and validate required ones"""
    # Find .env file
    env_path = find_env_file()
    
    if env_path:
        logger.info(f"Found .env file at: {env_path}")
        # Load environment variables from .env file
        load_dotenv(dotenv_path=env_path)
    else:
        logger.warning("No .env file found. Looking for environment variables in system environment.")
    
    return True

def validate_environment_variables() -> Dict[str, bool]:
    """Validate that required environment variables are set and not empty"""
    results = {}
    
    for var_name, var_desc in REQUIRED_VARIABLES.items():
        value = os.getenv(var_name)
        if value is None:
            logger.error(f"❌ Missing required environment variable: {var_name}")
            results[var_name] = False
        elif value.strip() == "":
            logger.error(f"❌ Required environment variable {var_name} is empty")
            results[var_name] = False
        elif "your_" in value.lower() and "_here" in value.lower():
            logger.error(f"❌ Environment variable {var_name} contains placeholder value")
            results[var_name] = False
        else:
            # Mask sensitive information in logs
            masked_value = value[:4] + "*" * (len(value) - 4) if len(value) > 8 else "****"
            logger.info(f"✅ Environment variable {var_name} is set: {masked_value}")
            results[var_name] = True
    
    # Check optional variables
    for var_name, var_desc in OPTIONAL_VARIABLES.items():
        value = os.getenv(var_name)
        if value is None:
            logger.info(f"ℹ️ Optional environment variable {var_name} is not set")
        else:
            logger.info(f"✅ Optional environment variable {var_name} is set: {value}")
    
    return results

def check_for_additional_variables() -> List[str]:
    """Check for any additional environment variables that start with specific prefixes"""
    prefixes = ["GITHUB_", "HUGGINGFACE_", "OPENAI_", "AWS_", "AZURE_", "GCP_"]
    additional_vars = []
    
    for key in os.environ:
        for prefix in prefixes:
            if key.startswith(prefix) and key not in REQUIRED_VARIABLES and key not in OPTIONAL_VARIABLES:
                additional_vars.append(key)
                # Mask potentially sensitive values
                value = os.getenv(key)
                masked_value = value[:4] + "*" * (len(value) - 4) if value and len(value) > 8 else "****"
                logger.info(f"ℹ️ Found additional environment variable: {key} = {masked_value}")
    
    return additional_vars

def suggest_fixes(results: Dict[str, bool]) -> None:
    """Suggest fixes for missing or invalid environment variables"""
    if all(results.values()):
        return
    
    print("\n📝 Suggested fixes for environment variables:")
    
    for var_name, is_valid in results.items():
        if not is_valid:
            print(f"  • {var_name}: {REQUIRED_VARIABLES[var_name]}")
            if var_name == "GITHUB_TOKEN":
                print("    - Create a token at: https://github.com/settings/tokens")
                print("    - Required scopes: repo, workflow")
            elif var_name == "HUGGINGFACE_API_KEY":
                print("    - Create a token at: https://huggingface.co/settings/tokens")
    
    print("\nAdd these variables to your .env file in the format:")
    print("VARIABLE_NAME=your_value_here")

def main() -> int:
    """Main execution function"""
    print("🔍 Checking Environment Variables\n")
    
    # Load environment variables
    load_environment_variables()
    
    # Validate required environment variables
    validation_results = validate_environment_variables()
    
    # Check for additional variables
    additional_vars = check_for_additional_variables()
    
    # Print summary
    print("\n📊 Environment Variables Summary:")
    total = len(validation_results)
    valid = sum(validation_results.values())
    print(f"  • Required variables: {valid}/{total} valid")
    print(f"  • Additional variables detected: {len(additional_vars)}")
    
    # Print current environment
    print(f"\n🌐 Current Environment:")
    print(f"  • Working directory: {os.getcwd()}")
    print(f"  • Python version: {sys.version.split()[0]}")
    print(f"  • Platform: {sys.platform}")
    
    # Suggest fixes if needed
    if not all(validation_results.values()):
        suggest_fixes(validation_results)
        return 1
    
    print("\n✅ All required environment variables are properly configured!")
    
    # Print values (with masking for security)
    print("\n🔐 Current Values (partial):")
    for var_name in REQUIRED_VARIABLES:
        value = os.getenv(var_name, "")
        masked_value = value[:4] + "*" * (len(value) - 4) if len(value) > 8 else "****"
        print(f"  • {var_name}: {masked_value}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())