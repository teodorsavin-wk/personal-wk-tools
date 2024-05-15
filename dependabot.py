import os
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

repo_urls = []

# Iterate over each repo name in the list
for repo_name in repo_names:
    # Construct the complete URL
    url = base_url + repo_name + "/pulls"

    # Make the GET request
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        pulls = response.json()

        # Extract repo URLs for PRs created by "dependabot"
        for pull in pulls:
            if pull.get("user", {}).get("login") == "dependabot":
                if "head" in pull and "repo" in pull["head"]:
                    repo_url = pull["html_url"]
                    repo_urls.append(repo_url)
        if not repo_urls:
            print(f"No dependabot for {repo_name}")
        else:
            print("URLs for Open PRs created by 'dependabot' for " + url + " :")
            for repo_url in repo_urls:
                print(repo_url)
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        print(response.text)