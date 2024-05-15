import os
from datetime import datetime, timezone
import requests

# Load the token from the environment variable
token = os.getenv("HOMEBREW_GITHUB_TOKEN")

if not token:
    raise ValueError("HOMEBREW_GITHUB_TOKEN environment variable not set")

# Define the headers and URL
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {token}",
    "X-GitHub-Api-Version": "2022-11-28"
}

base_url = "https://api.github.com/repos/Workiva/"
repo_names = [
    "xbrl-module",
    "xml-translator",
    "xbrl-translator",
    "xbrl-orchestrator",
    "xbrl-reports",
    "xbrl-model",
    "language-translator",
    "language_translator_client",
    "xbrl-data-server"
]

# Iterate over each repo name in the list
for repo_name in repo_names:

    print('-----------------------------------')
    print(f"Checking for dependabot PRs in {repo_name}")

    # Construct the complete URL
    url = base_url + repo_name + "/pulls"

    # Make the GET request
    response = requests.get(url, headers=headers)

    repo_urls = []
    # Check if the request was successful
    if response.status_code == 200:
        pulls = response.json()

        # Extract repo URLs for PRs created by "dependabot"
        for pull in pulls:
            if pull.get("user", {}).get("login") == "dependabot":
                if "head" in pull and "repo" in pull["head"]:
                    repo_url = pull["html_url"]
                    created_at = pull["created_at"]
                    # Calculate the number of days since the PR was opened
                    created_date = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                    current_date = datetime.now(timezone.utc)

                    days_open = (current_date - created_date).days
                    repo_urls.append((repo_url, days_open))
        if not repo_urls:
            print(f"No dependabot PRs for {repo_name}")
        else:
            print("URLs for Open PRs created by 'dependabot' for " + url + " :")
            for repo_url, days_open in repo_urls:
                print(f"    - {repo_url} - Open for {days_open} days")
        print('-----------------------------------')
        print('')
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        print(response.text)