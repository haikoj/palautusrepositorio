#!/usr/bin/env python3
"""Simple test runner to verify all tests pass"""
import subprocess
import sys

def main():
    print("Running tests...")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
        cwd="/home/haikoj/palautusrepositorio/viikko7/kivi-paperi-sakset",
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    print(f"\nExit code: {result.returncode}")
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())
