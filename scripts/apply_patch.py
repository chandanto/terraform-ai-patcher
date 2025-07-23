import re
import os

MODULE_PATH = "terraform-modules/datadog"
ANALYSIS_FILE = "claude_analysis.txt"

def extract_patches(analysis_text):
    """
    Very simple heuristic parser to extract HCL snippets from analysis text.
    Assumes AI output code snippets are between ```hcl ... ```
    """
    patches = re.findall(r"```hcl(.*?)```", analysis_text, re.DOTALL)
    return patches

def apply_patches_to_module(patches):
    main_tf_path = os.path.join(MODULE_PATH, "main.tf")
    if not os.path.exists(main_tf_path):
        print(f"{main_tf_path} not found.")
        return False

    with open(main_tf_path, "r") as f:
        content = f.read()

    for patch in patches:
        patch = patch.strip()
        # For demo: append patch at end of main.tf if not already present
        if patch not in content:
            print(f"Applying patch:\n{patch}\n")
            content += "\n\n# AI Patch Start\n" + patch + "\n# AI Patch End\n"

    with open(main_tf_path, "w") as f:
        f.write(content)

    return True

if __name__ == "__main__":
    if not os.path.exists(ANALYSIS_FILE):
        print(f"{ANALYSIS_FILE} not found, run analyze_with_claude.py first.")
        exit(1)

    with open(ANALYSIS_FILE) as f:
        analysis = f.read()

    patches = extract_patches(analysis)
    if not patches:
        print("No HCL patches found in analysis.")
        exit(0)

    success = apply_patches_to_module(patches)
    if success:
        print("Patches applied successfully.")
    else:
        print("Failed to apply patches.")
