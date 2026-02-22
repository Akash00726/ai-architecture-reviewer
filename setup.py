from setuptools import setup, find_packages

setup(
    name="arch-reviewer",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "openai",
        "google-generativeai",
        "click",
        "python-dotenv",
        "pyyaml"
    ],
    entry_points={
        "console_scripts": [
            "arch-reviewer=arch_reviewer.cli:cli"
        ]
    },
)