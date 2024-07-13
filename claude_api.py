import os
import requests
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
ANTHROPIC_API_URL = 'https://api.anthropic.com/v1/complete'

def generate_readme(project_name, project_description, project_features):
    prompt = f"""Generate a README markdown for a GitHub project with the following details:

Project Name: {project_name}
Project Description: {project_description}
Key Features: {', '.join(project_features)}

Please include sections for Installation, Usage, and Contributing."""

    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': ANTHROPIC_API_KEY,
    }

    data = {
        'prompt': prompt,
        'max_tokens_to_sample': 1000,
        'model': 'claude-v1',
    }

    response = requests.post(ANTHROPIC_API_URL, headers=headers, json=data)
    response.raise_for_status()
    return response.json()['completion']
