#!/usr/bin/env python3
"""Install packages listed in requirements.txt."""
import subprocess
from pathlib import Path
import sys


def main() -> None:
    reqs = Path(__file__).resolve().parent / "requirements.txt"
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(reqs)])


if __name__ == "__main__":
    main()
