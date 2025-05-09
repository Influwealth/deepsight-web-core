﻿import os

print('🔍 Checking environment variables...')
for var in ['HUGGINGFACE_API_KEY', 'GITHUB_TOKEN']:
    value = os.getenv(var)
    if value:
        print(f'✅ {var} is set')
    else:
        print(f'⚠️ {var} is missing! Please set it in your .env file.')
