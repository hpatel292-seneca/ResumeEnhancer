import subprocess


def lint():
    """Run linting using flake8."""
    print("Running lint checks...")
    subprocess.run(["flake8", "."])


def format():
    """Run code formatting using black."""
    print("Running code formatting...")
    subprocess.run(["black", "."])
