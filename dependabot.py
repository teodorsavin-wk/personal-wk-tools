import os
from datetime import datetime, timezone
import requests

TOKEN_ENV_VAR = "HOMEBREW_GITHUB_TOKEN"
GITHUB_PR_OWNER = "dependabot"
BASE_URL = "https://api.github.com/repos/Workiva/"
REPO_NAMES = [
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

def get_token():
    token = os.getenv(TOKEN_ENV_VAR)
    if not token:
        raise ValueError(f"{TOKEN_ENV_VAR} environment variable not set")
    return token

def get_headers(token):
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

def get_pulls(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve data: {response.status_code}\n{response.text}")
    return response.json()

def get_repo_urls(pulls):
    repo_urls = []
    for pull in pulls:
        if pull.get("user", {}).get("login") == GITHUB_PR_OWNER:
            if "html_url" in pull and "created_at" in pull:
                repo_url = pull["html_url"]
                created_at = pull["created_at"]
                created_date = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                current_date = datetime.now(timezone.utc)
                days_open = (current_date - created_date).days
                repo_urls.append((repo_url, days_open))
    return repo_urls

def print_repo_urls(repo_name, url, repo_urls):
    if not repo_urls:
        print(f"No {GITHUB_PR_OWNER} PRs for {repo_name}")
    else:
        print(f"URLs for Open PRs created by '{GITHUB_PR_OWNER}' for " + url + " :")
        for repo_url, days_open in repo_urls:
            print(f"    - {repo_url} - Open for {days_open} days")

def main():
    token = get_token()
    headers = get_headers(token)
    for repo_name in REPO_NAMES:
        print('-----------------------------------')
        print(f"Checking for {GITHUB_PR_OWNER} PRs in {repo_name}")
        url = BASE_URL + repo_name + "/pulls"
        pulls = get_pulls(url, headers)
        repo_urls = get_repo_urls(pulls)
        print_repo_urls(repo_name, url, repo_urls)
        print('-----------------------------------')
        print('')

if __name__ == "__main__":
    main()