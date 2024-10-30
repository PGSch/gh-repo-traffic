
# GitHub Repository Traffic Analyzer

[![GitHub Release](https://img.shields.io/github/v/release/PGSch/AutoCoder?logo=github)](https://github.com/PGSch/AutoCoder/releases)
[![GitHub License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE.txt)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-brightgreen)](https://www.python.org/downloads/)
[![Sponsor](https://img.shields.io/badge/sponsor-♥-f06292)](https://github.com/sponsors/PGSch)
[![Twitter Follow](https://img.shields.io/twitter/follow/pgschdev?style=social)](https://twitter.com/intent/follow?screen_name=pgschdev)

## Overview

**GitHub Repository Traffic Analyzer** is a Python-based tool that uses the GitHub API to fetch and analyze traffic data for all repositories under a given GitHub account. This tool provides insights into the number of views and unique visitors for each repository, and it visually displays the data as a bar chart. It's ideal for developers, project managers, and data analysts who want to monitor repository engagement and gain insights into visitor behavior.

## Features

- **Fetch Repository Data**: Retrieves all public repositories for a GitHub user.
- **Traffic Analysis**: Collects traffic data, including total views and unique visitors.
- **Data Visualization**: Displays traffic data as a table and bar chart.
- **Environment Variables**: Loads sensitive data (GitHub token and username) securely from a `.env` file.

## Directory Structure

```
.
├── LICENSE.txt             # License file
├── __init__.py             # Marks the project as a package
├── gh_repo_traffic.py      # Core functionality for fetching and displaying traffic data
├── main.py                 # Entry point to execute the analyzer
├── requirements.txt        # Python dependencies for the project
└── tests
    ├── __init__.py         # Marks the `tests` directory as a package
    └── tests.py            # Unit tests for core functionality
```

## Installation

### Prerequisites

- Python 3.10 or higher
- A GitHub Personal Access Token with permissions to read repository data

### Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/repository-traffic-analyzer.git
   cd repository-traffic-analyzer
   ```

2. **Create a virtual environment**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the `.env` file**

   Create a `.env` file in the root directory and add your GitHub token and username:

   ```env
   GITHUB_TOKEN=your_github_token
   GITHUB_USERNAME=your_github_username
   ```

## Usage

Run the main script to fetch and display traffic data:

```bash
python main.py
```

This will output a table showing each repository's traffic data (total views, unique visitors) and display a bar chart of the total views.

## Example Output

```plaintext
Traffic Data per Repository:
         Repository  Total Views  Unique Visitors  View Timestamps
0    user/repo1           10            5        2024-10-01T00:00:00Z (10 views)
1    user/repo2           25           18        2024-10-01T00:00:00Z (25 views)
```


![bar_chart_example](https://github.com/user-attachments/assets/b5fd4347-0b65-4248-9e31-c20277de3435)


## Running Tests

To ensure all functions work correctly, run the unit tests with:

```bash
python -m unittest discover -s tests
```

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request for any feature enhancements or bug fixes.

---

Feel free to reach out if you encounter issues or have feature requests. Happy analyzing!
