
import ray
import os
import time
import socket
import random

# 1. Connect to your cluster
# Ensure port 10001 is open.
try:
    os.environ["RAY_ENABLE_WINDOWS_OR_OSX_CLUSTER"] = "1"
    ray.init(address="ray://localhost:10001")
    print("✅ Connected to Ray Cluster successfully!")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    exit(1)

# 2. Define a remote task
@ray.remote
def get_node_info(i):
    # Simulate a heavy task
    seconds = random.randint(1, 30)
    print(f"Task {i} start on node: {socket.gethostname()}")

    for j in range(seconds):
        print(f"process {i} iteration {j}")
        time.sleep(1)

    # print the hostname of the machine actually running the task
    print(f"Task {i} executed on node: {socket.gethostname()} return {seconds}")
    # return the seconds waiting
    return seconds


def run_test():
    num_tasks = 32
    print(f"\n🚀 Launching {num_tasks} parallel tasks...")

    start_time = time.time()

    # .remote() returns a 'Future' (Object Reference) immediately
    futures = [get_node_info.remote(i) for i in range(num_tasks)]

    # ray.get() blocks until all tasks are finished and retrieves results
    results = ray.get(futures)

    end_time = time.time()
    duration = end_time - start_time

    print(f"⏱️ Total time: {duration:.2f} seconds")
    print("-" * 30)

    total = 0
    print (f"All results: {results}")
    for res in results:
        total += res

    print(f"Suma total {total}")

if __name__ == "__main__":
    run_test()
    ray.shutdown()