import ray
import os
import time

# 1. Enable Hybrid Cluster Flag
os.environ["RAY_ENABLE_WINDOWS_OR_OSX_CLUSTER"] = "1"
ray.init(address="ray://localhost:10001")


# We define a smaller task that uses 1 CPU.
# We don't set num_gpus=1 here because we want multiple tasks to share the GPU.
@ray.remote(num_cpus=1)
def max_out_core(duration=10):
    import torch
    import numpy as np
    import socket
    import time

    node = socket.gethostname()
    device = torch.device("mps")

    # 1. Allocate a smaller slice of RAM (approx 500MB per core = 4GB total per Mac)
    # Adjust this if you have 16GB+ RAM Mac Minis
    memory_hog = torch.randn(8000, 8000, device=device)

    start_time = time.time()
    while time.time() - start_time < duration:
        # GPU Stress (All 8 cores on the node will be hitting the same GPU)
        _ = torch.matmul(memory_hog[:1000, :1000], memory_hog[:1000, :1000])
        torch.mps.synchronize()

        # CPU Stress (Heavy math to pin the core)
        cpu_work = np.random.normal(size=(4000, 4000))
        np.dot(cpu_work, cpu_work)

    return f"✅ Core on {node} finished."


# 2. Dispatch 8 tasks per Mac Mini (4 Macs * 8 Cores = 32 Tasks)
print("📡 Dispatching 32 tasks to saturate 4 Mac Minis (8 cores each)...")

# We create a list of 32 "futures"
futures = [max_out_core.remote(duration=10) for _ in range(32)]

# 3. Watch the fireworks
print("🔥 All cores should be at 100% now. Check Activity Monitor!")
results = ray.get(futures)

print(f"✅ Completed {len(results)} core-tasks across the cluster.")