import ray
import os

##os.environ["RAY_ENABLE_WINDOWS_OR_OSX_CLUSTER"] = "1"
ray.init(address="ray://localhost:10001")


@ray.remote(num_gpus=1)
def stress_test_mps(duration=30):
    import torch
    import socket
    import time

    node_name = socket.gethostname()
    device = torch.device("mps")

    # Create large matrices for the GPU to chew on
    # 4000x4000 is usually enough to see a clear spike in Activity Monitor
    size = 4000
    a = torch.randn(size, size, device=device)
    b = torch.randn(size, size, device=device)

    print(f"🔥 Starting {duration}s stress test on {node_name}...")

    start_time = time.time()
    count = 0

    # Loop matrix multiplication for the specified duration
    while time.time() - start_time < duration:
        # Perform operation
        c = torch.matmul(a, b)
        # Force a sync so the GPU doesn't just 'queue' operations
        torch.mps.synchronize()
        count += 1

    return f"✅ {node_name} completed {count} iterations on Metal GPU."


# 2. Launch on all 4 Macs simultaneously
print("📡 Dispatching 10-second load to all 4 Mac Minis...")
futures = [stress_test_mps.remote(10) for _ in range(4)]

# 3. Monitor results
results = ray.get(futures)
for r in results:
    print(r)