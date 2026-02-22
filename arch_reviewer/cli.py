import click
import sys
from .analyzer import review_file
from .config import load_config

config = load_config()

THRESHOLD = config["risk"]["fail_on"].upper()

RISK_LEVELS = {
    "LOW": 1,
    "MEDIUM": 2,
    "HIGH": 3,
    "CRITICAL": 4
}


@click.group()
def cli():
    pass


@click.command()
@click.argument("file")
def review(file):

    print(f"\nScanning: {file}")

    result, detected_risk = review_file(file)

    print("\n--- AI Architecture Review ---\n")

    print(result)

    detected_risk = detected_risk.upper()

    detected_level = RISK_LEVELS.get(detected_risk, 0)
    threshold_level = RISK_LEVELS.get(THRESHOLD, 0)

    print(f"\nDetected Risk: {detected_risk}")
    print(f"Fail Threshold: {THRESHOLD}")

    if detected_level >= threshold_level:

        print("\nResult: FAILED")
        sys.exit(1)

    print("\nResult: PASSED")
    sys.exit(0)


cli.add_command(review)

if __name__ == "__main__":
    cli()