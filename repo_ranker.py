import requests
from datetime import datetime, timedelta

def calculate_repo_rank(owner, repo):
    """Calculates a simplified RepoRank score based on stars, forks, and recent activity."""
    try:
        # Fetch repository data
        repo_url = f"https://api.github.com/repos/{owner}/{repo}"
        repo_response = requests.get(repo_url)
        repo_data = repo_response.json()

        if 'message' in repo_data and repo_data['message'] == 'Not Found':
            return {"error": "Repository not found"}

        stars = repo_data.get('stargazers_count', 0)
        forks = repo_data.get('forks_count', 0)

        # Fetch recent commit activity
        commits_url = f"https://api.github.com/repos/{owner}/{repo}/commits?since={(datetime.now() - timedelta(days=30)).isoformat()}Z&per_page=1"
        commits_response = requests.get(commits_url)
        commit_data = commits_response.json()

        # Count commits in the last 30 days (simplified: count of recent commits returned)
        # A more robust solution would paginate and count precisely.
        recent_commits_count = len(commit_data)
        if commits_response.headers.get('Link'):
            # If there are more commits, assume higher activity
            recent_commits_count = 100 # Placeholder for significant activity

        # Simple scoring: stars + forks + (recent_commits * weight)
        # Weights can be adjusted based on desired emphasis.
        score = stars + forks + (recent_commits_count * 2)

        return {
            "owner": owner,
            "repo": repo,
            "stars": stars,
            "forks": forks,
            "recent_commits_30d": recent_commits_count,
            "repo_rank_score": score
        }

    except requests.exceptions.RequestException as e:
        return {"error": f"Network or API error: {e}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}

if __name__ == "__main__":
    # Example usage:
    # Replace with actual GitHub owner and repository names
    owner_name = "octocat"
    repo_name = "Spoon-Knife"

    rank_info = calculate_repo_rank(owner_name, repo_name)

    if "error" in rank_info:
        print(f"Error calculating rank for {owner_name}/{repo_name}: {rank_info['error']}")
    else:
        print(f"--- RepoRank Metrics for {rank_info['owner']}/{rank_info['repo']} ---")
        print(f"Stars: {rank_info['stars']}")
        print(f"Forks: {rank_info['forks']}")
        print(f"Recent Commits (last 30 days): {rank_info['recent_commits_30d']}")
        print(f"Calculated RepoRank Score: {rank_info['repo_rank_score']}")
