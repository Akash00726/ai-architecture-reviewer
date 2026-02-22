import click
import sys
from .analyzer import review_file
from .config import load_config

# Load config
config = load_config()

# Risk hierarchy
RISK_LEVELS = {
    "LOW": 1,
    "MEDIUM": 2,
    "HIGH": 3,
    "CRITICAL": 4
}


@click.group()
def cli():
    """AI Architecture Reviewer CLI"""
    pass


@click.command()
@click.argument("file")
@click.option(
    "--audit-only",
    is_flag=True,
    help="Audit mode: never fail pipeline regardless of risk score"
)
@click.option(
    "--config-file",
    default="arch-reviewer.yaml",
    help="Path to config file (default: arch-reviewer.yaml)"
)
def review(file, audit_only, config_file):
    """
    Review architecture, Terraform plan, or document.
    """

    # Reload config (supports custom config file)
    cfg = load_config(config_file)

    threshold = cfg.get("risk", {}).get("fail_on", "HIGH").upper()
    enforce_config = cfg.get("risk", {}).get("enforce", True)

    # CLI flag overrides config
    enforce = False if audit_only else enforce_config

    print(f"\nScanning: {file}")

    result, detected_risk = review_file(file)

    print("\n--- AI Architecture Review ---\n")
    print(result)

    detected_risk = detected_risk.upper()

    detected_level = RISK_LEVELS.get(detected_risk, 0)
    threshold_level = RISK_LEVELS.get(threshold, 0)

    print(f"\nDetected Risk: {detected_risk}")
    print(f"Threshold: {threshold}")
    print(f"Mode: {'ENFORCE' if enforce else 'AUDIT'}")

    # Enforcement logic
    if enforce and detected_level >= threshold_level:

        print("\nResult: FAILED (Risk >= Threshold)")
        sys.exit(1)

    elif not enforce:

        print("\nResult: AUDIT ONLY (No pipeline failure)")
        sys.exit(0)

    else:

        print("\nResult: PASSED")
        sys.exit(0)


# Register command
cli.add_command(review)


if __name__ == "__main__":
    cli()