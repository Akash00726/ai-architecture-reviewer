import yaml
import os

DEFAULT_CONFIG = {
    "ai": {
        "provider": "openai",
        "model": "gpt-4o-mini",
        "temperature": 0.2
    },
    "risk": {
        "fail_on": "HIGH"
    },
    "output": {
        "format": "text"
    }
}


def load_config(config_file="arch-reviewer.yaml"):

    if not os.path.exists(config_file):
        return DEFAULT_CONFIG

    with open(config_file, "r") as f:
        user_config = yaml.safe_load(f)

    return merge(DEFAULT_CONFIG, user_config)


def merge(default, user):

    result = default.copy()

    for key, value in user.items():

        if isinstance(value, dict) and key in result:
            result[key] = merge(result[key], value)
        else:
            result[key] = value

    return result