import requests
from datetime import date, timedelta


TOP_SIZE = 20


def get_trending_repositories(top_size):
    week_ago_date = date.today() - timedelta(days=7)
    payload = {'q': 'created:>{}' .format(week_ago_date), 'sort': 'stars'}
    sorted_repositories = requests.get('https://api.github.com/search/repositories', params=payload)
    return sorted_repositories.json()['items'][:top_size]


def get_open_issues_links(repo_owner, repo_name):
    all_issues = requests.get('http://api.github.com/repos/{0}/{1}/issues' .format(repo_owner, repo_name))
    issues_links = [issue['html_url'] for issue in all_issues.json()]
    return issues_links


def print_beauty(owner_name, repo_name, stars, issues_quantity, issues_links):
    print('{owner}\'s repository {repo_name} has {stars_q} stars and {iss_q} open issues.\nLinks to issues:' \
          .format(owner=owner_name, repo_name=repo_name, stars_q=stars, iss_q=issues_quantity))
    for link in issues_links:
        print(link)
    print()

if __name__ == '__main__':
    trending_repo_sorted = get_trending_repositories(TOP_SIZE)
    for item in trending_repo_sorted:
        issues_links = get_open_issues_links(item['owner']['login'], item['name'])
        print_beauty(item['owner']['login'], item['name'], \
                    item['stargazers_count'], len(issues_links), issues_links)