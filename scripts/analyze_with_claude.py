import subprocess
import json
import os
import boto3

# AWS Bedrock client setup
bedrock = boto3.client('bedrock-runtime')

def run_terraform_plan():
    """Run terraform plan and capture output."""
    result = subprocess.run(
        ["terraform", "plan", "-no-color"],
        capture_output=True,
        text=True
    )
    return result.stdout, result.returncode

def call_claude(prompt):
    """Call Claude model via AWS Bedrock."""
    response = bedrock.invoke_model(
        modelId='anthropic.claude-v1',
        contentType='application/json',
        accept='application/json',
        body=json.dumps({"prompt": prompt, "max_tokens_to_sample": 1000})
    )
    body = response['body'].read()
    result = json.loads(body)
    return result.get('completion', '')

def build_prompt(terraform_plan_output, provider_changelog):
    prompt = f"""
You are an expert Terraform developer.

Here is the output of 'terraform plan':

{terraform_plan_output}

Here is the AWS provider changelog:

{provider_changelog}

Please analyze the plan output and changelog, and suggest if any Terraform module patches are needed.
If yes, provide the HCL patch snippets and explanation.
If no patch needed, say so.
"""
    return prompt

def save_analysis(analysis_text):
    with open("claude_analysis.txt", "w") as f:
        f.write(analysis_text)

if __name__ == "__main__":
    plan_output, code = run_terraform_plan()
    if code != 0:
        print("Terraform plan reported errors, analyzing with Claude...")
    else:
        print("Terraform plan succeeded, analyzing for potential improvements...")
    try:
        with open("provider_changelog.txt") as f:
            changelog = f.read()
    except FileNotFoundError:
        changelog = "No changelog found."

    prompt = build_prompt(plan_output, changelog)
    print("Sending prompt to Claude AI...")
    analysis = call_claude(prompt)
    print("Received analysis from Claude AI:")
    print(analysis)

    save_analysis(analysis)
