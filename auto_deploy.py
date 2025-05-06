import subprocess

# Configure Git settings (use local instead of global)
subprocess.run(["git", "config", "--local", "user.name", "Influwealth"], check=True)
subprocess.run(["git", "config", "--local", "user.email", "influwealth@example.com"], check=True)

# Add all changes
subprocess.run(["git", "add", "."], check=True)

# Check if there are staged changes before committing
if subprocess.run(["git", "diff", "--cached", "--quiet"]).returncode != 0:
    subprocess.run(["git", "commit", "-m", "Finalized deployment setup"], check=True)
    subprocess.run(["git", "push", "origin", "Qbint", "--force"], check=True)
else:
    print("No changes to commit. Skipping commit.")

print("Deployment setup completed successfully!")


