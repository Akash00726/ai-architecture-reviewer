from .ai_engine import generate_review
import re
import json


def review_file(file_path):

    if file_path.endswith(".json"):
        content = parse_tfplan(file_path)
    else:
        with open(file_path, "r") as f:
            content = f.read()

    result = generate_review(content)

    risk_score = extract_risk_score(result)

    return result, risk_score


def parse_tfplan(file_path):

    try:

        with open(file_path, "r") as f:
            plan = json.load(f)

        resources = []

        for change in plan.get("resource_changes", []):

            resource_type = change.get("type")
            name = change.get("name")

            after = change.get("change", {}).get("after", {})

            resources.append({
                "type": resource_type,
                "name": name,
                "config": after
            })

        return f"""
Terraform plan resources:

{json.dumps(resources, indent=2)}

Perform security review.
"""

    except Exception as e:

        return f"Error parsing Terraform plan: {str(e)}"


def extract_risk_score(output):

    match = re.search(
        r"Risk Score:\s*(LOW|MEDIUM|HIGH|CRITICAL)",
        output,
        re.IGNORECASE
    )

    if match:
        return match.group(1).upper()

    return "UNKNOWN"