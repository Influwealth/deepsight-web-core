# -*- coding: utf-8 -*-
import subprocess

# Install dependencies
subprocess.run(["pip", "install", "-r", "requirements.txt"], shell=True, check=True)

# Set up Git configuration
subprocess.run(["git", "config", "--global", "user.name", "Influwealth"], shell=True, check=True)
subprocess.run(["git", "config", "--global", "user.email", "influwealth@example.com"], shell=True, check=True)

# Commit and push changes
subprocess.run(["git", "add", "."], shell=True, check=True)
subprocess.run(["git", "commit", "-m", "Finalized deployment setup"], shell=True, check=True)
subprocess.run(["git", "push", "origin", "Qbint", "--force"], shell=True, check=True)

print("âœ… Deployment completed successfully!")

