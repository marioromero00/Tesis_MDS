import sys
import os

# Get major and minor versions
major = sys.version_info.major
minor = sys.version_info.minor
full_version = sys.version.split()[0]

print(f"🔍 Current Colab Python: {full_version}")

if major == 3 and minor == 12:
    print("✅ SUCCESS: You are on Python 3.12.x. This matches your cluster.")
else:
    print(f"❌ MISMATCH: You are on {full_version}. Your cluster needs 3.12.x.")

# Optional: Also check Ray while we're at it
try:
    import ray
    print(f"📦 Ray version: {ray.__version__}")
    if ray.__version__ != "2.51.1":
        print(f"⚠️ Warning: Ray is {ray.__version__}, but your is 2.51.1. Run: !pip install ray==2.51.1")
except ImportError:
    print("📦 Ray is not installed yet.")