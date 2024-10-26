# main.py

from gh_repo_traffic import load_credentials, fetch_repositories, fetch_traffic_data, display_traffic_data

def main() -> None:
    """
    Main function to load credentials, fetch repository traffic data,
    and display it in a table and bar chart.
    """
    # Step 1: Load GitHub token and username from environment
    token, username = load_credentials()
    if not token or not username:
        print("Please ensure GITHUB_TOKEN and GITHUB_USERNAME are set in the .env file.")
        return

    # Step 2: Fetch repositories for the specified user
    repos = fetch_repositories(token, username)
    if not repos:
        print("No repositories found or failed to fetch repositories.")
        return

    # Step 3: Fetch and display traffic data for each repository
    traffic_data = fetch_traffic_data(token, repos)
    if traffic_data:
        display_traffic_data(traffic_data, username)

# Standard boilerplate to run the main function
if __name__ == "__main__":
    main()

