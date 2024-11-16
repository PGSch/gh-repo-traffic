# tests/test.py
# python -m unittest discover -s tests -v

import unittest
from termcolor import colored
from unittest.mock import patch, MagicMock
from gh_repo_traffic import (
    load_credentials,
    fetch_repositories,
    fetch_traffic_data,
    display_traffic_data,
)
import os
from xmlrunner import XMLTestRunner
from colorama import init

init()


class ColoredTestResult(unittest.TextTestResult):
    def addSuccess(self, test):
        super().addSuccess(test)
        self.stream.write(colored("PASS", "green") + "\n")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.stream.write(colored("FAIL", "red") + "\n")

    def addError(self, test, err):
        super().addError(test, err)
        self.stream.write(colored("ERROR", "yellow") + "\n")


class ColoredTestRunner(unittest.TextTestRunner):
    def _makeResult(self):
        return ColoredTestResult(self.stream, self.descriptions, self.verbosity)


class TestGHRepoTraffic(unittest.TestCase):
    @patch.dict(
        os.environ, {"GITHUB_TOKEN": "fake_token", "GITHUB_USERNAME": "fake_user"}
    )
    def test_load_credentials(self):
        """Test that load_credentials returns the correct token and username from the environment."""
        token, username = load_credentials()
        self.assertEqual(token, "fake_token")
        self.assertEqual(username, "fake_user")

    @patch("gh_repo_traffic.requests.get")
    def test_fetch_repositories(self, mock_get):
        """Test that fetch_repositories returns a list of repositories when API call is successful."""
        # Mock API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"full_name": "fake_user/fake_repo"}]
        mock_get.return_value = mock_response

        repos = fetch_repositories("fake_token", "fake_user")
        self.assertEqual(repos, ["fake_user/fake_repo"])
        mock_get.assert_called_once_with(
            "https://api.github.com/users/fake_user/repos",
            headers={"Authorization": "token fake_token"},
        )

    @patch("gh_repo_traffic.requests.get")
    def test_fetch_repositories_fail(self, mock_get):
        """Test that fetch_repositories returns an empty list when API call fails."""
        # Mock failed API response
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        repos = fetch_repositories("fake_token", "fake_user")
        self.assertEqual(repos, [])
        mock_get.assert_called_once_with(
            "https://api.github.com/users/fake_user/repos",
            headers={"Authorization": "token fake_token"},
        )

    @patch("gh_repo_traffic.requests.get")
    def test_fetch_traffic_data(self, mock_get):
        """Test that fetch_traffic_data returns correct data format when API call is successful."""
        # Mock API response for traffic data
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "count": 10,
            "uniques": 5,
            "views": [{"timestamp": "2024-10-01T00:00:00Z", "count": 10, "uniques": 5}],
        }
        mock_get.return_value = mock_response

        repos = ["fake_user/fake_repo"]
        traffic_data = fetch_traffic_data("fake_token", repos)
        expected_data = [
            {
                "Repository": "fake_user/fake_repo",
                "Total Views": 10,
                "Unique Visitors": 5,
                "View Timestamps": "2024-10-01T00:00:00Z (10 views)",
            }
        ]
        self.assertEqual(traffic_data, expected_data)

    @patch("gh_repo_traffic.plt.show")
    def test_display_traffic_data(self, mock_show):
        """Test that display_traffic_data runs without errors."""
        # Test data
        traffic_data = [
            {
                "Repository": "fake_user/fake_repo",
                "Total Views": 10,
                "Unique Visitors": 5,
                "View Timestamps": "2024-10-01T00:00:00Z (10 views)",
            }
        ]

        try:
            display_traffic_data(traffic_data, "fake_user")
            mock_show.assert_called_once()  # Ensure plot is shown
        except Exception as e:
            self.fail(f"display_traffic_data raised an exception: {e}")


if __name__ == "__main__":
    unittest.main(testRunner=ColoredTestRunner(verbosity=2))
    unittest.main(testRunner=XMLTestRunner(output="test-reports", verbosity=2))
