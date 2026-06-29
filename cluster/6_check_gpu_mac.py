import ray
import os

os.environ["RAY_ENABLE_WINDOWS_OR_OSX_CLUSTER"] = "1"
ray.init(address="ray://localhost:10001")


@ray.remote(num_gpus=1)
def diagnostic_mac_gpu():
    import torch
    import socket
    import platform

    # 1. Check if we are actually on a Mac
    is_mac = platform.system() == "Darwin"

    # 2. Check the specific MPS flags
    # In Torch 2.x+, these are the two main ways to check
    built = torch.backends.mps.is_built()
    available = torch.backends.mps.is_available()

    error_msg = ""
    device_info = "Not Detected"

    if available:
        try:
            # 3. Try to physically move a tensor to the GPU
            device = torch.device("mps")
            x = torch.ones(1, device=device)
            device_info = f"Apple Silicon GPU (Metal) - Active"
        except Exception as e:
            error_msg = str(e)
            device_info = "Detection Failed at Runtime"
    else:
        # Check why it's not available
        if not built:
            device_info = "Torch not compiled with MPS support"
        else:
            device_info = "Hardware/OS mismatch (Check macOS version)"

    return {
        "node": socket.gethostname(),
        "os": platform.mac_ver()[0],
        "mps_built": built,
        "mps_available": available,
        "status": device_info,
        "error": error_msg
    }


print("🔍 Running Deep Diagnostic on 4 Mac Minis...")
results = ray.get([diagnostic_mac_gpu.remote() for _ in range(4)])

for r in results:
    print(f"\n🖥️  Node: {r['node']} (macOS {r['os']})")
    print(f"   • Status:      {r['status']}")
    print(f"   • Built/Avail: {r['mps_built']} / {r['mps_available']}")
    if r['error']:
        print(f"   • Error:       {r['error']}")