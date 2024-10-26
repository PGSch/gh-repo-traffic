# gh_repo_traffic.py

import os
from typing import List, Tuple, Dict, Any
from dotenv import load_dotenv
import requests
import pandas as pd
import matplotlib.pyplot as plt

def load_credentials() -> Tuple[str, str]:
    """
    Load GitHub token and username from the .env file.

    Returns
    -------
    Tuple[str, str]
        A tuple containing the GitHub token and username.

    Examples
    --------
    >>> load_credentials()
    ('ghp_xxxxxxxx', 'PGSch')
    """
    load_dotenv()
    token = os.getenv("GITHUB_TOKEN", "")
    username = os.getenv("GITHUB_USERNAME", "")
    return token, username

def fetch_repositories(token: str, username: str) -> List[str]:
    """
    Fetch the list of repositories for a given GitHub user.

    Parameters
    ----------
    token : str
        GitHub API token for authentication.
    username : str
        GitHub username to fetch repositories for.

    Returns
    -------
    List[str]
        A list of repository names in the format 'username/repo_name'.

    Examples
    --------
    >>> fetch_repositories('ghp_xxxxxxxx', 'PGSch')
    ['PGSch/Repo1', 'PGSch/Repo2']
    """
    headers = {"Authorization": f"token {token}"}
    repo_url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(repo_url, headers=headers)
    if response.status_code == 200:
        return [repo['full_name'] for repo in response.json()]
    else:
        print(f"Failed to fetch repositories for user: {username}")
        return []

def fetch_traffic_data(token: str, repos: List[str]) -> List[Dict[str, Any]]:
    """
    Fetch traffic data for a list of repositories.

    Parameters
    ----------
    token : str
        GitHub API token for authentication.
    repos : List[str]
        List of repository names in the format 'username/repo_name'.

    Returns
    -------
    List[Dict[str, Any]]
        A list of dictionaries, each containing traffic data for a repository.

    Examples
    --------
    >>> fetch_traffic_data('ghp_xxxxxxxx', ['PGSch/Repo1', 'PGSch/Repo2'])
    [{'Repository': 'PGSch/Repo1', 'Total Views': 10, 'Unique Visitors': 5, 'View Timestamps': '2024-10-01T00:00:00Z (10 views)'}]
    """
    headers = {"Authorization": f"token {token}"}
    traffic_data = []

    for repo in repos:
        traffic_url = f"https://api.github.com/repos/{repo}/traffic/views"
        traffic_response = requests.get(traffic_url, headers=headers)
        
        if traffic_response.status_code == 200:
            repo_data = traffic_response.json()
            traffic_data.append({
                "Repository": repo,
                "Total Views": repo_data["count"],
                "Unique Visitors": repo_data["uniques"],
                "View Timestamps": ", ".join([f"{view['timestamp']} ({view['count']} views)" for view in repo_data["views"]])
            })
        else:
            print(f"Failed to fetch traffic data for {repo}")
    
    return traffic_data

def display_traffic_data(traffic_data: List[Dict[str, Any]], username: str) -> None:
    """
    Display traffic data in a table and plot total views per repository.

    Parameters
    ----------
    traffic_data : List[Dict[str, Any]]
        A list of dictionaries containing traffic data for each repository.
    username : str
        GitHub username for which the traffic data is being displayed.

    Returns
    -------
    None

    Examples
    --------
    >>> display_traffic_data([{'Repository': 'PGSch/Repo1', 'Total Views': 10, 'Unique Visitors': 5, 'View Timestamps': '2024-10-01T00:00:00Z (10 views)'}], 'PGSch')
    Traffic Data per Repository:
      Repository       Total Views  Unique Visitors      View Timestamps
    -----------------------------------------------------------------------
      PGSch/Repo1         10            5            2024-10-01T00:00:00Z (10 views)
    (Displays a bar chart for total views per repository.)
    """
    df = pd.DataFrame(traffic_data)
    print("Traffic Data per Repository:")
    print(df.to_string(index=False))

    # Plot a bar chart for total views by repository
    plt.figure(figsize=(12, 8))
    df.plot(x="Repository", y="Total Views", kind="bar", legend=False, color="skyblue", ax=plt.gca())
    plt.title(f"GitHub Traffic Views per Repository for {username}")
    plt.ylabel("Total Views")
    plt.xlabel("Repository")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig("bar_chart.png")
    plt.show()
