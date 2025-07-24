import requests
import json
import os
import re

def get_latest_terraform_version():
    url = "https://releases.hashicorp.com/terraform/index.json"
    response = requests.get(url)
    data = response.json()
    versions = list(data["versions"].keys())

    # Filter only valid semantic versions: "X.Y.Z" where X, Y, Z are integers
    semver_versions = [
        v for v in versions
        if re.fullmatch(r"\d+\.\d+\.\d+", v)
    ]
    # Sort semver versions
    latest_version = sorted(
        semver_versions,
        key=lambda s: list(map(int, s.split('.')))
    )[-1]

    return latest_version

def get_latest_aws_provider_version():
    # Use Terraform registry API for AWS provider
    url = "https://registry.terraform.io/v1/providers/hashicorp/aws/versions"
    response = requests.get(url)
    data = response.json()
    versions = [v["version"] for v in data["versions"]]
    versions = [v for v in versions if "rc" not in v and "beta" not in v]
    latest_version = sorted(versions, key=lambda s: list(map(int, s.split('.'))))[-1]
    return latest_version

def save_versions(terraform_version, aws_provider_version):
    with open("latest_versions.json", "w") as f:
        json.dump({
            "terraform": terraform_version,
            "aws_provider": aws_provider_version
        }, f, indent=2)

if __name__ == "__main__":
    terraform_version = get_latest_terraform_version()
    aws_provider_version = get_latest_aws_provider_version()
    print(f"Latest Terraform version: {terraform_version}")
    print(f"Latest AWS provider version: {aws_provider_version}")
    save_versions(terraform_version, aws_provider_version)
