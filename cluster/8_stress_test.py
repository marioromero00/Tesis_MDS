import ray
import os
import time

# 1. Enable Hybrid Cluster Flag
os.environ["RAY_ENABLE_WINDOWS_OR_OSX_CLUSTER"] = "1"
ray.init(address="ray://localhost:10001")


@ray.remote(num_cpus=1, num_gpus=1)
def high_load_task(duration=10, ram_gb=2):
    import torch
    import numpy as np
    import socket
    import time

    node = socket.gethostname()
    device = torch.device("mps")

    print(f"🔥 [START] Loading {node}: CPU, GPU, and ~{ram_gb}GB RAM...")

    # --- 1. RAM LOAD (Unified Memory) ---
    # We create several large tensors to eat up the RAM.
    # A float32 tensor of (16000, 16000) is approx 1GB.
    num_tensors = ram_gb
    tensors = []
    for i in range(num_tensors):
        # We move them to MPS (GPU Memory) which on Mac IS the System RAM
        tensors.append(torch.randn(3000, 3000, device=device))
        print(f"   {node}: Allocated tensor {i + 1}/{num_tensors}")

    # --- 2. CPU & GPU LOAD LOOP ---
    start_time = time.time()
    iterations = 0

    while time.time() - start_time < duration:
        # GPU Operation (Heavy Matrix Multi)
        # Using the tensors we just allocated to ensure we use the 'loaded' memory
        result_gpu = torch.matmul(tensors[0], tensors[1])
        torch.mps.synchronize()  # Force the GPU to finish before next loop

        # CPU Operation (Heavy NumPy Math)
        # This keeps one CPU core pinned at 100%
        cpu_work = np.random.normal(size=(8000, 8000))
        np.dot(cpu_work, cpu_work)

        iterations += 1

    # Cleanup
    del tensors
    del result_gpu

    return f"✅ {node} Stress Test Finished ({iterations} cycles completed)."


# 2. Dispatch to all 4 Mac Minis
# Adjust ram_gb=6 or higher if your Mac Minis have 16GB+ RAM.
# BE CAREFUL: Setting this too high for your hardware will cause a "kernel panic" or crash.
print("📡 Pushing Cluster to the limit for 30 seconds...")

# Change ram_gb to match your Mac Mini's capacity (e.g., 4, 8, or 12)
load_futures = [high_load_task.remote(duration=10, ram_gb=1) for _ in range(4)]

# 3. Collect Results
results = ray.get(load_futures)
for r in results:
    print(r)