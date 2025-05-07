import subprocess
import os
# Ensure public/ directory exists
output_dir = "deepsight-web-core/public"
os.makedirs(output_dir, exist_ok=True)

# Create essential deployment files
with open(f"{output_dir}/index.html", "w") as f:
    f.write("<!DOCTYPE html><html><body><h1>Auto Deployed</h1></body></html>")

with open(f"{output_dir}/styles.css", "w") as f:
    f.write("body { background-color: lightblue; }")

with open(f"{output_dir}/script.js", "w") as f:
    f.write("console.log('Auto deployed');")

# Add all changes
subprocess.run(["git", "add", "."], check=True)

# Check if there are staged changes before committing
if subprocess.run(["git", "diff", "--cached", "--quiet"]).returncode != 0:
    subprocess.run(["git", "commit", "-m", "Ensured Netlify public directory exists"], check=True)
    subprocess.run(["git", "push", "origin", "Qbint", "--force"], check=True)
else:
    print("No changes to commit. Skipping commit.")

print("Deployment setup completed successfully!")




