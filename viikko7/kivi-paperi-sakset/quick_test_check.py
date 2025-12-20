"""
Quick verification that pytest works and tests can be discovered
"""
import subprocess
import sys
import os

os.chdir('/home/haikoj/palautusrepositorio/viikko7/kivi-paperi-sakset')

print("=" * 60)
print("PYTEST VERIFICATION")
print("=" * 60)

# Check pytest is available
try:
    result = subprocess.run(
        [sys.executable, '-m', 'pytest', '--version'],
        capture_output=True,
        text=True,
        timeout=5
    )
    print(f"\n✓ Pytest version: {result.stdout.strip()}")
except Exception as e:
    print(f"\n✗ Error checking pytest: {e}")
    sys.exit(1)

# Collect tests
print("\n" + "=" * 60)
print("COLLECTING TESTS")
print("=" * 60)

try:
    result = subprocess.run(
        [sys.executable, '-m', 'pytest', 'tests/', '--collect-only', '-q'],
        capture_output=True,
        text=True,
        timeout=10
    )
    print(result.stdout)
    
    # Count tests
    lines = result.stdout.split('\n')
    test_count = sum(1 for line in lines if '::test_' in line)
    print(f"\n✓ Total tests discovered: {test_count}")
except Exception as e:
    print(f"\n✗ Error collecting tests: {e}")

# Run tests
print("\n" + "=" * 60)
print("RUNNING TESTS")
print("=" * 60)

try:
    result = subprocess.run(
        [sys.executable, '-m', 'pytest', 'tests/', '-v', '--tb=no'],
        capture_output=True,
        text=True,
        timeout=60
    )
    
    # Show summary
    lines = result.stdout.split('\n')
    for line in lines[-20:]:  # Last 20 lines usually have summary
        print(line)
    
    print(f"\n✓ Exit code: {result.returncode}")
    
    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ SOME TESTS FAILED")
        print("=" * 60)
        print("\nFull output:")
        print(result.stdout)
        if result.stderr:
            print("\nErrors:")
            print(result.stderr)
            
except Exception as e:
    print(f"\n✗ Error running tests: {e}")
    sys.exit(1)
