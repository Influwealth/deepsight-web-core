﻿import os
import subprocess

print('🚀 Starting Full DeepSight Deployment...')

# Install dependencies
subprocess.run('pip install -r requirements.txt', shell=True)

# Initialize Git & Push Changes
subprocess.run('git init', shell=True)
subprocess.run('git add .', shell=True)
subprocess.run('git commit -m \
Auto-deploy:
DeepSight
System\', shell=True)
subprocess.run('git push origin Qbint', shell=True)

# Deploy to Netlify
subprocess.run('netlify deploy', shell=True)

print('✅ DeepSight Deployment Complete!')
