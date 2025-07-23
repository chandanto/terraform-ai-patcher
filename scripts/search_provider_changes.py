import requests
import json

def search_duckduckgo(query):
    # Using DuckDuckGo instant answer API
    url = f"https://api.duckduckgo.com/?q={query}&format=json&no_redirect=1&skip_disambig=1"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch DuckDuckGo results for {query}")
        return None
    data = response.json()
    return data

def fetch_aws_provider_changelog(latest_version):
    query = f"Terraform AWS provider {latest_version} changelog"
    data = search_duckduckgo(query)
    if not data:
        return None
    # Simple heuristic: grab abstract text if available
    changelog_text = data.get("AbstractText", "")
    if changelog_text:
        print(f"Changelog snippet found: {changelog_text[:300]}...")
        with open("provider_changelog.txt", "w") as f:
            f.write(changelog_text)
    else:
        print("No changelog snippet found in DuckDuckGo abstract.")
    return changelog_text

if __name__ == "__main__":
    try:
        with open("latest_versions.json") as f:
            versions = json.load(f)
        aws_version = versions.get("aws_provider", "")
        if aws_version:
            fetch_aws_provider_changelog(aws_version)
        else:
            print("AWS provider version not found.")
    except FileNotFoundError:
        print("latest_versions.json not found. Run fetch_latest_versions.py first.")
