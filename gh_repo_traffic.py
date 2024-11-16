# gh_repo_traffic.py

import os
import logging
from typing import List, Tuple, Dict, Any
from dotenv import load_dotenv
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('gh_repo_traffic.log')
    ]
)

def load_credentials() -> Tuple[str, str]:
    """
    Load GitHub token and username from the .env file.

    Returns
    -------
    Tuple[str, str]
        A tuple containing the GitHub token and username.
    """
    load_dotenv()
    token = os.getenv("GITHUB_TOKEN", "")
    username = os.getenv("GITHUB_USERNAME", "")
    if not token or not username:
        logging.error("GITHUB_TOKEN or GITHUB_USERNAME not found in .env file.")
        raise EnvironmentError("Missing GITHUB_TOKEN or GITHUB_USERNAME in .env file.")
    logging.info("Credentials loaded successfully.")
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
    """
    headers = {"Authorization": f"token {token}"}
    repo_url = f"https://api.github.com/users/{username}/repos"
    try:
        response = requests.get(repo_url, headers=headers)
        response.raise_for_status()
        repositories = [repo["full_name"] for repo in response.json()]
        logging.info(f"Fetched {len(repositories)} repositories for user: {username}.")
        return repositories
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch repositories for user: {username}. Error: {e}")
        raise


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
    """
    headers = {"Authorization": f"token {token}"}
    traffic_data = []

    for repo in repos:
        traffic_url = f"https://api.github.com/repos/{repo}/traffic/views"
        try:
            traffic_response = requests.get(traffic_url, headers=headers)
            traffic_response.raise_for_status()
            repo_data = traffic_response.json()
            traffic_data.append(
                {
                    "Repository": repo,
                    "Total Views": repo_data["count"],
                    "Unique Visitors": repo_data["uniques"],
                    "View Timestamps": ", ".join(
                        [
                            f"{view['timestamp']} ({view['count']} views)"
                            for view in repo_data.get("views", [])
                        ]
                    ),
                }
            )
            logging.info(f"Fetched traffic data for repository: {repo}.")
        except requests.exceptions.RequestException as e:
            logging.warning(f"Failed to fetch traffic data for repository: {repo}. Error: {e}")
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
    """
    if not traffic_data:
        logging.warning("No traffic data to display.")
        print("No traffic data available.")
        return

    df = pd.DataFrame(traffic_data)
    print("Traffic Data per Repository:")
    print(df.to_string(index=False))

    # Plot a bar chart for total views by repository
    plt.figure(figsize=(12, 8))
    df.plot(
        x="Repository",
        y="Total Views",
        kind="bar",
        legend=False,
        color="skyblue",
        ax=plt.gca(),
    )
    plt.title(f"GitHub Traffic Views per Repository for {username}")
    plt.ylabel("Total Views")
    plt.xlabel("Repository")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig("bar_chart.png")
    plt.show()
    logging.info("Traffic data displayed and bar chart saved as 'bar_chart.png'.")


if __name__ == "__main__":
    try:
        token, username = load_credentials()
        repositories = fetch_repositories(token, username)
        traffic_data = fetch_traffic_data(token, repositories)
        display_traffic_data(traffic_data, username)
    except Exception as e:
        logging.critical(f"An error occurred: {e}")
